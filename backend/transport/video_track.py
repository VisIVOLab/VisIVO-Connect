from __future__ import annotations

import asyncio
import logging
import os
import sys
import time

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
        # vtkCocoaRenderWindow on macOS must render on main thread.
        force_main_thread = os.getenv("VISIVO_VTK_MAIN_THREAD", "1" if sys.platform == "darwin" else "0") == "1"
        self._render_on_main_thread = force_main_thread

    async def recv(self) -> av.VideoFrame:
        target_fps = min(max(self.session.target_stream_fps, 5.0), 60.0)
        min_interval_ns = int(1_000_000_000 / target_fps)
        if self._last_emit_ns:
            remaining_ns = min_interval_ns - (time.time_ns() - self._last_emit_ns)
            if remaining_ns > 0:
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
                frame_packet = await asyncio.to_thread(self.session.render_if_needed)
                if frame_packet is None:
                    await asyncio.sleep(0.01)
                    frame_packet = await asyncio.to_thread(self.session.render_if_needed, True)
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

            delivery_ms = (time.time_ns() - frame_packet.render_finished_ns) / 1e6
            self.session.stats.add_sample(self.session.stats.frame_delivery_latency_ms, delivery_ms)
            self.session.stats.delivered_frames += 1
            self._last_emit_ns = time.time_ns()
            return video_frame

        if self._last_bgr_frame is not None:
            # Rebuild from ndarray instead of AVFrame.reformat() to avoid libswscale crash path.
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
