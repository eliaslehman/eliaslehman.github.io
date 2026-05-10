#!/usr/bin/env python3
"""Validate food-for-thought.json for strict JSON and expected quote schema.

Usage:
  python3 validate-food-for-thought.py
  python3 validate-food-for-thought.py /path/to/food-for-thought.json

Exit codes:
  0 = valid
  1 = invalid

This script is intentionally dependency-free and safe to run from a desktop.
It checks:
  - strict JSON syntax
  - top-level array
  - non-empty array
  - every item is an object
  - required fields exist
  - field types match the expected schema
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, List


def _print_snippet(text: str, lineno: int, colno: int) -> None:
    lines = text.splitlines()
    if 1 <= lineno <= len(lines):
        line = lines[lineno - 1]
        print(f"  {lineno}: {line}")
        print(f"     {' ' * max(colno - 1, 0)}^")


def _load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise SystemExit(f"FAIL: file not found: {path}")
    except UnicodeDecodeError as exc:
        raise SystemExit(f"FAIL: file is not valid UTF-8: {exc}")


def _validate_schema(data: Any) -> List[str]:
    errors: List[str] = []

    if not isinstance(data, list):
        return ["Top-level JSON value must be an array."]

    if len(data) == 0:
        errors.append("Top-level array must not be empty.")
        return errors

    for i, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            errors.append(f"Item {i}: expected an object, got {type(item).__name__}.")
            continue

        required_fields = ("author", "work", "section", "quote")
        for field in required_fields:
            if field not in item:
                errors.append(f"Item {i}: missing required field '{field}'.")

        if "author" in item and not isinstance(item["author"], str):
            errors.append(f"Item {i}: 'author' must be a string.")
        if "work" in item and not isinstance(item["work"], str):
            errors.append(f"Item {i}: 'work' must be a string.")
        if "section" in item and not (isinstance(item["section"], str) or item["section"] is None):
            errors.append(f"Item {i}: 'section' must be a string or null.")
        if "quote" in item and not isinstance(item["quote"], str):
            errors.append(f"Item {i}: 'quote' must be a string.")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate food-for-thought.json as strict JSON and check its quote schema."
    )
    default_path = Path(__file__).with_name("food-for-thought.json")
    parser.add_argument(
        "json_file",
        nargs="?",
        default=str(default_path),
        help=f"Path to the JSON file (default: {default_path.name} next to this script)",
    )
    args = parser.parse_args()

    path = Path(args.json_file).expanduser().resolve()
    text = _load_text(path)

    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        print(f"FAIL: invalid JSON in {path.name}")
        print(f"  {exc.msg}")
        print(f"  Line {exc.lineno}, column {exc.colno}")
        _print_snippet(text, exc.lineno, exc.colno)
        return 1

    errors = _validate_schema(data)
    if errors:
        print(f"FAIL: schema validation failed for {path.name}")
        for error in errors:
            print(f"  - {error}")
        return 1

    print(f"PASS: {path.name} is valid strict JSON and matches the expected quote schema.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
