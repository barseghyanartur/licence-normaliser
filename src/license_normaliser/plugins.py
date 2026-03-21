"""Simple plugin interface definitions.

Each plugin is a callable that returns a dict or list of tuples.
Plugins are passed as CLASSES (not instances) - they're instantiated lazily.
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"

__all__ = (
    "RegistryPlugin",
    "URLPlugin",
    "AliasPlugin",
    "FamilyPlugin",
    "NamePlugin",
    "ProsePlugin",
)


class RegistryPlugin:
    """Returns key -> canonical_key mappings."""

    @staticmethod
    def load_registry() -> dict[str, str]:
        raise NotImplementedError


class URLPlugin:
    """Returns cleaned_url -> version_key mappings."""

    @staticmethod
    def load_urls() -> dict[str, str]:
        raise NotImplementedError


class AliasPlugin:
    """Returns alias_string -> version_key mappings."""

    @staticmethod
    def load_aliases() -> dict[str, str]:
        raise NotImplementedError


class FamilyPlugin:
    """Returns version_key -> family_key mappings."""

    @staticmethod
    def load_families() -> dict[str, str]:
        raise NotImplementedError


class NamePlugin:
    """Returns version_key -> name_key mappings."""

    @staticmethod
    def load_names() -> dict[str, str]:
        raise NotImplementedError


class ProsePlugin:
    """Returns list of (compiled_pattern, version_key) for prose matching."""

    @staticmethod
    def load_prose() -> list[tuple[re.Pattern[str], str]]:
        raise NotImplementedError
