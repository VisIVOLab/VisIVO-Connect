from __future__ import annotations

from backend.core.config import DEFAULT_ICE_SERVERS, _parse_ice_servers


def test_parse_ice_servers_fallback_on_invalid_json() -> None:
    assert _parse_ice_servers("{bad json") == DEFAULT_ICE_SERVERS


def test_parse_ice_servers_accepts_turn_stun_entries() -> None:
    raw = '[{"urls":["stun:stun.example.org:3478"]},{"urls":"turn:turn.example.org:3478","username":"u","credential":"p"}]'
    parsed = _parse_ice_servers(raw)
    assert len(parsed) == 2
    assert parsed[0]["urls"][0].startswith("stun:")
    assert parsed[1]["urls"][0].startswith("turn:")
    assert parsed[1]["username"] == "u"
