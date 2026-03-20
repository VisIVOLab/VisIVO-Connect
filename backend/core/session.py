from __future__ import annotations

import asyncio
import threading
import time
import uuid
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from aiortc import RTCPeerConnection

from backend.core.models import FramePacket, RenderStats, VisualizationState
from backend.core.observability import (
    FitsImportMetrics,
    SessionRuntimeMetrics,
    consume_last_fits_import_metrics,
)


@dataclass
class Viewport:
    width: int = 1280
    height: int = 720
    dpr: float = 1.0


class RemoteRenderSession:
    def __init__(self, dataset_path: str | None = None) -> None:
        from backend.rendering.vtk_datacube_renderer import VTKDatacubeRenderer

        self.session_id = str(uuid.uuid4())
        self._session_started_ns = time.time_ns()
        self.renderer = VTKDatacubeRenderer(dataset_path=dataset_path)
        self._session_initialized_ns = time.time_ns()
        self.viewport = Viewport()

        # Quality mode (interactive/high-quality) is independent from visualization mode.
        self.mode = "interactive"
        self.visualization = VisualizationState(
            mode=self.renderer.get_visualization_mode(),
            iso_value=self.renderer.get_iso_value(),
            volume_params=self.renderer.get_volume_params(),
        )

        self.stats = RenderStats()
        self.runtime_metrics = SessionRuntimeMetrics()
        self.runtime_metrics.refresh_memory_rss()
        self.import_metrics: FitsImportMetrics | None = consume_last_fits_import_metrics()

        self._latest_frame: FramePacket | None = None
        self.latest_pipeline_metrics: dict[str, Any] = {}
        self._frame_serial = 0
        self._dirty = True
        self._last_input_ns = 0
        self._last_render_finished_ns = 0
        self._renderer_lock = threading.RLock()
        self._closed = False
        self.last_activity_ns = time.time_ns()
        self.target_stream_fps = 30.0
        self.target_bitrate_mbps = 14.0

        self.peer_connection: RTCPeerConnection | None = None
        self.control_ws: Any | None = None
        self.hello_received_ns: int | None = None
        self.stream_ready_sent_ns: int | None = None
        self.remote_answer_set_ns: int | None = None
        self.ice_relay_only: bool = False
        self.latest_ice_metrics: dict[str, Any] = {}
        self._warmup_task_started = False

        self.request_render()

    def close(self) -> None:
        with self._renderer_lock:
            if self._closed:
                return
            self._closed = True
            try:
                self.renderer.close()
            except Exception:
                pass

    def request_render(self) -> None:
        self.last_activity_ns = time.time_ns()
        self._dirty = True

    def _normalize_quality_mode(self, mode: str | None) -> str | None:
        if not isinstance(mode, str):
            return None
        normalized = mode.strip().lower().replace("_", "-")
        if normalized in {"interactive", "high-quality", "highquality", "hq"}:
            return "interactive" if normalized == "interactive" else "high-quality"
        return None

    def _normalize_visualization_mode(self, mode: str | None) -> str | None:
        if not isinstance(mode, str):
            return None
        normalized = mode.strip().lower().replace("_", "-")
        if normalized in {"volume", "volumetric", "volume-rendering", "volume-render"}:
            return "volume"
        if normalized in {"iso", "isosurface", "iso-surface", "surface"}:
            return "isosurface"
        return None

    def set_mode(self, mode: str) -> None:
        normalized = self._normalize_quality_mode(mode)
        if normalized is None:
            return
        self.mode = normalized
        with self._renderer_lock:
            self.renderer.set_mode(self.mode)
            self.renderer.resize(self.viewport.width, self.viewport.height, self.viewport.dpr)
        self.request_render()

    def begin_interaction(self) -> None:
        self.set_mode("interactive")

    def end_interaction(self) -> None:
        self.set_mode("high-quality")

    def resize(self, width: int, height: int, dpr: float) -> None:
        self.viewport = Viewport(width=max(width, 32), height=max(height, 32), dpr=max(dpr, 0.5))
        with self._renderer_lock:
            self.renderer.resize(self.viewport.width, self.viewport.height, self.viewport.dpr)
        self.request_render()

    def set_visualization_mode(self, mode: str) -> None:
        normalized = self._normalize_visualization_mode(mode)
        if normalized is None:
            return
        self.visualization.mode = normalized
        with self._renderer_lock:
            self.renderer.set_visualization_mode(normalized)
            self.visualization.iso_value = self.renderer.get_iso_value()
        self.request_render()

    def set_visualization_params(self, payload: dict[str, Any]) -> None:
        params = payload.get("params") if isinstance(payload.get("params"), dict) else payload

        mode_value = params.get("visualizationMode", params.get("visualization_mode", params.get("mode")))
        visual_mode = self._normalize_visualization_mode(mode_value)
        if visual_mode is not None:
            self.visualization.mode = visual_mode

        iso_value = params.get("isoValue", params.get("iso_value"))
        if isinstance(iso_value, (int, float)):
            self.visualization.iso_value = float(iso_value)

        volume_params = params.get("volume", params.get("volumeParams", params.get("volume_params")))
        if isinstance(volume_params, dict):
            self.visualization.volume_params = dict(volume_params)

        with self._renderer_lock:
            self.renderer.set_visualization_mode(self.visualization.mode)
            if self.visualization.iso_value is not None:
                self.renderer.set_iso_value(self.visualization.iso_value)
            if self.visualization.volume_params:
                self.renderer.set_volume_params(self.visualization.volume_params)
            self.visualization.iso_value = self.renderer.get_iso_value()
            self.visualization.volume_params = self.renderer.get_volume_params()
        self.request_render()

    def apply_pointer(self, payload: dict[str, Any]) -> None:
        action = payload.get("action")
        if action != "move":
            return

        dx = float(payload.get("dx", 0.0))
        dy = float(payload.get("dy", 0.0))
        buttons = int(payload.get("buttons", 1) or 1)

        move_mode = "pan" if buttons == 2 else "rotate"
        with self._renderer_lock:
            self.renderer.apply_pointer_delta(dx, dy, mode=move_mode)
        self._last_input_ns = time.time_ns()
        self.request_render()

    def apply_wheel(self, payload: dict[str, Any]) -> None:
        mode = payload.get("mode", "zoom")
        dx = float(payload.get("deltaX", 0.0))
        dy = float(payload.get("deltaY", 0.0))

        if mode == "pan":
            with self._renderer_lock:
                self.renderer.apply_pointer_delta(dx / 600.0, dy / 600.0, mode="pan")
        else:
            zoom = 1.0 + max(min(-dy / 1200.0, 0.3), -0.3)
            with self._renderer_lock:
                self.renderer.apply_zoom(zoom)

        self._last_input_ns = time.time_ns()
        self.request_render()

    def apply_pinch(self, payload: dict[str, Any]) -> None:
        scale = float(payload.get("scale", 1.0))
        if scale <= 0.0:
            return
        zoom = 1.0 / max(min(scale, 1.8), 0.55)
        with self._renderer_lock:
            self.renderer.apply_zoom(zoom)
        self._last_input_ns = time.time_ns()
        self.request_render()

    def set_render_params(self, payload: dict[str, Any]) -> None:
        params = payload.get("params", {})
        if not isinstance(params, dict):
            params = {}

        render_scale = params.get("scale", payload.get("scale"))
        target_fps = params.get("targetFps", payload.get("targetFps"))
        bitrate_mbps = params.get("bitrateMbps", params.get("bitrate", payload.get("bitrateMbps", payload.get("bitrate"))))

        mode_value = params.get("mode", payload.get("mode"))
        quality_mode = self._normalize_quality_mode(mode_value)
        visual_mode = self._normalize_visualization_mode(mode_value)

        explicit_visual_mode = self._normalize_visualization_mode(
            params.get("visualizationMode", params.get("visualization_mode", payload.get("visualizationMode")))
        )
        if explicit_visual_mode is not None:
            visual_mode = explicit_visual_mode

        if isinstance(render_scale, (int, float)):
            with self._renderer_lock:
                self.renderer.set_user_render_scale(float(render_scale))
                self.renderer.resize(self.viewport.width, self.viewport.height, self.viewport.dpr)

        if isinstance(target_fps, (int, float)):
            self.target_stream_fps = min(max(float(target_fps), 5.0), 60.0)

        if isinstance(bitrate_mbps, (int, float)):
            self.target_bitrate_mbps = min(max(float(bitrate_mbps), 1.0), 50.0)

        if quality_mode is not None:
            self.set_mode(quality_mode)

        if visual_mode is not None:
            self.visualization.mode = visual_mode

        iso_value = params.get("isoValue", params.get("iso_value", payload.get("isoValue")))
        if isinstance(iso_value, (int, float)):
            self.visualization.iso_value = float(iso_value)

        volume_params = params.get("volume", params.get("volumeParams", params.get("volume_params", payload.get("volume"))))
        if isinstance(volume_params, dict):
            self.visualization.volume_params = dict(volume_params)

        with self._renderer_lock:
            self.renderer.set_visualization_mode(self.visualization.mode)
            if self.visualization.iso_value is not None:
                self.renderer.set_iso_value(self.visualization.iso_value)
            if self.visualization.volume_params:
                self.renderer.set_volume_params(self.visualization.volume_params)
            self.visualization.iso_value = self.renderer.get_iso_value()
            self.visualization.volume_params = self.renderer.get_volume_params()

        if quality_mode is None:
            self.request_render()

    def state_payload(self, text: str | None = None) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "type": "state",
            "mode": self.mode,
            "visualizationMode": self.visualization.mode,
            "isoValue": self.visualization.iso_value,
            "volume": self.renderer.get_volume_params(),
            "rendererDiagnostics": self.renderer.get_renderer_diagnostics(),
        }
        scalar_lo, scalar_hi = self.renderer.get_scalar_range()
        payload["isoRangeMin"] = scalar_lo
        payload["isoRangeMax"] = scalar_hi
        if text:
            payload["text"] = text
        return payload

    def mark_hello_received(self) -> None:
        if self.hello_received_ns is None:
            self.hello_received_ns = time.time_ns()
            self.runtime_metrics.first_frame_session_init_ms = max(
                0.0, (self._session_initialized_ns - self._session_started_ns) / 1e6
            )
            if self.import_metrics is not None:
                self.runtime_metrics.first_frame_fits_load_ms = self.import_metrics.fits_total_ms
                self.runtime_metrics.first_frame_sanitize_convert_ms = self.import_metrics.sanitize_convert_ms
                self.runtime_metrics.first_frame_vtk_build_ms = self.import_metrics.vtk_build_ms
            renderer_warmup_total = getattr(self.renderer, "get_warmup_metrics", lambda: {})().get("totalRendererWarmupMs")
            if isinstance(renderer_warmup_total, (int, float)):
                self.runtime_metrics.first_frame_renderer_warmup_ms = float(renderer_warmup_total)
            elif self.import_metrics is not None:
                self.runtime_metrics.first_frame_renderer_warmup_ms = max(
                    0.0,
                    self.runtime_metrics.first_frame_session_init_ms - self.import_metrics.fits_total_ms,
                )

    def mark_stream_ready_sent(self) -> None:
        if self.stream_ready_sent_ns is None:
            self.stream_ready_sent_ns = time.time_ns()

    def mark_remote_answer_set(self) -> None:
        if self.remote_answer_set_ns is None:
            self.remote_answer_set_ns = time.time_ns()

    def prime_first_frame(self) -> None:
        if self._latest_frame is not None:
            return
        with self._renderer_lock:
            self.renderer.prewarm_volume_renderer()
        self.render_if_needed(force=True)

    def maybe_start_warmup_task(self) -> bool:
        if self._warmup_task_started or self._latest_frame is not None or self._closed:
            return False
        self._warmup_task_started = True
        return True

    def latest_frame(self) -> FramePacket | None:
        return self._latest_frame

    def render_if_needed(self, force: bool = False) -> FramePacket | None:
        if self._closed:
            return None
        now_ns = time.time_ns()
        if not force and self._last_render_finished_ns:
            elapsed_s = (now_ns - self._last_render_finished_ns) / 1e9
            if not self._dirty and elapsed_s < self.renderer.target_update_interval:
                return self._latest_frame

        with self._renderer_lock:
            frame_rgb, started_ns, finished_ns, pipeline_metrics = self.renderer.render_rgb_frame()
        render_ms = float(pipeline_metrics.get("renderTimeMs", (finished_ns - started_ns) / 1e6))
        self.stats.add_sample(self.stats.render_time_ms, render_ms)
        capture_ms = pipeline_metrics.get("frameCaptureReadbackTimeMs")
        if isinstance(capture_ms, (int, float)):
            self.stats.add_sample(self.stats.frame_capture_time_ms, float(capture_ms))
        conversion_ms = pipeline_metrics.get("frameConversionTimeMs")
        if isinstance(conversion_ms, (int, float)):
            self.stats.add_sample(self.stats.frame_conversion_time_ms, float(conversion_ms))
        total_pipeline_ms = pipeline_metrics.get("totalFramePipelineTimeMs")
        if isinstance(total_pipeline_ms, (int, float)):
            self.stats.add_sample(self.stats.total_frame_pipeline_time_ms, float(total_pipeline_ms))
        self.runtime_metrics.record_render(
            mode=self.mode,
            render_ms=render_ms,
            finished_ns=finished_ns,
            session_started_ns=self._session_started_ns,
        )
        self._adapt_interactive_quality(render_ms)

        if self._last_input_ns:
            input_to_visible_ms = (finished_ns - self._last_input_ns) / 1e6
            if 0.0 <= input_to_visible_ms < 5000.0:
                self.stats.add_sample(self.stats.input_to_visible_latency_ms, input_to_visible_ms)

        if self._latest_frame is not None:
            self.stats.dropped_frames += 1
        self._frame_serial += 1
        self._latest_frame = FramePacket(
            serial=self._frame_serial,
            frame_rgb=frame_rgb,
            render_started_ns=started_ns,
            render_finished_ns=finished_ns,
            mode=self.mode,
            pipeline_metrics=dict(pipeline_metrics),
        )
        self.latest_pipeline_metrics = dict(pipeline_metrics)
        self._last_render_finished_ns = finished_ns
        self._dirty = False
        return self._latest_frame

    def record_first_frame_delivery(self, *, encode_ms: float, send_ms: float, delivered_ns: int) -> None:
        if self.runtime_metrics.first_frame_render_ms is not None:
            return
        pipeline = dict(self.latest_pipeline_metrics)
        self.runtime_metrics.first_frame_render_ms = float(pipeline.get("renderTimeMs", 0.0))
        self.runtime_metrics.first_frame_capture_ms = float(pipeline.get("frameCaptureReadbackTimeMs", 0.0))
        self.runtime_metrics.first_frame_conversion_ms = float(pipeline.get("frameConversionTimeMs", 0.0))
        self.runtime_metrics.first_frame_encode_ms = float(encode_ms)
        self.runtime_metrics.first_frame_send_ms = float(send_ms)
        if self.remote_answer_set_ns is not None:
            self.runtime_metrics.first_frame_signaling_setup_ms = max(
                0.0, (self.remote_answer_set_ns - self._session_started_ns) / 1e6
            )
        elif self.stream_ready_sent_ns is not None:
            self.runtime_metrics.first_frame_signaling_setup_ms = max(
                0.0, (self.stream_ready_sent_ns - self._session_started_ns) / 1e6
            )
        self.runtime_metrics.first_frame_latency_ms = max(0.0, (delivered_ns - self._session_started_ns) / 1e6)

    def _adapt_interactive_quality(self, render_ms: float) -> None:
        if self.mode != "interactive":
            with self._renderer_lock:
                if self.renderer.interactive_boost != 1.0:
                    self.renderer.set_interactive_boost(1.0)
            return

        if render_ms > 60.0:
            with self._renderer_lock:
                self.renderer.set_interactive_boost(self.renderer.interactive_boost * 1.1)
        elif render_ms < 28.0:
            with self._renderer_lock:
                self.renderer.set_interactive_boost(self.renderer.interactive_boost * 0.95)


class SessionManager:
    def __init__(
        self,
        max_sessions: int = 16,
        idle_timeout_s: int = 900,
        session_factory: Callable[[str | None], RemoteRenderSession] | None = None,
    ) -> None:
        self._sessions: dict[str, RemoteRenderSession] = {}
        self._lock = asyncio.Lock()
        self.max_sessions = max(1, int(max_sessions))
        self.idle_timeout_ns = max(30, int(idle_timeout_s)) * 1_000_000_000
        self.session_factory = session_factory or RemoteRenderSession

    async def create(self, dataset_path: str | None = None, session_id: str | None = None) -> RemoteRenderSession:
        async with self._lock:
            if session_id and session_id in self._sessions:
                return self._sessions[session_id]
            if len(self._sessions) >= self.max_sessions:
                await self._evict_oldest_locked()
            session = self.session_factory(dataset_path)
            if session_id:
                session.session_id = session_id
            self._sessions[session.session_id] = session
            return session

    async def get(self, session_id: str) -> RemoteRenderSession | None:
        async with self._lock:
            return self._sessions.get(session_id)

    async def get_or_create(self, session_id: str | None, dataset_path: str | None = None) -> RemoteRenderSession:
        if session_id:
            existing = await self.get(session_id)
            if existing:
                return existing
        return await self.create(dataset_path=dataset_path, session_id=session_id)

    async def close(self, session_id: str) -> None:
        async with self._lock:
            session = self._sessions.pop(session_id, None)
        if session:
            if session.peer_connection:
                await session.peer_connection.close()
            session.close()

    async def close_all(self) -> None:
        async with self._lock:
            ids = list(self._sessions)
        for sid in ids:
            await self.close(sid)

    async def cleanup_idle(self) -> int:
        now_ns = time.time_ns()
        async with self._lock:
            idle_ids = [
                sid
                for sid, session in self._sessions.items()
                if now_ns - session.last_activity_ns > self.idle_timeout_ns
            ]
        for sid in idle_ids:
            await self.close(sid)
        return len(idle_ids)

    async def _evict_oldest_locked(self) -> None:
        if not self._sessions:
            return
        oldest_id = min(self._sessions, key=lambda sid: self._sessions[sid].last_activity_ns)
        session = self._sessions.pop(oldest_id)
        if session.peer_connection:
            await session.peer_connection.close()
        session.close()
