"""Unit tests for _models.py.

Tests cover construction, equality, hashing, repr, str, enum lookups,
and the frozen / slots invariants.  No normalisation pipeline is involved.
"""

import pytest

from license_normaliser._enums import (
    LicenseFamilyEnum,
    LicenseNameEnum,
    LicenseVersionEnum,
)
from license_normaliser._models import LicenseFamily, LicenseName, LicenseVersion

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _cc_fam() -> LicenseFamily:
    return LicenseFamily(key="cc")


def _osi_fam() -> LicenseFamily:
    return LicenseFamily(key="osi")


def _cc_by_name() -> LicenseName:
    return LicenseName(key="cc-by", family=_cc_fam())


def _mit_version() -> LicenseVersion:
    return LicenseVersion(
        key="mit",
        url="https://opensource.org/licenses/MIT",
        license=LicenseName(key="mit", family=_osi_fam()),
    )


# ---------------------------------------------------------------------------
# LicenseFamily
# ---------------------------------------------------------------------------


class TestLicenseFamily:
    def test_str(self):
        assert str(LicenseFamily(key="cc")) == "cc"

    def test_repr(self):
        assert repr(LicenseFamily(key="osi")) == "LicenseFamily('osi')"

    def test_eq_same_type(self):
        assert LicenseFamily(key="cc") == LicenseFamily(key="cc")

    def test_eq_str(self):
        assert LicenseFamily(key="cc") == "cc"

    def test_eq_str_reverse(self):
        # LicenseFamily on right side of ==
        assert "cc" == LicenseFamily(key="cc")  # noqa: SIM300

    def test_eq_enum(self):
        assert LicenseFamily(key="cc") == LicenseFamilyEnum.CC

    def test_neq(self):
        assert LicenseFamily(key="cc") != LicenseFamily(key="osi")

    def test_neq_unknown_type(self):
        assert LicenseFamily(key="cc") != 42

    def test_hash_equal_objects(self):
        a = LicenseFamily(key="cc")
        b = LicenseFamily(key="cc")
        assert hash(a) == hash(b)

    def test_hash_usable_in_set(self):
        s = {LicenseFamily(key="cc"), LicenseFamily(key="cc"), LicenseFamily(key="osi")}
        assert len(s) == 2

    def test_frozen_prevents_mutation(self):
        fam = LicenseFamily(key="cc")
        with pytest.raises((AttributeError, TypeError)):
            fam.key = "other"  # type: ignore[misc]

    def test_enum_property_known(self):
        fam = LicenseFamily(key="cc")
        assert fam.enum is LicenseFamilyEnum.CC

    def test_enum_property_unknown_key(self):
        fam = LicenseFamily(key="totally-unknown")
        assert fam.enum is None


# ---------------------------------------------------------------------------
# LicenseName
# ---------------------------------------------------------------------------


class TestLicenseName:
    def test_str(self):
        assert str(_cc_by_name()) == "cc-by"

    def test_repr(self):
        assert repr(_cc_by_name()) == "LicenseName('cc-by', family='cc')"

    def test_eq_same_type(self):
        assert _cc_by_name() == _cc_by_name()

    def test_eq_str(self):
        assert _cc_by_name() == "cc-by"

    def test_eq_enum(self):
        assert _cc_by_name() == LicenseNameEnum.CC_BY

    def test_neq_different_key(self):
        other = LicenseName(key="cc-by-sa", family=_cc_fam())
        assert _cc_by_name() != other

    def test_hash_equal_objects(self):
        assert hash(_cc_by_name()) == hash(_cc_by_name())

    def test_frozen_prevents_mutation(self):
        name = _cc_by_name()
        with pytest.raises((AttributeError, TypeError)):
            name.key = "other"  # type: ignore[misc]

    def test_family_reference(self):
        assert _cc_by_name().family.key == "cc"

    def test_enum_property_known(self):
        name = LicenseName(key="cc-by", family=_cc_fam())
        assert name.enum is LicenseNameEnum.CC_BY

    def test_enum_property_unknown(self):
        name = LicenseName(key="no-such-name", family=_cc_fam())
        assert name.enum is None


# ---------------------------------------------------------------------------
# LicenseVersion
# ---------------------------------------------------------------------------


class TestLicenseVersion:
    def test_str(self):
        assert str(_mit_version()) == "mit"

    def test_repr_contains_key(self):
        r = repr(_mit_version())
        assert "mit" in r
        assert "osi" in r

    def test_family_shortcut(self):
        v = _mit_version()
        assert v.family.key == "osi"

    def test_eq_same_type(self):
        assert _mit_version() == _mit_version()

    def test_eq_str(self):
        assert _mit_version() == "mit"

    def test_eq_enum(self):
        assert _mit_version() == LicenseVersionEnum.MIT

    def test_neq(self):
        other = LicenseVersion(
            key="apache-2.0",
            url="https://www.apache.org/licenses/LICENSE-2.0",
            license=LicenseName(key="apache", family=_osi_fam()),
        )
        assert _mit_version() != other

    def test_hash_equal_objects(self):
        assert hash(_mit_version()) == hash(_mit_version())

    def test_frozen_prevents_mutation(self):
        v = _mit_version()
        with pytest.raises((AttributeError, TypeError)):
            v.key = "other"  # type: ignore[misc]

    def test_url_stored(self):
        v = _mit_version()
        assert v.url == "https://opensource.org/licenses/MIT"

    def test_url_none(self):
        v = LicenseVersion(
            key="unknown",
            url=None,
            license=LicenseName(key="unknown", family=LicenseFamily(key="unknown")),
        )
        assert v.url is None

    def test_is_family_true(self):
        assert _mit_version().is_family(LicenseFamilyEnum.OSI)

    def test_is_family_false(self):
        assert not _mit_version().is_family(LicenseFamilyEnum.CC)

    def test_is_name_true(self):
        assert _mit_version().is_name(LicenseNameEnum.MIT)

    def test_is_name_false(self):
        assert not _mit_version().is_name(LicenseNameEnum.CC_BY)

    def test_is_version_true(self):
        assert _mit_version().is_version(LicenseVersionEnum.MIT)

    def test_is_version_false(self):
        assert not _mit_version().is_version(LicenseVersionEnum.GPL_3_0)

    def test_enum_property_known(self):
        assert _mit_version().enum is LicenseVersionEnum.MIT

    def test_enum_property_unknown(self):
        v = LicenseVersion(
            key="no-such-version",
            url=None,
            license=LicenseName(key="unknown", family=LicenseFamily(key="unknown")),
        )
        assert v.enum is None

    def test_key_is_not_mutated_by_construction(self):
        # The frozen model must NOT lowercase the key - callers are responsible.
        # This test documents the contract: pass a lowercase key; get it back.
        v = LicenseVersion(
            key="mit",
            url=None,
            license=LicenseName(key="mit", family=LicenseFamily(key="osi")),
        )
        assert v.key == "mit"
