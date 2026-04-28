# Comprehensive review — audit report

This file consolidates the audit findings from the comprehensive review of the *Missing Manual for Information Scientists* carried out across PRs #15–#21. It captures items that were deferred from each part PR rather than fixed inline, plus cross-cutting connectivity findings, recommended `CLAUDE.md` updates, and a list of backlog candidates that remain open.

The goal of this report is not to dictate what gets fixed next. It is to make every deferred decision visible so the author can triage in one place rather than scrolling through seven PR descriptions.

---

## Scope of the review (what was delivered)

The review followed the plan in [`plans/perform-a-comprehensive-review-prancy-neumann.md`](.claude/plans/perform-a-comprehensive-review-prancy-neumann.md) (out of repo) and produced:

- **One PR per part**, in seven parts: I → II → III → IV → V → VI → VII.
- **Stakes and politics sections** in every content chapter (37 of 38; the cornerstone `artifacts-have-politics.qmd` was intentionally left in its essay shape). Each section is 150–300 words (tier-1) or 150–200 words (tier-3), grounded in 2–3 chapter-specific decisions, and cross-references `@sec-artifacts-politics`.
- **Further reading callouts** standardized across all 38 chapters: relocated to the very end of each chapter, expanded to 3–8 curated annotated items.
- **Targeted structural fixes** flagged by the structural audit:
  - `terminal.qmd`: added the missing `## Running theme: see before you act` section.
  - `ai-llm.qmd`: added the missing `## Running theme: AI can propose; you must verify` section; renamed `## Case studies` → `## Worked examples` for canonical conformance.
  - `debugging.qmd`: renamed `## Case studies` → `## Worked examples`.
  - `file-system.qmd`: added cross-refs to `@sec-scripts-vs-notebooks` and `@sec-git-github` (the audit flagged it for low outbound-cross-ref count).
  - `llm-internals.qmd` and `evaluating-ai.qmd`: added reciprocal cross-refs to/from the other AI chapters; the audit flagged both as isolated.

The cornerstone chapter `artifacts-have-politics.qmd` now has **inbound cross-references from every other content chapter** via the new Stakes sections. That is the largest connectivity change in the review.

---

## Deferred for follow-up — judgment calls

These items were noticed during the review but pushed to the audit report because they involve content judgment calls that the inline-vs-report threshold (per the plan) reserved for the author. None of them block the work that has shipped.

### 1. Legacy/orphan content predating the canonical structure

Several chapters carry trailing legacy sections that were drafted before the canonical 8-section template was adopted, and that were not in scope for this review.

- [parts/part-2-environment/file-system.qmd](parts/part-2-environment/file-system.qmd:329) — roughly 100 lines of legacy content at the end (post-Quick-reference): orphan paragraphs about Finder and File Explorer (the same material is covered better in the body of the chapter), a section on changing browser download locations for Chrome/Safari/Firefox/Edge, a section on unzipping files. **Recommendation:** delete or fold into the body. Most of the content is duplicated by earlier sections of the same chapter.
- [parts/part-2-environment/terminal.qmd](parts/part-2-environment/terminal.qmd:870) — three trailing sections that pre-date the canonical structure: `## Windows notes: PowerShell and WSL (optional)`, `## What is a terminal?`, `## What terminal commands should I know, as a basic foundation?`. The third has only an empty bullet list. **Recommendation:** delete the orphan sections; the canonical body of the chapter already covers this material.
- [parts/part-3-python/package-management.qmd](parts/part-3-python/package-management.qmd:756) — a block of empty stub sections at the bottom: `## Downloading`, `## Installation`, `## Installing libraries`, `## Maintaining libraries`, `## Removing libraries`, `## Environments`. Most are heading-only with no body. **Recommendation:** delete; the canonical body of the chapter covers all of this.
- [parts/part-3-python/jupyter.qmd](parts/part-3-python/jupyter.qmd:660) — the chapter ended at an empty `## Quick reference: IPython conveniences` heading with no body content (PR #17 added the Further reading callout below it, which now anchors the end of the chapter). **Recommendation:** either fill in the IPython conveniences quick reference or delete the heading.
- [parts/part-5-communication/presenting.qmd](parts/part-5-communication/presenting.qmd) — the timing-across-formats table appears twice (once in Worked examples, once in Quick reference), with identical content. **Recommendation:** keep one and delete the other.

### 2. Voice consistency across Stakes sections

The Stakes sections share a common shape (typically a "Three things to notice" or "Two things to notice" enumeration, ending with a cross-ref to `@sec-artifacts-politics` and a concrete reader prompt). That structure is intentional — it makes the values argument scannable and easy to apply — but it does carry a risk that reading several Stakes sections back-to-back feels formulaic.

**Recommendation:** read three or four Stakes sections in a row from different parts to check for boilerplate fatigue. If the structure is too repetitive, break the template in 2–3 chapters with a more narrative first paragraph. Tier-1 chapters (Part IV, much of Part VI, and Part VII) are the highest-leverage places to vary the voice; tier-3 chapters (`regex`, `latex`, `tracebacks`, etc.) deliberately stick to the template because the angle is harder to make load-bearing without it.

### 3. Tier-3 chapter Stakes sections — the weakest fits

The plan accepted that some chapters' politics angles would be harder to make load-bearing, and reserved the right to drop the section if it felt forced. After writing the review, the chapters whose Stakes sections most depend on a specific framing choice are:

- [parts/part-1-practice/common-formats.qmd](parts/part-1-practice/common-formats.qmd) — Markdown/CommonMark spec governance and Unicode-vs-ASCII assumptions. Holds together but is the lightest in the book.
- [parts/part-1-practice/tracebacks.qmd](parts/part-1-practice/tracebacks.qmd) — English error messages + tracebacks leaking machine context. Holds together but is brief.
- [parts/part-1-practice/debugging.qmd](parts/part-1-practice/debugging.qmd) — "works on my machine" and whose bug reports get closed. Anchors well on a single concrete question.
- [parts/part-3-python/regex.qmd](parts/part-3-python/regex.qmd) — Unicode-vs-ASCII default character classes. The strongest of the tier-3 angles; concrete and falsifiable.
- [parts/part-5-communication/latex.qmd](parts/part-5-communication/latex.qmd) — disciplinary marker + screen-reader accessibility. Holds together; the accessibility angle is sharp.

**Recommendation:** none require revision based on the review. Worth re-reading once to confirm the voice fits the chapter before considering this closed.

### 4. The cornerstone's "See also" list

[parts/part-1-practice/artifacts-have-politics.qmd](parts/part-1-practice/artifacts-have-politics.qmd:8) lists `@sec-ai-llm, @sec-evaluating-ai, @sec-documentation, @sec-secrets` in its See also. After the review, every content chapter cross-references the cornerstone, so the See also list is conservative relative to the actual graph.

**Recommendation:** leave as-is. The See also list is meant to surface the chapters whose connection is *thematic*, not the full inbound cross-ref set. The reciprocal mesh now exists through the Stakes sections without needing to reflect it back here.

### 5. CLAUDE.md updates

This PR (#22) updates `CLAUDE.md` to document the new canonical sections (`## Stakes and politics`, `## Further reading` callout) and the cornerstone's documented exception. The Style Guide section now has two new subsections explaining the templates and the tier-3 allowance.

The `Gap Chapter Backlog` section in `CLAUDE.md` was *not* updated by this review — none of the backlog candidates listed there were addressed in scope.

---

## Cross-cutting connectivity findings

After the review, every content chapter has at least one outbound cross-reference to `@sec-artifacts-politics` via its Stakes section. Spot-checks of the rendered HTML confirm that:

- All `@sec-*` cross-refs resolve cleanly (`quarto render --to html` is warning-free).
- The cornerstone has 30+ inbound edges, up from 0 before this review.
- Each AI chapter now reciprocally cross-refs the other three (the audit flagged `llm-internals` and `evaluating-ai` as isolated).
- `file-system.qmd` now connects forward to `@sec-scripts-vs-notebooks` and `@sec-git-github` (the audit flagged its outbound count at 5).

**Recommendation:** the connectivity work is done. No further sweep needed unless a future content change adds a chapter or removes a section ID, in which case the label table in `CLAUDE.md` should be updated and a single render pass will catch any broken references.

---

## `references.bib` consolidation

The review added **zero** entries to [`references.bib`](references.bib). All new external resources were added to the per-chapter Further reading callouts as plain links with one-sentence annotations rather than as `[@key]` citations. This preserves the existing pattern (only `documentation.qmd`, `automation.qmd`, and `artifacts-have-politics.qmd` use `[@…]` citations) and keeps the reference-handbook feel.

The Further reading callouts include several works that *could* be promoted to `references.bib` if the author wants to cite them inline somewhere. The most useful candidates would be:

- Bender, Gebru, McMillan-Major, Shmitchell, *On the Dangers of Stochastic Parrots* (FAccT 2021) — currently in Further reading for `ai-llm.qmd` and `llm-internals.qmd`; the strongest single citation for the AI Stakes sections.
- Mitchell et al., *Model Cards for Model Reporting* (FAT* 2019) — currently in `evaluating-ai.qmd` Further reading.
- Raji and Buolamwini, *Actionable Auditing* (AIES 2019) — currently in `evaluating-ai.qmd` Further reading.
- Edmondson, *The Fearless Organization* — currently in `collaboration.qmd` Further reading.
- Barocas, Hardt, Narayanan, *Fairness and Machine Learning* — currently in `evaluating-ai.qmd` Further reading.

**Recommendation:** leave `references.bib` alone unless inline citations to these works become useful. The Further reading callouts are already discoverable.

---

## Glossary additions in this PR

This PR adds five new entries to [`appendix-glossary.qmd`](parts/appendix/appendix-glossary.qmd) for vocabulary the new Stakes sections introduce:

- **Algorithmic audit** (`#term-audit`) — first/second/third party distinction, used in `evaluating-ai.qmd`.
- **Matilda effect** (`#term-matilda-effect`) — used in `writing-manuscripts.qmd`.
- **Open access (OA)** (`#term-open-access`) — gold/green distinction, used in `reading-scholarship.qmd`.
- **RLHF** (`#term-rlhf`) — used in `ai-llm.qmd` and the AI chapters' Further reading.
- **Schema** (`#term-schema`) — used in `sql-basics.qmd`'s Stakes framing of "schemas as frozen ontologies."

These can be linked from chapter bodies on first use with `[term](../appendix/appendix-glossary.qmd#term-<slug>)`. The current Stakes sections do not link to the glossary inline — they use the term and assume the reader will follow up if needed. Worth a one-pass review to add 1–2 inline glossary links where a term is first introduced.

---

## Backlog still open

These items are flagged in `CLAUDE.md`'s Gap Chapter Backlog and were **not** in scope for this review. They remain open as candidates for future work.

Carried over from earlier rounds:

- Data dictionary / schema docs — likely a section in `project-management.qmd`.
- Profiling / performance (`%%timeit`, `cProfile`) — a section in `jupyter.qmd` or a new short Part III chapter.

Newly identified candidates (from the original gap analysis, still open):

- Reproducible randomness — a short section in `pandas-basics.qmd` or `tabular-data.qmd`.
- Cloud notebooks (Colab, Kaggle, Codespaces) — a section in `jupyter.qmd` or `remote.qmd`.
- Out-of-memory data (chunked CSV, line-delimited JSON, Polars/DuckDB) — extension of `data-file-formats.qmd`.
- Diagram literacy (Mermaid, ER, sequence) — section in `documentation.qmd` or a new short chapter.
- Interactive debuggers (`pdb`, IDE breakpoints) — extension of `debugging.qmd`.
- Editor automation (snippets, format-on-save, multi-cursor) — extension of `text-editors.qmd`.
- Second-week Git (rebase, cherry-pick, reflog) — extension of `version-control.qmd`.
- Data ethics and licensing — possible new chapter or section in `artifacts-have-politics.qmd`.

The cornerstone chapter `artifacts-have-politics.qmd` is now load-bearing for every Stakes section in the book. If any of the backlog items above expand the cornerstone (e.g. a "data ethics and licensing" section), the inbound mesh of cross-references will continue to work; if any of them *replace* the cornerstone or significantly restructure it, every other chapter's Stakes section would need an audit.

---

## Verification

This PR was verified with:

```bash
quarto render --to html
```

— zero `Unable to resolve crossref` warnings, no new warnings overall.

```bash
grep -l "## Stakes and politics" parts/*/*.qmd | wc -l
```

— 37 of 38 content chapters (the cornerstone is the documented exception).

```bash
grep -l "sec-artifacts-politics" parts/*/*.qmd | wc -l
```

— 38 of 38 content chapters (the cornerstone matches its own anchor; every other chapter cross-refs it).

```bash
grep -l "Further reading" parts/*/*.qmd | wc -l
```

— 38 of 38 content chapters.
