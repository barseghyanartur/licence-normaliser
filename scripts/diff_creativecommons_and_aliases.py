#!/usr/bin/env python3
"""Compare creativecommons.json with aliases.json to find missing CC licenses.

Run with --dry-run first to review what would be added.

The script:
- Matches licenses by entry key OR version_key OR aliases list
- Is interactive - prompts for each missing license
- Adds entries in alphabetical order
- Idempotent - running multiple times adds nothing new

::

    # Dry-run: shows what would be added
    uv run python scripts/diff_creativecommons_and_aliases.py --dry-run

    # Interactive mode
    uv run python scripts/diff_creativecommons_and_aliases.py
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "src" / "licence_normaliser" / "data"

ALIASES_PATH = DATA_DIR / "aliases" / "aliases.json"
CC_PATH = DATA_DIR / "creativecommons" / "creativecommons.json"
DRYRUN_PATH = DATA_DIR / "aliases" / "aliases.dryrun.json"


def normalise_key(key: str) -> str:
    """Convert cc-by-nc-nd-3.0 -> cc by-nc-nd 3.0 (entry key format)."""
    return key.replace("-", " ")


def build_lookup_tables(aliases_data: dict) -> tuple[dict, dict, dict]:
    """Build lookup tables from aliases.json."""
    version_key_to_entry: dict[str, str] = {}
    alias_to_entry: dict[str, str] = {}
    entry_key_exists: dict[str, bool] = {}

    for entry_key, meta in aliases_data.items():
        if entry_key.startswith("_") or not isinstance(meta, dict):
            continue

        entry_key_exists[entry_key] = True

        vk = meta.get("version_key")
        if vk:
            version_key_to_entry[vk] = entry_key

        for alias in meta.get("aliases", []):
            alias_to_entry[alias] = entry_key

    return version_key_to_entry, alias_to_entry, entry_key_exists


def find_matching_entry(
    cc_key: str,
    version_key_to_entry: dict[str, str],
    alias_to_entry: dict[str, str],
    entry_key_exists: dict[str, bool],
) -> str | None:
    """Find matching entry key in aliases for a CC license key."""
    entry_key = normalise_key(cc_key)
    if entry_key in entry_key_exists:
        return entry_key

    if cc_key in version_key_to_entry:
        return version_key_to_entry[cc_key]

    if cc_key in alias_to_entry:
        return alias_to_entry[cc_key]

    return None


def load_cc_licenses() -> list[dict]:
    """Load CC licenses from creativecommons.json."""
    with open(CC_PATH, encoding="utf-8") as f:
        return json.load(f)


def create_new_entry(
    cc_license: dict, existing_entry_key: str | None, aliases_data: dict
) -> dict:
    """Create a new aliases entry for a CC license."""
    cc_key = cc_license["license_key"]
    url = cc_license.get("url", "")

    # Derive name_key from cc_key (e.g., cc-by-nc-nd-3.0 -> cc-by-nc-nd)
    # Extract base name before version
    parts = cc_key.replace("cc-", "").split("-")
    if parts[-1].replace(".", "").replace("igo", "").isdigit() or parts[-1] in ("igo",):
        # Remove version suffix
        base_parts = parts[:-1]
    else:
        base_parts = parts
    name_key = "cc-" + "-".join(base_parts)

    new_entry = {
        "version_key": cc_key,
        "name_key": name_key,
        "family_key": "cc",
        "aliases": [cc_key],
        "urls": [url] if url else [],
    }

    return new_entry


def format_entry(key: str, data: dict, is_last: bool) -> str:
    """Format entry with multiline arrays."""
    lines = [f'  "{key}": {{']

    field_order = ["version_key", "name_key", "family_key", "aliases", "urls"]

    fields_to_write = [fn for fn in field_order if fn in data]
    fields_to_write.extend(fn for fn in data if fn not in field_order)

    for i, field_name in enumerate(fields_to_write):
        is_field_last = i == len(fields_to_write) - 1
        value = data[field_name]

        if isinstance(value, list):
            if not value:
                lines.append(
                    f'    "{field_name}": []'
                    if is_field_last
                    else f'    "{field_name}": [],'
                )
            else:
                lines.append(f'    "{field_name}": [')
                for j, item in enumerate(value):
                    is_last_item = j == len(value) - 1
                    suffix = "" if is_last_item else ","
                    if isinstance(item, str):
                        lines.append(f'      "{item}"{suffix}')
                    else:
                        lines.append(f"      {item}{suffix}")
                lines.append("    ]" if is_field_last else "    ],")
        else:
            suffix = "" if is_field_last else ","
            if isinstance(value, str):
                lines.append(f'    "{field_name}": "{value}"{suffix}')
            else:
                lines.append(f"    {field_name}: {value}{suffix}")

    lines.append("  }")
    result = "\n".join(lines)
    if not is_last:
        result += ","

    return result


def write_aliases(
    aliases_data: dict,
    output_path: Path,
) -> None:
    """Write aliases.json preserving format."""
    comment_keys = sorted([k for k in aliases_data if k.startswith("_")])
    entry_keys = sorted(
        [k for k in aliases_data if not k.startswith("_")],
        key=lambda x: x.lower(),
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("{\n")

        for ck in comment_keys:
            f.write(f'  "{ck}": {json.dumps(aliases_data[ck])}')
            f.write(",\n")

        f.write("\n")

        for i, ek in enumerate(entry_keys):
            is_last = i == len(entry_keys) - 1
            entry_str = format_entry(ek, aliases_data[ek], is_last)
            f.write(entry_str)
            f.write("\n\n")

        f.write("}\n")


def interactive_add(
    missing: list[tuple[dict, str]],
    aliases_data: dict,
    dry_run: bool,
) -> list[tuple[dict, str]]:
    """Interactive prompt for each missing license."""
    if not missing:
        print("\nNo missing licenses found!")
        return []

    print("\n" + "=" * 60)
    print("Missing Creative Commons Licenses in Aliases")
    print("=" * 60)

    to_add: list[tuple[dict, str]] = []

    for i, (cc_license, _) in enumerate(missing):
        cc_key = cc_license["license_key"]
        url = cc_license.get("url", "")
        print(f"\n[{i + 1}/{len(missing)}] License: {cc_key}")
        print(f"    URL: {url}")

        while True:
            response = (
                input("    Add to aliases? [y]es/[n]o/[a]ll/[q]uit: ").strip().lower()
            )
            if response in ("y", ""):
                to_add.append((cc_license, cc_key))
                break
            elif response == "n":
                break
            elif response == "a":
                to_add.extend(missing[i:])
                break
            elif response == "q":
                print("\nQuitting...")
                return to_add
            else:
                print("    Please enter: y (yes), n (no), a (all), or q (quit)")

    return to_add


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare creativecommons.json with aliases.json"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Write to aliases.dryrun.json instead of aliases.json",
    )
    args = parser.parse_args()

    with open(ALIASES_PATH, encoding="utf-8") as f:
        aliases_content = f.read()

    with open(CC_PATH, encoding="utf-8") as f:
        cc_licenses = json.load(f)

    aliases_data: dict = json.loads(aliases_content)

    version_key_to_entry, alias_to_entry, entry_key_exists = build_lookup_tables(
        aliases_data
    )

    missing: list[tuple[dict, str]] = []

    for cc_license in cc_licenses:
        cc_key = cc_license["license_key"]
        entry_key = find_matching_entry(
            cc_key, version_key_to_entry, alias_to_entry, entry_key_exists
        )
        if entry_key is None:
            missing.append((cc_license, cc_key))

    print(f"\nCC licenses in creativecommons.json: {len(cc_licenses)}")
    print(f"Missing from aliases.json: {len(missing)}")

    if missing:
        print("\nMissing licenses:")
        for cc_license, _ in missing:
            print(f"  {cc_license['license_key']}")

    if args.dry_run:
        print("\nDry-run mode - no changes will be made")
        print("Run without --dry-run to add missing entries")

    if not args.dry_run:
        to_add = interactive_add(missing, aliases_data, args.dry_run)

        for cc_license, cc_key in to_add:
            entry_key = normalise_key(cc_key)
            new_entry = create_new_entry(cc_license, entry_key, aliases_data)
            aliases_data[entry_key] = new_entry
            print(f"\nAdded: {entry_key}")

        if to_add:
            output_path = DRYRUN_PATH if args.dry_run else ALIASES_PATH
            write_aliases(aliases_data, output_path)
            print(f"\nWritten to: {output_path}")
    else:
        if missing:
            print(f"\nDry-run: would add {len(missing)} entries")
            print("Run without --dry-run to add them interactively")


if __name__ == "__main__":
    main()
