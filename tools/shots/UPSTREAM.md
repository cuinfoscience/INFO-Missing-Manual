# Where tools/shots comes from

**Source:** [cuinfoscience/Web-Data-Science-Book](https://github.com/cuinfoscience/Web-Data-Science-Book), `tools/shots/` at commit `3de5578ab591a608bf81657c70ce546510415e11` (merged 2026-09-24), milestones M1–M3. That book's recipes were not copied.

The first commit that added this folder is the upstream code, byte for byte; everything since is a local change. To see the whole difference, compare this folder with the source commit, or run `git diff <first commit>..HEAD -- tools/shots`.

## Local changes

**For this book's layout and identity**

| Where | Upstream | Here | Why |
|---|---|---|---|
| `lib/env.py` `IMAGES` | `images/<chapter>/` | `graphics/<chapter>/` | the book keeps figures in `graphics/` |
| `lib/recipes.py` `chapters()`, `load()` | recipes named `ch-NN.yml`; chapter file found by `ch-NN-*.qmd` | recipes named for the chapter slug (`jupyter.yml`); chapter file `chapters/<slug>.qmd` | the book's chapters are slugs, not numbers |
| `lib/recipes.py` `DEFAULTS["user_agent"]` | `Web Data Science/v1 brian.keegan@colorado.edu` | `Missing Manual/v1 brian.keegan@colorado.edu` | this book's name, with the same contact address; see `docs/decisions.md`. The pilot's three figures were taken with an earlier string that gave the repository's link instead, and their provenance records it |
| `lib/legibility.py` `BOOK_PX` | 778 | 678 | measured: the body column in a 1280-pixel window (`tools/layout-audit/`) |
| `lib/annotate.py` `BOOK_WIDTH_IN` | `778 / 96` | `legibility.BOOK_PX / 96` | one number, kept in one place |
| `lib/legibility.py` `targets()` | the book target for chapters named `ch-*` | the book target for every recipe but `course` | chapter names are slugs |
| `shots.py` `figure_block()` | `images/<chapter>/<file>` | `/graphics/<chapter>/<file>`, and an error for a path without the leading slash | this book's figure paths need the slash (`AGENTS.md`, "Add a figure") |
| `shots.py` `clean` | folders named `ch-*` and `course` | every folder in `out/` | chapter names are slugs |
| `lib/sheet.py`, `lib/provenance.py`, `lib/capture.py`, `lib/guards.py` | docstrings name `images/` and `ch-05` | `graphics/`, `jupyter` | |
| `selftest.py` | expected messages hard-code 800×600, 78%, and the User-Agent | built from the toolkit's constants | the tests follow this book's settings |

**Infobars (requested by the maintainer, 2026-09-24)**

- `lib/headed.py` passes `--disable-infobars` itself. Upstream relied on Playwright's default argument list, which carries the flag today to hide Chrome for Testing's notice in persistent contexts. A 56-DIP notice slipping through was the reason for this change.
- Playwright's `ignore_default_args` filters *every* argument, not only its defaults: listing `--disable-infobars` there removes the toolkit's own copy too (the selftest caught this). So the flag is dropped only for a figure that expects an infobar (`expect: {infobar: true}`, a new key).
- `lib/guards.py` has `MAX_BARS` (100 DIPs) and `bars_problems()`. A headed take measures the browser's bars above the page, records them as `bars` in its log, and fails if they are taller than the limit, or, with `expect: {infobar: true}`, if they aren't.
- `lib/browser.py` passes the same flag to headless Chrome, which draws no bars, so neither mode depends on Playwright's defaults.
- `doctor` reads the bars back from a real headed window. `selftest` adds six checks: the guard's logic both ways, a headed take's recorded bars, Chrome's command line read back from `chrome://version` with and without the flag, and, where a window without the flag shows an infobar (as here), a live take that expects one.

**Size limits (requested by the maintainer, 2026-09-24)**

- `lib/legibility.py`: the default limit stays 800×600 (`SOFT_LIMIT`). A new tier, `RELAXED_LIMIT` (1024×768), allows a larger view when it reduces clutter, the recipe says why in `relaxed:` (a new key), and the text passes at every target. `size_report()` replaces `oversize()` and decides between nothing, a note, and a warning; `size_hint()` says what to try.
- `lib/legibility.py` `COLUMNS` and `book_px()`: a figure can be judged in one of Quarto's wider columns (`targets: {book: {column: page-inset-right}}`), measured in this book; `check` fails a figure whose chapter doesn't carry the matching class.
- `lib/recipes.py` validates `relaxed:` and the book target's `column`; both stay out of the recipe's hash, like `oversize:`.
- `selftest.py` adds six checks for the tiers, the wider column, and `check`'s column rule.

**A crop between two elements, for headless takes (the pilot, 2026-09-24)**

- `lib/crop.py`: `crop: {between: [A, B]}` crops from the top of the first element matching `A` to the bottom of the first matching `B`, across the width of both, with `pad` as for `selector`. The pilot needed it to show a code cell and the Markdown cell after it. Upstream implements `between` only for headed takes (`lib/headed.py`), although its recipe check accepts the key for any figure: a headless take with it fell through to the whole window, silently.
- `selftest.py` adds one check (a `between` crop of two marked elements, at its expected size), for 69 in all (upstream has 56).

**A hand capture's maker (2026-09-24)**

- `lib/provenance.py` `from_legacy()`: a `legacy:` block may say `by:`, who made the image ("hand capture by the maintainer"). Upstream always records "hand-run script, before tools/shots", which misdescribes a new hand capture.

**Pilot material, not in upstream:** the JupyterLab fixture in `fixtures/jupyter/`, the recipes, and "Patterns and pitfalls" in the README, which adds this book's lessons to upstream's.

## Worth offering upstream

These fix or extend behavior that *Web Data Science* shares:

1. The explicit `--disable-infobars`, the `ignore_default_args` pitfall, and the bars guard with its read-back tests.
2. The relaxed tier, if that book wants it; its column is wider (778), so a 1024-pixel figure keeps 76% of its text size there, against 66% here.
3. `figure_block()` accepting the leading slash, if that book's chapters ever move into a folder.
4. The headless `between` crop with its selftest check; at the least, a recipe check that rejects `between` on a headless figure instead of ignoring it.
5. The JupyterLab lessons in "Patterns and pitfalls" (saved layout and `?reset`, deferred navigation, hidden tabs, inner scrolling, the active cell's border, the file browser's selection, kernels that outlive captures), if that book ever captures JupyterLab.

## Syncing with upstream

1. Diff upstream's `tools/shots/` between the source commit above and its new head.
2. Apply each change here by hand, keeping the local changes listed above, and update this file's source commit and tables.
3. Run `tools/shots/run selftest` (every check must pass) and `tools/shots/run check`, then re-take one real figure before calling the sync done.
