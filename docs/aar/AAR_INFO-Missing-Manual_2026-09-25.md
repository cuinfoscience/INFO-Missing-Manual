# After-action report: the voice rewrite, September 2026

**Scope:** the rewrite of every chapter, appendix, the introduction, and the conclusion into the book's welcoming narrative voice, from the `tabular-data` pilot (#61) through Part VII (#68), all on 2026-09-25. How each part was done is in [`plans/2026-09-25-voice-rollout.md`](../plans/2026-09-25-voice-rollout.md); this report compares what the rules said with what happened.

## What the written rules said

The maintainer asked for chapters that read "informal, approachable, and welcoming to newcomers," name "common sources of confusion and frustration," link generously to official tutorials and Wikipedia, and have "a narrative-persuasive flow … instead of an enumeration of a sequence of facts," without losing authority; full rewrites were in scope, and "Learning objectives" became "Why read this chapter" bullets ([`decisions.md`](../decisions.md), 2026-09-25). `AGENTS.md` ("Tone and Voice") turned that into rules, with `tabular-data` as the model. The plan set the process: one pull request per part, one agent per chapter working from a shared brief, then mechanical checks, a read of each chapter's opening and Stakes section, a render, and the layout audits before any commit.

## What happened

All eight pull requests merged the same day, each rendering with zero warnings and passing CI. Every content chapter now opens with 5–8 "Why read this chapter" bullets, teaches in prose, and has 35–56 checked links (it had 7–24). No chapter lost an ID, a cross-reference, a figure, or a citation.

The larger result was accuracy. Running every example and checking every fact found well over a hundred errors in text that had passed earlier reviews, including:

- **Advice that was wrong or dangerous:** `rm "$DIR"/*` described as safe when the variable is empty; `with sqlite3.connect()` said to close the connection; `load_dotenv()` said to read `.env` from the current directory; import advice for `src/` that fails from every folder; a notebook's kernel said to start in the launch folder.
- **Examples that didn't do what the text said:** "error" examples that raised nothing under pandas 3, a `-999` example that silently averaged, a worked example contradicting itself, an `if` block that always printed `exit 0`.
- **Invented references:** a Further reading item whose DOI returned 404 and whose authors didn't exist, and a LaTeX template crediting the maintainer with a paper that doesn't exist.
- **Figures that disagreed with their captions or text:** three terminal illustrations, each regenerated.
- **Silent rendering bugs:** README examples whose inner code fences ended the outer block early.
- **Layout:** five pages that scrolled sideways on a phone; since Part V, none does.

## Where practice differed from the rules, and why

1. **Length.** The brief first said "don't grow"; long chapters (7,000+ words) complied, but every short chapter grew 30–65%, past the "about a third" the brief allowed from Part III on. The growth was almost entirely real output for the confusions the maintainer asked the book to name. The rule was wrong for short chapters, not the agents; each pull request reported the overshoot and the easiest cuts.
2. **Cross-chapter facts.** Chapters are rewritten in parallel, but they repeat each other's facts (where a kernel starts, pandas 3's behaviors, temperature 0). The brief said nothing about it at first. Passing a verified fact to a running agent with `SendMessage`, and grepping the rest of the book before committing, caught every conflict found; `docs/plans/…` now says to do both.
3. **Stakes openings.** The rule forbade two stock openings but not repetition across parts; three chapters first opened on a form that rejects your name, and two adjacent ones on the same study. Reading all Stakes openings side by side before each commit fixed it.
4. **Unverifiable environments.** The session's proxy blocked some sites (curl exit 56/35, GitHub pages), and agents at first replaced reachable-elsewhere links as dead. The brief now says a proxy refusal isn't evidence a link is dead.
5. **Interruptions.** Three of four Part IV agents hit a rate limit mid-edit, and one container was replaced between turns, emptying the scratch directory. Resuming each agent from where its file stood, rebuilding the tools, and not committing until every agent reported kept the work intact; the handoff now says to expect both.
6. **Claims only the maintainer can make.** The AI-disclosure appendix said every paragraph was read by a human author and every code example checked by one. After an agent rewrite those claims could no longer be verified from the records, so they were scoped to what the records show and flagged for the maintainer to confirm or reword.
7. **Model identifiers.** One agent put specific model IDs in API examples; they now use a `MODEL-NAME` placeholder with a pointer to the provider's models page, which is also more durable.

## What changes as a result

Already in place, in the same pull requests:

- `AGENTS.md`: "Every code block runs, and every fact holds"; nested code fences need a four-backtick outer fence; every reference must be real and example entries obviously fake. `CONTRIBUTING.md` carries the short versions.
- The plan records the brief, the review steps, and each part's lessons, so a future rewrite of any chapter starts from them.
- `tools/layout-audit/audit.py widths --widths 390` is part of each part's checks.

Recommended, not yet done:

- **Update the book's own CI** to the GitHub Actions versions `automation` now teaches (roadmap).
- **Keep the brief's growth rule honest:** for chapters under about 4,500 words, expect 30–60% growth when every confusion gets real output, and say so up front rather than as an overshoot.
- **Re-run the examples on a schedule.** Several fixes were caused by tools changing (pandas 3, git 2.43, ruff 0.16, the Anthropic SDK dropping `temperature=`). A yearly pass, like the one the handoff already asks for the CU Boulder callouts, would catch the next round.
