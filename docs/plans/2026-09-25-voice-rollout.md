# Plan: the book's new voice, part by part

**Status:** in progress. The pilot (`tabular-data`, #61) and Part I (#62) are done; Parts II–VII, the appendices, the introduction, and the conclusion remain. Progress goes in [`handoff.md`](../handoff.md) and the checklist in [`roadmap.md`](../roadmap.md).

## What the maintainer asked for

In September 2026 the maintainer asked for every chapter to read "informal, approachable, and welcoming to newcomers," to "acknowledge common sources of confusion and frustration," to "make liberal use of hyperlinks out to other resources, particularly tutorials in official documentation as well as Wikipedia," and to have "a narrative-persuasive flow … instead of an enumeration of a sequence of facts," without giving up authority. Full rewrites are in scope. They also replaced each chapter's "Learning objectives" with 5–8 "Why read this chapter" bullets grounded in what frustrates novice and intermediate students ([`decisions.md`](../decisions.md), 2026-09-25). The rules are in `AGENTS.md`, "Tone and Voice" and "Canonical Chapter Structure"; `chapters/tabular-data.qmd` is the model.

## How each part is done

One pull request per part, one commit per chapter. Part I was rewritten by one agent per chapter, working in parallel from the brief below, then reviewed chapter by chapter before its commit. That worked; do it the same way.

**Review each chapter before committing it:**

1. Mechanical checks against `main`: front matter byte-identical; every `{#…}` ID, `%%| label`, `@sec-`/`@fig-`/`@tbl-` reference, and `[@citation]` key still present; no "Learning objectives"; 5–8 "Why read this chapter" bullets and no intro line; the canonical heading order with Further reading last; the Stakes closing sentence intact and its length in range; none of the stock phrases `AGENTS.md` lists; no URL linked twice.
2. Read Purpose, Why read this chapter, and Stakes and politics in full, and spot-check any factual claim the agent flagged as unverified. In Part I that caught a docstring typo attributed to the wrong function, a bullet promising something the chapter never discusses, and a Further reading link swapped out only because this session's proxy couldn't reach it (the proxy blocking a site is not evidence the link is dead; keep it).
3. Render the whole book (zero warnings), then run `audit.py widths` (desktop widths), `audit.py toc`, and `audit.py widths --widths 390` to catch a new table that is too wide for a phone. Part I's rewrite of `debugging` added one; merging two of its columns fixed it.

**What Part I taught:**

- **The rewrites find errors.** Running every example and checking every fact turned up about thirty mistakes in seven chapters: examples that didn't fail the way the text said (pandas 3 reads `'N/A'` as missing, so two "error" examples raised nothing), a mangled `sep="\t"`, outdated error messages, wrong claims about YAML and Markdown, historical claims stronger than their sources, and Further reading items pointing at the wrong page. Budget for it; it's the most valuable part of the pass.
- **Link counts land above the brief's 20–35 for long chapters** (40–50 in Part I, with 12–17 to Wikipedia; `artifacts-have-politics` has 41 to Wikipedia because it names many cases and laws). That's acceptable for chapters longer than the pilot; cut links that don't help a reader rather than to hit a number.
- **Chapters grow** (20–60% more words), mostly from naming confusions and adding real output. Keep an eye on the checklists and quick references, which should stay short.

## The brief given to each agent

The brief below is what each Part I agent received, with its chapter named in the task. Paths to the scratch Python environment are session-specific; point them at whatever environment has pandas 3 (and PyYAML for format chapters).

> Rewrite ONE chapter of the book in its new voice. Edit only that file; don't commit, push, or render.
>
> **Read first:** `AGENTS.md` ("Tone and Voice", "Canonical Chapter Structure", "Stakes and politics section", "Further reading callout", "Formatting Conventions", "Add a figure", and "Keep the first screen of a chapter free of margin content"); `chapters/tabular-data.qmd` in full, the model; your chapter in full.
>
> **Do:** rewrite teaching sections as narrative (lists stay for material a reader scans); name the confusion before resolving it; talk to "you", with contractions, and none of the stock formal phrases; persuade with reasons and concrete cases; replace "Learning objectives" with "Why read this chapter" (5–8 one-sentence bullets, no intro line); rewrite Purpose as a situation the reader recognizes; link tools to official tutorials and concepts to Wikipedia on first mention, checking every link returns 200 (and every `#fragment` exists), and re-checking the chapter's existing links; run every code block (pandas 3) and make shown output match real output; don't invent facts, and verify any you add; don't cut teaching content.
>
> **Don't change:** front matter; the H1 and every `{#…}` ID, cell label, and `@fig-`/`@tbl-` reference; the meme shortcode; the prerequisites callout's references; the canonical order; Stakes and politics' position, length, concrete opening, and closing sentence; glossary links, `@sec-` references, and citations; figures and their `fig-alt`; Further reading's position and format. No new margin content near the top. Blank lines around fenced code in list items.
>
> **Style:** plain punctuation (colons, commas, parentheses rather than chains of em dashes), American spelling, sentence-case headings, no emoji beyond 📚.
>
> **Report:** what changed by section; link counts before and after and confirmation each was checked; which code ran and what didn't work; factual claims corrected, softened, or unverifiable; anything the reviewer should look at.
