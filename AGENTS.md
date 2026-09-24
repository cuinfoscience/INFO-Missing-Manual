# Missing Manual for Information Scientists — agent instructions

Instructions for AI coding agents (Claude Code, Codex, and any other) and for people extending the book. This is the one instructions file: `CLAUDE.md` only imports it, and an agent that looks for its own file (`GEMINI.md`, `.cursorrules`, and so on) should read this one. Read it before making any changes.

---

## Project memory: `docs/`

The book's records live in `docs/`: after-action reports (AARs) and reviews, plans, the roadmap, the decision log, and the hand-off note. `docs/README.md` says how each kind is kept. They are how one session's lessons reach the next, so use them:

- **Before starting work,** read `docs/handoff.md` (where work stands: what is done, paused, waiting on the maintainer, or known to be broken) and `docs/decisions.md` (standing decisions and the reason for each). Don't reverse a recorded decision on your own; if you think one is wrong, say so and let the maintainer decide.
- **Before working in an area a record covers,** read that record. AARs and reviews are in `docs/aar/`, plans for larger work in `docs/plans/`, and the chapter backlog in `docs/roadmap.md`. For example, read the comprehensive review (`docs/aar/2026-04-27-comprehensive-review.md`) before restructuring a chapter it flagged.
- **When the state changes, update the records in the same pull request.** Rewrite `handoff.md` when a session stops or work pauses; add an entry to `decisions.md` when the maintainer decides something; tick off `roadmap.md` items when they land.
- **After a sprint, or a failure worth learning from,** write an AAR in `docs/aar/` named `AAR_INFO-Missing-Manual_<YYYY-MM-DD>.md`: what the written rules said should happen, what happened, why the two differed, and what changes as a result.
- **Write rules down.** A rule the maintainer states in conversation does not survive the session. Put it in this file or in `decisions.md`, in the same pull request.

---

## Project Overview

The **Missing Manual for Information Scientists** is a Quarto book for undergraduate non-CS majors — students in data science, social science, humanities, and adjacent fields who use computing as a tool but haven't learned the systematic practices that surround it. The handbook fills the "hidden curriculum" gap: the skills that fall between knowing what to type and understanding how to work professionally.

**Author:** Brian C. Keegan
**Format:** [Quarto book](https://quarto.org/docs/books/) rendered to HTML (primary) and PDF
**Intended use:** **Reference documentation**, not a front-to-back read. Each chapter is designed to stand on its own so a reader can drop in mid-book and still get value.

---

## How to Build

### Prerequisites

- **Quarto ≥ 1.9.0** (required for `llms-txt` support) — https://quarto.org/docs/download/
- **TinyTeX** (optional, local only) — only needed if you want to render the PDF; `quarto install tinytex`. CI builds HTML only.
- Optional: Python 3.11+ if you want to add executable code cells (not currently used)

### Commands

```bash
# Live preview (auto-rebuild on save)
quarto preview

# Render HTML (matches CI)
quarto render --to html

# Render PDF locally (requires TinyTeX, not run in CI)
quarto render --to pdf
```

Output lands in `book/` (gitignored). The landing page is `book/index.html`. The LLM-friendly files are `book/llms.txt` and one `*.llms.md` per chapter. A PDF is only produced if you explicitly run `--to pdf`.

### Verify

After `quarto render --to html`:

- **Zero warnings** from `quarto render --to html`.
- `book/index.html` opens and the sidebar lists all seven parts with their chapters.
- `book/llms.txt` exists and enumerates all chapters.
- At least a handful of `@sec-*` cross-references resolve (click through in HTML).
- Optional, local only: `quarto render --to pdf` renders without LaTeX errors (requires TinyTeX).

---

## Repository Structure

```
INFO-Missing-Manual/
│
├── AGENTS.md                        # this file: instructions for agents and people
├── CLAUDE.md                        # imports AGENTS.md, for Claude Code
├── docs/                            # project records (see "Project memory" above)
│   ├── README.md                    # how each kind of record is kept
│   ├── handoff.md                   # where work stands right now
│   ├── decisions.md                 # standing decisions, newest first
│   ├── roadmap.md                   # chapter backlog and open follow-ups
│   ├── aar/                         # after-action reports and reviews
│   └── plans/                       # plans for larger pieces of work
├── _quarto.yml                      # book config (HTML + PDF, llms-txt: true)
├── index.qmd                        # landing page (Introduction)
├── conclusion.qmd                   # final chapter
├── references.bib                   # BibTeX bibliography (22 entries)
├── .github/
│   ├── workflows/build-book.yml     # CI: renders + publishes on push/PR
│   ├── workflows/labels.yml         # manual run: creates the labels the issue forms use
│   └── ISSUE_TEMPLATE/              # five issue forms + chooser config (see "Issue templates")
│
├── chapters/                        # every chapter and appendix, one flat directory
│   │                                # reading order and part grouping live in _quarto.yml
│   ├── questions.qmd                # Part I — Practice of Technical Work
│   ├── documentation.qmd
│   ├── common-formats.qmd
│   ├── reading-docs.qmd
│   ├── debugging.qmd
│   ├── tracebacks.qmd
│   ├── artifacts-have-politics.qmd
│   ├── operating-system.qmd         # Part II — Computing Environment
│   ├── file-system.qmd
│   ├── terminal.qmd
│   ├── text-editors.qmd
│   ├── remote.qmd
│   ├── package-management.qmd       # Part III — Python Management
│   ├── virtual-environments.qmd
│   ├── jupyter.qmd
│   ├── scripting.qmd
│   ├── regex.qmd
│   ├── linting.qmd
│   ├── data-file-formats.qmd        # Part IV — Working with Data
│   ├── tabular-data.qmd
│   ├── pandas-basics.qmd
│   ├── sql-basics.qmd
│   ├── http-apis.qmd
│   ├── reading-scholarship.qmd      # Part V — Communication
│   ├── writing-manuscripts.qmd
│   ├── writing-thesis.qmd
│   ├── presenting.qmd
│   ├── latex.qmd
│   ├── project-management.qmd       # Part VI — Project Management
│   ├── version-control.qmd
│   ├── collaboration.qmd
│   ├── automation.qmd
│   ├── secrets.qmd
│   ├── ai-llm.qmd                   # Part VII — Algorithmic Systems
│   ├── llm-internals.qmd
│   ├── ai-agents.qmd
│   ├── evaluating-ai.qmd
│   ├── appendix-glossary.qmd        # Appendix A (glossary with term anchors)
│   └── appendix-ai-disclosure.qmd   # Appendix B (AI disclosure statement)
│
├── graphics/                        # PNGs referenced from chapters
│   └── memes/                       # generated chapter memes (PNG + .spec hash)
└── tools/                           # supporting code; every folder has a README
    ├── README.md                    # what each tool does and when it runs
    ├── requirements.txt             # what CI installs (empty: the meme generator is stdlib only)
    ├── chapter-meme/                # {{< chapter-meme >}} shortcode + memegen.link generator
    ├── terminal-figures/            # annotated terminal illustrations (HTML -> PNG)
    ├── issue-forms/                 # rebuilds the chapter dropdown in every issue form
    ├── shots/                       # screenshot toolkit, ported from Web-Data-Science-Book
    └── layout-audit/                # browser checks on a rendered book (TOC visibility, column width)
```

**Naming rules:**

- Chapter file slugs: lowercase, hyphens (`virtual-environments.qmd`, not `virtual_environments.qmd` — underscores collide with Quarto's section-ID syntax).
- Section IDs: `{#sec-<slug>}`, matching the chapter file name without the extension.
- Every chapter lives directly in `chapters/`. There are no part subdirectories: Quarto mirrors the source tree into the output, so nesting chapters by part is what produced URLs like `/parts/part-3-python/jupyter.html`. Flat sources give `/chapters/jupyter.html`. Part grouping is declared by the `part:` entries in `_quarto.yml` and is unaffected by where files sit on disk.

**Published URLs.** Each chapter renders to `/chapters/<slug>.html` — for example <https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/jupyter.html>.

**Old chapter URLs are dead, on purpose.** Until August 2026 chapters published under `/parts/part-N-<topic>/`, and those URLs now **404**. If someone reports a dead chapter link, this is almost certainly why: map `parts/part-N-<topic>/<slug>.html` to `chapters/<slug>.html`; the slug is unchanged. Why there are no redirects, and what that cost, is recorded in `docs/decisions.md` (2026-08-28).

**Treat chapter URLs as stable from here on.** Renaming a chapter file, or moving chapters into or out of `chapters/`, breaks every external link to it, silently and permanently. If a future change does need to move them, Quarto can emit redirect stubs via an `aliases:` entry in a chapter's frontmatter:

```yaml
---
aliases:
  - /parts/part-3-python/jupyter.html
---
```

The leading slash is required — without it the alias resolves relative to `chapters/` and the stub lands at `/chapters/parts/...`, redirecting nothing. Note these stubs are JavaScript redirects, not HTTP 301s, so they work in a browser but are weak for search engines and invisible to non-JS clients.

---

## Section Labels (for `@sec-*` cross-references)

Every chapter has an explicit H1 section ID immediately after the heading. Use them in other chapters with `@sec-<name>`.

| Chapter | Label |
|---|---|
| Asking Technical Questions | `@sec-asking-questions` |
| Technical Documentation | `@sec-documentation` |
| Common Text Formats | `@sec-common-formats` |
| Reading Official Documentation | `@sec-reading-docs` |
| Debugging | `@sec-debugging` |
| Reading Python Tracebacks | `@sec-tracebacks` |
| Artifacts Have Politics | `@sec-artifacts-politics` |
| Operating System | `@sec-os-management` |
| Local File System | `@sec-filesystem` |
| Command Line | `@sec-terminal` |
| Text Editors | `@sec-text-editors` |
| Remote Computing | `@sec-remote-computing` |
| Package Management | `@sec-pkg-mgmt` |
| Virtual Environments | `@sec-virtual-environments` |
| Jupyter | `@sec-jupyter` |
| Scripting | `@sec-scripts-vs-notebooks` |
| Regular Expressions | `@sec-regex` |
| Code Style, Linting, and Formatting | `@sec-linting` |
| Data File Formats | `@sec-data-file-formats` |
| Tabular Data: Shape, Cleaning, and Validation | `@sec-tabular-data` |
| pandas Basics | `@sec-pandas-basics` |
| SQL Basics | `@sec-sql-basics` |
| HTTP and Web APIs | `@sec-http-apis` |
| How to Read Scholarly Articles and Books | `@sec-reading-scholarship` |
| How to Write Scholarly Manuscripts | `@sec-writing-manuscripts` |
| How to Write a Thesis | `@sec-writing-thesis` |
| How to Present | `@sec-presenting` |
| How to Use LaTeX | `@sec-latex` |
| Project Management | `@sec-project-management` |
| Version Control | `@sec-git-github` |
| Collaboration Mechanics | `@sec-collaboration` |
| Automation | `@sec-automation` |
| Environment Variables and Secrets | `@sec-secrets` |
| Using AI Tools | `@sec-ai-llm` |
| LLM Internals | `@sec-llm-internals` |
| AI Agents | `@sec-ai-agents` |
| Evaluating AI | `@sec-evaluating-ai` |
| Glossary (appendix) | `@sec-glossary` |
| AI Disclosure (appendix) | `@sec-ai-disclosure` |

**Inline reference form:**

```markdown
See @sec-debugging for the investigative loop.
```

Quarto auto-prefixes `Chapter` when rendering, so do **not** write "Chapter @sec-debugging" — it becomes "Chapter Chapter 4 Debugging."

---

## Style Guide

### Tone and Voice

- **Friendly guide** — warm, second-person, like a knowledgeable senior colleague.
- Always address the reader as **"you"** (not "the user," "the student," "one," or "a reader").
- Empathetic about frustration; high expectations about capability.
- Direct and imperative for instructions: "Run this command," "Check the version."
- Non-judgmental about mistakes and questions.

### Canonical Chapter Structure

Every content chapter follows this structure:

1.  `# Chapter Title {#sec-<slug>}` (H1 with explicit section ID)
2.  **Prerequisites callout** (top of chapter, `::: {.callout-tip collapse="true"}`)
3.  `## Purpose {.unnumbered}` — one to three paragraphs explaining why this chapter exists
4.  `## Learning objectives {.unnumbered}` — numbered list; intro is always *"By the end of this chapter, you should be able to:"*
5.  `## Running theme: <short phrase> {.unnumbered}` — one-sentence principle for the chapter
6.  Numbered `## Section` blocks — main content
7.  `## Stakes and politics` — chapter-specific public-interest framing, immediately before Worked examples (see "Stakes and politics section" below)
8.  `## Worked examples` — numbered subsections
9.  `## Templates` — reusable snippets (optional, varies by chapter)
10. `## Exercises` — numbered list
11. `## One-page checklist` — bullet list for quick reference
12. `## Quick reference: ...` — tables and one-liners (optional)
13. **Further reading callout** — `::: {.callout-note}` with a `## 📚 Further reading` heading; 3–7 curated annotated items at the very end of the chapter (see "Further reading section" below)

The cornerstone chapter `chapters/artifacts-have-politics.qmd` is the documented exception: it is intentionally a reflective essay and does not include Worked examples, Exercises, or a One-page checklist.

### Stakes and politics section

Every content chapter (except the cornerstone) ends — just before Worked examples — with a numbered `## Stakes and politics` section that names the public-interest dimension of the chapter's topic. The section is roughly 150–300 words, anchored on 2–3 concrete decisions specific to the chapter, and always cross-references the cornerstone with `@sec-artifacts-politics`. The section closes with one sentence pointing to the cornerstone and a concrete prompt the reader can carry forward.

```markdown
## Stakes and politics

<2–4 sentences making the chapter-specific stakes concrete: who benefits when this works as designed, who pays when it fails, what choices look technical but are political. Do not re-litigate the artifacts-have-politics chapter; specialize to this topic.>

<1–2 sentences naming the specific Winner-style move: which defaults are the politics, which costs are externalized, which gatekeeping is hidden in the workflow.>

See @sec-artifacts-politics for the broader framework. The concrete prompt to carry forward: <one sentence the reader can apply when they next encounter this chapter's topic>.
```

Tier-3 chapters (narrowly technical topics where the politics angle is hardest to make load-bearing — for example `regex`, `tracebacks`, `latex`, `common-formats`, `debugging`, `file-system`) get shorter sections (~150–200 words) anchored on a single concrete question rather than a forced full-checklist application.

### Further reading callout

Every chapter ends with a Further reading callout using the cornerstone's pattern: a `callout-note` block with a `## 📚 Further reading` heading and 3–7 annotated bullet items.

```markdown
::: {.callout-note}
## 📚 Further reading

- **<Author/Source>**, [<Title>](<url-or-DOI>) — <one sentence: why this is on the list>.
- **<Official docs>**, [<Title>](<url>) — <one sentence>.
- **<Community resource>**, [<Title>](<url>) — <one sentence>.
:::
```

Curation rules: 3–7 items per chapter, mix of books/articles, official docs, and community resources, one sentence of annotation each. Prefer durable sources (books, official docs, well-maintained community sites) over blog posts that will rot. Do not duplicate items already linked from the chapter body. New external resources go here as plain links rather than as new `references.bib` entries — the book uses `[@key]` citations sparingly (currently only `documentation.qmd`, `automation.qmd`, and `artifacts-have-politics.qmd`) to preserve the reference-handbook feel.

### Prerequisites and see-also callout (chapter independence)

Every content chapter begins with a collapsible callout that lists 0–3 prerequisite chapters and 0–3 related chapters. This is how we signal that each chapter is self-contained but linkable.

```markdown
::: {.callout-tip collapse="true"}
## Prerequisites and see-also

**Prerequisites (read first if unfamiliar):** @sec-foo, @sec-bar.

**See also:** @sec-baz, @sec-qux.
:::
```

Inline `(see @sec-foo)` references are also fine inside prose — the two mechanisms reinforce each other.

### Formatting Conventions

**Emphasis:**

```markdown
**bold first definitions**   <!-- bold for first mention of a term -->
*italic emphasis*            <!-- italic for concepts -->
`code`                       <!-- backticks for commands/filenames -->
```

**Lists:** plain markdown; no pandoc-style list options. Quarto respects list spacing automatically.

**Code blocks:** fenced blocks with a language hint where it helps highlighting.

````markdown
```bash
pip install pandas
```

```python
df = pd.read_csv("data.csv")
```
````

Non-executable code blocks are the default; the book does not currently use Jupyter/Python execution. If you add executable cells, use ` ```{python} ` and configure `execute: enabled: true`.

**Citations:**

```markdown
[@wilson2017goodenough]
[@wilson2017goodenough; @chacon2014progit]
```

Bibliography file: `references.bib` at the repo root. Bibliography rendering is handled automatically via `bibliography: references.bib` in `_quarto.yml`.

**Links and margin notes:**

```markdown
[link text](https://example.com)

^[A sidenote appears as a numbered margin note in HTML.]

::: {.column-margin}
![Caption.](graphics/figure.png){#fig-my-figure}
:::
```

**Callouts** (five flavors: `note`, `tip`, `warning`, `important`, `caution`):

```markdown
::: {.callout-note}
A helpful note.
:::
```

**Cross-references:**

- Section: `## Topic {#sec-topic}` → `@sec-topic`
- Figure: `![Caption.](img.png){#fig-foo}` → `@fig-foo`
- Table: `| col |\n|---|\n| data |` with `: Caption {#tbl-foo}` → `@tbl-foo`

**Glossary links:**

```markdown
A [virtual environment](appendix-glossary.qmd#term-virtual-environment) is...
```

Each glossary term in `appendix-glossary.qmd` has an explicit `{#term-<slug>}` anchor. Use these sparingly — link only on first use in a chapter.

### What Not to Change

- `_quarto.yml` top-level structure without a reason. In particular, do not remove the sibling `website: { llms-txt: true }` block; Quarto 1.9 has a bug where `llms-txt` under `book:` does not activate llms.txt generation, but under `website:` it does. See @sec-automation analog in the issue tracker if you want to upstream this.
- Section ID prefixes. They are baked into cross-references across the book.
- The `shortcodes:` key in `_quarto.yml`. It is what loads `{{< chapter-meme >}}`.

---

## Chapter memes

Each chapter declares an optional meme in YAML frontmatter; the rendered PNG appears in the column-margin next to the `## Purpose` section.

**Frontmatter contract** (`chapters/<chapter>.qmd`):

```yaml
meme:
  template: "fine"           # memegen template id
  lines:                     # positional, one per text region in the template
    - ""
    - "MY CODE IS ON FIRE BUT THIS IS FINE"
  alt: "Short caption for screen readers."   # required for accessibility
  rationale: "humor — short source-only note explaining the choice"  # optional
  # width: 1000              # optional override; default 1000 (output width in pixels)
  # font: "impact"           # optional override; default "impact"
```

Inside the chapter body — conventionally just below the `## Purpose {.unnumbered}` heading — invoke the shortcode:

```markdown
{{< chapter-meme >}}
```

**Pipeline.** The Lua shortcode at `tools/chapter-meme/chapter-meme.lua` reads the frontmatter, hashes `template + width + font + lines` into a `.spec` sidecar, and invokes `tools/chapter-meme/generate_chapter_meme.py` if the cached PNG is missing or the hash changed. The Python script is a thin wrapper that builds a memegen URL of the form `https://api.memegen.link/images/<template>.png?text[]=line1&text[]=line2&width=1000&font=impact` and writes the response bytes to disk. Generated assets land in `graphics/memes/<slug>.png` (and a sidecar `<slug>.spec` holding the hash). All three components are checked in and the PNGs are committed to the repo so CI doesn't need to hit memegen on every build — but the `meme:` frontmatter is the source of truth, and editing it on a chapter triggers regeneration on next `quarto render`.

**Width and font knobs.** memegen sizes captions to each template's authored text-box geometry, so there is no `fontsize` setting; the analogous knobs are `width` (output resolution in pixels, default `1000`) and `font` (memegen font id, default `impact`). A chapter can override with `meme.width: 1200` or `meme.font: notosans`; both are part of the spec hash, so changes invalidate the cache cleanly. To retune the defaults for every chapter, edit the constants in [tools/chapter-meme/generate_chapter_meme.py](tools/chapter-meme/generate_chapter_meme.py) **and** the `or "1000"` / `or "impact"` fallbacks in [tools/chapter-meme/chapter-meme.lua](tools/chapter-meme/chapter-meme.lua) — keep them in sync. Then force a full regeneration:

```bash
rm graphics/memes/*.png graphics/memes/*.spec
quarto render --to html
```

**Pushing meme changes.** A full regeneration replaces all 37 PNGs (~23 MB total). git's default HTTP post buffer (1 MB) is too small for that payload and the push will fail with `RPC failed; HTTP 400 curl 22`. Use a larger buffer for the push:

```bash
git -c http.postBuffer=524288000 push
```

The `http.postBuffer=524288000` (500 MB) flag is per-invocation, so it does not need to be configured globally. Smaller meme changes (one or two PNGs) push fine with the default buffer.

**How the shortcode is loaded.** `_quarto.yml` names it in a project-level `shortcodes:` key (`- tools/chapter-meme/chapter-meme.lua`), so it sits beside the script it calls instead of in an `_extensions/` folder. Don't remove that key: every chapter that calls `{{< chapter-meme >}}` would render the literal shortcode instead of its meme. (An earlier version of this file said the shortcode could only live under `_extensions/`; that was wrong. See `docs/decisions.md`, 2026-09-24.)

**Dependency.** The generator uses Python's standard library only (`urllib.request`); there is no `pip install` step. The build host needs outbound HTTPS to `api.memegen.link` on the first render after a meme's frontmatter changes; subsequent renders read the cached PNG and run offline. CI's GitHub Actions runners have outbound HTTPS by default, so no workflow changes are needed. See [memegen.link](https://github.com/jacebrowning/memegen) for template ids and font choices.

---

## Terminal figures

Chapters that show a shell session use generated illustrations rather than screen captures. [tools/terminal-figures/generate_terminal_figures.py](tools/terminal-figures/generate_terminal_figures.py) draws each figure as a small HTML page and renders it to PNG with headless Chromium at 2x on a 4:3 card, producing `graphics/<slug>.png`. The five current figures are `macos-terminal-annotated`, `windows-terminal-annotated` (both @sec-terminal), `ssh-connected` (@sec-remote-computing), `venv-prompt` (@sec-virtual-environments), and `pip-install-success` (@sec-pkg-mgmt).

```bash
python tools/terminal-figures/generate_terminal_figures.py           # regenerate all figures
python tools/terminal-figures/generate_terminal_figures.py --check   # fail if a PNG is stale
```

Figures are defined declaratively in the script's `FIGURES` dict: terminal lines plus numbered callouts positioned by character offset into a line. To add or edit one, change that dict and re-run. As with the memes, the PNGs are committed and CI never regenerates them — this is an authoring tool, not a build step.

Two constraints worth knowing before you touch it. **Use a headless-shell build of Chromium.** A full Chrome build reserves about 87px of the window height for browser chrome, so the bottom of every figure renders blank while the PNG is still emitted at full size; `check_viewport()` fails loudly rather than letting that ship. Set `$CHROME` if the automatic search picks the wrong binary. **Callout offsets are character positions,** which only works because the figures use DejaVu Sans Mono; changing the font family means re-deriving `CHAR_ADVANCE`.

Why not a recorder like [terminalizer](https://github.com/faressoft/terminalizer) or [asciinema](https://asciinema.org)? They emit animated GIF or SVG, which the PDF build cannot embed; they cannot draw the numbered callouts that carry the teaching; and a recording cannot show a Windows Terminal tab bar without a Windows machine to record on. [charmbracelet/freeze](https://github.com/charmbracelet/freeze) is the closest static alternative and worth revisiting if the book ever wants many unannotated output figures, at the cost of a Go dependency.

**Remaining `PLACEHOLDER-*` images.** Twelve chapters still reference placeholder PNGs that do not exist. They are all screenshots of third-party GUIs — VS Code (×2), JupyterLab (×2), GitHub web UI (×4), Windows and macOS settings panels (×2), a browser JSON view, and a rendered pandas DataFrame. Unlike terminal sessions, these cannot be honestly simulated and need real captures from a real machine; treat them as an open editorial decision rather than a generation task.

## Issue templates

Readers report problems through GitHub **issue forms** in `.github/ISSUE_TEMPLATE/` — structured YAML forms with dropdowns and required fields, not free-text markdown templates. They were modelled on the sibling repo [Web-Data-Science-Book](https://github.com/cuinfoscience/Web-Data-Science-Book/tree/main/.github/ISSUE_TEMPLATE) and tuned for a novice audience: plain language, reassurance that the reporter does not need to know the fix, and as few required fields as each form can get away with. Quarto's `repo-actions: [issue]` puts a "Report an issue" link on every chapter page that lands on the chooser, so this is the front door most readers will use.

| Form | File | Label | Use |
|---|---|---|---|
| Something is wrong | `something-is-wrong.yml` | `broken` | A command fails, steps don't match the reader's computer, dead link, wrong fact |
| I'm stuck or confused | `im-stuck.yml` | `gap` | Missing or unclear explanation — **and** questions the book doesn't answer |
| Typo or quick fix | `typo.yml` | `typo` | Three fields; the lowest-friction form |
| Suggestion | `suggestion.yml` | `suggestion` | Improvements, including "Propose a new chapter or topic" as a kind |
| Accessibility problem | `accessibility.yml` | `accessibility` | Screen reader, keyboard, contrast, zoom, missing alt text |

`config.yml` disables blank issues and offers two contact links (read the book; not sure which form). Design decisions worth keeping: the "I searched existing issues" checkbox is present but **optional** on every form — a duplicate is cheap to close, a novice bouncing off a required box is a lost report. Questions were folded into the gap form rather than given their own, because GitHub Discussions is not enabled on this repo and a reader's question is itself a gap signal. Adding a sixth form should clear a high bar; the chooser is part of the accessibility surface.

**The chapter dropdown is generated.** Each form's "Which chapter?" options sit between `# BEGIN chapters` and `# END chapters` markers and are rebuilt from `_quarto.yml` plus each chapter's H1 by `tools/issue-forms/sync_issue_chapters.py` (stdlib only). Numbering matches the rendered book, with the Introduction as Chapter 1. Do not edit that block by hand; run the script after any chapter add, rename, or reorder, and `--check` in review to catch drift. Options outside the markers (e.g. "The book as a whole") are hand-maintained per form.

**Labels are not created automatically.** GitHub silently drops a form's labels if they do not exist in the repository. `.github/workflows/labels.yml` is a manual-trigger workflow that creates or refreshes all five with `gh label create --force`; run it once from the Actions tab after the forms land, and again if a label's color or description changes there. The workflow is the source of truth for label names and colors.

## Common Tasks

### Add a new chapter

1.  Create a file at `chapters/<slug>.qmd`.
2.  Start the file with `# Chapter Title {#sec-<slug>}`.
3.  Add the Prerequisites callout template (copy from any existing chapter).
4.  Follow the canonical 8-section structure above.
5.  Register the chapter in `_quarto.yml` under the appropriate `part:`.
6.  Run `python tools/issue-forms/sync_issue_chapters.py` so the chapter appears in the issue forms' "Which chapter?" dropdown (nothing in CI does this for you; `--check` tells you if it is stale).
7.  If the chapter introduces new vocabulary, add glossary terms to `appendix-glossary.qmd`.
8.  Run `quarto preview` and verify the sidebar and cross-references work.

### Add a cross-reference

1.  Confirm the target chapter has a `{#sec-<slug>}` on its H1 (all current chapters do; see the label table above).
2.  Write `@sec-<slug>` in the source chapter. Quarto auto-prefixes "Chapter" on render.
3.  Run `quarto render` and confirm no `Unable to resolve crossref` warnings.

### Add a figure

1.  Place the PNG in `graphics/`.
2.  Reference it with a **leading slash** on the path:

    ```markdown
    ![Short descriptive caption.](/graphics/filename.png){#fig-slug fig-alt="What a reader who cannot see the image needs to know."}
    ```

    The leading slash matters. Chapters live in `chapters/`, so a bare `graphics/filename.png` resolves against `chapters/` and renders as a broken link with no warning from Quarto. A `/`-prefixed path is resolved against the project root and rewritten per page. (The unfilled `PLACEHOLDER-*` references still use the bare form; fix the path when you fill one in.)

3.  Cross-reference it in prose with `@fig-slug`, and give every figure a `fig-alt`.
4.  Use `::: {.column-margin}` only for small, simple images. Anything with labels, callouts, or fine detail is illegible at margin width (300 CSS px, against about 680 px for the body column; `tools/layout-audit/` measures both) and belongs in the body column.

### Add a bibliography entry

1.  Add the BibTeX entry to `references.bib`.
2.  Cite with `[@key]` in the text.
3.  Quarto renders the full bibliography at the end of the book automatically.

---

## Backlog

The chapter backlog lives in `docs/roadmap.md`: the history of the gap analysis, the topics still waiting, and the review follow-ups that are still open. Each item there would be a reasonable first PR for a contributor. Follow the canonical chapter structure (see Style Guide), add a new chapter to `_quarto.yml` and to the label table above, and tick the item off in the roadmap in the same PR.

---

## CI/CD

`.github/workflows/build-book.yml` renders the book on every push to `main` and on pull requests against `main`, using the latest stable Quarto release (`quarto-dev/quarto-actions/setup@v2`). Pull requests run a render-only validation step (`quarto-dev/quarto-actions/render@v2`) and do not publish. Pushes to `main` (and manual `workflow_dispatch` runs) render and publish the book to GitHub Pages via `quarto-dev/quarto-actions/publish@v2` with `target: gh-pages`.

The minimum Quarto version is 1.9.0 (`llms-txt` requires it). If you need to pin a specific version for reproducibility, set `version:` in the workflow's `setup@v2` step.
