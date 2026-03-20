from __future__ import annotations

import importlib
import json
from typing import Any

import pytest


CONFIG_ENV_KEYS = (
    "VISIVO_APP_ENV",
    "VISIVO_APP_NAME",
    "VISIVO_APP_VERSION",
    "VISIVO_FRONTEND_BUILD",
    "VISIVO_HOST",
    "VISIVO_PORT",
    "VISIVO_LOG_LEVEL",
    "VISIVO_DATACUBE_PATH",
    "VISIVO_DATASET_ROOT",
    "VISIVO_STRICT_DATASET_PATH",
    "VISIVO_FITS_CACHE_MAX_ENTRIES",
    "VISIVO_AUTH_TOKEN",
    "VISIVO_METRICS_TOKEN",
    "VISIVO_MAX_SESSIONS",
    "VISIVO_IDLE_TIMEOUT_S",
    "VISIVO_CLEANUP_INTERVAL_S",
    "VISIVO_ALLOWED_ORIGINS",
    "VISIVO_ICE_SERVERS",
    "VISIVO_CLIENT_ICE_SERVERS",
    "VISIVO_FORCE_RELAY_ONLY",
    "VISIVO_ICE_GATHER_TIMEOUT_MS",
    "VISIVO_ICE_GATHER_TIMEOUT_MS_RELAY",
    "VISIVO_DEFAULT_TARGET_FPS",
    "VISIVO_DEFAULT_BITRATE_MBPS",
    "VISIVO_DEFAULT_INTERACTIVE_DOWNSAMPLE",
    "VISIVO_DEFAULT_HQ_DETAIL_PRESET",
    "VISIVO_WS_RECONNECT_BASE_DELAY_MS",
    "VISIVO_WS_RECONNECT_MAX_DELAY_MS",
)


def _load_app_module(monkeypatch: Any, **env: str) -> Any:
    for key in CONFIG_ENV_KEYS:
        monkeypatch.delenv(key, raising=False)
    for key, value in env.items():
        monkeypatch.setenv(key, value)

    import backend.app.main as app_main

    return importlib.reload(app_main)


def _json_payload(response: Any) -> dict[str, Any]:
    return json.loads(response.body.decode("utf-8"))


@pytest.mark.anyio
async def test_healthz_returns_basic_service_status(monkeypatch: Any) -> None:
    app_main = _load_app_module(monkeypatch)

    response = await app_main.healthz()
    assert response.status_code == 200
    payload = _json_payload(response)
    assert payload["status"] == "ok"
    assert payload["service"] == "VisIVO Connect"
    assert payload["backendVersion"] == "0.1.0"
    assert "frontendBuild" in payload
    assert isinstance(payload["uptimeS"], (int, float))
    assert payload["uptimeS"] >= 0


@pytest.mark.anyio
async def test_readyz_reports_readiness_summary(monkeypatch: Any) -> None:
    app_main = _load_app_module(
        monkeypatch,
        VISIVO_APP_ENV="production",
        VISIVO_FRONTEND_BUILD="build-20260320",
        VISIVO_ALLOWED_ORIGINS='["https://viewer.example.org"]',
        VISIVO_STRICT_DATASET_PATH="0",
    )

    response = await app_main.readyz()
    assert response.status_code == 200
    payload = _json_payload(response)
    assert payload["status"] == "ready"
    assert payload["backendVersion"] == "0.1.0"
    assert payload["frontendBuild"] == "build-20260320"
    assert payload["webDirPresent"] is True
    assert "config" in payload
    assert "activeSessions" in payload
    assert payload["activeSessions"] == 0
    assert payload["maxSessions"] == 16
    assert isinstance(payload["warnings"], list)
    assert isinstance(payload["errors"], list)


@pytest.mark.anyio
async def test_api_version_exposes_build_and_sanitized_config(monkeypatch: Any) -> None:
    app_main = _load_app_module(
        monkeypatch,
        VISIVO_APP_NAME="VisIVO Connect Prod",
        VISIVO_APP_VERSION="1.2.3",
        VISIVO_FRONTEND_BUILD="frontend-abcd",
        VISIVO_AUTH_TOKEN="top-secret-auth",
        VISIVO_METRICS_TOKEN="top-secret-metrics",
    )

    response = await app_main.api_version()
    assert response.status_code == 200
    payload = _json_payload(response)
    assert payload["service"] == "VisIVO Connect Prod"
    assert payload["backendVersion"] == "1.2.3"
    assert payload["frontendBuild"] == "frontend-abcd"
    assert isinstance(payload["uptimeS"], (int, float))
    assert payload["config"]["authEnabled"] is True
    assert payload["config"]["metricsAuthEnabled"] is True
    serialized = json.dumps(payload)
    assert "top-secret-auth" not in serialized
    assert "top-secret-metrics" not in serialized


@pytest.mark.anyio
async def test_runtime_config_returns_safe_runtime_defaults_without_secrets(monkeypatch: Any) -> None:
    app_main = _load_app_module(
        monkeypatch,
        VISIVO_AUTH_TOKEN="very-secret-auth",
        VISIVO_METRICS_TOKEN="very-secret-metrics",
        VISIVO_FORCE_RELAY_ONLY="1",
        VISIVO_DEFAULT_TARGET_FPS="24",
        VISIVO_DEFAULT_BITRATE_MBPS="18",
        VISIVO_DEFAULT_INTERACTIVE_DOWNSAMPLE="1.9",
        VISIVO_DEFAULT_HQ_DETAIL_PRESET="ultra",
        VISIVO_WS_RECONNECT_BASE_DELAY_MS="1500",
        VISIVO_WS_RECONNECT_MAX_DELAY_MS="20000",
    )

    response = await app_main.api_runtime_config()
    assert response.status_code == 200
    payload = _json_payload(response)
    assert payload["relayOnlyDefault"] is True
    assert payload["authEnabled"] is True
    assert payload["metricsAuthEnabled"] is True
    assert payload["defaults"]["targetFps"] == 24
    assert payload["defaults"]["bitrateMbps"] == 18.0
    assert payload["defaults"]["interactiveDownsample"] == 1.9
    assert payload["defaults"]["hqDetailPreset"] == "ultra"
    assert payload["defaults"]["wsReconnectBaseDelayMs"] == 1500
    assert payload["defaults"]["wsReconnectMaxDelayMs"] == 20000

    serialized = json.dumps(payload)
    assert "very-secret-auth" not in serialized
    assert "very-secret-metrics" not in serialized
    assert "credential" not in payload
    assert "token" not in payload
