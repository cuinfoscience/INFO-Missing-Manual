# Plan: revising the whole book after the September 2026 peer review

**Status:** Phase 1 done (#70); the rest proposed, waiting on the maintainer's decisions in "Decide first." Written 2026-09-25 from the ten simulated reviews in [`aar/2026-09-25-peer-review.md`](../aar/2026-09-25-peer-review.md) (R1–R10 below), after the voice rewrite (#61–#68). Progress goes in [`handoff.md`](../handoff.md) and the checklist in [`roadmap.md`](../roadmap.md).

## What the reviews say, in one paragraph

The voice rewrite worked; no reviewer asked to undo it, and several asked to keep specific sections as they are. What the reviewers want is mostly *around* the chapters rather than inside them. They want the book ordered and connected so an instructor can assign it (prerequisites that follow the sidebar, reading paths, one running project, less repetition). They want the practice to be checkable (exercises with answers, predict-then-run items). And they want the book to reach the parts of its audience it currently serves thinly: students who have never installed Python, Windows and Chromebook users, humanities students, social scientists who think in measurement and R, students who will share or archive data, and graduates headed to a job rather than to graduate school. Nothing in the reviews says the book is wrong at its core. They say it's a strong set of chapters that isn't yet a strong course.

## Decide first (the maintainer)

These change what every later phase does, so they come before any writing.

1. **Reorder chapters?** Several reviewers found prerequisites that point forward in the sidebar (R1, R2, R3, R8, R9). The proposal in Phase 2 moves six chapters within or between parts. Chapter URLs don't change (the files stay in `chapters/`), but chapter *numbers* do, and any syllabus that cites "Chapter 12" would drift. Approve, adjust, or keep the current order and fix prerequisites only.
2. **One default setup path.** R1 and R3 both say the book never installs Python and never commits to one path. Pick the default the book teaches first: python.org plus `venv` (simplest to explain), `uv` (fastest, one tool, still young), or Miniforge/conda (what many courses hand out). The others become labeled detours.
3. **New chapters or appendices.** The reviews argue for up to four: a "Day zero" setup appendix (R1, R3); a chapter on charts and figures, since nothing takes a cleaned table to a defensible chart (R7); a chapter on sharing, archiving, licensing, and data ethics (R4, R5, R6, R7, R9), which would also settle the roadmap's open "Data ethics and licensing" item; and a "Writing at work" chapter (status updates, decision memos, incident write-ups) (R10). Approve any subset.
4. **A running project and a practice repository.** Four project names are in use today (`coffee-sales`, the survey project, `sales-project`, `~/Courses/INFO-3010/Project`), and exercises that say "a bug you ran into this week" leave a new student with nothing to use (R1, R2, R3, R9). Approve one book-wide project (the plan proposes `sales-project`, since `scripting` and `jupyter` already share it) and a separate public repository of practice files, including deliberately broken ones, that exercises can point to.
5. **Where answers go.** R2 asks for answers to exercises. In-book (collapsed callouts after each exercise block) is easiest for self-learners; a separate instructor guide keeps answers out of students' way. Pick one.
6. **A humanities thread.** R6 proposes carrying one small humanities collection (digitized letters) through `common-formats`, `regex`, and `data-file-formats`, alongside the social-science examples. Approve or decline.
7. **The AI-disclosure appendix.** R5 found a contradiction: "What the AI was *not* asked to do" says claims about authors and papers stayed out of AI hands, while the new September 2026 paragraph reports invented references found and fixed. #68 also scoped two review claims to what the records show. Only the maintainer can say what happened, so this wording is theirs.
8. **A length budget.** Chapters grew 20–60% in the voice rewrite, and several additions below would grow them again. Set a ceiling (for example, 7,000 prose words), and split chapters that pass it (R1 suggests splitting `debugging`; R3 suggests moving profiling out of `jupyter`).

## Phase 1: corrections and small fixes (one pull request)

Specific, low-risk fixes the reviewers found, each small enough to do and check in one pass. They don't depend on the decisions above.

- `ai-agents`, "Turning a notebook workflow into an agent": an agent that picks the analysis and retries until something works is automated p-hacking; say analyses are pre-specified and agents do fixed transformations (R8).
- `llm-internals`, Exercise 5: warn that a model's self-reported `confidence` isn't calibrated (R8).
- `evaluating-ai`: separate a *random* sample for estimating accuracy from a hard-case suite for regression checks, add a held-out split so rubric tuning isn't done on the test items, use a paired comparison (paired bootstrap or McNemar) when comparing prompts, mention the Wilson interval and Krippendorff's alpha, and say plainly that kappa measures reliability, not validity (R7, R8). Add `pandas-basics` and `tabular-data` as prerequisites (R7, R8).
- `remote`: the Slurm example activates a venv without saying it must be built on the cluster from the loaded module's Python; add that step (R3).
- `scripting` and other Part III chapters: use `python -m pip` consistently, and pick one Python version for examples (3.11 and 3.12 are mixed) (R3).
- `terminal`: show PowerShell's "is not recognized as the name of a cmdlet" beside `command not found`; teach Ctrl+C; add a "which prompt am I at?" box (shell `$`/`%` vs. Python's `>>>`), and name the `pip install` at `>>>` case in `tracebacks`' `SyntaxError` entry (R1).
- `debugging`: add `SyntaxError` and `IndentationError` to the error-families table, and put a pure-Python bug before the pandas ones (R1).
- `text-editors`: add the VS Code interpreter trap (the Run button may use a different Python than your terminal), linking to "VS Code and venvs" (R1).
- `secrets`: add two-factor authentication, cloud CLI credentials (`~/.aws/credentials`), and "tell your security contact first" at the top of "What if I already leaked a secret?" (R10); add a parallel section on leaked *personal* data and who to tell (R4).
- `automation`: say that GitHub Actions minutes are limited for private repositories (R10).
- `http-apis`: save raw responses to `data/raw/` with a timestamp before parsing (R7); add a paragraph on human-subjects data and when to ask about IRB review (R7).
- `data-file-formats`: "When not to use Parquet" adds sharing and preservation (UTF-8 CSV plus a data dictionary); add Stata/SPSS files (`pd.read_stata` keeps value labels) (R4).
- `reading-scholarship`: add "how did they measure it?" to "Is this paper any good?" (R8); add a page-number locator to the reading-note template and a rule to keep quotation marks on copied text (R5).
- `writing-manuscripts`: point "a replication-ready code and data release" to `version-control`'s Zenodo DOIs, and add a data-availability statement to the submission checklist (R5).
- `collaboration`: its "Why read" bullet promises what open-source maintainers expect, and no section delivers it; write a short one or cut the bullet (R9).
- `common-formats`: `json.dumps` and PyYAML escape non-ASCII text unless you pass `ensure_ascii=False` / `allow_unicode=True`; put it beside the Norway problem (R6).
- `latex`: add the real `Unicode character … not set up for use with LaTeX` error and the fix (XeLaTeX or LuaLaTeX with `fontspec`), and put `\DocumentMetadata` in the Templates (R6).
- `operating-system`: give the backup section a free route before the external drive (R1); present every "At CU Boulder" callout as a template other schools replace (R1).
- Glossary: add the stewardship terms the chapters use (provenance, metadata, license, DOI, checksum, personal data, de-identification), plus Git, API, environment variable, and a "repository" entry separating a Git repository, a data repository, and an institutional repository; link the twelve entries no chapter links to, or cut them (R4).
- Introduction: the computational-thinking section's four skills never recur; tie them to the running themes or cut the section (R2).

## Phase 2: order, prerequisites, and repetition (one pull request, after decision 1)

**Proposed order changes** (sidebar only; files and URLs stay put):

- `tracebacks` before `debugging` in Part I, and `debugging`'s prerequisite on `terminal` reworded as "see also" (R1, R2).
- `virtual-environments` before `package-management` in Part III, ending the prerequisite loop between them (R3).
- `remote` from Part II to the end of Part III, after environments exist (R3).
- `pandas-basics` before `tabular-data` in Part IV (R2).
- `regex` from Part III into Part IV, after `pandas-basics` (R2).
- `version-control` first in Part VI, since `project-management` uses `git init` and issue numbers (R9).

**Every prerequisite callout** then gets checked against the new order: a prerequisite must come earlier in the sidebar, or be labeled "see also."

**One home for each repeated explanation** (R1, R2, R3, R9), with the other chapters linking to it:

| Explanation | Keep it in | Replace elsewhere with a link from |
|---|---|---|
| "File not found" is really "wrong folder" | `file-system` | `terminal`, `debugging` |
| Diátaxis, the four kinds of docs | `reading-docs` | `documentation` (which becomes a writing chapter) |
| Creating and activating a venv; `python -m pip`; registering a kernel | `virtual-environments` | `package-management`, `jupyter` |
| Pimentel et al. and `nbconvert --to script` | `scripting` | `jupyter` |
| Notebook or script? | `scripting` | `jupyter` |
| Profiling (`cProfile`, `line_profiler`) | `scripting` (or `debugging`) | `jupyter` |
| What a good issue contains | `collaboration` | `project-management` |
| Review-comment labels (Blocker, Suggestion, Question, Nit) | `collaboration` | `version-control` |

**"Which Python is running?"** (`sys.executable`, in nine chapters) is the book's threshold concept (R2): name it once in the introduction, and have later chapters ask the reader to recall it rather than re-explain it.

**Reading paths** in the introduction's Outline (R1, R2, R9): a first programming course, the first two weeks of a data course, a new research-lab assistant, and a first job on a data team. Each is five to eight chapters in order.

## Phase 3: setup and a shared project (after decisions 2 and 4)

- **Day zero appendix** (R1, R3): install Python by the default path on Windows, macOS, Linux, and a Chromebook (Linux environment or Codespaces), with a check that it worked, the python.org "Add python.exe to PATH" box, and the labeled detours. Every chapter that needs Python links to it.
- **One running project** (R2, R3, R9): rename examples to one project across Parts II–VI, with a lab-shaped variant in Part VI (several people over several years, not only a semester group project) (R9). Vary the three "night before the group project is due" openings in Part VI (R9).
- **Practice repository**: a public companion repository with the project's files, a few deliberately broken ones, and the data every exercise needs, so no exercise depends on the reader's own history.

## Phase 4: filling the gaps, one theme per pull request

Each theme is its own pull request, in this order (the first two unblock the most readers).

1. **Windows and Chromebooks as first-class** (R1): every terminal example shows the PowerShell form or says why not; errors are shown as Windows users see them; the Chromebook route from Phase 3 is linked where it matters.
2. **The research data lifecycle** (R4, R5, R7, R9, R10), in `project-management` (a closing "Share, archive, and let go" section: licenses for data and code, `CITATION.cff`, a dataset README, repositories and DOIs, FAIR as one paragraph, what to keep and what to destroy), `tabular-data` (a row-count log the pipeline writes), and `writing-thesis` (a data management plan, and realistic time for IRB and data use agreements). If decision 3 approves a data-ethics chapter, most of this goes there instead.
3. **Measurement and uncertainty** (R7, R8): name validity and reliability; MCAR/MAR/MNAR in `tabular-data`'s Stakes section; a short section on levels of measurement and survey weights; LLM labels treated as measurement with error, with a worked misclassification correction in `evaluating-ai`.
4. **Social-science practice in `pandas-basics`** (R7): a survey example (`value_counts(normalize=True, dropna=False)`, `crosstab`, an ordered categorical for a Likert scale, `np.average(..., weights=...)`); an "If you learned R first" callout (index, `assign`, `groupby().agg()`, and `NaN` skipped silently where R returns `NA`); a `dplyr` column in `sql-basics`' translation table.
5. **Information literacy** (R5): a section on searching (databases by field, keywords vs. subject terms, one Boolean example, a search log) and on books in `reading-scholarship`; quoting, paraphrasing, plagiarism, and citation styles in `writing-manuscripts`; word-processor citation plugins beside Better BibTeX; librarians as research consultants, not only as warnings about predatory venues; cross-links between the four places the book evaluates sources, with one shared prompt ("who says so, and how do they know?").
6. **AI for research and writing** (R5): a research-and-writing path through `ai-llm` (AI search and summary tools and their failures, citing AI output in APA/MLA/Chicago, AI detectors and their false positives for second-language writers, keeping drafts as evidence), and thesis AI policies in `writing-thesis`.
7. **Humanities and multilingual text** (R6, after decision 6): an XML section in `common-formats` (elements vs. attributes, well-formed vs. valid, `xmllint`); format longevity; `biblatex-chicago` and an archival citation in `latex`; in `presenting`, reading a paper aloud as a real genre, image permissions and credits, and depositing slides.
8. **The cornerstone chapter** (R6): accessibility and disability law (ADA, Section 508); copyright beyond the DMCA (fair use, text-and-data mining, Creative Commons, licensing your own work); memory and loss; classification (Bowker and Star); the CARE principles; "Access" and "Durability" in its checklist; and links to every chapter whose Stakes section points back to it.
9. **Workplace readiness** (R9, R10): a worked example of joining an existing repository (invite, two-factor, following someone else's README, a branch-protection rejection, a first small PR); a departure checklist spanning `collaboration`, `automation`, `secrets`, and `remote` (move repositories to the organization, replace personal tokens, transfer scheduled jobs, hand over or delete cloud resources); cloud work on an organization's account (ask first, tag resources with an owner and end date); planning with estimates and outside blockers in `project-management`; and, if decision 3 approves it, the "Writing at work" chapter.

## Phase 5: new chapters (after decision 3)

Each new chapter follows the canonical structure and the voice rules, gets a meme, is registered in `_quarto.yml` and the label table, and has its code run and links checked, as in the voice rollout.

- **Charts and figures** (Part IV, after `http-apis` or `tabular-data`): from a cleaned table to a chart that supports a stated finding, with honest axes, uncertainty, accessible color, and alt text (R7, and R6 on accessibility).
- **Sharing, archiving, licensing, and data ethics** (Part IV or VI), if approved.
- **Writing at work** (Part V): status updates for non-technical readers, decision memos, incident write-ups, and saying "this will be late" early (R10).
- **Day zero** (appendix), from Phase 3.

## Phase 6: practice you can check (part by part)

R2's assessment critique, done as one pull request per part, like the voice rollout:

- two or three predict-then-run exercises per chapter, starting with `regex` (what does `.str.extract(r"Order #(\d+)")` return for row 3?), with answers where decision 5 puts them;
- a partly worked example between each fully worked example and its open exercise (for instance, a question draft in `questions` with two fields left blank);
- every one-page checklist in the "I can…" form;
- every "your own bug" or "your own project" exercise given a fallback in the practice repository.

## How each pull request is checked

The voice rollout's checks still apply: render with zero warnings, `audit.py widths` (390–1920 px) and `audit.py toc`, the issue-form and margin-header checks, every link checked, every code block run, every fact sourced, and the Stakes openings read side by side. Add one: each pull request lists the review items (R1–R10) it addresses, so this plan's items can be ticked off with a pull request number.

## Traceability

| Theme | Reviews | Phase |
|---|---|---|
| Order and prerequisites | R1, R2, R3, R8, R9 | 2 |
| Repetition | R1, R2, R3, R9 | 2 |
| Reading paths | R1, R2, R9 | 2 |
| Installing Python; one setup path | R1, R3 | 3, 5 |
| One running project; practice files | R1, R2, R3, R7, R9 | 3 |
| Windows and Chromebooks | R1 | 1, 4 |
| Data lifecycle, sharing, ethics | R4, R5, R7, R9, R10 | 1, 4, 5 |
| Measurement and uncertainty | R7, R8 | 1, 4 |
| Social-science and R users | R7 | 4 |
| Information literacy; plagiarism | R5 | 1, 4 |
| AI for research and writing; disclosure | R5 | 4; decision 7 |
| Humanities and multilingual text | R6 | 1, 4 |
| Cornerstone chapter | R6 | 4 |
| Workplace readiness | R9, R10 | 1, 4, 5 |
| Charts and figures | R7 | 5 |
| Assessment and exercises | R2 | 6 |
