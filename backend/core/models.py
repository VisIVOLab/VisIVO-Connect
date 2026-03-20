from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class QualityProfile:
    name: str
    render_scale: float
    sample_distance_scale: float
    shade: bool
    update_rate_hz: float


@dataclass
class RenderStats:
    render_time_ms: list[float] = field(default_factory=list)
    frame_capture_time_ms: list[float] = field(default_factory=list)
    frame_conversion_time_ms: list[float] = field(default_factory=list)
    encode_time_ms: list[float] = field(default_factory=list)
    rtp_pacing_time_ms: list[float] = field(default_factory=list)
    total_frame_pipeline_time_ms: list[float] = field(default_factory=list)
    frame_delivery_latency_ms: list[float] = field(default_factory=list)
    input_to_visible_latency_ms: list[float] = field(default_factory=list)
    network_latency_ms: list[float] = field(default_factory=list)
    dropped_frames: int = 0
    delivered_frames: int = 0

    def add_sample(self, target: list[float], value: float, max_len: int = 512) -> None:
        target.append(value)
        if len(target) > max_len:
            del target[: len(target) - max_len]


@dataclass
class FramePacket:
    serial: int
    frame_rgb: Any
    render_started_ns: int
    render_finished_ns: int
    mode: str
    pipeline_metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class VisualizationState:
    mode: str = "volume"
    iso_value: float | None = None
    volume_params: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "visualizationMode": self.mode,
            "isoValue": self.iso_value,
            "volume": dict(self.volume_params),
        }


INTERACTIVE_PROFILE = QualityProfile(
    name="interactive",
    render_scale=0.6,
    sample_distance_scale=2.8,
    shade=False,
    update_rate_hz=30.0,
)

HIGH_QUALITY_PROFILE = QualityProfile(
    name="high-quality",
    render_scale=1.0,
    sample_distance_scale=1.0,
    shade=True,
    update_rate_hz=12.0,
)
