"""Publisher parser - loads publishers.json with URLs and shorthand aliases."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from license_normaliser.plugins import AliasPlugin, URLPlugin

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2026 Artur Barseghyan"
__license__ = "MIT"
__all__ = ("PublisherParser",)


class PublisherParser(AliasPlugin, URLPlugin):
    url = None
    local_path = "data/publishers/publishers.json"

    def parse(self) -> list[tuple[str, dict[str, Any]]]:
        path = Path(__file__).parent.parent / self.local_path
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        results: list[tuple[str, dict[str, Any]]] = []
        urls: dict[str, dict[str, str]] = data.get("urls", {})
        for url, meta in urls.items():
            if isinstance(meta, dict):
                results.append((url, meta))
        return results

    @staticmethod
    def load_aliases() -> dict[str, str]:
        path = Path(__file__).parent.parent / PublisherParser.local_path
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        aliases: dict[str, str] = data.get("shorthand_aliases", {})
        return dict(aliases)

    @staticmethod
    def load_urls() -> dict[str, str]:
        path = Path(__file__).parent.parent / PublisherParser.local_path
        data: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
        result: dict[str, str] = {}
        for url, meta in data.get("urls", {}).items():
            if not isinstance(meta, dict):
                continue
            vk = meta.get("version_key", "")
            if not vk:
                continue
            clean = url.strip().lower().rstrip("/")
            if clean.startswith("http://"):
                clean = "https://" + clean[7:]
            result[clean] = vk
        return result
