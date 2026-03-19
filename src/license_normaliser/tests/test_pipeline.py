"""Unit tests for _pipeline.py.

Each resolution step is tested in complete isolation.  Tests verify both
positive (match found) and negative (returns None) cases for every step.
"""

from license_normaliser._pipeline import (
    _PROSE_MIN_LEN,
    step_alias,
    step_cc_regex,
    step_direct,
    step_fallback,
    step_prose,
    step_url,
)

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"


# ---------------------------------------------------------------------------
# Step 1: step_direct
# ---------------------------------------------------------------------------


class TestStepDirect:
    def test_exact_match(self):
        assert step_direct("mit") == "mit"

    def test_cc_by_4_0(self):
        assert step_direct("cc-by-4.0") == "cc-by-4.0"

    def test_no_match_returns_none(self):
        assert step_direct("not-a-known-key") is None

    def test_uppercase_no_match(self):
        # Step 1 does not clean - caller must pass cleaned (lowercase) string
        assert step_direct("MIT") is None

    def test_unknown_key(self):
        assert step_direct("unknown") == "unknown"


# ---------------------------------------------------------------------------
# Step 2: step_alias
# ---------------------------------------------------------------------------


class TestStepAlias:
    def test_mit_license(self):
        assert step_alias("mit license") == "mit"

    def test_apache_2_0(self):
        assert step_alias("apache 2.0") == "apache-2.0"

    def test_cc_by_4_0(self):
        assert step_alias("cc by 4.0") == "cc-by-4.0"

    def test_gpl_shorthand(self):
        assert step_alias("gpl") == "gpl-3.0"

    def test_public_domain(self):
        assert step_alias("public domain") == "public-domain"

    def test_all_rights_reserved(self):
        assert step_alias("all rights reserved") == "all-rights-reserved"

    def test_no_match_returns_none(self):
        assert step_alias("definitely not an alias") is None

    def test_cc_nc_nd_international_license(self):
        key = (
            "creative commons attribution-noncommercial-noderivatives "
            "4.0 international license"
        )
        assert step_alias(key) == "cc-by-nc-nd-4.0"


# ---------------------------------------------------------------------------
# Step 3: step_url
# ---------------------------------------------------------------------------


class TestStepUrl:
    def test_canonical_https_cc(self):
        assert step_url("https://creativecommons.org/licenses/by/4.0") == "cc-by-4.0"

    def test_http_normalised_to_https(self):
        # http:// input is scheme-normalised before lookup
        assert step_url("http://creativecommons.org/licenses/by/4.0") == "cc-by-4.0"

    def test_trailing_slash_stripped(self):
        assert step_url("https://creativecommons.org/licenses/by/4.0/") == "cc-by-4.0"

    def test_http_trailing_slash(self):
        assert step_url("http://creativecommons.org/licenses/by/4.0/") == "cc-by-4.0"

    def test_elsevier_oa(self):
        assert (
            step_url("http://www.elsevier.com/open-access/userlicense/1.0/")
            == "elsevier-oa"
        )

    def test_wiley_tdm_1_1(self):
        assert (
            step_url("http://doi.wiley.com/10.1002/tdm_license_1.1") == "wiley-tdm-1.1"
        )

    def test_cc_igo(self):
        assert (
            step_url("https://creativecommons.org/licenses/by/3.0/igo")
            == "cc-by-3.0-igo"
        )

    def test_no_match_returns_none(self):
        assert step_url("https://example.com/some-unknown-license") is None

    def test_non_url_returns_none(self):
        assert step_url("mit") is None


# ---------------------------------------------------------------------------
# Step 4: step_cc_regex
# ---------------------------------------------------------------------------


class TestStepCcRegex:
    def test_known_cc_url_returns_version(self):
        v = step_cc_regex("https://creativecommons.org/licenses/by/4.0/")
        assert v is not None
        assert v.key == "cc-by-4.0"

    def test_synthetic_old_version(self):
        # cc-by-1.0 is in VERSION_REGISTRY via URL_MAP extras but also
        # parseable by regex - either path gives the same result
        v = step_cc_regex("https://creativecommons.org/licenses/by/1.0/")
        assert v is not None
        assert v.key == "cc-by-1.0"

    def test_igo_variant(self):
        v = step_cc_regex("https://creativecommons.org/licenses/by-nc-sa/3.0/igo/")
        assert v is not None
        assert v.key == "cc-by-nc-sa-3.0-igo"

    def test_cc_zero(self):
        v = step_cc_regex("https://creativecommons.org/publicdomain/zero/1.0/")
        assert v is not None
        assert v.key == "cc0"

    def test_cc_pdm(self):
        v = step_cc_regex("https://creativecommons.org/publicdomain/mark/1.0/")
        assert v is not None
        assert v.key == "cc-pdm"

    def test_non_cc_url_returns_none(self):
        assert step_cc_regex("https://opensource.org/licenses/MIT") is None

    def test_plain_text_returns_none(self):
        assert step_cc_regex("mit") is None

    def test_family_is_cc(self):
        v = step_cc_regex("https://creativecommons.org/licenses/by-nc-nd/4.0/")
        assert v is not None
        assert v.family.key == "cc"

    def test_http_input_also_parsed(self):
        v = step_cc_regex("http://creativecommons.org/licenses/by-sa/3.0/")
        assert v is not None
        assert v.key == "cc-by-sa-3.0"


# ---------------------------------------------------------------------------
# Step 5: step_prose
# ---------------------------------------------------------------------------


class TestStepProse:
    def test_short_input_returns_none(self):
        short = "cc by"  # shorter than _PROSE_MIN_LEN
        assert len(short) < _PROSE_MIN_LEN
        assert step_prose(short) is None

    def test_cc_by_4_0_in_sentence(self):
        s = "This article is licensed under a CC BY 4.0 International License."
        assert step_prose(s) == "cc-by-4.0"

    def test_cc_by_nc_nd_in_sentence(self):
        s = "Published under the CC BY-NC-ND 4.0 terms and conditions."
        assert step_prose(s) == "cc-by-nc-nd-4.0"

    def test_attribution_noncommercial_prose(self):
        s = (
            "This work is licensed under a Creative Commons "
            "Attribution NonCommercial NoDerivatives license."
        )
        assert step_prose(s) == "cc-by-nc-nd"

    def test_attribution_only_prose(self):
        s = "Reuse permitted provided proper attribution is given to the authors."
        assert step_prose(s) == "cc-by"

    def test_all_rights_reserved_prose(self):
        s = "Copyright 2024 ACME Corp. All rights reserved worldwide."
        assert step_prose(s) == "all-rights-reserved"

    def test_public_domain_prose(self):
        s = "This dataset has been released into the public domain."
        assert step_prose(s) == "public-domain"

    def test_elsevier_tdm_prose(self):
        s = "This content is covered by the Elsevier TDM user agreement."
        assert step_prose(s) == "elsevier-tdm"

    def test_no_match_returns_none(self):
        s = "This license string contains absolutely no recognisable patterns here."
        assert step_prose(s) is None
        # "open access" pattern would fire - use something genuinely opaque
        assert step_prose("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") is None

    def test_minimum_length_boundary(self):
        # Exactly at boundary: should attempt scan
        at_boundary = "a" * _PROSE_MIN_LEN
        # No pattern matches garbage - returns None
        assert step_prose(at_boundary) is None

    def test_one_below_boundary_returns_none(self):
        below = "a" * (_PROSE_MIN_LEN - 1)
        assert step_prose(below) is None


# ---------------------------------------------------------------------------
# Step 6: step_fallback
# ---------------------------------------------------------------------------


class TestStepFallback:
    def test_always_returns_version(self):
        v = step_fallback("some-weird-token")
        assert v.key == "some-weird-token"

    def test_family_is_unknown(self):
        v = step_fallback("no-such-license")
        assert v.family.key == "unknown"

    def test_url_is_none(self):
        assert step_fallback("xyz").url is None

    def test_empty_string(self):
        v = step_fallback("")
        assert v.key == ""
        assert v.family.key == "unknown"
