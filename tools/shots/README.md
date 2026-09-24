# tools/shots

Capture, check, and record the book's screenshots, so that every figure can be made again the same way and says where it came from.

The toolkit is ported from the companion book *Web Data Science* ([`tools/shots` there](https://github.com/cuinfoscience/Web-Data-Science-Book/tree/main/tools/shots)). [`UPSTREAM.md`](UPSTREAM.md) records the commit it came from and every local change. Before changing the toolkit or adding a screenshot, read:

- "Patterns and pitfalls" below: what earlier captures taught, as rules for writing a recipe;
- the plan for screenshots in this book, [`docs/plans/2026-09-24-screenshots.md`](../../docs/plans/2026-09-24-screenshots.md): which figures, in what order, and the decisions behind them;
- this book's [screenshot AAR](../../docs/aar/AAR_INFO-Missing-Manual_2026-09-24.md), on the pilot (the Jupyter chapter, from a local JupyterLab), and the upstream after-action reports whose lessons this port builds in: the [screenshot AAR](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/docs/aar/2026-09-24-screenshots.md) and the [toolkit sprint AAR](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/docs/aar/AAR_Web-Data-Science-Book_2026-09-24.md).

A **chapter** here is a chapter's slug: `jupyter` means `chapters/jupyter.qmd`, whose recipe is `recipes/jupyter.yml` and whose approved images go in `graphics/jupyter/`.

## Quick start

```bash
bash tools/shots/bootstrap.sh --headed --tex      # once per machine or container; safe to re-run
tools/shots/run doctor jupyter                    # every time, first: can this session capture?
bash tools/shots/fixtures/jupyter/start.sh        # this chapter captures a local JupyterLab
tools/shots/run capture jupyter                   # takes go to tools/shots/out/jupyter/<figure>/
tools/shots/run sheet jupyter                     # look at every take at the size it will be shown
tools/shots/run promote jupyter jupyterlab-overview   # copy the take into graphics/jupyter/, record it
bash tools/shots/fixtures/jupyter/stop.sh         # stop the fixture when the takes are done
tools/shots/run check                             # before a pull request
tools/shots/run selftest                          # after changing the toolkit
```

- **`bootstrap.sh`** installs what is missing; creates `tools/shots/.venv` with the pinned packages in `requirements.txt`; fetches Chrome for Testing at a pinned major version (154) through Selenium Manager; makes sure Chrome trusts a session proxy's certificate, if there is one; and installs fonts. `--headed` adds the virtual display (Xvfb), real input (xdotool), and screen grabs (ImageMagick) that headed figures need; `--tex` adds pdflatex with TikZ and pdftocairo, which draw markers. It never runs `playwright install` and never turns off certificate checks. It uses `apt-get`; on a Mac, install the equivalents yourself or capture in a Linux container.
- **`doctor`** answers whether capture works in this session. Don't reuse an earlier session's answer. It checks the proxy, the browser, a real headless capture of example.com, and a real headed one with DevTools open, including the height of the browser's bars (see "Headed figures"). It checks for TeX, and fails if a recipe has markers and TeX is missing. With a chapter, it makes one request to each host that chapter's recipes use, and reports a proxy refusal as a policy block, which you report rather than route around. For a chapter captured from a local fixture it warns `localhost: not reachable now`, fixture running or not, because it asks for `https://localhost/robots.txt`; ignore that warning, and check that the fixture answers instead (its `start.sh` waits until it does). Teaching `doctor` about fixtures is an open action in the [screenshot AAR](../../docs/aar/AAR_INFO-Missing-Manual_2026-09-24.md).

## The rules

- **Real or labeled.** A screenshot is a real capture of a real page or program. Diagrams and renders are welcome, marked with their `kind` (`capture`, `render`, `diagram`, `illustration`). Never rebuild a real site's or program's interface with invented content. The book's terminal figures are drawn, not captured (`tools/terminal-figures/`), and their captions say so.
- **One honest User-Agent** for every request: `Missing Manual/v1 (+https://github.com/cuinfoscience/INFO-Missing-Manual)`. It goes to Chrome as Chrome's own `--user-agent` flag, so the User-Agent Client Hints (`Sec-CH-UA-Platform` and the rest) name the system the capture runs on. (Playwright's `user_agent` option rewrites the hints too, and for a string that names no system it claims Windows.) Page loads on one host are 8–30 seconds apart.
- **Retries:** a 5xx or a dropped connection is retried three times, 30, 60, then 120 seconds apart. A block page, a 403, or a proxy refusal is not retried.
- **No logins, no credentials, no student names or work.** A page behind a login is captured by hand, by the maintainer, and recorded with `adopt`.
- **Dated captions.** A figure that shows things that change (counts, versions, live pages) says in its caption when it was captured, as in "in September 2026". `check` warns when a drifting figure's caption lacks the year.
- **Readable, and not crammed.** A figure shows **at most 800×600 CSS pixels** of the screen by default. It may show **up to 1024×768 when the larger view reduces clutter and its text still passes** the legibility check wherever it is shown; the recipe says why in `relaxed:`. See "Legibility".

## Patterns and pitfalls

What earlier captures taught, so you don't have to learn it again. Read this before writing a recipe. The full stories are in this book's [screenshot AAR](../../docs/aar/AAR_INFO-Missing-Manual_2026-09-24.md) and in *Web Data Science*'s [sprint AAR](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/docs/aar/AAR_Web-Data-Science-Book_2026-09-24.md).

**Choosing what to show**

- **Start from the sentence the figure supports,** and show the smallest part of the screen that makes its point. Crop before you reach for a bigger window.
- **Web apps rearrange themselves by width,** so look at the layout at the size you pick. At 680 px GitHub switches to its phone layout and moves the About sidebar below the files; at 800 px JupyterLab folds the kernel indicator into an overflow menu and wraps a DataFrame's dates. When the default window crams what the text describes, that is the case for `relaxed:` (up to 1024×768), and the reason names what the larger view shows.
- **Do the arithmetic for this book's 678-px column first.** The book shows a figure at 678 ÷ (its width in CSS px) of its on-screen size, and text must come out at 11 px or more. An 800-px-wide figure needs 13-px text on screen; a 1024-px figure needs 16.6 px in the body column, or 12 px in `column-page-inset-right` (954 px). JupyterLab's 13-px interface at 1024 px passes only in the wider column (it measured 12.1 px there).
- **A figure in a wider column covers the table of contents** while it is on screen, and Quarto folds the table of contents into its toggle until the reader scrolls past. Use a wider column only for a figure that needs the width.
- **Never put a screenshot in `.column-margin`.** It is illegible at 300 px, and margin content near the top of a chapter hides the table of contents at load.

**Getting a stable take**

- **Wait for selectors, not text,** in application interfaces. A text wait needs *visible* text and can match a hidden element first; the first JupyterLab trial timed out that way. Scope selectors to the visible instance: `.first` can land on a hidden tab.
- **Wait for the application's own deferred work before acting.** JupyterLab moves its file browser into the notebook's folder about a second after the notebook appears, and a click on "home" before that is silently undone. Wait for the state you expect (here, the `notebooks` breadcrumb), act, then wait for the result.
- **Applications remember state between captures.** JupyterLab restores its last layout from the server, so the second capture inherited the first one's folded sidebar and open tab. Its kernels outlive captures too, and the status bar counts them: an overview taken after the `pandas-basics` capture showed two. Start every capture from a known state (`?reset` for JupyterLab's layout; a fresh start of the fixture for its kernels; the toolkit already gives each take a fresh browser context), and run the whole recipe file, not just one figure, before promoting.
- **Some applications scroll inside the page** (JupyterLab's notebook does), so content below the fold is not on screen to crop. Use a window taller than the crop; only the crop counts toward the size limits.
- **Interface state leaks into crops:** the active cell's blue border and toolbar, a selected file, a hover style, the selected URL in a headed take's address bar. JupyterLab selects the first item whenever its file browser changes folder, and only Ctrl+Space (which toggles the focused item) clears it. Move focus or selection outside the crop (click another cell), crop headed takes to `{content: true}`, and check the crop's edge rows for stray borders. A negative `pad` trims a pixel. A border cut in half is one or two pixels tall and easy to miss by eye, so count the colored pixels along each edge. The pilot's first four takes of `jupyter-cell-types` scored 20 or more on one edge, and the take it promoted scored 0 on all four. A figure whose subject really does run off the edge in color scores too, so treat a count as a reason to look, not a verdict:

```bash
tools/shots/.venv/bin/python - tools/shots/out/<chapter>/<figure>/*.png <<'EOF'
import sys
from PIL import Image
for path in sys.argv[1:]:
    im = Image.open(path).convert("RGB")
    w, h = im.size
    edges = {"top": [(x, 0) for x in range(w)], "bottom": [(x, h - 1) for x in range(w)],
             "left": [(0, y) for y in range(h)], "right": [(w - 1, y) for y in range(h)]}
    print(path, {k: sum(max(p) - min(p) > 60 for p in map(im.getpixel, v)) for k, v in edges.items()})
EOF
```

- **For a span of elements** (a code cell through the Markdown cell after it), use `crop: {between: [A, B]}`; Playwright's `>> nth=1` picks a second match.
- **Capture software from a pinned local fixture,** not from someone's machine or a live account: pinned versions, synthetic data, a scratch copy of the project, a fixed port, settings that silence first-run prompts, and a stop script. [`fixtures/jupyter/`](fixtures/jupyter/) is the model.

**Headed captures**

- **Chrome for Testing shows a 56-px notice** unless `--disable-infobars` is passed, and the toolkit passes it itself. Never list that flag in Playwright's `ignore_default_args`: it strips the toolkit's copy too. The bars guard fails any take whose browser bars exceed 100 DIPs.
- **The address bar's URL is selected** in every headed take; crop to the content unless the address bar is the point.

**Finishing a figure**

- **Review every take at book size with `sheet`,** then look at the full-size take itself before promoting.
- **Write the caption and alt text from the capture,** not from the placeholder's wish list: the placeholders describe imagined screens (one listed CI steps the book's workflow doesn't have). Alt text transcribes the text and numbers a reader needs in 280–440 characters, and a caption dates anything that drifts ("JupyterLab 4.6 … in September 2026").
- **Check the figure against the sentences around it,** not only against the placeholder. The Jupyter chapter says the file browser shows `data/`, `notebooks/`, `src/`, and the README; the fixture had no README until a late retake added one.
- **Put each decision where the next person will look:** a comment in the recipe beside each workaround, `notes:` for the source, and `relaxed:` or `oversize:` for the size.

**Replacing a placeholder**

Each `PLACEHOLDER-*` image in the chapters sits in a `::: {.column-margin}` block, with a wish list for a caption (`![ALT: …]`), a path without the leading slash, and no `fig-alt`. To replace one:

1. Name the recipe's figure after the placeholder's file (`PLACEHOLDER-jupyterlab-overview.png` becomes `id: jupyterlab-overview`), so the image lands at `graphics/<chapter>/<id>.png`.
2. Delete the `.column-margin` wrapper. The margin is 300 px wide, too narrow for a screenshot, and margin content near the top of a chapter collapses the table of contents.
3. Point the image at `/graphics/<chapter>/<id>.png`, with the leading slash; `check` fails without it. Keep the `#fig-…` label, since other text may cite it, and add the wider column's class if the recipe names one.
4. Write a dated caption and a `fig-alt` from the capture, as above.
5. Put the figure next to the passage it illustrates, and cite it there with `@fig-…` (Quarto writes "Figure N.M").
6. Run `tools/shots/run check`, then render the chapter and look at the figure on the page.

## How a capture works

`capture` runs each figure's recipe in a fresh browser context:

1. It paces the request.
2. It loads the page.
3. It runs the steps.
4. It checks the page and the image against the guards.
5. It crops.
6. It writes the take to `tools/shots/out/<chapter>/<figure>/<UTC time>.png`, with a `.json` log beside it.

A take fails its guards when:

- the status is unexpected;
- the page reads like an error or block page (a Cloudflare challenge, "Access denied");
- expected text is missing;
- the image is nearly blank;
- in a headed window, the browser's bars above the page are taller than `guards.MAX_BARS` (100 DIPs): an infobar or notice is showing.

A failed take is named `<UTC time>.FAILED.png` and kept for inspection. `promote` refuses it. Nothing but `promote` writes to `graphics/`.

`compare` scores a take against the approved image with a difference hash: near 0 of 64 for the same region of the same page, about 32 for a different page. The score ignores scale, so a 2× take compares fairly with a 1× image, and live numbers that drift barely move it.

## Recipes

One YAML file per chapter in `recipes/`, named for the chapter's slug; [`recipes/README.md`](recipes/README.md) has a starter file. A figure:

```yaml
- id: github-repo                # the image is graphics/version-control/github-repo.png
  kind: capture                  # capture | render | diagram | illustration
  section: "Hosting on GitHub"
  url: https://github.com/cuinfoscience/INFO-Missing-Manual
  steps:                         # each step waits for a condition; none sleeps blindly
    - wait: {text: '^Go to file$'}          # a regular expression; reaches into shadow DOM
  expect:                        # guards beyond the defaults
    text: ['INFO-Missing-Manual']
  crop: {selector: 'main', pad: 8}          # CSS pixels; or {window: true}, {top: 0, height: 600}
  drifts: true                   # shows things that change: the caption must say when
```

- **Defaults:** an 800×600 window at scale 2, 8–30 second pauses, a 60-second limit on each wait, three retries, and JavaScript on. A chapter can change them under `defaults:`, and a figure can override any of them.
- **Steps:** `wait` (for `text`, `selector`, or `network_idle`), `hover`, `click` (by `selector`, `text`, or, as a last resort, `position`), `scroll`, `press`, and `settle` (seconds, for animation with no end signal). `scroll: {selector: …, offset: 175}` puts an element's top 175 pixels below the window's top. A `wait` needs the text to be *visible*: a site's narrow layout may hide what its desktop layout shows.
- **Crops around an element** take `pad` as one number or four (top, right, bottom, left, as in CSS), and `width` and `height` to fix the size: `{selector: '.card', pad: [13, 0, 0, 18.5], width: 560, height: 595}`. **A crop between two elements**, `{between: ['.first', '.last'], pad: 8}`, runs from the top of the first to the bottom of the second, as wide as both.
- **Other modes:** `mode: headed` and `mode: composite` are below. An `engine:` other than Playwright marks a figure that `capture` skips with a note.
- **Patterns** are regular expressions. A leading `(?i)` ignores case; the tool turns it into JavaScript's `i` flag, because Playwright and DevTools evaluate patterns in JavaScript, which has no inline flags.
- **Quoting:** quote any YAML value that contains ` #`, or everything after it becomes a comment. In single quotes, a backslash is literal: write `'quotes\?page=2'`.
- **Size and legibility keys:** `relaxed:` and `oversize:` (a sentence each) and `targets:` are under "Legibility".

## Headed figures

A figure that shows browser UI (DevTools, View Source, the browser's own JSON viewer, a menu) sets `mode: headed`:

```yaml
- id: browser-json
  kind: capture
  url: https://api.github.com/repos/cuinfoscience/INFO-Missing-Manual
  mode: headed
  window: [800, 600]                # the whole browser window, in CSS pixels
  expect: {text: ['"full_name"']}
  crop: {content: true}             # below the browser's own bars
```

How a headed capture runs:

- **The window:** Chrome for Testing opens on a virtual display sized for the window at its scale. It gets a fresh profile, a debugging port, no "controlled by automated test software" bar, and **`--disable-infobars`, passed by the toolkit itself.** Playwright's default argument list carries that flag today, and it is what hides Chrome for Testing's "only for automated testing" notice (on a machine run as root, the `--no-sandbox` warning instead: about 56 DIPs either way). The toolkit doesn't rely on Playwright's default. Note that Playwright's `ignore_default_args` filters *every* argument, the toolkit's included, so never list `--disable-infobars` there except to show an infobar on purpose.
- **The bars guard:** before the crop, the toolkit measures the browser's own bars above the page (`window.outerHeight - innerHeight`, or DevTools' height when docked) and records it as `bars` in the take's log. The tab strip and toolbar measure 87 DIPs; anything over `guards.MAX_BARS` (100) fails the take, because an infobar shows in a whole-window crop and pushes the page down in every other. A figure whose subject *is* an infobar says `expect: {infobar: true}`: the flag is left out, and the guard then requires one. `doctor` reads the bars back from a real headed window, and `selftest` reads Chrome's own command line back from `chrome://version`.
- **The address bar:** Chrome selects the URL when a page opens, so a whole-window take shows it highlighted. Crop with `{content: true}` when the address bar isn't the point.
- **DevTools settings:** `devtools:` opens DevTools with the page, from settings written into the profile before launch: `dock` (`right`, `bottom`, `left`); `zoom` (1.25 keeps DevTools readable in a small window); `size` (the pane's width, or its height when docked at the bottom); `layout` (`side-by-side` puts Styles beside the Elements tree; DevTools' default stacks it underneath in a narrow window); `sidebar` (the Styles pane's size); `overview: false` (hides the Network timeline); `columns` (Network columns to show or hide); and `first_visit: true` (clears cookies and cache before the Network panel's reload, so the log shows a first visit). DevTools 154 ignores the stored `panel`, so the toolkit clicks that panel's tab; for `network`, it then reloads the page so the log is complete.
- **Finding DevTools controls:** docked DevTools is itself a web page. The toolkit reads that page over the debugging port to find where a tab, button, request row, or header name is drawn, then clicks it for real with xdotool. No pixel positions are typed into recipes.
- **Before any step:** it waits for the page's `load` event and, with DevTools open, for DevTools to draw its Elements tree.
- **The screen grab:** the pointer is parked in the page's bottom-left corner, so hover styles and DevTools' node highlight clear. Then the screen is grabbed.

Headed steps, in addition to the ones above: `inspect: {selector: …, selects: '^<img'}` (select an element in DevTools through its element picker), `tree: {keys: [Left], until: '^<section', max: 24}` (walk the Elements tree by keyboard), `devtools_click` and `devtools_wait` (find something in DevTools by its text or `css:`; `button: 3` right-clicks, 4 and 5 turn the wheel), and `key`, `type`, and `pointer` (real keys, real typing, and the real pointer resting on something, for tooltips).

Crops for headed figures are in window coordinates: `{window: true}`, `{devtools: true}` (the docked DevTools pane alone), `{content: true, height: 560}` (below the browser's bars), `{top: 0, height: 480}`, `{between: ['body', 'td.line-number[value="43"]']}` (View Source cut at a line), and `{selector: …, pad: 8}`.

## Markers

A figure with numbered markers lists them under `annotate:`. Each mark points `at` something, and the browser measures where that is at the moment of capture, so a retake moves the markers with the page. Nothing is placed by typing in pixel positions.

```yaml
annotate:
  width_in: 7.06         # the whole figure's printed width; sets the markers' scale (default: the book's column)
  size: small            # 11-point markers, or small ones (8.5 points)
  marks:
    - {n: 1, at: {selector: '#repository-container-header', box: element}}
    - {n: 2, at: {text: '^Go to file$'}, side: left}
    - {n: 3, shape: brace, at: {selector: 'table[aria-labelledby="folders-and-files"]'}}
    - {label: '← the default branch', at: {text: '^main$', nth: 0}, x: -4}
```

What a mark can point `at`: a page element (`selector:` or `text:`, with `box: element`, `text`, or `first-line`); something in DevTools (`devtools: {row: …}`, `{selected: true}`, `{text: …}`, or `{css: …}`); `nth` to pick among matches or join a run of them; and, as a last resort, `xy: [x, y]` in image pixels, which the tool flags because it won't follow the page. A mark's `shape` is `marker` (a numbered circle), `brace`, `bracket`, `box`, or `label`. `x` and `y` pin a mark to a place in the crop; markers sharing a `column` line up; markers that would overlap spread apart and get leader lines.

`capture` draws the markers on every passing take, beside it: `<UTC time>.annotated.pdf` (vector) and `.png` (the book's, at one pixel per pixel of the screenshot). `annotate` redraws them from an existing take after you change the marks. `promote` draws them once more and copies both files into `graphics/<chapter>/` as `<figure>_annotated.png` and `.pdf`. The style is `styles/shotmarkers.sty`, from the course handouts of *Web Data Science*.

Numbered markers replace hand-drawn callouts, and the caption explains each number, as the terminal figures' captions do.

## Legibility

A figure has to be readable where it is shown, and it must not be so crammed that it stops looking like the screen the reader has. The limits below serve both ends; the text measurement is what decides.

**How much of the screen a figure shows** (its image size over its scale, in CSS pixels):

| Size | Allowed when | What the tools say |
|---|---|---|
| up to **800×600** | always (the default window) | nothing |
| up to **1024×768** | the larger view **reduces clutter** (the site's desktop layout instead of its narrow one, or enough of the page around the subject that a reader can find it), the recipe says why in `relaxed:`, and **the text passes at every target** | a note |
| anything larger | the recipe says why in `oversize:` (for example, "the lesson is the whole page's layout") | a note |
| any size over 800×600 without a reason, or `relaxed:` whose text fails | | a warning |

```yaml
relaxed: "GitHub's desktop layout keeps the About sidebar the text points to; at 800 pixels it moves below the files"
```

**The text itself.** Every take records the size of the text inside its crop, counted by character, from the page and from DevTools. The check works out how tall that text will be where the figure is shown:

| Target | Recipe | Shown at | Threshold |
|---|---|---|---|
| book | on for every chapter figure; `targets: {book: false}` turns it off | the body column, 678 pixels in a 1280-pixel window, or the image's own width if narrower | 11 px |
| book, wider column | `targets: {book: {column: page-inset-right}}` | the Quarto column named, as wide as this book draws it at 1280 pixels (`lib/legibility.py` `COLUMNS`) | 11 px |
| slides | `targets: {slides: {width: 0.8}}`, the share of a 16:9 slide's text width | a slide 1920 pixels wide | 16 px |
| handout | `targets: {handout: {width_in: 5.04}}` | print | 6 pt |

The size judged is the one that four in five characters reach or exceed, so a footer doesn't fail a figure but small main text does. `capture` reports it for every take. `check` fails a promoted image under a threshold, unless its recipe says why the words don't matter: `legibility: {skip: "the lesson is the empty page"}`. `relaxed:` still needs the text to pass, whatever `skip` says.

**What the numbers mean in this book.** Its body column is narrower than *Web Data Science*'s (678 pixels against 778), so a figure is shown smaller:

- an 800-pixel figure keeps 85% of its on-screen text size: 14-pixel text comes out at 11.9, and 12-pixel text at 10.2, which fails;
- a 1024-pixel figure in the body column keeps 66%: 16-pixel text comes out at 10.6, which fails. So a relaxed figure usually needs a wider column. In a 1280-pixel window, `column-body-outset` is 829 pixels, `column-page-inset-right` 954 (93% of 1024), and `column-page-right` 1004. Put the class on the figure, `![…](/graphics/…){#fig-… .column-page-inset-right fig-alt="…"}`, and name the column in the recipe; `check` fails a figure whose recipe names a column its chapter doesn't use.
- Every wider column reaches into the right margin, over the table of contents. Quarto collapses the table of contents while such a figure is on screen (see issue #30 and `tools/layout-audit/`), so use them for the figures that need them, not by default.

To find what a figure needs, capture it and run `sheet`: it draws each take at the size each target shows it.

## Composites

`mode: composite` captures each of its `parts` as a figure of its own, then joins them side by side on white, each labeled below, inside a thin frame:

```yaml
- id: javascript-off-on
  url: https://quotes.toscrape.com/js/
  mode: composite
  window: [600, 450]
  parts:
    - {label: JavaScript off, javascript: false, steps: [{wait: {text: 'Quotes to Scrape'}}]}
    - {label: JavaScript on, steps: [{wait: {text: 'Albert Einstein'}}]}
  layout: {gap: 28, pad: 15, label_px: 28}     # CSS pixels
```

A part can set its own `url`, `steps`, `expect`, `crop`, `javascript`, `window`, `scale`, `mode` (headless or headed), and `devtools`. Each part is paced, guarded, and retried like any take, and the joined take lists its parts. The joined figure is judged against the size limits as a whole.

## Contact sheets

`sheet <chapter>` draws each figure's newest take, with its markers if it has any, at the size each of its targets shows it. The measured text size, the verdict, and any size note are written above each one. Look at the sheet before a pull request, and attach it to the pull request, so a reviewer sees what readers will see.

## Provenance

- **`graphics/<chapter>/provenance.json`** records, for each image: its kind and source URL; when it was captured, and by whom (the tool, or a hand capture recorded with `adopt`); the browser, User-Agent, window, scale, and crop; a hash of the recipe and of the image; the sizes of its text; for a composite, its parts; for an image with markers, hashes of the annotated PNG and PDF.
- **The recipe's hash** covers what decides the capture. Marks, targets, and the `relaxed`, `oversize`, and legibility settings are left out, so changing them needs no new take.
- **Hand captures and older images:** `adopt` records an image made outside the toolkit, from its recipe's `legacy:` block (`captured:` date and `method:`). Use it for the operating-system screenshots that need a real macOS or Windows machine.
- **`graphics/<chapter>/IMAGES.md`** gets a table generated from `provenance.json`, between `<!-- shots:begin -->` and `<!-- shots:end -->`. Everything outside the markers is for people: what a figure shows that is easy to miss, and what a retake needs.

Screenshots live in per-chapter folders; the flat files directly in `graphics/` are older images, the terminal illustrations, and `graphics/memes/`. `_quarto.yml` publishes all of `graphics/`, so provenance files are public too, which is fine: they hold nothing but how each image was made.

## Checks

`check` reports **errors**, which exit 1: a recipe that does not validate; an image without provenance; an image changed after its provenance was recorded; a kind that disagrees with the recipe; an annotated PNG or PDF that is missing or changed; text too small to read at one of the figure's targets; a figure block with no `fig-alt`; a figure referenced as `graphics/…` without the leading slash (it renders as a broken image from `chapters/`); a figure whose recipe names a wider column that its chapter doesn't use; and an out-of-date `IMAGES.md` table.

It reports **warnings** for: a figure not used in its chapter; alt text under 80 characters; a drifting figure whose caption doesn't give the capture year; marks changed since the annotated image was drawn; and a figure over 800×600 whose recipe gives no reason, or whose `relaxed:` text fails.

`selftest` runs 69 offline checks against a local web server. It needs the browser but no network. It covers the guards (the bars guard included), retries, `promote`, and `check`; the User-Agent and Client Hints; anchors and markers; crops between two elements; the size limits (800×600, the relaxed 1024×768 tier with its text condition, a wider column, and `check`'s column rule); legibility; composites; `sheet`; and headed capture, including Chrome's command line read back from `chrome://version` with and without `--disable-infobars`. It skips the marker checks if TeX is missing and the headed checks if the virtual display is.

## Files

| Path | What it is |
|---|---|
| `bootstrap.sh`, `requirements.txt`, `run` | setup, pinned packages, and a wrapper that uses the toolkit's own Python |
| `shots.py` | the commands |
| `selftest.py` | the offline test |
| `UPSTREAM.md` | where this came from, and what changed here |
| `recipes/` | one recipe file per chapter, and a README with a starter file |
| `fixtures/` | pinned local applications that recipes capture from: [`fixtures/jupyter/`](fixtures/jupyter/) is JupyterLab with a made-up project |
| `lib/env.py` | paths (`graphics/`, `recipes/`, `out/`), the proxy, and the pinned browser |
| `lib/recipes.py` | loading and validating recipes; the default identity and window |
| `lib/browser.py`, `lib/steps.py`, `lib/crop.py` | launching Chrome for Testing, running steps, and cropping |
| `lib/display.py` | the virtual display, real input, and screen grabs |
| `lib/devtools.py` | DevTools settings, and reading the DevTools page to find things on screen |
| `lib/headed.py` | one headed attempt: window, flags, bars, DevTools, headed steps, and the crop |
| `lib/measure.py` | at capture: anchors' boxes and the text's sizes, in the take's pixels |
| `lib/annotate.py`, `styles/shotmarkers.sty` | markers laid out from anchors, drawn with TikZ to PDF and PNG |
| `lib/legibility.py` | the size limits, the book's columns, and text size at each target |
| `lib/sheet.py` | contact sheets |
| `lib/guards.py` | error and block pages, the bars guard, retries, and policy blocks |
| `lib/capture.py` | one figure, start to finish, composites, and the take log |
| `lib/compare.py` | take against approved image |
| `lib/provenance.py` | `provenance.json` and the `IMAGES.md` table |
