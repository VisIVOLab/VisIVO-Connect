from __future__ import annotations

import asyncio
import base64
import json
import logging
import time
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit, urlunsplit

from astropy.io import fits
from aiortc import RTCPeerConnection, RTCConfiguration, RTCIceCandidate, RTCIceServer, RTCSessionDescription
from aiortc.sdp import candidate_from_sdp
import av
import numpy as np
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles

from backend.core.config import (
    AppConfig,
    ConfigError,
    dataset_relative_path,
    dataset_root_path,
    is_supported_dataset_file,
    load_config,
    resolve_dataset_browser_path,
    resolve_dataset_path,
)
from backend.core.session import RemoteRenderSession, SessionManager
from backend.data.importers import _parse_dataset_request, _select_fits_hdu
from backend.transport.video_track import LatestFrameVideoTrack

BASE_DIR = Path(__file__).resolve().parents[2]
WEB_DIR = BASE_DIR / "web"
try:
    config: AppConfig = load_config()
except ConfigError as exc:
    raise RuntimeError(f"Invalid VisIVO configuration: {exc}") from exc

APP_STARTED_NS = time.time_ns()
STARTUP_WARNINGS: list[str] = []
STARTUP_ERRORS: list[str] = []
LAST_RENDERER_DIAGNOSTICS: dict[str, Any] | None = None

app = FastAPI(title=config.app_name, version=config.app_version)
if config.allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

if WEB_DIR.exists():
    app.mount("/web", StaticFiles(directory=str(WEB_DIR), html=True), name="web")

sessions = SessionManager(max_sessions=config.max_sessions, idle_timeout_s=config.idle_timeout_s)
cleanup_task = None
log = logging.getLogger("uvicorn.error")
log.setLevel(getattr(logging, config.log_level, logging.INFO))


class ClientFacingError(RuntimeError):
    def __init__(
        self,
        code: str,
        message: str,
        *,
        phase: str,
        retryable: bool = False,
        details: dict[str, Any] | None = None,
        close_code: int | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.phase = phase
        self.retryable = retryable
        self.details = details or {}
        self.close_code = close_code


def _sample_mean(values: list[float]) -> float | None:
    if not values:
        return None
    return float(sum(values) / len(values))


def _uptime_s() -> float:
    return max(0.0, (time.time_ns() - APP_STARTED_NS) / 1e9)


def _error_payload(
    code: str,
    message: str,
    *,
    phase: str,
    retryable: bool = False,
    session_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "type": "error",
        "code": code,
        "message": message,
        "phase": phase,
        "retryable": retryable,
    }
    if session_id:
        payload["sessionId"] = session_id
    if details:
        payload["details"] = details
    return payload


def _error_response(
    code: str,
    message: str,
    *,
    phase: str,
    status_code: int,
    retryable: bool = False,
    details: dict[str, Any] | None = None,
) -> JSONResponse:
    return JSONResponse(
        _error_payload(code, message, phase=phase, retryable=retryable, details=details),
        status_code=status_code,
    )


async def _send_ws_error(
    ws: WebSocket,
    code: str,
    message: str,
    *,
    phase: str,
    retryable: bool = False,
    session_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    await ws.send_json(
        _error_payload(
            code,
            message,
            phase=phase,
            retryable=retryable,
            session_id=session_id,
            details=details,
        )
    )


async def _send_dataset_loading(
    ws: WebSocket,
    *,
    phase: str,
    label: str,
    dataset_path: str | None,
    session: RemoteRenderSession | None = None,
    done: bool = False,
) -> None:
    dataset_name = Path(dataset_path.split("#", 1)[0]).name if isinstance(dataset_path, str) and dataset_path else None
    relative_path = dataset_relative_path(dataset_path, allowed_root=config.dataset_root)
    payload: dict[str, Any] = {
        "type": "dataset.loading",
        "phase": phase,
        "label": label,
        "datasetPath": relative_path or dataset_path,
        "datasetName": dataset_name,
        "done": done,
    }
    if session is not None:
        payload["sessionId"] = session.session_id
        if session.import_metrics is not None:
            payload["importMetrics"] = {
                "fitsOpenMs": session.import_metrics.fits_open_ms,
                "hduSelectMs": session.import_metrics.hdu_select_ms,
                "sanitizeConvertMs": session.import_metrics.sanitize_convert_ms,
                "vtkBuildMs": session.import_metrics.vtk_build_ms,
                "fitsTotalMs": session.import_metrics.fits_total_ms,
                "cacheHit": session.import_metrics.cache_hit,
            }
        payload["warmupMetrics"] = session.renderer.get_warmup_metrics()
    await ws.send_json(payload)


def _startup_snapshot() -> dict[str, Any]:
    return {
        "status": "ok" if not STARTUP_ERRORS else "error",
        "uptimeS": round(_uptime_s(), 3),
        "backendVersion": config.app_version,
        "frontendBuild": config.frontend_build,
        "webDirPresent": WEB_DIR.exists(),
        "warnings": list(STARTUP_WARNINGS),
        "errors": list(STARTUP_ERRORS),
        "config": config.sanitized_summary(),
    }


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


def _apply_video_bandwidth_hints(sdp: str, bitrate_mbps: float | int | None) -> str:
    if not isinstance(sdp, str) or not sdp.strip():
        return sdp
    if not isinstance(bitrate_mbps, (int, float)) or bitrate_mbps <= 0:
        return sdp

    bitrate_bps = int(float(bitrate_mbps) * 1_000_000)
    bitrate_as = max(1, int(round(bitrate_bps / 1000.0)))
    lines = sdp.splitlines()
    result: list[str] = []
    in_video = False
    inserted = False

    for line in lines:
        if line.startswith("m="):
            if in_video and not inserted:
                result.append(f"b=AS:{bitrate_as}")
                result.append(f"b=TIAS:{bitrate_bps}")
            in_video = line.startswith("m=video ")
            inserted = False
            result.append(line)
            continue
        if in_video and line.startswith("b="):
            continue
        if in_video and not inserted and line.startswith("c="):
            result.append(line)
            result.append(f"b=AS:{bitrate_as}")
            result.append(f"b=TIAS:{bitrate_bps}")
            inserted = True
            continue
        result.append(line)

    if in_video and not inserted:
        result.append(f"b=AS:{bitrate_as}")
        result.append(f"b=TIAS:{bitrate_bps}")
    return "\r\n".join(result) + "\r\n"


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


def _request_token(request: Request) -> str | None:
    auth_header = request.headers.get("authorization", "").strip()
    if auth_header.lower().startswith("bearer "):
        bearer = auth_header[7:].strip()
        if bearer:
            return bearer
    query_token = request.query_params.get("token")
    return query_token.strip() if isinstance(query_token, str) and query_token.strip() else None


def _dataset_browser_listing(relative_path: str | None, *, active_dataset_path: str | None = None) -> dict[str, Any]:
    root_path = dataset_root_path(config.dataset_root)
    current_path, current_relative = resolve_dataset_browser_path(
        relative_path,
        allowed_root=config.dataset_root,
        expect_directory=True,
        strict_exists=True,
    )
    parent_relative: str | None = None
    if current_path != root_path:
        parent_relative = current_path.parent.relative_to(root_path).as_posix() if current_path.parent != root_path else ""
    active_relative = dataset_relative_path(active_dataset_path, allowed_root=config.dataset_root)
    entries: list[dict[str, Any]] = []
    for child in sorted(current_path.iterdir(), key=lambda entry: (not entry.is_dir(), entry.name.lower())):
        if child.name.startswith("."):
            continue
        try:
            resolved_child = child.resolve(strict=False)
            resolved_child.relative_to(root_path)
        except (OSError, ValueError):
            continue
        is_directory = child.is_dir()
        is_supported = is_directory or is_supported_dataset_file(child)
        if not is_supported:
            continue
        relative = resolved_child.relative_to(root_path).as_posix()
        stat_result = child.stat()
        entries.append(
            {
                "name": child.name,
                "type": "directory" if is_directory else "file",
                "path": relative,
                "sizeBytes": None if is_directory else int(stat_result.st_size),
                "modifiedMs": int(stat_result.st_mtime_ns // 1_000_000),
                "supported": is_supported_dataset_file(child),
                "active": relative == active_relative or (
                    isinstance(active_relative, str) and active_relative.startswith(f"{relative}#")
                ),
            }
        )
    return {
        "rootConfigured": True,
        "currentPath": current_relative,
        "parentPath": parent_relative,
        "activeDatasetPath": active_relative,
        "entries": entries,
    }


def _dataset_file_details(relative_path: str | None) -> dict[str, Any]:
    selected_file, selected_relative = resolve_dataset_browser_path(
        relative_path,
        allowed_root=config.dataset_root,
        expect_directory=False,
        strict_exists=True,
    )
    stat_result = selected_file.stat()
    payload: dict[str, Any] = {
        "name": selected_file.name,
        "path": selected_relative,
        "type": "file",
        "supported": is_supported_dataset_file(selected_file),
        "sizeBytes": int(stat_result.st_size),
        "modifiedMs": int(stat_result.st_mtime_ns // 1_000_000),
        "fits": None,
    }
    if not payload["supported"]:
        return payload

    hdus: list[dict[str, Any]] = []
    header_preview: dict[str, Any] = {}
    default_hdu_index: int | None = None
    with fits.open(selected_file, memmap=True) as hdul:
        try:
            default_hdu_index, _ = _select_fits_hdu(hdul, None)
        except ValueError:
            default_hdu_index = None
        for index, hdu in enumerate(hdul):
            header = hdu.header
            shape = getattr(hdu, "shape", None)
            dtype = None
            data = getattr(hdu, "data", None)
            ndim = int(np.ndim(data)) if data is not None else None
            if data is not None:
                dtype = str(getattr(data, "dtype", None) or "")
            hdu_header_preview: dict[str, Any] = {}
            for key in (
                "EXTNAME",
                "OBJECT",
                "BTYPE",
                "BUNIT",
                "CTYPE1",
                "CTYPE2",
                "CTYPE3",
                "CUNIT1",
                "CUNIT2",
                "CUNIT3",
            ):
                if key in header:
                    hdu_header_preview[key] = header[key]
            hdus.append(
                {
                    "index": index,
                    "name": str(header.get("EXTNAME", "") or ""),
                    "className": type(hdu).__name__,
                    "shape": list(shape) if isinstance(shape, tuple) else None,
                    "dtype": dtype or None,
                    "isImage": bool(data is not None),
                    "ndim": ndim,
                    "isSelectable": bool(data is not None and ndim is not None and ndim >= 3),
                    "isDefault": default_hdu_index == index,
                    "headerPreview": hdu_header_preview,
                }
            )
        if hdul:
            first_header = hdul[0].header
            for key in (
                "OBJECT",
                "BTYPE",
                "BUNIT",
                "TELESCOP",
                "INSTRUME",
                "CTYPE1",
                "CTYPE2",
                "CTYPE3",
                "CUNIT1",
                "CUNIT2",
                "CUNIT3",
                "BSCALE",
                "BZERO",
                "BLANK",
            ):
                if key in first_header:
                    header_preview[key] = first_header[key]
    payload["fits"] = {
        "hduCount": len(hdus),
        "selectableHduCount": sum(1 for hdu in hdus if hdu["isSelectable"]),
        "defaultHduIndex": default_hdu_index,
        "hdus": hdus,
        "headerPreview": header_preview,
    }
    return payload


def _resolve_requested_dataset_path(requested_dataset_path: str | None) -> str | None:
    candidate = (requested_dataset_path or "").strip()
    if candidate and config.dataset_root:
        try:
            request = _parse_dataset_request(candidate)
            selected_file, _ = resolve_dataset_browser_path(
                str(request.path),
                allowed_root=config.dataset_root,
                expect_directory=False,
                strict_exists=config.strict_dataset_path,
            )
        except (ConfigError, ValueError):
            pass
        else:
            parsed = urlsplit(candidate)
            resolved_candidate = str(selected_file)
            if parsed.fragment:
                resolved_candidate = urlunsplit(("", "", str(selected_file), "", parsed.fragment))
            return resolve_dataset_path(
                resolved_candidate,
                default_path=config.dataset_path,
                allowed_root=config.dataset_root,
                strict_exists=config.strict_dataset_path,
            )
    return resolve_dataset_path(
        requested_dataset_path,
        default_path=config.dataset_path,
        allowed_root=config.dataset_root,
        strict_exists=config.strict_dataset_path,
    )


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
    global LAST_RENDERER_DIAGNOSTICS
    LAST_RENDERER_DIAGNOSTICS = session.renderer.get_renderer_diagnostics()
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
    gather_wait_ms = config.ice_gather_timeout_ms_relay if relay_only else config.ice_gather_timeout_ms
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
    offer_sdp = _apply_video_bandwidth_hints(pc.localDescription.sdp, session.target_bitrate_mbps)
    log.warning(
        "Offer video bandwidth hints session=%s bitrateMbps=%.2f",
        session.session_id,
        session.target_bitrate_mbps,
    )
    await ws.send_json(
        {
            "type": "offer",
            "description": {"type": pc.localDescription.type, "sdp": offer_sdp},
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


async def _prime_session_frame(session: RemoteRenderSession) -> None:
    await asyncio.sleep(0)
    try:
        session.prime_first_frame()
    except Exception:
        log.exception("Session background warmup failed session=%s", session.session_id)


@app.get("/")
async def index() -> Response:
    if not WEB_DIR.exists():
        return _error_response("web-dir-missing", "web directory not found", phase="startup", status_code=404)
    return FileResponse(WEB_DIR / "index.html")


@app.get("/healthz")
async def healthz() -> JSONResponse:
    return JSONResponse(
        {
            "status": "ok",
            "service": config.app_name,
            "backendVersion": config.app_version,
            "frontendBuild": config.frontend_build,
            "uptimeS": round(_uptime_s(), 3),
        }
    )


@app.get("/readyz")
async def readyz() -> JSONResponse:
    session_summary = await sessions.summary()
    payload = _startup_snapshot()
    payload.update(session_summary)
    payload["rendererDiagnostics"] = LAST_RENDERER_DIAGNOSTICS
    ready = bool(WEB_DIR.exists() and not STARTUP_ERRORS)
    if config.strict_dataset_path and config.dataset_path:
        try:
            resolve_dataset_path(
                config.dataset_path,
                allowed_root=config.dataset_root,
                strict_exists=True,
            )
        except ConfigError as exc:
            ready = False
            payload["errors"] = [*payload["errors"], str(exc)]
    payload["status"] = "ready" if ready else "degraded"
    return JSONResponse(payload, status_code=200 if ready else 503)


@app.get("/api/version")
async def api_version() -> JSONResponse:
    return JSONResponse(
        {
            "service": config.app_name,
            "backendVersion": config.app_version,
            "frontendBuild": config.frontend_build,
            "uptimeS": round(_uptime_s(), 3),
            "config": config.sanitized_summary(),
        }
    )


@app.get("/api/runtime-config")
async def api_runtime_config() -> JSONResponse:
    payload = config.public_runtime_config()
    payload["datasetBrowserEnabled"] = bool(config.dataset_root)
    payload["defaultDatasetPath"] = config.dataset_path
    payload["defaultDatasetRelativePath"] = dataset_relative_path(config.dataset_path, allowed_root=config.dataset_root)
    return JSONResponse(payload)


@app.get("/api/datasets")
async def api_datasets(request: Request) -> JSONResponse:
    if not _is_authorized(_request_token(request), config.auth_token):
        return _error_response("unauthorized", "unauthorized", phase="dataset-browser", status_code=401)
    try:
        payload = _dataset_browser_listing(request.query_params.get("path"), active_dataset_path=config.dataset_path)
    except ConfigError as exc:
        return _error_response("dataset-browser-unavailable", str(exc), phase="dataset-browser", status_code=400)
    except OSError as exc:
        return _error_response("dataset-browser-io", str(exc), phase="dataset-browser", status_code=500)
    return JSONResponse(payload)


@app.get("/api/datasets/details")
async def api_dataset_details(request: Request) -> JSONResponse:
    if not _is_authorized(_request_token(request), config.auth_token):
        return _error_response("unauthorized", "unauthorized", phase="dataset-browser", status_code=401)
    try:
        payload = _dataset_file_details(request.query_params.get("path"))
    except ConfigError as exc:
        return _error_response("dataset-details-invalid", str(exc), phase="dataset-browser", status_code=400)
    except OSError as exc:
        return _error_response("dataset-details-io", str(exc), phase="dataset-browser", status_code=500)
    return JSONResponse(payload)


@app.get("/api/metrics/{session_id}")
async def session_metrics(session_id: str, request: Request) -> JSONResponse:
    metrics_token = request.query_params.get("token")
    if not _is_authorized(metrics_token, config.metrics_auth_token):
        return _error_response("unauthorized", "unauthorized", phase="metrics", status_code=401)
    session = await sessions.get(session_id)
    if session is None:
        return _error_response("session-not-found", "session not found", phase="metrics", status_code=404, retryable=True)
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
            "effectiveQualityProfiles": session.effective_quality_profiles(),
            "iceMetrics": dict(session.latest_ice_metrics),
            "rendererDiagnostics": session.renderer.get_renderer_diagnostics(),
        }
    )


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await ws.accept()
    session: RemoteRenderSession | None = None
    ws_stream_task: asyncio.Task[None] | None = None
    phase = "connect"
    token = ws.query_params.get("token")
    if config.auth_token and token and token != config.auth_token:
        await _send_ws_error(ws, "unauthorized", "unauthorized", phase="auth", retryable=False)
        await ws.close(code=4401)
        return

    try:
        while True:
            raw = await ws.receive_text()
            try:
                payload = json.loads(raw)
            except json.JSONDecodeError:
                await _send_ws_error(ws, "invalid-json", "invalid json", phase="protocol", retryable=True)
                continue

            msg_type = payload.get("type")

            try:
                if msg_type == "hello":
                    phase = "hello"
                    requested_session_id = payload.get("sessionId")
                    requested_dataset_path = payload.get("datasetPath")
                    dataset_path = _resolve_requested_dataset_path(requested_dataset_path)
                    if config.strict_dataset_path and not dataset_path:
                        raise ClientFacingError(
                            "dataset-required",
                            "No dataset configured for this session",
                            phase="session-init",
                            retryable=False,
                        )
                    initial_render_params = payload.get("initialRenderParams")
                    force_ws_fallback = bool(payload.get("forceWsFallback"))
                    force_relay_only = bool(payload.get("forceRelayOnly")) or config.relay_only_default
                    msg_token = payload.get("token")
                    if config.auth_token and not (msg_token == config.auth_token or token == config.auth_token):
                        raise ClientFacingError("unauthorized", "unauthorized", phase="auth", close_code=4401)
                    try:
                        session = await sessions.get_or_create(requested_session_id, dataset_path=dataset_path)
                    except Exception as exc:
                        raise ClientFacingError(
                            "session-init-failed",
                            "Could not initialize session",
                            phase="session-init",
                            retryable=False,
                            details={"datasetPath": dataset_path},
                        ) from exc
                    session.mark_hello_received()
                    session.control_ws = ws
                    viewport = payload.get("viewport") or {}
                    session.resize(
                        width=int(viewport.get("width", 1280)),
                        height=int(viewport.get("height", 720)),
                        dpr=float(viewport.get("dpr", 1.0)),
                    )
                    if isinstance(initial_render_params, dict):
                        session.set_render_params({"params": initial_render_params})
                    if not force_ws_fallback:
                        phase = "signaling"
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
                    if session.maybe_start_warmup_task():
                        asyncio.create_task(_prime_session_frame(session))
                    phase = "ready"
                    continue

                if session is None:
                    raise ClientFacingError("hello-required", "send hello first", phase="protocol", retryable=True)

                if msg_type in {"answer", "webrtc.answer"}:
                    phase = "signaling"
                    description = _normalize_description(payload)
                    if description and session.peer_connection:
                        await session.peer_connection.setRemoteDescription(description)
                        session.mark_remote_answer_set()
                    continue

                if msg_type in {"webrtc.stop", "rtc.stop"}:
                    phase = "webrtc-stop"
                    await _close_peer_connection(session)
                    continue

                if msg_type in {"ice", "ice-candidate", "webrtc.ice"}:
                    phase = "ice"
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
                    phase = "ws-fallback"
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
                    phase = "ws-fallback"
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
                    phase = "resize"
                    viewport = payload.get("viewport", {})
                    session.resize(
                        width=int(viewport.get("width", session.viewport.width)),
                        height=int(viewport.get("height", session.viewport.height)),
                        dpr=float(viewport.get("dpr", session.viewport.dpr)),
                    )
                    continue

                if msg_type in {"dataset.select", "dataset.switch"}:
                    phase = "dataset-switch"
                    selected_relative_path = payload.get("path", payload.get("relativePath"))
                    request = _parse_dataset_request(str(selected_relative_path or ""))
                    selected_file, _ = resolve_dataset_browser_path(
                        str(request.path),
                        allowed_root=config.dataset_root,
                        expect_directory=False,
                        strict_exists=True,
                    )
                    if not is_supported_dataset_file(selected_file):
                        raise ClientFacingError(
                            "dataset-unsupported",
                            "Selected file is not a supported FITS dataset",
                            phase=phase,
                            retryable=False,
                            details={"path": str(selected_relative_path or "")},
                        )
                    parsed_selected = urlsplit(str(selected_relative_path or ""))
                    dataset_candidate = str(selected_file)
                    if parsed_selected.fragment:
                        dataset_candidate = urlunsplit(("", "", str(selected_file), "", parsed_selected.fragment))
                    dataset_path = resolve_dataset_path(
                        dataset_candidate,
                        allowed_root=config.dataset_root,
                        strict_exists=True,
                    )
                    if not dataset_path:
                        raise ClientFacingError(
                            "dataset-invalid",
                            "Could not resolve selected dataset",
                            phase=phase,
                            retryable=False,
                        )
                    await _send_dataset_loading(
                        ws,
                        phase="opening-fits",
                        label="Opening FITS",
                        dataset_path=dataset_path,
                        session=session,
                    )
                    session.switch_dataset(dataset_path)
                    await _send_dataset_loading(
                        ws,
                        phase="initializing-renderer",
                        label="Initializing renderer",
                        dataset_path=dataset_path,
                        session=session,
                    )
                    await _send_dataset_loading(
                        ws,
                        phase="warming-up",
                        label="Warming up first frame",
                        dataset_path=dataset_path,
                        session=session,
                    )
                    session.prime_first_frame()
                    await _send_dataset_loading(
                        ws,
                        phase="complete",
                        label="Dataset ready",
                        dataset_path=dataset_path,
                        session=session,
                        done=True,
                    )
                    await _emit_state(ws, session, text=f"Dataset loaded: {selected_file.name}")
                    continue

                if msg_type == "interaction.start":
                    phase = "interaction"
                    session.begin_interaction()
                    await _emit_state(ws, session)
                    continue

                if msg_type == "interaction.end":
                    phase = "interaction"
                    session.end_interaction()
                    await _emit_state(ws, session)
                    continue

                if msg_type == "camera.pointer":
                    phase = "camera"
                    session.apply_pointer(payload)
                    continue

                if msg_type == "camera.wheel":
                    phase = "camera"
                    session.apply_wheel(payload)
                    continue

                if msg_type == "camera.pinch":
                    phase = "camera"
                    session.apply_pinch(payload)
                    continue

                if msg_type in {"render.mode", "visualization.mode", "visualization.switch"}:
                    phase = "render-config"
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
                    phase = "render-config"
                    session.set_render_params(payload)
                    await _emit_state(ws, session)
                    continue

                if msg_type == "control-input":
                    phase = "control-ack"
                    sent_at = payload.get("sentAt")
                    if isinstance(sent_at, (int, float)):
                        rtt_ms = max(0.0, float(time.time_ns() / 1e6 - sent_at))
                        session.stats.add_sample(session.stats.network_latency_ms, rtt_ms)
                    await ws.send_json({"type": "control-ack", "id": payload.get("id"), "sequence": payload.get("sequence")})
                    continue

                if msg_type == "ping":
                    phase = "ping"
                    ts = payload.get("ts")
                    if isinstance(ts, (int, float)):
                        rtt_ms = max(0.0, float(time.time_ns() / 1e6 - ts))
                        session.stats.add_sample(session.stats.network_latency_ms, rtt_ms)
                    await ws.send_json({"type": "pong", "ts": ts})
                    continue

                raise ClientFacingError(
                    "unsupported-message-type",
                    f"unsupported message type: {msg_type}",
                    phase="protocol",
                    retryable=True,
                )
            except ConfigError as exc:
                await _send_ws_error(
                    ws,
                    "config-invalid",
                    str(exc),
                    phase=phase,
                    retryable=False,
                    session_id=session.session_id if session else None,
                )
            except ClientFacingError as exc:
                log.warning(
                    "WS client error phase=%s code=%s session=%s details=%s",
                    exc.phase,
                    exc.code,
                    session.session_id if session else None,
                    exc.details or None,
                )
                await _send_ws_error(
                    ws,
                    exc.code,
                    exc.message,
                    phase=exc.phase,
                    retryable=exc.retryable,
                    session_id=session.session_id if session else None,
                    details=exc.details,
                )
                if exc.close_code is not None:
                    await ws.close(code=exc.close_code)
                    return
            except Exception:
                log.exception("Unhandled websocket error phase=%s session=%s", phase, session.session_id if session else None)
                await _send_ws_error(
                    ws,
                    "internal-error",
                    "Internal server error",
                    phase=phase,
                    retryable=False,
                    session_id=session.session_id if session else None,
                )

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
            session.control_ws = None
            await _close_peer_connection(session)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    global cleanup_task
    if cleanup_task:
        cleanup_task.cancel()
    await sessions.close_all()


@app.on_event("startup")
async def on_startup() -> None:
    global cleanup_task
    STARTUP_WARNINGS.clear()
    STARTUP_ERRORS.clear()
    if not WEB_DIR.exists():
        STARTUP_ERRORS.append(f"web directory not found: {WEB_DIR}")
    if config.dataset_root:
        try:
            dataset_root_path(config.dataset_root)
        except ConfigError as exc:
            STARTUP_ERRORS.append(str(exc))
    if config.dataset_path:
        try:
            resolve_dataset_path(
                config.dataset_path,
                allowed_root=config.dataset_root,
                strict_exists=config.strict_dataset_path,
            )
        except ConfigError as exc:
            if config.strict_dataset_path:
                STARTUP_ERRORS.append(str(exc))
            else:
                STARTUP_WARNINGS.append(str(exc))
    elif config.is_production:
        STARTUP_WARNINGS.append("No VISIVO_DATACUBE_PATH configured; clients must provide datasetPath explicitly")

    backend_turn = any(_has_turn(entry) for entry in config.ice_servers if isinstance(entry, dict))
    client_turn = any(_has_turn(entry) for entry in config.client_ice_servers if isinstance(entry, dict))
    log.warning("Startup config %s", json.dumps(config.sanitized_summary(), sort_keys=True))
    log.warning(
        "Startup ICE summary backend_entries=%s backend_has_turn=%s client_entries=%s client_has_turn=%s",
        len(config.ice_servers),
        backend_turn,
        len(config.client_ice_servers),
        client_turn,
    )
    for warning in STARTUP_WARNINGS:
        log.warning("Startup warning: %s", warning)
    for error in STARTUP_ERRORS:
        log.error("Startup error: %s", error)

    async def _cleanup_loop() -> None:
        while True:
            await sessions.cleanup_idle()
            await asyncio.sleep(config.cleanup_interval_s)

    cleanup_task = asyncio.create_task(_cleanup_loop())
