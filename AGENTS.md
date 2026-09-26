# Missing Manual for Information Scientists — agent instructions

Instructions for AI coding agents (Claude Code, Codex, and any other) and for people extending the book. This is the one instructions file: `CLAUDE.md` only imports it, and an agent that looks for its own file (`GEMINI.md`, `.cursorrules`, and so on) should read this one. Read it before making any changes.

People contributing for the first time start at `CONTRIBUTING.md`, the novice-facing guide; this file holds the detail behind it. The two, the issue forms, and the README link to each other, so when you change one (a form's name or label, the build prerequisites, a style rule), update the others in the same pull request.

---

## Project memory: `docs/`

The book's records live in `docs/`: after-action reports (AARs) and reviews, plans, the roadmap, the decision log, and the hand-off note. `docs/README.md` says how each kind is kept. They are how one session's lessons reach the next, so use them:

- **Before starting work,** read `docs/handoff.md` (where work stands: what is done, paused, waiting on the maintainer, or known to be broken) and `docs/decisions.md` (standing decisions and the reason for each). Don't reverse a recorded decision on your own; if you think one is wrong, say so and let the maintainer decide.
- **Before working in an area a record covers,** read that record. AARs and reviews are in `docs/aar/`, plans for larger work in `docs/plans/`, and the chapter backlog in `docs/roadmap.md`. For example, read the comprehensive review (`docs/aar/2026-04-27-comprehensive-review.md`) before restructuring a chapter it flagged, and before touching `tools/shots` or adding a screenshot, read "Patterns and pitfalls" in `tools/shots/README.md`, this book's screenshot AAR (`docs/aar/AAR_INFO-Missing-Manual_2026-09-24.md`), and the screenshot plan with the upstream AARs it links (in the companion book *Web Data Science*). Before rewriting a chapter's voice, read the voice plan (`docs/plans/2026-09-25-voice-rollout.md`: its brief, review steps, and lessons) and its AAR (`docs/aar/AAR_INFO-Missing-Manual_2026-09-25.md`); before starting any revision from the September 2026 peer review, read the revision plan (`docs/plans/2026-09-25-peer-review-revisions.md`) and the reviews it cites (`docs/aar/2026-09-25-peer-review.md`).
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

- **Quarto 1.10 or later** — https://quarto.org/docs/download/. CI uses the latest release (1.10.18 as of September 2026). Quarto 1.9.15 rejects the `website: llms-txt` key in `_quarto.yml` and won't build the book.
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
├── references.bib                   # BibTeX bibliography (51 entries)
├── CONTRIBUTING.md                  # the novice-facing contributing guide (start here as a person)
├── .github/
│   ├── workflows/build-book.yml     # CI: renders + publishes on push/PR
│   ├── workflows/labels.yml         # manual run: creates the labels the issue forms use
│   ├── ISSUE_TEMPLATE/              # five issue forms + chooser config (see "Issue templates")
│   └── pull_request_template.md     # short, optional checklist for pull requests
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
├── styles/layout.css                # one column layout for every chapter (see "Page layout")
├── graphics/                        # PNGs referenced from chapters
│   ├── memes/                       # generated chapter memes (PNG + .spec hash)
│   └── <slug>/                      # screenshots for one chapter, with provenance.json (tools/shots)
└── tools/                           # supporting code; every folder has a README
    ├── README.md                    # what each tool does and when it runs
    ├── requirements.txt             # what CI installs (empty: the meme generator is stdlib only)
    ├── chapter-meme/                # {{< chapter-meme >}} shortcode + memegen.link generator
    ├── terminal-figures/            # annotated terminal illustrations (HTML -> PNG)
    ├── issue-forms/                 # rebuilds the chapter dropdown in every issue form
    ├── shots/                       # screenshot toolkit, ported from Web-Data-Science-Book
    │   ├── recipes/                 # one YAML recipe per chapter with screenshots
    │   └── fixtures/                # pinned local programs to capture (JupyterLab, code-server)
    └── layout-audit/                # browser checks on a rendered book (TOC visibility, column widths, sideways scroll)
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

The book should read like a knowledgeable friend talking you through something, not like technical documentation. The maintainer set this in September 2026 (`docs/decisions.md`, 2026-09-25): informal, approachable, and welcoming to newcomers; honest about what confuses and frustrates people; never academic or formal; and still authoritative and persuasive. `chapters/tabular-data.qmd` is the model, rewritten as the pilot.

- **Talk to the reader.** Address them as **"you"** (not "the user," "the student," "one," or "a reader"). Contractions are fine. Be direct and imperative for instructions ("Run this command," "Check the version"), and non-judgmental about mistakes and questions.
- **Name the confusion before resolving it.** Most sections have a moment where newcomers get stuck: an error message that doesn't say what's wrong, a result that looks right and isn't, a term everyone uses and nobody defines. Say it out loud ("If that has happened to you, you're in good company"), then explain. Empathetic about frustration, high expectations about capability.
- **Tell it as a story, not a list of facts.** Open a section with the situation or the problem it solves, and let each paragraph follow from the last: why this matters, what goes wrong, how to do it, what to watch for. A sequence of steps can still be prose, with each step bolded at the start of its paragraph (see "Cleaning, one decision at a time" in `tabular-data`). Keep lists for material a reader scans: the "Why read this chapter" bullets, checklists, quick references, exercises, templates, and short sets of genuinely parallel options.
- **Persuade with reasons and examples, not formality.** Authority comes from explaining *why* and showing a concrete case (a row count that doubled, an error message, a real number), not from stiff phrasing. Avoid stock formal phrases: "it is important to note," "furthermore," "in order to," "utilize," "this chapter provides."
- **Link generously.** Link a tool to its official documentation, preferring its tutorial or user guide over the API reference when one exists, and link concepts to Wikipedia (primary key, sentinel value, ISO 8601, data lineage). Link on first mention in a chapter, not every time. Check that every new link resolves before the pull request (`curl -sL -o /dev/null -w '%{http_code}' <url>`), and don't repeat a link that the chapter's Further reading already has.
- **Every code block runs, and every fact holds.** When you rewrite a chapter, run its code (on made-up data if need be), make any output shown match what the code really prints, and fix what doesn't work; a friendly voice doesn't excuse a broken example. Check the facts you touch, too, and soften or cut what you can't source. Rewriting Part I this way found about thirty errors in seven chapters; `docs/plans/2026-09-25-voice-rollout.md` says how each part is done and reviewed.

### Canonical Chapter Structure

Every content chapter follows this structure:

1.  `# Chapter Title {#sec-<slug>}` (H1 with explicit section ID)
2.  **Prerequisites callout** (top of chapter, `::: {.callout-tip collapse="true"}`)
3.  `## Purpose {.unnumbered}` — one to three paragraphs explaining why this chapter exists
4.  `## Why read this chapter {.unnumbered}` — 5–8 bullets, each one sentence addressed to "you," naming a frustration, a snag, a use, or a gap that brings a novice-to-intermediate student to this chapter ("You merged two tables and ended up with more rows than you started with"). No intro line. It replaced the stodgy "Learning objectives" list in September 2026 (`docs/decisions.md`, 2026-09-25); `tabular-data` is the model
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

**Open on something specific to the chapter:** a case, an event, or an experience the reader has had. Read side by side in September 2026, fifteen sections opened with one of two stock moves ("X looks like neutral plumbing, but…" and "X is taught as Y, and it is. It is also…"), and most announced a count ("Three things to notice"); in a row they read as boilerplate. Don't add more of either. `package-management`, `version-control`, and `evaluating-ai` show the alternative. The closing sentence stays fixed, as the template shows.

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

Curation rules: 3–7 items per chapter, mix of books/articles, official docs, and community resources, one sentence of annotation each. Prefer durable sources (books, official docs, well-maintained community sites) over blog posts that will rot. Do not duplicate items already linked from the chapter body. New external resources go here as plain links rather than as new `references.bib` entries — the book uses `[@key]` citations sparingly (currently only `index.qmd`, `documentation.qmd`, `automation.qmd`, and `artifacts-have-politics.qmd`) to preserve the reference-handbook feel.

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

**Code blocks:** fenced blocks with a language hint where it helps highlighting. Shell commands install with `python -m pip` (or `%pip` in a notebook), so a package lands in the Python that runs it, and examples use Python 3.12 unless the version is the point (peer-review Phase 1, #70).

````markdown
```bash
pip install pandas
```

```python
df = pd.read_csv("data.csv")
```
````

**A code block that shows another code block** (a README with its commands, a notes file) needs a longer outer fence: open it with four backticks followed by the language (`markdown`) and close it with four backticks. Three won't do, because a closing fence may be indented up to three spaces, so an inner three-backtick fence indented under a list item ends the outer block early and the rest of the example renders as ordinary text, with no warning. `scripting` and `terminal` both had this until September 2026.

Non-executable code blocks are the default; the book does not currently use Jupyter/Python execution. If you add executable cells, use ` ```{python} ` and configure `execute: enabled: true`.

**Citations:**

```markdown
[@wilson2017goodenough]
[@wilson2017goodenough; @chacon2014progit]
```

Bibliography file: `references.bib` at the repo root. Bibliography rendering is handled automatically via `bibliography: references.bib` in `_quarto.yml`.

**Every reference is real, and every example entry is obviously fake.** A citation, a Further reading item, or a DOI must resolve to the work it names; check it (a DOI at `https://doi.org/<doi>`) before it goes in. A template or example that needs a sample entry uses placeholders (`Lastname, Firstname`, `Title of Your Paper`, DOI `10.1145/0000000.0000000`), never a made-up paper under a real person's name. The Part V rewrite found one of each: a Further reading item whose DOI returned 404 and whose authors were invented, and a template entry crediting the maintainer with a paper that doesn't exist.

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

- `_quarto.yml` top-level structure without a reason. In particular, do not remove the sibling `website: { llms-txt: true }` block; Quarto 1.9 has a bug where `llms-txt` under `book:` does not activate llms.txt generation, but under `website:` it does. See @sec-automation analog in the issue tracker if you want to upstream this. (Quarto 1.9.15 rejects the key under `website:` outright, which is why local builds need 1.10 or later.)
- Section ID prefixes. They are baked into cross-references across the book.
- The `shortcodes:` key in `_quarto.yml`. It is what loads `{{< chapter-meme >}}`.

---

## Chapter memes

Each chapter declares an optional meme in YAML frontmatter. On wide screens (992 px and up) the rendered PNG heads the right sidebar, directly above the table of contents; on narrower screens it appears at the top of the `## Purpose` section.

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

**Where the meme appears (issue #30).** A meme in the margin made Quarto collapse the table of contents on every chapter that had one, so the meme now has two copies:

- **Wide screens:** the chapter's `margin-header`, which Quarto places at the top of the right sidebar, above the table of contents. Quarto reads `margin-header` before any filter runs, so it can't be computed during a render: `tools/chapter-meme/sync_margin_header.py` writes it into the chapter's front matter from `meme:`, under a "do not edit" comment. **Run it after adding, removing, or editing a `meme:` block**; CI runs it with `--check` and fails if a chapter is stale.
- **Narrow screens,** where Quarto hides that sidebar: the shortcode's inline copy (class `chapter-meme-inline`, hidden at 992 px and up by Bootstrap's `d-lg-none`). Other output formats keep the old margin placement.
- Sizing is in `tools/chapter-meme/chapter-meme.css`, loaded from `_quarto.yml`.

**Keep the first screen of a chapter free of margin content.** Any margin note near the top (a footnote, since `reference-location: margin`, or a `.column-margin` block in Purpose) collapses the table of contents at load, just as the margin meme did. Link inline instead; `tools/layout-audit/audit.py toc` checks every page.

**How the shortcode is loaded.** `_quarto.yml` names it in a project-level `shortcodes:` key (`- tools/chapter-meme/chapter-meme.lua`), so it sits beside the script it calls instead of in an `_extensions/` folder. Don't remove that key: every chapter that calls `{{< chapter-meme >}}` would render the literal shortcode instead of its meme. (An earlier version of this file said the shortcode could only live under `_extensions/`; that was wrong. See `docs/decisions.md`, 2026-09-24.)

**Dependency.** The generator uses Python's standard library only (`urllib.request`); there is no `pip install` step. The build host needs outbound HTTPS to `api.memegen.link` on the first render after a meme's frontmatter changes; subsequent renders read the cached PNG and run offline. CI's GitHub Actions runners have outbound HTTPS by default, so no workflow changes are needed. See [memegen.link](https://github.com/jacebrowning/memegen) for template ids and font choices.

---

## Page layout: one width for every chapter

**Every chapter has the same column widths:** the body column is 678 CSS px in a 1280-px window (699 px at 1440 and wider), the table of contents is 300 px, and the left navigation is 226 px. Don't change these (the maintainer's rule, `docs/decisions.md`, 2026-09-25); make a figure smaller instead.

Quarto doesn't do this by itself. It gives a page a narrower body and a wider table of contents (the `slimcontent` class) when the page has anything in the right margin (a figure caption, since `fig-cap-location: margin`, or a footnote), so until September 2026 chapters without figures or footnotes rendered 100 px wider in the body. `styles/layout.css` gives every page the same grid, and also stops long URLs and code from widening a page past the window. After any change to the theme, `_quarto.yml`'s `format: html`, or `styles/`, render and run:

```bash
tools/shots/.venv/bin/python tools/layout-audit/audit.py widths
```

It fails if any page's columns differ from the rest, or if any page scrolls sideways, at 1024, 1280, 1440, and 1920 px. Run it again with `--widths 390` for a phone: a table wider than the screen makes a page scroll sideways there, and since #66 none does. Keep tables to three short columns where you can.

## Terminal figures

Chapters that show a shell session use generated illustrations rather than screen captures. [tools/terminal-figures/generate_terminal_figures.py](tools/terminal-figures/generate_terminal_figures.py) draws each figure as a small HTML page and renders it to PNG with headless Chromium at 2x on a 4:3 card, producing `graphics/<slug>.png`. The five current figures are `macos-terminal-annotated`, `windows-terminal-annotated` (both @sec-terminal), `ssh-connected` (@sec-remote-computing), `venv-prompt` (@sec-virtual-environments), and `pip-install-success` (@sec-pkg-mgmt).

```bash
python tools/terminal-figures/generate_terminal_figures.py           # regenerate all figures
python tools/terminal-figures/generate_terminal_figures.py --check   # fail if a PNG is stale
```

Figures are defined declaratively in the script's `FIGURES` dict: terminal lines plus numbered callouts positioned by character offset into a line. To add or edit one, change that dict and re-run. As with the memes, the PNGs are committed and CI never regenerates them — this is an authoring tool, not a build step.

Two constraints worth knowing before you touch it. **Use a headless-shell build of Chromium.** A full Chrome build reserves about 87px of the window height for browser chrome, so the bottom of every figure renders blank while the PNG is still emitted at full size; `check_viewport()` fails loudly rather than letting that ship. Set `$CHROME` if the automatic search picks the wrong binary. **Callout offsets are character positions,** which only works because the figures use DejaVu Sans Mono; changing the font family means re-deriving `CHAR_ADVANCE`.

Why not a recorder like [terminalizer](https://github.com/faressoft/terminalizer) or [asciinema](https://asciinema.org)? They emit animated GIF or SVG, which the PDF build cannot embed; they cannot draw the numbered callouts that carry the teaching; and a recording cannot show a Windows Terminal tab bar without a Windows machine to record on. [charmbracelet/freeze](https://github.com/charmbracelet/freeze) is the closest static alternative and worth revisiting if the book ever wants many unannotated output figures, at the cost of a Go dependency.

**Remaining `PLACEHOLDER-*` images.** Two placeholder PNGs, both in `operating-system`, still don't exist: the Windows and macOS About panels, which are hand captures on real machines. The other ten are real captures since September 2026: two JupyterLab views, a rendered DataFrame, this book's repository page, one of its CI jobs, the maintainer's hand capture of an API response in Firefox, two views of VS Code in the browser, and one review thread on this book's own pull request, shown open in `version-control` and resolved in `collaboration`. Unlike terminal sessions, these cannot be honestly simulated; they are real captures, made with `tools/shots` (next section) or, for the operating-system panels, by hand on a real machine. Which ones, in what order, is in `docs/plans/2026-09-24-screenshots.md`.

## Screenshots

Screenshots of real pages and programs are made with `tools/shots`, a toolkit ported from the companion book *Web Data Science*: a YAML recipe per chapter (`tools/shots/recipes/<slug>.yml`), guarded capture in Chrome for Testing, review at the size the book shows each figure, and `promote` into `graphics/<slug>/` with a `provenance.json` record. `tools/shots/README.md` is the manual; `tools/shots/UPSTREAM.md` lists what differs from upstream. Follow the rollout in `docs/plans/2026-09-24-screenshots.md`: the pilot (`jupyter`, plus the DataFrame figure in `pandas-basics`) is done, and each remaining chapter gets its own pull request.

**Before writing a recipe, read "Patterns and pitfalls" in `tools/shots/README.md`.** It is the short list of what the captures so far have taught: how to choose the window and the column, how to get the same take twice from an application that remembers state, and how to keep interface state out of a crop. The [screenshot AAR](docs/aar/AAR_INFO-Missing-Manual_2026-09-24.md) tells the story behind each rule, and `tools/shots/recipes/jupyter.yml` is a worked example with a comment beside each workaround. When a capture teaches you something new, add it to "Patterns and pitfalls", and as a comment in the recipe, in the same pull request.

- **Real or labeled.** A screenshot is a real capture of a real page or program. Never rebuild a real interface by hand with invented content. Diagrams and illustrations are welcome, labeled as what they are; a figure drawn to look like a window (the terminal figures) says so in its caption.
- **Readable, and not crammed.** A figure shows at most **800×600 CSS pixels** of the screen by default. It may show up to **1024×768** when the larger view **reduces clutter** (a site's desktop layout instead of its narrow one, or enough of the page around the subject that a reader can find it) **and its text still passes the legibility check** where the book shows it. The recipe says why in `relaxed:`, and `tools/shots` checks the text. This book's body column is only 678 px wide, so a 1024-px figure's text shrinks to 66% there: a relaxed figure usually goes in a wider Quarto column (`.column-page-inset-right`, 954 px) and names that column in its recipe. Wider columns cover the table of contents while they are on screen, so use them only where a figure needs one. Anything larger than 1024×768 is an exception, explained in `oversize:`.
- **Scope first.** Crop to what the text discusses before reaching for a bigger view; for DevTools, zoom DevTools rather than widen the window.
- **Honest and private.** Captures identify themselves with one User-Agent (`tools/shots/lib/recipes.py`) and pace their requests. No logins, no credentials, no student names or student work, and nothing from the capture machine (a proxy's address, an IP, a location) in frame. A figure that must show people's names or faces, such as a review thread, blurs them with the recipe's `blur:` key and says so in its caption (`docs/decisions.md`, 2026-09-25).
- **Programs come from a pinned local fixture.** A program that runs on your own computer (JupyterLab, and VS Code as code-server) is captured from a fixture in `tools/shots/fixtures/<name>/`: pinned versions, made-up data, a scratch copy of the project, settings that silence first-run prompts, and start and stop scripts. Never capture your own setup or a live account, and start every capture from a known state (for JupyterLab, `?reset` on the URL, and a fresh `start.sh` before each full set of captures, since kernels outlive captures). `tools/shots/fixtures/jupyter/` is the model.
- **Dated and described.** A figure of something that changes says in its caption when it was captured ("in September 2026"). Every figure has `fig-alt` that transcribes the text and numbers a reader needs from it; 280–440 characters is a good target for a screenshot. Write both from the capture itself, not from the placeholder's description, which describes a screen someone imagined, and read the figure against the paragraph beside it: no check catches a figure that contradicts its text.
- **Checked.** Before a pull request that adds or changes a screenshot, capture the chapter's whole recipe file again (`tools/shots/run capture <slug>`), since one figure's steps can leave state that breaks the next; run `tools/shots/run sheet <slug>` and look at every take at book size, including the crop's edges; then run `tools/shots/run check`. After changing the toolkit, run `tools/shots/run selftest`; every check must pass, and one real figure must be retaken before the change counts as done.

## Issue templates

Readers report problems through GitHub **issue forms** in `.github/ISSUE_TEMPLATE/` — structured YAML forms with dropdowns and required fields, not free-text markdown templates. They were modelled on the sibling repo [Web-Data-Science-Book](https://github.com/cuinfoscience/Web-Data-Science-Book/tree/main/.github/ISSUE_TEMPLATE) and tuned for a novice audience: plain language, reassurance that the reporter does not need to know the fix, and as few required fields as each form can get away with. Quarto's `repo-actions: [issue]` puts a "Report an issue" link on every chapter page that lands on the chooser, so this is the front door most readers will use.

| Form | File | Label | Use |
|---|---|---|---|
| Something is wrong | `something-is-wrong.yml` | `broken` | A command fails, steps don't match the reader's computer, dead link, wrong fact |
| I'm stuck or confused | `im-stuck.yml` | `gap` | Missing or unclear explanation — **and** questions the book doesn't answer |
| Typo or quick fix | `typo.yml` | `typo` | Three fields; the lowest-friction form |
| Suggestion | `suggestion.yml` | `suggestion` | Improvements, including "Propose a new chapter or topic" as a kind |
| Accessibility problem | `accessibility.yml` | `accessibility` | Screen reader, keyboard, contrast, zoom, missing alt text |

`config.yml` disables blank issues and offers three contact links (read the book; fix it yourself, which opens `CONTRIBUTING.md`; not sure which form). The *Typo* form's intro points to the browser-editing route in `CONTRIBUTING.md`, and *Something is wrong* and *Suggestion* end with an optional "I would like to fix/make this myself" box, so a report can come with a volunteer. Design decisions worth keeping: the "I searched existing issues" checkbox is present but **optional** on every form — a duplicate is cheap to close, a novice bouncing off a required box is a lost report. Questions were folded into the gap form rather than given their own, because GitHub Discussions is not enabled on this repo and a reader's question is itself a gap signal. Adding a sixth form should clear a high bar; the chooser is part of the accessibility surface.

**The chapter dropdown is generated.** Each form's "Which chapter?" options sit between `# BEGIN chapters` and `# END chapters` markers and are rebuilt from `_quarto.yml` plus each chapter's H1 by `tools/issue-forms/sync_issue_chapters.py` (stdlib only). Numbering matches the rendered book, with the Introduction as Chapter 1. Do not edit that block by hand; run the script after any chapter add, rename, or reorder. CI runs it with `--check` and fails the build if a form is stale. Options outside the markers (e.g. "The book as a whole") are hand-maintained per form.

**Labels are not created automatically.** GitHub silently drops a form's labels if they do not exist in the repository. `.github/workflows/labels.yml` is a manual-trigger workflow that creates or refreshes all five with `gh label create --force`; run it once from the Actions tab after the forms land, and again if a label's color or description changes there. The workflow is the source of truth for label names and colors.

## Common Tasks

### Add a new chapter

1.  Create a file at `chapters/<slug>.qmd`.
2.  Start the file with `# Chapter Title {#sec-<slug>}`.
3.  Add the Prerequisites callout template (copy from any existing chapter).
4.  Follow the canonical 8-section structure above.
5.  Register the chapter in `_quarto.yml` under the appropriate `part:`.
6.  If the chapter has a `meme:` block, run `python tools/chapter-meme/sync_margin_header.py`. Then run `python tools/issue-forms/sync_issue_chapters.py` so the chapter appears in the issue forms' "Which chapter?" dropdown. CI runs both with `--check` and fails if either is stale, but neither fixes itself.
7.  If the chapter introduces new vocabulary, add glossary terms to `appendix-glossary.qmd`.
8.  Run `quarto preview` and verify the sidebar and cross-references work.

### Add a cross-reference

1.  Confirm the target chapter has a `{#sec-<slug>}` on its H1 (all current chapters do; see the label table above).
2.  Write `@sec-<slug>` in the source chapter. Quarto auto-prefixes "Chapter" on render.
3.  Run `quarto render` and confirm no `Unable to resolve crossref` warnings.

### Add a figure

1.  Place the PNG in `graphics/`. (A screenshot goes through `tools/shots` instead, which puts it in `graphics/<slug>/` with its provenance; see "Screenshots".)
2.  Reference it with a **leading slash** on the path:

    ```markdown
    ![Short descriptive caption.](/graphics/filename.png){#fig-slug fig-alt="What a reader who cannot see the image needs to know."}
    ```

    The leading slash matters. Chapters live in `chapters/`, so a bare `graphics/filename.png` resolves against `chapters/` and renders as a broken link with no warning from Quarto. A `/`-prefixed path is resolved against the project root and rewritten per page. (The unfilled `PLACEHOLDER-*` references still use the bare form; fix the path when you fill one in.)

3.  Cross-reference it in prose with `@fig-slug`, and give every figure a `fig-alt`. A Mermaid diagram (a ```` ```{mermaid} ```` block) is the exception: Quarto doesn't pass `fig-alt` through to it, so put `accTitle:` and `accDescr:` lines inside the diagram, which Mermaid writes into the drawing for screen readers (see `documentation.qmd`).
4.  Use `::: {.column-margin}` only for small, simple images. Anything with labels, callouts, or fine detail is illegible at margin width (300 CSS px, against about 680 px for the body column; `tools/layout-audit/` measures both) and belongs in the body column.

### Add a bibliography entry

1.  Add the BibTeX entry to `references.bib`.
2.  Cite with `[@key]` in the text.
3.  Quarto renders the full bibliography at the end of the book automatically.

---

## Backlog

The chapter backlog lives in `docs/roadmap.md`: the history of the gap analysis, the topics still waiting, and the review follow-ups that are still open. Each item there would be a reasonable first PR for a contributor. Follow the canonical chapter structure (see Style Guide), add a new chapter to `_quarto.yml` and to the label table above, and tick the item off in the roadmap in the same PR.

The next large piece of work is the revision planned after the September 2026 peer review (`docs/plans/2026-09-25-peer-review-revisions.md`). Its Phase 1 corrections can start any time; the other phases wait on eight decisions the maintainer hasn't made yet, listed at the top of the plan and in `docs/handoff.md`. Don't make those decisions for them: a new chapter, a reordered part, or a running example changes the book's shape for every reader and every course that assigns it.

---

## CI/CD

`.github/workflows/build-book.yml` renders the book on every push to `main` and on pull requests against `main`, using the latest stable Quarto release (`quarto-dev/quarto-actions/setup@v2`). Pull requests run a render-only validation step (`quarto-dev/quarto-actions/render@v2`) and do not publish. Pushes to `main` (and manual `workflow_dispatch` runs) render and publish the book to GitHub Pages via `quarto-dev/quarto-actions/publish@v2` with `target: gh-pages`.

CI installs the latest Quarto release (1.10.18 as of September 2026). Local builds need 1.10 or later, since Quarto 1.9.15 rejects `website: llms-txt`. If you need to pin a specific version for reproducibility, set `version:` in the workflow's `setup@v2` step.
