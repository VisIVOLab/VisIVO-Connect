from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any
from urllib.parse import SplitResult, urlsplit, urlunsplit


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class AppConfig:
    app_env: str
    app_name: str
    app_version: str
    frontend_build: str
    host: str
    port: int
    log_level: str
    dataset_path: str | None
    dataset_root: str | None
    strict_dataset_path: bool
    auth_token: str | None
    metrics_auth_token: str | None
    max_sessions: int
    idle_timeout_s: int
    cleanup_interval_s: int
    allowed_origins: list[str]
    ice_servers: list[dict[str, Any]]
    client_ice_servers: list[dict[str, Any]]
    relay_only_default: bool
    ice_gather_timeout_ms: int
    ice_gather_timeout_ms_relay: int
    fits_cache_max_entries: int
    default_target_fps: int
    default_bitrate_mbps: float
    default_interactive_downsample: float
    default_hq_detail_preset: str
    ws_reconnect_base_delay_ms: int
    ws_reconnect_max_delay_ms: int

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    def public_runtime_config(self) -> dict[str, Any]:
        return {
            "appName": self.app_name,
            "backendVersion": self.app_version,
            "frontendBuild": self.frontend_build,
            "relayOnlyDefault": self.relay_only_default,
            "authEnabled": bool(self.auth_token),
            "metricsAuthEnabled": bool(self.metrics_auth_token),
            "defaults": {
                "targetFps": self.default_target_fps,
                "bitrateMbps": self.default_bitrate_mbps,
                "interactiveDownsample": self.default_interactive_downsample,
                "hqDetailPreset": self.default_hq_detail_preset,
                "wsReconnectBaseDelayMs": self.ws_reconnect_base_delay_ms,
                "wsReconnectMaxDelayMs": self.ws_reconnect_max_delay_ms,
            },
        }

    def sanitized_summary(self) -> dict[str, Any]:
        return {
            "appEnv": self.app_env,
            "appName": self.app_name,
            "appVersion": self.app_version,
            "frontendBuild": self.frontend_build,
            "host": self.host,
            "port": self.port,
            "logLevel": self.log_level,
            "datasetPathConfigured": bool(self.dataset_path),
            "datasetRoot": self.dataset_root,
            "strictDatasetPath": self.strict_dataset_path,
            "authEnabled": bool(self.auth_token),
            "metricsAuthEnabled": bool(self.metrics_auth_token),
            "maxSessions": self.max_sessions,
            "idleTimeoutS": self.idle_timeout_s,
            "cleanupIntervalS": self.cleanup_interval_s,
            "allowedOrigins": list(self.allowed_origins),
            "relayOnlyDefault": self.relay_only_default,
            "iceGatherTimeoutMs": self.ice_gather_timeout_ms,
            "iceGatherTimeoutMsRelay": self.ice_gather_timeout_ms_relay,
            "fitsCacheMaxEntries": self.fits_cache_max_entries,
            "defaultTargetFps": self.default_target_fps,
            "defaultBitrateMbps": self.default_bitrate_mbps,
            "defaultInteractiveDownsample": self.default_interactive_downsample,
            "defaultHqDetailPreset": self.default_hq_detail_preset,
            "wsReconnectBaseDelayMs": self.ws_reconnect_base_delay_ms,
            "wsReconnectMaxDelayMs": self.ws_reconnect_max_delay_ms,
            "backendIceEntries": len(self.ice_servers),
            "clientIceEntries": len(self.client_ice_servers),
        }


DEFAULT_ICE_SERVERS = [{"urls": ["stun:stun.l.google.com:19302"]}]
_VALID_LOG_LEVELS = {"CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"}
_VALID_APP_ENVS = {"development", "production", "test"}
_VALID_HQ_PRESETS = {"balanced", "sharp", "ultra"}


def _parse_bool(raw: str | None, default: bool = False) -> bool:
    if raw is None:
        return default
    normalized = str(raw).strip().lower()
    if normalized in {"1", "true", "yes", "on"}:
        return True
    if normalized in {"0", "false", "no", "off"}:
        return False
    return default



def _parse_int_env(name: str, default: int, *, minimum: int | None = None, maximum: int | None = None) -> int:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        value = default
    else:
        try:
            value = int(raw)
        except ValueError as exc:
            raise ConfigError(f"{name} must be an integer") from exc
    if minimum is not None and value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise ConfigError(f"{name} must be <= {maximum}")
    return value



def _parse_float_env(name: str, default: float, *, minimum: float | None = None, maximum: float | None = None) -> float:
    raw = os.getenv(name)
    if raw is None or not raw.strip():
        value = default
    else:
        try:
            value = float(raw)
        except ValueError as exc:
            raise ConfigError(f"{name} must be a number") from exc
    if minimum is not None and value < minimum:
        raise ConfigError(f"{name} must be >= {minimum}")
    if maximum is not None and value > maximum:
        raise ConfigError(f"{name} must be <= {maximum}")
    return value



def _parse_csv_or_json_list(raw: str | None) -> list[str]:
    if raw is None or not raw.strip():
        return []
    text = raw.strip()
    if text.startswith("["):
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError as exc:
            raise ConfigError("VISIVO_ALLOWED_ORIGINS must be valid JSON or comma-separated") from exc
        if not isinstance(parsed, list):
            raise ConfigError("VISIVO_ALLOWED_ORIGINS JSON must be a list")
        return [str(item).strip() for item in parsed if str(item).strip()]
    return [item.strip() for item in text.split(",") if item.strip()]



def _normalize_log_level(raw: str | None) -> str:
    level = (raw or "INFO").strip().upper()
    if level not in _VALID_LOG_LEVELS:
        raise ConfigError(f"VISIVO_LOG_LEVEL must be one of {sorted(_VALID_LOG_LEVELS)}")
    return level



def _normalize_app_env(raw: str | None) -> str:
    env = (raw or "development").strip().lower()
    if env not in _VALID_APP_ENVS:
        raise ConfigError(f"VISIVO_APP_ENV must be one of {sorted(_VALID_APP_ENVS)}")
    return env



def _normalize_hq_preset(raw: str | None) -> str:
    preset = (raw or "sharp").strip().lower()
    if preset not in _VALID_HQ_PRESETS:
        raise ConfigError(f"VISIVO_DEFAULT_HQ_DETAIL_PRESET must be one of {sorted(_VALID_HQ_PRESETS)}")
    return preset



def _parse_ice_servers(raw: str | None, *, allow_empty: bool = False, strict: bool = False) -> list[dict[str, Any]]:
    if raw is None or not raw.strip():
        return [] if allow_empty and strict else DEFAULT_ICE_SERVERS
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        if strict:
            raise ConfigError("ICE servers must be valid JSON") from exc
        return DEFAULT_ICE_SERVERS

    if not isinstance(parsed, list):
        if strict:
            raise ConfigError("ICE servers JSON must be a list")
        return DEFAULT_ICE_SERVERS
    if not parsed:
        return [] if allow_empty else DEFAULT_ICE_SERVERS

    servers: list[dict[str, Any]] = []
    for entry in parsed:
        if not isinstance(entry, dict):
            continue
        urls = entry.get("urls")
        if isinstance(urls, str):
            urls = [urls]
        if not isinstance(urls, list) or not urls:
            continue
        normalized_urls = [str(url).strip() for url in urls if str(url).strip()]
        if not normalized_urls:
            continue
        server = {"urls": normalized_urls}
        if isinstance(entry.get("username"), str):
            server["username"] = entry["username"]
        if isinstance(entry.get("credential"), str):
            server["credential"] = entry["credential"]
        servers.append(server)

    if servers:
        return servers
    if strict:
        raise ConfigError("ICE servers JSON did not contain any valid entries")
    return [] if allow_empty else DEFAULT_ICE_SERVERS



def _resolve_dataset_url(raw_path: str, allowed_root: str | None) -> str:
    parsed = urlsplit(raw_path)
    candidate = Path(parsed.path or raw_path).expanduser()
    resolved = candidate.resolve(strict=False)
    if allowed_root:
        root_path = Path(allowed_root).expanduser().resolve(strict=False)
        try:
            resolved.relative_to(root_path)
        except ValueError as exc:
            raise ConfigError(f"Dataset path {resolved} is outside VISIVO_DATASET_ROOT") from exc
    rebuilt = SplitResult(parsed.scheme, parsed.netloc, str(resolved), parsed.query, parsed.fragment)
    return urlunsplit(rebuilt)



def resolve_dataset_path(
    raw_path: str | None,
    *,
    default_path: str | None = None,
    allowed_root: str | None = None,
    strict_exists: bool = False,
) -> str | None:
    candidate = (raw_path or default_path or "").strip()
    if not candidate:
        return None
    resolved = _resolve_dataset_url(candidate, allowed_root)
    parsed = urlsplit(resolved)
    path = Path(parsed.path)
    if strict_exists and not path.exists():
        raise ConfigError(f"Dataset path does not exist: {path}")
    return resolved



def load_config() -> AppConfig:
    app_env = _normalize_app_env(os.getenv("VISIVO_APP_ENV"))
    strict_dataset_default = app_env == "production"
    backend_ice_servers_raw = os.getenv("VISIVO_ICE_SERVERS")
    backend_ice_servers = _parse_ice_servers(
        backend_ice_servers_raw,
        allow_empty=backend_ice_servers_raw is not None,
        strict=backend_ice_servers_raw is not None,
    )
    client_ice_servers_raw = os.getenv("VISIVO_CLIENT_ICE_SERVERS")
    client_ice_servers = (
        _parse_ice_servers(client_ice_servers_raw, allow_empty=True, strict=True)
        if client_ice_servers_raw is not None
        else backend_ice_servers
    )
    dataset_root = os.getenv("VISIVO_DATASET_ROOT")
    strict_dataset_path = _parse_bool(os.getenv("VISIVO_STRICT_DATASET_PATH"), strict_dataset_default)
    dataset_path = resolve_dataset_path(
        os.getenv("VISIVO_DATACUBE_PATH"),
        allowed_root=dataset_root,
        strict_exists=False,
    )

    allowed_origins = _parse_csv_or_json_list(os.getenv("VISIVO_ALLOWED_ORIGINS"))
    if not allowed_origins and app_env == "development":
        allowed_origins = ["*"]

    return AppConfig(
        app_env=app_env,
        app_name=os.getenv("VISIVO_APP_NAME", "VisIVO Connect").strip() or "VisIVO Connect",
        app_version=(os.getenv("VISIVO_APP_VERSION", "0.1.0").strip() or "0.1.0"),
        frontend_build=(os.getenv("VISIVO_FRONTEND_BUILD", "dev").strip() or "dev"),
        host=(os.getenv("VISIVO_HOST", "0.0.0.0").strip() or "0.0.0.0"),
        port=_parse_int_env("VISIVO_PORT", 8080, minimum=1, maximum=65535),
        log_level=_normalize_log_level(os.getenv("VISIVO_LOG_LEVEL")),
        dataset_path=dataset_path,
        dataset_root=dataset_root,
        strict_dataset_path=strict_dataset_path,
        auth_token=os.getenv("VISIVO_AUTH_TOKEN") or None,
        metrics_auth_token=os.getenv("VISIVO_METRICS_TOKEN") or None,
        max_sessions=_parse_int_env("VISIVO_MAX_SESSIONS", 16, minimum=1, maximum=1024),
        idle_timeout_s=_parse_int_env("VISIVO_IDLE_TIMEOUT_S", 900, minimum=30, maximum=86400),
        cleanup_interval_s=_parse_int_env("VISIVO_CLEANUP_INTERVAL_S", 30, minimum=5, maximum=3600),
        allowed_origins=allowed_origins,
        ice_servers=backend_ice_servers,
        client_ice_servers=client_ice_servers,
        relay_only_default=_parse_bool(os.getenv("VISIVO_FORCE_RELAY_ONLY"), False),
        ice_gather_timeout_ms=_parse_int_env("VISIVO_ICE_GATHER_TIMEOUT_MS", 300, minimum=0, maximum=20000),
        ice_gather_timeout_ms_relay=_parse_int_env("VISIVO_ICE_GATHER_TIMEOUT_MS_RELAY", 200, minimum=0, maximum=20000),
        fits_cache_max_entries=_parse_int_env("VISIVO_FITS_CACHE_MAX_ENTRIES", 2, minimum=0, maximum=128),
        default_target_fps=_parse_int_env("VISIVO_DEFAULT_TARGET_FPS", 30, minimum=5, maximum=60),
        default_bitrate_mbps=_parse_float_env("VISIVO_DEFAULT_BITRATE_MBPS", 14.0, minimum=1.0, maximum=100.0),
        default_interactive_downsample=_parse_float_env("VISIVO_DEFAULT_INTERACTIVE_DOWNSAMPLE", 1.6, minimum=1.0, maximum=4.0),
        default_hq_detail_preset=_normalize_hq_preset(os.getenv("VISIVO_DEFAULT_HQ_DETAIL_PRESET")),
        ws_reconnect_base_delay_ms=_parse_int_env("VISIVO_WS_RECONNECT_BASE_DELAY_MS", 1000, minimum=100, maximum=30000),
        ws_reconnect_max_delay_ms=_parse_int_env("VISIVO_WS_RECONNECT_MAX_DELAY_MS", 15000, minimum=500, maximum=120000),
    )
