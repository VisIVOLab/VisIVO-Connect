from __future__ import annotations

from collections import OrderedDict
from dataclasses import dataclass
from time import perf_counter_ns
from pathlib import Path
import math
from typing import Any
from urllib.parse import parse_qs, urlsplit

import numpy as np
import vtk
from astropy.io import fits
from vtk.util import numpy_support

from backend.core.config import load_config
from backend.core.observability import (
    FitsImportMetrics,
    clear_last_fits_import_metrics,
    record_last_fits_import_metrics,
    set_last_fits_import_details,
)


_NUMPY_SUFFIXES = {".npy"}
_FITS_SUFFIXES = {".fits", ".fit", ".fts"}
_FITS_GZIP_SUFFIXES = (".fits.gz", ".fit.gz", ".fts.gz")
_VALIDITY_MASK_ARRAY_NAME = "_visivo_valid_mask"
_FITS_CACHE_KEY = tuple[str, int | str | None, int, int]


@dataclass(frozen=True)
class _CachedFitsCube:
    cube: np.ndarray
    packed_valid_mask: np.ndarray | None
    mask_shape: tuple[int, ...] | None
    load_details: dict[str, Any] | None = None


_fits_cube_cache: OrderedDict[_FITS_CACHE_KEY, _CachedFitsCube] = OrderedDict()


@dataclass(frozen=True)
class _DatasetRequest:
    path: Path
    fits_hdu: int | str | None = None


@dataclass(frozen=True)
class _DatasetLoadPolicy:
    requested_mode: str
    effective_mode: str
    large_dataset: bool
    dataset_voxel_count: int
    dataset_shape: tuple[int, int, int]
    dataset_bytes_estimate: int
    preview_shape: tuple[int, int, int] | None
    preview_voxel_count: int | None
    preview_downsample_factor: tuple[int, int, int] | None
    preview_bytes_estimate: int | None
    memory_policy_applied: str | None
    large_dataset_policy_applied: bool


def _normalize_path_for_cache(path: Path) -> str:
    return str(path.resolve())


def _cache_get(cache_key: _FITS_CACHE_KEY) -> _CachedFitsCube | None:
    entry = _fits_cube_cache.get(cache_key)
    if entry is None:
        return None
    _fits_cube_cache.move_to_end(cache_key)
    return entry


def _cache_put(cache_key: _FITS_CACHE_KEY, entry: _CachedFitsCube) -> None:
    max_entries = load_config().fits_cache_max_entries
    if max_entries <= 0:
        _fits_cube_cache.clear()
        return
    if cache_key in _fits_cube_cache:
        _fits_cube_cache.pop(cache_key, None)
    _fits_cube_cache[cache_key] = entry
    while len(_fits_cube_cache) > max_entries:
        _fits_cube_cache.popitem(last=False)


def load_image_data(dataset_path: str | None, *, load_mode: str = "auto") -> vtk.vtkImageData:
    clear_last_fits_import_metrics()
    if not dataset_path:
        return _synthetic_cube()

    request = _parse_dataset_request(dataset_path)
    if not request.path.exists():
        return _synthetic_cube()

    suffix = request.path.suffix.lower()
    stem_name = request.path.name.lower()

    if suffix == ".vti":
        return _load_vti(request.path)

    if suffix in {".mhd", ".mha"}:
        return _load_metaimage(request.path)

    if suffix in _NUMPY_SUFFIXES:
        return _load_numpy(request.path)

    if suffix in _FITS_SUFFIXES or any(stem_name.endswith(ext) for ext in _FITS_GZIP_SUFFIXES):
        return _load_fits(request.path, request.fits_hdu, load_mode=load_mode)

    return _synthetic_cube()


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


def _load_vti(path: Path) -> vtk.vtkImageData:
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(str(path))
    reader.Update()
    image_data = reader.GetOutput()
    if image_data is not None and image_data.GetPointData().GetScalars() is not None:
        return image_data
    return _synthetic_cube()


def _load_metaimage(path: Path) -> vtk.vtkImageData:
    reader = vtk.vtkMetaImageReader()
    reader.SetFileName(str(path))
    reader.Update()
    image_data = reader.GetOutput()
    if image_data is not None and image_data.GetPointData().GetScalars() is not None:
        return image_data
    return _synthetic_cube()


def _load_numpy(path: Path) -> vtk.vtkImageData:
    arr = np.load(path, allow_pickle=False)
    if arr.ndim != 3:
        raise ValueError(f".npy datacube must be a 3D array, got {arr.ndim}D")

    cube = np.asarray(arr, dtype=np.float32)
    valid_mask = np.isfinite(cube)
    if not valid_mask.all():
        cube = np.array(cube, copy=True, order="C")
        np.nan_to_num(cube, copy=False, nan=0.0, posinf=0.0, neginf=0.0)
    elif not cube.flags.c_contiguous:
        cube = np.ascontiguousarray(cube)

    invalid_voxel_count = int(valid_mask.size - np.count_nonzero(valid_mask))
    set_last_fits_import_details(
        {
            "validityMaskSource": "importer",
            "validityMaskPresent": True,
            "validityMaskPackedInCache": False,
            "validityMaskAllValid": invalid_voxel_count == 0,
            "invalidVoxelCount": invalid_voxel_count,
            "nanVoxelCount": invalid_voxel_count,
            "cacheHit": False,
        }
    )

    return _numpy_to_vtk_image_data(cube, valid_mask=valid_mask)


def _load_fits(path: Path, fits_hdu: int | str | None, *, load_mode: str = "auto") -> vtk.vtkImageData:
    total_started_ns = perf_counter_ns()
    cache_key = _fits_cache_key(path, fits_hdu if load_mode == "full" else f"{fits_hdu}|{load_mode}")
    cached_entry = _cache_get(cache_key)
    if cached_entry is not None:
        valid_mask = _unpack_valid_mask(cached_entry.packed_valid_mask, cached_entry.mask_shape)
        vtk_build_started_ns = perf_counter_ns()
        image_data = _numpy_to_vtk_image_data(cached_entry.cube, valid_mask=valid_mask)
        vtk_build_finished_ns = perf_counter_ns()
        total_finished_ns = perf_counter_ns()
        invalid_voxel_count = 0 if valid_mask is None else int(valid_mask.size - np.count_nonzero(valid_mask))
        cache_shape = tuple(int(v) for v in cached_entry.cube.shape)
        cache_voxel_count = int(np.prod(cache_shape, dtype=np.int64))
        cached_details = dict(cached_entry.load_details or {})
        cached_details.update(
            {
                "validityMaskSource": "cache",
                "validityMaskPresent": valid_mask is not None,
                "validityMaskPackedInCache": cached_entry.packed_valid_mask is not None,
                "validityMaskAllValid": bool(valid_mask is not None and invalid_voxel_count == 0),
                "invalidVoxelCount": invalid_voxel_count,
                "nanVoxelCount": invalid_voxel_count,
                "cacheHit": True,
                "datasetVoxelCount": cached_details.get("datasetVoxelCount", cache_voxel_count),
                "datasetBytesEstimate": cached_details.get("datasetBytesEstimate", cache_voxel_count * 4),
                "memoryPolicyApplied": cached_details.get("memoryPolicyApplied", "fits-cache-hit"),
            }
        )
        set_last_fits_import_details(cached_details)
        record_last_fits_import_metrics(
            FitsImportMetrics(
                fits_open_ms=0.0,
                hdu_select_ms=0.0,
                sanitize_convert_ms=0.0,
                vtk_build_ms=(vtk_build_finished_ns - vtk_build_started_ns) / 1e6,
                fits_total_ms=(total_finished_ns - total_started_ns) / 1e6,
                cache_hit=True,
            )
        )
        return image_data

    open_started_ns = perf_counter_ns()
    with fits.open(path, memmap=True) as hdul:
        open_finished_ns = perf_counter_ns()

        hdu_select_started_ns = perf_counter_ns()
        hdu_index, hdu = _select_fits_hdu(hdul, fits_hdu)
        hdu_select_finished_ns = perf_counter_ns()

        data = getattr(hdu, "data", None)
        if data is None:
            raise ValueError(f"FITS HDU {hdu_index} does not contain image data")

        cube = np.asarray(data)
        if cube.ndim < 3:
            raise ValueError(f"FITS HDU {hdu_index} must be at least 3D; got {cube.ndim}D data")
        if cube.ndim > 3:
            cube = _reduce_cube_to_first_3_axes(cube)

        load_policy = _decide_fits_load_policy(cube, requested_mode=load_mode)
        source_cube = cube
        if load_policy.effective_mode == "preview":
            source_cube = _build_preview_cube(source_cube, load_policy.preview_downsample_factor)

        sanitize_started_ns = perf_counter_ns()
        cube, valid_mask = _sanitize_fits_cube(source_cube, hdu.header)
        sanitize_finished_ns = perf_counter_ns()
        load_details = {
            "datasetLoadMode": load_policy.effective_mode,
            "largeDataset": load_policy.large_dataset,
            "datasetVoxelCount": load_policy.dataset_voxel_count,
            "datasetBytesEstimate": load_policy.dataset_bytes_estimate,
            "previewShape": list(load_policy.preview_shape) if load_policy.preview_shape is not None else None,
            "previewVoxelCount": load_policy.preview_voxel_count,
            "previewDownsampleFactor": (
                list(load_policy.preview_downsample_factor) if load_policy.preview_downsample_factor is not None else None
            ),
            "previewBytesEstimate": load_policy.preview_bytes_estimate,
            "memoryPolicyApplied": load_policy.memory_policy_applied,
            "largeDatasetPolicyApplied": load_policy.large_dataset_policy_applied,
        }
        if _should_cache_fits_cube(load_policy):
            _store_fits_cache(cache_key, cube, valid_mask, load_details=load_details)

        vtk_build_started_ns = perf_counter_ns()
        image_data = _numpy_to_vtk_image_data(cube, valid_mask=valid_mask)
        vtk_build_finished_ns = perf_counter_ns()

    total_finished_ns = perf_counter_ns()
    invalid_voxel_count = int(valid_mask.size - np.count_nonzero(valid_mask))
    set_last_fits_import_details(
        {
            "validityMaskSource": "importer",
            "validityMaskPresent": True,
            "validityMaskPackedInCache": False,
            "validityMaskAllValid": invalid_voxel_count == 0,
            "invalidVoxelCount": invalid_voxel_count,
            "nanVoxelCount": invalid_voxel_count,
            "cacheHit": False,
            **load_details,
        }
    )
    record_last_fits_import_metrics(
        FitsImportMetrics(
            fits_open_ms=(open_finished_ns - open_started_ns) / 1e6,
            hdu_select_ms=(hdu_select_finished_ns - hdu_select_started_ns) / 1e6,
            sanitize_convert_ms=(sanitize_finished_ns - sanitize_started_ns) / 1e6,
            vtk_build_ms=(vtk_build_finished_ns - vtk_build_started_ns) / 1e6,
            fits_total_ms=(total_finished_ns - total_started_ns) / 1e6,
            cache_hit=False,
        )
    )
    return image_data


def _decide_fits_load_policy(cube: np.ndarray, *, requested_mode: str) -> _DatasetLoadPolicy:
    config = load_config()
    shape = tuple(int(v) for v in np.asarray(cube).shape[-3:])
    voxel_count = int(np.prod(shape, dtype=np.int64))
    dataset_bytes_estimate = voxel_count * 4
    large_dataset = voxel_count > config.large_dataset_voxels
    normalized_mode = str(requested_mode or "auto").strip().lower()
    if normalized_mode not in {"auto", "preview", "full"}:
        normalized_mode = "auto"

    effective_mode = normalized_mode
    if effective_mode == "auto":
        effective_mode = "preview" if large_dataset else "full"

    preview_shape: tuple[int, int, int] | None = None
    preview_voxel_count: int | None = None
    preview_downsample_factor: tuple[int, int, int] | None = None
    preview_bytes_estimate: int | None = None
    memory_policy_applied: str | None = None
    large_dataset_policy_applied = False

    if effective_mode == "preview":
        preview_downsample_factor = _compute_preview_downsample_factor(shape, config.preview_target_voxels)
        preview_shape = tuple(int(math.ceil(dim / factor)) for dim, factor in zip(shape, preview_downsample_factor))
        preview_voxel_count = int(np.prod(preview_shape, dtype=np.int64))
        preview_bytes_estimate = preview_voxel_count * 4
        memory_policy_applied = "preview-first"
        large_dataset_policy_applied = large_dataset
    elif large_dataset:
        memory_policy_applied = "large-dataset-full"
        large_dataset_policy_applied = True

    return _DatasetLoadPolicy(
        requested_mode=normalized_mode,
        effective_mode=effective_mode,
        large_dataset=large_dataset,
        dataset_voxel_count=voxel_count,
        dataset_shape=shape,
        dataset_bytes_estimate=dataset_bytes_estimate,
        preview_shape=preview_shape,
        preview_voxel_count=preview_voxel_count,
        preview_downsample_factor=preview_downsample_factor,
        preview_bytes_estimate=preview_bytes_estimate,
        memory_policy_applied=memory_policy_applied,
        large_dataset_policy_applied=large_dataset_policy_applied,
    )


def _compute_preview_downsample_factor(shape: tuple[int, int, int], target_voxels: int) -> tuple[int, int, int]:
    voxel_count = int(np.prod(shape, dtype=np.int64))
    if voxel_count <= max(1, int(target_voxels)):
        return (1, 1, 1)

    factor = max(1.0, (voxel_count / max(1, int(target_voxels))) ** (1.0 / 3.0))
    factors = [max(1, int(math.ceil(factor))) for _ in shape]
    while True:
        preview_shape = [int(math.ceil(dim / step)) for dim, step in zip(shape, factors)]
        preview_voxels = int(np.prod(preview_shape, dtype=np.int64))
        if preview_voxels <= target_voxels:
            return tuple(factors)
        largest_axis = max(range(3), key=lambda index: preview_shape[index])
        factors[largest_axis] += 1


def _build_preview_cube(cube: np.ndarray, downsample_factor: tuple[int, int, int] | None) -> np.ndarray:
    if downsample_factor is None or downsample_factor == (1, 1, 1):
        return np.asarray(cube)
    zf, yf, xf = downsample_factor
    return np.asarray(cube)[::zf, ::yf, ::xf]


def _should_cache_fits_cube(policy: _DatasetLoadPolicy) -> bool:
    config = load_config()
    if policy.effective_mode == "preview":
        return True
    if policy.dataset_bytes_estimate > int(config.session_memory_budget_mb) * 1024 * 1024:
        return False
    return not policy.large_dataset


def _fits_cache_key(path: Path, fits_hdu: int | str | None) -> _FITS_CACHE_KEY:
    stat = path.stat()
    return (_normalize_path_for_cache(path), fits_hdu, int(stat.st_mtime_ns), int(stat.st_size))



def _pack_valid_mask(valid_mask: np.ndarray | None) -> tuple[np.ndarray | None, tuple[int, ...] | None]:
    if valid_mask is None:
        return None, None

    contiguous = np.ascontiguousarray(valid_mask, dtype=np.bool_)
    shape = tuple(contiguous.shape)
    if contiguous.size == 0:
        return None, shape
    if contiguous.all():
        # Common case: all voxels are valid, so avoid storing a dense mask in cache.
        return None, shape

    packed = np.packbits(contiguous.reshape(-1), bitorder="little")
    return packed, shape


def _unpack_valid_mask(packed_mask: np.ndarray | None, shape: tuple[int, ...] | None) -> np.ndarray | None:
    if shape is None:
        return None
    if packed_mask is None:
        return np.ones(shape, dtype=np.bool_)

    total = int(np.prod(shape, dtype=np.int64))
    unpacked = np.unpackbits(packed_mask, bitorder="little", count=total)
    return unpacked.astype(np.bool_, copy=False).reshape(shape)


def _store_fits_cache(
    cache_key: _FITS_CACHE_KEY,
    cube: np.ndarray,
    valid_mask: np.ndarray | None,
    load_details: dict[str, Any] | None = None,
) -> None:
    packed_mask, mask_shape = _pack_valid_mask(valid_mask)
    entry = _CachedFitsCube(
        cube=np.ascontiguousarray(cube, dtype=np.float32),
        packed_valid_mask=packed_mask,
        mask_shape=mask_shape,
        load_details=dict(load_details) if load_details is not None else None,
    )
    _cache_put(cache_key, entry)


def _select_fits_hdu(hdul: fits.HDUList, selector: int | str | None) -> tuple[int, Any]:
    if selector is None:
        for index, hdu in enumerate(hdul):
            data = getattr(hdu, "data", None)
            if data is not None and np.ndim(data) >= 3:
                return index, hdu
        raise ValueError("No 3D FITS HDU found")

    if isinstance(selector, int):
        if selector < 0 or selector >= len(hdul):
            raise ValueError(f"FITS HDU index {selector} out of range (available: 0..{len(hdul) - 1})")
        return selector, hdul[selector]

    wanted = selector.strip()
    if not wanted:
        return _select_fits_hdu(hdul, None)

    if wanted.isdigit():
        return _select_fits_hdu(hdul, int(wanted))

    for index, hdu in enumerate(hdul):
        extname = str(hdu.header.get("EXTNAME", "")).strip()
        if extname and extname.casefold() == wanted.casefold():
            return index, hdu

    raise ValueError(f"Could not find FITS HDU named {wanted!r}")


def _sanitize_fits_cube(data: np.ndarray, header: fits.Header) -> tuple[np.ndarray, np.ndarray]:
    arr = np.asarray(data)
    if np.iscomplexobj(arr):
        raise ValueError(f"Complex FITS cubes are not supported (dtype={arr.dtype})")

    blank = header.get("BLANK")
    original_dtype = arr.dtype
    try:
        arr = arr.astype(np.float32, copy=(arr.dtype != np.float32))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Unsupported FITS cube dtype {original_dtype}") from exc

    if not arr.flags.c_contiguous:
        arr = np.ascontiguousarray(arr)

    if blank is not None and np.issubdtype(original_dtype, np.integer):
        arr[arr == float(blank)] = np.nan

    valid_mask = np.isfinite(arr)
    if not valid_mask.flags.c_contiguous:
        valid_mask = np.ascontiguousarray(valid_mask)

    if not valid_mask.all():
        np.nan_to_num(arr, copy=False, nan=0.0, posinf=0.0, neginf=0.0)

    return arr, valid_mask


def _reduce_cube_to_first_3_axes(data: np.ndarray) -> np.ndarray:
    """Reduce an N-D FITS cube to 3D by taking index 0 on extra leading axes.

    FITS data read with astropy is typically ordered as (..., z, y, x). When
    ndim > 3 we preserve the last three axes and select the first entry from
    each extra axis.
    """
    arr = np.asarray(data)
    while arr.ndim > 3:
        arr = arr[0]
    return arr


def _numpy_to_vtk_image_data(arr: np.ndarray, valid_mask: np.ndarray | None = None) -> vtk.vtkImageData:
    if arr.ndim != 3:
        raise ValueError(f"vtk image import expects a 3D array, got {arr.ndim}D")

    # FITS datacubes loaded with astropy/numpy are shaped as (z, y, x);
    # VTK dimensions must be set as (x, y, z).
    z, y, x = arr.shape
    contiguous = np.ascontiguousarray(arr, dtype=np.float32)
    image = vtk.vtkImageData()
    image.SetDimensions(x, y, z)
    image.SetExtent(0, x - 1, 0, y - 1, 0, z - 1)

    vtk_scalars = numpy_support.numpy_to_vtk(
        contiguous.ravel(order="C"),
        deep=True,
        array_type=vtk.VTK_FLOAT,
    )
    image.GetPointData().SetScalars(vtk_scalars)

    if valid_mask is not None:
        valid_mask_bool = np.ascontiguousarray(valid_mask, dtype=np.bool_)
        mask_array = np.empty(valid_mask_bool.shape, dtype=np.uint8)
        mask_array[valid_mask_bool] = 255
        mask_array[~valid_mask_bool] = 0
        vtk_mask = numpy_support.numpy_to_vtk(
            mask_array.ravel(order="C"),
            deep=True,
            array_type=vtk.VTK_UNSIGNED_CHAR,
        )
        vtk_mask.SetName(_VALIDITY_MASK_ARRAY_NAME)
        image.GetPointData().AddArray(vtk_mask)

    return image


def _synthetic_cube() -> vtk.vtkImageData:
    src = vtk.vtkRTAnalyticSource()
    src.SetWholeExtent(-128, 128, -128, 128, -96, 96)
    src.SetMaximum(255.0)
    src.Update()
    return src.GetOutput()
