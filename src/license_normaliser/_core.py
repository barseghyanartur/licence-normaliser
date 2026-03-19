"""License Normaliser - public orchestration shim.

This module re-exports the full public API so that external code importing
from ``license_normaliser._core`` continues to work unchanged.  The actual
implementation is split across the focused sub-modules:

* :mod:`._models`   - dataclasses (LicenseFamily, LicenseName, LicenseVersion)
* :mod:`._enums`    - enum definitions
* :mod:`._registry` - all data and object factories
* :mod:`._pipeline` - six resolution steps
* :mod:`._cache`    - caching wrapper and public normalise_* functions
"""

from __future__ import annotations

from ._cache import normalise_license_cached as normalise_license
from ._cache import normalise_licenses
from ._models import LicenseFamily, LicenseName, LicenseVersion

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "LicenseFamily",
    "LicenseName",
    "LicenseVersion",
    "normalise_license",
    "normalise_licenses",
)
