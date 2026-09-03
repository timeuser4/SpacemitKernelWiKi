#!/usr/bin/env python3
"""Search the sourced SpacemiT K-series Wiki reference pages."""

from __future__ import annotations

import argparse
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("terms", nargs="+", help="case-insensitive terms; all must match")
    parser.add_argument("--context", type=int, default=2, help="lines before and after each match")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    needles = [term.casefold() for term in args.terms]
    found = 0

    for path in sorted((root / "references").glob("*.md")):
        lines = path.read_text(encoding="utf-8").splitlines()
        matching = [
            index
            for index, line in enumerate(lines)
            if all(needle in line.casefold() for needle in needles)
        ]
        for index in matching:
            found += 1
            begin = max(0, index - args.context)
            end = min(len(lines), index + args.context + 1)
            print(f"{path.relative_to(root)}:{index + 1}")
            for line_number in range(begin, end):
                marker = ">" if line_number == index else " "
                print(f"{marker} {line_number + 1:4}: {lines[line_number]}")
            print()

    return 0 if found else 1


if __name__ == "__main__":
    raise SystemExit(main())
