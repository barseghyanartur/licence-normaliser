"""Built-in prose-keyword data source.

Reads ``data/prose/prose_patterns.json`` - an ordered list of
``{pattern, version_key, name_key, family_key}`` objects.  Patterns are Python
regular expressions applied (case-insensitive) to the cleaned input string.

File format (``data/prose/prose_patterns.json``)
-------------------------------------------------
.. code-block:: json

    [
      {"pattern": "cc\\s*by-nc-nd\\s*4\\.0",
       "version_key": "cc-by-nc-nd-4.0", "name_key": "cc-by-nc-nd", "family_key": "cc"},
      {"pattern": "all\\s*rights\\s*reserved",
       "version_key": "all-rights-reserved", "name_key": "all-rights-reserved",
       "family_key": "publisher-proprietary"}
    ]

Order matters: the first matching pattern wins, so list more-specific patterns
before more-general ones.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from ..exceptions import DataSourceError
from . import SourceContribution, VersionMetadata

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("BuiltinProseSource",)

logger = logging.getLogger(__name__)

_PROSE_FILE = "prose/prose_patterns.json"


class BuiltinProseSource:
    """Loads ordered prose-keyword patterns from a JSON file."""

    name = "builtin-prose"

    def load(self, data_dir: Path) -> SourceContribution:
        path = data_dir / _PROSE_FILE
        if not path.exists():
            raise DataSourceError(
                f"Builtin prose patterns file not found: {path}. "
                "Ensure the package data is correctly installed."
            )
        try:
            raw: list[object] = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise DataSourceError(
                f"Failed to parse prose patterns file {path}: {exc}"
            ) from exc

        if not isinstance(raw, list):
            raise DataSourceError(
                f"Prose patterns file {path} must contain a JSON array."
            )

        prose: dict[str, str] = {}
        metadata: dict[str, VersionMetadata] = {}
        for i, entry in enumerate(raw):
            if not isinstance(entry, dict):
                logger.warning("Skipping non-object prose entry at index %d", i)
                continue
            pattern = entry.get("pattern")
            vkey = entry.get("version_key")
            name_key = entry.get("name_key")
            family_key = entry.get("family_key")
            if not all(
                isinstance(v, str) for v in (pattern, vkey, name_key, family_key)
            ):
                logger.warning(
                    "Skipping prose entry at index %d: missing or non-string "
                    "'pattern', 'version_key', 'name_key', or 'family_key'",
                    i,
                )
                continue
            prose[str(pattern)] = str(vkey)  # type: ignore[arg-type]
            if str(vkey) not in metadata:
                metadata[str(vkey)] = {  # type: ignore[arg-type]
                    "name_key": str(name_key),  # type: ignore[arg-type]
                    "family_key": str(family_key),  # type: ignore[arg-type]
                }

        return SourceContribution(
            name=self.name,
            aliases={},
            url_map={},
            prose=prose,
            metadata=metadata,
        )
