# Plan: screenshots throughout the book

**Status:** M1, the pilot, done 2026-09-24, in the pull request that fixed [#30](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/30): three of the twelve placeholders are real captures from a local JupyterLab (§6), with the pilot chapter taken from §8's recommendation. The other decisions in §8 were settled the same day ([`decisions.md`](../decisions.md), "The screenshot plan's open decisions, settled"); M2 has started with `version-control`. The pilot's lessons are in the [screenshot AAR](../aar/AAR_INFO-Missing-Manual_2026-09-24.md) and in "Patterns and pitfalls" in `tools/shots/README.md`. It departed from §6 in three places: a fixed port (8899), since the recipes name it; no font-size override, since JupyterLab's default text passed; and `doctor` doesn't check the fixture yet (an open action in the AAR). The toolkit gained a headless `between` crop (selftest 69 of 69).
**Decided already** ([`decisions.md`](../decisions.md), 2026-09-24): screenshots are real captures made with `tools/shots`; a figure shows at most 800×600 CSS pixels, or up to 1024×768 when that reduces clutter and its text still passes; headed captures pass `--disable-infobars` themselves and fail on tall browser bars.

## 1. Goal

Replace the twelve `PLACEHOLDER-*` images with real captures that anyone can remake, each with a recipe, a provenance record, a dated caption where the subject drifts, and alt text that transcribes what a reader needs. Then open the same path to the chapters that describe graphical interfaces at length. Never ship a look-alike: if a screen can't be captured honestly, the placeholder stays.

## 2. Lessons carried over from *Web Data Science*

The sibling book ran this toolkit through two sprints and wrote them up ([screenshot AAR](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/docs/aar/2026-09-24-screenshots.md), [sprint AAR](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/docs/aar/AAR_Web-Data-Science-Book_2026-09-24.md)). What each lesson means here:

| Lesson there | How this plan applies it |
|---|---|
| Hand-built look-alikes of GitHub pages sat among real screenshots, disclosed only in a commit message | Real captures or labeled illustrations only (decided). The placeholders' alt text describes imagined screens, for example CI steps this book's workflow doesn't have, so each caption and alt text is rewritten from the real capture, not the other way round. |
| An 800×600 cap fixed tiny text but produced crammed figures | Two-sided rule (decided): 800×600 by default, 1024×768 with `relaxed:` when it reduces clutter and the text passes. This book's column is 678 px, not 778, so the check is measured, not assumed (§7). |
| Settings sent to Chrome and DevTools weren't read back; some silently did nothing | Read-backs in the port: the User-Agent and Client Hints (selftest), `--disable-infobars` from `chrome://version` (selftest), and the browser's bar height (doctor, and every headed take). |
| Toolkit changes counted as done before a real figure was made | One real figure was captured, promoted, and checked with the ported code before this plan (§7). Any later toolkit change repeats that. |
| Rolling out everywhere at once hid problems | One pilot chapter, then one chapter per pull request. |
| Squash merges forced repeated force-pushes of a reused branch | Proposed here as a decision (§8, item 8). |
| Alt text of 280–440 characters that transcribes the screen set the bar | Adopted in `AGENTS.md` ("Screenshots"). |

## 3. The twelve placeholders

| Chapter | Placeholder | What the text needs it to show | Route |
|---|---|---|---|
| `version-control` | `github-repo` | A repository page: tabs, file list, README | A: web page |
| `version-control` | `github-pr-diff` | A pull request's diff with removed and added lines, and a comment thread | A: web page (needs a scroll step) |
| `automation` | `github-actions-run` | A workflow run and its steps | A: web page; signed-out views hide step logs (§7) |
| `http-apis` | `browser-json-response` | The browser showing a JSON response | A: headed, Chrome's JSON view. Use the chapter's own running example (`api.github.com/repos/pandas-dev/pandas`), and move the figure out of the margin, where no screenshot is legible |
| `jupyter` | `jupyterlab-overview` | JupyterLab: file browser with `data/`, `notebooks/`, `src/`; a notebook tab; the kernel indicator | B: local JupyterLab |
| `jupyter` | `jupyter-cell-types` | A code cell with `df.head()` output above a rendered Markdown cell | B: local JupyterLab |
| `pandas-basics` | `dataframe-render` | A rendered DataFrame with index and bold headers | B: local JupyterLab |
| `text-editors` | `vscode-overview` | VS Code: explorer, editor with a Run button, integrated terminal | C: desktop app (decision §8, item 3) |
| `linting` | `vscode-ruff-squiggles` | Ruff's squiggles on three lines, and a hover showing a rule | C: desktop app, with the Ruff extension |
| `collaboration` | `github-pr-review-comment` | An inline review comment, a reply, and a resolved thread | D: a real review thread (decision §8, item 4) |
| `operating-system` | `windows-about` | Settings → System → About, with version and build | E: hand capture on Windows |
| `operating-system` | `macos-about` | About This Mac, with version and build | E: hand capture on macOS |

**Routes:**

- **A. Web pages,** headless or headed, through the toolkit as it is. Pages from the book's own repository keep the content honest and stable enough; captions give the month.
- **B. Local JupyterLab,** served on `localhost` from a fixture checked into `tools/shots/fixtures/jupyter/`: a pinned JupyterLab in its own environment, a small project (`data/`, `notebooks/`, `src/`) with synthetic data, the light theme, and news notifications turned off. No network, no pacing, fully reproducible.
- **C. A desktop application** (VS Code). Three options in §8, item 3.
- **D. A real conversation** on GitHub, which can't be generated honestly by a script.
- **E. Hand captures** by the maintainer on real machines, recorded with `tools/shots/run adopt` and a `legacy:` block (date and method), after cropping anything identifying: About This Mac shows a serial number, and Windows shows the device name.

## 4. Beyond the placeholders

- **Chapters that describe interfaces at length.** A word scan for click, right-click, menu, button, dialog, sidebar, toolbar, Settings, Preferences, Finder, File Explorer, and drag counts 129 in `file-system`, 90 in `operating-system`, 33 in `text-editors`, 22 in `jupyter`, 13 in `terminal`, 12 in `latex`, and 10 in `remote`. The top two are operating-system screens (route E): Finder's column view, File Explorer's view toggles, and the sync-status icons that the cloud-storage plan ([`2026-09-24-cloud-storage-sections.md`](2026-09-24-cloud-storage-sections.md)) will need.
- **Older screenshots in use.** Ten images predate the toolkit: Finder and Explorer icons, four browser download-settings shots, three menu icons, and the conda diagram. Record them with `adopt` (date unknown, "before 2026-08") or retake them as their chapters come up. The four download shots belong to a trailing section of `file-system` that the roadmap proposes folding into the body, so settle that first.
- **Eight orphaned images** that no chapter uses: `How_to_export_as_HTML`, `apple_logo`, `mac_software_update_app`, `mac_software_update_screen`, `macos_finder_columns`, `windows_logo`, `windows_update_app`, and `windows_update_screen` (all `.png`). Git keeps them if they are deleted.
- **The five terminal figures** are illustrations drawn by `tools/terminal-figures`, not captures. Their alt text says "Illustration of…" but their captions don't. The rule adopted here is that a figure drawn to look like a window says so in its caption.

## 5. Milestones

Each milestone is one pull request, or one per chapter, with the contact sheet (`tools/shots/run sheet <slug>`) attached for review.

- **M0, decisions.** The maintainer settles §8.
- **M1, pilot: `jupyter`,** plus `pandas-basics`' DataFrame from the same fixture (route B). It is local, needs no third-party site, and exercises recipes, waits on selectors, the legibility check, `promote`, and `check` end to end. Write a short AAR if the pilot changes any rule or the toolkit.
- **M2, web pages:** `version-control` (2), `http-apis` (1), `automation` (1). Route A, one pull request per chapter, captions dated.
- **M3, review thread:** `collaboration` (1), once its source is chosen.
- **M4, editors:** `text-editors` and `linting`, by the route chosen. If that is the desktop app, the toolkit first gains an `app` mode (launch the program on the virtual display, grab its window) in its own pull request, with selftest coverage and one real capture.
- **M5, operating systems:** `operating-system` (2), hand captures with a short checklist: window size, scale, crop, what to hide, and the `adopt` step.
- **M6, CI:** a workflow on pull requests that touch `graphics/` or `tools/shots/recipes/`, running `tools/shots/run check` (no browser needed), as *Web Data Science*'s AAR recommends (its P1-1).
- **Later:** the interface-heavy chapters in §4, the older images, and the orphans.

## 6. Pilot details (M1)

1. Fixture: `tools/shots/fixtures/jupyter/` with `requirements.txt` (JupyterLab pinned), a `settings/` overrides file (light theme; `fetchNews` off; a fixed font size), and a project tree with a notebook whose first cells match the chapter's example.
2. A `start.sh` that creates the environment, starts JupyterLab on a free local port with no token, and prints the URL; `stop.sh` to end it. `doctor jupyter` reports whether it is up.
3. Recipes in `tools/shots/recipes/jupyter.yml` and `pandas-basics.yml`: waits on selectors, not text (in the trial, the first text match was hidden), crops to what each figure needs, `drifts: true` with the JupyterLab version in the caption.
4. Review the sheet at book size. If a crop can't keep the text legible within 800×600, try `relaxed:` with a wider column, and record the choice.
5. Promote, rewrite captions and alt text from the captures, run `check` and a full render, and open the pull request.

## 7. Evidence from this session

- **The port works end to end.** The repository page was captured headless and headed at 680×510 and 2×, promoted into a scratch `graphics/`, and checked; `check` caught a figure path without the leading slash. Its text measured 14 px at book size.
- **Narrow windows change the page, not just its size.** At 680 CSS pixels GitHub switches to its narrow layout: a menu button instead of the header, and the About sidebar moved below the files. A wait on the About text timed out because the text wasn't visible. This is the clutter that the relaxed tier addresses.
- **Legibility in this book's column.** At an 800-pixel window, GitHub's text measured about 10.2 px at book size in an earlier trial, under the 11-px threshold. The text on dense web pages therefore fails at 800 pixels unless the crop is narrower or the figure sits in a wider column (`column-page-inset-right`: 954 px at 1280).
- **Infobars.** A headed Chrome for Testing window's bars measure 87 DIPs with `--disable-infobars` and 143 without. Passing the flag and then listing it in Playwright's `ignore_default_args` removes it again; the selftest now checks both ways.
- **JupyterLab** (a trial with version 4.6.4): the news notification appeared over the page, and a text wait timed out on a hidden first match. Both are handled in §6.
- **VS Code desktop on the virtual display** worked after two workarounds: a short `--user-data-dir` (the IPC socket path limit is 107 characters) and an unset `NODE_OPTIONS`.
- **GitHub signed out:** an Actions run page hides the step logs, and a pull request's diff needs a scroll step to reach a given file.
- **Headed captures** show the URL selected in the address bar; crop to the content unless the address bar is the point.

## 8. Decisions needed from the maintainer

1. **Capture identity.** The toolkit sends `Missing Manual/v1 (+https://github.com/cuinfoscience/INFO-Missing-Manual)`. *Web Data Science* sends a contact email instead. Keep the repository link, or use an address?
2. **Pilot chapter.** Recommended: `jupyter` (route B, local, reproducible).
3. **VS Code.** (i) VS Code for Linux on the virtual display, with a new `app` mode in the toolkit: real VS Code, but a Linux window frame, captioned as such; (ii) code-server in the browser: the same editor core, but a different product with different chrome; or (iii) hand captures on the maintainer's Mac, recorded with `adopt`. Recommended: (i), or (iii) if a Mac frame matters more than reproducibility.
4. **The review thread** for `collaboration`: an existing pull request in this repository that has an inline review comment, or a review the maintainer holds on a real pull request for the purpose (real, and captioned as this book's repository).
5. **The Actions run** for `automation`: the signed-out run summary (capturable now), or a signed-in view with step logs, captured by hand.
6. **Terminal illustrations:** add "Illustration:" (or similar) to their five captions?
7. **The eight orphaned images:** delete them?
8. **Merge policy:** adopt *Web Data Science*'s (merge commits, no force-pushes of shared branches, a fresh branch per pull request)? This repository already merges with merge commits.
9. **Wider columns** for relaxed figures cover the table of contents while on screen. Accept that for the few figures that need it, or require a crop to 800 pixels first? This interacts with [`2026-09-24-toc-below-meme.md`](2026-09-24-toc-below-meme.md).
