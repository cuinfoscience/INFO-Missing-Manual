#!/usr/bin/env python3
"""Keep the chapter dropdown in every issue form in step with the book.

Each form under .github/ISSUE_TEMPLATE/ has a "Which chapter?" dropdown. The
options live between two marker comments:

    # BEGIN chapters (...)
    # END chapters

This script rebuilds that block from the chapter order in _quarto.yml and the
H1 title of each chapter file, numbered the way the rendered book numbers them
(the Introduction is Chapter 1). Run it after adding, removing, renaming, or
reordering a chapter.

    python scripts/sync_issue_chapters.py           # rewrite the forms
    python scripts/sync_issue_chapters.py --check   # exit 1 if any form is stale

Standard library only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FORMS_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
CONFIG = ROOT / "_quarto.yml"

BEGIN = re.compile(r"^(\s*)# BEGIN chapters\b")
END = re.compile(r"^\s*# END chapters\b")
QMD_ITEM = re.compile(r"^\s*-\s+([\w./-]+\.qmd)\s*$")
H1 = re.compile(r"^#\s+(.*?)\s*(\{#[^}]*\})?\s*$")


def h1_title(path: str) -> str:
    for line in (ROOT / path).read_text(encoding="utf-8").splitlines():
        m = H1.match(line)
        if m:
            return m.group(1).strip()
    sys.exit(f"{path}: no H1 heading found")


def chapter_options() -> list[str]:
    """Numbered chapter titles, then appendices, in _quarto.yml order."""
    options: list[str] = []
    mode = None
    number = 0
    for line in CONFIG.read_text(encoding="utf-8").splitlines():
        if line == "  chapters:":
            mode = "chapter"
            continue
        if line == "  appendices:":
            mode = "appendix"
            continue
        if line and not line.startswith(" "):
            mode = None  # a new top-level key ends the book block
        m = QMD_ITEM.match(line)
        if not m or mode is None:
            continue
        title = h1_title(m.group(1))
        if mode == "chapter":
            number += 1
            options.append(f"Ch. {number} — {title}")
        else:
            options.append(f"Appendix — {title}")
    if not options:
        sys.exit("no chapters found in _quarto.yml; is the file shape unchanged?")
    return options


def sync_form(path: Path, options: list[str], check: bool) -> bool:
    """Rewrite the marker block in one form. Returns True if it changed."""
    lines = path.read_text(encoding="utf-8").split("\n")
    out: list[str] = []
    i = 0
    found = False
    changed = False
    while i < len(lines):
        m = BEGIN.match(lines[i])
        if not m:
            out.append(lines[i])
            i += 1
            continue
        found = True
        indent = m.group(1)
        out.append(lines[i])
        i += 1
        old: list[str] = []
        while i < len(lines) and not END.match(lines[i]):
            old.append(lines[i])
            i += 1
        if i >= len(lines):
            sys.exit(f"{path}: '# BEGIN chapters' without matching '# END chapters'")
        new = [f'{indent}- "{o.replace(chr(34), chr(92) + chr(34))}"' for o in options]
        if old != new:
            changed = True
        out.extend(new)
    if not found:
        return False
    if changed and not check:
        path.write_text("\n".join(out), encoding="utf-8")
    return changed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="report stale forms without writing")
    args = parser.parse_args()

    options = chapter_options()
    stale = []
    for form in sorted(FORMS_DIR.glob("*.yml")):
        if sync_form(form, options, args.check):
            stale.append(form.name)
            print(("stale" if args.check else "updated") + f"  {form.relative_to(ROOT)}")
        else:
            print(f"ok       {form.relative_to(ROOT)}")
    print(f"{len(options)} chapter options")
    if args.check and stale:
        sys.exit(f"out of date: {', '.join(stale)} (run without --check to fix)")


if __name__ == "__main__":
    main()
