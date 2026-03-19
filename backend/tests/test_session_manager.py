from __future__ import annotations

import asyncio
import time

from backend.core.session import SessionManager


class FakeSession:
    def __init__(self, dataset_path: str | None = None) -> None:
        self.dataset_path = dataset_path
        self.session_id = f"s-{time.time_ns()}"
        self.peer_connection = None
        self.last_activity_ns = time.time_ns()
        self.closed = False

    def close(self) -> None:
        self.closed = True


def test_session_manager_evicts_oldest_when_full() -> None:
    async def run() -> None:
        manager = SessionManager(max_sessions=1, idle_timeout_s=3600, session_factory=FakeSession)
        first = await manager.create(session_id="a")
        first.last_activity_ns = 1
        second = await manager.create(session_id="b")
        assert second.session_id == "b"
        assert await manager.get("a") is None
        assert await manager.get("b") is not None

    asyncio.run(run())


def test_session_manager_cleans_idle_sessions() -> None:
    async def run() -> None:
        manager = SessionManager(max_sessions=2, idle_timeout_s=1, session_factory=FakeSession)
        session = await manager.create(session_id="idle")
        session.last_activity_ns = 1
        cleaned = await manager.cleanup_idle()
        assert cleaned == 1
        assert await manager.get("idle") is None

    asyncio.run(run())
