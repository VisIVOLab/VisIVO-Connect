from __future__ import annotations

import vtk

from backend.rendering.isosurface_pipeline import HIGH_QUALITY_ISOSURFACE_PRESET, INTERACTIVE_ISOSURFACE_PRESET


def test_isosurface_preset_apply_works_with_vtk_property() -> None:
    prop = vtk.vtkActor().GetProperty()

    INTERACTIVE_ISOSURFACE_PRESET.apply(prop)
    assert prop.GetRepresentationAsString().lower() == "wireframe"

    HIGH_QUALITY_ISOSURFACE_PRESET.apply(prop)
    assert prop.GetRepresentationAsString().lower() == "surface"
