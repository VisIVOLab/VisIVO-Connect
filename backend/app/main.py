from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import time
from pathlib import Path
from typing import Any

from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceCandidate, RTCIceServer, RTCSessionDescription
from aiortc.sdp import candidate_from_sdp
import av
import numpy as np
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


def _sample_mean(values: list[float]) -> float | None:
    if not values:
        return None
    return float(sum(values) / len(values))


def _is_relay_candidate(candidate: Any) -> bool:
    if candidate is None:
        return False
    return str(getattr(candidate, "type", "")).strip().lower() == "relay"


def _iter_urls(entry: dict[str, Any]) -> list[str]:
    urls = entry.get("urls")
    if isinstance(urls, str):
        return [urls]
    if isinstance(urls, list):
        return [str(url).strip() for url in urls if str(url).strip()]
    return []


def _has_turn(entry: dict[str, Any]) -> bool:
    return any(url.lower().startswith(("turn:", "turns:")) for url in _iter_urls(entry))


def _effective_backend_ice_entries() -> list[dict[str, Any]]:
    """
    Build backend ICE config for aiortc.
    Priority:
    - VISIVO_ICE_SERVERS entries (explicit backend config)
    - plus TURN entries from VISIVO_CLIENT_ICE_SERVERS (to avoid browser-only TURN setups)
    """
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add_entry(entry: dict[str, Any]) -> None:
        urls = _iter_urls(entry)
        if not urls:
            return
        key = json.dumps(
            {
                "urls": urls,
                "username": entry.get("username"),
                "credential": entry.get("credential"),
            },
            sort_keys=True,
        )
        if key in seen:
            return
        seen.add(key)
        normalized: dict[str, Any] = {"urls": urls}
        if isinstance(entry.get("username"), str):
            normalized["username"] = entry["username"]
        if isinstance(entry.get("credential"), str):
            normalized["credential"] = entry["credential"]
        merged.append(normalized)

    for entry in config.ice_servers:
        if isinstance(entry, dict):
            add_entry(entry)
    for entry in config.client_ice_servers:
        if isinstance(entry, dict) and _has_turn(entry):
            add_entry(entry)

    return merged


def _stat_value(stat: Any, key: str, default: Any = None) -> Any:
    if isinstance(stat, dict):
        return stat.get(key, default)
    return getattr(stat, key, default)


def _iter_stats(report: Any) -> list[Any]:
    values = getattr(report, "values", None)
    if callable(values):
        try:
            return list(values())
        except Exception:
            return []
    if isinstance(report, dict):
        return list(report.values())
    return []


def _get_stat(report: Any, stat_id: str | None) -> Any | None:
    if not stat_id:
        return None
    getter = getattr(report, "get", None)
    if callable(getter):
        try:
            return getter(stat_id)
        except Exception:
            return None
    if isinstance(report, dict):
        return report.get(stat_id)
    return None


def _selected_candidate_pair(report: Any) -> tuple[Any | None, Any | None, Any | None]:
    selected_pair_id: str | None = None
    for stat in _iter_stats(report):
        if _stat_value(stat, "type") == "transport":
            selected_pair_id = _stat_value(stat, "selectedCandidatePairId")
            if selected_pair_id:
                break

    pair = _get_stat(report, selected_pair_id) if selected_pair_id else None
    if pair is None:
        for stat in _iter_stats(report):
            if _stat_value(stat, "type") == "candidate-pair" and (
                _stat_value(stat, "selected")
                or _stat_value(stat, "nominated")
                or _stat_value(stat, "state") == "succeeded"
            ):
                pair = stat
                break
    if pair is None:
        return None, None, None

    local = _get_stat(report, _stat_value(pair, "localCandidateId"))
    remote = _get_stat(report, _stat_value(pair, "remoteCandidateId"))
    return pair, local, remote


class _JpegEncoder:
    def encode(self, frame_rgb: Any) -> bytes:
        frame = np.ascontiguousarray(frame_rgb)
        if frame.dtype != np.uint8:
            frame = np.clip(frame, 0, 255).astype(np.uint8, copy=False)
        height = int(frame.shape[0])
        width = int(frame.shape[1])

        codec = av.CodecContext.create("mjpeg", "w")
        codec.width = width
        codec.height = height
        codec.pix_fmt = "yuvj420p"
        codec.options = {"q": "5"}
        codec.open()

        video_frame = av.VideoFrame.from_ndarray(frame, format="rgb24")
        packets = codec.encode(video_frame)
        packets.extend(codec.encode(None))
        if not packets:
            return b""
        return b"".join(bytes(packet) for packet in packets)


async def _close_peer_connection(session: RemoteRenderSession) -> None:
    if session.peer_connection is not None:
        await session.peer_connection.close()
        session.peer_connection = None


def _is_authorized(token: str | None, expected: str | None) -> bool:
    if not expected:
        return True
    return bool(token) and token == expected


def _pc_config_from_env() -> RTCConfiguration:
    effective_entries = _effective_backend_ice_entries()
    servers = [
        RTCIceServer(
            urls=entry["urls"],
            username=entry.get("username"),
            credential=entry.get("credential"),
        )
        for entry in effective_entries
    ]
    backend_turn = any(_has_turn(entry) for entry in config.ice_servers if isinstance(entry, dict))
    effective_turn = any(_has_turn(entry) for entry in effective_entries)
    log.warning(
        "Backend ICE config entries=%s backend_has_turn=%s effective_has_turn=%s",
        len(effective_entries),
        backend_turn,
        effective_turn,
    )
    for idx, entry in enumerate(effective_entries, start=1):
        log.warning(
            "Backend ICE[%s] urls=%s username=%s",
            idx,
            _iter_urls(entry),
            bool(entry.get("username")),
        )
    return RTCConfiguration(iceServers=servers)


def _client_ice_servers(relay_only: bool) -> list[dict[str, Any]]:
    if not relay_only:
        return config.client_ice_servers
    filtered: list[dict[str, Any]] = []
    for entry in config.client_ice_servers:
        if not isinstance(entry, dict):
            continue
        urls = [url for url in _iter_urls(entry) if url.lower().startswith(("turn:", "turns:"))]
        if not urls:
            continue
        normalized = {"urls": urls}
        if isinstance(entry.get("username"), str):
            normalized["username"] = entry["username"]
        if isinstance(entry.get("credential"), str):
            normalized["credential"] = entry["credential"]
        filtered.append(normalized)
    return filtered


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


async def _attach_peer_connection(session: RemoteRenderSession, ws: WebSocket, relay_only: bool = False) -> RTCPeerConnection:
    await _close_peer_connection(session)

    pc = RTCPeerConnection(_pc_config_from_env())
    session.peer_connection = pc
    session.ice_relay_only = relay_only
    attach_started_ns = time.time_ns()
    session.latest_ice_metrics = {
        "relayOnly": relay_only,
        "candidateCount": 0,
        "localCandidateCount": 0,
        "remoteCandidateCount": 0,
        "filteredLocalCandidateCount": 0,
        "filteredRemoteCandidateCount": 0,
        "timeToFirstCandidateMs": None,
        "iceGatheringTimeMs": None,
        "timeToSelectedCandidateMs": None,
        "selectedCandidateType": None,
        "selectedCandidatePair": None,
        "iceConnectionState": pc.iceConnectionState,
        "connectionState": pc.connectionState,
    }
    stats_task: asyncio.Task[None] | None = None
    last_pair_summary = ""
    last_rtp_summary = ""
    gathering_started_ns = time.time_ns()

    video_track = LatestFrameVideoTrack(session)
    pc.addTrack(video_track)

    async def _stats_loop() -> None:
        nonlocal last_pair_summary, last_rtp_summary
        while True:
            await asyncio.sleep(2.0)
            try:
                report = await pc.getStats()
            except Exception:
                continue

            pair, local, remote = _selected_candidate_pair(report)
            if pair is not None:
                local_type = _stat_value(local, "candidateType", "unknown")
                remote_type = _stat_value(remote, "candidateType", "unknown")
                protocol = _stat_value(local, "protocol", _stat_value(pair, "protocol", "unknown"))
                local_addr = _stat_value(local, "address", _stat_value(local, "ip", "?"))
                local_port = _stat_value(local, "port", "?")
                remote_addr = _stat_value(remote, "address", _stat_value(remote, "ip", "?"))
                remote_port = _stat_value(remote, "port", "?")
                relay_selected = local_type == "relay" or remote_type == "relay"
                if session.latest_ice_metrics.get("timeToSelectedCandidateMs") is None:
                    session.latest_ice_metrics["timeToSelectedCandidateMs"] = max(
                        0.0, (time.time_ns() - attach_started_ns) / 1e6
                    )
                    session.latest_ice_metrics["selectedCandidateType"] = (
                        f"{local_type}/{remote_type}" if local_type or remote_type else None
                    )
                    session.latest_ice_metrics["selectedCandidatePair"] = {
                        "localType": local_type,
                        "remoteType": remote_type,
                        "protocol": protocol,
                        "localAddress": local_addr,
                        "remoteAddress": remote_addr,
                    }
                pair_summary = (
                    f"ICE pair selected session={session.session_id} "
                    f"local={local_type}@{local_addr}:{local_port} "
                    f"remote={remote_type}@{remote_addr}:{remote_port} "
                    f"protocol={protocol} state={_stat_value(pair, 'state', '?')} "
                    f"relay={relay_selected}"
                )
                if pair_summary != last_pair_summary:
                    last_pair_summary = pair_summary
                    log.warning(pair_summary)

            outbound_video = None
            remote_inbound_video = None
            for stat in _iter_stats(report):
                stat_type = _stat_value(stat, "type")
                if outbound_video is None and stat_type == "outbound-rtp" and _stat_value(stat, "kind") == "video":
                    outbound_video = stat
                if remote_inbound_video is None and stat_type == "remote-inbound-rtp" and _stat_value(stat, "kind") == "video":
                    remote_inbound_video = stat

            if outbound_video is not None:
                rtp_summary = (
                    f"RTP out video session={session.session_id} "
                    f"bytesSent={int(_stat_value(outbound_video, 'bytesSent', 0) or 0)} "
                    f"packetsSent={int(_stat_value(outbound_video, 'packetsSent', 0) or 0)} "
                    f"framesSent={int(_stat_value(outbound_video, 'framesSent', 0) or 0)}"
                )
                if remote_inbound_video is not None:
                    rtp_summary += (
                        f" remoteLost={int(_stat_value(remote_inbound_video, 'packetsLost', 0) or 0)} "
                        f"rtt={float(_stat_value(remote_inbound_video, 'roundTripTime', 0.0) or 0.0):.4f}"
                    )
                if rtp_summary != last_rtp_summary:
                    last_rtp_summary = rtp_summary
                    log.warning(rtp_summary)

    @pc.on("connectionstatechange")
    async def on_connectionstatechange() -> None:
        nonlocal stats_task
        log.warning("PeerConnection state=%s session=%s", pc.connectionState, session.session_id)
        session.latest_ice_metrics["connectionState"] = pc.connectionState
        if pc.connectionState in {"connecting", "connected"} and stats_task is None:
            stats_task = asyncio.create_task(_stats_loop())
        if pc.connectionState in {"failed", "closed"} and stats_task is not None:
            stats_task.cancel()
            stats_task = None

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange() -> None:
        nonlocal stats_task
        log.warning("ICE state=%s session=%s", pc.iceConnectionState, session.session_id)
        session.latest_ice_metrics["iceConnectionState"] = pc.iceConnectionState
        if pc.iceConnectionState in {"failed", "closed", "disconnected"} and stats_task is not None:
            stats_task.cancel()
            stats_task = None

    @pc.on("icegatheringstatechange")
    async def on_icegatheringstatechange() -> None:
        log.warning("ICE gathering state=%s session=%s", pc.iceGatheringState, session.session_id)
        if pc.iceGatheringState == "complete":
            session.latest_ice_metrics["iceGatheringTimeMs"] = max(0.0, (time.time_ns() - gathering_started_ns) / 1e6)

    @pc.on("icecandidate")
    async def on_icecandidate(candidate: RTCIceCandidate | None) -> None:
        if candidate is None:
            log.warning("Local ICE candidate end-of-candidates session=%s", session.session_id)
            return
        session.latest_ice_metrics["localCandidateCount"] += 1
        session.latest_ice_metrics["candidateCount"] += 1
        if session.latest_ice_metrics.get("timeToFirstCandidateMs") is None:
            session.latest_ice_metrics["timeToFirstCandidateMs"] = max(0.0, (time.time_ns() - attach_started_ns) / 1e6)
        if relay_only and not _is_relay_candidate(candidate):
            session.latest_ice_metrics["filteredLocalCandidateCount"] += 1
            log.warning(
                "Filtered local ICE candidate type=%s session=%s relayOnly=%s",
                getattr(candidate, "type", "unknown"),
                session.session_id,
                relay_only,
            )
            return
        candidate_str = candidate.candidate or ""
        candidate_ip = getattr(candidate, "ip", None) or getattr(candidate, "address", None) or "unknown"
        candidate_port = getattr(candidate, "port", None) or "unknown"
        redacted_candidate = candidate_str[:180] + ("..." if len(candidate_str) > 180 else "")
        log.warning(
            "Local ICE candidate type=%s protocol=%s addr=%s:%s session=%s candidate=%s",
            getattr(candidate, "type", "unknown"),
            getattr(candidate, "protocol", "unknown"),
            candidate_ip,
            candidate_port,
            session.session_id,
            redacted_candidate,
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
    gather_wait_ms = int(
        os.getenv(
            "VISIVO_ICE_GATHER_TIMEOUT_MS_RELAY" if relay_only else "VISIVO_ICE_GATHER_TIMEOUT_MS",
            "200" if relay_only else "300",
        )
    )
    if gather_wait_ms > 0:
        gather_deadline = time.time() + (gather_wait_ms / 1000.0)
        while pc.iceGatheringState != "complete" and time.time() < gather_deadline:
            await asyncio.sleep(0.05)
        log.warning(
            "Offer dispatch session=%s iceGatheringState=%s timeoutMs=%s",
            session.session_id,
            pc.iceGatheringState,
            gather_wait_ms,
        )
    await ws.send_json(
        {
            "type": "offer",
            "description": {"type": pc.localDescription.type, "sdp": pc.localDescription.sdp},
            "iceServers": _client_ice_servers(relay_only),
        }
    )
    return pc


async def _ws_stream_loop(
    session: RemoteRenderSession,
    ws: WebSocket,
    fps: float,
) -> None:
    min_interval_s = 1.0 / min(max(float(fps), 1.0), 30.0)
    encoder = _JpegEncoder()
    try:
        while True:
            loop_started_ns = time.time_ns()
            frame_packet = session.render_if_needed()
            if frame_packet is None:
                frame_packet = session.render_if_needed(force=True)
            if frame_packet is None:
                await asyncio.sleep(min_interval_s)
                continue

            encode_started_ns = time.time_ns()
            jpeg_bytes = encoder.encode(frame_packet.frame_rgb)
            encode_ms = (time.time_ns() - encode_started_ns) / 1e6
            session.stats.add_sample(session.stats.encode_time_ms, encode_ms)
            session.stats.add_sample(session.stats.rtp_pacing_time_ms, 0.0)
            total_pipeline_ms = (time.time_ns() - frame_packet.render_started_ns) / 1e6
            session.stats.add_sample(session.stats.total_frame_pipeline_time_ms, total_pipeline_ms)
            pipeline_metrics = dict(frame_packet.pipeline_metrics)
            pipeline_metrics.update(
                {
                    "encodeTimeMs": encode_ms,
                    "rtpPacingTimeMs": 0.0,
                    "totalFramePipelineTimeMs": total_pipeline_ms,
                }
            )
            session.latest_pipeline_metrics = pipeline_metrics
            if not jpeg_bytes:
                await asyncio.sleep(min_interval_s)
                continue

            frame_delivery_ms = (time.time_ns() - frame_packet.render_finished_ns) / 1e6
            session.stats.add_sample(session.stats.frame_delivery_latency_ms, frame_delivery_ms)
            session.stats.delivered_frames += 1
            session.record_first_frame_delivery(
                encode_ms=encode_ms,
                send_ms=frame_delivery_ms,
                delivered_ns=time.time_ns(),
            )
            await ws.send_json(
                {
                    "type": "ws-frame",
                    "serial": frame_packet.serial,
                    "mime": "image/jpeg",
                    "data": base64.b64encode(jpeg_bytes).decode("ascii"),
                    "width": int(frame_packet.frame_rgb.shape[1]),
                    "height": int(frame_packet.frame_rgb.shape[0]),
                    "sessionId": session.session_id,
                }
            )
            elapsed_s = (time.time_ns() - loop_started_ns) / 1e9
            sleep_s = min_interval_s - elapsed_s
            if sleep_s > 0:
                await asyncio.sleep(sleep_s)
    except asyncio.CancelledError:
        raise
    except Exception:
        log.exception("WS fallback stream loop failed session=%s", session.session_id)


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
    pipeline_metrics = dict(session.latest_pipeline_metrics)
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
                    "cacheHit": session.import_metrics.cache_hit,
                }
                if session.import_metrics
                else None
            ),
            "runtimeMetrics": {
                "firstFrameLatencyMs": session.runtime_metrics.first_frame_latency_ms,
                "firstFrameSessionInitMs": session.runtime_metrics.first_frame_session_init_ms,
                "firstFrameSignalingSetupMs": session.runtime_metrics.first_frame_signaling_setup_ms,
                "firstFrameFitsLoadMs": session.runtime_metrics.first_frame_fits_load_ms,
                "firstFrameSanitizeConvertMs": session.runtime_metrics.first_frame_sanitize_convert_ms,
                "firstFrameVtkBuildMs": session.runtime_metrics.first_frame_vtk_build_ms,
                "firstFrameRendererWarmupMs": session.runtime_metrics.first_frame_renderer_warmup_ms,
                "firstFrameRenderMs": session.runtime_metrics.first_frame_render_ms,
                "firstFrameCaptureMs": session.runtime_metrics.first_frame_capture_ms,
                "firstFrameConversionMs": session.runtime_metrics.first_frame_conversion_ms,
                "firstFrameEncodeMs": session.runtime_metrics.first_frame_encode_ms,
                "firstFrameSendMs": session.runtime_metrics.first_frame_send_ms,
                "highQualityRenderTimeMs": session.runtime_metrics.high_quality_render_time_ms,
                "interactiveFps": session.runtime_metrics.interactive_fps,
                "memoryRssMb": session.runtime_metrics.memory_rss_mb,
            },
            "pipelineMetrics": {
                "activeMapperClass": pipeline_metrics.get("activeMapperClass"),
                "requestedMapperClass": pipeline_metrics.get("requestedMapperClass"),
                "smartMapperRequestedMode": pipeline_metrics.get("smartMapperRequestedMode"),
                "smartMapperLastUsedMode": pipeline_metrics.get("smartMapperLastUsedMode"),
                "renderTimeMs": _sample_mean(session.stats.render_time_ms),
                "frameCaptureReadbackTimeMs": _sample_mean(session.stats.frame_capture_time_ms),
                "frameConversionTimeMs": _sample_mean(session.stats.frame_conversion_time_ms),
                "encodeTimeMs": _sample_mean(session.stats.encode_time_ms),
                "rtpPacingTimeMs": _sample_mean(session.stats.rtp_pacing_time_ms),
                "totalFramePipelineTimeMs": _sample_mean(session.stats.total_frame_pipeline_time_ms),
            },
            "iceMetrics": dict(session.latest_ice_metrics),
            "rendererDiagnostics": session.renderer.get_renderer_diagnostics(),
        }
    )


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    session: RemoteRenderSession | None = None
    ws_stream_task: asyncio.Task[None] | None = None
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
                force_ws_fallback = bool(payload.get("forceWsFallback"))
                force_relay_only = bool(payload.get("forceRelayOnly")) or os.getenv("VISIVO_FORCE_RELAY_ONLY", "0") == "1"
                msg_token = payload.get("token")
                if config.auth_token and not (msg_token == config.auth_token or token == config.auth_token):
                    await ws.send_json({"type": "error", "message": "unauthorized"})
                    await ws.close(code=4401)
                    return
                session = await sessions.get_or_create(requested_session_id, dataset_path=dataset_path)
                session.mark_hello_received()
                session.control_ws = ws
                viewport = payload.get("viewport") or {}
                session.resize(
                    width=int(viewport.get("width", 1280)),
                    height=int(viewport.get("height", 720)),
                    dpr=float(viewport.get("dpr", 1.0)),
                )
                session.prime_first_frame()
                if not force_ws_fallback:
                    await _attach_peer_connection(session, ws, relay_only=force_relay_only)
                else:
                    await _close_peer_connection(session)
                    if ws_stream_task is not None:
                        ws_stream_task.cancel()
                        try:
                            await ws_stream_task
                        except asyncio.CancelledError:
                            pass
                    ws_stream_task = asyncio.create_task(_ws_stream_loop(session, ws, 8.0))
                    await ws.send_json({"type": "ws-stream.started", "fps": 8.0, "sessionId": session.session_id})
                await ws.send_json({"type": "stream-ready", "sessionId": session.session_id})
                session.mark_stream_ready_sent()
                await _emit_state(ws, session, text="Session connected")
                continue

            if session is None:
                await ws.send_json({"type": "error", "message": "send hello first"})
                continue

            if msg_type in {"answer", "webrtc.answer"}:
                description = _normalize_description(payload)
                if description and session.peer_connection:
                    await session.peer_connection.setRemoteDescription(description)
                    session.mark_remote_answer_set()
                continue

            if msg_type in {"webrtc.stop", "rtc.stop"}:
                await _close_peer_connection(session)
                continue

            if msg_type in {"ice", "ice-candidate", "webrtc.ice"}:
                candidate = _normalize_candidate(payload)
                if candidate and session.peer_connection:
                    session.latest_ice_metrics["remoteCandidateCount"] = int(
                        session.latest_ice_metrics.get("remoteCandidateCount", 0)
                    ) + 1
                    session.latest_ice_metrics["candidateCount"] = int(
                        session.latest_ice_metrics.get("candidateCount", 0)
                    ) + 1
                    if session.ice_relay_only and not _is_relay_candidate(candidate):
                        session.latest_ice_metrics["filteredRemoteCandidateCount"] = int(
                            session.latest_ice_metrics.get("filteredRemoteCandidateCount", 0)
                        ) + 1
                        log.warning(
                            "Filtered remote ICE candidate type=%s session=%s relayOnly=%s",
                            getattr(candidate, "type", "unknown"),
                            session.session_id,
                            session.ice_relay_only,
                        )
                        continue
                    candidate_str = getattr(candidate, "candidate", "") or ""
                    redacted_candidate = candidate_str[:180] + ("..." if len(candidate_str) > 180 else "")
                    candidate_ip = getattr(candidate, "ip", None) or getattr(candidate, "address", None) or "unknown"
                    candidate_port = getattr(candidate, "port", None) or "unknown"
                    log.warning(
                        "Remote ICE candidate type=%s protocol=%s addr=%s:%s session=%s candidate=%s",
                        getattr(candidate, "type", "unknown"),
                        getattr(candidate, "protocol", "unknown"),
                        candidate_ip,
                        candidate_port,
                        session.session_id,
                        redacted_candidate,
                    )
                    await session.peer_connection.addIceCandidate(candidate)
                continue

            if msg_type in {"ws-stream.start", "ws.stream.start"}:
                await _close_peer_connection(session)
                target_fps = payload.get("fps", 8)
                try:
                    target_fps = float(target_fps)
                except Exception:
                    target_fps = 8.0
                target_fps = min(max(target_fps, 1.0), 30.0)
                if ws_stream_task is not None:
                    ws_stream_task.cancel()
                    try:
                        await ws_stream_task
                    except asyncio.CancelledError:
                        pass
                ws_stream_task = asyncio.create_task(_ws_stream_loop(session, ws, target_fps))
                await ws.send_json({"type": "ws-stream.started", "fps": target_fps, "sessionId": session.session_id})
                continue

            if msg_type in {"ws-stream.stop", "ws.stream.stop"}:
                if ws_stream_task is not None:
                    ws_stream_task.cancel()
                    try:
                        await ws_stream_task
                    except asyncio.CancelledError:
                        pass
                    ws_stream_task = None
                await ws.send_json({"type": "ws-stream.stopped", "sessionId": session.session_id})
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
        if ws_stream_task is not None:
            ws_stream_task.cancel()
            try:
                await ws_stream_task
            except asyncio.CancelledError:
                pass
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
    backend_turn = any(_has_turn(entry) for entry in config.ice_servers if isinstance(entry, dict))
    client_turn = any(_has_turn(entry) for entry in config.client_ice_servers if isinstance(entry, dict))
    log.warning(
        "Startup ICE summary backend_entries=%s backend_has_turn=%s client_entries=%s client_has_turn=%s",
        len(config.ice_servers),
        backend_turn,
        len(config.client_ice_servers),
        client_turn,
    )

    async def _cleanup_loop() -> None:
        while True:
            await sessions.cleanup_idle()
            await asyncio.sleep(30)

    cleanup_task = asyncio.create_task(_cleanup_loop())
