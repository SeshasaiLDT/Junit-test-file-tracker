#!/usr/bin/env python3
"""
scan_java_files_grouped.py

Recursively find all *.java files beneath a root directory
and write their metadata to a JSON file grouped by:
  - client or service
  - subfolders (e.g., client/checkout)

Usage:
    python scan_java_files_grouped.py /path/to/project_root output.json
"""

import sys
import json
from pathlib import Path
from collections import defaultdict


def group_java_files(root: Path) -> dict:
    grouped = {"client": defaultdict(list), "service": defaultdict(list)}

    for p in root.rglob("*.java"):
        if not p.is_file():
            continue

        rel_path = p.relative_to(root).as_posix()
        path_parts = rel_path.split("/")

        if not path_parts:
            continue

        top_level = path_parts[0]  # "client" or "service"
        if top_level not in grouped:
            continue

        # Use last folder before the .java file as the grouping key
        parent_dir = p.parent.name
        subfolder_key = f"{top_level}/{parent_dir}"

        grouped[top_level][subfolder_key].append({
            "file": p.name,
            "path": rel_path,
            "has_test": False,
            "has_doc": False,
            "ready_approval": False
        })

    # convert defaultdicts to regular dicts
    return {key: dict(value) for key, value in grouped.items()}



def main():
    if len(sys.argv) != 3:
        print("Usage: python scan_java_files_grouped.py <root_folder> <output_json>")
        sys.exit(1)

    root = Path(sys.argv[1]).resolve()
    output_file = Path(sys.argv[2]).resolve()

    if not root.is_dir():
        print(f"Error: '{root}' is not a directory.")
        sys.exit(1)

    grouped_data = group_java_files(root)

    with output_file.open("w", encoding="utf-8") as f:
        json.dump(grouped_data, f, indent=2)

    print(f"Grouped Java file metadata written to {output_file}")


if __name__ == "__main__":
    main()
