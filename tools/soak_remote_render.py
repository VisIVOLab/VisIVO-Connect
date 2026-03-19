#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import sys
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType, SimpleNamespace
from typing import Any

# Keep the script runnable from the repo root without installing the package.
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.core.models import RenderStats  # noqa: E402
from backend.core.session import RemoteRenderSession, SessionManager  # noqa: E402
from backend.transport.video_track import LatestFrameVideoTrack  # noqa: E402
from tools.validate_fits_datacube import create_synthetic_fits_cube  # noqa: E402


@dataclass
class RenderSample:
    serial: int
    input_seq: int
    mode: str
    render_ms: float
    delivery_ms: float | None
    timestamp_ns: int


@dataclass
class SoakSummary:
    ok: bool
    dataset_path: str
    duration_s: float
    input_events: int
    delivered_frames: int
    dropped_frames: int
    fps_estimate: float
    max_input_gap: int
    backlog_growth: int
    backlog_stable: bool
    latest_frame_wins: bool
    transition_ok: bool
    render_latency_ms_avg: float | None
    input_to_visible_latency_ms_avg: float | None
    frame_delivery_latency_ms_avg: float | None
    render_latency_ms_p95: float | None
    input_to_visible_latency_ms_p95: float | None
    frame_delivery_latency_ms_p95: float | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "datasetPath": self.dataset_path,
            "durationSeconds": round(self.duration_s, 3),
            "counts": {
                "inputEvents": self.input_events,
                "deliveredFrames": self.delivered_frames,
                "droppedFrames": self.dropped_frames,
            },
            "fpsEstimate": round(self.fps_estimate, 2),
            "backlog": {
                "maxInputGap": self.max_input_gap,
                "growth": self.backlog_growth,
            },
            "checks": {
                "backlogStable": self.backlog_stable,
                "latestFrameWins": self.latest_frame_wins,
                "interactiveToHqTransition": self.transition_ok,
            },
            "latenciesMs": {
                "renderAvg": _round_or_none(self.render_latency_ms_avg),
                "renderP95": _round_or_none(self.render_latency_ms_p95),
                "inputToVisibleAvg": _round_or_none(self.input_to_visible_latency_ms_avg),
                "inputToVisibleP95": _round_or_none(self.input_to_visible_latency_ms_p95),
                "frameDeliveryAvg": _round_or_none(self.frame_delivery_latency_ms_avg),
                "frameDeliveryP95": _round_or_none(self.frame_delivery_latency_ms_p95),
            },
        }


class FakeRenderer:
    """Deterministic renderer stub for soak validation.

    The session layer is what we are validating here, not VTK itself. The fake
    renderer preserves the same public surface used by RemoteRenderSession.
    """

    def __init__(self, dataset_path: str | None = None) -> None:
        self.dataset_path = dataset_path
        self.window_width = 1280
        self.window_height = 720
        self.current_mode = "interactive"
        self.visualization_mode = "volume"
        self.iso_value = 0.5
        self.volume_params: dict[str, Any] = {}
        self.user_render_scale = 1.0
        self.interactive_boost = 1.0
        self.pointer_x = 0.0
        self.pointer_y = 0.0
        self.zoom = 1.0
        self.render_count = 0
        self.current_profile = SimpleNamespace(name="interactive", update_rate_hz=30.0)
        self.before_render_hook: Any | None = None
        self.last_render_input_seq = 0
        self.last_render_mode = "interactive"
        self.last_render_started_ns = 0
        self.last_render_finished_ns = 0
        self._render_latency_s = 0.012

    def set_mode(self, mode: str) -> None:
        self.current_mode = "interactive" if mode == "interactive" else "high-quality"
        if self.current_mode == "interactive":
            self.current_profile = SimpleNamespace(name="interactive", update_rate_hz=30.0)
            self._render_latency_s = 0.012
        else:
            self.current_profile = SimpleNamespace(name="high-quality", update_rate_hz=12.0)
            self._render_latency_s = 0.022

    def set_visualization_mode(self, mode: str) -> None:
        normalized = str(mode).strip().lower().replace("_", "-")
        self.visualization_mode = "isosurface" if normalized in {"iso", "isosurface", "iso-surface", "surface"} else "volume"

    def get_visualization_mode(self) -> str:
        return self.visualization_mode

    def set_iso_value(self, iso_value: float | None) -> None:
        if iso_value is not None:
            self.iso_value = float(iso_value)

    def get_iso_value(self) -> float:
        return self.iso_value

    def set_volume_params(self, params: dict[str, Any]) -> None:
        self.volume_params = dict(params)

    def resize(self, width: int, height: int, dpr: float = 1.0) -> None:
        self.window_width = max(64, int(width))
        self.window_height = max(64, int(height))

    def set_user_render_scale(self, render_scale: float) -> None:
        self.user_render_scale = float(render_scale)

    def set_interactive_boost(self, boost: float) -> None:
        self.interactive_boost = float(boost)

    def apply_pointer_delta(self, dx_norm: float, dy_norm: float, mode: str = "rotate") -> None:
        if mode == "pan":
            self.pointer_x += dx_norm * 0.65
            self.pointer_y += dy_norm * 0.65
        else:
            self.pointer_x += dx_norm * 0.9
            self.pointer_y += dy_norm * 0.9

    def apply_zoom(self, zoom_factor: float) -> None:
        self.zoom = max(0.25, min(self.zoom * float(zoom_factor), 4.0))

    def render_bgr_frame(self) -> tuple[Any, int, int]:
        if self.before_render_hook is not None:
            self.before_render_hook()

        started_ns = time.time_ns()
        self.last_render_started_ns = started_ns
        time.sleep(self._render_latency_s)
        self.render_count += 1
        self.last_render_finished_ns = time.time_ns()
        self.last_render_mode = self.current_mode

        # Keep the array tiny; the harness cares about sequencing, not pixels.
        import numpy as np

        frame = np.zeros((2, 2, 3), dtype=np.uint8)
        frame[0, 0, 0] = self.render_count % 255
        frame[0, 0, 1] = 1 if self.current_mode == "interactive" else 2
        frame[0, 0, 2] = int(abs(self.pointer_x + self.pointer_y) * 100.0) % 255
        frame[1, 1, 0] = int(self.zoom * 32.0) % 255
        return frame, started_ns, self.last_render_finished_ns

    @property
    def target_update_interval(self) -> float:
        return 1.0 / self.current_profile.update_rate_hz


def _round_or_none(value: float | None) -> float | None:
    if value is None:
        return None
    return round(float(value), 2)


def install_fake_renderer() -> None:
    module = ModuleType("backend.rendering.vtk_datacube_renderer")
    module.VTKDatacubeRenderer = FakeRenderer
    sys.modules[module.__name__] = module


def _mean(values: list[float]) -> float | None:
    if not values:
        return None
    return sum(values) / len(values)


def _p95(values: list[float]) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, math.ceil(len(ordered) * 0.95) - 1))
    return ordered[index]


def summarize_soak(
    *,
    samples: list[RenderSample],
    stats: RenderStats,
    input_events: int,
    duration_s: float,
    dataset_path: str,
    hq_started_ns: int,
) -> SoakSummary:
    serials = [sample.serial for sample in samples]
    input_seq_gaps = [samples[i].input_seq - samples[i - 1].input_seq for i in range(1, len(samples))]

    midpoint_ns = samples[0].timestamp_ns + int((samples[-1].timestamp_ns - samples[0].timestamp_ns) / 2) if samples else 0
    first_half_gaps = []
    second_half_gaps = []
    for index, gap in enumerate(input_seq_gaps, start=1):
        bucket = first_half_gaps if samples[index].timestamp_ns <= midpoint_ns else second_half_gaps
        bucket.append(gap)
    first_half_max = max(first_half_gaps) if first_half_gaps else 0
    second_half_max = max(second_half_gaps) if second_half_gaps else 0
    backlog_growth = second_half_max - first_half_max
    max_input_gap = max(input_seq_gaps) if input_seq_gaps else 0

    latest_frame_wins = all(
        samples[i].serial > samples[i - 1].serial and samples[i].input_seq >= samples[i - 1].input_seq
        for i in range(1, len(samples))
    )
    transition_ok = False
    seen_hq = False
    for sample in samples:
        if sample.timestamp_ns < hq_started_ns:
            continue
        seen_hq = True
        if sample.mode != "high-quality":
            transition_ok = False
            break
        transition_ok = True
    transition_ok = transition_ok and seen_hq

    render_avg = _mean(stats.render_time_ms)
    input_visible_avg = _mean(stats.input_to_visible_latency_ms)
    delivery_avg = _mean(stats.frame_delivery_latency_ms)
    fps_estimate = len(samples) / max(duration_s, 1e-6)

    ok = (
        bool(samples)
        and serials == sorted(serials)
        and all(sample.input_seq >= 0 for sample in samples)
        and latest_frame_wins
        and transition_ok
    )
    backlog_stable = backlog_growth <= max(4, max_input_gap // 2 + 1)
    ok = ok and backlog_stable

    return SoakSummary(
        ok=ok,
        dataset_path=dataset_path,
        duration_s=duration_s,
        input_events=input_events,
        delivered_frames=stats.delivered_frames,
        dropped_frames=stats.dropped_frames,
        fps_estimate=fps_estimate,
        max_input_gap=max_input_gap,
        backlog_growth=backlog_growth,
        backlog_stable=backlog_stable,
        latest_frame_wins=latest_frame_wins,
        transition_ok=transition_ok,
        render_latency_ms_avg=render_avg,
        input_to_visible_latency_ms_avg=input_visible_avg,
        frame_delivery_latency_ms_avg=delivery_avg,
        render_latency_ms_p95=_p95(stats.render_time_ms),
        input_to_visible_latency_ms_p95=_p95(stats.input_to_visible_latency_ms),
        frame_delivery_latency_ms_p95=_p95(stats.frame_delivery_latency_ms),
    )


@dataclass
class _InputState:
    lock: threading.Lock = field(default_factory=threading.Lock)
    input_seq: int = 0

    def increment(self) -> int:
        with self.lock:
            self.input_seq += 1
            return self.input_seq

    def snapshot(self) -> int:
        with self.lock:
            return self.input_seq


async def run_soak(
    *,
    dataset_path: str,
    duration_s: float,
    burst_size: int,
    input_hz: float,
    burst_every_ms: float,
    target_fps: float,
    hq_snapshots: int,
) -> SoakSummary:
    manager = SessionManager(max_sessions=1, idle_timeout_s=30)
    session = await manager.create(dataset_path=dataset_path, session_id="soak")
    session.target_stream_fps = float(target_fps)
    renderer = session.renderer

    state = _InputState()
    samples: list[RenderSample] = []
    stop_event = threading.Event()
    started_ns = time.time_ns()
    hq_started_ns = 0

    if isinstance(renderer, FakeRenderer):
        def on_before_render() -> None:
            renderer.last_render_input_seq = state.snapshot()
        renderer.before_render_hook = on_before_render

    def input_loop() -> None:
        step_interval_s = 1.0 / max(input_hz, 1.0)
        burst_interval_steps = max(1, int(round((burst_every_ms / 1000.0) / step_interval_s)))
        next_step_ns = time.perf_counter_ns()
        step = 0
        deadline_ns = next_step_ns + int(duration_s * 1_000_000_000)

        while time.perf_counter_ns() < deadline_ns and not stop_event.is_set():
            seq = state.increment()
            dx = 0.003 + (seq % 7) * 0.00015
            dy = 0.002 + (seq % 5) * 0.00011
            session.apply_pointer({"action": "move", "dx": dx, "dy": dy, "buttons": 1})

            step += 1
            if step % burst_interval_steps == 0:
                for burst_index in range(max(0, burst_size - 1)):
                    seq = state.increment()
                    dx = 0.005 + burst_index * 0.0001
                    dy = 0.004 + burst_index * 0.00008
                    session.apply_pointer({"action": "move", "dx": dx, "dy": dy, "buttons": 1})

            next_step_ns += int(step_interval_s * 1_000_000_000)
            sleep_ns = next_step_ns - time.perf_counter_ns()
            if sleep_ns > 0:
                time.sleep(sleep_ns / 1_000_000_000)

    session.begin_interaction()
    input_thread = threading.Thread(target=input_loop, name="soak-input", daemon=True)
    input_thread.start()

    track = LatestFrameVideoTrack(session)
    last_serial = 0
    end_of_drag_ns = started_ns + int(duration_s * 1_000_000_000)

    try:
        while time.time_ns() < end_of_drag_ns or input_thread.is_alive():
            await track.recv()
            packet = session.latest_frame()
            if packet is None or packet.serial == last_serial:
                continue

            last_serial = packet.serial
            samples.append(
                RenderSample(
                    serial=packet.serial,
                    input_seq=(renderer.last_render_input_seq if isinstance(renderer, FakeRenderer) else state.snapshot()),
                    mode=packet.mode,
                    render_ms=(packet.render_finished_ns - packet.render_started_ns) / 1e6,
                    delivery_ms=session.stats.frame_delivery_latency_ms[-1] if session.stats.frame_delivery_latency_ms else None,
                    timestamp_ns=packet.render_finished_ns,
                )
            )

        stop_event.set()
        input_thread.join(timeout=2.0)

        session.end_interaction()
        hq_started_ns = time.time_ns()
        for _ in range(max(1, hq_snapshots)):
            session.request_render()
            await track.recv()
            packet = session.latest_frame()
            if packet is None or packet.serial == last_serial:
                continue
            last_serial = packet.serial
            samples.append(
                RenderSample(
                    serial=packet.serial,
                    input_seq=(renderer.last_render_input_seq if isinstance(renderer, FakeRenderer) else state.snapshot()),
                    mode=packet.mode,
                    render_ms=(packet.render_finished_ns - packet.render_started_ns) / 1e6,
                    delivery_ms=session.stats.frame_delivery_latency_ms[-1] if session.stats.frame_delivery_latency_ms else None,
                    timestamp_ns=packet.render_finished_ns,
                )
            )
    finally:
        stop_event.set()
        input_thread.join(timeout=2.0)
        await manager.close_all()

    duration_measured_s = max((samples[-1].timestamp_ns - started_ns) / 1e9 if samples else duration_s, duration_s)
    summary = summarize_soak(
        samples=samples,
        stats=session.stats,
        input_events=state.snapshot(),
        duration_s=duration_measured_s,
        dataset_path=dataset_path,
        hq_started_ns=hq_started_ns,
    )
    return summary


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Soak-test remote rendering session behavior with burst drag input and HQ transition",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--dataset-path", type=Path, help="path to a FITS datacube used for the session")
    parser.add_argument("--duration-s", type=float, default=3.0, help="duration of the drag phase")
    parser.add_argument("--burst-size", type=int, default=6, help="extra pointer events sent in each burst")
    parser.add_argument("--input-hz", type=float, default=90.0, help="continuous drag rate in events/second")
    parser.add_argument("--burst-every-ms", type=float, default=100.0, help="burst interval during the drag phase")
    parser.add_argument("--target-fps", type=float, default=30.0, help="stream target FPS for the track")
    parser.add_argument("--hq-snapshots", type=int, default=4, help="HQ frames captured after interaction.end")
    parser.add_argument("--real-renderer", action="store_true", help="use the actual VTK renderer instead of the fake one")
    parser.add_argument("--json", action="store_true", help="emit JSON only")
    return parser


def main() -> int:
    parser = _build_arg_parser()
    args = parser.parse_args()

    dataset_path = args.dataset_path
    temp_dataset: Path | None = None
    if dataset_path is None:
        temp_dataset = Path.cwd() / ".tmp-soak-cube.fits"
        create_synthetic_fits_cube(temp_dataset, size=32)
        dataset_path = temp_dataset

    if not args.real_renderer:
        install_fake_renderer()

    summary = asyncio_run(
        run_soak(
            dataset_path=str(dataset_path),
            duration_s=float(args.duration_s),
            burst_size=max(1, int(args.burst_size)),
            input_hz=max(1.0, float(args.input_hz)),
            burst_every_ms=max(10.0, float(args.burst_every_ms)),
            target_fps=max(5.0, float(args.target_fps)),
            hq_snapshots=max(1, int(args.hq_snapshots)),
        )
    )

    output = summary.as_dict()
    if args.json:
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(
            "soak "
            f"ok={output['ok']} "
            f"fps={output['fpsEstimate']} "
            f"render_avg_ms={output['latenciesMs']['renderAvg']} "
            f"input_visible_avg_ms={output['latenciesMs']['inputToVisibleAvg']} "
            f"delivered={output['counts']['deliveredFrames']} "
            f"dropped={output['counts']['droppedFrames']} "
            f"max_gap={output['backlog']['maxInputGap']} "
            f"growth={output['backlog']['growth']}"
        )
        print(json.dumps(output, indent=2, sort_keys=True))

    if temp_dataset is not None and temp_dataset.exists():
        temp_dataset.unlink(missing_ok=True)

    return 0 if summary.ok else 2


def asyncio_run(coro):
    import asyncio

    return asyncio.run(coro)


if __name__ == "__main__":
    raise SystemExit(main())
