# CLAUDE.md — Missing Manual for Information Scientists

This file guides Claude Code sessions working on this repository. Read it before making any changes.

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
- `book/index.html` opens and the sidebar lists all six parts with their chapters.
- `book/llms.txt` exists and enumerates all chapters.
- At least a handful of `@sec-*` cross-references resolve (click through in HTML).
- Optional, local only: `quarto render --to pdf` renders without LaTeX errors (requires TinyTeX).

---

## Repository Structure

```
ParatechnicalComputingHandbook/
│
├── _quarto.yml                      # book config (HTML + PDF, llms-txt: true)
├── index.qmd                        # landing page (Introduction)
├── conclusion.qmd                   # final chapter
├── appendix-glossary.qmd            # Appendix A (glossary with term anchors)
├── references.bib                   # BibTeX bibliography (22 entries)
├── .github/workflows/build-book.yml # CI: renders HTML + PDF on push/PR
│
├── parts/
│   ├── part-1-practice/             # Part I — Practice of Technical Work
│   │   ├── questions.qmd
│   │   ├── documentation.qmd
│   │   ├── common-formats.qmd
│   │   ├── reading-docs.qmd
│   │   ├── debugging.qmd
│   │   ├── tracebacks.qmd
│   │   └── artifacts-have-politics.qmd
│   ├── part-2-environment/          # Part II — Computing Environment
│   │   ├── operating-system.qmd
│   │   ├── file-system.qmd
│   │   ├── terminal.qmd
│   │   ├── text-editors.qmd
│   │   └── remote.qmd
│   ├── part-3-python/               # Part III — Python Management
│   │   ├── package-management.qmd
│   │   ├── virtual-environments.qmd
│   │   ├── jupyter.qmd
│   │   ├── scripting.qmd
│   │   ├── regex.qmd
│   │   └── linting.qmd
│   ├── part-4-data/                 # Part IV — Working with Data
│   │   ├── data-file-formats.qmd
│   │   ├── tabular-data.qmd
│   │   ├── pandas-basics.qmd
│   │   ├── sql-basics.qmd
│   │   └── http-apis.qmd
│   ├── part-5-projects/             # Part V — Project Management
│   │   ├── project-management.qmd
│   │   ├── version-control.qmd
│   │   ├── collaboration.qmd
│   │   ├── automation.qmd
│   │   └── secrets.qmd
│   └── part-6-algorithmic/          # Part VI — Algorithmic Systems
│       ├── ai-llm.qmd
│       ├── llm-internals.qmd
│       ├── ai-agents.qmd
│       └── evaluating-ai.qmd
│
└── graphics/                        # PNGs referenced from chapters
```

**Naming rules:**

- Directory slugs: lowercase, hyphens, `part-N-<topic>` (no spaces, no uppercase).
- Chapter file slugs: lowercase, hyphens (`virtual-environments.qmd`, not `virtual_environments.qmd` — underscores collide with Quarto's section-ID syntax).
- Section IDs: `{#sec-<slug>}`, matching the chapter file name without the extension.

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
7.  `## Worked examples` — numbered subsections
8.  `## Templates` — reusable snippets (optional, varies by chapter)
9.  `## Exercises` — numbered list
10. `## One-page checklist` — bullet list for quick reference
11. `## Quick reference: ...` — tables and one-liners (optional)

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
A [virtual environment](../../appendix-glossary.qmd#term-virtual-environment) is...
```

Each glossary term in `appendix-glossary.qmd` has an explicit `{#term-<slug>}` anchor. Use these sparingly — link only on first use in a chapter.

### What Not to Change

- `_quarto.yml` top-level structure without a reason. In particular, do not remove the sibling `website: { llms-txt: true }` block; Quarto 1.9 has a bug where `llms-txt` under `book:` does not activate llms.txt generation, but under `website:` it does. See @sec-automation analog in the issue tracker if you want to upstream this.
- Section ID prefixes. They are baked into cross-references across the book.

---

## Common Tasks

### Add a new chapter

1.  Create a file at `parts/part-N-<topic>/<slug>.qmd`.
2.  Start the file with `# Chapter Title {#sec-<slug>}`.
3.  Add the Prerequisites callout template (copy from any existing chapter).
4.  Follow the canonical 8-section structure above.
5.  Register the chapter in `_quarto.yml` under the appropriate `part:`.
6.  If the chapter introduces new vocabulary, add glossary terms to `appendix-glossary.qmd`.
7.  Run `quarto preview` and verify the sidebar and cross-references work.

### Add a cross-reference

1.  Confirm the target chapter has a `{#sec-<slug>}` on its H1 (all current chapters do; see the label table above).
2.  Write `@sec-<slug>` in the source chapter. Quarto auto-prefixes "Chapter" on render.
3.  Run `quarto render` and confirm no `Unable to resolve crossref` warnings.

### Add a figure

1.  Place the PNG in `graphics/`.
2.  Reference it with:

    ```markdown
    ::: {.column-margin}
    ![Short descriptive caption.](graphics/filename.png){#fig-slug}
    :::
    ```

3.  Cross-reference it in prose with `@fig-slug`.

### Add a bibliography entry

1.  Add the BibTeX entry to `references.bib`.
2.  Cite with `[@key]` in the text.
3.  Quarto renders the full bibliography at the end of the book automatically.

---

## Gap Chapter Backlog

The handbook's original gap analysis identified 16 candidate chapters. The first round added three high-priority chapters that survived (`tracebacks`, `virtual-environments`, `data-file-formats`); a fourth, on testing with pytest, was drafted but later removed because the topic was outside the handbook's intended audience. The second round added eight more: `reading-docs`, `regex`, `linting`, `tabular-data`, `pandas-basics`, `sql-basics`, `http-apis`, and `secrets`. (Pre-commit hooks were originally drafted as a separate chapter, then condensed into a section of `automation.qmd` because the standalone treatment was too detailed for the intended audience.) The third round added `common-formats` (Markdown, YAML, JSON syntax) and moved `ai-llm` from Part I to Part VI (Algorithmic Systems), where it sits alongside the other AI chapters. The following topics remain as candidates for future work.

**Lower priority (but valuable):**

- **Data dictionary / schema docs** — new section in `project-management.qmd` covering column documentation and schema change tracking.
- **Shell scripting (bash `.sh`)** — expand `automation.qmd` with a section on writing `.sh` scripts with control flow, exit codes, and error handling.
- **Profiling / performance (`%%timeit`, `cProfile`)** — add to `jupyter.qmd` or a new short chapter in Part III.
- **Containers / Docker intro** — add to `automation.qmd` or a stand-alone chapter: what a container is, why it matters for reproducibility, when to reach for one.
- **Stack Overflow hygiene** — add to `questions.qmd`.

Each of the above would be a reasonable first PR for a contributor. Follow the canonical 8-section structure (see Style Guide) and add the chapter to `_quarto.yml` + the label table above.

---

## CI/CD

`.github/workflows/build-book.yml` renders the book on every push to `main` and on pull requests against `main`, using the latest stable Quarto release (`quarto-dev/quarto-actions/setup@v2` with `version: release`). The rendered `book/` output is uploaded as an artifact named `paratechnical-computing-handbook` and retained for 30 days. On pushes to `main`, the workflow also publishes the book to GitHub Pages by pushing `book/` to the `gh-pages` branch (`quarto-dev/quarto-actions/publish@v2`, `target: gh-pages`). PRs are render-only and do not publish.

The minimum Quarto version is 1.9.0 (`llms-txt` requires it). If you need to pin a specific version for reproducibility, set `version:` in the workflow's `setup@v2` step.
