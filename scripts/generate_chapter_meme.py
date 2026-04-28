"""Render a single chapter meme to a PNG via the memegen.link API.

Usage:
    python scripts/generate_chapter_meme.py \
        --template fine \
        --line "" --line "MY CODE IS ON FIRE BUT THIS IS FINE" \
        --out graphics/memes/debugging.png

The chapter-meme Quarto shortcode invokes this script per chapter; the
editorial content (template id and lines of text) lives in each chapter's
YAML frontmatter, not here.

The script hits https://api.memegen.link/ using the query-parameter form
(``?text[]=line1&text[]=line2``) so memegen's path-style escaping rules do
not need to be reimplemented here. Captions are sized and aligned by
memegen against each template's authored text-box geometry — there is no
``fontsize`` knob.
"""
from __future__ import annotations

import argparse
import sys
import urllib.error
import urllib.parse
import urllib.request


MEMEGEN_BASE = "https://api.memegen.link/images"
USER_AGENT = "info-missing-manual chapter-meme/1.0"
TIMEOUT_SECONDS = 30


def build_url(template: str, lines: list[str], width: int, font: str) -> str:
    params: list[tuple[str, str]] = [("text[]", line) for line in lines]
    params.append(("width", str(width)))
    params.append(("font", font))
    query = urllib.parse.urlencode(params)
    return f"{MEMEGEN_BASE}/{urllib.parse.quote(template, safe='')}.png?{query}"


def fetch_png(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        return resp.read()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--template", required=True, help="memegen template id")
    parser.add_argument(
        "--line",
        action="append",
        default=[],
        help="positional line of meme text (repeatable, in template order)",
    )
    parser.add_argument("--out", required=True, help="output PNG path")
    parser.add_argument(
        "--width",
        type=int,
        default=1000,
        help="output width in pixels (default 1000)",
    )
    parser.add_argument(
        "--font",
        default="impact",
        help="memegen font id (default 'impact')",
    )
    args = parser.parse_args()

    url = build_url(args.template, args.line, args.width, args.font)
    try:
        png_bytes = fetch_png(url)
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as exc:
        sys.stderr.write(f"chapter-meme: failed to fetch {url}: {exc}\n")
        return 1

    with open(args.out, "wb") as f:
        f.write(png_bytes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
