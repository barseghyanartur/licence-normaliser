"""Unit tests for _registry.py.

Covers VERSION_REGISTRY derivation, ALIASES correctness, URL_MAP
normalisation, CC URL regex parsing, and the three factory functions.
"""

import pytest

from license_normaliser._enums import LicenseNameEnum, LicenseVersionEnum
from license_normaliser._registry import (
    ALIASES,
    URL_MAP,
    VERSION_REGISTRY,
    key_from_cc_url,
    make,
    make_synthetic,
    make_unknown,
)

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"


# ---------------------------------------------------------------------------
# VERSION_REGISTRY
# ---------------------------------------------------------------------------


class TestVersionRegistry:
    def test_derived_from_enum_completeness(self):
        """Every LicenseVersionEnum value must appear as a key."""
        for e in LicenseVersionEnum:
            assert e.value in VERSION_REGISTRY, f"Missing: {e.value}"

    def test_url_and_name_stored(self):
        url, name_enum = VERSION_REGISTRY["cc-by-4.0"]
        assert url == "https://creativecommons.org/licenses/by/4.0/"
        assert name_enum is LicenseNameEnum.CC_BY

    def test_unknown_has_no_url(self):
        url, _ = VERSION_REGISTRY["unknown"]
        assert url is None

    def test_mit_name_enum(self):
        _, name_enum = VERSION_REGISTRY["mit"]
        assert name_enum is LicenseNameEnum.MIT


# ---------------------------------------------------------------------------
# ALIASES
# ---------------------------------------------------------------------------


class TestAliases:
    def test_all_alias_targets_exist_in_registry(self):
        """Every alias must point to a key that exists in VERSION_REGISTRY."""
        bad = {k: v for k, v in ALIASES.items() if v not in VERSION_REGISTRY}
        assert not bad, f"Alias targets missing from registry: {bad}"

    def test_apache_2_0_alias(self):
        assert ALIASES["apache 2.0"] == "apache-2.0"

    def test_mit_license_alias(self):
        assert ALIASES["mit license"] == "mit"

    def test_cc_by_4_0_alias(self):
        assert ALIASES["cc by 4.0"] == "cc-by-4.0"

    def test_gpl_alias(self):
        assert ALIASES["gpl"] == "gpl-3.0"

    def test_full_cc_nc_nd_4_alias(self):
        key = (
            "creative commons attribution-noncommercial-noderivatives "
            "4.0 international license"
        )
        assert ALIASES[key] == "cc-by-nc-nd-4.0"

    def test_copyright_symbol_alias(self):
        # The properly-encoded © alias must resolve
        assert ALIASES["© the author(s)"] == "publisher-specific-oa"


# ---------------------------------------------------------------------------
# URL_MAP
# ---------------------------------------------------------------------------


class TestUrlMap:
    def test_all_url_map_targets_exist_in_registry(self):
        bad = {k: v for k, v in URL_MAP.items() if v not in VERSION_REGISTRY}
        assert not bad, f"URL map targets missing from registry: {bad}"

    def test_canonical_cc_by_4_https(self):
        assert URL_MAP["https://creativecommons.org/licenses/by/4.0"] == "cc-by-4.0"

    def test_http_scheme_normalised_to_https(self):
        # http:// variants must not appear as keys - they would be redundant
        http_keys = [k for k in URL_MAP if k.startswith("http://")]
        assert not http_keys, f"Raw http:// keys still in URL_MAP: {http_keys[:5]}"

    def test_trailing_slash_stripped(self):
        # No key should have a trailing slash
        trailing = [k for k in URL_MAP if k.endswith("/")]
        assert not trailing, f"Keys with trailing slash: {trailing[:5]}"

    def test_elsevier_oa(self):
        assert (
            URL_MAP["https://www.elsevier.com/open-access/userlicense/1.0"]
            == "elsevier-oa"
        )

    def test_wiley_tdm(self):
        assert URL_MAP["https://doi.wiley.com/10.1002/tdm_license_1"] == "wiley-tdm"

    def test_springer_tdm(self):
        assert URL_MAP["https://www.springer.com/tdm"] == "springer-tdm"

    def test_oup_chorus(self):
        key = (
            "https://academic.oup.com/journals/pages/open_access/funder_policies/"
            "chorus/standard_publication_model"
        )
        assert URL_MAP[key] == "oup-chorus"

    def test_cc_igo_url(self):
        assert (
            URL_MAP["https://creativecommons.org/licenses/by/3.0/igo"]
            == "cc-by-3.0-igo"
        )


# ---------------------------------------------------------------------------
# key_from_cc_url
# ---------------------------------------------------------------------------


class TestKeyFromCcUrl:
    def test_by_4_0(self):
        result = key_from_cc_url("https://creativecommons.org/licenses/by/4.0/")
        assert result is not None
        vk, nk, url = result
        assert vk == "cc-by-4.0"
        assert nk == "cc-by"
        assert url == "https://creativecommons.org/licenses/by/4.0/"

    def test_by_nc_nd_3_0(self):
        result = key_from_cc_url("https://creativecommons.org/licenses/by-nc-nd/3.0/")
        assert result is not None
        assert result[0] == "cc-by-nc-nd-3.0"
        assert result[1] == "cc-by-nc-nd"

    def test_igo_variant(self):
        result = key_from_cc_url(
            "https://creativecommons.org/licenses/by-nc-sa/3.0/igo/"
        )
        assert result is not None
        vk, nk, _ = result
        assert vk == "cc-by-nc-sa-3.0-igo"
        assert nk == "cc-by-nc-sa-igo"

    def test_cc_zero(self):
        result = key_from_cc_url("https://creativecommons.org/publicdomain/zero/1.0/")
        assert result is not None
        assert result[0] == "cc0"
        assert result[1] == "cc0"

    def test_cc_pdm(self):
        result = key_from_cc_url("https://creativecommons.org/publicdomain/mark/1.0/")
        assert result is not None
        assert result[0] == "cc-pdm"

    def test_non_cc_url_returns_none(self):
        assert key_from_cc_url("https://opensource.org/licenses/MIT") is None

    def test_garbage_returns_none(self):
        assert key_from_cc_url("not a url") is None

    def test_http_scheme_also_parsed(self):
        # The regex doesn't care about scheme - it matches on the domain
        result = key_from_cc_url("http://creativecommons.org/licenses/by/4.0/")
        assert result is not None
        assert result[0] == "cc-by-4.0"


# ---------------------------------------------------------------------------
# Factory functions
# ---------------------------------------------------------------------------


class TestMake:
    def test_make_known_key(self):
        v = make("mit")
        assert v.key == "mit"
        assert v.url == "https://opensource.org/licenses/MIT"
        assert v.license.key == "mit"
        assert v.family.key == "osi"

    def test_make_cc_by_4_0(self):
        v = make("cc-by-4.0")
        assert v.key == "cc-by-4.0"
        assert v.family.key == "cc"

    def test_make_unknown_key_raises(self):
        with pytest.raises(KeyError):
            make("this-key-does-not-exist")

    def test_make_returns_frozen(self):
        v = make("mit")
        with pytest.raises((AttributeError, TypeError)):
            v.key = "other"  # type: ignore[misc]


class TestMakeUnknown:
    def test_key_preserved(self):
        v = make_unknown("some-exotic-token")
        assert v.key == "some-exotic-token"

    def test_url_is_none(self):
        assert make_unknown("xyz").url is None

    def test_family_is_unknown(self):
        v = make_unknown("xyz")
        assert v.family.key == "unknown"

    def test_license_key_is_unknown(self):
        v = make_unknown("xyz")
        assert v.license.key == "unknown"


class TestMakeSynthetic:
    def test_synthetic_cc_url(self):
        v = make_synthetic(
            "cc-by-2.0",
            "https://creativecommons.org/licenses/by/2.0/",
            "cc-by",
        )
        assert v.key == "cc-by-2.0"
        assert v.url == "https://creativecommons.org/licenses/by/2.0/"
        assert v.license.key == "cc-by"
        assert v.family.key == "cc"

    def test_synthetic_novel_cc_name(self):
        # A CC name key not in the enum - family inferred structurally
        v = make_synthetic(
            "cc-by-nc-sa-2.0",
            "https://creativecommons.org/licenses/by-nc-sa/2.0/",
            "cc-by-nc-sa",
        )
        assert v.family.key == "cc"

    def test_synthetic_thread_safety(self):
        """make_synthetic must not mutate any global state."""
        import threading

        results = []

        def _call():
            v = make_synthetic(
                "cc-by-sa-1.0",
                "https://creativecommons.org/licenses/by-sa/1.0/",
                "cc-by-sa",
            )
            results.append(v.key)

        threads = [threading.Thread(target=_call) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(r == "cc-by-sa-1.0" for r in results)
