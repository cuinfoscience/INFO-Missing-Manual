# AAR: screenshot toolkit, pilot, and the table-of-contents fix

**Date:** 2026-09-24. **Covers:** porting `tools/shots` from *Web Data Science* (#35), the cloud-storage sections (#36), and, in the pull request that adds this report, the fix for #30 and the screenshot pilot (the Jupyter chapter and one pandas-basics figure).
**Written for:** agents and people who add screenshots to this book, change its page layout, or port the toolkit to another book. The practical rules are in "Patterns and pitfalls" in [`tools/shots/README.md`](../../tools/shots/README.md); this report is the story behind them.

## 1. Summary

- The pilot replaced three of the twelve placeholder images with real, reproducible captures of JupyterLab 4.6, taken from a pinned local fixture with made-up data. All three pass the legibility check (12.1–12.3 px at book size).
- The default 800×600 window crammed JupyterLab: its toolbar folded and table cells wrapped. The overview figure uses the relaxed 1024×768 limit in a wider column, the tier's first real use.
- Getting stable takes needed eight fixes that the plan did not foresee:
  - six were JupyterLab behaviours: a saved layout, a deferred navigation, hidden tabs, inner scrolling, a folder selected on every change of folder, and kernels that outlive captures;
  - one was the active cell's border leaking into crops;
  - one was a missing crop mode.

  Each is now a recipe comment, a toolkit feature, or a rule.
- A last read of each figure against the paragraph beside it found one mismatch. The chapter promises a README in the file browser, and the fixture had none; a retake fixed it.
- The #30 fix moved every chapter's meme out of the margin and into the sidebar above the table of contents. The table of contents is now open at load on 41 of 41 pages, up from 4.
- Checks that read results back caught three silent failures before they shipped: a Chrome flag that Playwright stripped (the port), a Quarto setting that a Lua filter cannot change (#30), and a generated front-matter comment that the issue-forms sync read as every chapter's title (#30).

## 2. What was supposed to happen

The screenshot plan ([`plans/2026-09-24-screenshots.md`](../plans/2026-09-24-screenshots.md)) set milestone M1 as a pilot on the Jupyter chapter, plus the pandas-basics DataFrame figure, from a local JupyterLab:

1. a fixture with pinned JupyterLab, a light theme, news notifications off, and a project with `data/`, `notebooks/`, and `src/`;
2. start and stop scripts;
3. recipes that wait on selectors, crop to what each figure needs, and date the captions;
4. review of each take at book size, with `relaxed:` and a wider column only if a crop could not stay legible within 800×600;
5. promotion, captions and alt text rewritten from the captures, `check`, a full render, and a pull request;
6. a short AAR if the pilot changed any rule or the toolkit. It changed both, hence this report.

## 3. What happened

1. **Fixture.** Built as planned: `tools/shots/fixtures/jupyter/`, with JupyterLab 4.6.4, pandas 3.0.6, and 84 rows of synthetic sales. `start.sh` copies the project to a scratch folder, runs and trusts the notebooks, and serves them on port 8899.
2. **First look at 800×600.** Crammed: a 450-px notebook area, a DataFrame with wrapped dates, and the kernel indicator folded into an overflow menu. That is the clutter the relaxed tier exists for, so the overview was captured at 1024×768 and judged in `column-page-inset-right`, where its text measured 12.1 px.
3. **Overview take 1:** the file browser showed `notebooks/`, not the project root, although the step that clicked "home" and waited for the root listing had passed. A timing probe showed JupyterLab moving the browser into the notebook's folder about a second after the notebook appears, which undid the click. Fix: wait for that move (the `notebooks` breadcrumb), then click.
4. **The cell-types figure** needed a crop from the top of one cell to the bottom of another, which headless takes could not do. `crop: {between: [A, B]}` was added for headless takes, with a selftest check (69 of 69 pass).
5. **DataFrame take 1 failed:** its wait timed out, and the crop "matched nothing visible". JupyterLab had restored the previous capture's layout (a folded sidebar and a second notebook tab), and `.first` found the hidden tab's cell. Fix: `?reset` on every URL.
6. **Crop edges, three takes:** the active cell's blue border showed along the top of one crop, then along the bottom after the active cell moved. Fixes: make a cell outside the crop active, and end the crop two pixels inside the Markdown cell's blank padding. An edge-row pixel check confirmed both edges clean.
7. **Promotion and chapters:**
   - Captions and alt text were written from the captures, not from the placeholders' descriptions of imagined screens. Alt texts run 428–439 characters.
   - The figures moved out of `.column-margin`.
   - The DataFrame figure now sits under the code that builds it.
   - `check` passes, the render has zero warnings, and the table-of-contents audit still reports 41 of 41.
8. **A late retake of the overview.** Read against the paragraph beside it, the overview lacked the README that the chapter says the file browser shows. A README was added to the fixture, and the retake exposed two more kinds of carried-over state:
   - JupyterLab had selected the `data` folder when the file browser went home, as it does on every change of folder. Clicks elsewhere and Escape left it selected; Ctrl+Space, which toggles the focused item, cleared it, once the recipe waited for the selection to appear first.
   - The status bar counted two kernels, one left running by an earlier `pandas-basics` capture. A fresh start of the fixture, capturing `jupyter` first, brought it back to one.

## 4. What went well

- **The toolkit's guards and measurements did their job:**
  - the legibility check turned "does this look readable?" into a number at the size the book shows it;
  - the contact sheets showed each take at that size;
  - failed takes were kept for inspection (a `.FAILED.png` made the saved-layout cause obvious).
- **A local fixture made the pilot fast and repeatable:**
  - no pacing, no network, and no personal data;
  - re-running a capture takes seconds.
- **The rules held up.** The relaxed tier, written the same morning, had its first real use within hours, and its text condition was what made the wider column necessary.

## 5. What went wrong or surprised us

Each item gives what happened, why, the fix, and where the lesson is recorded now.

1. **Playwright's `ignore_default_args` strips the caller's copies too** (the port, #35). The code dropped Playwright's default `--disable-infobars` and passed its own, and so lost both. A selftest that read Chrome's own command line back from `chrome://version` caught it. *Recorded:* `tools/shots/UPSTREAM.md`, the shots README, `docs/decisions.md`.
2. **Applications change their layout with width.** GitHub at 680 px and JupyterLab at 800 px both hid what the text describes. *Recorded:* the playbook ("Choosing what to show").
3. **The 678-px column makes 1024-px figures fail in the body column.** Ordinary 13–16 px interface text comes out under 11 px. Only the wider column keeps it legible, and that column covers the table of contents while on screen. *Recorded:* the playbook, `lib/legibility.py`, `AGENTS.md`.
4. **JupyterLab keeps state on the server between captures:** the fix is `?reset`. *Recorded:* the recipes, the fixture README, the playbook.
5. **Deferred navigation undid a click:** the fix is to wait for the application's own move first. *Recorded:* the recipe (with a comment), the fixture README, the playbook.
6. **`.first` found an element in a hidden tab.** *Recorded:* the playbook.
7. **Interface state leaked into crops:** the active cell's border and toolbar. It took three takes and a pixel check. *Recorded:* the recipes, the playbook.
8. **The notebook scrolls inside the page,** so a tall crop needs a tall window. *Recorded:* the recipe, the playbook.
9. **No headless `between` crop existed.** It was added with a test. *Recorded:* `lib/crop.py`, the shots README, `UPSTREAM.md`.
10. **The placeholders' alt text described imagined screens,** for example CI steps this book's workflow doesn't have. Captions were written from the captures instead. *Recorded:* the playbook ("Finishing a figure").
11. **More state carried over than the layout:** a folder selected by the file browser's own navigation, and kernels from earlier captures in the status bar's count. Neither was visible in a single take; both showed when takes were compared. *Recorded:* the recipe, the fixture README, the playbook.
12. **A figure contradicted its paragraph** (no README) and passed every check, because no check reads the text around a figure. *Recorded:* the playbook ("Finishing a figure").
13. **#30:**
    - A Lua filter cannot set `margin-header`, because Quarto reads it before filters run; a scratch-book test showed that. The generator writes it into the front matter instead, and CI checks it.
    - A footnote in one chapter's Purpose section collapsed the table of contents exactly as the margin meme had, because `reference-location: margin` makes footnotes margin notes.
    - The generated block opens with a YAML comment, `# margin-header: …`, and `tools/issue-forms/sync_issue_chapters.py` took it for each chapter's H1. Nothing in CI runs that script, so it surfaced only when its `--check` was run by hand before the push; a sync would have listed 37 chapters by that comment. The script now skips front matter.

    *Recorded:* `AGENTS.md` ("Chapter memes"), `tools/chapter-meme/README.md`, `tools/issue-forms/README.md`.
14. **Quarto 1.9 cannot build the book,** although the docs said "1.9 or later". This came up while writing `CONTRIBUTING.md`. *Recorded:* README, `AGENTS.md`, `CONTRIBUTING.md`.
15. **A compound request was read as half of itself.** "Come up with a plan to address #34 and create new sections" produced only the plan, and the maintainer had to ask again. *Recorded:* the lessons below.

## 6. Lessons

1. Read a compound request literally: "plan … and create …" asks for both. If one half seems to depend on decisions, make them with the plan's recommended defaults, say which, and do the work.
2. Read back every setting you send to a program (flags, settings, Quarto metadata) with a test that checks its effect, not just that you sent it.
3. Look at the layout at the window you choose before judging a figure. Then do the legibility arithmetic for the column the figure will sit in.
4. For application screenshots, build a pinned local fixture, and make every capture start from a known state.
5. Wait for the state the application settles into, not only for the element you need.
6. After any change to a recipe, re-run the whole recipe file and inspect the crop edges.
7. Write captions from what the capture shows.
8. Before promoting, read each figure against the paragraph beside it.
9. After generating text into files that other tools read, run every generator's `--check`, not only your own.

## 7. Actions

| Action | Owner | Status |
|---|---|---|
| Patterns and pitfalls in `tools/shots/README.md`; pointers from `AGENTS.md` | agent | Done, in this pull request |
| Headless `between` crop, with a selftest check | agent | Done (selftest 69 of 69) |
| Confirm the wider column for relaxed figures, since it covers the table of contents while on screen (screenshot plan §8, item 9). The pilot used it for one figure. | maintainer | Open |
| `doctor <chapter>` requests `https://localhost/robots.txt` for a local fixture and warns. It should check that the fixture is running instead. | agent | Open |
| Offer the headless `between` crop, the explicit `--disable-infobars` with the bars guard, and the relaxed tier to *Web Data Science* | maintainer | Open |
| The remaining nine placeholders, one chapter per pull request (plan M2–M5) | agent, then the maintainer for hand captures | Open |
| A CI check for screenshots (plan M6) | agent | Open |
| Run `tools/issue-forms/sync_issue_chapters.py --check` in CI, as `sync_margin_header.py --check` already is; run by hand, it caught the `margin-header` regression | maintainer to decide, then agent | Open |

*Note, 2026-09-24, after #37 merged:* the maintainer settled item 9 (wider columns allowed sparingly) and asked for the issue-forms check in CI, which the next pull request adds. See `docs/decisions.md`.
