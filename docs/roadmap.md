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

- [x] **Interactive debuggers (`pdb`, IDE breakpoints)** — added to `debugging.qmd` in September 2026: `breakpoint()` with a real `pdb` session, the commands, post-mortem debugging (`python -m pdb`, `%debug`), conditional breakpoints and logpoints, and keeping breakpoints out of commits (Ruff's `T100`). A glossary entry for *breakpoint*.
- [x] **Second-week Git (rebase, cherry-pick, reflog)** — added to `version-control.qmd` in September 2026 as "The second week": the reflog, `git stash`, `git cherry-pick`, `git rebase` (with its conflicts and `ORIG_HEAD`), and `git rebase -i`, with transcripts from a practice repository. The chapter's Worked examples are still one-line outlines; filling them in would be a good follow-up.

### 2. Cloud notebooks and data too big for memory

- [x] **Cloud notebooks (Colab, Kaggle, Codespaces)** — added to `jupyter.qmd` in September 2026 as "Notebooks on someone else's computer": a comparison table, then persistence, environments, secrets (each platform's own store), GPUs, and what not to upload; `remote.qmd` points to it. The same pull request filled `jupyter`'s empty Exercises heading. Limits were checked against each platform's docs in September 2026; re-check them when the chapter is next reviewed.
- [x] **Out-of-memory data (chunked CSV, line-delimited JSON, Polars/DuckDB)** — added to `data-file-formats.qmd` in September 2026 as "Data bigger than memory": how much memory a file needs (measured in pandas 3.0 and 2.2), then read less, read in chunks, convert to Parquet, and DuckDB or Polars, with a table of measured time and memory.

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
- [x] **`package-management.qmd` empty stubs.** Deleted in September 2026. The stranded paragraph after the Quick reference (Anaconda or Miniconda; where conda can't be installed) moved into "Choosing tools" with its diagram, and its footnotes became links.
- [x] **`jupyter.qmd` empty heading.** Filled in September 2026 with a table of the IPython conveniences the chapter teaches.
- [x] **`presenting.qmd` duplicate table.** The copy in Templates was removed in September 2026; the Quick reference keeps it.
- [ ] **pandas 3 text columns.** pandas 3.0 (the current release in September 2026) reads text as the `str` dtype, not `object`, so advice such as "if a numeric column shows up as `object`, you have hidden strings" is out of date for new installs. About eight passages in `data-file-formats`, `tabular-data`, `debugging`, and `questions` say `object`; each should say what both versions show.
- [x] **Stakes voice check.** Read side by side in September 2026: the content is specific, but fifteen openings used one of two stock moves. `package-management`, `version-control`, and `evaluating-ai` now open on a concrete case, and `AGENTS.md` asks new chapters to do the same ([`decisions.md`](decisions.md)).
- [x] **Inline glossary links.** Linked in September 2026 on first use: auditing in `evaluating-ai`, Matilda effects in `writing-manuscripts`, open access in `reading-scholarship`, RLHF in `ai-llm` and `ai-agents`, and schema in `sql-basics`. The RLHF entry now points to `ai-agents` instead of `llm-internals`, which never mentions it.

## How the backlog got here

The handbook's original gap analysis identified 16 candidate chapters. The first round added three high-priority chapters that survived (`tracebacks`, `virtual-environments`, `data-file-formats`); a fourth, on testing with pytest, was drafted but later removed because the topic was outside the handbook's intended audience. The second round added eight more: `reading-docs`, `regex`, `linting`, `tabular-data`, `pandas-basics`, `sql-basics`, `http-apis`, and `secrets`. (Pre-commit hooks were originally drafted as a separate chapter, then condensed into a section of `automation.qmd` because the standalone treatment was too detailed for the intended audience.) The third round added `common-formats` (Markdown, YAML, JSON syntax) and moved `ai-llm` from Part I to the Algorithmic Systems part, where it sits alongside the other AI chapters. The fourth round added a new **Part V — Communication** with five chapters: `reading-scholarship`, `writing-manuscripts`, `writing-thesis`, `presenting`, and `latex`; this pushed Project Management to Part VI and Algorithmic Systems to Part VII. The fifth round folded four standing backlog items into existing chapters rather than creating new ones: a Stack Overflow section in `questions.qmd` (search-first habits, asking norms, what gets a question closed); a `wget`/`curl` section in `http-apis.qmd` (CLI fetches before Python, when to use which); a Docker / containers section in `virtual-environments.qmd` (when venvs are not enough, minimal Dockerfile, when *not* to reach for a container); and a substantially expanded shell-scripting section in `automation.qmd` covering `set -euo pipefail`, control flow, functions, exit-code conventions, and `trap`-based cleanup, with a short pointer from `terminal.qmd`.

Since then, work has gone into existing chapters rather than new ones: deeper Markdown coverage in `common-formats.qmd` (#27) and an "Opening a terminal" walkthrough in `terminal.qmd` (#28).
