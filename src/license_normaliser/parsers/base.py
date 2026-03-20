"""Base parser interface."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseParser(ABC):
    """All data parsers must implement this."""

    url: str
    local_path: str

    @abstractmethod
    def parse(self) -> list[tuple[str, dict[str, Any]]]:
        """Return (license_key, metadata_dict) for every entry."""
        ...

    @classmethod
    def refresh(cls, force: bool = False) -> bool:
        """Fetch fresh data from ``cls.url`` and write to ``cls.local_path``.

        The local path is resolved relative to the package root
        (``src/license_normaliser/``).

        Returns True on success, False on failure.
        """
        import json
        import urllib.request

        target = Path(__file__).parent.parent / cls.local_path
        skipped = target.exists() and not force
        if skipped:
            return True
        try:
            with urllib.request.urlopen(cls.url, timeout=30) as response:  # noqa: S310
                data = response.read()
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            json.loads(data.decode("utf-8"))
            return True
        except Exception:
            return False
