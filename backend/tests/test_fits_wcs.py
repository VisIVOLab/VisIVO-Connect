from __future__ import annotations

import numpy as np
import pytest
from astropy.io import fits

from backend.data.fits_wcs import compute_pointer_readout, get_slice_reference


def _write_wcs_cube(path) -> None:
    data = np.zeros((4, 5, 6), dtype=np.float32)
    header = fits.Header()
    header["NAXIS"] = 3
    header["NAXIS1"] = 6
    header["NAXIS2"] = 5
    header["NAXIS3"] = 4
    header["CTYPE1"] = "GLON-TAN"
    header["CTYPE2"] = "GLAT-TAN"
    header["CTYPE3"] = "VELO-LSR"
    header["CUNIT1"] = "deg"
    header["CUNIT2"] = "deg"
    header["CUNIT3"] = "km/s"
    header["CRPIX1"] = 3.0
    header["CRPIX2"] = 2.5
    header["CRPIX3"] = 1.0
    header["CRVAL1"] = 10.0
    header["CRVAL2"] = -2.0
    header["CRVAL3"] = 0.0
    header["CDELT1"] = -0.05
    header["CDELT2"] = 0.05
    header["CDELT3"] = 1.0
    fits.PrimaryHDU(data=data, header=header).writeto(path)


def test_slice_reference_reports_celestial_wcs_for_z_slice(tmp_path) -> None:
    dataset = tmp_path / "cube.fits"
    _write_wcs_cube(dataset)

    reference = get_slice_reference(str(dataset), slice_axis="z", slice_index=2, wcs_system="galactic")

    assert reference["wcsAvailable"] is True
    assert reference["selectedWcsSystem"] == "galactic"
    assert reference["selectedSliceAxis"] == "z"
    assert reference["selectedSliceIndex"] == 2
    assert reference["selectedAxisSize"] == 4
    assert reference["sliceAxisSizes"] == {"x": 6, "y": 5, "z": 4}
    assert reference["wcsAxesVisible"] is True
    assert reference["bottomAxis"]["title"] == "Galactic l"
    assert len(reference["bottomAxis"]["ticks"]) >= 3


def test_slice_reference_degrades_gracefully_for_non_celestial_plane(tmp_path) -> None:
    dataset = tmp_path / "cube.fits"
    _write_wcs_cube(dataset)

    reference = get_slice_reference(str(dataset), slice_axis="x", slice_index=1, wcs_system="fk5")

    assert reference["wcsAvailable"] is False
    assert reference["wcsUnavailableReason"] == "slice-axis-not-celestial-plane"
    assert reference["selectedWcsSystem"] == "fk5"


def test_pointer_readout_returns_pixel_and_wcs_coordinates(tmp_path) -> None:
    dataset = tmp_path / "cube.fits"
    _write_wcs_cube(dataset)

    readout = compute_pointer_readout(
        str(dataset),
        slice_axis="z",
        slice_index=1,
        wcs_system="ecliptic",
        x_norm=0.5,
        y_norm=0.5,
    )

    assert readout["available"] is True
    assert readout["selectedWcsSystem"] == "ecliptic"
    assert readout["imageCoord"] is not None
    assert readout["wcsCoord"] is not None
    assert "galactic" in readout["otherSystems"]
    assert "fk5" in readout["otherSystems"]
