from __future__ import annotations

import sys
import time
from dataclasses import dataclass
from types import ModuleType
from typing import Any

import numpy as np
import vtk


@dataclass
class _FakeProfile:
    name: str
    update_rate_hz: float


class _FakeVolumeMapper:
    def __init__(self) -> None:
        source = vtk.vtkRTAnalyticSource()
        source.SetWholeExtent(0, 1, 0, 1, 0, 1)
        source.Update()
        self._input = source.GetOutput()
        self.sample_distance = 1.0
        self.blend_mode = "composite"

    def GetInput(self) -> vtk.vtkImageData:
        return self._input

    def SetBlendModeToComposite(self) -> None:
        self.blend_mode = "composite"

    def SetBlendModeToMaximumIntensity(self) -> None:
        self.blend_mode = "mip"

    def SetBlendModeToMinimumIntensity(self) -> None:
        self.blend_mode = "minip"

    def SetSampleDistance(self, value: float) -> None:
        self.sample_distance = float(value)


class _FakeVolumeProperty:
    def __init__(self) -> None:
        self.shade = 0

    def SetShade(self, value: int) -> None:
        self.shade = int(value)


class _FakeVolume:
    def __init__(self) -> None:
        self.visible = 1

    def SetVisibility(self, value: int) -> None:
        self.visible = int(value)


class SessionFakeRenderer:
    """Lightweight renderer stub that matches the session layer API."""

    def __init__(self, dataset_path: str | None = None) -> None:
        self.dataset_path = dataset_path
        self.window_width = 1280
        self.window_height = 720
        self.stability_mode = False
        self.volume_mapper = _FakeVolumeMapper()
        self.volume_property = _FakeVolumeProperty()
        self.volume = _FakeVolume()
        self.current_profile = _FakeProfile(name="interactive", update_rate_hz=30.0)
        self.interactive_boost = 1.0
        self.user_render_scale = 1.0
        self.current_mode = "interactive"
        self.visualization_mode = "volume"
        self.iso_value = 0.5
        self.volume_params: dict[str, Any] = {}
        self.render_count = 0
        self.added_actors: list[Any] = []
        self._render_latency_s = 0.0

    def AddActor(self, actor: Any) -> None:
        self.added_actors.append(actor)

    def set_mode(self, mode: str) -> None:
        self.current_mode = "interactive" if mode == "interactive" else "high-quality"
        if self.current_mode == "interactive":
            self.current_profile = _FakeProfile(name="interactive", update_rate_hz=30.0)
        else:
            self.current_profile = _FakeProfile(name="high-quality", update_rate_hz=12.0)

    def set_visualization_mode(self, mode: str) -> None:
        normalized = str(mode).strip().lower().replace("_", "-")
        if normalized in {"isosurface", "iso-surface", "iso", "surface"}:
            self.visualization_mode = "isosurface"
            self.volume.SetVisibility(0)
        else:
            self.visualization_mode = "volume"
            self.volume.SetVisibility(1)

    def get_visualization_mode(self) -> str:
        return self.visualization_mode

    def set_iso_value(self, value: float | None) -> None:
        if value is not None:
            self.iso_value = float(value)

    def get_iso_value(self) -> float:
        return self.iso_value

    def get_scalar_range(self) -> tuple[float, float]:
        return (0.0, 1.0)

    def get_volume_params(self) -> dict[str, Any]:
        return {
            "activeMapper": "smart",
            "selectedRenderPath": "cpu",
            "capabilityProfile": "cpu-safe",
            "renderMode": "composite",
            "opacityScale": 1.0,
            "sampleDistanceScale": self.volume_mapper.sample_distance,
            "imageSampleDistance": None,
            "shade": bool(self.volume_property.shade),
            "sliceAxis": "z",
            "sliceIndex": 0,
            "sliceMaxIndex": 1,
            "slicePosition": 0.5,
            "cropping": {"enabled": False, "bounds": [0, 1, 0, 1, 0, 1]},
        }

    def get_runtime_capabilities(self) -> dict[str, Any]:
        return {
            "renderWindowBackend": "fake",
            "renderWindowRequest": "fake",
            "offscreenEnabled": True,
            "useOffscreenBuffers": True,
            "openGLVendor": "fake",
            "openGLRenderer": "fake",
            "openGLVersion": "fake",
            "openglAvailable": True,
            "volumeMapperClass": "FakeVolumeMapper",
            "gpuMapperClass": None,
            "cpuMapperClass": "FakeVolumeMapper",
            "gpuMapperAvailable": False,
            "cpuFallbackAvailable": True,
            "gpuOffscreenAvailable": False,
            "selectedRenderPath": "cpu",
            "capabilityProfile": "cpu-safe",
            "fallbackReason": "fake-renderer",
        }

    def get_renderer_diagnostics(self) -> dict[str, Any]:
        diagnostics = self.get_runtime_capabilities()
        diagnostics.update(
            {
                "activeMapper": "smart",
                "selectedRenderPath": "cpu",
                "capabilityProfile": "cpu-safe",
                "visualizationMode": self.visualization_mode,
                "volumeRenderMode": "composite",
                "stabilityMode": self.stability_mode,
            }
        )
        return diagnostics

    def set_volume_params(self, params: dict[str, Any]) -> None:
        self.volume_params = dict(params)
        sample = self.volume_params.get("sampleDistanceScale")
        if isinstance(sample, (int, float)):
            self.volume_mapper.SetSampleDistance(float(sample))

    def resize(self, width: int, height: int, dpr: float = 1.0) -> None:
        self.window_width = max(64, int(width))
        self.window_height = max(64, int(height))

    def set_user_render_scale(self, render_scale: float) -> None:
        self.user_render_scale = float(render_scale)

    def set_interactive_boost(self, boost: float) -> None:
        self.interactive_boost = float(boost)

    def apply_pointer_delta(self, dx_norm: float, dy_norm: float, mode: str = "rotate") -> None:
        return

    def apply_zoom(self, zoom_factor: float) -> None:
        return

    def render_bgr_frame(self) -> tuple[np.ndarray, int, int]:
        started_ns = time.time_ns()
        if self._render_latency_s > 0.0:
            time.sleep(self._render_latency_s)
        self.render_count += 1
        finished_ns = time.time_ns()

        frame = np.zeros((2, 2, 3), dtype=np.uint8)
        frame[0, 0, 0] = self.render_count % 255
        frame[0, 0, 1] = 1 if self.current_mode == "interactive" else 2
        frame[0, 0, 2] = self.volume.visible
        frame[1, 1, 0] = int(self.volume_mapper.sample_distance * 10.0) % 255
        return frame, started_ns, finished_ns

    @property
    def target_update_interval(self) -> float:
        return 1.0 / self.current_profile.update_rate_hz


def install_fake_renderer(monkeypatch: Any) -> None:
    module = ModuleType("backend.rendering.vtk_datacube_renderer")
    module.VTKDatacubeRenderer = SessionFakeRenderer
    monkeypatch.setitem(sys.modules, module.__name__, module)
