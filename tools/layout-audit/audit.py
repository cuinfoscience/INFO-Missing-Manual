#!/usr/bin/env python3
"""Browser checks against a rendered copy of the book.

    tools/shots/.venv/bin/python tools/layout-audit/audit.py toc
    tools/shots/.venv/bin/python tools/layout-audit/audit.py column
    tools/shots/.venv/bin/python tools/layout-audit/audit.py widths

toc     On every page, at each window size: is the right-hand table of contents
        showing when the page loads, or has Quarto collapsed it behind its
        "On this page" toggle? And is the chapter meme displayed? Exits 1 if any
        page fails either check. (Issue #30.)
column  How wide the body column and the margin column are, in CSS pixels, at
        common window widths. The screenshot toolkit's legibility targets are
        set from the body width (tools/shots/lib/legibility.py, BOOK_PX).
widths  On every page, at each window width: are the body column, the table of
        contents, and the left navigation the same width as on every other page,
        and does the page fit the window without a sideways scroll? Exits 1 if
        any page differs or overflows. (styles/layout.css.)

Both read the rendered HTML in book/ (render first with `quarto render --to html`,
or pass --book), serve it on 127.0.0.1, and never touch the network. They use
the screenshot toolkit's Python and its Chrome for Testing, so run
`bash tools/shots/bootstrap.sh` once first.
"""
from __future__ import annotations

import argparse
import functools
import http.server
import json
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools" / "shots"))

# Quarto shows the right-hand sidebar (and so the table of contents) at 992 CSS
# pixels and wider; below that the TOC is not expected in the margin.
SIDEBAR_MIN_WIDTH = 992

TOC_JS = """() => {
  const toc = document.querySelector('#TOC');
  const link = toc && toc.querySelector('a.nav-link, a');
  // Quarto adds this toggle when it collapses the TOC to make room for margin content.
  const toggle = document.querySelector('#quarto-toc-toggle');
  let onTop = false;
  if (link) {
    const r = link.getBoundingClientRect();
    const hit = document.elementFromPoint(r.left + 4, r.top + r.height / 2);
    onTop = !!hit && toc.contains(hit);
  }
  const memes = [...document.querySelectorAll('img[src*="graphics/memes/"]')];
  return {
    has_toc: !!toc,
    toc_visible: onTop && !toggle,
    collapsed: !!toggle,
    has_meme: memes.length > 0,
    meme_visible: memes.some(i => { const r = i.getBoundingClientRect(); return r.width > 0 && r.height > 0; }),
  };
}"""

WIDTHS_JS = """() => {
  const w = sel => { const e = document.querySelector(sel); return e && e.offsetWidth ? Math.round(e.getBoundingClientRect().width) : null; };
  const main = document.querySelector('main.content');
  const para = main && [...main.querySelectorAll('p')].find(p => p.offsetWidth > 0 &&
      !p.closest('.column-margin, .callout, figure, [class*="column-page"], [class*="column-body-outset"], [class*="column-screen"]'));
  return {body: para ? Math.round(para.getBoundingClientRect().width) : null,
          toc: w('#quarto-margin-sidebar'), nav: w('#quarto-sidebar'),
          overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth};
}"""

COLUMN_JS = """() => {
  const main = document.querySelector('main.content') || document.querySelector('main');
  const para = [...main.querySelectorAll('p')].find(p => p.offsetWidth > 0 && !p.closest('.column-margin, .callout, figure'));
  const margin = [...document.querySelectorAll('.column-margin')].find(e => e.offsetWidth > 0);
  return {body: para ? Math.round(para.getBoundingClientRect().width) : null,
          margin: margin ? Math.round(margin.getBoundingClientRect().width) : null};
}"""


def parse_sizes(text):
    return [tuple(int(n) for n in s.split("x")) for s in text.split(",") if s]


def pages(book):
    """Every rendered chapter page, in a stable order."""
    found = [book / "index.html", *sorted((book / "chapters").glob("*.html")), book / "conclusion.html"]
    return [p.relative_to(book).as_posix() for p in found if p.exists()]


class Server:
    """Serve the rendered book on a free local port, in a background thread."""

    def __init__(self, book):
        handler = functools.partial(_QuietHandler, directory=str(book))
        self.httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        self.url = f"http://127.0.0.1:{self.httpd.server_address[1]}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def close(self):
        self.httpd.shutdown()


class _QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def browser(playwright):
    from lib.env import chrome_path   # the toolkit's pinned Chrome for Testing
    return playwright.chromium.launch(executable_path=chrome_path(), headless=True)


def cmd_toc(args, book):
    from playwright.sync_api import sync_playwright
    sizes = parse_sizes(args.sizes)
    paths = pages(book)
    report, failed = {}, False
    server = Server(book)
    try:
        with sync_playwright() as p:
            b = browser(p)
            for width, height in sizes:
                page = b.new_page(viewport={"width": width, "height": height})
                collapsed, no_meme = [], []
                for path in paths:
                    page.goto(f"{server.url}/{path}", wait_until="load")
                    page.wait_for_timeout(400)   # Quarto lays out the sidebar after load
                    r = page.evaluate(TOC_JS)
                    report.setdefault(path, {})[f"{width}x{height}"] = r
                    name = Path(path).stem
                    if width >= SIDEBAR_MIN_WIDTH and r["has_toc"] and not r["toc_visible"]:
                        collapsed.append(name)
                    if r["has_meme"] and not r["meme_visible"]:
                        no_meme.append(name)
                page.close()
                toc_note = (f"TOC collapsed on {len(collapsed)}/{len(paths)} pages"
                            if width >= SIDEBAR_MIN_WIDTH else "TOC not checked below 992 px")
                print(f"{width}x{height}: {toc_note}; meme hidden on {len(no_meme)} pages")
                if collapsed and args.verbose:
                    print("  collapsed: " + ", ".join(collapsed))
                if no_meme:
                    print("  meme hidden: " + ", ".join(no_meme))
                failed = failed or bool(collapsed or no_meme)
            b.close()
    finally:
        server.close()
    if args.json:
        Path(args.json).write_text(json.dumps(report, indent=1) + "\n")
    return 1 if failed else 0


def cmd_column(args, book):
    from playwright.sync_api import sync_playwright
    server = Server(book)
    try:
        with sync_playwright() as p:
            b = browser(p)
            for width in (int(w) for w in args.widths.split(",")):
                page = b.new_page(viewport={"width": width, "height": 900})
                page.goto(f"{server.url}/{args.page}", wait_until="load")
                print(f"{width} px window: " + json.dumps(page.evaluate(COLUMN_JS)))
                page.close()
            b.close()
    finally:
        server.close()
    return 0


def cmd_widths(args, book):
    from collections import Counter
    from playwright.sync_api import sync_playwright
    paths = pages(book)
    failed = False
    server = Server(book)
    try:
        with sync_playwright() as p:
            b = browser(p)
            for width in (int(w) for w in args.widths.split(",")):
                page = b.new_page(viewport={"width": width, "height": 900})
                rows = {}
                for path in paths:
                    page.goto(f"{server.url}/{path}", wait_until="load")
                    page.wait_for_timeout(300)
                    rows[path] = page.evaluate(WIDTHS_JS)
                page.close()
                line = [f"{width} px window:"]
                for key in ("body", "toc", "nav"):
                    counts = Counter(r[key] for r in rows.values())
                    usual = counts.most_common(1)[0][0]
                    odd = [Path(k).stem for k, r in rows.items() if r[key] != usual]
                    line.append(f"{key} {usual} px" + (f" (differs on {', '.join(odd)})" if odd else ""))
                    failed = failed or bool(odd)
                wide = [f"{Path(k).stem} (+{r['overflow']} px)" for k, r in rows.items() if r["overflow"] > 0]
                line.append("no page overflows" if not wide else "overflows: " + ", ".join(wide))
                failed = failed or bool(wide)
                print("  ".join(line))
            b.close()
    finally:
        server.close()
    return 1 if failed else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--book", default=str(ROOT / "book"), help="rendered HTML book (default: book/)")
    sub = parser.add_subparsers(dest="command", required=True)
    toc = sub.add_parser("toc", help="is the table of contents showing, and the meme displayed?")
    toc.add_argument("--sizes", default="390x844,1280x800,1440x900,1920x1080",
                     help="comma-separated WIDTHxHEIGHT window sizes (default: a phone and three desktops)")
    toc.add_argument("--json", help="also write every page's result to this file")
    toc.add_argument("-v", "--verbose", action="store_true", help="name every page whose TOC is collapsed")
    column = sub.add_parser("column", help="measure the body and margin columns")
    column.add_argument("--widths", default="1280,1440,1920", help="comma-separated window widths")
    column.add_argument("--page", default="chapters/terminal.html", help="page to measure, relative to the book")
    widths = sub.add_parser("widths", help="are the columns the same width on every page, with no sideways scroll?")
    widths.add_argument("--widths", default="1024,1280,1440,1920", help="comma-separated window widths")
    args = parser.parse_args()

    book = Path(args.book).resolve()
    if not (book / "index.html").exists():
        sys.exit(f"no rendered book at {book}; run `quarto render --to html` first, or pass --book")
    return {"toc": cmd_toc, "column": cmd_column, "widths": cmd_widths}[args.command](args, book)


if __name__ == "__main__":
    sys.exit(main())
