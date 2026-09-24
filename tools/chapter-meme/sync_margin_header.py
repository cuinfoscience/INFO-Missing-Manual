#!/usr/bin/env python3
"""Put each chapter's meme at the top of the right sidebar, above the table of contents.

Quarto shows a page's `margin-header` above the table of contents in the right
sidebar, on screens 992 px and wider. Quarto reads that field before any filter
runs, so it can't be computed during a render (a Lua filter was tried). This
script writes it into each chapter's front matter from the chapter's `meme:`
block instead, and removes it from a chapter that no longer has a meme. The
`{{< chapter-meme >}}` shortcode keeps an inline copy for narrower screens,
where Quarto hides the sidebar. Issue #30 is why: a meme in the margin made
Quarto collapse the table of contents on every chapter that had one.

    python tools/chapter-meme/sync_margin_header.py           # rewrite the chapters
    python tools/chapter-meme/sync_margin_header.py --check   # exit 1 if any chapter is stale

Run it after adding, removing, or editing a chapter's `meme:` block. Never edit
the generated lines by hand. Standard library only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHAPTERS = ROOT / "chapters"

MARKER = "# margin-header: generated from meme: by tools/chapter-meme/sync_margin_header.py; do not edit"
ALT = re.compile(r"^  alt:\s*(.*?)\s*$")


def scalar(text: str) -> str:
    """A one-line YAML scalar's value: double-quoted, single-quoted, or plain."""
    if text.startswith('"'):
        return json.loads(text)                  # YAML double quotes escape like JSON here
    if text.startswith("'"):
        return text[1:-1].replace("''", "'")
    return text


def plain(markdown: str) -> str:
    """The alt text as the shortcode shows it: Pandoc's stringify drops code and emphasis marks."""
    return re.sub(r"[`*]", "", markdown)


def front_matter(lines: list[str]) -> tuple[int, int] | None:
    """(first, last) line indexes of the front matter's content, or None."""
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return 1, i
    return None


def meme_alt(block: list[str]) -> str | None:
    """The alt text of the `meme:` block, or None if there is no meme."""
    inside = False
    alt = None
    for line in block:
        if line.startswith("meme:"):
            inside = True
            continue
        if inside and line and not line.startswith(" "):
            break                                # the next top-level key ends the block
        if inside:
            m = ALT.match(line)
            if m:
                alt = scalar(m.group(1))
    if not inside:
        return None
    return alt if alt is not None else "Chapter meme"


def strip_generated(block: list[str], path: Path) -> list[str]:
    """The front matter without the generated margin-header (and complain about a hand-written one)."""
    out = []
    i = 0
    while i < len(block):
        if block[i] == MARKER:
            i += 1
            if i < len(block) and block[i].startswith("margin-header:"):
                i += 1
                while i < len(block) and block[i].startswith("  "):
                    i += 1
            continue
        if block[i].startswith("margin-header:"):
            sys.exit(f"{path.relative_to(ROOT)}: has a hand-written margin-header; "
                     "remove it, or remove its meme, before running this script")
        out.append(block[i])
        i += 1
    return out


def generated(slug: str, alt: str) -> list[str]:
    escaped = plain(alt).replace("\\", "\\\\").replace('"', '\\"')
    return [MARKER, "margin-header: |",
            f'  ![](/graphics/memes/{slug}.png){{.chapter-meme fig-alt="{escaped}"}}']


def sync(path: Path) -> str | None:
    """The chapter's new text, or None if it has no front matter."""
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    span = front_matter(lines)
    if span is None:
        return None
    first, last = span
    block = strip_generated(lines[first:last], path)
    alt = meme_alt(block)
    if alt is not None:
        block = block + generated(path.stem, alt)
    return "\n".join(lines[:first] + block + lines[last:])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--check", action="store_true", help="exit 1 if any chapter is out of date")
    args = parser.parse_args()
    stale, memes = [], 0
    for path in sorted(CHAPTERS.glob("*.qmd")):
        new = sync(path)
        if new is None:
            continue
        memes += MARKER in new
        if new != path.read_text(encoding="utf-8"):
            stale.append(path)
            if not args.check:
                path.write_text(new, encoding="utf-8")
    for path in stale:
        print(f"{'stale  ' if args.check else 'updated'}  {path.relative_to(ROOT)}")
    print(f"{memes} chapter memes in margin headers")
    return 1 if (args.check and stale) else 0


if __name__ == "__main__":
    sys.exit(main())
