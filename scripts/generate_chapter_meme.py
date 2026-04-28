"""Render a single chapter meme to a PNG via the memegen.link API.

Usage:
    python scripts/generate_chapter_meme.py \
        --template fine \
        --line "" --line "MY CODE IS ON FIRE BUT THIS IS FINE" \
        --out graphics/memes/debugging.png

The chapter-meme Quarto shortcode invokes this script per chapter; the
editorial content (template id and lines of text) lives in each chapter's
YAML frontmatter, not here.

The script hits https://api.memegen.link/ using the path-style form
(``/images/<template>/<line-1>/<line-2>.png``). The query-parameter form
``?text[]=...`` is documented but does not actually populate captions on
the image endpoint -- see https://github.com/jacebrowning/memegen/issues/993.
Each line is encoded into a path segment per memegen's rules: ``_`` for
space, ``__`` for a literal underscore, ``--`` for a literal dash, and
``~q``/``~s``/``~h``/etc. for reserved URL characters.

Before fetching the image, the script queries
``https://api.memegen.link/templates/<template>`` to read the template's
``lines`` count and rejects any chapter that supplies more lines than the
template has caption boxes -- otherwise memegen silently truncates and the
chapter loses captions.

Captions are sized and aligned by memegen against each template's
authored text-box geometry -- there is no ``fontsize`` knob.
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request


MEMEGEN_BASE = "https://api.memegen.link/images"
TEMPLATES_BASE = "https://api.memegen.link/templates"
USER_AGENT = "info-missing-manual chapter-meme/1.0"
TIMEOUT_SECONDS = 30


# memegen's path-encoding table. Order matters: literal `_` and `-` are
# escaped to `__` / `--` *before* spaces collapse to `_`. The double-quote
# rule is memegen-specific (`"` -> `''`).
_MEMEGEN_ESCAPES: list[tuple[str, str]] = [
    ("_", "__"),
    ("-", "--"),
    ("\n", "~n"),
    ("?", "~q"),
    ("&", "~a"),
    ("%", "~p"),
    ("#", "~h"),
    ("/", "~s"),
    ("\\", "~b"),
    ("<", "~l"),
    (">", "~g"),
    ('"', "''"),
    (" ", "_"),
]


def escape_path_segment(text: str) -> str:
    """Encode one caption line into a memegen URL path segment.

    Empty input becomes ``_`` so the line still appears as a path segment
    (rather than collapsing into ``//``) and renders as a blank caption.
    """
    if text == "":
        return "_"
    out = text
    for src, dst in _MEMEGEN_ESCAPES:
        out = out.replace(src, dst)
    # Percent-encode anything still URL-unsafe (backticks, apostrophes,
    # parens, commas, etc.) while preserving memegen's own escape syntax:
    # `_`, `-`, `~`, `'` are the bytes that appear in the table above.
    return urllib.parse.quote(out, safe="_-~'")


def build_url(template: str, lines: list[str], width: int, font: str) -> str:
    safe_template = urllib.parse.quote(template, safe="")
    query = urllib.parse.urlencode([("width", str(width)), ("font", font)])
    if not lines:
        return f"{MEMEGEN_BASE}/{safe_template}.png?{query}"
    segments = "/".join(escape_path_segment(line) for line in lines)
    return f"{MEMEGEN_BASE}/{safe_template}/{segments}.png?{query}"


def fetch_template_line_count(template: str) -> int:
    """Return the number of caption boxes the template defines.

    Raises ``urllib.error.HTTPError`` (404 = bogus template id) or
    ``urllib.error.URLError`` / ``TimeoutError`` if the API is unreachable.
    """
    url = f"{TEMPLATES_BASE}/{urllib.parse.quote(template, safe='')}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        payload = json.loads(resp.read())
    return int(payload["lines"])


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
    parser.add_argument(
        "--skip-template-check",
        action="store_true",
        help="skip the line-count validation against /templates/<id> "
             "(use only when the templates endpoint is unreachable)",
    )
    args = parser.parse_args()

    expected: int | None = None
    if not args.skip_template_check:
        try:
            expected = fetch_template_line_count(args.template)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                sys.stderr.write(
                    f"chapter-meme: template '{args.template}' not found at "
                    f"{TEMPLATES_BASE}/. Check the meme.template id in the "
                    f"chapter frontmatter.\n"
                )
                return 1
            sys.stderr.write(
                f"chapter-meme: HTTP {exc.code} fetching template metadata "
                f"for '{args.template}': {exc}\n"
            )
            return 1
        except (urllib.error.URLError, TimeoutError) as exc:
            sys.stderr.write(
                f"chapter-meme: cannot reach memegen template API "
                f"({TEMPLATES_BASE}): {exc}. Re-run with "
                f"--skip-template-check to bypass validation.\n"
            )
            return 1

    if expected is not None and len(args.line) > expected:
        sys.stderr.write(
            f"chapter-meme: template '{args.template}' supports {expected} "
            f"caption line(s) but this chapter supplies {len(args.line)}. "
            f"Trim meme.lines in the chapter frontmatter or pick a template "
            f"with more boxes.\n"
        )
        return 1

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
