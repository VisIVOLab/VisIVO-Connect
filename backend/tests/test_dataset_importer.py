from __future__ import annotations

from pathlib import Path

import numpy as np
import pytest

from backend.data import load_image_data


_BLOCK_SIZE = 2880


def _fits_card(keyword: str, value: object | None = None, comment: str | None = None) -> bytes:
    if value is None:
        text = f"{keyword:<8}"
    elif isinstance(value, str):
        text = f"{keyword:<8}= '{value}'"
    elif isinstance(value, bool):
        text = f"{keyword:<8}= {'T' if value else 'F':>20}"
    elif isinstance(value, float):
        text = f"{keyword:<8}= {value:>20.12E}"
    else:
        text = f"{keyword:<8}= {value:>20}"

    if comment:
        text = f"{text} / {comment}"
    return text.encode("ascii").ljust(80, b" ")


def _write_fits_file(path: Path, headers: list[list[tuple[str, object | None, str | None]]], payloads: list[bytes]) -> None:
    with path.open("wb") as handle:
        for header_cards, payload in zip(headers, payloads, strict=True):
            cards = b"".join(_fits_card(keyword, value, comment) for keyword, value, comment in header_cards)
            cards += _fits_card("END")
            header_pad = (-len(cards)) % _BLOCK_SIZE
            handle.write(cards)
            if header_pad:
                handle.write(b" " * header_pad)
            handle.write(payload)
            data_pad = (-len(payload)) % _BLOCK_SIZE
            if data_pad:
                handle.write(b"\0" * data_pad)


def _fits_image_payload(array: np.ndarray) -> bytes:
    return np.ascontiguousarray(array).tobytes(order="C")


def test_load_image_data_reads_fits_hdu_fragment_and_axes(tmp_path: Path) -> None:
    path = tmp_path / "cube.fits"

    primary_header = [
        ("SIMPLE", True, None),
        ("BITPIX", 8, None),
        ("NAXIS", 0, None),
    ]
    image = np.arange(24, dtype=">i2").reshape((4, 3, 2))
    extension_header = [
        ("XTENSION", "IMAGE   ", None),
        ("BITPIX", 16, None),
        ("NAXIS", 3, None),
        ("NAXIS1", 2, None),
        ("NAXIS2", 3, None),
        ("NAXIS3", 4, None),
        ("PCOUNT", 0, None),
        ("GCOUNT", 1, None),
        ("EXTNAME", "SCI", None),
    ]
    _write_fits_file(path, [primary_header, extension_header], [b"", _fits_image_payload(image)])

    image_data = load_image_data(f"{path}#hdu=1")

    assert image_data.GetDimensions() == (2, 3, 4)
    assert image_data.GetScalarComponentAsFloat(0, 0, 0, 0) == 0.0
    assert image_data.GetScalarComponentAsFloat(1, 2, 3, 0) == 23.0

    image_data_by_name = load_image_data(f"{path}#hdu=SCI")
    assert image_data_by_name.GetDimensions() == (2, 3, 4)


def test_load_image_data_rejects_non_3d_fits_cube(tmp_path: Path) -> None:
    path = tmp_path / "plane.fits"
    header = [
        ("SIMPLE", True, None),
        ("BITPIX", 16, None),
        ("NAXIS", 2, None),
        ("NAXIS1", 2, None),
        ("NAXIS2", 3, None),
    ]
    payload = _fits_image_payload(np.arange(6, dtype=">i2").reshape((3, 2)))
    _write_fits_file(path, [header], [payload])

    with pytest.raises(ValueError, match=r"(No 3D FITS HDU found|must be a 3D image cube)"):
        load_image_data(str(path))


def test_load_image_data_rejects_missing_fits_hdu(tmp_path: Path) -> None:
    path = tmp_path / "cube.fits"
    header = [
        ("SIMPLE", True, None),
        ("BITPIX", 16, None),
        ("NAXIS", 3, None),
        ("NAXIS1", 2, None),
        ("NAXIS2", 3, None),
        ("NAXIS3", 4, None),
    ]
    payload = _fits_image_payload(np.arange(24, dtype=">i2").reshape((4, 3, 2)))
    _write_fits_file(path, [header], [payload])

    with pytest.raises(ValueError, match=r"(Could not find FITS HDU|out of range)"):
        load_image_data(f"{path}#hdu=9")


def test_load_image_data_sanitizes_invalid_values_for_fits(tmp_path: Path) -> None:
    from astropy.io import fits

    path = tmp_path / "invalid_values.fits"
    cube = np.array(
        [
            [[0.0, np.nan], [np.inf, -np.inf]],
            [[1.0, 2.0], [3.0, 4.0]],
        ],
        dtype=np.float32,
    )
    fits.HDUList([fits.PrimaryHDU(data=cube)]).writeto(path, overwrite=True)

    image_data = load_image_data(str(path))

    assert image_data.GetDimensions() == (2, 2, 2)
    assert image_data.GetScalarComponentAsFloat(1, 0, 0, 0) == 0.0
    assert image_data.GetScalarComponentAsFloat(0, 1, 0, 0) == 0.0
    assert image_data.GetScalarComponentAsFloat(1, 1, 0, 0) == 0.0


def test_load_image_data_preserves_numpy_support(tmp_path: Path) -> None:
    path = tmp_path / "cube.npy"
    cube = np.arange(12, dtype=np.float32).reshape((3, 2, 2))
    np.save(path, cube)

    image_data = load_image_data(str(path))

    assert image_data.GetDimensions() == (2, 2, 3)
    assert image_data.GetScalarComponentAsFloat(1, 1, 2, 0) == pytest.approx(11.0)
