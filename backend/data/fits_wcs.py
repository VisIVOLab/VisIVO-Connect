from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlsplit

import numpy as np
from astropy.coordinates import FK5, BarycentricMeanEcliptic, Galactic, SkyCoord
from astropy.io import fits
from astropy.wcs import WCS


_CACHE_MAX_ENTRIES = 8
_FITS_WCS_CACHE: OrderedDict[tuple[str, int | str | None, int, int], "_FitsWcsContext"] = OrderedDict()
_SUPPORTED_WCS_SYSTEMS = {"galactic", "fk5", "ecliptic"}


@dataclass(frozen=True)
class _DatasetRequest:
    path: Path
    fits_hdu: int | str | None = None


@dataclass
class _FitsWcsContext:
    dataset_path: str
    header: fits.Header
    shape_xyz: tuple[int, int, int]
    hdu_index: int
    celestial_wcs: WCS | None
    has_celestial: bool
    ctype: list[str]
    cunit: list[str]


def _parse_dataset_request(raw_path: str) -> _DatasetRequest:
    parsed = urlsplit(raw_path)
    path = Path(parsed.path or raw_path)
    fits_hdu: int | str | None = None
    fragment = parsed.fragment.strip()
    if fragment:
        fragment_params = parse_qs(fragment, keep_blank_values=True)
        if "hdu" in fragment_params and fragment_params["hdu"]:
            fits_hdu = _coerce_hdu_selector(fragment_params["hdu"][0])
        elif fragment.isdigit():
            fits_hdu = int(fragment)
        else:
            fits_hdu = _coerce_hdu_selector(fragment)
    return _DatasetRequest(path=path, fits_hdu=fits_hdu)


def _coerce_hdu_selector(raw_value: str) -> int | str:
    value = raw_value.strip()
    if not value:
        return 0
    try:
        return int(value)
    except ValueError:
        return value


def _select_fits_hdu(hdul: fits.HDUList, fits_hdu: int | str | None) -> tuple[int, Any]:
    if fits_hdu is not None:
        hdu = hdul[fits_hdu]
        return int(hdul.index_of(hdu)), hdu
    for index, hdu in enumerate(hdul):
        data = getattr(hdu, "data", None)
        if data is None:
            continue
        ndim = int(np.ndim(data))
        if ndim >= 3:
            return index, hdu
    raise ValueError("FITS file does not contain a 3D image HDU")


def _cache_key(path: Path, fits_hdu: int | str | None) -> tuple[str, int | str | None, int, int]:
    stat = path.stat()
    return (str(path.resolve()), fits_hdu, int(stat.st_mtime_ns), int(stat.st_size))


def _cache_get(key: tuple[str, int | str | None, int, int]) -> _FitsWcsContext | None:
    entry = _FITS_WCS_CACHE.get(key)
    if entry is None:
        return None
    _FITS_WCS_CACHE.move_to_end(key)
    return entry


def _cache_put(key: tuple[str, int | str | None, int, int], entry: _FitsWcsContext) -> None:
    if key in _FITS_WCS_CACHE:
        _FITS_WCS_CACHE.pop(key, None)
    _FITS_WCS_CACHE[key] = entry
    while len(_FITS_WCS_CACHE) > _CACHE_MAX_ENTRIES:
        _FITS_WCS_CACHE.popitem(last=False)


def _reduce_shape_to_xyz(shape: tuple[int, ...]) -> tuple[int, int, int]:
    if len(shape) < 3:
        raise ValueError("FITS data must be at least 3D for slice WCS")
    reduced = tuple(int(v) for v in shape[-3:])
    return (reduced[2], reduced[1], reduced[0])


def load_fits_wcs_context(dataset_path: str | None) -> _FitsWcsContext | None:
    candidate = (dataset_path or "").strip()
    if not candidate:
        return None
    request = _parse_dataset_request(candidate)
    if not request.path.exists():
        return None
    key = _cache_key(request.path, request.fits_hdu)
    cached = _cache_get(key)
    if cached is not None:
        return cached
    with fits.open(request.path, memmap=True) as hdul:
        hdu_index, hdu = _select_fits_hdu(hdul, request.fits_hdu)
        data = getattr(hdu, "data", None)
        if data is None:
            return None
        shape_xyz = _reduce_shape_to_xyz(tuple(int(v) for v in np.asarray(data).shape))
        header = hdu.header.copy()
        try:
            celestial_wcs = WCS(header, relax=True).celestial
            has_celestial = bool(celestial_wcs.pixel_n_dim == 2 and celestial_wcs.world_n_dim == 2)
        except Exception:
            celestial_wcs = None
            has_celestial = False
        context = _FitsWcsContext(
            dataset_path=candidate,
            header=header,
            shape_xyz=shape_xyz,
            hdu_index=hdu_index,
            celestial_wcs=celestial_wcs,
            has_celestial=has_celestial,
            ctype=[str(header.get(f"CTYPE{i}", "") or "") for i in (1, 2, 3)],
            cunit=[str(header.get(f"CUNIT{i}", "") or "") for i in (1, 2, 3)],
        )
        _cache_put(key, context)
        return context


def _axis_sizes(shape_xyz: tuple[int, int, int]) -> dict[str, int]:
    return {"x": int(shape_xyz[0]), "y": int(shape_xyz[1]), "z": int(shape_xyz[2])}


def _plane_axes_for_slice(slice_axis: str) -> tuple[str, str]:
    axis = str(slice_axis or "z").strip().lower()
    if axis == "x":
        return ("y", "z")
    if axis == "y":
        return ("x", "z")
    return ("x", "y")


def clamp_slice_index(slice_axis: str, slice_index: int | None, shape_xyz: tuple[int, int, int]) -> int:
    sizes = _axis_sizes(shape_xyz)
    axis = str(slice_axis or "z").strip().lower()
    max_index = max(0, sizes.get(axis, 1) - 1)
    if slice_index is None:
        return max_index // 2
    return max(0, min(int(slice_index), max_index))


def get_slice_reference(
    dataset_path: str | None,
    *,
    slice_axis: str,
    slice_index: int | None,
    wcs_system: str = "galactic",
) -> dict[str, Any]:
    context = load_fits_wcs_context(dataset_path)
    selected_system = normalize_wcs_system(wcs_system)
    if context is None:
        return _empty_slice_reference(selected_system, slice_axis)
    sizes = _axis_sizes(context.shape_xyz)
    selected_index = clamp_slice_index(slice_axis, slice_index, context.shape_xyz)
    horizontal_axis, vertical_axis = _plane_axes_for_slice(slice_axis)
    selected_axis_size = sizes.get(slice_axis, 1)
    reference: dict[str, Any] = {
        "wcsAvailable": bool(context.has_celestial and slice_axis == "z"),
        "wcsUnavailableReason": None,
        "selectedWcsSystem": selected_system,
        "supportedWcsSystems": ["galactic", "fk5", "ecliptic"],
        "selectedSliceAxis": slice_axis,
        "selectedSliceIndex": selected_index,
        "selectedAxisSize": selected_axis_size,
        "sliceAxisSizes": sizes,
        "horizontalAxis": horizontal_axis,
        "verticalAxis": vertical_axis,
        "wcsAxesVisible": False,
        "bottomAxis": None,
        "leftAxis": None,
    }
    if not context.has_celestial:
        reference["wcsUnavailableReason"] = "missing-celestial-wcs"
        return reference
    if slice_axis != "z":
        reference["wcsUnavailableReason"] = "slice-axis-not-celestial-plane"
        return reference
    overlay = _build_overlay_axes(context, selected_system)
    reference["wcsAxesVisible"] = bool(overlay)
    reference.update(overlay)
    return reference


def _empty_slice_reference(selected_system: str, slice_axis: str) -> dict[str, Any]:
    return {
        "wcsAvailable": False,
        "wcsUnavailableReason": "dataset-unavailable",
        "selectedWcsSystem": selected_system,
        "supportedWcsSystems": ["galactic", "fk5", "ecliptic"],
        "selectedSliceAxis": slice_axis,
        "selectedSliceIndex": 0,
        "selectedAxisSize": 1,
        "sliceAxisSizes": {"x": 1, "y": 1, "z": 1},
        "horizontalAxis": _plane_axes_for_slice(slice_axis)[0],
        "verticalAxis": _plane_axes_for_slice(slice_axis)[1],
        "wcsAxesVisible": False,
        "bottomAxis": None,
        "leftAxis": None,
    }


def normalize_wcs_system(value: Any) -> str:
    normalized = str(value or "galactic").strip().lower()
    return normalized if normalized in _SUPPORTED_WCS_SYSTEMS else "galactic"


def _build_overlay_axes(context: _FitsWcsContext, selected_system: str) -> dict[str, Any]:
    if context.celestial_wcs is None:
        return {}
    nx, ny, _ = context.shape_xyz
    x_positions = _tick_positions(nx)
    y_positions = _tick_positions(ny)
    bottom_ticks = []
    left_ticks = []
    for x_pixel, x_norm in x_positions:
        coordinate = _transform_pixel_to_system(context.celestial_wcs, x_pixel, (ny - 1) * 0.5, selected_system)
        if coordinate is not None:
            bottom_ticks.append({"position": x_norm, "label": coordinate["lonLabel"]})
    for y_pixel, y_norm in y_positions:
        coordinate = _transform_pixel_to_system(context.celestial_wcs, (nx - 1) * 0.5, y_pixel, selected_system)
        if coordinate is not None:
            left_ticks.append({"position": y_norm, "label": coordinate["latLabel"]})
    axis_titles = _axis_titles_for_system(selected_system)
    return {
        "bottomAxis": {"title": axis_titles[0], "ticks": bottom_ticks},
        "leftAxis": {"title": axis_titles[1], "ticks": left_ticks},
    }


def _tick_positions(size: int) -> list[tuple[float, float]]:
    if size <= 1:
        return [(0.0, 0.0)]
    normalized_positions = [0.0, 0.25, 0.5, 0.75, 1.0]
    positions: list[tuple[float, float]] = []
    for value in normalized_positions:
        pixel = float((size - 1) * value)
        positions.append((pixel, value))
    return positions


def _axis_titles_for_system(system: str) -> tuple[str, str]:
    if system == "fk5":
        return ("RA (J2000)", "Dec (J2000)")
    if system == "ecliptic":
        return ("Ecliptic λ", "Ecliptic β")
    return ("Galactic l", "Galactic b")


def _transform_pixel_to_system(celestial_wcs: WCS, x_pixel: float, y_pixel: float, system: str) -> dict[str, Any] | None:
    try:
        skycoord = celestial_wcs.pixel_to_world(x_pixel, y_pixel)
    except Exception:
        return None
    return _serialize_skycoord(skycoord, system)


def _serialize_skycoord(skycoord: SkyCoord, system: str) -> dict[str, Any]:
    if system == "fk5":
        coord = skycoord.transform_to(FK5(equinox="J2000"))
        lon = float(coord.ra.deg)
        lat = float(coord.dec.deg)
    elif system == "ecliptic":
        coord = skycoord.transform_to(BarycentricMeanEcliptic())
        lon = float(coord.lon.deg)
        lat = float(coord.lat.deg)
    else:
        coord = skycoord.transform_to(Galactic())
        lon = float(coord.l.deg)
        lat = float(coord.b.deg)
    return {
        "system": system,
        "lonDeg": lon,
        "latDeg": lat,
        "lonLabel": f"{lon:.3f}°",
        "latLabel": f"{lat:.3f}°",
    }


def compute_pointer_readout(
    dataset_path: str | None,
    *,
    slice_axis: str,
    slice_index: int | None,
    wcs_system: str,
    x_norm: float,
    y_norm: float,
) -> dict[str, Any]:
    context = load_fits_wcs_context(dataset_path)
    selected_system = normalize_wcs_system(wcs_system)
    if context is None:
        return {
            "available": False,
            "selectedWcsSystem": selected_system,
            "imageCoord": None,
            "voxelIndex": None,
            "wcsCoord": None,
            "otherSystems": {},
            "reason": "dataset-unavailable",
        }
    sizes = _axis_sizes(context.shape_xyz)
    axis = str(slice_axis or "z").strip().lower()
    horizontal_axis, vertical_axis = _plane_axes_for_slice(axis)
    horizontal_size = sizes.get(horizontal_axis, 1)
    vertical_size = sizes.get(vertical_axis, 1)
    pixel_i = max(0, min(int(round(float(x_norm) * max(horizontal_size - 1, 0))), max(horizontal_size - 1, 0)))
    pixel_j = max(
        0,
        min(int(round((1.0 - float(y_norm)) * max(vertical_size - 1, 0))), max(vertical_size - 1, 0)),
    )
    selected_index = clamp_slice_index(axis, slice_index, context.shape_xyz)
    voxel = {"x": 0, "y": 0, "z": 0}
    voxel[horizontal_axis] = pixel_i
    voxel[vertical_axis] = pixel_j
    voxel[axis] = selected_index
    payload = {
        "available": True,
        "selectedWcsSystem": selected_system,
        "imageCoord": {"i": pixel_i, "j": pixel_j},
        "voxelIndex": voxel,
        "wcsCoord": None,
        "otherSystems": {},
        "reason": None,
    }
    if not context.has_celestial:
        payload["reason"] = "missing-celestial-wcs"
        return payload
    if axis != "z":
        payload["reason"] = "slice-axis-not-celestial-plane"
        return payload
    if context.celestial_wcs is None:
        payload["reason"] = "missing-celestial-wcs"
        return payload
    coordinate = _transform_pixel_to_system(context.celestial_wcs, voxel["x"], voxel["y"], selected_system)
    if coordinate is None:
        payload["reason"] = "wcs-transform-failed"
        return payload
    payload["wcsCoord"] = coordinate
    for system in ("galactic", "fk5", "ecliptic"):
        if system == selected_system:
            continue
        extra = _transform_pixel_to_system(context.celestial_wcs, voxel["x"], voxel["y"], system)
        if extra is not None:
            payload["otherSystems"][system] = extra
    return payload
