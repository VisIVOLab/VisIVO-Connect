from __future__ import annotations

from dataclasses import dataclass

import vtk

__all__ = [
    "HIGH_QUALITY_ISOSURFACE_PRESET",
    "INTERACTIVE_ISOSURFACE_PRESET",
    "IsosurfacePipeline",
    "IsosurfaceVisualPreset",
    "build_isosurface_pipeline",
]


@dataclass(frozen=True)
class IsosurfaceVisualPreset:
    """Property-level styling for an isosurface actor."""

    name: str
    representation: str
    shading: bool
    opacity: float
    ambient: float
    diffuse: float
    specular: float
    specular_power: float
    line_width: float
    color: tuple[float, float, float]
    edge_visibility: bool = False
    edge_color: tuple[float, float, float] = (0.1, 0.1, 0.1)

    def __post_init__(self) -> None:
        representation = self.representation.strip().casefold()
        if representation not in {"surface", "wireframe"}:
            raise ValueError(f"Unsupported representation {self.representation!r}")

    def apply(self, prop: vtk.vtkProperty) -> None:
        representation = self.representation.strip().casefold()
        if representation == "wireframe":
            prop.SetRepresentationToWireframe()
        else:
            prop.SetRepresentationToSurface()

        if self.shading:
            prop.SetInterpolationToPhong()
        else:
            prop.SetInterpolationToFlat()
        if hasattr(prop, "SetLighting"):
            prop.SetLighting(1 if self.shading else 0)
        prop.SetOpacity(float(self.opacity))
        prop.SetAmbient(float(self.ambient))
        prop.SetDiffuse(float(self.diffuse))
        prop.SetSpecular(float(self.specular))
        prop.SetSpecularPower(float(self.specular_power))
        prop.SetLineWidth(float(self.line_width))
        prop.SetColor(*self.color)
        prop.SetEdgeVisibility(1 if self.edge_visibility else 0)
        prop.SetEdgeColor(*self.edge_color)


INTERACTIVE_ISOSURFACE_PRESET = IsosurfaceVisualPreset(
    name="interactive",
    representation="wireframe",
    shading=False,
    opacity=0.55,
    ambient=0.35,
    diffuse=0.55,
    specular=0.0,
    specular_power=8.0,
    line_width=1.4,
    color=(0.65, 0.9, 1.0),
)

HIGH_QUALITY_ISOSURFACE_PRESET = IsosurfaceVisualPreset(
    name="high-quality",
    representation="surface",
    shading=True,
    opacity=1.0,
    ambient=0.16,
    diffuse=0.84,
    specular=0.32,
    specular_power=28.0,
    line_width=1.0,
    color=(0.98, 0.94, 0.88),
)


def _require_image_scalars(image_data: vtk.vtkImageData) -> None:
    scalars = image_data.GetPointData().GetScalars()
    if scalars is None or scalars.GetNumberOfTuples() == 0:
        raise ValueError("vtkImageData must contain point scalars to build an isosurface pipeline")


def _default_iso_value(image_data: vtk.vtkImageData) -> float:
    scalar_range = image_data.GetScalarRange()
    lo = float(scalar_range[0])
    hi = float(scalar_range[1])
    if hi <= lo:
        return lo
    return lo + (hi - lo) * 0.5


def _create_contour_source() -> tuple[vtk.vtkAlgorithm, str]:
    flying_edges = getattr(vtk, "vtkFlyingEdges3D", None)
    if flying_edges is not None:
        return flying_edges(), "vtkFlyingEdges3D"
    return vtk.vtkMarchingCubes(), "vtkMarchingCubes"


def _preset_for_mode(mode: str) -> IsosurfaceVisualPreset:
    normalized = mode.strip().casefold().replace("_", "-")
    if normalized in {"interactive", "preview", "fast", "low", "wireframe"}:
        return INTERACTIVE_ISOSURFACE_PRESET
    if normalized in {"high-quality", "highquality", "hq", "quality", "surface"}:
        return HIGH_QUALITY_ISOSURFACE_PRESET
    raise ValueError(f"Unsupported visual mode {mode!r}")


class IsosurfacePipeline:
    """Reusable isosurface pipeline for vtkImageData inputs.

    The pipeline keeps the contour algorithm, normals filter, mapper, and actor
    accessible so callers can wire the actor into any renderer and update the
    iso-value or visual mode without touching session-specific code.
    """

    def __init__(
        self,
        image_data: vtk.vtkImageData,
        iso_value: float | None = None,
        visual_mode: str = "high-quality",
    ) -> None:
        _require_image_scalars(image_data)

        self.image_data = image_data
        self.contour_source, self.contour_algorithm_name = _create_contour_source()
        self.preview_contour_source, self.preview_contour_algorithm_name = _create_contour_source()
        self.normals_filter = vtk.vtkPolyDataNormals()
        self.mapper = vtk.vtkPolyDataMapper()
        self.preview_mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()
        self.preview_shrink = vtk.vtkImageShrink3D()

        # Interactive path: downsampled volume to keep first isosurface switch responsive.
        self.preview_shrink.SetInputData(self.image_data)
        self.preview_shrink.SetShrinkFactors(2, 2, 2)
        self.preview_shrink.AveragingOn()
        self.preview_contour_source.SetInputConnection(self.preview_shrink.GetOutputPort())

        self.normals_filter.SetInputConnection(self.contour_source.GetOutputPort())
        self.normals_filter.ConsistencyOn()
        self.normals_filter.AutoOrientNormalsOn()
        self.normals_filter.ComputePointNormalsOn()
        self.normals_filter.ComputeCellNormalsOff()
        self.normals_filter.SplittingOff()
        self.normals_filter.SetFeatureAngle(60.0)

        self.mapper.SetInputConnection(self.normals_filter.GetOutputPort())
        self.mapper.ScalarVisibilityOff()
        self.preview_mapper.SetInputConnection(self.preview_contour_source.GetOutputPort())
        self.preview_mapper.ScalarVisibilityOff()

        self.actor.SetMapper(self.preview_mapper)

        self.visual_preset = HIGH_QUALITY_ISOSURFACE_PRESET
        self.visual_mode = self.visual_preset.name
        self.iso_value = _default_iso_value(image_data) if iso_value is None else float(iso_value)
        self.set_iso_value(self.iso_value)
        self.set_visual_mode(visual_mode)

    @property
    def output_port(self) -> vtk.vtkAlgorithmOutput:
        return self.normals_filter.GetOutputPort()

    def set_iso_value(self, iso_value: float) -> None:
        self.iso_value = float(iso_value)
        self.contour_source.SetInputData(self.image_data)
        self.contour_source.SetValue(0, self.iso_value)
        self.preview_contour_source.SetValue(0, self.iso_value)

    def set_visual_preset(self, preset: IsosurfaceVisualPreset) -> None:
        self.visual_preset = preset
        self.visual_mode = preset.name
        preset.apply(self.actor.GetProperty())

    def set_visual_mode(self, mode: str) -> None:
        preset = _preset_for_mode(mode)
        self.set_visual_preset(preset)

    def set_interactive_visuals(self) -> None:
        self.actor.SetMapper(self.preview_mapper)
        self.set_visual_preset(INTERACTIVE_ISOSURFACE_PRESET)

    def set_high_quality_visuals(self) -> None:
        self.actor.SetMapper(self.mapper)
        self.set_visual_preset(HIGH_QUALITY_ISOSURFACE_PRESET)


def build_isosurface_pipeline(
    image_data: vtk.vtkImageData,
    iso_value: float | None = None,
    visual_mode: str = "high-quality",
) -> IsosurfacePipeline:
    """Build an isosurface pipeline for the provided vtkImageData."""

    return IsosurfacePipeline(image_data=image_data, iso_value=iso_value, visual_mode=visual_mode)
