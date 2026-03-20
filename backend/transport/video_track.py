from __future__ import annotations

import asyncio
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

import av
from aiortc import VideoStreamTrack
import numpy as np

from backend.core.session import RemoteRenderSession


class LatestFrameVideoTrack(VideoStreamTrack):
    """WebRTC track that always emits the latest available rendered frame."""

    def __init__(self, session: RemoteRenderSession) -> None:
        super().__init__()
        self.session = session
        self._last_serial = -1
        self._last_bgr_frame: np.ndarray | None = None
        self._last_emit_ns = 0
        self._log = logging.getLogger(__name__)
        # Some backends (notably EGL and Cocoa) are sensitive to thread affinity.
        # Keep explicit env override, otherwise auto-select a safe default.
        main_thread_override = os.getenv("VISIVO_VTK_MAIN_THREAD")
        if main_thread_override is not None:
            self._render_on_main_thread = main_thread_override.strip().lower() in {"1", "true", "yes", "on"}
        else:
            renderer_backend = str(getattr(session.renderer, "_render_window_backend", "")).strip().lower()
            renderer_request = str(getattr(session.renderer, "_render_window_request", "")).strip().lower()
            backend_requires_main_thread = (
                sys.platform == "darwin"
                or "egl" in renderer_backend
                or renderer_request in {"egl", "vtkeglrenderwindow"}
            )
            self._render_on_main_thread = backend_requires_main_thread
        self._log.warning(
            "VideoTrack render threading session=%s main_thread=%s backend=%s request=%s",
            self.session.session_id,
            self._render_on_main_thread,
            getattr(session.renderer, "_render_window_backend", "unknown"),
            getattr(session.renderer, "_render_window_request", "unknown"),
        )
        self._render_executor: ThreadPoolExecutor | None = None
        if not self._render_on_main_thread:
            # Keep VTK/EGL calls on a stable worker thread to avoid context issues.
            self._render_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="visivo-render")
        self._first_frame_logged = False
        self._empty_cycles = 0

    async def recv(self) -> av.VideoFrame:
        target_fps = min(max(self.session.target_stream_fps, 5.0), 60.0)
        min_interval_ns = int(1_000_000_000 / target_fps)
        recv_started_ns = time.time_ns()
        pacing_wait_ns = 0
        if self._last_emit_ns:
            remaining_ns = min_interval_ns - (time.time_ns() - self._last_emit_ns)
            if remaining_ns > 0:
                pacing_wait_ns = remaining_ns
                await asyncio.sleep(remaining_ns / 1_000_000_000)

        pts, time_base = await self.next_timestamp()

        frame_packet = None
        try:
            if self._render_on_main_thread:
                frame_packet = self.session.render_if_needed()
                if frame_packet is None:
                    await asyncio.sleep(0.01)
                    frame_packet = self.session.render_if_needed(force=True)
            else:
                # Keep RTC timers responsive even if VTK render is expensive.
                loop = asyncio.get_running_loop()
                frame_packet = await loop.run_in_executor(self._render_executor, self.session.render_if_needed)
                if frame_packet is None:
                    await asyncio.sleep(0.01)
                    frame_packet = await loop.run_in_executor(self._render_executor, self.session.render_if_needed, True)
        except Exception:
            self._log.exception("render_if_needed failed; keeping stream alive with fallback frame")

        if frame_packet is not None and frame_packet.serial != self._last_serial:
            encode_started_ns = time.time_ns()
            try:
                video_frame = av.VideoFrame.from_ndarray(frame_packet.frame_bgr, format="bgr24")
            except Exception:
                self._log.exception("frame conversion failed; fallback to cached frame")
                if self._last_bgr_frame is not None:
                    repeat = av.VideoFrame.from_ndarray(self._last_bgr_frame, format="bgr24")
                    repeat.pts = pts
                    repeat.time_base = time_base
                    self._last_emit_ns = time.time_ns()
                    return repeat
                blank = av.VideoFrame(width=640, height=360, format="yuv420p")
                blank.pts = pts
                blank.time_base = time_base
                self._last_emit_ns = time.time_ns()
                return blank
            video_frame.pts = pts
            video_frame.time_base = time_base
            # Keep a raw ndarray copy; avoid reusing/reformatting AVFrame across calls.
            self._last_bgr_frame = frame_packet.frame_bgr
            self._last_serial = frame_packet.serial

            encode_ms = (time.time_ns() - encode_started_ns) / 1e6
            self.session.stats.add_sample(self.session.stats.encode_time_ms, encode_ms)
            self.session.stats.add_sample(self.session.stats.rtp_pacing_time_ms, pacing_wait_ns / 1e6)
            total_pipeline_ms = (time.time_ns() - frame_packet.render_started_ns) / 1e6
            self.session.stats.add_sample(self.session.stats.total_frame_pipeline_time_ms, total_pipeline_ms)
            pipeline_metrics = dict(frame_packet.pipeline_metrics)
            pipeline_metrics.update(
                {
                    "encodeTimeMs": encode_ms,
                    "rtpPacingTimeMs": pacing_wait_ns / 1e6,
                    "totalFramePipelineTimeMs": total_pipeline_ms,
                }
            )
            self.session.latest_pipeline_metrics = pipeline_metrics

            delivery_ms = (time.time_ns() - frame_packet.render_finished_ns) / 1e6
            self.session.stats.add_sample(self.session.stats.frame_delivery_latency_ms, delivery_ms)
            self.session.stats.delivered_frames += 1
            if not self._first_frame_logged:
                self._first_frame_logged = True
                self._log.warning(
                    "First video frame delivered session=%s serial=%s size=%sx%s mode=%s mapper=%s requested=%s smartRequested=%s smartUsed=%s render=%.2fms readback=%.2fms convert=%.2fms encode=%.2fms total=%.2fms",
                    self.session.session_id,
                    frame_packet.serial,
                    frame_packet.frame_bgr.shape[1],
                    frame_packet.frame_bgr.shape[0],
                    frame_packet.mode,
                    pipeline_metrics.get("activeMapperClass") or "unknown",
                    pipeline_metrics.get("requestedMapperClass") or "unknown",
                    pipeline_metrics.get("smartMapperRequestedMode") or "-",
                    pipeline_metrics.get("smartMapperLastUsedMode") or "-",
                    float(pipeline_metrics.get("renderTimeMs", 0.0)),
                    float(pipeline_metrics.get("frameCaptureReadbackTimeMs", 0.0)),
                    float(pipeline_metrics.get("frameConversionTimeMs", 0.0)),
                    float(pipeline_metrics.get("encodeTimeMs", 0.0)),
                    float(pipeline_metrics.get("totalFramePipelineTimeMs", 0.0)),
                )
            self._last_emit_ns = time.time_ns()
            return video_frame

        if self._last_bgr_frame is not None:
            # Rebuild from ndarray instead of AVFrame.reformat() to avoid libswscale crash path.
            repeat = av.VideoFrame.from_ndarray(self._last_bgr_frame, format="bgr24")
            repeat.pts = pts
            repeat.time_base = time_base
            self._last_emit_ns = time.time_ns()
            return repeat

        self._empty_cycles += 1
        if self._empty_cycles in {30, 120, 300}:
            self._log.warning("No frame available yet session=%s cycles=%s", self.session.session_id, self._empty_cycles)

        blank = av.VideoFrame(width=640, height=360, format="yuv420p")
        blank.pts = pts
        blank.time_base = time_base
        self._last_emit_ns = time.time_ns()
        return blank

    def stop(self) -> None:
        super().stop()
        if self._render_executor is not None:
            self._render_executor.shutdown(wait=False, cancel_futures=True)
            self._render_executor = None
