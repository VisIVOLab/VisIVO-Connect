from __future__ import annotations

import asyncio

import pytest

from backend.core.session import RemoteRenderSession, SessionManager
from backend.tests.fake_renderers import install_fake_renderer


def _create_session_manager() -> SessionManager:
    return SessionManager(max_sessions=1, idle_timeout_s=60, session_factory=RemoteRenderSession)


def test_visualization_mode_switch_volume_to_iso_surface(monkeypatch: pytest.MonkeyPatch) -> None:
    install_fake_renderer(monkeypatch)

    async def run() -> None:
        manager = _create_session_manager()
        session = await manager.create(dataset_path="/tmp/sample.fits", session_id="render-protocol")

        assert session.visualization.mode == "volume"
        assert session.renderer.volume.visible == 1

        session.set_visualization_mode("iso-surface")
        assert session.visualization.mode == "isosurface"
        assert session.renderer.volume.visible == 0
        assert session.renderer.visualization_mode == "isosurface"

        session.set_visualization_mode("volume")
        assert session.visualization.mode == "volume"
        assert session.renderer.volume.visible == 1
        assert session.renderer.visualization_mode == "volume"

        await manager.close_all()

    asyncio.run(run())


def test_iso_value_update_path_updates_iso_contour(monkeypatch: pytest.MonkeyPatch) -> None:
    install_fake_renderer(monkeypatch)

    async def run() -> None:
        manager = _create_session_manager()
        session = await manager.create(dataset_path="/tmp/sample.fits", session_id="iso-value")

        session.set_visualization_mode("iso-surface")
        session.set_visualization_params({"params": {"isoValue": 0.42}})

        assert session.visualization.mode == "isosurface"
        assert session.visualization.iso_value == pytest.approx(0.42)
        assert session.renderer.volume.visible == 0
        assert session.renderer.get_iso_value() == pytest.approx(0.42)

        session.set_visualization_params({"params": {"isoValue": 0.55, "volume": {"sampleDistanceScale": 2.0}}})
        assert session.visualization.iso_value == pytest.approx(0.55)
        assert session.visualization.volume_params["sampleDistanceScale"] == pytest.approx(2.0)
        assert session.renderer.get_iso_value() == pytest.approx(0.55)
        assert session.renderer.volume_mapper.sample_distance == pytest.approx(2.0)

        await manager.close_all()

    asyncio.run(run())


def test_interactive_to_hq_transition_preserved(monkeypatch: pytest.MonkeyPatch) -> None:
    install_fake_renderer(monkeypatch)

    async def run() -> None:
        manager = _create_session_manager()
        session = await manager.create(dataset_path="/tmp/sample.fits", session_id="transition")
        session.renderer._render_latency_s = 0.0

        session.begin_interaction()
        first = session.render_if_needed(force=True)
        assert first is not None
        assert first.mode == "interactive"

        session.end_interaction()
        second = session.render_if_needed(force=True)
        assert second is not None
        assert second.mode == "high-quality"
        assert session.mode == "high-quality"

        await manager.close_all()

    asyncio.run(run())
