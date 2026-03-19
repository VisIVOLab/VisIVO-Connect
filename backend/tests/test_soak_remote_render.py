from __future__ import annotations

import asyncio

import pytest

from backend.core.models import RenderStats
from backend.core.session import SessionManager
from backend.tests.fake_renderers import install_fake_renderer
from tools.soak_remote_render import RenderSample, summarize_soak


def test_summarize_soak_detects_monotonic_serials_and_hq_transition() -> None:
    stats = RenderStats(
        render_time_ms=[12.0, 11.0, 22.0],
        input_to_visible_latency_ms=[14.0, 13.0, 18.0],
        frame_delivery_latency_ms=[1.5, 1.3, 1.8],
        dropped_frames=2,
        delivered_frames=3,
    )
    samples = [
        RenderSample(serial=1, input_seq=4, mode="interactive", render_ms=12.0, delivery_ms=1.5, timestamp_ns=1_000),
        RenderSample(serial=2, input_seq=7, mode="interactive", render_ms=11.0, delivery_ms=1.3, timestamp_ns=2_000),
        RenderSample(serial=3, input_seq=9, mode="high-quality", render_ms=22.0, delivery_ms=1.8, timestamp_ns=3_000),
    ]

    summary = summarize_soak(
        samples=samples,
        stats=stats,
        input_events=9,
        duration_s=1.0,
        dataset_path="/tmp/sample.fits",
        hq_started_ns=2_500,
    )

    assert summary.ok is True
    assert summary.latest_frame_wins is True
    assert summary.transition_ok is True
    assert summary.max_input_gap == 3
    assert summary.backlog_growth <= 0
    assert summary.delivered_frames == 3
    assert summary.dropped_frames == 2
    assert summary.fps_estimate == pytest.approx(3.0)


def test_fake_renderer_session_path_overwrites_previous_frame_and_switches_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    install_fake_renderer(monkeypatch)

    async def run() -> None:
        manager = SessionManager(max_sessions=1, idle_timeout_s=60)
        session = await manager.create(dataset_path="/tmp/sample.fits", session_id="soak")
        session.renderer._render_latency_s = 0.0

        session.apply_pointer({"action": "move", "dx": 0.01, "dy": 0.02, "buttons": 1})
        first = session.render_if_needed()
        assert first is not None
        assert first.serial == 1
        assert first.mode == "interactive"

        session.apply_pointer({"action": "move", "dx": 0.03, "dy": -0.01, "buttons": 1})
        second = session.render_if_needed(force=True)
        assert second is not None
        assert second.serial == 2
        assert second.mode == "interactive"
        assert session.stats.dropped_frames == 1
        assert session.latest_frame() is second

        session.end_interaction()
        third = session.render_if_needed(force=True)
        assert third is not None
        assert third.serial == 3
        assert third.mode == "high-quality"
        assert session.mode == "high-quality"

        await manager.close_all()

    asyncio.run(run())
