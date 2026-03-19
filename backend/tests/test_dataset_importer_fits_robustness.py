from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from backend.data import load_image_data


fits = pytest.importorskip("astropy.io.fits")


def _write_fits(path: Path, *hdus: object) -> None:
    fits.HDUList(list(hdus)).writeto(path, overwrite=True)


def _voxel(image_data: object, x: int, y: int, z: int) -> float:
    return float(image_data.GetScalarComponentAsFloat(x, y, z, 0))


def test_fits_defaults_to_named_3d_extension_when_primary_has_no_data(tmp_path: Path) -> None:
    path = tmp_path / "extension_only.fits"
    cube = np.arange(24, dtype=np.float32).reshape((4, 3, 2))
    _write_fits(path, fits.PrimaryHDU(), fits.ImageHDU(data=cube, name="SCI"))

    image_data = load_image_data(str(path))

    assert image_data.GetDimensions() == (2, 3, 4)
    assert _voxel(image_data, 0, 0, 0) == pytest.approx(0.0)
    assert _voxel(image_data, 1, 2, 3) == pytest.approx(23.0)


def test_fits_non_3d_hdu_is_rejected_for_default_and_explicit_selection(tmp_path: Path) -> None:
    path = tmp_path / "non3d.fits"
    _write_fits(path, fits.PrimaryHDU(), fits.ImageHDU(data=np.arange(6, dtype=np.int16).reshape((3, 2)), name="SCI"))

    with pytest.raises(ValueError, match=r"No 3D FITS HDU found"):
        load_image_data(str(path))

    with pytest.raises(ValueError, match=r"must be at least 3D"):
        load_image_data(f"{path}#hdu=SCI")


def test_fits_sanitizes_nan_and_inf_values(tmp_path: Path) -> None:
    path = tmp_path / "nan_inf.fits"
    cube = np.array(
        [
            [[0.0, np.nan], [np.inf, -np.inf]],
            [[1.0, 2.0], [3.0, 4.0]],
        ],
        dtype=np.float32,
    )
    _write_fits(path, fits.PrimaryHDU(data=cube))

    image_data = load_image_data(str(path))

    assert image_data.GetDimensions() == (2, 2, 2)
    assert _voxel(image_data, 1, 0, 0) == pytest.approx(0.0)
    assert _voxel(image_data, 0, 1, 0) == pytest.approx(0.0)
    assert _voxel(image_data, 1, 1, 0) == pytest.approx(0.0)
    assert _voxel(image_data, 0, 0, 1) == pytest.approx(1.0)


def test_fits_integer_cube_applies_scaling_and_blank_sanitization(tmp_path: Path) -> None:
    path = tmp_path / "scaled_blank.fits"
    blank = -999
    raw = np.array(
        [
            [[1, 2], [3, blank]],
            [[5, 6], [7, 8]],
        ],
        dtype=np.int16,
    )
    hdu = fits.PrimaryHDU(data=raw)
    hdu.header["BSCALE"] = 2.0
    hdu.header["BZERO"] = 10.0
    hdu.header["BLANK"] = blank
    _write_fits(path, hdu)

    image_data = load_image_data(str(path))

    assert image_data.GetDimensions() == (2, 2, 2)
    assert _voxel(image_data, 0, 0, 0) == pytest.approx(12.0)
    assert _voxel(image_data, 1, 1, 0) == pytest.approx(0.0)
    assert _voxel(image_data, 1, 1, 1) == pytest.approx(26.0)


def test_fits_large_cube_loads_with_expected_dimensions_and_samples(tmp_path: Path) -> None:
    path = tmp_path / "large_cube.fits"
    cube = np.arange(32 * 48 * 40, dtype=np.float32).reshape((32, 48, 40))
    _write_fits(path, fits.PrimaryHDU(data=cube))

    image_data = load_image_data(str(path))

    assert image_data.GetDimensions() == (40, 48, 32)
    assert _voxel(image_data, 0, 0, 0) == pytest.approx(0.0)
    assert _voxel(image_data, 39, 47, 31) == pytest.approx(float(cube[-1, -1, -1]))


def test_fits_4d_cube_uses_first_index_of_extra_axis_and_loads_as_3d(tmp_path: Path) -> None:
    path = tmp_path / "cube4d.fits"
    cube4d = np.arange(2 * 4 * 3 * 2, dtype=np.float32).reshape((2, 4, 3, 2))
    _write_fits(path, fits.PrimaryHDU(data=cube4d))

    image_data = load_image_data(str(path))

    first_block = cube4d[0]
    assert image_data.GetDimensions() == (2, 3, 4)
    assert _voxel(image_data, 0, 0, 0) == pytest.approx(float(first_block[0, 0, 0]))
    assert _voxel(image_data, 1, 2, 3) == pytest.approx(float(first_block[3, 2, 1]))


def test_fits_hdu_selection_by_index_or_name_and_missing_hdu_errors(tmp_path: Path) -> None:
    path = tmp_path / "selectors.fits"
    sci = np.ones((3, 2, 2), dtype=np.float32)
    den = np.full((3, 2, 2), 5.0, dtype=np.float32)
    _write_fits(path, fits.PrimaryHDU(), fits.ImageHDU(data=sci, name="SCI"), fits.ImageHDU(data=den, name="DENSITY"))

    by_index = load_image_data(f"{path}#hdu=2")
    by_name = load_image_data(f"{path}#hdu=density")

    assert by_index.GetDimensions() == (2, 2, 3)
    assert _voxel(by_index, 0, 0, 0) == pytest.approx(5.0)
    assert _voxel(by_name, 1, 1, 2) == pytest.approx(5.0)

    with pytest.raises(ValueError, match=r"out of range"):
        load_image_data(f"{path}#hdu=9")
    with pytest.raises(ValueError, match=r"Could not find FITS HDU named"):
        load_image_data(f"{path}#hdu=MISSING")
