# Roadmap

The chapter backlog, and follow-ups from reviews that are still open. Each item would make a reasonable first PR for a contributor. When one lands, tick it off here with the PR number in the same pull request; when a new candidate comes up, add it with a line on where it would go. Plans for larger pieces of work are in [`plans/`](plans/), and what is actively in progress is in [`handoff.md`](handoff.md).

New chapters follow the canonical structure in `AGENTS.md` ("Style Guide"), get registered in `_quarto.yml` and the label table in `AGENTS.md`, and need the issue forms' chapter dropdown regenerated.

## Planned work

Larger pieces with a written plan, waiting on the maintainer's decisions (listed in each plan and in [`handoff.md`](handoff.md)):

- [ ] **Screenshots for the twelve placeholders**, then the interface-heavy chapters, with `tools/shots`: [`plans/2026-09-24-screenshots.md`](plans/2026-09-24-screenshots.md). The pilot (M1) replaced three in the pull request that fixed #30: two JupyterLab views in `jupyter` and the rendered DataFrame in `pandas-basics`. M2 added the repository page (`version-control`), the Actions job (`automation`), and the API response (`http-apis`, a hand capture); M4 added the two VS Code views (`text-editors`, `linting`) from a code-server fixture. Four remain, in three chapters.
- [x] **The table of contents below the chapter meme** ([#30](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/30)): [`plans/2026-09-24-toc-below-meme.md`](plans/2026-09-24-toc-below-meme.md). Done in the pull request that closed #30 (September 2026).
- [x] **Cloud storage, sync, and your disk** ([#34](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/34)), in chapters 9 and 10: [`plans/2026-09-24-cloud-storage-sections.md`](plans/2026-09-24-cloud-storage-sections.md). Done in the pull request that closed #34 (September 2026); the plan's optional folding of chapter 10's trailing sections is still open below.

## Chapter and section candidates

In the maintainer's order of priority (September 2026). All of them come after the screenshots and the polish of existing chapters (see "Order of work" in [`decisions.md`](decisions.md)).

### 1. Debugging and Git, the next level

- [ ] **Interactive debuggers (`pdb`, IDE breakpoints)** — extend `debugging.qmd` with a section on stepping through code interactively rather than relying solely on print statements.
- [ ] **Second-week Git (rebase, cherry-pick, reflog)** — extend `version-control.qmd` with the operations that show up in real collaboration once the basic add/commit/push loop is fluent.

### 2. Cloud notebooks and data too big for memory

- [ ] **Cloud notebooks (Colab, Kaggle, Codespaces)** — add to `jupyter.qmd` or `remote.qmd`: what each platform is good for, how their environments differ from a local venv, and gotchas around persistence, secrets, and GPU access.
- [ ] **Out-of-memory data (chunked CSV, line-delimited JSON, Polars/DuckDB)** — extension of `data-file-formats.qmd`: when to graduate from `pd.read_csv` to chunking, streaming, or a different tool entirely.

### 3. Documenting and licensing data

- [ ] **Data dictionary / schema docs** — new section in `project-management.qmd` covering column documentation and schema change tracking.
- [ ] **Data ethics and licensing** — possible new chapter or section in `artifacts-have-politics.qmd` covering data licenses (CC-BY, ODbL, terms of use), citation of datasets, and the ethics of scraping vs. downloading from a published source.

### 4. The rest

- [ ] **Profiling / performance (`%%timeit`, `cProfile`)** — add to `jupyter.qmd`, or a new short chapter in Part III.
- [ ] **Reproducible randomness** — short section (likely in `pandas-basics.qmd` or `tabular-data.qmd`) on `np.random.default_rng(seed)`, why globals like `np.random.seed` are insufficient for parallel work, and how to thread a seed through a pipeline.
- [ ] **Diagram literacy (Mermaid, ER, sequence)** — add to `documentation.qmd` or a new short chapter: how to read and produce ER diagrams, sequence diagrams, and architecture sketches as part of writing for technical audiences.
- [ ] **Editor automation (snippets, format-on-save, multi-cursor)** — extend `text-editors.qmd`: the keystrokes and configurations that turn an editor from a notepad into a tool.

## Open follow-ups from the comprehensive review

From [`aar/2026-04-27-comprehensive-review.md`](aar/2026-04-27-comprehensive-review.md), checked against the chapters in September 2026.

- [x] **`file-system.qmd` trailing legacy sections.** Folded in September 2026: copying a full path went into the Windows and macOS navigation sections, where downloads land into "Organizing work" (with links to each browser's own help instead of four outdated screenshots), and unzipping into "File operations and safety". The repeated Finder and File Explorer walkthroughs, the first-person paths example, and the orphaned footnotes were cut.
- [x] **`terminal.qmd` trailing section.** Folded in September 2026: the PowerShell translation notes (`Get-Location`, `Get-Help`, pipes that pass objects) now sit where the chapter tells you to check which shell you are in.
- [ ] **`package-management.qmd` empty stubs.** Six heading-only sections (`## Downloading` through `## Environments`) still sit before Further reading. Delete them; the body covers the material.
- [ ] **`jupyter.qmd` empty heading.** `## Quick reference: IPython conveniences` has no body. Fill it or delete it.
- [ ] **`presenting.qmd` duplicate table.** The timing-across-formats table appears in Worked examples and again as the Quick reference. Keep one.
- [ ] **Stakes voice check.** Read three or four Stakes sections from different parts in a row; if the shared template reads as boilerplate, vary the opening paragraph in two or three tier-1 chapters.
- [ ] **Inline glossary links.** Link the five terms the review added to the glossary (algorithmic audit, Matilda effect, open access, RLHF, schema) on first use in the chapters that introduce them.

## How the backlog got here

The handbook's original gap analysis identified 16 candidate chapters. The first round added three high-priority chapters that survived (`tracebacks`, `virtual-environments`, `data-file-formats`); a fourth, on testing with pytest, was drafted but later removed because the topic was outside the handbook's intended audience. The second round added eight more: `reading-docs`, `regex`, `linting`, `tabular-data`, `pandas-basics`, `sql-basics`, `http-apis`, and `secrets`. (Pre-commit hooks were originally drafted as a separate chapter, then condensed into a section of `automation.qmd` because the standalone treatment was too detailed for the intended audience.) The third round added `common-formats` (Markdown, YAML, JSON syntax) and moved `ai-llm` from Part I to the Algorithmic Systems part, where it sits alongside the other AI chapters. The fourth round added a new **Part V — Communication** with five chapters: `reading-scholarship`, `writing-manuscripts`, `writing-thesis`, `presenting`, and `latex`; this pushed Project Management to Part VI and Algorithmic Systems to Part VII. The fifth round folded four standing backlog items into existing chapters rather than creating new ones: a Stack Overflow section in `questions.qmd` (search-first habits, asking norms, what gets a question closed); a `wget`/`curl` section in `http-apis.qmd` (CLI fetches before Python, when to use which); a Docker / containers section in `virtual-environments.qmd` (when venvs are not enough, minimal Dockerfile, when *not* to reach for a container); and a substantially expanded shell-scripting section in `automation.qmd` covering `set -euo pipefail`, control flow, functions, exit-code conventions, and `trap`-based cleanup, with a short pointer from `terminal.qmd`.

Since then, work has gone into existing chapters rather than new ones: deeper Markdown coverage in `common-formats.qmd` (#27) and an "Opening a terminal" walkthrough in `terminal.qmd` (#28).
