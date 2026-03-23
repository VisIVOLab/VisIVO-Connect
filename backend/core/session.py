from __future__ import annotations

import asyncio
import threading
import time
import uuid
import gc
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable

if TYPE_CHECKING:
    from aiortc import RTCPeerConnection

from backend.core.models import FramePacket, RenderStats, VisualizationState
from backend.core.config import dataset_relative_path, load_config
from backend.core.observability import (
    FitsImportMetrics,
    SessionRuntimeMetrics,
    consume_last_fits_import_details,
    consume_last_fits_import_metrics,
)


@dataclass
class Viewport:
    width: int = 1280
    height: int = 720
    dpr: float = 1.0


@dataclass
class _RendererSlot:
    renderer_id: str
    renderer: Any
    render_lock: threading.Lock = field(default_factory=threading.Lock)
    in_use_count: int = 0
    retired: bool = False
    retired_ns: int | None = None


class RemoteRenderSession:
    @staticmethod
    def _next_renderer_id() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def _create_renderer(dataset_path: str | None, *, dataset_load_mode: str) -> Any:
        from backend.rendering.vtk_datacube_renderer import VTKDatacubeRenderer

        try:
            return VTKDatacubeRenderer(dataset_path=dataset_path, dataset_load_mode=dataset_load_mode)
        except TypeError:
            return VTKDatacubeRenderer(dataset_path=dataset_path)

    def __init__(self, dataset_path: str | None = None) -> None:
        config = load_config()
        self.session_id = str(uuid.uuid4())
        self._session_started_ns = time.time_ns()
        self.renderer = self._create_renderer(dataset_path, dataset_load_mode="auto")
        self._active_renderer_slot = _RendererSlot(renderer_id=self._next_renderer_id(), renderer=self.renderer)
        self._retired_renderer_slots: list[_RendererSlot] = []
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
        self.import_details: dict[str, Any] | None = consume_last_fits_import_details()
        self.loading_state: dict[str, Any] = self._initial_loading_state(dataset_path)

        self._latest_frame: FramePacket | None = None
        self.latest_pipeline_metrics: dict[str, Any] = {}
        self._frame_serial = 0
        self._dirty = True
        self._last_input_ns = 0
        self._last_render_finished_ns = 0
        self._renderer_lock = threading.RLock()
        self._closed = False
        self.last_activity_ns = time.time_ns()
        self.target_stream_fps = float(config.default_target_fps)
        self.target_bitrate_mbps = float(config.default_bitrate_mbps)
        self.requested_bitrate_mbps = float(config.default_bitrate_mbps)
        self.requested_render_scale = 1.0
        self.adaptive_scaling_enabled = True
        self.adaptive_viewport_active_in_interactive_only = True
        self.current_viewport_scale = 1.0
        self.last_scale_update_ts = 0.0
        self.smoothed_pipeline_ms: float | None = None
        self._adaptive_scale_started = False
        self.adaptive_bitrate_enabled = True
        self.current_adaptive_bitrate_mbps = float(config.default_bitrate_mbps)
        self.last_bitrate_update_ts = 0.0
        self._adaptive_bitrate_started = False
        self._adaptive_bitrate_min_mbps = 4.0
        self._adaptive_bitrate_max_mbps = 40.0

        self.peer_connection: RTCPeerConnection | None = None
        self.control_ws: Any | None = None
        self.hello_received_ns: int | None = None
        self.stream_ready_sent_ns: int | None = None
        self.remote_answer_set_ns: int | None = None
        self.ice_relay_only: bool = False
        self.latest_ice_metrics: dict[str, Any] = {}
        self._warmup_task_started = False
        self.requested_quality_profiles: dict[str, Any] = {}
        self._refine_task: asyncio.Task[None] | None = None
        self._renderer_swap_in_progress = False
        self._last_renderer_swap_error: str | None = None
        self._egl_context_error_detected = False

        self._refresh_renderer_diagnostics_state()
        self.request_render()

    def _dataset_load_mode(self) -> str:
        if isinstance(self.import_details, dict):
            mode = self.import_details.get("datasetLoadMode")
            if isinstance(mode, str) and mode in {"preview", "full"}:
                return mode
        return "full"

    def _is_large_dataset(self) -> bool:
        return bool(isinstance(self.import_details, dict) and self.import_details.get("largeDataset"))

    def _should_refine_full_resolution(self) -> bool:
        return self._dataset_load_mode() == "preview" and self._is_large_dataset()

    def _initial_loading_state(self, dataset_path: str | None) -> dict[str, Any]:
        state = {
            "active": False,
            "phase": None,
            "label": None,
            "datasetPath": dataset_path,
            "datasetLoadMode": self._dataset_load_mode(),
            "largeDataset": self._is_large_dataset(),
            "refinePending": self._should_refine_full_resolution(),
            "refineScheduled": False,
            "refineRunning": False,
            "refineCompleted": False,
            "refineFailed": False,
            "activeRepresentation": "preview" if self._dataset_load_mode() == "preview" else "full",
            "fullRendererReadyForSwap": False,
            "lastRefineError": None,
            "previewPinnedUntilFullReady": self._dataset_load_mode() == "preview",
            "rendererSwapInProgress": False,
            "activeRendererId": getattr(getattr(self, "_active_renderer_slot", None), "renderer_id", None),
            "retiredRendererCount": len(getattr(self, "_retired_renderer_slots", [])),
            "lastRendererSwapError": None,
            "eglContextErrorDetected": False,
        }
        state.update(self._background_refine_policy())
        if not state.get("backgroundRefineEnabled"):
            state["refinePending"] = False
            state["previewPinnedUntilFullReady"] = False
        return state

    def _refresh_renderer_diagnostics_state(self) -> None:
        self.loading_state.update(
            {
                "rendererSwapInProgress": self._renderer_swap_in_progress,
                "activeRendererId": self._active_renderer_slot.renderer_id if self._active_renderer_slot is not None else None,
                "retiredRendererCount": len(self._retired_renderer_slots),
                "lastRendererSwapError": self._last_renderer_swap_error,
                "eglContextErrorDetected": self._egl_context_error_detected,
            }
        )

    def _checkout_active_renderer_slot(self) -> _RendererSlot:
        with self._renderer_lock:
            slot = self._active_renderer_slot
            slot.in_use_count += 1
            return slot

    def _release_renderer_slot(self, slot: _RendererSlot) -> None:
        slots_to_close: list[_RendererSlot] = []
        with self._renderer_lock:
            slot.in_use_count = max(0, slot.in_use_count - 1)
            slots_to_close = self._collect_retired_renderer_slots_locked()
            self._refresh_renderer_diagnostics_state()
        self._close_retired_renderer_slots(slots_to_close)

    def _collect_retired_renderer_slots_locked(self) -> list[_RendererSlot]:
        ready: list[_RendererSlot] = []
        keep: list[_RendererSlot] = []
        now_ns = time.time_ns()
        for slot in self._retired_renderer_slots:
            retired_long_enough = slot.retired_ns is not None and (now_ns - slot.retired_ns) >= 250_000_000
            if slot.in_use_count == 0 and retired_long_enough:
                ready.append(slot)
            else:
                keep.append(slot)
        self._retired_renderer_slots = keep
        return ready

    def _close_retired_renderer_slots(self, slots: list[_RendererSlot]) -> None:
        for slot in slots:
            close_renderer = getattr(slot.renderer, "close", None)
            if callable(close_renderer):
                try:
                    close_renderer()
                except Exception:
                    pass

    def _retire_renderer_slot_locked(self, slot: _RendererSlot) -> None:
        slot.retired = True
        slot.retired_ns = time.time_ns()
        self._retired_renderer_slots.append(slot)

    def _background_refine_policy(self) -> dict[str, Any]:
        renderer_backend = None
        try:
            renderer_backend = self.renderer.get_renderer_diagnostics().get("renderWindowBackend")
        except Exception:
            renderer_backend = None

        enabled = self._should_refine_full_resolution()
        deferred = False
        reason: str | None = None
        if enabled and sys.platform == "darwin" and renderer_backend in {"vtkRenderWindow", "vtkCocoaRenderWindow"}:
            enabled = False
            deferred = True
            reason = "cocoa-main-thread-only"
        if enabled and renderer_backend == "vtkEGLRenderWindow":
            enabled = False
            deferred = True
            reason = "egl-background-refine-unsafe"

        return {
            "backgroundRefineEnabled": enabled,
            "backgroundRefineDeferred": deferred,
            "backgroundRefineDeferredReason": reason,
        }

    def set_loading_state(self, *, active: bool, phase: str | None, label: str | None) -> None:
        background_refine = self._background_refine_policy()
        self.loading_state.update(
            {
                "active": bool(active),
                "phase": phase,
                "label": label,
                "datasetPath": getattr(self.renderer, "dataset_path", None),
                "datasetLoadMode": self._dataset_load_mode(),
                "largeDataset": self._is_large_dataset(),
                "refinePending": self._should_refine_full_resolution() and background_refine["backgroundRefineEnabled"],
                **background_refine,
            }
        )
        if not self.loading_state.get("backgroundRefineEnabled"):
            self.loading_state["refinePending"] = False
            self.loading_state["previewPinnedUntilFullReady"] = False
        self._refresh_renderer_diagnostics_state()

    def mark_refine_pending(self, pending: bool) -> None:
        self.loading_state["refinePending"] = bool(pending)

    def cancel_background_tasks(self) -> None:
        if self._refine_task is not None:
            self._refine_task.cancel()
            self._refine_task = None

    def close(self) -> None:
        slots_to_close: list[_RendererSlot] = []
        with self._renderer_lock:
            if self._closed:
                return
            self._closed = True
            self.cancel_background_tasks()
            slots_to_close = [self._active_renderer_slot, *self._retired_renderer_slots]
            self._retired_renderer_slots = []
        self._close_retired_renderer_slots(slots_to_close)

    def request_render(self) -> None:
        self.last_activity_ns = time.time_ns()
        self._dirty = True

    def _effective_viewport_scale(self) -> float:
        requested = min(max(float(self.requested_render_scale), 0.4), 2.0)
        adaptive = 1.0
        adaptive_active = self.adaptive_scaling_enabled and (
            not self.adaptive_viewport_active_in_interactive_only or self.mode == "interactive"
        )
        if adaptive_active:
            adaptive = min(max(float(self.current_viewport_scale), 0.5), 1.0)
        return min(max(requested * adaptive, 0.4), 2.0)

    def _apply_renderer_scale_locked(self, renderer: Any) -> None:
        renderer.set_user_render_scale(self._effective_viewport_scale())
        renderer.resize(self.viewport.width, self.viewport.height, self.viewport.dpr)

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
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                slot.renderer.set_mode(self.mode)
                self._apply_renderer_scale_locked(slot.renderer)
        finally:
            self._release_renderer_slot(slot)
        self.request_render()

    def begin_interaction(self) -> None:
        self.set_mode("interactive")

    def end_interaction(self) -> None:
        self.set_mode("high-quality")

    def resize(self, width: int, height: int, dpr: float) -> None:
        self.viewport = Viewport(width=max(width, 32), height=max(height, 32), dpr=max(dpr, 0.5))
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                self._apply_renderer_scale_locked(slot.renderer)
        finally:
            self._release_renderer_slot(slot)
        self.request_render()

    def set_visualization_mode(self, mode: str) -> None:
        normalized = self._normalize_visualization_mode(mode)
        if normalized is None:
            return
        self.visualization.mode = normalized
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                slot.renderer.set_visualization_mode(normalized)
                self.visualization.iso_value = slot.renderer.get_iso_value()
        finally:
            self._release_renderer_slot(slot)
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

        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                slot.renderer.set_visualization_mode(self.visualization.mode)
                if self.visualization.iso_value is not None:
                    slot.renderer.set_iso_value(self.visualization.iso_value)
                if self.visualization.volume_params:
                    slot.renderer.set_volume_params(self.visualization.volume_params)
                self.visualization.iso_value = slot.renderer.get_iso_value()
                self.visualization.volume_params = slot.renderer.get_volume_params()
        finally:
            self._release_renderer_slot(slot)
        self.request_render()

    def apply_pointer(self, payload: dict[str, Any]) -> None:
        action = payload.get("action")
        if action != "move":
            return

        dx = float(payload.get("dx", 0.0))
        dy = float(payload.get("dy", 0.0))
        buttons = int(payload.get("buttons", 1) or 1)

        move_mode = "pan" if buttons == 2 else "rotate"
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                slot.renderer.apply_pointer_delta(dx, dy, mode=move_mode)
        finally:
            self._release_renderer_slot(slot)
        self._last_input_ns = time.time_ns()
        self.request_render()

    def apply_wheel(self, payload: dict[str, Any]) -> None:
        mode = payload.get("mode", "zoom")
        dx = float(payload.get("deltaX", 0.0))
        dy = float(payload.get("deltaY", 0.0))

        if mode == "pan":
            slot = self._checkout_active_renderer_slot()
            try:
                with slot.render_lock:
                    slot.renderer.apply_pointer_delta(dx / 600.0, dy / 600.0, mode="pan")
            finally:
                self._release_renderer_slot(slot)
        else:
            zoom = 1.0 + max(min(-dy / 1200.0, 0.3), -0.3)
            slot = self._checkout_active_renderer_slot()
            try:
                with slot.render_lock:
                    slot.renderer.apply_zoom(zoom)
            finally:
                self._release_renderer_slot(slot)

        self._last_input_ns = time.time_ns()
        self.request_render()

    def apply_pinch(self, payload: dict[str, Any]) -> None:
        scale = float(payload.get("scale", 1.0))
        if scale <= 0.0:
            return
        zoom = 1.0 / max(min(scale, 1.8), 0.55)
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                slot.renderer.apply_zoom(zoom)
        finally:
            self._release_renderer_slot(slot)
        self._last_input_ns = time.time_ns()
        self.request_render()

    def update_slice_pointer(self, payload: dict[str, Any]) -> dict[str, Any] | None:
        x_norm = payload.get("xNorm", payload.get("x"))
        y_norm = payload.get("yNorm", payload.get("y"))
        if not isinstance(x_norm, (int, float)) or not isinstance(y_norm, (int, float)):
            return None
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                return slot.renderer.update_pointer_readout(float(x_norm), float(y_norm))
        finally:
            self._release_renderer_slot(slot)

    def set_render_params(self, payload: dict[str, Any]) -> None:
        params = payload.get("params", {})
        if not isinstance(params, dict):
            params = {}

        render_scale = params.get("scale", payload.get("scale"))
        target_fps = params.get("targetFps", payload.get("targetFps"))
        bitrate_mbps = params.get("bitrateMbps", params.get("bitrate", payload.get("bitrateMbps", payload.get("bitrate"))))
        quality_profiles = params.get("qualityProfiles", payload.get("qualityProfiles"))

        mode_value = params.get("mode", payload.get("mode"))
        quality_mode = self._normalize_quality_mode(mode_value)
        visual_mode = self._normalize_visualization_mode(mode_value)

        explicit_visual_mode = self._normalize_visualization_mode(
            params.get("visualizationMode", params.get("visualization_mode", payload.get("visualizationMode")))
        )
        if explicit_visual_mode is not None:
            visual_mode = explicit_visual_mode

        if isinstance(render_scale, (int, float)):
            self.requested_render_scale = min(max(float(render_scale), 0.4), 2.0)
            slot = self._checkout_active_renderer_slot()
            try:
                with slot.render_lock:
                    self._apply_renderer_scale_locked(slot.renderer)
            finally:
                self._release_renderer_slot(slot)

        if isinstance(target_fps, (int, float)):
            self.target_stream_fps = min(max(float(target_fps), 5.0), 60.0)

        if isinstance(bitrate_mbps, (int, float)):
            self.requested_bitrate_mbps = min(max(float(bitrate_mbps), 1.0), 50.0)
            bounded = min(max(self.requested_bitrate_mbps, self._adaptive_bitrate_min_mbps), self._adaptive_bitrate_max_mbps)
            self.current_adaptive_bitrate_mbps = bounded
            self.target_bitrate_mbps = bounded
            self.last_bitrate_update_ts = 0.0
            self._adaptive_bitrate_started = False

        if isinstance(quality_profiles, dict):
            normalized_profiles: dict[str, Any] = {}
            interactive = quality_profiles.get("interactive")
            if isinstance(interactive, dict):
                normalized_profiles["interactive"] = dict(interactive)
            high_quality = quality_profiles.get("highQuality", quality_profiles.get("high-quality"))
            if isinstance(high_quality, dict):
                normalized_profiles["highQuality"] = dict(high_quality)
            if normalized_profiles:
                self.requested_quality_profiles = normalized_profiles

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

        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                slot.renderer.set_visualization_mode(self.visualization.mode)
                if self.visualization.iso_value is not None:
                    slot.renderer.set_iso_value(self.visualization.iso_value)
                if self.visualization.volume_params:
                    slot.renderer.set_volume_params(self.visualization.volume_params)
                self.visualization.iso_value = slot.renderer.get_iso_value()
                self.visualization.volume_params = slot.renderer.get_volume_params()
        finally:
            self._release_renderer_slot(slot)

        if quality_mode is None:
            self.request_render()

    def state_payload(self, text: str | None = None) -> dict[str, Any]:
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                dataset_path = getattr(slot.renderer, "dataset_path", None)
                volume_params = slot.renderer.get_volume_params()
                renderer_diagnostics = slot.renderer.get_renderer_diagnostics()
                scalar_lo, scalar_hi = slot.renderer.get_scalar_range()
                iso_lo, iso_hi = slot.renderer.get_iso_range() if hasattr(slot.renderer, "get_iso_range") else (scalar_lo, scalar_hi)
                slice_reference = slot.renderer.get_slice_reference()
                pointer_readout = slot.renderer.get_last_pointer_readout()
        finally:
            self._release_renderer_slot(slot)
        payload: dict[str, Any] = {
            "type": "state",
            "datasetPath": dataset_path,
            "datasetRelativePath": dataset_relative_path(dataset_path, allowed_root=load_config().dataset_root),
            "datasetName": Path(dataset_path.split("#", 1)[0]).name if isinstance(dataset_path, str) and dataset_path else None,
            "mode": self.mode,
            "visualizationMode": self.visualization.mode,
            "isoValue": self.visualization.iso_value,
            "volume": volume_params,
            "rendererDiagnostics": {
                **renderer_diagnostics,
                "refinePending": bool(self.loading_state.get("refinePending")),
                "refineScheduled": bool(self.loading_state.get("refineScheduled")),
                "refineRunning": bool(self.loading_state.get("refineRunning")),
                "refineCompleted": bool(self.loading_state.get("refineCompleted")),
                "refineFailed": bool(self.loading_state.get("refineFailed")),
                "datasetLoadingActive": bool(self.loading_state.get("active")),
                "backgroundRefineEnabled": bool(self.loading_state.get("backgroundRefineEnabled")),
                "backgroundRefineDeferred": bool(self.loading_state.get("backgroundRefineDeferred")),
                "backgroundRefineDeferredReason": self.loading_state.get("backgroundRefineDeferredReason"),
                "activeRepresentation": self.loading_state.get("activeRepresentation"),
                "fullRendererReadyForSwap": bool(self.loading_state.get("fullRendererReadyForSwap")),
                "lastRefineError": self.loading_state.get("lastRefineError"),
                "previewPinnedUntilFullReady": bool(self.loading_state.get("previewPinnedUntilFullReady")),
                "rendererSwapInProgress": bool(self.loading_state.get("rendererSwapInProgress")),
                "activeRendererId": self.loading_state.get("activeRendererId"),
                "retiredRendererCount": self.loading_state.get("retiredRendererCount"),
                "lastRendererSwapError": self.loading_state.get("lastRendererSwapError"),
                "eglContextErrorDetected": bool(self.loading_state.get("eglContextErrorDetected")),
                "adaptiveScalingEnabled": bool(self.adaptive_scaling_enabled),
                "adaptiveViewportActiveInInteractiveOnly": bool(self.adaptive_viewport_active_in_interactive_only),
                "currentViewportScale": float(self.current_viewport_scale),
                "smoothedPipelineMs": self.smoothed_pipeline_ms,
                "adaptiveBitrateEnabled": bool(self.adaptive_bitrate_enabled),
                "currentAdaptiveBitrateMbps": float(self.current_adaptive_bitrate_mbps),
            },
            "datasetLoading": dict(self.loading_state),
            "sliceReference": slice_reference,
            "slicePointerReadout": pointer_readout,
        }
        payload["isoRangeMin"] = iso_lo
        payload["isoRangeMax"] = iso_hi
        if text:
            payload["text"] = text
        return payload

    def switch_dataset(self, dataset_path: str) -> None:
        slots_to_close: list[_RendererSlot] = []
        with self._renderer_lock:
            self.cancel_background_tasks()
            previous_slot = self._active_renderer_slot
            replacement = self._create_renderer(dataset_path, dataset_load_mode="auto")
            self._apply_renderer_scale_locked(replacement)
            replacement.set_mode(self.mode)
            replacement.set_visualization_mode(self.visualization.mode)
            if self.visualization.iso_value is not None:
                replacement.set_iso_value(self.visualization.iso_value)
            if self.visualization.volume_params:
                replacement.set_volume_params(self.visualization.volume_params)
            self.renderer = replacement
            self._renderer_swap_in_progress = True
            self._active_renderer_slot = _RendererSlot(renderer_id=self._next_renderer_id(), renderer=replacement)
            self._retire_renderer_slot_locked(previous_slot)
            self.visualization = VisualizationState(
                mode=self.renderer.get_visualization_mode(),
                iso_value=self.renderer.get_iso_value(),
                volume_params=self.renderer.get_volume_params(),
            )
            self.import_metrics = consume_last_fits_import_metrics()
            self.import_details = consume_last_fits_import_details()
            self.runtime_metrics = SessionRuntimeMetrics()
            self.runtime_metrics.refresh_memory_rss()
            self.stats = RenderStats()
            self._latest_frame = None
            self.latest_pipeline_metrics = {}
            self.requested_render_scale = min(max(float(self.requested_render_scale), 0.4), 2.0)
            self.current_viewport_scale = 1.0
            self.last_scale_update_ts = 0.0
            self.smoothed_pipeline_ms = None
            self._adaptive_scale_started = False
            self.current_adaptive_bitrate_mbps = min(
                max(float(self.requested_bitrate_mbps), self._adaptive_bitrate_min_mbps),
                self._adaptive_bitrate_max_mbps,
            )
            self.target_bitrate_mbps = self.current_adaptive_bitrate_mbps
            self.last_bitrate_update_ts = 0.0
            self._adaptive_bitrate_started = False
            self._frame_serial = 0
            self._dirty = True
            self._last_input_ns = 0
            self._last_render_finished_ns = 0
            self._warmup_task_started = False
            self._session_started_ns = time.time_ns()
            self._session_initialized_ns = self._session_started_ns
            self.hello_received_ns = None
            self.stream_ready_sent_ns = None
            self.remote_answer_set_ns = None
            self.loading_state = self._initial_loading_state(dataset_path)
            self._renderer_swap_in_progress = False
            self._last_renderer_swap_error = None
            self._refresh_renderer_diagnostics_state()
            slots_to_close = self._collect_retired_renderer_slots_locked()
        self._close_retired_renderer_slots(slots_to_close)
        if self._is_large_dataset():
            gc.collect()

    def can_schedule_full_resolution_refine(self) -> bool:
        if self._closed or not self._should_refine_full_resolution():
            return False
        policy = self._background_refine_policy()
        self.loading_state.update(policy)
        if not policy["backgroundRefineEnabled"]:
            self.loading_state["refinePending"] = False
            return False
        if self.loading_state.get("refineScheduled") or self.loading_state.get("refineRunning"):
            return False
        if self.loading_state.get("refineCompleted") or self.loading_state.get("refineFailed"):
            return False
        if self._refine_task is not None and not self._refine_task.done():
            return False
        return True

    @staticmethod
    def _build_full_resolution_candidate(
        dataset_path: str,
        *,
        viewport: Viewport,
        mode: str,
        visualization_mode: str,
        iso_value: float | None,
        volume_params: dict[str, Any],
        camera_state: dict[str, Any] | None,
    ) -> tuple[Any, FitsImportMetrics | None, dict[str, Any] | None]:
        renderer = RemoteRenderSession._create_renderer(dataset_path, dataset_load_mode="full")
        renderer.set_user_render_scale(1.0)
        renderer.resize(viewport.width, viewport.height, viewport.dpr)
        renderer.set_mode(mode)
        renderer.set_visualization_mode(visualization_mode)
        if iso_value is not None:
            renderer.set_iso_value(iso_value)
        if volume_params:
            renderer.set_volume_params(volume_params)
        if camera_state:
            renderer.apply_camera_state(camera_state)
        frame_rgb, _, _, _ = renderer.render_rgb_frame()
        if getattr(frame_rgb, "size", 0) <= 0 or len(getattr(frame_rgb, "shape", ())) < 2:
            raise RuntimeError("full-resolution renderer did not produce a valid frame")
        import_metrics = consume_last_fits_import_metrics()
        import_details = consume_last_fits_import_details()
        return renderer, import_metrics, import_details

    async def _refine_full_resolution(self) -> None:
        dataset_path = getattr(self.renderer, "dataset_path", None)
        if not dataset_path:
            return
        self.loading_state.update(
            {
                "refineScheduled": False,
                "refineRunning": True,
                "refineCompleted": False,
                "refineFailed": False,
                "fullRendererReadyForSwap": False,
                "lastRefineError": None,
                "previewPinnedUntilFullReady": True,
            }
        )
        self.set_loading_state(active=True, phase="refining-full", label="Refining full resolution")
        camera_state = None
        volume_params = dict(self.visualization.volume_params)
        with self._renderer_lock:
            try:
                camera_state = self._active_renderer_slot.renderer.get_camera_state()
            except Exception:
                camera_state = None
        try:
            replacement, import_metrics, import_details = await asyncio.to_thread(
                self._build_full_resolution_candidate,
                dataset_path,
                viewport=self.viewport,
                mode=self.mode,
                visualization_mode=self.visualization.mode,
                iso_value=self.visualization.iso_value,
                volume_params=volume_params,
                camera_state=camera_state,
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            self.loading_state.update(
                {
                    "refineRunning": False,
                    "refineFailed": True,
                    "lastRefineError": str(exc),
                    "fullRendererReadyForSwap": False,
                    "previewPinnedUntilFullReady": False,
                }
            )
            self.set_loading_state(active=False, phase="refining-full", label="Full-resolution refine failed")
            self.loading_state["refinePending"] = False
            raise
        self.loading_state["fullRendererReadyForSwap"] = True

        slots_to_close: list[_RendererSlot] = []
        with self._renderer_lock:
            if self._closed:
                replacement.close()
                return
            previous_slot = self._active_renderer_slot
            self._renderer_swap_in_progress = True
            self.renderer = replacement
            self._active_renderer_slot = _RendererSlot(renderer_id=self._next_renderer_id(), renderer=replacement)
            self._retire_renderer_slot_locked(previous_slot)
            self.import_metrics = import_metrics or self.import_metrics
            self.import_details = import_details or self.import_details
            self.visualization = VisualizationState(
                mode=self.renderer.get_visualization_mode(),
                iso_value=self.renderer.get_iso_value(),
                volume_params=self.renderer.get_volume_params(),
            )
            self.loading_state.update(
                {
                    "refineRunning": False,
                    "refineCompleted": True,
                    "refineFailed": False,
                    "refinePending": False,
                    "activeRepresentation": "full",
                    "previewPinnedUntilFullReady": False,
                    "lastRefineError": None,
                }
            )
            self.set_loading_state(active=False, phase="complete", label="Full resolution ready")
            self._renderer_swap_in_progress = False
            self._last_renderer_swap_error = None
            self._refresh_renderer_diagnostics_state()
            slots_to_close = self._collect_retired_renderer_slots_locked()
        self._close_retired_renderer_slots(slots_to_close)
        gc.collect()
        self.request_render()

    def effective_quality_profiles(self) -> dict[str, Any]:
        viewport_width = self.viewport.width
        viewport_height = self.viewport.height
        viewport_dpr = self.viewport.dpr

        def _profile_request(key: str) -> dict[str, Any]:
            value = self.requested_quality_profiles.get(key)
            return value if isinstance(value, dict) else {}

        interactive_req = _profile_request("interactive")
        hq_req = _profile_request("highQuality")
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                return {
                    "interactive": slot.renderer.describe_effective_quality_profile(
                        mode="interactive",
                        width=viewport_width,
                        height=viewport_height,
                        dpr=viewport_dpr,
                        requested_render_scale=interactive_req.get("renderScale"),
                        requested_sample_distance_scale=interactive_req.get("sampleDistanceScale"),
                        requested_image_sample_distance=interactive_req.get("imageSampleDistance"),
                        requested_bitrate_mbps=interactive_req.get("bitrateMbps"),
                    ),
                    "highQuality": slot.renderer.describe_effective_quality_profile(
                        mode="high-quality",
                        width=viewport_width,
                        height=viewport_height,
                        dpr=viewport_dpr,
                        requested_render_scale=hq_req.get("renderScale"),
                        requested_sample_distance_scale=hq_req.get("sampleDistanceScale"),
                        requested_image_sample_distance=hq_req.get("imageSampleDistance"),
                        requested_bitrate_mbps=hq_req.get("bitrateMbps"),
                    ),
                }
        finally:
            self._release_renderer_slot(slot)

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
        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                slot.renderer.prewarm_volume_renderer()
        finally:
            self._release_renderer_slot(slot)
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
        with self._renderer_lock:
            active_slot = self._active_renderer_slot
            target_update_interval = active_slot.renderer.target_update_interval
        now_ns = time.time_ns()
        if not force and self._last_render_finished_ns:
            elapsed_s = (now_ns - self._last_render_finished_ns) / 1e9
            if not self._dirty and elapsed_s < target_update_interval:
                return self._latest_frame

        slot = self._checkout_active_renderer_slot()
        try:
            with slot.render_lock:
                frame_rgb, started_ns, finished_ns, pipeline_metrics = slot.renderer.render_rgb_frame()
        except Exception as exc:
            if "eglMakeCurrent" in str(exc):
                with self._renderer_lock:
                    self._egl_context_error_detected = True
                    self._last_renderer_swap_error = str(exc)
                    self._refresh_renderer_diagnostics_state()
            raise
        finally:
            self._release_renderer_slot(slot)
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
        self._update_adaptive_runtime_controls(pipeline_metrics, finished_ns)
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

    def _update_adaptive_runtime_controls(self, pipeline_metrics: dict[str, Any], finished_ns: int) -> None:
        if self.loading_state.get("active"):
            return
        if self._dataset_load_mode() == "preview" and self.loading_state.get("refineRunning"):
            return
        if self.stats.delivered_frames < 1 and self._frame_serial < 3:
            return

        total_pipeline_ms = pipeline_metrics.get("totalFramePipelineTimeMs")
        if not isinstance(total_pipeline_ms, (int, float)) or not float(total_pipeline_ms) > 0.0:
            render_ms = float(pipeline_metrics.get("renderTimeMs", 0.0) or 0.0)
            capture_ms = float(pipeline_metrics.get("frameCaptureReadbackTimeMs", 0.0) or 0.0)
            encode_ms = float(pipeline_metrics.get("encodeTimeMs", 0.0) or 0.0)
            total_pipeline_ms = render_ms + capture_ms + encode_ms
        if not isinstance(total_pipeline_ms, (int, float)) or not float(total_pipeline_ms) > 0.0:
            return

        sample = float(total_pipeline_ms)
        alpha = 0.25
        if self.smoothed_pipeline_ms is None:
            self.smoothed_pipeline_ms = sample
        else:
            self.smoothed_pipeline_ms = (1.0 - alpha) * float(self.smoothed_pipeline_ms) + alpha * sample

        now_s = finished_ns / 1e9
        scale_changed = False

        if not self.adaptive_scaling_enabled:
            self.current_viewport_scale = 1.0
        elif self.mode == "interactive":
            if not self._adaptive_scale_started:
                self._adaptive_scale_started = True
                self.last_scale_update_ts = now_s
            elif now_s - self.last_scale_update_ts >= 1.0:
                next_scale = float(self.current_viewport_scale)
                if self.smoothed_pipeline_ms > 60.0:
                    next_scale *= 0.9
                elif self.smoothed_pipeline_ms < 30.0:
                    next_scale *= 1.05
                next_scale = min(max(next_scale, 0.5), 1.0)
                if abs(next_scale - self.current_viewport_scale) >= 0.03:
                    self.current_viewport_scale = next_scale
                    scale_changed = True
                self.last_scale_update_ts = now_s

        if self.adaptive_bitrate_enabled:
            if not self._adaptive_bitrate_started:
                self._adaptive_bitrate_started = True
                self.last_bitrate_update_ts = now_s
            elif now_s - self.last_bitrate_update_ts >= 1.5:
                next_bitrate = float(self.current_adaptive_bitrate_mbps)
                if self.smoothed_pipeline_ms > 60.0:
                    next_bitrate *= 0.9
                elif self.smoothed_pipeline_ms < 30.0:
                    next_bitrate *= 1.05
                next_bitrate = min(max(next_bitrate, self._adaptive_bitrate_min_mbps), self._adaptive_bitrate_max_mbps)
                if abs(next_bitrate - self.current_adaptive_bitrate_mbps) >= 0.5:
                    # aiortc in this environment does not expose a runtime sender.setParameters()
                    # path, so keep the adaptive bitrate target authoritative in session state for
                    # subsequent offers / renegotiation and production diagnostics.
                    self.current_adaptive_bitrate_mbps = next_bitrate
                    self.target_bitrate_mbps = next_bitrate
                self.last_bitrate_update_ts = now_s

        if scale_changed:
            slot = self._checkout_active_renderer_slot()
            try:
                with slot.render_lock:
                    self._apply_renderer_scale_locked(slot.renderer)
            finally:
                self._release_renderer_slot(slot)
            self.request_render()

    def _adapt_interactive_quality(self, render_ms: float) -> None:
        if self.mode != "interactive":
            slot = self._checkout_active_renderer_slot()
            try:
                with slot.render_lock:
                    if slot.renderer.interactive_boost != 1.0:
                        slot.renderer.set_interactive_boost(1.0)
            finally:
                self._release_renderer_slot(slot)
            return

        if render_ms > 60.0:
            slot = self._checkout_active_renderer_slot()
            try:
                with slot.render_lock:
                    slot.renderer.set_interactive_boost(slot.renderer.interactive_boost * 1.1)
            finally:
                self._release_renderer_slot(slot)
        elif render_ms < 28.0:
            slot = self._checkout_active_renderer_slot()
            try:
                with slot.render_lock:
                    slot.renderer.set_interactive_boost(slot.renderer.interactive_boost * 0.95)
            finally:
                self._release_renderer_slot(slot)

    def adaptive_scaling_state(self) -> dict[str, Any]:
        return {
            "adaptiveScalingEnabled": bool(self.adaptive_scaling_enabled),
            "adaptiveViewportActiveInInteractiveOnly": bool(self.adaptive_viewport_active_in_interactive_only),
            "currentViewportScale": float(self.current_viewport_scale),
            "smoothedPipelineMs": self.smoothed_pipeline_ms,
            "requestedRenderScale": float(self.requested_render_scale),
            "adaptiveBitrateEnabled": bool(self.adaptive_bitrate_enabled),
            "currentAdaptiveBitrateMbps": float(self.current_adaptive_bitrate_mbps),
            "requestedBitrateMbps": float(self.requested_bitrate_mbps),
        }


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

    async def count(self) -> int:
        async with self._lock:
            return len(self._sessions)

    async def summary(self) -> dict[str, int]:
        async with self._lock:
            return {
                "activeSessions": len(self._sessions),
                "maxSessions": self.max_sessions,
            }

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
