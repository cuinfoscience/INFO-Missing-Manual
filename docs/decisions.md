# Decision log

Standing decisions for the book and its tools, newest first. Each entry gives the decision, the reason, and where it is written down or enforced. Entries are never deleted. When a decision is replaced, mark it *superseded* and link the entry that replaces it. Proposals that nobody has decided yet belong in [`handoff.md`](handoff.md), not here.

Entries dated before September 2026 were reconstructed from commit messages, pull requests, and the old `CLAUDE.md` when this log was started, and cite the PR that carried each one.

## 2026-09-24 · One instructions file, `AGENTS.md`; project records in `docs/`

**Decision.**
- The agent instructions live in `AGENTS.md`, renamed from `CLAUDE.md`. `CLAUDE.md` only imports it (`@AGENTS.md`), so Claude Code still loads them. An agent that looks for another file (`GEMINI.md`, `.cursorrules`) is pointed at `AGENTS.md` by the README.
- Project records live in `docs/`: AARs and reviews, plans, the roadmap, this log, and the hand-off note. `REVIEW.md` moved to `docs/aar/`, and the gap-chapter backlog moved from `CLAUDE.md` to `docs/roadmap.md`.
- Agents read the hand-off note and this log before starting, read the relevant AAR or plan before working in an area it covers, and update the records in the same pull request.

**Why.** The maintainer asked for it, following the pattern the companion book *Web Data Science* adopted the same day. Instructions under one tool's name are missed by other tools, and a lesson that lives only in a conversation is lost when the session ends.

**Where.** `AGENTS.md` ("Project memory"), `README.md` ("For AI agents"), [`README.md`](README.md) in this folder.

## 2026-09-24 · A screenshot shows at most 800×600, or 1024×768 when that reduces clutter and stays legible

**Decision.**
- A screenshot shows at most 800×600 CSS pixels of the screen by default.
- It may show up to 1024×768 when the larger view reduces clutter (a site's desktop layout instead of its narrow one, or enough of the page around the subject that a reader can find it) and its text still passes the legibility check where the book shows it. The recipe says why in `relaxed:`; the toolkit checks the text.
- Anything larger is an exception, explained in the recipe's `oversize:`.

**Why.** The maintainer's instruction. *Web Data Science* capped figures at 800×600, and its pilot found the other failure: figures so crammed they stopped reading as the screen a student sees ([upstream AAR](https://github.com/cuinfoscience/Web-Data-Science-Book/blob/main/docs/aar/AAR_Web-Data-Science-Book_2026-09-24.md), §5.1). A trial capture here showed the same thing: at 680 pixels GitHub switches to its narrow layout, hiding the About sidebar.

**What it means in this book.** The body column is 678 CSS pixels, so a 1024-pixel figure keeps only 66% of its text size there, and ordinary 16-pixel page text fails the 11-pixel threshold. A relaxed figure therefore usually goes in one of Quarto's wider columns (measured at 1280 pixels: `column-page-inset-right` 954, `column-page-right` 1004), which the recipe names and `check` confirms. Those columns cover the table of contents while on screen (see #30).

**Where.** `tools/shots/lib/legibility.py` (`SOFT_LIMIT`, `RELAXED_LIMIT`, `COLUMNS`), `tools/shots/README.md` ("Legibility"), `AGENTS.md` ("Screenshots"). The selftest covers each tier.

## 2026-09-24 · Headed captures pass `--disable-infobars` themselves, and a guard catches tall bars

**Decision.**
- Every headed capture passes `--disable-infobars` explicitly instead of relying on Playwright's default argument list.
- A headed take measures the browser's bars above the page and fails if they are taller than 100 DIPs (the tab strip and toolbar measure 87). A figure whose subject is an infobar says `expect: {infobar: true}`.

**Why.** The maintainer's instruction: a 56-pixel Chrome for Testing notice slipped into captures because only Playwright's default suppressed it. Porting the fix exposed a second trap: Playwright's `ignore_default_args` removes matching arguments the caller passed too, so dropping Playwright's copy of the flag silently dropped the toolkit's. The selftest's read-back of Chrome's command line caught it.

**Where.** `tools/shots/lib/headed.py`, `tools/shots/lib/guards.py` (`MAX_BARS`), `doctor`, and the selftest.

## 2026-09-24 · Screenshots are real captures, made with `tools/shots`

**Decision.**
- Screenshots of real pages and programs are made with `tools/shots`, ported from *Web Data Science* (commit `3de5578`, local changes in `tools/shots/UPSTREAM.md`): a recipe per chapter, guarded capture, provenance, and legibility checks.
- A screenshot is a real capture. Diagrams and illustrations are labeled as what they are. A real interface is never rebuilt by hand with invented content; if it can't be captured, the placeholder stays.
- Captures identify themselves with one User-Agent and pace their requests; no logins, credentials, or student names or work.
- The rollout starts with one pilot chapter.

**Why.** The maintainer asked for the toolkit to be adapted and for a plan to add screenshots throughout the book. The rules are the ones *Web Data Science* learned the hard way (its screenshot AARs), and they match this book's earlier choice not to simulate GUIs (2026-08-28).

**Status.** The toolkit is ported and tested (selftest 68 of 68; a real capture promoted and checked in a scratch tree). The rollout and the capture identity are proposals, waiting on the maintainer: see [`handoff.md`](handoff.md) and [`plans/2026-09-24-screenshots.md`](plans/2026-09-24-screenshots.md).

**Where.** `tools/shots/`, `AGENTS.md` ("Screenshots").

## 2026-09-24 · Supporting code lives in `tools/`, one folder per tool

**Decision.**
- Everything that supports the book but isn't part of it lives in `tools/`, one folder per tool, each with a README: `chapter-meme/`, `terminal-figures/`, `issue-forms/`, `shots/`, and `layout-audit/`. `scripts/` is gone.
- The chapter-meme shortcode moved out of `_extensions/cuinfo/chapter-meme/` to sit beside its generator. `_quarto.yml` loads it with a project-level `shortcodes:` key.

**Why.** The maintainer asked for a `tools/` folder to hold the screenshot toolkit and the existing scripts together. The old `CLAUDE.md` said the shortcode could only live under `_extensions/`; a scratch project showed the `shortcodes:` key loads it from any path, and a full render after the move matched the previous one except for the pages whose text changed, with all 37 memes identical.

**Where.** `tools/README.md`, `_quarto.yml` (`shortcodes:`), `AGENTS.md` ("Repository Structure", "Chapter memes"). *Supersedes* the April 2026 instruction not to relocate the shortcode without a dedicated PR.

## 2026-09-01 · Readers report problems through five issue forms

**Decision.**
- Five GitHub issue forms, written for novices: *Something is wrong*, *I'm stuck or confused*, *Typo or quick fix*, *Suggestion*, and *Accessibility problem*. Blank issues are off.
- The "I searched existing issues" checkbox is on every form but optional.
- Questions go in the *I'm stuck* form; there is no separate question form.
- Each form's chapter dropdown is generated from `_quarto.yml`, never edited by hand.
- A manual workflow creates the labels the forms apply, and is the source of truth for their names and colors.

**Why.** Quarto's "Report an issue" link on every chapter makes the chooser the front door for most readers, so it is part of the accessibility surface. A duplicate report is cheap to close, and a novice who bounces off a required box is a lost report. GitHub Discussions is not enabled, and a reader's question is itself a sign of a gap in the book. GitHub silently drops a form's labels if they don't exist. (#33, closing #31.)

**Where.** `.github/ISSUE_TEMPLATE/`, `.github/workflows/labels.yml`, the chapter-dropdown sync script, and `AGENTS.md` ("Issue templates").

## 2026-08-28 · Chapter URLs are flat, and the old URLs are allowed to 404

**Decision.**
- Every chapter and appendix lives directly in `chapters/` and publishes at `/chapters/<slug>.html`. Parts are declared in `_quarto.yml`, not by directories.
- The old URLs, `/parts/part-N-<topic>/<slug>.html`, are not redirected. They 404.
- Chapter URLs are stable from here on. A future move must add `aliases:` stubs (with a leading slash) and record why.

**Why.** URLs like `/parts/part-3-python/jupyter.html` were longer than they needed to be, and Quarto ignores `output-file` in books, so the only way to shorten a URL is to move the source. Redirect stubs were built (one `aliases:` entry per chapter) and then removed at the maintainer's choice, for a clean site with one canonical URL per chapter.

**The cost, kept on record.** Anything that linked a chapter before the move is broken: syllabi, assignment sheets, Canvas pages, Slack messages, other sites. GitHub Pages cannot issue a server-side redirect, so nothing catches those links. When someone reports a dead chapter link, map `parts/part-N-<topic>/<slug>.html` to `chapters/<slug>.html`; slugs did not change. Quarto's alias stubs are JavaScript redirects, not HTTP 301s, so even if they are re-added they work in a browser but are weak for search engines and invisible to non-JS clients.

**Where.** `AGENTS.md` ("Repository Structure": naming rules, published URLs, and the alias how-to). (#32.)

## 2026-08-28 · Figures are referenced with a leading slash

**Decision.** Every figure path is written from the project root: `![...](/graphics/<file>.png)`.

**Why.** Chapters sit one directory below the root, so a bare `graphics/<file>.png` resolves against the chapter's directory and renders as a broken image, with no warning from Quarto. Ten figures on the published site were broken this way before the fix. (#29.)

**Where.** `AGENTS.md` ("Add a figure").

## 2026-08-28 · Terminal sessions are drawn; other interfaces are not simulated

**Decision.**
- Figures of a shell session are generated illustrations: an HTML page rendered to PNG by headless Chromium at 2× on a 4:3 card, with numbered callouts. They sit in the body column, not the margin.
- They are not made with a terminal recorder (terminalizer, asciinema).
- Screenshots of third-party graphical interfaces (VS Code, JupyterLab, GitHub, operating-system settings, a browser) are not simulated. They need real captures; until then the placeholder stays.

**Why.** Recorders emit animated GIF or SVG, which the PDF build cannot embed, cannot draw the numbered callouts that carry the teaching, and cannot show a Windows Terminal without a Windows machine. A text terminal can be drawn faithfully; a GUI rebuilt by hand is a look-alike, not a record. The maintainer chose to decide the GUI screenshots later. (#29.)

**Where.** The terminal-figure generator and `AGENTS.md` ("Terminal figures").

## 2026-08-26 · Markdown is taught inside Common Text Formats

**Decision.** Markdown gets deeper coverage (as a communication style and as syntax) inside the Common Text Formats chapter, not a chapter of its own.

**Why.** The maintainer's call, made after first asking for a separate chapter. Common Text Formats already introduced Markdown beside YAML and JSON. (#27.)

**Where.** `chapters/common-formats.qmd`.

## 2026-04-28 · Chapter memes come from memegen.link and are committed

**Decision.**
- Each chapter declares its meme in frontmatter (`meme:` with template, lines, alt text, and an optional rationale). The frontmatter is the source of truth.
- A Lua shortcode calls a stdlib-only generator that fetches the image from memegen.link's path-style API. The PNG and a `.spec` hash of its inputs are committed, so CI renders offline unless a meme's frontmatter changes.

**Why.** The first generator (memeplotlib, matplotlib-based) drew captions outside many templates' text boxes. memegen.link renders captions against each template's own geometry. Its query-parameter form did not populate captions, so the generator uses the path-style URLs. (#23–#26.)

**Where.** `AGENTS.md` ("Chapter memes").

## 2026-04-27 · Every chapter names its stakes and ends with further reading

**Decision.**
- Every content chapter has a `## Stakes and politics` section just before Worked examples that cross-references `@sec-artifacts-politics`, and ends with a Further reading callout of 3–7 annotated items.
- Narrowly technical chapters get shorter Stakes sections, anchored on one concrete question.
- The cornerstone chapter, *Artifacts Have Politics*, is the exception: a reflective essay without Worked examples, Exercises, or a checklist.
- New external resources go in Further reading as plain links, not in `references.bib`; `[@key]` citations stay rare.

**Why.** The comprehensive review (PRs #15–#22) set out to connect every chapter to the book's public-interest argument and to make further reading consistent. It left the cornerstone with inbound links from every other chapter. ([Review](aar/2026-04-27-comprehensive-review.md).)

**Where.** `AGENTS.md` ("Canonical Chapter Structure", "Stakes and politics section", "Further reading callout").

## 2026-04-10 · The book's scope is its audience

**Decision.** Topics outside the needs of undergraduate non-CS majors are cut or condensed rather than covered in depth. A chapter on testing with pytest was drafted and removed; pre-commit hooks were drafted as a chapter and condensed into a section of Automation.

**Why.** The book is for students who use computing as a tool, not for software engineers. Both drafts were judged outside, or too advanced for, that audience (commits `851e952` and `c127108`).

**Where.** [`roadmap.md`](roadmap.md) (history of the gap analysis) and `AGENTS.md` ("Project Overview").

## Before 2026-04 · A reference handbook, not a course text

**Decision.**
- Each chapter stands on its own, so a reader can arrive mid-book from a search and still get value. Every content chapter opens with a collapsible "Prerequisites and see-also" callout.
- The reader is always "you"; the tone is a friendly, knowledgeable senior colleague.
- Code blocks are narrative. The book does not execute code at render time.

**Why.** Readers arrive with a problem in hand, not at chapter 1; the README tells them to "drop into any chapter that matches your current problem".

**Where.** `AGENTS.md` ("Project Overview", "Style Guide").
