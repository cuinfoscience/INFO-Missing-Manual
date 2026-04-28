"""Render a single chapter meme to a PNG using memeplotlib.

Usage:
    python scripts/generate_chapter_meme.py \
        --template fine \
        --line "" --line "MY CODE IS ON FIRE BUT THIS IS FINE" \
        --out graphics/memes/debugging.png

The chapter-meme Quarto shortcode invokes this script per chapter; the
editorial content (template id and lines of text) lives in each chapter's
YAML frontmatter, not here.
"""
from __future__ import annotations

import argparse

import memeplotlib as memes


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--template", required=True, help="memegen template id"
    )
    parser.add_argument(
        "--line",
        action="append",
        default=[],
        help="positional line of meme text (repeatable, in template order)",
    )
    parser.add_argument(
        "--out", required=True, help="output PNG path"
    )
    args = parser.parse_args()
    memes.meme(args.template, *args.line, savefig=args.out, show=False)


if __name__ == "__main__":
    main()
