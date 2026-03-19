from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AppConfig:
    dataset_path: str | None
    auth_token: str | None
    metrics_auth_token: str | None
    max_sessions: int
    idle_timeout_s: int
    ice_servers: list[dict[str, Any]]
    client_ice_servers: list[dict[str, Any]]


DEFAULT_ICE_SERVERS = [{"urls": ["stun:stun.l.google.com:19302"]}]


def _parse_ice_servers(raw: str | None) -> list[dict[str, Any]]:
    if not raw:
        return DEFAULT_ICE_SERVERS
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return DEFAULT_ICE_SERVERS

    if not isinstance(parsed, list):
        return DEFAULT_ICE_SERVERS

    servers: list[dict[str, Any]] = []
    for entry in parsed:
        if not isinstance(entry, dict):
            continue
        urls = entry.get("urls")
        if isinstance(urls, str):
            urls = [urls]
        if not isinstance(urls, list) or not urls:
            continue
        server = {"urls": urls}
        if isinstance(entry.get("username"), str):
            server["username"] = entry["username"]
        if isinstance(entry.get("credential"), str):
            server["credential"] = entry["credential"]
        servers.append(server)

    return servers or DEFAULT_ICE_SERVERS


def load_config() -> AppConfig:
    backend_ice_servers = _parse_ice_servers(os.getenv("VISIVO_ICE_SERVERS"))
    client_ice_servers_raw = os.getenv("VISIVO_CLIENT_ICE_SERVERS")
    client_ice_servers = (
        _parse_ice_servers(client_ice_servers_raw) if client_ice_servers_raw is not None else backend_ice_servers
    )
    return AppConfig(
        dataset_path=os.getenv("VISIVO_DATACUBE_PATH"),
        auth_token=os.getenv("VISIVO_AUTH_TOKEN"),
        metrics_auth_token=os.getenv("VISIVO_METRICS_TOKEN"),
        max_sessions=int(os.getenv("VISIVO_MAX_SESSIONS", "16")),
        idle_timeout_s=int(os.getenv("VISIVO_IDLE_TIMEOUT_S", "900")),
        ice_servers=backend_ice_servers,
        client_ice_servers=client_ice_servers,
    )
