"""Integration tests for the full normalisation pipeline via the public API.

These tests exercise ``normalise_license`` end-to-end - from raw string input
to a fully-resolved LicenseVersion - covering every license family and every
pipeline step.
"""

import pytest

from license_normaliser import (
    LicenseFamilyEnum,
    LicenseNameEnum,
    LicenseVersionEnum,
    normalise_license,
    normalise_licenses,
)

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"


# ---------------------------------------------------------------------------
# Pipeline step 1: direct registry lookup
# ---------------------------------------------------------------------------


class TestDirectLookup:
    """Inputs that are exact registry keys (already lowercase)."""

    def test_mit(self):
        v = normalise_license("mit")
        assert v.key == "mit"
        assert v.family.key == "osi"

    def test_cc_by_4_0(self):
        v = normalise_license("cc-by-4.0")
        assert v.key == "cc-by-4.0"
        assert v.family.key == "cc"

    def test_gpl_3_0(self):
        v = normalise_license("gpl-3.0")
        assert v.family.key == "copyleft"

    def test_unknown(self):
        v = normalise_license("unknown")
        assert v.key == "unknown"
        assert v.family.key == "unknown"

    def test_odbl(self):
        v = normalise_license("odbl")
        assert v.family.key == "open-data"

    def test_all_rights_reserved(self):
        v = normalise_license("all-rights-reserved")
        assert v.key == "all-rights-reserved"


# ---------------------------------------------------------------------------
# Pipeline step 2: alias table
# ---------------------------------------------------------------------------


class TestAliasLookup:
    """Inputs that resolve via the ALIASES dict."""

    def test_mit_titlecase(self):
        assert normalise_license("MIT").key == "mit"

    def test_mit_license(self):
        assert normalise_license("mit license").key == "mit"

    def test_the_mit_license(self):
        assert normalise_license("The MIT License").key == "mit"

    def test_apache_2_0_alias(self):
        assert normalise_license("Apache 2.0").key == "apache-2.0"

    def test_apache_license(self):
        assert normalise_license("Apache License").key == "apache-2.0"

    def test_gpl_short(self):
        assert normalise_license("GPL").key == "gpl-3.0"

    def test_gpl_v2(self):
        assert normalise_license("GNU GPL v2").key == "gpl-2.0"

    def test_agpl(self):
        assert normalise_license("AGPL").key == "agpl-3.0"

    def test_lgpl(self):
        assert normalise_license("LGPL").key == "lgpl-3.0"

    def test_bsd_alias(self):
        assert normalise_license("BSD").key == "bsd-3-clause"

    def test_cc_by_alias(self):
        assert normalise_license("CC BY").key == "cc-by"

    def test_cc_by_4_0_alias(self):
        assert normalise_license("CC BY 4.0").key == "cc-by-4.0"

    def test_cc_by_nc_nd_4_0_alias(self):
        assert normalise_license("CC BY-NC-ND 4.0").key == "cc-by-nc-nd-4.0"

    def test_cc0_1_0_alias(self):
        assert normalise_license("CC0 1.0").key == "cc0-1.0"

    def test_creative_commons_attribution_full(self):
        assert (
            normalise_license("Creative Commons Attribution 4.0 International").key
            == "cc-by-4.0"
        )

    def test_cc_nc_nd_international_license(self):
        v = normalise_license(
            "Creative Commons Attribution-NonCommercial-NoDerivatives "
            "4.0 International License"
        )
        assert v.key == "cc-by-nc-nd-4.0"

    def test_public_domain_alias(self):
        assert normalise_license("public domain").key == "public-domain"

    def test_all_rights_reserved_alias(self):
        assert normalise_license("all rights reserved").key == "all-rights-reserved"

    def test_wiley_tdm_shorthand(self):
        assert normalise_license("wiley tdm license").key == "wiley-tdm"

    def test_springernature_tdm_shorthand(self):
        assert normalise_license("springer nature tdm").key == "springernature-tdm"


# ---------------------------------------------------------------------------
# Pipeline step 3: URL map
# ---------------------------------------------------------------------------


class TestUrlLookup:
    """Inputs that are URLs resolving via URL_MAP."""

    def test_cc_by_https(self):
        v = normalise_license("https://creativecommons.org/licenses/by/4.0/")
        assert v.key == "cc-by-4.0"

    def test_cc_by_http(self):
        v = normalise_license("http://creativecommons.org/licenses/by/4.0/")
        assert v.key == "cc-by-4.0"

    def test_cc_by_no_trailing_slash(self):
        v = normalise_license("https://creativecommons.org/licenses/by/4.0")
        assert v.key == "cc-by-4.0"

    def test_cc_by_nc_nd_3_0_url(self):
        v = normalise_license("http://creativecommons.org/licenses/by-nc-nd/3.0/")
        assert v.key == "cc-by-nc-nd-3.0"

    def test_cc_igo_url(self):
        v = normalise_license("https://creativecommons.org/licenses/by/3.0/igo/")
        assert v.key == "cc-by-3.0-igo"

    def test_cc0_url(self):
        v = normalise_license("https://creativecommons.org/publicdomain/zero/1.0/")
        assert v.key == "cc0"

    def test_elsevier_oa_url(self):
        v = normalise_license("http://www.elsevier.com/open-access/userlicense/1.0/")
        assert v.key == "elsevier-oa"
        assert v.family.key == "publisher-oa"

    def test_elsevier_tdm_url(self):
        v = normalise_license("https://www.elsevier.com/tdm/userlicense/1.0/")
        assert v.key == "elsevier-tdm"
        assert v.family.key == "publisher-tdm"

    def test_wiley_tdm_1_1_url(self):
        v = normalise_license("http://doi.wiley.com/10.1002/tdm_license_1.1")
        assert v.key == "wiley-tdm-1.1"

    def test_springer_tdm_url(self):
        v = normalise_license("http://www.springer.com/tdm")
        assert v.key == "springer-tdm"

    def test_tandf_terms_url(self):
        v = normalise_license("https://www.tandfonline.com/action/showCopyRight")
        assert v.key == "tandf-terms"

    def test_acs_authorchoice_ccby_url(self):
        v = normalise_license(
            "https://pubs.acs.org/page/policy/authorchoice_ccby_termsofuse.html"
        )
        assert v.key == "acs-authorchoice-ccby"

    def test_aps_default_url(self):
        v = normalise_license("https://link.aps.org/licenses/aps-default-license")
        assert v.key == "aps-default"

    def test_bmj_copyright_url(self):
        v = normalise_license(
            "https://www.bmj.com/company/legal-stuff/copyright-notice/"
        )
        assert v.key == "bmj-copyright"

    def test_jama_cc_by_url(self):
        v = normalise_license("https://jamanetwork.com/pages/cc-by-license-permissions")
        assert v.key == "jama-cc-by"

    def test_iop_tdm_url(self):
        v = normalise_license(
            "https://iopscience.iop.org/info/page/text-and-data-mining"
        )
        assert v.key == "iop-tdm"

    def test_gnu_gpl_2_url(self):
        v = normalise_license("http://www.gnu.org/licenses/gpl-2.0.html")
        assert v.key == "gpl-2.0"

    def test_gnu_gpl_3_url(self):
        v = normalise_license("https://www.gnu.org/licenses/gpl-3.0.html")
        assert v.key == "gpl-3.0"


# ---------------------------------------------------------------------------
# Pipeline step 4: structural CC URL regex
# ---------------------------------------------------------------------------


class TestCcUrlRegex:
    """Inputs that are CC URLs not in the explicit URL_MAP but parseable."""

    def test_cc_by_nc_sa_2_5(self):
        v = normalise_license("https://creativecommons.org/licenses/by-nc-sa/2.5/")
        assert v.key == "cc-by-nc-sa-2.5"
        assert v.family.key == "cc"

    def test_cc_by_sa_2_0(self):
        v = normalise_license("https://creativecommons.org/licenses/by-sa/2.0/")
        assert v.key == "cc-by-sa-2.0"

    def test_synthetic_family_is_cc(self):
        v = normalise_license("https://creativecommons.org/licenses/by-nc/2.0/")
        assert v.family.key == "cc"

    def test_cc_by_nc_nd_igo_3_0(self):
        v = normalise_license("https://creativecommons.org/licenses/by-nc-nd/3.0/igo/")
        assert v.key == "cc-by-nc-nd-3.0-igo"


# ---------------------------------------------------------------------------
# Pipeline step 5: prose keyword scan
# ---------------------------------------------------------------------------


class TestProseScan:
    """Long inputs that do NOT match any earlier step but contain keywords."""

    def test_cc_by_nc_nd_in_prose(self):
        # This alias now covers the 4.0 international license variant,
        # so we use a prose sentence that bypasses the alias table
        v = normalise_license(
            "Distributed under attribution noncommercial noderivatives terms."
        )
        assert v.key == "cc-by-nc-nd"

    def test_attribution_only_prose(self):
        v = normalise_license(
            "Reuse is permitted provided proper attribution is given."
        )
        assert v.key == "cc-by"

    def test_all_rights_reserved_prose(self):
        v = normalise_license(
            "Copyright 2024 ACME Corp. All rights reserved worldwide."
        )
        assert v.key == "all-rights-reserved"

    def test_elsevier_tdm_prose(self):
        v = normalise_license(
            "This content is licensed under the Elsevier TDM agreement."
        )
        assert v.key == "elsevier-tdm"

    def test_public_domain_prose(self):
        v = normalise_license(
            "This dataset has been released into the public domain by its author."
        )
        assert v.key == "public-domain"

    def test_url_in_prose_wins_over_prose_scan(self):
        # Step 3 should catch the URL before step 5 fires
        v = normalise_license(
            "This is an open access article under the CC BY license "
            "(http://creativecommons.org/licenses/by/4.0/)"
        )
        assert v.key == "cc-by-4.0"


# ---------------------------------------------------------------------------
# Pipeline step 6: fallback
# ---------------------------------------------------------------------------


class TestFallback:
    def test_unknown_string(self):
        v = normalise_license("some-totally-unknown-license-xyz")
        assert v.key == "some-totally-unknown-license-xyz"
        assert v.family.key == "unknown"
        assert v.url is None

    def test_empty_string(self):
        v = normalise_license("")
        assert v.key == "unknown"

    def test_whitespace_only(self):
        v = normalise_license("   ")
        assert v.key == "unknown"


# ---------------------------------------------------------------------------
# Creative Commons family - comprehensive
# ---------------------------------------------------------------------------


class TestCreativeCommons:
    @pytest.mark.parametrize(
        "raw,expected_key",
        [
            ("cc-by", "cc-by"),
            ("CC BY 4.0", "cc-by-4.0"),
            ("CC BY 3.0", "cc-by-3.0"),
            ("CC BY 2.5", "cc-by-2.5"),
            ("CC BY 2.0", "cc-by-2.0"),
            ("cc-by-sa-4.0", "cc-by-sa-4.0"),
            ("cc-by-sa-3.0", "cc-by-sa-3.0"),
            ("CC BY-ND 4.0", "cc-by-nd-4.0"),
            ("cc-by-nc", "cc-by-nc"),
            ("CC BY-NC 4.0", "cc-by-nc-4.0"),
            ("cc-by-nc-sa", "cc-by-nc-sa"),
            ("CC BY-NC-SA 4.0", "cc-by-nc-sa-4.0"),
            ("cc-by-nc-nd", "cc-by-nc-nd"),
            ("CC BY-NC-ND 4.0", "cc-by-nc-nd-4.0"),
            ("CC BY-NC-ND 3.0 IGO", "cc-by-nc-nd-3.0-igo"),
            ("cc0", "cc0"),
            ("CC0 1.0", "cc0-1.0"),
            ("cc-pdm", "cc-pdm"),
        ],
    )
    def test_cc_variant(self, raw, expected_key):
        assert normalise_license(raw).key == expected_key

    def test_all_cc_results_have_cc_or_cc0_family(self):
        cc_variants = [
            "cc-by-4.0",
            "cc-by-sa-4.0",
            "cc-by-nd-4.0",
            "cc-by-nc-4.0",
            "cc-by-nc-sa-4.0",
            "cc-by-nc-nd-4.0",
        ]
        for raw in cc_variants:
            v = normalise_license(raw)
            assert v.family.key == "cc", f"Expected cc family for {raw}"

    def test_cc0_family_is_cc0_not_cc(self):
        v = normalise_license("cc0")
        assert v.family.key == "cc0"

    def test_cc_pdm_family_is_public_domain(self):
        v = normalise_license("cc-pdm")
        assert v.family.key == "public-domain"


# ---------------------------------------------------------------------------
# OSI permissive
# ---------------------------------------------------------------------------


class TestOSI:
    @pytest.mark.parametrize(
        "raw,expected_key",
        [
            ("MIT", "mit"),
            ("Apache-2.0", "apache-2.0"),
            ("BSD-2-Clause", "bsd-2-clause"),
            ("BSD-3-Clause", "bsd-3-clause"),
            ("ISC", "isc"),
            ("MPL-2.0", "mpl-2.0"),
        ],
    )
    def test_osi_key(self, raw, expected_key):
        v = normalise_license(raw)
        assert v.key == expected_key
        assert v.family.key == "osi"

    def test_mit_has_url(self):
        assert normalise_license("MIT").url == "https://opensource.org/licenses/MIT"


# ---------------------------------------------------------------------------
# Copyleft
# ---------------------------------------------------------------------------


class TestCopyleft:
    @pytest.mark.parametrize(
        "raw,expected_key",
        [
            ("GPL-2.0", "gpl-2.0"),
            ("GPL-2.0-only", "gpl-2.0-only"),
            ("GPL-3.0", "gpl-3.0"),
            ("GPL-3.0-only", "gpl-3.0-only"),
            ("AGPL-3.0", "agpl-3.0"),
            ("LGPL-2.1", "lgpl-2.1"),
            ("LGPL-3.0", "lgpl-3.0"),
        ],
    )
    def test_copyleft_key(self, raw, expected_key):
        v = normalise_license(raw)
        assert v.key == expected_key
        assert v.family.key == "copyleft"


# ---------------------------------------------------------------------------
# Publisher licenses
# ---------------------------------------------------------------------------


class TestPublisherLicenses:
    def test_elsevier_oa_family(self):
        v = normalise_license("elsevier-oa")
        assert v.family.key == "publisher-oa"

    def test_elsevier_tdm_family(self):
        v = normalise_license("elsevier-tdm")
        assert v.family.key == "publisher-tdm"

    def test_wiley_vor_family(self):
        v = normalise_license("wiley-vor")
        assert v.family.key == "publisher-proprietary"

    def test_springer_tdm_family(self):
        v = normalise_license("springer-tdm")
        assert v.family.key == "publisher-tdm"

    def test_acs_authorchoice_family(self):
        v = normalise_license("acs-authorchoice")
        assert v.family.key == "publisher-oa"

    def test_aaas_author_reuse(self):
        v = normalise_license("aaas-author-reuse")
        assert v.family.key == "publisher-proprietary"

    def test_thieme_nlm(self):
        v = normalise_license("thieme-nlm")
        assert v.family.key == "publisher-oa"


# ---------------------------------------------------------------------------
# Open data
# ---------------------------------------------------------------------------


class TestOpenData:
    def test_odbl(self):
        v = normalise_license("odbl")
        assert v.family.key == "open-data"

    def test_pddl(self):
        v = normalise_license("pddl")
        assert v.family.key == "open-data"

    def test_odc_by(self):
        v = normalise_license("odc-by")
        assert v.family.key == "open-data"


# ---------------------------------------------------------------------------
# Catch-all / edge cases
# ---------------------------------------------------------------------------


class TestCatchAll:
    def test_author_manuscript(self):
        v = normalise_license("author-manuscript")
        assert v.family.key == "publisher-oa"

    def test_no_reuse(self):
        v = normalise_license("no-reuse")
        assert v.family.key == "publisher-proprietary"

    def test_unspecified_oa(self):
        v = normalise_license("unspecified-oa")
        assert v.family.key == "other-oa"

    def test_implied_oa(self):
        v = normalise_license("implied-oa")
        assert v.family.key == "publisher-oa"


# ---------------------------------------------------------------------------
# Hierarchy navigation
# ---------------------------------------------------------------------------


class TestHierarchyNavigation:
    def test_version_license_family_chain(self):
        v = normalise_license("CC BY-NC-ND 4.0")
        assert v.key == "cc-by-nc-nd-4.0"
        assert v.license.key == "cc-by-nc-nd"
        assert v.license.family.key == "cc"
        assert v.family.key == "cc"  # shortcut

    def test_str_representations(self):
        v = normalise_license("CC BY-NC-ND 4.0")
        assert str(v) == "cc-by-nc-nd-4.0"
        assert str(v.license) == "cc-by-nc-nd"
        assert str(v.family) == "cc"

    def test_enum_checking_methods(self):
        v = normalise_license("MIT")
        assert v.is_family(LicenseFamilyEnum.OSI)
        assert not v.is_family(LicenseFamilyEnum.CC)
        assert v.is_name(LicenseNameEnum.MIT)
        assert not v.is_name(LicenseNameEnum.CC_BY)
        assert v.is_version(LicenseVersionEnum.MIT)
        assert not v.is_version(LicenseVersionEnum.GPL_3_0)

    def test_version_enum_property(self):
        v = normalise_license("MIT")
        assert v.enum is LicenseVersionEnum.MIT

    def test_name_enum_property(self):
        v = normalise_license("MIT")
        assert v.license.enum is LicenseNameEnum.MIT

    def test_family_enum_property(self):
        v = normalise_license("MIT")
        assert v.family.enum is LicenseFamilyEnum.OSI


# ---------------------------------------------------------------------------
# Batch normalisation
# ---------------------------------------------------------------------------


class TestBatchNormalisation:
    def test_basic_batch(self, batch_raw):
        results = normalise_licenses(batch_raw)
        assert [r.key for r in results] == ["mit", "apache-2.0", "cc-by-4.0"]

    def test_batch_preserves_order(self):
        raw = ["GPL-3.0", "MIT", "CC BY 4.0", "Apache-2.0"]
        expected = ["gpl-3.0", "mit", "cc-by-4.0", "apache-2.0"]
        assert [r.key for r in normalise_licenses(raw)] == expected

    def test_batch_accepts_generator(self):
        results = normalise_licenses(x for x in ["MIT", "ISC"])
        assert results[0].key == "mit"

    def test_batch_empty(self):
        assert normalise_licenses([]) == []


# ---------------------------------------------------------------------------
# Enum classes - direct access
# ---------------------------------------------------------------------------


class TestEnums:
    def test_family_enum_values(self):
        assert LicenseFamilyEnum.CC.value == "cc"
        assert LicenseFamilyEnum.OSI.value == "osi"
        assert LicenseFamilyEnum.COPYLEFT.value == "copyleft"
        assert LicenseFamilyEnum.UNKNOWN.value == "unknown"

    def test_name_enum_family_property(self):
        assert LicenseNameEnum.CC_BY.family is LicenseFamilyEnum.CC
        assert LicenseNameEnum.MIT.family is LicenseFamilyEnum.OSI
        assert LicenseNameEnum.GPL_3.family is LicenseFamilyEnum.COPYLEFT

    def test_version_enum_name_property(self):
        assert LicenseVersionEnum.CC_BY_4_0.name_enum is LicenseNameEnum.CC_BY
        assert LicenseVersionEnum.MIT.name_enum is LicenseNameEnum.MIT

    def test_version_enum_family_property(self):
        assert LicenseVersionEnum.CC_BY_4_0.family is LicenseFamilyEnum.CC
        assert LicenseVersionEnum.MIT.family is LicenseFamilyEnum.OSI

    def test_reverse_lookup_by_value(self):
        assert LicenseVersionEnum("cc-by-4.0") is LicenseVersionEnum.CC_BY_4_0
        assert LicenseNameEnum("mit") is LicenseNameEnum.MIT
        assert LicenseFamilyEnum("osi") is LicenseFamilyEnum.OSI
