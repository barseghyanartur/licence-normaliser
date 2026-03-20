"""End-to-end data validation — every entry in every JSON data file.

This module tests the entire data surface area:

- ``aliases/aliases.json`` — every alias resolves to its expected version_key
- ``urls/url_map.json`` — every URL resolves to its expected version_key
- ``prose/prose_patterns.json`` — every pattern compiles and matches a sample string
- ``spdx/spdx-licenses.json`` (curated) — every SPDX ID resolves to a known family
- ``opendefinition/...`` (curated) — every OD ID resolves to a known family
- ``VERSION_REGISTRY`` — every entry has non-empty name_key and family_key

Unlike ``normalize_licenses.py`` (a developer tool that reports gaps), these
are strict assertions that must always pass.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from license_normaliser import normalise_license

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"


def _data_dir() -> Path:
    """Absolute path to the package-level ``data/`` directory."""
    return Path(__file__).parent.parent / "data"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _load_aliases() -> dict[str, dict[str, str]]:
    path = _data_dir() / "aliases" / "aliases.json"
    raw: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    return {
        k: v  # type: ignore[assignment]
        for k, v in raw.items()
        if isinstance(k, str) and isinstance(v, dict) and not k.startswith("_comment")
    }


def _load_urls() -> dict[str, dict[str, str]]:
    path = _data_dir() / "urls" / "url_map.json"
    raw: dict[str, object] = json.loads(path.read_text(encoding="utf-8"))
    return {
        k: v  # type: ignore[assignment]
        for k, v in raw.items()
        if isinstance(k, str) and isinstance(v, dict) and not k.startswith("_comment")
    }


def _load_prose() -> list[dict[str, str]]:
    path = _data_dir() / "prose" / "prose_patterns.json"
    raw: list[object] = json.loads(path.read_text(encoding="utf-8"))
    return [e for e in raw if isinstance(e, dict)]  # type: ignore[return-value]


def _load_spdx_curated() -> list[str]:
    path = _data_dir() / "spdx" / "spdx-licenses.json"
    data: dict = json.loads(path.read_text(encoding="utf-8"))
    return [
        e["licenseId"].lower() for e in data.get("licenses", []) if isinstance(e, dict)
    ]


def _load_od_curated() -> list[str]:
    path = _data_dir() / "opendefinition" / "opendefinition_licenses_all.json"
    data: dict = json.loads(path.read_text(encoding="utf-8"))
    return [
        entry["id"].lower()
        for entry in data.values()
        if isinstance(entry, dict) and entry.get("id")
    ]


# ---------------------------------------------------------------------------
# Aliases
# ---------------------------------------------------------------------------


class TestAliases:
    """Every entry in aliases/aliases.json resolves to its expected version_key."""

    @pytest.mark.parametrize("alias", sorted(_load_aliases().keys()), ids=str)
    def test_alias_resolves(self, alias: str):
        entry = _load_aliases()[alias]
        expected_vkey = entry["version_key"]
        expected_name_key = entry["name_key"]
        expected_family_key = entry["family_key"]

        result = normalise_license(alias)

        assert result.key == expected_vkey, (
            f"Alias {alias!r} → {result.key!r}, expected {expected_vkey!r}"
        )
        assert result.license.key == expected_name_key, (
            f"Alias {alias!r} has license.key={result.license.key!r}, "
            f"expected {expected_name_key!r}"
        )
        assert result.family.key == expected_family_key, (
            f"Alias {alias!r} has family.key={result.family.key!r}, "
            f"expected {expected_family_key!r}"
        )


# ---------------------------------------------------------------------------
# URLs
# ---------------------------------------------------------------------------


class TestUrls:
    """Every entry in urls/url_map.json resolves to its expected version_key."""

    @pytest.mark.parametrize("url", sorted(_load_urls().keys()), ids=str)
    def test_url_resolves(self, url: str):
        entry = _load_urls()[url]
        expected_vkey = entry["version_key"]
        expected_name_key = entry["name_key"]
        expected_family_key = entry["family_key"]

        result = normalise_license(url)

        assert result.key == expected_vkey, (
            f"URL {url!r} → {result.key!r}, expected {expected_vkey!r}"
        )
        assert result.license.key == expected_name_key, (
            f"URL {url!r} has license.key={result.license.key!r}, "
            f"expected {expected_name_key!r}"
        )
        assert result.family.key == expected_family_key, (
            f"URL {url!r} has family.key={result.family.key!r}, "
            f"expected {expected_family_key!r}"
        )


# ---------------------------------------------------------------------------
# Prose patterns
# ---------------------------------------------------------------------------


class TestProsePatterns:
    """Every entry in prose/prose_patterns.json compiles and matches a test string."""

    @pytest.fixture(params=_load_prose(), ids=lambda e: e.get("pattern", ""))
    def pattern_entry(self, request: pytest.FixtureRequest) -> dict[str, str]:
        return request.param

    def test_pattern_compiles(self, pattern_entry: dict[str, str]):
        pattern = pattern_entry["pattern"]
        compiled = re.compile(pattern, re.IGNORECASE)
        assert hasattr(compiled, "search")

    def test_pattern_version_key_resolves(self, pattern_entry: dict[str, str]):
        expected_vkey = pattern_entry["version_key"]
        expected_name_key = pattern_entry["name_key"]
        expected_family_key = pattern_entry["family_key"]

        result = normalise_license(expected_vkey)
        assert result.key == expected_vkey, (
            f"version_key={expected_vkey!r} normalised to {result.key!r}"
        )
        assert result.license.key == expected_name_key, (
            f"version_key={expected_vkey!r} has license.key={result.license.key!r}, "
            f"expected {expected_name_key!r}"
        )
        assert result.family.key == expected_family_key, (
            f"version_key={expected_vkey!r} has family={result.family.key!r}, "
            f"expected {expected_family_key!r}"
        )


# ---------------------------------------------------------------------------
# SPDX curated subset
# ---------------------------------------------------------------------------


class TestSpdxCurated:
    """Every SPDX ID in the curated subset resolves to a known family."""

    @pytest.mark.parametrize("spdx_id", sorted(_load_spdx_curated()), ids=str)
    def test_spdx_id_resolves(self, spdx_id: str):
        result = normalise_license(spdx_id)
        assert result.family.key != "unknown", (
            f"SPDX ID {spdx_id!r} resolved to family=unknown. "
            f"Add coverage for it in aliases/aliases.json or urls/url_map.json."
        )
        assert result.key == spdx_id, (
            f"SPDX ID {spdx_id!r} resolved to key={result.key!r}"
        )


# ---------------------------------------------------------------------------
# OpenDefinition curated subset
# ---------------------------------------------------------------------------


class TestOpenDefinitionCurated:
    """Every OpenDefinition ID in the curated subset resolves to a known family."""

    @pytest.mark.parametrize("od_id", sorted(_load_od_curated()), ids=str)
    def test_od_id_resolves(self, od_id: str):
        result = normalise_license(od_id)
        assert result.family.key != "unknown", (
            f"OD ID {od_id!r} resolved to family=unknown. "
            f"Add coverage for it in aliases/aliases.json or urls/url_map.json."
        )
        assert result.key == od_id, f"OD ID {od_id!r} resolved to key={result.key!r}"


# ---------------------------------------------------------------------------
# VERSION_REGISTRY integrity
# ---------------------------------------------------------------------------


class TestVersionRegistryIntegrity:
    """Every VERSION_REGISTRY entry has valid, non-empty metadata."""

    def test_all_entries_have_non_empty_name_key(self):
        from license_normaliser._registry import VERSION_REGISTRY

        bad = {
            k: meta["name_key"]
            for k, meta in VERSION_REGISTRY.items()
            if not meta.get("name_key")
        }
        assert not bad, f"Entries with empty name_key: {bad}"

    def test_all_entries_have_non_empty_family_key(self):
        from license_normaliser._registry import VERSION_REGISTRY

        bad = {
            k: meta["family_key"]
            for k, meta in VERSION_REGISTRY.items()
            if not meta.get("family_key")
        }
        assert not bad, f"Entries with empty family_key: {bad}"

    def test_no_family_key_is_unknown_for_builtin_entries(self):
        from license_normaliser._registry import VERSION_REGISTRY

        aliases = _load_aliases()
        builtin_vkeys = {e["version_key"] for e in aliases.values()}

        bad = {
            k: meta["family_key"]
            for k, meta in VERSION_REGISTRY.items()
            if k in builtin_vkeys and meta.get("family_key") == "unknown"
        }
        assert not bad, (
            f"Builtin entries resolved to family=unknown: {bad}. "
            f"These should have explicit family_key in the JSON data files."
        )

    def test_name_key_resolution_round_trip(self):
        from license_normaliser._registry import VERSION_REGISTRY

        for vkey, meta in VERSION_REGISTRY.items():
            name_key = meta.get("name_key", "")
            if not name_key:
                continue

            result = normalise_license(vkey)
            assert result.license.key == name_key, (
                f"Version key {vkey!r} has name_key={name_key!r} but "
                f"normalise_license({vkey!r}).license.key={result.license.key!r}"
            )
