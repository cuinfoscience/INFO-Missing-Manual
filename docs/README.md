# Project records

The records behind the book: what was decided, what was planned, what was reviewed, and where work stands. None of it is book content, and Quarto does not render it (`_quarto.yml` lists only the chapters).

Read [`handoff.md`](handoff.md) and [`decisions.md`](decisions.md) before starting work. `AGENTS.md` at the repository root says the same for agents, and says when to read the rest.

| Path | What it holds | How it is kept |
|---|---|---|
| [`handoff.md`](handoff.md) | Where work stands: what is done, paused, waiting on a decision, or known to be broken | Rewritten, not appended, when a session stops or the state changes. It describes the present; history lives in git and in the other records. |
| [`decisions.md`](decisions.md) | Standing decisions, with the reason for each and where it is enforced | Newest first. A decision is never deleted. When one is replaced, mark it *superseded* and link the entry that replaces it. Proposals nobody has decided yet go in `handoff.md`, not here. |
| [`roadmap.md`](roadmap.md) | The chapter backlog and the follow-ups from reviews that are still open | Items are ticked off, with the PR that closed them, when they land. New candidates are added with a line on where they would go. |
| `aar/` | After-action reports and reviews: what the written rules said should happen, what happened, why the two differed, and the revisions that follow | One file per review. New reports are named `AAR_INFO-Missing-Manual_<YYYY-MM-DD>.md`. A report is not rewritten after the fact; when one of its actions is resolved, add a dated note. |
| `plans/` | Plans for larger pieces of work, often recommended by an AAR | Named `YYYY-MM-DD-<topic>.md`. A plan records a proposal and the decisions behind it. Once work starts, progress goes in `handoff.md`, not in the plan. |

## Current contents

| File | What it is |
|---|---|
| [`aar/2026-04-27-comprehensive-review.md`](aar/2026-04-27-comprehensive-review.md) | The audit report from the comprehensive review (PRs #15–#22): what the review delivered and the judgment calls it deferred to the author. It was `REVIEW.md` at the repository root until September 2026. |
| [`plans/2026-09-24-screenshots.md`](plans/2026-09-24-screenshots.md) | Real screenshots for the twelve placeholders and beyond, with `tools/shots`: routes, milestones, the pilot, and the decisions it needs. Proposed. |
| [`plans/2026-09-24-toc-below-meme.md`](plans/2026-09-24-toc-below-meme.md) | Issue #30: keep the table of contents open by putting the chapter meme above it in the right sidebar. Proposed; the approach is tested. |
| [`plans/2026-09-24-cloud-storage-sections.md`](plans/2026-09-24-cloud-storage-sections.md) | Issue #34: new sections on how much space tools take (chapter 9) and on cloud sync, access, and sharing (chapter 10). Implemented. |

## Records kept elsewhere

The companion book [*Web Data Science*](https://github.com/cuinfoscience/Web-Data-Science-Book) keeps its own `docs/`. Its screenshot AARs and plans are the source of this book's screenshot toolkit, and `AGENTS.md` says when to read them.
