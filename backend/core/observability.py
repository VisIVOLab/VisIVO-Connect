from __future__ import annotations

from collections import deque
from contextvars import ContextVar
from dataclasses import dataclass, field
import sys

try:
    import resource
except ImportError:  # pragma: no cover - non-Unix fallback
    resource = None  # type: ignore[assignment]


@dataclass(frozen=True)
class FitsImportMetrics:
    fits_open_ms: float
    hdu_select_ms: float
    sanitize_convert_ms: float
    vtk_build_ms: float
    fits_total_ms: float


@dataclass
class SessionRuntimeMetrics:
    first_frame_latency_ms: float | None = None
    high_quality_render_time_ms: float = 0.0
    interactive_fps: float | None = None
    memory_rss_mb: float | None = None
    _interactive_finish_ns: deque[int] = field(default_factory=lambda: deque(maxlen=30), repr=False, compare=False)

    def refresh_memory_rss(self) -> None:
        self.memory_rss_mb = current_memory_rss_mb()

    def record_render(self, *, mode: str, render_ms: float, finished_ns: int, session_started_ns: int) -> None:
        if self.first_frame_latency_ms is None:
            self.first_frame_latency_ms = max(0.0, (finished_ns - session_started_ns) / 1e6)

        if mode == "high-quality":
            self.high_quality_render_time_ms += render_ms
            self._interactive_finish_ns.clear()
        else:
            self._interactive_finish_ns.append(finished_ns)
            if len(self._interactive_finish_ns) >= 2:
                elapsed_ns = self._interactive_finish_ns[-1] - self._interactive_finish_ns[0]
                if elapsed_ns > 0:
                    self.interactive_fps = (len(self._interactive_finish_ns) - 1) * 1_000_000_000.0 / elapsed_ns

        self.refresh_memory_rss()


_last_fits_import_metrics: ContextVar[FitsImportMetrics | None] = ContextVar(
    "last_fits_import_metrics",
    default=None,
)


def clear_last_fits_import_metrics() -> None:
    _last_fits_import_metrics.set(None)


def record_last_fits_import_metrics(metrics: FitsImportMetrics) -> None:
    _last_fits_import_metrics.set(metrics)


def consume_last_fits_import_metrics() -> FitsImportMetrics | None:
    metrics = _last_fits_import_metrics.get()
    _last_fits_import_metrics.set(None)
    return metrics


def current_memory_rss_mb() -> float | None:
    if resource is None:
        return None

    try:
        usage = resource.getrusage(resource.RUSAGE_SELF)
    except Exception:
        return None

    rss = float(usage.ru_maxrss)
    if sys.platform == "darwin":
        rss /= 1024.0 * 1024.0
    else:
        rss /= 1024.0
    return rss
