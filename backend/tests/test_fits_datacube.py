from __future__ import annotations

import numpy as np
from astropy.io import fits

from tools.validate_fits_datacube import create_synthetic_fits_cube, load_fits_cube


def test_synthetic_fits_cube_loads_default_science_hdu(tmp_path) -> None:
    fits_path = tmp_path / "synthetic.fits"
    create_synthetic_fits_cube(fits_path, size=8)

    cube, hdu_index = load_fits_cube(fits_path)

    assert hdu_index == 1
    assert cube.shape == (8, 8, 8)
    assert cube.dtype == np.float32
    assert np.isfinite(cube).all()


def test_hdu_selection_and_sanitization(tmp_path) -> None:
    fits_path = tmp_path / "mixed_hdus.fits"
    primary = fits.PrimaryHDU(data=np.zeros((4, 4), dtype=np.float32))
    bad_cube = np.array(
        [
            [[0.0, np.nan], [np.inf, -np.inf]],
            [[1.0, 2.0], [3.0, 4.0]],
        ],
        dtype=np.float32,
    )
    science = fits.ImageHDU(data=bad_cube, name="SCI")
    fits.HDUList([primary, science]).writeto(fits_path, overwrite=True)

    default_cube, default_hdu_index = load_fits_cube(fits_path)
    assert default_hdu_index == 1
    assert default_cube.shape == (2, 2, 2)

    selected_cube, selected_hdu_index = load_fits_cube(fits_path, hdu_index=1)
    assert selected_hdu_index == 1
    assert np.isfinite(selected_cube).all()
    assert selected_cube[0, 0, 1] == 0.0
    assert selected_cube[0, 1, 0] == 0.0
    assert selected_cube[0, 1, 1] == 0.0
