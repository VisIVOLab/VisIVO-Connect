from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def build_cube(size: int) -> np.ndarray:
    z, y, x = np.mgrid[-1:1:complex(size), -1:1:complex(size), -1:1:complex(size)]
    sphere = np.exp(-8.0 * (x * x + y * y + z * z))
    wave = 0.35 * (np.sin(10 * x) + np.cos(9 * y) + np.sin(8 * z))
    cube = sphere + wave
    cube = (cube - cube.min()) / (cube.max() - cube.min())
    return (cube * 255.0).astype(np.float32)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a sample datacube .npy for remote rendering demo")
    parser.add_argument("--size", type=int, default=192)
    parser.add_argument("--output", type=Path, default=Path("web/data/sample_datacube.npy"))
    args = parser.parse_args()

    cube = build_cube(args.size)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    np.save(args.output, cube)
    print(f"saved datacube: {args.output} shape={cube.shape}")


if __name__ == "__main__":
    main()
