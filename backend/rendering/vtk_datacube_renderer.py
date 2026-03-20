from __future__ import annotations

import os
import sys
import time
import logging
import re
from typing import Any

import numpy as np
import vtk
from vtk.util import numpy_support

from backend.core.models import HIGH_QUALITY_PROFILE, INTERACTIVE_PROFILE, QualityProfile
from backend.data import load_image_data
from backend.rendering.isosurface_pipeline import build_isosurface_pipeline


class VTKDatacubeRenderer:
    """Server-side VTK renderer for FITS-backed volumetric datasets.

    Supports two visualization modes:
    - `volume`: ray-casting/composite volume rendering
    - `isosurface`: contour surface rendering

    Quality mode remains orthogonal and is controlled by existing profiles:
    - `interactive`: fast preview while input is active
    - `high-quality`: refined rendering after input release
    """

    def __init__(self, dataset_path: str | None = None) -> None:
        self.dataset_path = dataset_path
        self.window_width = 1280
        self.window_height = 720
        self.stability_mode = os.getenv("VISIVO_STABILITY_MODE", "1" if sys.platform == "darwin" else "0") == "1"
        # Use uvicorn logger to ensure diagnostics are visible in server console.
        self._log = logging.getLogger("uvicorn.error")
        self._render_window_backend = "unknown"
        self._render_window_request = os.getenv("VISIVO_VTK_RENDER_WINDOW", "auto").strip().lower()
        self._closed = False
        self._capability_profile_name = "cpu-safe"
        self._selected_render_path = "cpu"
        self._fallback_reason: str | None = None
        self._runtime_capabilities: dict[str, Any] = {}

        self.renderer = vtk.vtkRenderer()
        self.render_window = self._create_render_window()
        self.render_window.SetOffScreenRendering(1)
        if hasattr(self.render_window, "SetUseOffScreenBuffers"):
            self.render_window.SetUseOffScreenBuffers(1)
        if hasattr(self.render_window, "SwapBuffersOff"):
            self.render_window.SwapBuffersOff()
        self.render_window.AddRenderer(self.renderer)
        self.render_window.SetSize(self.window_width, self.window_height)

        self.window_to_image = vtk.vtkWindowToImageFilter()
        self.window_to_image.SetInput(self.render_window)
        self.window_to_image.SetInputBufferTypeToRGB()
        self.window_to_image.ReadFrontBufferOff()

        mapper_cls = getattr(vtk, "vtkGPUVolumeRayCastMapper", None)
        self.gpu_volume_mapper = mapper_cls() if mapper_cls is not None else None
        self.cpu_fallback_mapper = vtk.vtkSmartVolumeMapper()
        self.volume_mapper = self.cpu_fallback_mapper
        self._active_mapper_name = "smart"
        self._black_frame_streak = 0
        self._black_frame_streak_fallback = 0
        self._dark_frame_streak_total = 0
        self.volume = vtk.vtkVolume()
        self.volume_property = vtk.vtkVolumeProperty()
        self.outline_actor = vtk.vtkActor()
        self.slice_mapper = vtk.vtkImageSliceMapper()
        self.slice_actor = vtk.vtkImageSlice()

        self.image_data: vtk.vtkImageData | None = None
        self.isosurface_pipeline = None
        self.visualization_mode = "volume"
        self.iso_value: float | None = None
        self.volume_opacity_scale = 1.0
        self.volume_sample_distance_scale_override: float | None = None
        self.volume_image_sample_distance_override: float | None = None
        self.volume_shade_override: bool | None = None
        self.volume_render_mode = "composite"
        self.slice_axis = "z"
        self.slice_index: int | None = None
        self.cropping_enabled = False
        self.cropping_bounds_norm = (0.0, 1.0, 0.0, 1.0, 0.0, 1.0)

        self._volume_scalar_range = (0.0, 1.0)
        self._volume_color_points = (
            (0.0, (0.01, 0.02, 0.05)),
            (0.20, (0.06, 0.15, 0.35)),
            (0.45, (0.25, 0.6, 0.9)),
            (0.70, (0.95, 0.75, 0.25)),
            (1.0, (1.0, 0.95, 0.95)),
        )
        self._volume_opacity_points = (
            (0.0, 0.0),
            (0.20, 0.0),
            (0.40, 0.06),
            (0.65, 0.22),
            (0.85, 0.55),
            (1.0, 0.90),
        )

        self._configure_scene()
        self._detect_runtime_capabilities()
        self.current_profile: QualityProfile = (
            HIGH_QUALITY_PROFILE if self._capability_profile_name == "gpu-high" else INTERACTIVE_PROFILE
        )
        self.user_render_scale = 1.0
        self.interactive_boost = 1.0
        self.set_profile(self.current_profile)
        self.set_visualization_mode("volume")
        self._log.warning(
            "Renderer initialized backend=%s request=%s path=%s profile=%s mapper=%s mode=%s",
            self._render_window_backend,
            self._render_window_request,
            self._selected_render_path,
            self._capability_profile_name,
            self._active_mapper_name,
            self.visualization_mode,
        )

    def _create_render_window(self) -> vtk.vtkRenderWindow:
        requested = self._render_window_request
        is_linux = sys.platform.startswith("linux")
        is_macos = sys.platform == "darwin"

        if requested in {"egl", "vtkeglrenderwindow"}:
            candidates = ["vtkEGLRenderWindow"]
        elif requested in {"osmesa", "vtkosopenglrenderwindow"}:
            # OSMesa backend is Linux-oriented in VTK; avoid known unsupported platforms.
            if not is_linux:
                raise RuntimeError("VISIVO_VTK_RENDER_WINDOW=osmesa is not supported on this operating system")
            candidates = ["vtkOSOpenGLRenderWindow"]
        elif requested in {"x", "x11", "vtkrenderwindow"}:
            candidates = ["vtkRenderWindow"]
        else:
            # Safe defaults:
            # - Linux headless: prefer EGL first, then native render window.
            # - macOS/others: use native render window (OffScreenRendering enabled above).
            if is_linux:
                candidates = ["vtkEGLRenderWindow", "vtkRenderWindow"]
            elif is_macos:
                candidates = ["vtkRenderWindow"]
            else:
                candidates = ["vtkRenderWindow"]

        last_error: Exception | None = None
        for class_name in candidates:
            cls = getattr(vtk, class_name, None)
            if cls is None:
                continue
            try:
                window = cls()
                self._render_window_backend = class_name
                self._log.warning("Using VTK render window backend: %s", class_name)
                return window
            except Exception as exc:  # pragma: no cover - backend-specific failure path
                last_error = exc
                self._log.warning("Failed to initialize VTK render window backend %s: %s", class_name, exc)

        if last_error is not None:
            raise RuntimeError("Could not initialize a VTK render window backend") from last_error
        raise RuntimeError(
            "No compatible VTK render window backend found. "
            "Try VISIVO_VTK_RENDER_WINDOW=egl/osmesa or run under Xvfb."
        )

    def _load_image_data(self) -> vtk.vtkImageData:
        return load_image_data(self.dataset_path)

    def _configure_scene(self) -> None:
        self.image_data = self._load_image_data()
        self._log_scalar_summary(self.image_data)
        self._configure_volume_pipeline(self.image_data)
        self._configure_outline(self.image_data)
        self._configure_slice_pipeline(self.image_data)
        self._configure_isosurface_pipeline(self.image_data)

        self.renderer.AddVolume(self.volume)
        self.renderer.AddActor(self.outline_actor)
        self.renderer.AddViewProp(self.slice_actor)
        if self.isosurface_pipeline is not None:
            self.renderer.AddActor(self.isosurface_pipeline.actor)
        self.renderer.SetBackground(0.03, 0.04, 0.06)
        self.renderer.ResetCamera()

    def _log_scalar_summary(self, image_data: vtk.vtkImageData) -> None:
        try:
            scalars = image_data.GetPointData().GetScalars()
            if scalars is None:
                self._log.warning("Loaded image data has no scalars")
                return
            values = numpy_support.vtk_to_numpy(scalars)
            if values.size == 0:
                self._log.warning("Loaded image data has empty scalar array")
                return
            finite = values[np.isfinite(values)]
            if finite.size == 0:
                self._log.warning("Loaded image data has no finite values")
                return
            p01, p50, p99 = np.percentile(finite, [1.0, 50.0, 99.0]).astype(float)
            non_zero_ratio = float(np.count_nonzero(np.abs(finite) > 0.0) / finite.size)
            dims = image_data.GetDimensions()
            self._log.info(
                "Dataset summary dims=%s finite=%d min=%.6g max=%.6g p01=%.6g p50=%.6g p99=%.6g nonZero=%.2f%%",
                dims,
                int(finite.size),
                float(finite.min()),
                float(finite.max()),
                p01,
                p50,
                p99,
                non_zero_ratio * 100.0,
            )
        except Exception:  # pragma: no cover - diagnostic only
            self._log.exception("Failed to compute dataset scalar summary")

    def _configure_volume_pipeline(self, image_data: vtk.vtkImageData) -> None:
        if self.gpu_volume_mapper is not None:
            self._configure_mapper(self.gpu_volume_mapper, image_data)
        self._configure_mapper(self.cpu_fallback_mapper, image_data)

        self._configure_volume_transfer_functions(image_data)
        self.volume.SetMapper(self.volume_mapper)
        self.volume.SetProperty(self.volume_property)
        self._apply_volume_render_mode()
        self._apply_cropping()

    def _configure_mapper(self, mapper: vtk.vtkAbstractVolumeMapper, image_data: vtk.vtkImageData) -> None:
        mapper.SetInputData(image_data)
        if hasattr(mapper, "SetBlendModeToComposite"):
            mapper.SetBlendModeToComposite()
        if hasattr(mapper, "SetAutoAdjustSampleDistances"):
            mapper.SetAutoAdjustSampleDistances(0)
        if hasattr(mapper, "UseJitteringOn"):
            mapper.UseJitteringOn()
        if hasattr(mapper, "SetCropping"):
            mapper.SetCropping(0)
        if isinstance(mapper, vtk.vtkSmartVolumeMapper):
            # Headless servers often fail on pure GPU-only mode; prefer robust CPU ray-cast/default.
            smart_mode = os.getenv("VISIVO_SMART_MAPPER_MODE", "raycast").strip().lower()
            if smart_mode == "gpu" and hasattr(mapper, "SetRequestedRenderModeToGPU"):
                mapper.SetRequestedRenderModeToGPU()
            elif smart_mode == "default" and hasattr(mapper, "SetRequestedRenderModeToDefault"):
                mapper.SetRequestedRenderModeToDefault()
            elif hasattr(mapper, "SetRequestedRenderModeToRayCast"):
                mapper.SetRequestedRenderModeToRayCast()
            elif hasattr(mapper, "SetRequestedRenderModeToDefault"):
                mapper.SetRequestedRenderModeToDefault()

    def _switch_active_mapper(self, mapper_name: str) -> None:
        if mapper_name == self._active_mapper_name:
            return
        if mapper_name == "gpu":
            if self.gpu_volume_mapper is None:
                self._fallback_reason = "gpu-mapper-unavailable"
                self._log.warning("GPU mapper requested but unavailable; staying on CPU-safe path")
                return
            self.volume_mapper = self.gpu_volume_mapper
            self._selected_render_path = "gpu"
        else:
            self.volume_mapper = self.cpu_fallback_mapper
            self._selected_render_path = "cpu"
        self.volume.SetMapper(self.volume_mapper)
        self._active_mapper_name = mapper_name
        self._apply_volume_render_mode()
        self._apply_cropping()
        if hasattr(self, "current_profile"):
            self.set_profile(self.current_profile)
        self._log.warning("Switched volume mapper to %s", mapper_name)

    def _detect_runtime_capabilities(self) -> None:
        vendor = ""
        renderer = ""
        version = ""
        capabilities_report = ""
        probe_error: str | None = None
        render_probe_succeeded = False
        try:
            self.render_window.Render()
            render_probe_succeeded = True
            vendor, renderer, version, capabilities_report = self._probe_opengl_context()
        except Exception as exc:  # pragma: no cover - backend-specific probe path
            probe_error = str(exc)
            self._log.warning("Renderer capability probe render failed: %s", exc)

        offscreen_enabled = bool(
            hasattr(self.render_window, "GetOffScreenRendering") and self.render_window.GetOffScreenRendering()
        )
        use_offscreen_buffers = bool(
            hasattr(self.render_window, "GetUseOffScreenBuffers") and self.render_window.GetUseOffScreenBuffers()
        )
        supports_opengl = self._safe_window_bool("SupportsOpenGL")
        direct_rendering = self._safe_window_bool("IsDirect")
        gpu_mapper_available = self.gpu_volume_mapper is not None
        cpu_fallback_available = self.cpu_fallback_mapper is not None
        backend_implies_opengl = self._render_window_backend in {
            "vtkEGLRenderWindow",
            "vtkOSOpenGLRenderWindow",
            "vtkXOpenGLRenderWindow",
            "vtkCocoaRenderWindow",
            "vtkWin32OpenGLRenderWindow",
        }
        opengl_available = any([vendor, renderer, version]) or bool(capabilities_report)
        gpu_context_available = bool(
            render_probe_succeeded
            and offscreen_enabled
            and (
                opengl_available
                or supports_opengl is True
                or backend_implies_opengl
            )
        )
        gpu_offscreen_available = bool(gpu_mapper_available and gpu_context_available)

        if gpu_offscreen_available:
            self._switch_active_mapper("gpu")
            if self._render_window_backend == "vtkEGLRenderWindow" and not self.stability_mode:
                capability_profile = "gpu-high"
            else:
                capability_profile = "gpu-balanced"
            fallback_reason = None
        else:
            self._switch_active_mapper("smart")
            capability_profile = "cpu-safe"
            if probe_error:
                fallback_reason = f"probe-error:{probe_error}"
            elif not gpu_mapper_available:
                fallback_reason = "gpu-mapper-unavailable"
            elif not offscreen_enabled:
                fallback_reason = "offscreen-unavailable"
            elif not gpu_context_available:
                fallback_reason = "opengl-unavailable"
            else:
                fallback_reason = "gpu-offscreen-unavailable"

        self._capability_profile_name = capability_profile
        self._fallback_reason = fallback_reason
        self._runtime_capabilities = {
            "renderWindowBackend": self._render_window_backend,
            "renderWindowRequest": self._render_window_request,
            "offscreenEnabled": offscreen_enabled,
            "useOffscreenBuffers": use_offscreen_buffers,
            "renderProbeSucceeded": render_probe_succeeded,
            "supportsOpenGL": supports_opengl,
            "directRendering": direct_rendering,
            "openGLVendor": vendor or None,
            "openGLRenderer": renderer or None,
            "openGLVersion": version or None,
            "openGLReport": capabilities_report or None,
            "openglAvailable": opengl_available,
            "gpuContextAvailable": gpu_context_available,
            "volumeMapperClass": self.volume_mapper.GetClassName() if self.volume_mapper is not None else None,
            "activeMapperClass": self.volume_mapper.GetClassName() if self.volume_mapper is not None else None,
            "gpuMapperClass": self.gpu_volume_mapper.GetClassName() if self.gpu_volume_mapper is not None else None,
            "cpuMapperClass": self.cpu_fallback_mapper.GetClassName() if self.cpu_fallback_mapper is not None else None,
            "gpuMapperAvailable": gpu_mapper_available,
            "cpuFallbackAvailable": cpu_fallback_available,
            "gpuOffscreenAvailable": gpu_offscreen_available,
            "selectedRenderPath": self._selected_render_path,
            "capabilityProfile": self._capability_profile_name,
            "fallbackReason": self._fallback_reason,
        }
        self._log.warning(
            "Renderer capabilities backend=%s vendor=%s renderer=%s version=%s gpuContext=%s gpuOffscreen=%s cpuFallback=%s profile=%s path=%s mapper=%s fallback=%s",
            self._render_window_backend,
            vendor or "unknown",
            renderer or "unknown",
            version or "unknown",
            gpu_context_available,
            gpu_offscreen_available,
            cpu_fallback_available,
            self._capability_profile_name,
            self._selected_render_path,
            self._runtime_capabilities["volumeMapperClass"] or "unknown",
            self._fallback_reason or "none",
        )

    def _safe_window_string(self, method_name: str) -> str:
        method = getattr(self.render_window, method_name, None)
        if not callable(method):
            return ""
        try:
            value = method()
        except Exception:
            return ""
        return str(value).strip()

    def _safe_window_bool(self, method_name: str) -> bool | None:
        method = getattr(self.render_window, method_name, None)
        if not callable(method):
            return None
        try:
            return bool(method())
        except Exception:
            return None

    def _probe_opengl_context(self) -> tuple[str, str, str, str]:
        vendor = self._safe_window_string("GetOpenGLVendor")
        renderer = self._safe_window_string("GetOpenGLRenderer")
        version = self._safe_window_string("GetOpenGLVersion")
        report = self._safe_window_string("ReportCapabilities")
        if report:
            parsed_vendor, parsed_renderer, parsed_version = self._parse_opengl_report(report)
            vendor = vendor or parsed_vendor
            renderer = renderer or parsed_renderer
            version = version or parsed_version
        return vendor, renderer, version, report

    def _parse_opengl_report(self, report: str) -> tuple[str, str, str]:
        text = report.strip()
        if not text:
            return ("", "", "")

        patterns = {
            "vendor": [
                r"OpenGL vendor string:\s*(.+)",
                r"Vendor:\s*(.+)",
            ],
            "renderer": [
                r"OpenGL renderer string:\s*(.+)",
                r"Renderer:\s*(.+)",
            ],
            "version": [
                r"OpenGL version string:\s*(.+)",
                r"Version:\s*(.+)",
            ],
        }

        def extract(keys: list[str]) -> str:
            for pattern in keys:
                match = re.search(pattern, text, flags=re.IGNORECASE)
                if match:
                    return match.group(1).strip()
            return ""

        return (
            extract(patterns["vendor"]),
            extract(patterns["renderer"]),
            extract(patterns["version"]),
        )

    def _smart_mapper_mode_name(self, value: int | None) -> str | None:
        if value is None:
            return None
        mapper = vtk.vtkSmartVolumeMapper
        mapping = {
            getattr(mapper, "DefaultRenderMode", object()): "default",
            getattr(mapper, "RayCastRenderMode", object()): "raycast",
            getattr(mapper, "GPURenderMode", object()): "gpu",
            getattr(mapper, "OSPRayRenderMode", object()): "ospray",
            getattr(mapper, "AnariRenderMode", object()): "anari",
            getattr(mapper, "InvalidRenderMode", object()): "invalid",
            getattr(mapper, "UndefinedRenderMode", object()): "undefined",
        }
        return mapping.get(value, str(value))

    def _active_mapper_diagnostics(self) -> dict[str, Any]:
        active_mapper_class = self.volume_mapper.GetClassName() if self.volume_mapper is not None else None
        requested_mapper_class = self.gpu_volume_mapper.GetClassName() if self.gpu_volume_mapper is not None else None
        if self._active_mapper_name != "gpu":
            requested_mapper_class = self.cpu_fallback_mapper.GetClassName() if self.cpu_fallback_mapper is not None else None

        smart_requested_mode: str | None = None
        smart_last_used_mode: str | None = None
        if isinstance(self.volume_mapper, vtk.vtkSmartVolumeMapper):
            requested_mode = None
            last_used_mode = None
            if hasattr(self.volume_mapper, "GetRequestedRenderMode"):
                try:
                    requested_mode = int(self.volume_mapper.GetRequestedRenderMode())
                except Exception:
                    requested_mode = None
            if hasattr(self.volume_mapper, "GetLastUsedRenderMode"):
                try:
                    last_used_mode = int(self.volume_mapper.GetLastUsedRenderMode())
                except Exception:
                    last_used_mode = None
            smart_requested_mode = self._smart_mapper_mode_name(requested_mode)
            smart_last_used_mode = self._smart_mapper_mode_name(last_used_mode)

        return {
            "activeMapperClass": active_mapper_class,
            "requestedMapperClass": requested_mapper_class,
            "smartMapperRequestedMode": smart_requested_mode,
            "smartMapperLastUsedMode": smart_last_used_mode,
        }

    def _configure_slice_pipeline(self, image_data: vtk.vtkImageData) -> None:
        self.slice_mapper.SetInputData(image_data)
        self._apply_slice_axis()
        default_slice = self._slice_bounds_for_axis(self.slice_axis)[0]
        self._set_slice_index(default_slice)
        self.slice_actor.SetMapper(self.slice_mapper)
        self.slice_actor.GetProperty().SetInterpolationTypeToLinear()
        self.slice_actor.GetProperty().SetOpacity(1.0)
        self.slice_actor.SetVisibility(0)
        self._apply_slice_window_level()

    def _configure_volume_transfer_functions(self, image_data: vtk.vtkImageData) -> None:
        lo, hi = self._initial_scalar_range(image_data)
        if hi <= lo:
            hi = lo + 1.0
        self._volume_scalar_range = (lo, hi)

        color = vtk.vtkColorTransferFunction()
        opacity = vtk.vtkPiecewiseFunction()
        for fraction, rgb in self._volume_color_points:
            scalar = lo + (hi - lo) * fraction
            color.AddRGBPoint(scalar, *rgb)
        for fraction, alpha in self._volume_opacity_points:
            scalar = lo + (hi - lo) * fraction
            opacity.AddPoint(scalar, self._scaled_opacity(alpha))

        self.volume_property.SetColor(color)
        self.volume_property.SetScalarOpacity(opacity)
        self.volume_property.SetInterpolationTypeToLinear()
        self.volume_property.SetIndependentComponents(1)

    def _configure_outline(self, image_data: vtk.vtkImageData) -> None:
        outline_filter = vtk.vtkOutlineFilter()
        outline_filter.SetInputData(image_data)
        outline_mapper = vtk.vtkPolyDataMapper()
        outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
        self.outline_actor.SetMapper(outline_mapper)
        self.outline_actor.GetProperty().SetColor(0.9, 0.9, 0.9)
        self.outline_actor.GetProperty().SetLineWidth(1.5)

    def _configure_isosurface_pipeline(self, image_data: vtk.vtkImageData) -> None:
        scalar_range = image_data.GetScalarRange()
        default_iso = float(scalar_range[0] + (scalar_range[1] - scalar_range[0]) * 0.5)
        self.iso_value = default_iso
        self.isosurface_pipeline = build_isosurface_pipeline(
            image_data=image_data,
            iso_value=default_iso,
            visual_mode="high-quality",
        )
        self.isosurface_pipeline.actor.SetVisibility(0)

    def _initial_scalar_range(self, image_data: vtk.vtkImageData) -> tuple[float, float]:
        scalars = image_data.GetPointData().GetScalars()
        if scalars is None or scalars.GetNumberOfTuples() == 0:
            scalar_range = image_data.GetScalarRange()
            return float(scalar_range[0]), float(scalar_range[1])

        values = numpy_support.vtk_to_numpy(scalars)
        if values.size == 0:
            scalar_range = image_data.GetScalarRange()
            return float(scalar_range[0]), float(scalar_range[1])

        finite = values[np.isfinite(values)]
        if finite.size == 0:
            scalar_range = image_data.GetScalarRange()
            return float(scalar_range[0]), float(scalar_range[1])

        max_samples = 262_144
        if finite.size > max_samples:
            stride = max(finite.size // max_samples, 1)
            finite = finite[::stride]

        if finite.size < 16:
            lo = float(finite.min())
            hi = float(finite.max())
        else:
            lo, hi = np.percentile(finite, [1.0, 99.0]).astype(float)

        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            scalar_range = image_data.GetScalarRange()
            lo, hi = float(scalar_range[0]), float(scalar_range[1])
        return lo, hi

    def _scaled_opacity(self, alpha: float) -> float:
        return min(max(float(alpha) * float(self.volume_opacity_scale), 0.0), 1.0)

    def _refresh_volume_opacity(self) -> None:
        lo, hi = self._volume_scalar_range
        opacity = vtk.vtkPiecewiseFunction()
        for fraction, alpha in self._volume_opacity_points:
            scalar = lo + (hi - lo) * fraction
            opacity.AddPoint(scalar, self._scaled_opacity(alpha))
        self.volume_property.SetScalarOpacity(opacity)

    def _normalize_visualization_mode(self, mode: str) -> str:
        normalized = str(mode).strip().casefold().replace("_", "-")
        if normalized in {"volume", "volumetric", "volume-rendering", "volume-render"}:
            return "volume"
        if normalized in {"isosurface", "iso-surface", "iso", "surface"}:
            return "isosurface"
        return "volume"

    def get_visualization_mode(self) -> str:
        return self.visualization_mode

    def get_iso_value(self) -> float | None:
        return self.iso_value

    def get_scalar_range(self) -> tuple[float, float]:
        if self.image_data is None:
            return (0.0, 1.0)
        scalar_range = self.image_data.GetScalarRange()
        lo = float(scalar_range[0])
        hi = float(scalar_range[1])
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            return (0.0, 1.0)
        return (lo, hi)

    def get_volume_params(self) -> dict[str, Any]:
        lo, hi = self._slice_bounds_for_axis(self.slice_axis)
        span = max(1, hi - lo)
        slice_position = 0.5 if self.slice_index is None else (self.slice_index - lo) / span
        return {
            "activeMapper": self._active_mapper_name,
            "selectedRenderPath": self._selected_render_path,
            "capabilityProfile": self._capability_profile_name,
            "renderMode": self.volume_render_mode,
            "opacityScale": self.volume_opacity_scale,
            "sampleDistanceScale": self.volume_sample_distance_scale_override,
            "imageSampleDistance": self.volume_image_sample_distance_override,
            "shade": self.volume_shade_override,
            "sliceAxis": self.slice_axis,
            "sliceIndex": self.slice_index,
            "sliceMaxIndex": hi,
            "slicePosition": float(min(max(slice_position, 0.0), 1.0)),
            "cropping": {
                "enabled": self.cropping_enabled,
                "bounds": list(self.cropping_bounds_norm),
            },
        }

    def get_runtime_capabilities(self) -> dict[str, Any]:
        capabilities = dict(self._runtime_capabilities)
        capabilities.update(self._active_mapper_diagnostics())
        capabilities["volumeMapperClass"] = capabilities.get("activeMapperClass")
        capabilities["selectedRenderPath"] = self._selected_render_path
        capabilities["capabilityProfile"] = self._capability_profile_name
        capabilities["fallbackReason"] = self._fallback_reason
        return capabilities

    def get_renderer_diagnostics(self) -> dict[str, Any]:
        diagnostics = self.get_runtime_capabilities()
        diagnostics.update(
            {
                "activeMapper": self._active_mapper_name,
                "selectedRenderPath": self._selected_render_path,
                "capabilityProfile": self._capability_profile_name,
                "visualizationMode": self.visualization_mode,
                "volumeRenderMode": self.volume_render_mode,
                "stabilityMode": self.stability_mode,
            }
        )
        return diagnostics

    def set_iso_value(self, iso_value: float | None) -> None:
        if iso_value is None:
            return
        self.iso_value = float(iso_value)
        if self.isosurface_pipeline is not None:
            self.isosurface_pipeline.set_iso_value(self.iso_value)

    def set_volume_opacity_scale(self, opacity_scale: float) -> None:
        self.volume_opacity_scale = min(max(float(opacity_scale), 0.0), 4.0)
        self._refresh_volume_opacity()

    def set_volume_params(self, params: dict[str, Any]) -> None:
        if not isinstance(params, dict):
            return
        render_mode = params.get("renderMode", params.get("mode"))
        if isinstance(render_mode, str):
            normalized_mode = render_mode.strip().lower().replace("_", "-")
            if normalized_mode in {"composite", "volume", "raycast", "ray-cast"}:
                self.volume_render_mode = "composite"
            elif normalized_mode in {"mip", "maximum", "maximum-intensity"}:
                self.volume_render_mode = "mip"
            elif normalized_mode in {"slice", "orthoslice", "ortho-slice"}:
                self.volume_render_mode = "slice"
        if isinstance(params.get("opacityScale"), (int, float)):
            self.set_volume_opacity_scale(float(params["opacityScale"]))
        if isinstance(params.get("sampleDistanceScale"), (int, float)):
            self.volume_sample_distance_scale_override = max(0.1, float(params["sampleDistanceScale"]))
        if isinstance(params.get("imageSampleDistance"), (int, float)):
            self.volume_image_sample_distance_override = max(0.5, min(8.0, float(params["imageSampleDistance"])))
        if isinstance(params.get("shade"), bool):
            self.volume_shade_override = bool(params["shade"])
        if isinstance(params.get("sliceAxis"), str):
            normalized_axis = params["sliceAxis"].strip().lower()
            if normalized_axis in {"x", "y", "z"}:
                self.slice_axis = normalized_axis
                self._apply_slice_axis()
        if isinstance(params.get("sliceIndex"), (int, float)):
            self._set_slice_index(int(params["sliceIndex"]))
        if isinstance(params.get("slicePosition"), (int, float)):
            self._set_slice_from_normalized(float(params["slicePosition"]))
        crop_payload = params.get("cropping")
        if isinstance(crop_payload, dict):
            enabled = crop_payload.get("enabled")
            if isinstance(enabled, bool):
                self.cropping_enabled = enabled
            bounds = crop_payload.get("bounds")
            if isinstance(bounds, (list, tuple)) and len(bounds) == 6:
                floats = []
                for value in bounds:
                    if not isinstance(value, (int, float)):
                        floats = []
                        break
                    floats.append(float(value))
                if len(floats) == 6:
                    x0, x1, y0, y1, z0, z1 = floats
                    self.cropping_bounds_norm = (
                        max(0.0, min(1.0, x0)),
                        max(0.0, min(1.0, x1)),
                        max(0.0, min(1.0, y0)),
                        max(0.0, min(1.0, y1)),
                        max(0.0, min(1.0, z0)),
                        max(0.0, min(1.0, z1)),
                    )

        self._apply_volume_render_mode()
        self._apply_cropping()
        self._apply_slice_window_level()
        self._apply_visualization_mode()

    def set_visualization_mode(self, mode: str) -> None:
        self.visualization_mode = self._normalize_visualization_mode(mode)
        self._apply_visualization_mode()

    def _apply_visualization_mode(self) -> None:
        is_volume = self.visualization_mode == "volume"
        show_slice = is_volume and self.volume_render_mode == "slice"
        self.volume.SetVisibility(1 if is_volume and not show_slice else 0)
        self.slice_actor.SetVisibility(1 if show_slice else 0)
        if self.isosurface_pipeline is not None:
            self.isosurface_pipeline.actor.SetVisibility(0 if is_volume else 1)
        self.outline_actor.SetVisibility(1 if is_volume else 0)
        self.set_profile(self.current_profile)

    def _apply_volume_render_mode(self) -> None:
        if self.volume_render_mode == "mip":
            self.volume_mapper.SetBlendModeToMaximumIntensity()
        else:
            self.volume_mapper.SetBlendModeToComposite()

    def _apply_cropping(self) -> None:
        if self.image_data is None or not hasattr(self.volume_mapper, "CroppingOn"):
            return
        if not self.cropping_enabled or self.volume_render_mode == "slice":
            self.volume_mapper.CroppingOff()
            return
        xmin, xmax, ymin, ymax, zmin, zmax = self._volume_bounds_world()
        bx0, bx1, by0, by1, bz0, bz1 = self.cropping_bounds_norm
        wx0 = xmin + (xmax - xmin) * min(bx0, bx1)
        wx1 = xmin + (xmax - xmin) * max(bx0, bx1)
        wy0 = ymin + (ymax - ymin) * min(by0, by1)
        wy1 = ymin + (ymax - ymin) * max(by0, by1)
        wz0 = zmin + (zmax - zmin) * min(bz0, bz1)
        wz1 = zmin + (zmax - zmin) * max(bz0, bz1)
        self.volume_mapper.SetCroppingRegionPlanes(wx0, wx1, wy0, wy1, wz0, wz1)
        if hasattr(self.volume_mapper, "SetCroppingRegionFlagsToSubVolume"):
            self.volume_mapper.SetCroppingRegionFlagsToSubVolume()
        self.volume_mapper.CroppingOn()

    def _volume_bounds_world(self) -> tuple[float, float, float, float, float, float]:
        if self.image_data is None:
            return (0.0, 1.0, 0.0, 1.0, 0.0, 1.0)
        extent = self.image_data.GetExtent()
        origin = self.image_data.GetOrigin()
        spacing = self.image_data.GetSpacing()

        def bounds_1d(i_min: int, i_max: int, o: float, s: float) -> tuple[float, float]:
            a = o + i_min * s
            b = o + i_max * s
            return (min(a, b), max(a, b))

        xmin, xmax = bounds_1d(extent[0], extent[1], origin[0], spacing[0])
        ymin, ymax = bounds_1d(extent[2], extent[3], origin[1], spacing[1])
        zmin, zmax = bounds_1d(extent[4], extent[5], origin[2], spacing[2])
        return (xmin, xmax, ymin, ymax, zmin, zmax)

    def _apply_slice_axis(self) -> None:
        if self.slice_axis == "x":
            self.slice_mapper.SetOrientationToX()
        elif self.slice_axis == "y":
            self.slice_mapper.SetOrientationToY()
        else:
            self.slice_mapper.SetOrientationToZ()

    def _apply_slice_window_level(self) -> None:
        # Use robust scalar range first to avoid all-black slices with strong outliers.
        lo, hi = self._volume_scalar_range
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            lo, hi = self.get_scalar_range()
        if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
            lo, hi = 0.0, 1.0
        window = max(hi - lo, 1e-6)
        level = (hi + lo) * 0.5
        self.slice_actor.GetProperty().SetColorWindow(float(window))
        self.slice_actor.GetProperty().SetColorLevel(float(level))

    def _slice_bounds_for_axis(self, axis: str) -> tuple[int, int]:
        if self.image_data is None:
            return (0, 0)
        extent = self.image_data.GetExtent()
        if axis == "x":
            return (int(extent[0]), int(extent[1]))
        if axis == "y":
            return (int(extent[2]), int(extent[3]))
        return (int(extent[4]), int(extent[5]))

    def _set_slice_index(self, index: int) -> None:
        lo, hi = self._slice_bounds_for_axis(self.slice_axis)
        safe = min(max(int(index), lo), hi)
        self.slice_index = safe
        self.slice_mapper.SetSliceNumber(safe)

    def _set_slice_from_normalized(self, position: float) -> None:
        lo, hi = self._slice_bounds_for_axis(self.slice_axis)
        t = min(max(float(position), 0.0), 1.0)
        idx = int(round(lo + (hi - lo) * t))
        self._set_slice_index(idx)

    def _volume_sample_distance_for_profile(self, profile: QualityProfile) -> float:
        spacing = (1.0, 1.0, 1.0)
        if self.image_data is not None:
            spacing = self.image_data.GetSpacing()
        positives = [abs(float(v)) for v in spacing if np.isfinite(v) and float(v) > 0.0]
        base_spacing = min(positives) if positives else 1.0
        base_spacing = max(base_spacing, 1e-3)

        if self.volume_sample_distance_scale_override is not None:
            sample_scale = self.volume_sample_distance_scale_override
        else:
            sample_scale = float(profile.sample_distance_scale)

        if profile.name == "interactive":
            sample_scale *= self.interactive_boost
        if self.stability_mode:
            sample_scale = min(max(sample_scale, 1.2), 2.6)
        return base_spacing * sample_scale

    def set_profile(self, profile: QualityProfile) -> None:
        self.current_profile = profile

        if self.visualization_mode == "volume":
            if self.volume_render_mode == "slice":
                self.slice_actor.GetProperty().SetOpacity(0.95)
                self.outline_actor.GetProperty().SetOpacity(0.4)
                return

            if self.volume_render_mode == "mip":
                shade_enabled = False
            else:
                shade_enabled = self.volume_shade_override if self.volume_shade_override is not None else profile.shade
            if shade_enabled and not self.stability_mode:
                self.volume_property.SetShade(1)
                self.volume_property.SetAmbient(0.25)
                self.volume_property.SetDiffuse(0.7)
                self.volume_property.SetSpecular(0.15)
                self.volume_property.SetSpecularPower(12.0)
            else:
                self.volume_property.SetShade(0)

            if hasattr(self.volume_mapper, "SetInteractiveUpdateRate"):
                self.volume_mapper.SetInteractiveUpdateRate(profile.update_rate_hz)
            self.volume_mapper.SetSampleDistance(self._volume_sample_distance_for_profile(profile))
            image_sample = self.volume_image_sample_distance_override
            if image_sample is None:
                image_sample = 2.2 if profile.name == "interactive" else 1.0
            if self.stability_mode and profile.name == "interactive":
                image_sample = max(image_sample, 2.4)
            if hasattr(self.volume_mapper, "SetImageSampleDistance"):
                self.volume_mapper.SetImageSampleDistance(float(image_sample))
            self.outline_actor.GetProperty().SetOpacity(0.9 if profile.name == "interactive" else 0.35)
        else:
            if self.isosurface_pipeline is not None:
                if profile.name == "interactive":
                    self.isosurface_pipeline.set_interactive_visuals()
                else:
                    self.isosurface_pipeline.set_high_quality_visuals()

    def set_mode(self, mode: str) -> None:
        normalized = str(mode).strip().casefold()
        if normalized == "interactive":
            self.set_profile(INTERACTIVE_PROFILE)
        else:
            self.set_profile(HIGH_QUALITY_PROFILE)

    def resize(self, width: int, height: int, dpr: float = 1.0) -> None:
        effective_dpr = min(max(dpr, 1.0), 1.25)
        if self.stability_mode:
            scale = max(self.user_render_scale * effective_dpr, 0.4)
        else:
            scale = max(self.current_profile.render_scale * self.user_render_scale * effective_dpr, 0.2)

        w = max(64, int(width * scale))
        h = max(64, int(height * scale))
        self.window_width = w if w % 2 == 0 else w - 1
        self.window_height = h if h % 2 == 0 else h - 1
        self.render_window.SetSize(self.window_width, self.window_height)

    def set_user_render_scale(self, render_scale: float) -> None:
        self.user_render_scale = min(max(float(render_scale), 0.4), 1.5)

    def set_interactive_boost(self, boost: float) -> None:
        self.interactive_boost = min(max(float(boost), 1.0), 3.5)
        self.set_profile(self.current_profile)

    def apply_pointer_delta(self, dx_norm: float, dy_norm: float, mode: str = "rotate") -> None:
        camera = self.renderer.GetActiveCamera()
        dx = float(dx_norm)
        dy = float(dy_norm)

        if mode == "pan":
            self._pan_camera(camera, dx, dy)
            return

        camera.Azimuth(-dx * 220.0)
        camera.Elevation(dy * 220.0)
        camera.OrthogonalizeViewUp()
        self.renderer.ResetCameraClippingRange()

    def apply_zoom(self, zoom_factor: float) -> None:
        camera = self.renderer.GetActiveCamera()
        clamped = min(max(zoom_factor, 0.5), 1.8)
        camera.Dolly(clamped)
        self.renderer.ResetCameraClippingRange()

    def _pan_camera(self, camera: vtk.vtkCamera, dx: float, dy: float) -> None:
        pos = np.array(camera.GetPosition(), dtype=np.float64)
        focal = np.array(camera.GetFocalPoint(), dtype=np.float64)
        view_up = np.array(camera.GetViewUp(), dtype=np.float64)

        view_dir = focal - pos
        view_norm = np.linalg.norm(view_dir)
        if view_norm == 0.0:
            return
        view_dir /= view_norm

        right = np.cross(view_dir, view_up)
        right_norm = np.linalg.norm(right)
        if right_norm == 0.0:
            return
        right /= right_norm

        up = np.cross(right, view_dir)
        up /= max(np.linalg.norm(up), 1e-8)

        shift_scale = view_norm * 0.6
        shift = (-dx * right + dy * up) * shift_scale

        camera.SetPosition(*(pos + shift))
        camera.SetFocalPoint(*(focal + shift))
        self.renderer.ResetCameraClippingRange()

    def render_rgb_frame(self) -> tuple[np.ndarray, int, int, dict[str, Any]]:
        if self._closed:
            raise RuntimeError("renderer is closed")
        started_ns = time.time_ns()
        render_started_ns = started_ns
        self.render_window.Render()
        render_finished_ns = time.time_ns()

        capture_started_ns = render_finished_ns
        self.window_to_image.Modified()
        self.window_to_image.Update()
        capture_finished_ns = time.time_ns()

        conversion_started_ns = capture_finished_ns
        vtk_image = self.window_to_image.GetOutput()
        width, height, _ = vtk_image.GetDimensions()
        scalars = vtk_image.GetPointData().GetScalars()
        arr = numpy_support.vtk_to_numpy(scalars).reshape(height, width, 3)
        rgb = np.ascontiguousarray(arr[::-1])
        self._handle_black_frame_detection(rgb)
        finished_ns = time.time_ns()
        mapper_diagnostics = self._active_mapper_diagnostics()
        pipeline_metrics = {
            "renderTimeMs": (render_finished_ns - render_started_ns) / 1e6,
            "frameCaptureReadbackTimeMs": (capture_finished_ns - capture_started_ns) / 1e6,
            "frameConversionTimeMs": (finished_ns - conversion_started_ns) / 1e6,
            "totalFramePipelineTimeMs": (finished_ns - started_ns) / 1e6,
            **mapper_diagnostics,
        }
        return rgb, started_ns, finished_ns, pipeline_metrics

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True

    def _handle_black_frame_detection(self, frame_rgb: np.ndarray) -> None:
        if self.visualization_mode != "volume" or self.volume_render_mode == "slice":
            self._black_frame_streak = 0
            self._black_frame_streak_fallback = 0
            self._dark_frame_streak_total = 0
            return
        # Detect pathological frames where only dark background is present.
        sample = (
            frame_rgb[::4, ::4, :]
            if frame_rgb.shape[0] > 8 and frame_rgb.shape[1] > 8
            else frame_rgb
        )
        mean_intensity = float(np.mean(sample))
        max_intensity = int(np.max(sample))
        std_intensity = float(np.std(sample))
        p99_intensity = float(np.percentile(sample, 99.0))
        dark = (max_intensity <= 1 or mean_intensity < 0.35) or (std_intensity < 2.0 and p99_intensity < 20.0)
        if not dark:
            self._black_frame_streak = 0
            self._black_frame_streak_fallback = 0
            self._dark_frame_streak_total = 0
            return
        self._dark_frame_streak_total += 1

        if self._active_mapper_name == "gpu":
            self._black_frame_streak += 1
            if self._black_frame_streak >= 3:
                self._fallback_reason = "runtime-gpu-fallback:black-frame"
                self._switch_active_mapper("smart")
                self._black_frame_streak = 0
            # Even after GPU fallback attempts, force a visible mode if frames remain dark.
            if self._dark_frame_streak_total >= 8 and self.volume_render_mode != "slice":
                self.volume_render_mode = "slice"
                self._apply_volume_render_mode()
                self._apply_slice_window_level()
                self._apply_visualization_mode()
                self._dark_frame_streak_total = 0
                self._fallback_reason = "runtime-visibility-fallback:slice-mode"
                self._log.warning("Frame remained background-only; forced slice mode for visibility")
            return

        self._black_frame_streak_fallback += 1
        if self._black_frame_streak_fallback >= 5 and self.volume_render_mode != "slice":
            # Last-resort visibility fallback: switch to orthoslice so user sees data immediately.
            self.volume_render_mode = "slice"
            self._apply_volume_render_mode()
            self._apply_slice_window_level()
            self._apply_visualization_mode()
            self._black_frame_streak_fallback = 0
            self._dark_frame_streak_total = 0
            self._fallback_reason = "runtime-visibility-fallback:slice-mode"
            self._log.warning("Volume frame remained dark; switched to slice mode fallback")

    @property
    def target_update_interval(self) -> float:
        return 1.0 / self.current_profile.update_rate_hz
