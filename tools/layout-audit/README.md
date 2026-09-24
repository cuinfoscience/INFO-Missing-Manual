# layout-audit

Checks a rendered copy of the book in a real browser, for layout questions that the HTML alone cannot answer. It serves `book/` on `127.0.0.1` and never touches the network.

```bash
quarto render --to html                                         # the audit reads book/
tools/shots/.venv/bin/python tools/layout-audit/audit.py toc     # TOC showing? meme displayed?
tools/shots/.venv/bin/python tools/layout-audit/audit.py column  # column widths in CSS px
```

It borrows the screenshot toolkit's Python (Playwright) and its pinned Chrome for Testing, so run `bash tools/shots/bootstrap.sh` once first. `--book <dir>` audits a render somewhere other than `book/`.

## `toc`: is the table of contents showing?

For every page at each window size (`--sizes`, default a phone and three desktop sizes), it reports:

- whether the right-hand table of contents is visible when the page loads. Quarto collapses the TOC behind an "On this page" toggle whenever margin content (such as a chapter meme) would overlap it; the check looks for that toggle and confirms the first TOC link is the element actually on top at its position. It is skipped below 992 px, where Quarto doesn't show the right sidebar at all;
- whether the chapter meme is displayed, on pages whose markup includes one.

It exits 1 if any page fails either check, so it can serve as the acceptance test for a layout fix. `-v` names each collapsed page; `--json <file>` writes every page's result.

**September 2026 baseline** (issue [#30](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/30)): the TOC is collapsed at load on 37 of 41 pages at 1280×800, 1440×900, and 1920×1080. The four where it shows (the Introduction, the Conclusion, and both appendices) are the four without a meme. Memes display at every size.

## `column`: how wide are the columns?

Measures the width of a body paragraph and of the margin column on one page (`--page`, default the Command Line chapter) at several window widths (`--widths`).

**September 2026 measurements:** the body column is 678 CSS px in a 1280 px window and 699 px at 1440 and 1920; the margin column is 300 px. The screenshot toolkit's legibility check uses the body width (`BOOK_PX` in `tools/shots/lib/legibility.py`). Re-measure after changing the theme, the page layout, or `format: html` options, and update `BOOK_PX` if the column moved.
