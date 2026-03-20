from __future__ import annotations

from pathlib import Path

import pytest

from backend.core.config import DEFAULT_ICE_SERVERS, ConfigError, _parse_ice_servers, resolve_dataset_path


def test_parse_ice_servers_fallback_on_invalid_json() -> None:
    assert _parse_ice_servers("{bad json") == DEFAULT_ICE_SERVERS


def test_parse_ice_servers_accepts_turn_stun_entries() -> None:
    raw = '[{"urls":["stun:stun.example.org:3478"]},{"urls":"turn:turn.example.org:3478","username":"u","credential":"p"}]'
    parsed = _parse_ice_servers(raw)
    assert len(parsed) == 2
    assert parsed[0]["urls"][0].startswith("stun:")
    assert parsed[1]["urls"][0].startswith("turn:")
    assert parsed[1]["username"] == "u"


def test_parse_ice_servers_allows_explicit_empty_list_when_enabled() -> None:
    assert _parse_ice_servers("[]", allow_empty=True) == []


def test_parse_ice_servers_empty_list_falls_back_by_default() -> None:
    assert _parse_ice_servers("[]") == DEFAULT_ICE_SERVERS


def test_resolve_dataset_path_rejects_paths_outside_allowed_root(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    outsider = tmp_path / "outside.fits"
    outsider.write_text("x")

    with pytest.raises(ConfigError, match="outside VISIVO_DATASET_ROOT"):
        resolve_dataset_path(str(outsider), allowed_root=str(allowed), strict_exists=True)


def test_resolve_dataset_path_keeps_fragment_and_resolves_inside_root(tmp_path: Path) -> None:
    allowed = tmp_path / "allowed"
    allowed.mkdir()
    dataset = allowed / "cube.fits"
    dataset.write_text("x")

    resolved = resolve_dataset_path(f"{dataset}#hdu=SCI", allowed_root=str(allowed), strict_exists=True)
    assert resolved is not None
    assert resolved.endswith("#hdu=SCI")
