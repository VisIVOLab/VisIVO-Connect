from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any

import pytest
from starlette.requests import Request

from backend.tests.fake_renderers import install_fake_renderer


CONFIG_ENV_KEYS = (
    "VISIVO_APP_ENV",
    "VISIVO_DATACUBE_PATH",
    "VISIVO_DATASET_ROOT",
    "VISIVO_STRICT_DATASET_PATH",
    "VISIVO_AUTH_TOKEN",
)


def _load_app_module(monkeypatch: Any, **env: str) -> Any:
    for key in CONFIG_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)
    import backend.app.main as app_main

    return importlib.reload(app_main)


def _request(path: str, query: str = "") -> Request:
    scope = {
        "type": "http",
        "method": "GET",
        "path": path,
        "query_string": query.encode("utf-8"),
        "headers": [],
    }
    return Request(scope)


def _json_payload(response: Any) -> dict[str, Any]:
    return json.loads(response.body.decode("utf-8"))


@pytest.mark.anyio
async def test_api_datasets_lists_root_and_subdirectory(monkeypatch: Any, tmp_path: Path) -> None:
    root = tmp_path / "datasets"
    root.mkdir()
    nested = root / "nested"
    nested.mkdir()
    active = root / "cube_a.fits"
    active.write_text("a")
    (nested / "cube_b.fits.gz").write_text("b")
    (root / "ignore.txt").write_text("x")
    (root / ".hidden.fits").write_text("y")

    app_main = _load_app_module(
        monkeypatch,
        VISIVO_DATASET_ROOT=str(root),
        VISIVO_DATACUBE_PATH=str(active),
        VISIVO_STRICT_DATASET_PATH="1",
    )

    root_response = await app_main.api_datasets(_request("/api/datasets"))
    assert root_response.status_code == 200
    root_payload = _json_payload(root_response)
    assert root_payload["currentPath"] == ""
    assert root_payload["parentPath"] is None
    assert root_payload["activeDatasetPath"] == "cube_a.fits"
    assert [entry["name"] for entry in root_payload["entries"]] == ["nested", "cube_a.fits"]

    nested_response = await app_main.api_datasets(_request("/api/datasets", "path=nested"))
    assert nested_response.status_code == 200
    nested_payload = _json_payload(nested_response)
    assert nested_payload["currentPath"] == "nested"
    assert nested_payload["parentPath"] == ""
    assert [entry["name"] for entry in nested_payload["entries"]] == ["cube_b.fits.gz"]


@pytest.mark.anyio
async def test_api_datasets_rejects_path_traversal(monkeypatch: Any, tmp_path: Path) -> None:
    root = tmp_path / "datasets"
    root.mkdir()

    app_main = _load_app_module(
        monkeypatch,
        VISIVO_DATASET_ROOT=str(root),
        VISIVO_STRICT_DATASET_PATH="1",
    )

    response = await app_main.api_datasets(_request("/api/datasets", "path=../secret"))
    assert response.status_code == 400
    payload = _json_payload(response)
    assert payload["code"] == "dataset-browser-unavailable"
    assert payload["phase"] == "dataset-browser"
    assert ".." in payload["message"]


@pytest.mark.anyio
async def test_api_dataset_details_returns_fits_summary_on_demand(monkeypatch: Any, tmp_path: Path) -> None:
    root = tmp_path / "datasets"
    root.mkdir()
    fits_path = root / "cube.fits"
    from astropy.io import fits
    import numpy as np

    cube = np.arange(24, dtype=np.float32).reshape((4, 3, 2))
    fits.HDUList([fits.PrimaryHDU(data=cube)]).writeto(fits_path, overwrite=True)

    app_main = _load_app_module(
        monkeypatch,
        VISIVO_DATASET_ROOT=str(root),
        VISIVO_STRICT_DATASET_PATH="1",
    )

    response = await app_main.api_dataset_details(_request("/api/datasets/details", "path=cube.fits"))
    assert response.status_code == 200
    payload = _json_payload(response)
    assert payload["name"] == "cube.fits"
    assert payload["supported"] is True
    assert payload["fits"]["hduCount"] >= 1
    assert payload["fits"]["hdus"][0]["shape"] == [4, 3, 2]


def test_resolve_requested_dataset_path_supports_relative_paths_and_default_fallback(
    monkeypatch: Any, tmp_path: Path
) -> None:
    root = tmp_path / "datasets"
    root.mkdir()
    nested = root / "nested"
    nested.mkdir()
    selected = nested / "cube_b.fits"
    selected.write_text("b")
    default_dataset = root / "cube_a.fits"
    default_dataset.write_text("a")

    app_main = _load_app_module(
        monkeypatch,
        VISIVO_DATASET_ROOT=str(root),
        VISIVO_DATACUBE_PATH=str(default_dataset),
        VISIVO_STRICT_DATASET_PATH="1",
    )

    assert app_main._resolve_requested_dataset_path("nested/cube_b.fits") == str(selected.resolve())
    assert app_main._resolve_requested_dataset_path(None) == str(default_dataset.resolve())


def test_session_switch_dataset_updates_renderer_with_selected_file(monkeypatch: Any, tmp_path: Path) -> None:
    install_fake_renderer(monkeypatch)
    dataset_a = tmp_path / "cube_a.fits"
    dataset_b = tmp_path / "cube_b.fits"
    dataset_a.write_text("a")
    dataset_b.write_text("b")

    import backend.core.session as session_mod

    session_mod = importlib.reload(session_mod)
    session = session_mod.RemoteRenderSession(dataset_path=str(dataset_a))
    try:
        session.switch_dataset(str(dataset_b))
        assert session.renderer.dataset_path == str(dataset_b)
        assert session.latest_frame() is None
        assert session.latest_pipeline_metrics == {}
        assert session.visualization.mode == "volume"
    finally:
        session.close()
