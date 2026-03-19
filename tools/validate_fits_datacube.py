from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from astropy.io import fits


def build_cube(size: int) -> np.ndarray:
    z, y, x = np.mgrid[-1:1:complex(size), -1:1:complex(size), -1:1:complex(size)]
    sphere = np.exp(-8.0 * (x * x + y * y + z * z))
    wave = 0.35 * (np.sin(10 * x) + np.cos(9 * y) + np.sin(8 * z))
    cube = sphere + wave
    cube = (cube - cube.min()) / (cube.max() - cube.min())
    return (cube * 255.0).astype(np.float32)


def sanitize_volume(volume: np.ndarray) -> np.ndarray:
    arr = np.asarray(volume, dtype=np.float32)
    return np.nan_to_num(arr, nan=0.0, posinf=0.0, neginf=0.0)


def create_synthetic_fits_cube(path: Path, size: int = 32) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    cube = build_cube(size)
    primary = fits.PrimaryHDU()
    science = fits.ImageHDU(data=cube, name="SCI")
    fits.HDUList([primary, science]).writeto(path, overwrite=True)
    return path


def _select_hdu_index(hdul: fits.HDUList, hdu_index: int | None) -> int:
    if hdu_index is not None:
        if hdu_index < 0 or hdu_index >= len(hdul):
            raise IndexError(f"HDU index {hdu_index} out of range for file with {len(hdul)} HDUs")
        return hdu_index

    for index, hdu in enumerate(hdul):
        data = getattr(hdu, "data", None)
        if data is not None and getattr(data, "ndim", 0) == 3:
            return index
    raise ValueError("No 3D FITS HDU found")


def load_fits_cube(path: Path, hdu_index: int | None = None, sanitize: bool = True) -> tuple[np.ndarray, int]:
    with fits.open(path, memmap=False) as hdul:
        index = _select_hdu_index(hdul, hdu_index)
        data = hdul[index].data
        if data is None:
            raise ValueError(f"HDU {index} does not contain image data")
        cube = np.asarray(data, dtype=np.float32)
        if cube.ndim != 3:
            raise ValueError(f"HDU {index} is not a 3D cube: shape={cube.shape}")
        if sanitize:
            cube = sanitize_volume(cube)
        return np.ascontiguousarray(cube), index


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create or validate a synthetic FITS datacube")
    parser.add_argument("--output", type=Path, help="write a synthetic FITS file to this path")
    parser.add_argument("--input", type=Path, help="validate an existing FITS file")
    parser.add_argument("--size", type=int, default=32, help="cube edge length for synthetic files")
    parser.add_argument("--hdu", type=int, default=None, help="explicit HDU index to load")
    parser.add_argument(
        "--keep-invalid-values",
        action="store_true",
        help="skip NaN/Inf sanitization when validating",
    )
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    target = args.input or args.output
    if target is None:
        parser.error("provide --input to validate an existing file or --output to create one")

    if args.input is None:
        create_synthetic_fits_cube(target, size=args.size)

    cube, index = load_fits_cube(target, hdu_index=args.hdu, sanitize=not args.keep_invalid_values)
    finite = int(np.isfinite(cube).sum())
    print(f"validated FITS cube: path={target} hdu={index} shape={cube.shape} finite={finite}/{cube.size}")


if __name__ == "__main__":
    main()
