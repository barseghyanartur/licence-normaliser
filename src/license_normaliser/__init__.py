"""license_normaliser - Comprehensive license normalisation with a
three-level hierarchy."""

from ._core import (
    LicenseFamily,
    LicenseName,
    LicenseVersion,
    normalise_license,
    normalise_licenses,
)
from ._enums import (
    LicenseFamilyEnum,
    LicenseNameEnum,
    LicenseVersionEnum,
)

__title__ = "license-normaliser"
__version__ = "0.1.1"
__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "LicenseFamily",
    "LicenseName",
    "LicenseVersion",
    "LicenseFamilyEnum",
    "LicenseNameEnum",
    "LicenseVersionEnum",
    "__version__",
    "normalise_license",
    "normalise_licenses",
)
