#!/usr/bin/env python3
"""Migrate publishers.json (urls + shorthand_aliases) into aliases/aliases.json.

Adds:
  - URLs to the "urls" array
  - Shorthand aliases to the "aliases" array

Run AFTER the url_map migration (or on the already-merged file).

The script:
- Matches by version_key OR aliases in the entry
- Preserves exact format (2-space indent, blank lines, ordering)
- Adds new entries in alphabetical order by version_key
- Is idempotent — running multiple times adds nothing new

::

    # Dry-run: shows summary + writes aliases.dryrun.json
    uv run python scripts/migrate_publishers_to_aliases.py --dry-run

    # Real migration: overwrites aliases.json
    uv run python scripts/migrate_publishers_to_aliases.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "src" / "licence_normaliser" / "data"

ALIASES_PATH = DATA_DIR / "aliases" / "aliases.json"
PUBLISHERS_PATH = DATA_DIR / "publishers" / "publishers.json"
DRYRUN_PATH = DATA_DIR / "aliases" / "aliases.dryrun.json"


def normalise_url(url: str) -> str:
    """Normalise URL exactly as _normaliser.py does at runtime."""
    key = url.strip().lower().rstrip("/")
    if key.startswith("http://"):
        key = "https://" + key[7:]
    return key


def build_entry_lookup(aliases_data: dict) -> tuple[dict, dict]:
    """Build lookup tables from version_key and aliases to entry key."""
    version_key_to_entry_key: dict[str, str] = {}
    alias_to_entry_key: dict[str, str] = {}

    for entry_key, meta in aliases_data.items():
        if entry_key.startswith("_") or not isinstance(meta, dict):
            continue

        vk = meta.get("version_key")
        if vk:
            version_key_to_entry_key[vk] = entry_key

        aliases = meta.get("aliases", [])
        if isinstance(aliases, list):
            for alias in aliases:
                alias_to_entry_key[alias] = entry_key

    return version_key_to_entry_key, alias_to_entry_key


def find_matching_entry_key(
    version_key: str,
    version_key_to_entry_key: dict[str, str],
    alias_to_entry_key: dict[str, str],
) -> str | None:
    """Find the entry key that matches this version_key."""
    if version_key in version_key_to_entry_key:
        return version_key_to_entry_key[version_key]
    if version_key in alias_to_entry_key:
        return alias_to_entry_key[version_key]
    return None


def format_entry_with_multiline_arrays(key: str, data: dict, is_last: bool) -> str:
    """Format entry with multiline arrays like the original format."""
    lines = [f'  "{key}": {{']

    field_order = [
        "version_key",
        "name_key",
        "family_key",
        "aliases",
        "justification",
        "urls",
    ]

    fields_to_write = [fn for fn in field_order if fn in data]
    fields_to_write.extend(fn for fn in data if fn not in field_order)

    for i, field_name in enumerate(fields_to_write):
        is_field_last = i == len(fields_to_write) - 1
        value = data[field_name]

        if isinstance(value, list):
            if not value:
                if not is_field_last:
                    lines.append(f'    "{field_name}": [],')
                else:
                    lines.append(f'    "{field_name}": []')
            else:
                lines.append(f'    "{field_name}": [')
                for j, item in enumerate(value):
                    is_last_item = j == len(value) - 1
                    suffix = "" if is_last_item else ","
                    if isinstance(item, str):
                        lines.append(f'      "{item}"{suffix}')
                    else:
                        lines.append(f"      {item}{suffix}")
                if not is_field_last:
                    lines.append("    ],")
                else:
                    lines.append("    ]")
        else:
            suffix = "" if is_field_last else ","
            if isinstance(value, str):
                lines.append(f'    "{field_name}": "{value}"{suffix}')
            elif value is None:
                lines.append(f'    "{field_name}": null{suffix}')
            elif isinstance(value, bool):
                lines.append(
                    f'    "{field_name}": {"true" if value else "false"}{suffix}'
                )
            else:
                lines.append(f'    "{field_name}": {value}{suffix}')

    lines.append("  }")

    result = "\n".join(lines)
    if not is_last:
        result += ","

    return result


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Migrate publishers.json into aliases.json"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write to aliases.dryrun.json instead of aliases.json",
    )
    args = parser.parse_args()

    with open(ALIASES_PATH, encoding="utf-8") as f:
        aliases_content = f.read()

    with open(PUBLISHERS_PATH, encoding="utf-8") as f:
        publishers: dict = json.loads(f.read())

    aliases_data: dict = json.loads(aliases_content)

    version_key_to_entry_key, alias_to_entry_key = build_entry_lookup(aliases_data)

    urls_added = 0
    aliases_added = 0
    new_entries_created = 0
    unmatched_urls: list[tuple[str, str]] = []
    unmatched_aliases: list[tuple[str, str]] = []

    # 1. Process URLs
    url_to_version: dict[str, str] = {}
    for raw_url, meta in publishers.get("urls", {}).items():
        if not isinstance(meta, dict):
            continue
        vk = meta.get("version_key")
        if vk:
            norm_url = normalise_url(raw_url)
            url_to_version[norm_url] = vk

    for norm_url, vk in url_to_version.items():
        entry_key = find_matching_entry_key(
            vk, version_key_to_entry_key, alias_to_entry_key
        )

        if entry_key is None:
            unmatched_urls.append((norm_url, vk))
            continue

        entry = aliases_data[entry_key]
        if "urls" not in entry:
            entry["urls"] = []

        if norm_url not in entry["urls"]:
            entry["urls"].append(norm_url)
            urls_added += 1

    # Create new entries for unmatched URLs
    for norm_url, vk in url_to_version.items():
        entry_key = find_matching_entry_key(
            vk, version_key_to_entry_key, alias_to_entry_key
        )
        if entry_key is not None:
            continue

        if any(
            e.get("version_key") == vk
            for e in aliases_data.values()
            if isinstance(e, dict)
        ):
            continue

        meta = publishers.get("urls", {}).get(norm_url, {})
        new_entry = {
            "version_key": vk,
            "name_key": meta.get("name_key", vk),
            "family_key": meta.get("family_key", "unknown"),
            "aliases": [],
            "urls": [norm_url],
        }
        aliases_data[vk] = new_entry
        new_entries_created += 1

        version_key_to_entry_key[vk] = vk

    # Rebuild lookup after adding new entries
    version_key_to_entry_key, alias_to_entry_key = build_entry_lookup(aliases_data)

    # 2. Process shorthand_aliases
    for alias_key, vk in publishers.get("shorthand_aliases", {}).items():
        if not isinstance(alias_key, str) or not isinstance(vk, str):
            continue

        entry_key = find_matching_entry_key(
            vk, version_key_to_entry_key, alias_to_entry_key
        )

        if entry_key is None:
            unmatched_aliases.append((alias_key, vk))
            continue

        entry = aliases_data[entry_key]
        if "aliases" not in entry:
            entry["aliases"] = []

        if alias_key not in entry["aliases"] and alias_key != vk:
            entry["aliases"].append(alias_key)
            aliases_added += 1

    # Create new entries for unmatched aliases
    for alias_key, vk in publishers.get("shorthand_aliases", {}).items():
        if not isinstance(alias_key, str) or not isinstance(vk, str):
            continue

        entry_key = find_matching_entry_key(
            vk, version_key_to_entry_key, alias_to_entry_key
        )
        if entry_key is not None:
            continue

        if any(
            e.get("version_key") == vk
            for e in aliases_data.values()
            if isinstance(e, dict)
        ):
            continue

        new_entry = {
            "version_key": vk,
            "name_key": vk,
            "family_key": "unknown",
            "aliases": [alias_key],
            "urls": [],
        }
        aliases_data[vk] = new_entry
        new_entries_created += 1

    output_path = DRYRUN_PATH if args.dry_run else ALIASES_PATH

    comment_keys = sorted([k for k in aliases_data if k.startswith("_")])
    entry_keys = sorted(
        [k for k in aliases_data if not k.startswith("_")],
        key=lambda x: x.lower(),
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("{\n")

        for ck in comment_keys:
            f.write(f'  "{ck}": {json.dumps(aliases_data[ck])}')
            f.write(",")
            f.write("\n")

        f.write("\n")

        for i, ek in enumerate(entry_keys):
            is_last = i == len(entry_keys) - 1
            entry_str = format_entry_with_multiline_arrays(
                ek, aliases_data[ek], is_last
            )
            f.write(entry_str)
            f.write("\n\n")

        f.write("}\n")

    print("\nMigration summary:")
    print(f"  URLs added              : {urls_added}")
    print(f"  Shorthand aliases added : {aliases_added}")
    print(f"  New entries created     : {new_entries_created}")
    print(f"  Unmatched URLs          : {len(unmatched_urls)}")
    print(f"  Unmatched aliases       : {len(unmatched_aliases)}")

    if unmatched_urls:
        print("\nUnmatched URLs (no matching alias entry):")
        for url, vk in unmatched_urls[:10]:
            print(f"  {url} -> {vk}")
        if len(unmatched_urls) > 10:
            print(f"  ... and {len(unmatched_urls) - 10} more")

    if unmatched_aliases:
        print("\nUnmatched aliases (no matching alias entry):")
        for alias, vk in unmatched_aliases[:10]:
            print(f"  {alias} -> {vk}")
        if len(unmatched_aliases) > 10:
            print(f"  ... and {len(unmatched_aliases) - 10} more")

    if args.dry_run:
        print(f"\nDry-run output written to: {output_path}")
        print("Review the file, then run without --dry-run to apply.")
    else:
        print(f"\nMigration completed. Output written to: {output_path}")


if __name__ == "__main__":
    main()
