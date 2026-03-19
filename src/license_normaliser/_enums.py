"""License enums - source of truth for all license data.

Every LicenseFamilyEnum, LicenseNameEnum, and LicenseVersionEnum value is
defined here.  No other module should define license data - everything is
derived from these enums.
"""

from enum import Enum
from typing import Optional

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "LicenseFamilyEnum",
    "LicenseNameEnum",
    "LicenseVersionEnum",
)


class LicenseFamilyEnum(Enum):
    """License family enum for type-safe checking."""

    CC = "cc"
    CC0 = "cc0"
    PUBLIC_DOMAIN = "public-domain"
    OSI = "osi"
    COPYLEFT = "copyleft"
    OPEN_DATA = "open-data"
    PUBLISHER_TDM = "publisher-tdm"
    PUBLISHER_OA = "publisher-oa"
    PUBLISHER_PROPRIETARY = "publisher-proprietary"
    OTHER_OA = "other-oa"
    UNKNOWN = "unknown"


class LicenseNameEnum(Enum):
    """License name enum for type-safe checking.

    Each member encodes ``(key, family)`` so that all name-level data lives
    in one place.  Use ``LicenseNameEnum("cc-by")`` for reverse lookup.
    """

    def __new__(
        cls,
        key: str,
        family: "LicenseFamilyEnum",
    ) -> "LicenseNameEnum":
        obj = object.__new__(cls)
        obj._value_ = key
        obj.family_enum = family  # type: ignore[attr-defined]
        return obj

    # ------------------------------------------------------------------
    # Creative Commons - public domain
    # ------------------------------------------------------------------
    CC0 = ("cc0", LicenseFamilyEnum.CC0)
    CC_PDM = ("cc-pdm", LicenseFamilyEnum.PUBLIC_DOMAIN)

    # ------------------------------------------------------------------
    # Creative Commons - standard variants
    # ------------------------------------------------------------------
    CC_BY = ("cc-by", LicenseFamilyEnum.CC)
    CC_BY_SA = ("cc-by-sa", LicenseFamilyEnum.CC)
    CC_BY_ND = ("cc-by-nd", LicenseFamilyEnum.CC)
    CC_BY_NC = ("cc-by-nc", LicenseFamilyEnum.CC)
    CC_BY_NC_SA = ("cc-by-nc-sa", LicenseFamilyEnum.CC)
    CC_BY_NC_ND = ("cc-by-nc-nd", LicenseFamilyEnum.CC)

    # ------------------------------------------------------------------
    # Creative Commons - IGO sub-variants
    # ------------------------------------------------------------------
    CC_BY_IGO = ("cc-by-igo", LicenseFamilyEnum.CC)
    CC_BY_SA_IGO = ("cc-by-sa-igo", LicenseFamilyEnum.CC)
    CC_BY_ND_IGO = ("cc-by-nd-igo", LicenseFamilyEnum.CC)
    CC_BY_NC_IGO = ("cc-by-nc-igo", LicenseFamilyEnum.CC)
    CC_BY_NC_SA_IGO = ("cc-by-nc-sa-igo", LicenseFamilyEnum.CC)
    CC_BY_NC_ND_IGO = ("cc-by-nc-nd-igo", LicenseFamilyEnum.CC)

    # ------------------------------------------------------------------
    # OSI permissive
    # ------------------------------------------------------------------
    MIT = ("mit", LicenseFamilyEnum.OSI)
    APACHE = ("apache", LicenseFamilyEnum.OSI)
    BSD_2_CLAUSE = ("bsd-2-clause", LicenseFamilyEnum.OSI)
    BSD_3_CLAUSE = ("bsd-3-clause", LicenseFamilyEnum.OSI)
    ISC = ("isc", LicenseFamilyEnum.OSI)
    MPL = ("mpl", LicenseFamilyEnum.OSI)

    # ------------------------------------------------------------------
    # Copyleft
    # ------------------------------------------------------------------
    GPL_2 = ("gpl-2", LicenseFamilyEnum.COPYLEFT)
    GPL_3 = ("gpl-3", LicenseFamilyEnum.COPYLEFT)
    AGPL_3 = ("agpl-3", LicenseFamilyEnum.COPYLEFT)
    LGPL_2_1 = ("lgpl-2.1", LicenseFamilyEnum.COPYLEFT)
    LGPL_3 = ("lgpl-3", LicenseFamilyEnum.COPYLEFT)

    # ------------------------------------------------------------------
    # Open Data
    # ------------------------------------------------------------------
    ODBL = ("odbl", LicenseFamilyEnum.OPEN_DATA)
    ODC_BY = ("odc-by", LicenseFamilyEnum.OPEN_DATA)
    PDDL = ("pddl", LicenseFamilyEnum.OPEN_DATA)
    FAL = ("fal", LicenseFamilyEnum.OTHER_OA)

    # ------------------------------------------------------------------
    # Publisher - Elsevier
    # ------------------------------------------------------------------
    ELSEVIER_OA = ("elsevier-oa", LicenseFamilyEnum.PUBLISHER_OA)
    ELSEVIER_TDM = ("elsevier-tdm", LicenseFamilyEnum.PUBLISHER_TDM)

    # ------------------------------------------------------------------
    # Publisher - Wiley
    # ------------------------------------------------------------------
    WILEY_TDM = ("wiley-tdm", LicenseFamilyEnum.PUBLISHER_TDM)
    WILEY_VOR = ("wiley-vor", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)
    WILEY_AM = ("wiley-am", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)
    WILEY_TERMS = ("wiley-terms", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - Springer Nature
    # ------------------------------------------------------------------
    SPRINGER_TDM = ("springer-tdm", LicenseFamilyEnum.PUBLISHER_TDM)
    SPRINGERNATURE_TDM = ("springernature-tdm", LicenseFamilyEnum.PUBLISHER_TDM)

    # ------------------------------------------------------------------
    # Publisher - Taylor & Francis
    # ------------------------------------------------------------------
    TANDF_TERMS = ("tandf-terms", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - OUP
    # ------------------------------------------------------------------
    OUP_CHORUS = ("oup-chorus", LicenseFamilyEnum.PUBLISHER_OA)
    OUP_TERMS = ("oup-terms", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - SAGE
    # ------------------------------------------------------------------
    SAGE_PERMISSIONS = ("sage-permissions", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - ACS
    # ------------------------------------------------------------------
    ACS_AUTHORCHOICE = ("acs-authorchoice", LicenseFamilyEnum.PUBLISHER_OA)
    ACS_AUTHORCHOICE_CCBY = ("acs-authorchoice-ccby", LicenseFamilyEnum.PUBLISHER_OA)
    ACS_AUTHORCHOICE_CCBYNCND = (
        "acs-authorchoice-ccbyncnd",
        LicenseFamilyEnum.PUBLISHER_OA,
    )
    ACS_AUTHORCHOICE_NIH = ("acs-authorchoice-nih", LicenseFamilyEnum.PUBLISHER_OA)

    # ------------------------------------------------------------------
    # Publisher - RSC
    # ------------------------------------------------------------------
    RSC_TERMS = ("rsc-terms", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - IOP
    # ------------------------------------------------------------------
    IOP_TDM = ("iop-tdm", LicenseFamilyEnum.PUBLISHER_TDM)
    IOP_COPYRIGHT = ("iop-copyright", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - BMJ
    # ------------------------------------------------------------------
    BMJ_COPYRIGHT = ("bmj-copyright", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - AAAS / Science
    # ------------------------------------------------------------------
    AAAS_AUTHOR_REUSE = ("aaas-author-reuse", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - PNAS
    # ------------------------------------------------------------------
    PNAS_LICENSES = ("pnas-licenses", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - APS
    # ------------------------------------------------------------------
    APS_DEFAULT = ("aps-default", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)
    APS_TDM = ("aps-tdm", LicenseFamilyEnum.PUBLISHER_TDM)

    # ------------------------------------------------------------------
    # Publisher - Cambridge
    # ------------------------------------------------------------------
    CUP_TERMS = ("cup-terms", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - AIP
    # ------------------------------------------------------------------
    AIP_RIGHTS = ("aip-rights", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - JAMA
    # ------------------------------------------------------------------
    JAMA_CC_BY = ("jama-cc-by", LicenseFamilyEnum.PUBLISHER_OA)

    # ------------------------------------------------------------------
    # Publisher - De Gruyter
    # ------------------------------------------------------------------
    DEGRUYTER_TERMS = ("degruyter-terms", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)

    # ------------------------------------------------------------------
    # Publisher - Thieme
    # ------------------------------------------------------------------
    THIEME_NLM = ("thieme-nlm", LicenseFamilyEnum.PUBLISHER_OA)

    # ------------------------------------------------------------------
    # Catch-all / unknown
    # ------------------------------------------------------------------
    PUBLIC_DOMAIN_MARK = ("public-domain", LicenseFamilyEnum.PUBLIC_DOMAIN)
    OTHER_OA = ("other-oa", LicenseFamilyEnum.OTHER_OA)
    PUBLISHER_SPECIFIC_OA = ("publisher-specific-oa", LicenseFamilyEnum.PUBLISHER_OA)
    UNSPECIFIED_OA = ("unspecified-oa", LicenseFamilyEnum.OTHER_OA)
    OPEN_ACCESS = ("open-access", LicenseFamilyEnum.OTHER_OA)
    IMPLIED_OA = ("implied-oa", LicenseFamilyEnum.PUBLISHER_OA)
    AUTHOR_MANUSCRIPT = ("author-manuscript", LicenseFamilyEnum.PUBLISHER_OA)
    ALL_RIGHTS_RESERVED = (
        "all-rights-reserved",
        LicenseFamilyEnum.PUBLISHER_PROPRIETARY,
    )
    NO_REUSE = ("no-reuse", LicenseFamilyEnum.PUBLISHER_PROPRIETARY)
    UNKNOWN = ("unknown", LicenseFamilyEnum.UNKNOWN)

    @property
    def family(self) -> LicenseFamilyEnum:
        """Return the :class:`LicenseFamilyEnum` for this license name."""
        return self.family_enum  # type: ignore[attr-defined]


class LicenseVersionEnum(Enum):
    """License version enum for type-safe checking.

    Each member encodes ``(key, url, name_enum)`` so that all version-level
    data lives in one place.  Use ``LicenseVersionEnum("cc-by-4.0")`` for
    reverse lookup by key string.
    """

    def __new__(
        cls,
        key: str,
        url: Optional[str],
        name: "LicenseNameEnum",
    ) -> "LicenseVersionEnum":
        obj = object.__new__(cls)
        obj._value_ = key
        obj.url = url  # type: ignore[attr-defined]
        obj.license_name = name  # type: ignore[attr-defined]
        return obj

    # ------------------------------------------------------------------
    # CC Zero / Public Domain
    # ------------------------------------------------------------------
    CC0 = (
        "cc0",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        LicenseNameEnum.CC0,
    )
    CC0_1_0 = (
        "cc0-1.0",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        LicenseNameEnum.CC0,
    )
    CC_ZERO = (
        "cc-zero",
        "https://creativecommons.org/publicdomain/zero/1.0/",
        LicenseNameEnum.CC0,
    )
    CC_PDM = (
        "cc-pdm",
        "https://creativecommons.org/publicdomain/mark/1.0/",
        LicenseNameEnum.CC_PDM,
    )

    # ------------------------------------------------------------------
    # CC BY
    # ------------------------------------------------------------------
    CC_BY = (
        "cc-by",
        "https://creativecommons.org/licenses/by/4.0/",
        LicenseNameEnum.CC_BY,
    )
    CC_BY_4_0 = (
        "cc-by-4.0",
        "https://creativecommons.org/licenses/by/4.0/",
        LicenseNameEnum.CC_BY,
    )
    CC_BY_3_0 = (
        "cc-by-3.0",
        "https://creativecommons.org/licenses/by/3.0/",
        LicenseNameEnum.CC_BY,
    )
    CC_BY_2_5 = (
        "cc-by-2.5",
        "https://creativecommons.org/licenses/by/2.5/",
        LicenseNameEnum.CC_BY,
    )
    CC_BY_2_0 = (
        "cc-by-2.0",
        "https://creativecommons.org/licenses/by/2.0/",
        LicenseNameEnum.CC_BY,
    )
    CC_BY_1_0 = (
        "cc-by-1.0",
        "https://creativecommons.org/licenses/by/1.0/",
        LicenseNameEnum.CC_BY,
    )

    # ------------------------------------------------------------------
    # CC BY-SA
    # ------------------------------------------------------------------
    CC_BY_SA = (
        "cc-by-sa",
        "https://creativecommons.org/licenses/by-sa/4.0/",
        LicenseNameEnum.CC_BY_SA,
    )
    CC_BY_SA_4_0 = (
        "cc-by-sa-4.0",
        "https://creativecommons.org/licenses/by-sa/4.0/",
        LicenseNameEnum.CC_BY_SA,
    )
    CC_BY_SA_3_0 = (
        "cc-by-sa-3.0",
        "https://creativecommons.org/licenses/by-sa/3.0/",
        LicenseNameEnum.CC_BY_SA,
    )
    CC_BY_SA_2_5 = (
        "cc-by-sa-2.5",
        "https://creativecommons.org/licenses/by-sa/2.5/",
        LicenseNameEnum.CC_BY_SA,
    )
    CC_BY_SA_2_0 = (
        "cc-by-sa-2.0",
        "https://creativecommons.org/licenses/by-sa/2.0/",
        LicenseNameEnum.CC_BY_SA,
    )

    # ------------------------------------------------------------------
    # CC BY-ND
    # ------------------------------------------------------------------
    CC_BY_ND = (
        "cc-by-nd",
        "https://creativecommons.org/licenses/by-nd/4.0/",
        LicenseNameEnum.CC_BY_ND,
    )
    CC_BY_ND_4_0 = (
        "cc-by-nd-4.0",
        "https://creativecommons.org/licenses/by-nd/4.0/",
        LicenseNameEnum.CC_BY_ND,
    )
    CC_BY_ND_3_0 = (
        "cc-by-nd-3.0",
        "https://creativecommons.org/licenses/by-nd/3.0/",
        LicenseNameEnum.CC_BY_ND,
    )
    CC_BY_ND_2_0 = (
        "cc-by-nd-2.0",
        "https://creativecommons.org/licenses/by-nd/2.0/",
        LicenseNameEnum.CC_BY_ND,
    )

    # ------------------------------------------------------------------
    # CC BY-NC
    # ------------------------------------------------------------------
    CC_BY_NC = (
        "cc-by-nc",
        "https://creativecommons.org/licenses/by-nc/4.0/",
        LicenseNameEnum.CC_BY_NC,
    )
    CC_BY_NC_4_0 = (
        "cc-by-nc-4.0",
        "https://creativecommons.org/licenses/by-nc/4.0/",
        LicenseNameEnum.CC_BY_NC,
    )
    CC_BY_NC_3_0 = (
        "cc-by-nc-3.0",
        "https://creativecommons.org/licenses/by-nc/3.0/",
        LicenseNameEnum.CC_BY_NC,
    )
    CC_BY_NC_2_5 = (
        "cc-by-nc-2.5",
        "https://creativecommons.org/licenses/by-nc/2.5/",
        LicenseNameEnum.CC_BY_NC,
    )
    CC_BY_NC_2_0 = (
        "cc-by-nc-2.0",
        "https://creativecommons.org/licenses/by-nc/2.0/",
        LicenseNameEnum.CC_BY_NC,
    )

    # ------------------------------------------------------------------
    # CC BY-NC-SA
    # ------------------------------------------------------------------
    CC_BY_NC_SA = (
        "cc-by-nc-sa",
        "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        LicenseNameEnum.CC_BY_NC_SA,
    )
    CC_BY_NC_SA_4_0 = (
        "cc-by-nc-sa-4.0",
        "https://creativecommons.org/licenses/by-nc-sa/4.0/",
        LicenseNameEnum.CC_BY_NC_SA,
    )
    CC_BY_NC_SA_3_0 = (
        "cc-by-nc-sa-3.0",
        "https://creativecommons.org/licenses/by-nc-sa/3.0/",
        LicenseNameEnum.CC_BY_NC_SA,
    )
    CC_BY_NC_SA_2_5 = (
        "cc-by-nc-sa-2.5",
        "https://creativecommons.org/licenses/by-nc-sa/2.5/",
        LicenseNameEnum.CC_BY_NC_SA,
    )
    CC_BY_NC_SA_2_0 = (
        "cc-by-nc-sa-2.0",
        "https://creativecommons.org/licenses/by-nc-sa/2.0/",
        LicenseNameEnum.CC_BY_NC_SA,
    )

    # ------------------------------------------------------------------
    # CC BY-NC-ND
    # ------------------------------------------------------------------
    CC_BY_NC_ND = (
        "cc-by-nc-nd",
        "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        LicenseNameEnum.CC_BY_NC_ND,
    )
    CC_BY_NC_ND_4_0 = (
        "cc-by-nc-nd-4.0",
        "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        LicenseNameEnum.CC_BY_NC_ND,
    )
    CC_BY_NC_ND_3_0 = (
        "cc-by-nc-nd-3.0",
        "https://creativecommons.org/licenses/by-nc-nd/3.0/",
        LicenseNameEnum.CC_BY_NC_ND,
    )
    CC_BY_NC_ND_2_5 = (
        "cc-by-nc-nd-2.5",
        "https://creativecommons.org/licenses/by-nc-nd/2.5/",
        LicenseNameEnum.CC_BY_NC_ND,
    )
    CC_BY_NC_ND_2_0 = (
        "cc-by-nc-nd-2.0",
        "https://creativecommons.org/licenses/by-nc-nd/2.0/",
        LicenseNameEnum.CC_BY_NC_ND,
    )

    # ------------------------------------------------------------------
    # CC IGO variants
    # ------------------------------------------------------------------
    CC_BY_3_0_IGO = (
        "cc-by-3.0-igo",
        "https://creativecommons.org/licenses/by/3.0/igo/",
        LicenseNameEnum.CC_BY_IGO,
    )
    CC_BY_4_0_IGO = (
        "cc-by-4.0-igo",
        "https://creativecommons.org/licenses/by/4.0/",
        LicenseNameEnum.CC_BY_IGO,
    )
    CC_BY_NC_SA_3_0_IGO = (
        "cc-by-nc-sa-3.0-igo",
        "https://creativecommons.org/licenses/by-nc-sa/3.0/igo/",
        LicenseNameEnum.CC_BY_NC_SA_IGO,
    )
    CC_BY_NC_ND_3_0_IGO = (
        "cc-by-nc-nd-3.0-igo",
        "https://creativecommons.org/licenses/by-nc-nd/3.0/igo/",
        LicenseNameEnum.CC_BY_NC_ND_IGO,
    )
    CC_BY_NC_ND_4_0_IGO = (
        "cc-by-nc-nd-4.0-igo",
        "https://creativecommons.org/licenses/by-nc-nd/4.0/",
        LicenseNameEnum.CC_BY_NC_ND_IGO,
    )

    # ------------------------------------------------------------------
    # OSI permissive
    # ------------------------------------------------------------------
    MIT = (
        "mit",
        "https://opensource.org/licenses/MIT",
        LicenseNameEnum.MIT,
    )
    APACHE_2_0 = (
        "apache-2.0",
        "https://www.apache.org/licenses/LICENSE-2.0",
        LicenseNameEnum.APACHE,
    )
    BSD_2_CLAUSE = (
        "bsd-2-clause",
        "https://opensource.org/licenses/BSD-2-Clause",
        LicenseNameEnum.BSD_2_CLAUSE,
    )
    BSD_3_CLAUSE = (
        "bsd-3-clause",
        "https://opensource.org/licenses/BSD-3-Clause",
        LicenseNameEnum.BSD_3_CLAUSE,
    )
    ISC = (
        "isc",
        "https://opensource.org/licenses/ISC",
        LicenseNameEnum.ISC,
    )
    MPL_2_0 = (
        "mpl-2.0",
        "https://www.mozilla.org/en-US/MPL/2.0/",
        LicenseNameEnum.MPL,
    )

    # ------------------------------------------------------------------
    # Copyleft
    # ------------------------------------------------------------------
    GPL_2_0 = (
        "gpl-2.0",
        "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
        LicenseNameEnum.GPL_2,
    )
    GPL_2_0_ONLY = (
        "gpl-2.0-only",
        "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
        LicenseNameEnum.GPL_2,
    )
    GPL_3_0 = (
        "gpl-3.0",
        "https://www.gnu.org/licenses/gpl-3.0.html",
        LicenseNameEnum.GPL_3,
    )
    GPL_3_0_ONLY = (
        "gpl-3.0-only",
        "https://www.gnu.org/licenses/gpl-3.0.html",
        LicenseNameEnum.GPL_3,
    )
    AGPL_3_0 = (
        "agpl-3.0",
        "https://www.gnu.org/licenses/agpl-3.0.html",
        LicenseNameEnum.AGPL_3,
    )
    AGPL_3_0_ONLY = (
        "agpl-3.0-only",
        "https://www.gnu.org/licenses/agpl-3.0.html",
        LicenseNameEnum.AGPL_3,
    )
    LGPL_2_1 = (
        "lgpl-2.1",
        "https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html",
        LicenseNameEnum.LGPL_2_1,
    )
    LGPL_2_1_ONLY = (
        "lgpl-2.1-only",
        "https://www.gnu.org/licenses/old-licenses/lgpl-2.1.html",
        LicenseNameEnum.LGPL_2_1,
    )
    LGPL_3_0 = (
        "lgpl-3.0",
        "https://www.gnu.org/licenses/lgpl-3.0.html",
        LicenseNameEnum.LGPL_3,
    )
    LGPL_3_0_ONLY = (
        "lgpl-3.0-only",
        "https://www.gnu.org/licenses/lgpl-3.0.html",
        LicenseNameEnum.LGPL_3,
    )

    # ------------------------------------------------------------------
    # Open Data
    # ------------------------------------------------------------------
    ODBL = (
        "odbl",
        "https://opendatacommons.org/licenses/odbl/1-0/",
        LicenseNameEnum.ODBL,
    )
    ODC_BY = (
        "odc-by",
        "https://opendatacommons.org/licenses/by/1-0/",
        LicenseNameEnum.ODC_BY,
    )
    PDDL = (
        "pddl",
        "https://opendatacommons.org/licenses/pddl/1-0/",
        LicenseNameEnum.PDDL,
    )
    FAL = (
        "fal",
        "https://artlibre.org/licence/lal/en/",
        LicenseNameEnum.FAL,
    )
    FLDL = (
        "fldl",
        "https://artlibre.org/licence/lal/en/",
        LicenseNameEnum.FAL,
    )

    # ------------------------------------------------------------------
    # Publisher - Elsevier
    # ------------------------------------------------------------------
    ELSEVIER_OA = (
        "elsevier-oa",
        "https://www.elsevier.com/open-access/userlicense/1.0/",
        LicenseNameEnum.ELSEVIER_OA,
    )
    ELSEVIER_TDM = (
        "elsevier-tdm",
        "https://www.elsevier.com/tdm/userlicense/1.0/",
        LicenseNameEnum.ELSEVIER_TDM,
    )

    # ------------------------------------------------------------------
    # Publisher - Wiley
    # ------------------------------------------------------------------
    WILEY_TDM = (
        "wiley-tdm",
        "http://doi.wiley.com/10.1002/tdm_license_1",
        LicenseNameEnum.WILEY_TDM,
    )
    WILEY_TDM_1_1 = (
        "wiley-tdm-1.1",
        "http://doi.wiley.com/10.1002/tdm_license_1.1",
        LicenseNameEnum.WILEY_TDM,
    )
    WILEY_VOR = (
        "wiley-vor",
        "http://onlinelibrary.wiley.com/termsAndConditions#vor",
        LicenseNameEnum.WILEY_VOR,
    )
    WILEY_AM = (
        "wiley-am",
        "http://onlinelibrary.wiley.com/termsAndConditions#am",
        LicenseNameEnum.WILEY_AM,
    )
    WILEY_TERMS = (
        "wiley-terms",
        "https://onlinelibrary.wiley.com/terms-and-conditions",
        LicenseNameEnum.WILEY_TERMS,
    )

    # ------------------------------------------------------------------
    # Publisher - Springer
    # ------------------------------------------------------------------
    SPRINGER_TDM = (
        "springer-tdm",
        "https://www.springer.com/tdm",
        LicenseNameEnum.SPRINGER_TDM,
    )
    SPRINGERNATURE_TDM = (
        "springernature-tdm",
        "https://www.springernature.com/gp/researchers/text-and-data-mining",
        LicenseNameEnum.SPRINGERNATURE_TDM,
    )

    # ------------------------------------------------------------------
    # Publisher - Taylor & Francis
    # ------------------------------------------------------------------
    TANDF_TERMS = (
        "tandf-terms",
        "https://www.tandfonline.com/action/showCopyRight",
        LicenseNameEnum.TANDF_TERMS,
    )

    # ------------------------------------------------------------------
    # Publisher - OUP
    # ------------------------------------------------------------------
    OUP_CHORUS = (
        "oup-chorus",
        "https://academic.oup.com/journals/pages/open_access/funder_policies/"
        "chorus/standard_publication_model",
        LicenseNameEnum.OUP_CHORUS,
    )
    OUP_TERMS = (
        "oup-terms",
        "https://academic.oup.com/pages/standard-publication-reuse-rights",
        LicenseNameEnum.OUP_TERMS,
    )

    # ------------------------------------------------------------------
    # Publisher - SAGE
    # ------------------------------------------------------------------
    SAGE_PERMISSIONS = (
        "sage-permissions",
        "https://us.sagepub.com/en-us/nam/journals-permissions",
        LicenseNameEnum.SAGE_PERMISSIONS,
    )

    # ------------------------------------------------------------------
    # Publisher - ACS
    # ------------------------------------------------------------------
    ACS_AUTHORCHOICE_CCBY = (
        "acs-authorchoice-ccby",
        "https://pubs.acs.org/page/policy/authorchoice_ccby_termsofuse.html",
        LicenseNameEnum.ACS_AUTHORCHOICE_CCBY,
    )
    ACS_AUTHORCHOICE_CCBYNCND = (
        "acs-authorchoice-ccbyncnd",
        "https://pubs.acs.org/page/policy/authorchoice_ccbyncnd_termsofuse.html",
        LicenseNameEnum.ACS_AUTHORCHOICE_CCBYNCND,
    )
    ACS_AUTHORCHOICE = (
        "acs-authorchoice",
        "https://pubs.acs.org/page/policy/authorchoice_termsofuse.html",
        LicenseNameEnum.ACS_AUTHORCHOICE,
    )
    ACS_AUTHORCHOICE_NIH = (
        "acs-authorchoice-nih",
        "https://pubs.acs.org/page/policy/"
        "acs_authorchoice_with_nih_addendum_termsofuse.html",
        LicenseNameEnum.ACS_AUTHORCHOICE_NIH,
    )

    # ------------------------------------------------------------------
    # Publisher - RSC
    # ------------------------------------------------------------------
    RSC_TERMS = (
        "rsc-terms",
        "https://www.rsc.org/journals-books-databases/journal-authors-reviewers/"
        "licences-copyright-permissions/",
        LicenseNameEnum.RSC_TERMS,
    )

    # ------------------------------------------------------------------
    # Publisher - IOP
    # ------------------------------------------------------------------
    IOP_TDM = (
        "iop-tdm",
        "https://iopscience.iop.org/info/page/text-and-data-mining",
        LicenseNameEnum.IOP_TDM,
    )
    IOP_COPYRIGHT = (
        "iop-copyright",
        "https://iopscience.iop.org/page/copyright",
        LicenseNameEnum.IOP_COPYRIGHT,
    )

    # ------------------------------------------------------------------
    # Publisher - BMJ
    # ------------------------------------------------------------------
    BMJ_COPYRIGHT = (
        "bmj-copyright",
        "https://www.bmj.com/company/legal-stuff/copyright-notice/",
        LicenseNameEnum.BMJ_COPYRIGHT,
    )

    # ------------------------------------------------------------------
    # Publisher - AAAS / Science
    # ------------------------------------------------------------------
    AAAS_AUTHOR_REUSE = (
        "aaas-author-reuse",
        "https://www.science.org/content/page/science-licenses-journal-article-reuse",
        LicenseNameEnum.AAAS_AUTHOR_REUSE,
    )

    # ------------------------------------------------------------------
    # Publisher - PNAS
    # ------------------------------------------------------------------
    PNAS_LICENSES = (
        "pnas-licenses",
        "https://www.pnas.org/site/aboutpnas/licenses.xhtml",
        LicenseNameEnum.PNAS_LICENSES,
    )

    # ------------------------------------------------------------------
    # Publisher - APS
    # ------------------------------------------------------------------
    APS_DEFAULT = (
        "aps-default",
        "https://link.aps.org/licenses/aps-default-license",
        LicenseNameEnum.APS_DEFAULT,
    )
    APS_TDM = (
        "aps-tdm",
        "https://link.aps.org/licenses/aps-default-text-mining-license",
        LicenseNameEnum.APS_TDM,
    )

    # ------------------------------------------------------------------
    # Publisher - Cambridge
    # ------------------------------------------------------------------
    CUP_TERMS = (
        "cup-terms",
        "https://www.cambridge.org/core/terms",
        LicenseNameEnum.CUP_TERMS,
    )

    # ------------------------------------------------------------------
    # Publisher - AIP
    # ------------------------------------------------------------------
    AIP_RIGHTS = (
        "aip-rights",
        "https://publishing.aip.org/authors/rights-and-permissions",
        LicenseNameEnum.AIP_RIGHTS,
    )

    # ------------------------------------------------------------------
    # Publisher - JAMA
    # ------------------------------------------------------------------
    JAMA_CC_BY = (
        "jama-cc-by",
        "https://jamanetwork.com/pages/cc-by-license-permissions",
        LicenseNameEnum.JAMA_CC_BY,
    )

    # ------------------------------------------------------------------
    # Publisher - De Gruyter
    # ------------------------------------------------------------------
    DEGRUYTER_TERMS = (
        "degruyter-terms",
        "https://www.degruyter.com/dg/page/496",
        LicenseNameEnum.DEGRUYTER_TERMS,
    )

    # ------------------------------------------------------------------
    # Publisher - Thieme
    # ------------------------------------------------------------------
    THIEME_NLM = (
        "thieme-nlm",
        "https://www.thieme.de/statics/dokumente/thieme/final/de/dokumente/"
        "sw_oa/nlm_license_terms_thieme.pdf",
        LicenseNameEnum.THIEME_NLM,
    )

    # ------------------------------------------------------------------
    # Catch-all / unknown
    # ------------------------------------------------------------------
    PUBLIC_DOMAIN = (
        "public-domain",
        None,
        LicenseNameEnum.PUBLIC_DOMAIN_MARK,
    )
    OTHER_OA = (
        "other-oa",
        None,
        LicenseNameEnum.OTHER_OA,
    )
    PUBLISHER_SPECIFIC_OA = (
        "publisher-specific-oa",
        None,
        LicenseNameEnum.PUBLISHER_SPECIFIC_OA,
    )
    UNSPECIFIED_OA = (
        "unspecified-oa",
        None,
        LicenseNameEnum.UNSPECIFIED_OA,
    )
    OPEN_ACCESS = (
        "open-access",
        None,
        LicenseNameEnum.OPEN_ACCESS,
    )
    IMPLIED_OA = (
        "implied-oa",
        None,
        LicenseNameEnum.IMPLIED_OA,
    )
    AUTHOR_MANUSCRIPT = (
        "author-manuscript",
        None,
        LicenseNameEnum.AUTHOR_MANUSCRIPT,
    )
    ALL_RIGHTS_RESERVED = (
        "all-rights-reserved",
        None,
        LicenseNameEnum.ALL_RIGHTS_RESERVED,
    )
    NO_REUSE = (
        "no-reuse",
        None,
        LicenseNameEnum.NO_REUSE,
    )
    UNKNOWN = (
        "unknown",
        None,
        LicenseNameEnum.UNKNOWN,
    )

    @property
    def name_enum(self) -> LicenseNameEnum:
        """Return the :class:`LicenseNameEnum` for this version."""
        return self.license_name  # type: ignore[attr-defined]

    @property
    def family(self) -> LicenseFamilyEnum:
        """Return the :class:`LicenseFamilyEnum` for this version."""
        return self.license_name.family  # type: ignore[attr-defined]
