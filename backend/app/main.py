from __future__ import annotations

import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Any

import aioice.stun
from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceCandidate, RTCIceServer, RTCSessionDescription
from aiortc.sdp import candidate_from_sdp
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from backend.core.config import AppConfig, load_config
from backend.core.session import RemoteRenderSession, SessionManager
from backend.transport.video_track import LatestFrameVideoTrack

BASE_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = BASE_DIR / "web"
config: AppConfig = load_config()
app = FastAPI(title="VisIVO Connect", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

sessions = SessionManager(max_sessions=config.max_sessions, idle_timeout_s=config.idle_timeout_s)
cleanup_task = None
log = logging.getLogger("uvicorn.error")


def _install_aioice_retry_guard() -> None:
    """Avoid noisy asyncio callback crashes when STUN retries outlive closed transports.

    Seen on Python 3.11 + aioice where Transaction.__retry may run after underlying
    DatagramTransport / loop internals are already torn down, raising:
    - AttributeError: 'NoneType' object has no attribute 'sendto'
    - AttributeError: 'NoneType' object has no attribute 'call_exception_handler'
    """

    transaction_cls = aioice.stun.Transaction
    original = getattr(transaction_cls, "_Transaction__retry", None)
    if not callable(original) or getattr(transaction_cls, "_visivo_retry_guard_installed", False):
        return

    def _safe_retry(self: aioice.stun.Transaction) -> None:  # type: ignore[name-defined]
        try:
            original(self)
        except AttributeError as exc:
            message = str(exc)
            if "sendto" not in message and "call_exception_handler" not in message:
                raise
            future = getattr(self, "_Transaction__future", None)
            if future is not None and not future.done():
                future.set_exception(aioice.stun.TransactionTimeout())
        except RuntimeError as exc:
            # Defensive path for late callbacks on a closed event loop.
            if "Event loop is closed" not in str(exc):
                raise
            future = getattr(self, "_Transaction__future", None)
            if future is not None and not future.done():
                future.set_exception(aioice.stun.TransactionTimeout())

    setattr(transaction_cls, "_Transaction__retry", _safe_retry)
    setattr(transaction_cls, "_visivo_retry_guard_installed", True)
    log.warning("Installed aioice retry guard for late STUN callbacks")


def _is_authorized(token: str | None, expected: str | None) -> bool:
    if not expected:
        return True
    return bool(token) and token == expected


def _pc_config_from_env() -> RTCConfiguration:
    servers = [
        RTCIceServer(
            urls=entry["urls"],
            username=entry.get("username"),
            credential=entry.get("credential"),
        )
        for entry in config.ice_servers
    ]
    return RTCConfiguration(iceServers=servers)


def _prefer_safari_friendly_video_codecs(pc: RTCPeerConnection) -> None:
    """Prefer H264 in the server offer for better Safari interoperability."""
    try:
        # Imported lazily to avoid hard dependency on internals during startup.
        from aiortc import RTCRtpSender  # type: ignore

        capabilities = RTCRtpSender.getCapabilities("video")
        codecs = list(getattr(capabilities, "codecs", []) or [])
        if not codecs:
            return

        def _codec_rank(codec: Any) -> tuple[int, int, int]:
            mime = str(getattr(codec, "mimeType", "")).lower()
            params = getattr(codec, "parameters", {}) or {}
            if "h264" in mime:
                packetization_mode = str(params.get("packetization-mode", "0"))
                profile_level_id = str(params.get("profile-level-id", "")).lower()
                baseline_like = profile_level_id.startswith(("42", "4d", "58"))
                return (0, 0 if packetization_mode == "1" else 1, 0 if baseline_like else 1)
            if "vp8" in mime:
                return (1, 0, 0)
            if "vp9" in mime:
                return (2, 0, 0)
            if "av1" in mime:
                return (3, 0, 0)
            if "rtx" in mime:
                return (8, 0, 0)
            return (5, 0, 0)

        ordered = sorted(codecs, key=_codec_rank)
        applied = False
        for transceiver in pc.getTransceivers():
            if getattr(transceiver, "kind", None) != "video":
                continue
            if hasattr(transceiver, "setCodecPreferences"):
                transceiver.setCodecPreferences(ordered)
                applied = True
        if applied:
            names = [str(getattr(codec, "mimeType", "unknown")) for codec in ordered]
            log.warning("Applied video codec preference (H264-first): %s", names)
    except Exception:
        log.exception("Failed to apply Safari-friendly video codec preference")


def _normalize_description(payload: dict[str, Any]) -> RTCSessionDescription | None:
    if "sdp" in payload and isinstance(payload["sdp"], dict):
        inner = payload["sdp"]
        if inner.get("type") and inner.get("sdp"):
            return RTCSessionDescription(sdp=inner["sdp"], type=inner["type"])
    if payload.get("description") and isinstance(payload["description"], dict):
        inner = payload["description"]
        if inner.get("type") and inner.get("sdp"):
            return RTCSessionDescription(sdp=inner["sdp"], type=inner["type"])
    if payload.get("type") in {"offer", "answer"} and payload.get("sdp"):
        return RTCSessionDescription(sdp=payload["sdp"], type=payload["type"])
    return None


def _normalize_candidate(payload: dict[str, Any]) -> RTCIceCandidate | None:
    cand = payload.get("candidate", payload)
    if isinstance(cand, dict):
        candidate_str = cand.get("candidate")
        sdp_mid = cand.get("sdpMid")
        sdp_mline = cand.get("sdpMLineIndex")
        if candidate_str is not None:
            parsed = candidate_from_sdp(candidate_str)
            parsed.sdpMid = sdp_mid
            parsed.sdpMLineIndex = int(sdp_mline) if sdp_mline is not None else 0
            return parsed
    return None


async def _emit_state(ws: WebSocket, session: RemoteRenderSession, text: str | None = None) -> None:
    await ws.send_json(session.state_payload(text=text))


async def _attach_peer_connection(session: RemoteRenderSession, ws: WebSocket) -> RTCPeerConnection:
    if session.peer_connection is not None:
        await session.peer_connection.close()

    pc = RTCPeerConnection(_pc_config_from_env())
    session.peer_connection = pc

    video_track = LatestFrameVideoTrack(session)
    pc.addTrack(video_track)
    _prefer_safari_friendly_video_codecs(pc)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange() -> None:
        log.warning("PeerConnection state=%s session=%s", pc.connectionState, session.session_id)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange() -> None:
        log.warning("ICE state=%s session=%s", pc.iceConnectionState, session.session_id)

    @pc.on("icecandidate")
    async def on_icecandidate(candidate: RTCIceCandidate | None) -> None:
        if candidate is None:
            return
        log.warning(
            "Local ICE candidate type=%s protocol=%s session=%s",
            getattr(candidate, "type", "unknown"),
            getattr(candidate, "protocol", "unknown"),
            session.session_id,
        )
        await ws.send_json(
            {
                "type": "ice",
                "candidate": {
                    "candidate": candidate.candidate,
                    "sdpMid": candidate.sdpMid,
                    "sdpMLineIndex": candidate.sdpMLineIndex,
                },
            }
        )

    offer = await pc.createOffer()
    await pc.setLocalDescription(offer)
    await ws.send_json(
        {
            "type": "offer",
            "description": {"type": offer.type, "sdp": offer.sdp},
            "iceServers": config.ice_servers,
        }
    )
    return pc


@app.get("/")
async def index() -> Response:
    if not WEB_DIR.exists():
        return JSONResponse({"error": "web directory not found"}, status_code=404)
    return FileResponse(WEB_DIR / "index.html")


@app.get("/healthz")
async def healthz() -> JSONResponse:
    return JSONResponse({"status": "ok"})


@app.get("/api/metrics/{session_id}")
async def session_metrics(session_id: str, request: Request) -> JSONResponse:
    metrics_token = request.query_params.get("token")
    if not _is_authorized(metrics_token, config.metrics_auth_token):
        return JSONResponse({"error": "unauthorized"}, status_code=401)
    session = await sessions.get(session_id)
    if session is None:
        return JSONResponse({"error": "session not found"}, status_code=404)
    return JSONResponse(
        {
            "sessionId": session.session_id,
            "datasetPath": getattr(session.renderer, "dataset_path", None),
            "datasetName": (
                Path(getattr(session.renderer, "dataset_path", "")).name
                if getattr(session.renderer, "dataset_path", None)
                else None
            ),
            "mode": session.mode,
            "visualizationMode": session.visualization.mode,
            "isoValue": session.visualization.iso_value,
            "volume": dict(session.visualization.volume_params),
            "samples": {
                "renderTimeMs": session.stats.render_time_ms,
                "encodeTimeMs": session.stats.encode_time_ms,
                "networkLatencyMs": session.stats.network_latency_ms,
                "frameDeliveryLatencyMs": session.stats.frame_delivery_latency_ms,
                "inputToVisibleLatencyMs": session.stats.input_to_visible_latency_ms,
            },
            "counts": {
                "deliveredFrames": session.stats.delivered_frames,
                "droppedFrames": session.stats.dropped_frames,
            },
            "importMetrics": (
                {
                    "fitsOpenMs": session.import_metrics.fits_open_ms,
                    "hduSelectMs": session.import_metrics.hdu_select_ms,
                    "sanitizeConvertMs": session.import_metrics.sanitize_convert_ms,
                    "vtkBuildMs": session.import_metrics.vtk_build_ms,
                    "fitsTotalMs": session.import_metrics.fits_total_ms,
                }
                if session.import_metrics
                else None
            ),
            "runtimeMetrics": {
                "firstFrameLatencyMs": session.runtime_metrics.first_frame_latency_ms,
                "highQualityRenderTimeMs": session.runtime_metrics.high_quality_render_time_ms,
                "interactiveFps": session.runtime_metrics.interactive_fps,
                "memoryRssMb": session.runtime_metrics.memory_rss_mb,
            },
        }
    )


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    session: RemoteRenderSession | None = None
    token = ws.query_params.get("token")
    if config.auth_token and token and token != config.auth_token:
        await ws.send_json({"type": "error", "message": "unauthorized"})
        await ws.close(code=4401)
        return

    try:
        while True:
            raw = await ws.receive_text()
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                await ws.send_json({"type": "error", "message": "invalid json"})
                continue

            msg_type = payload.get("type")

            if msg_type == "hello":
                requested_session_id = payload.get("sessionId")
                dataset_path = payload.get("datasetPath") or config.dataset_path
                msg_token = payload.get("token")
                if config.auth_token and not (msg_token == config.auth_token or token == config.auth_token):
                    await ws.send_json({"type": "error", "message": "unauthorized"})
                    await ws.close(code=4401)
                    return
                session = await sessions.get_or_create(requested_session_id, dataset_path=dataset_path)
                session.control_ws = ws
                viewport = payload.get("viewport") or {}
                session.resize(
                    width=int(viewport.get("width", 1280)),
                    height=int(viewport.get("height", 720)),
                    dpr=float(viewport.get("dpr", 1.0)),
                )
                await _attach_peer_connection(session, ws)
                await ws.send_json({"type": "stream-ready", "sessionId": session.session_id})
                await _emit_state(ws, session, text="Session connected")
                continue

            if session is None:
                await ws.send_json({"type": "error", "message": "send hello first"})
                continue

            if msg_type in {"answer", "webrtc.answer"}:
                description = _normalize_description(payload)
                if description and session.peer_connection:
                    await session.peer_connection.setRemoteDescription(description)
                continue

            if msg_type in {"ice", "ice-candidate", "webrtc.ice"}:
                candidate = _normalize_candidate(payload)
                if candidate and session.peer_connection:
                    log.warning(
                        "Remote ICE candidate type=%s protocol=%s session=%s",
                        getattr(candidate, "type", "unknown"),
                        getattr(candidate, "protocol", "unknown"),
                        session.session_id,
                    )
                    await session.peer_connection.addIceCandidate(candidate)
                continue

            if msg_type == "resize":
                viewport = payload.get("viewport", {})
                session.resize(
                    width=int(viewport.get("width", session.viewport.width)),
                    height=int(viewport.get("height", session.viewport.height)),
                    dpr=float(viewport.get("dpr", session.viewport.dpr)),
                )
                continue

            if msg_type == "interaction.start":
                session.begin_interaction()
                await _emit_state(ws, session)
                continue

            if msg_type == "interaction.end":
                session.end_interaction()
                await _emit_state(ws, session)
                continue

            if msg_type == "camera.pointer":
                session.apply_pointer(payload)
                continue

            if msg_type == "camera.wheel":
                session.apply_wheel(payload)
                continue

            if msg_type == "camera.pinch":
                session.apply_pinch(payload)
                continue

            if msg_type in {"render.mode", "visualization.mode", "visualization.switch"}:
                requested_mode = payload.get("mode")
                if requested_mode is None:
                    requested_mode = payload.get("visualizationMode")
                if isinstance(requested_mode, str):
                    normalized = requested_mode.strip().lower().replace("_", "-")
                    if normalized in {"interactive", "high-quality"}:
                        session.set_mode(normalized)
                    else:
                        session.set_visualization_mode(requested_mode)
                await _emit_state(ws, session)
                continue

            if msg_type in {"render.params", "visualization.params", "visualization.update"}:
                session.set_render_params(payload)
                await _emit_state(ws, session)
                continue

            if msg_type == "control-input":
                sent_at = payload.get("sentAt")
                if isinstance(sent_at, (int, float)):
                    rtt_ms = max(0.0, float(time.time_ns() / 1e6 - sent_at))
                    session.stats.add_sample(session.stats.network_latency_ms, rtt_ms)
                await ws.send_json({"type": "control-ack", "id": payload.get("id"), "sequence": payload.get("sequence")})
                continue

            if msg_type == "ping":
                ts = payload.get("ts")
                if isinstance(ts, (int, float)):
                    rtt_ms = max(0.0, float(time.time_ns() / 1e6 - ts))
                    session.stats.add_sample(session.stats.network_latency_ms, rtt_ms)
                await ws.send_json({"type": "pong", "ts": ts})
                continue

            await ws.send_json({"type": "error", "message": f"unsupported message type: {msg_type}"})

    except WebSocketDisconnect:
        pass
    finally:
        if session:
            await sessions.close(session.session_id)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    global cleanup_task
    if cleanup_task:
        cleanup_task.cancel()
    await sessions.close_all()


@app.on_event("startup")
async def on_startup() -> None:
    global cleanup_task
    _install_aioice_retry_guard()

    async def _cleanup_loop() -> None:
        while True:
            await sessions.cleanup_idle()
            await asyncio.sleep(30)

    cleanup_task = asyncio.create_task(_cleanup_loop())
