# Plan: the table of contents, consistently below the chapter meme (#30)

**Status:** implemented 2026-09-24 (option A, sticky, memes up to 15rem tall), in the pull request that closed [#30](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/30). Two findings changed the implementation: a Lua filter cannot set `margin-header` (Quarto reads it before filters run), so a generator writes it into the front matter; and a footnote in `presenting`'s Purpose collapsed the table of contents the same way the meme did, so it became an inline link.

## 1. The problem

The report: on some chapters the table of contents "shows hidden, and only appears once you scroll down", apparently where the meme sits higher up, as when moving from chapter 1 to chapter 2. The reporter asks for images to be kept to one consistent area.

**Why it happens.** Every chapter's meme is placed with `.column-margin` beside its Purpose section, near the top of the page. Quarto's page script collapses the right-hand table of contents into an "On this page" toggle (`#quarto-toc-toggle`) whenever margin content would overlap it. At page load the meme is in view, so the table of contents collapses; after scrolling past the meme, it opens again.

**Measured** with `tools/layout-audit/audit.py toc` on a local render: the table of contents is collapsed at load on **37 of 41 pages** at 1280×800, 1440×900, and 1920×1080. The four pages where it shows (the Introduction, the Conclusion, and both appendices) are the four without a meme.

**A second cost.** Quarto's **Edit this page** and **Report an issue** links sit inside the table of contents, so on those 37 pages they are hidden too. `CONTRIBUTING.md` currently has to tell readers to open "On this page" to find them.

## 2. Options

| Option | What it does | For | Against |
|---|---|---|---|
| **A. Meme in the right sidebar, above the table of contents** (recommended) | On wide screens, the meme becomes the sidebar's header and the table of contents sits directly under it. On narrow screens, where Quarto hides the sidebar, the meme stays in the page as now. | Exactly what the issue asks: one consistent place, the table of contents always open. The margin stays free for notes and figures. | The sidebar is sticky, so the meme stays on screen while reading (see §4); the table of contents starts about 300 px lower. |
| B. Meme in the body column | The meme becomes a small figure at the top of Purpose. | Simple, no margin overlap at all. | Changes the book's look, and pushes the first paragraph down on every chapter. |
| C. Override Quarto's collapse | Keep the margin meme and stop the table of contents from collapsing. | Least visible change. | Meme and table of contents would overlap; fights Quarto's own layout code. |
| D. Move the meme lower | Place the meme later in the chapter. | Trivial. | Moves the collapse to wherever the meme is; doesn't fix it. |

## 3. How option A works (tested)

Quarto supports a **`margin-header`**: Markdown placed in the right sidebar *above* the table of contents. A scratch book rendered with Quarto 1.9.15 showed that a per-chapter `margin-header` in a chapter's front matter works: the image rendered inside `#quarto-margin-sidebar`, directly before `<nav id="TOC">`, on that chapter only. At 1280×800 the meme sat at the top right (250×250 px), the table of contents was visible at load, and nothing collapsed. At 390 px wide the sidebar is hidden, so the header image wasn't shown; hence the second copy below.

An earlier prototype moved the meme into the sidebar with JavaScript after load. It fixed the desktop view but lost the meme on phones, and it depends on Quarto's page structure; `margin-header` needs no JavaScript.

Implementation:

1. **Generate the header from the existing `meme:` front matter**, so a chapter still declares its meme once. First try a Lua filter (in `tools/chapter-meme/`) that sets the document's `margin-header` from `meme:`; Quarto may read `margin-header` before filters run, in which case fall back to a small generator that writes the `margin-header` field into each chapter's front matter from its `meme:` block, with a `--check` mode like the issue-form sync. The image goes in without a caption, with its alt text, as today.
2. **Keep the inline meme for narrow screens.** The shortcode's current `.column-margin` output stays, with a class hidden at 992 px and wider (Quarto's breakpoint for showing the sidebar), so each width shows exactly one copy. Confirm that a hidden margin element no longer triggers the collapse; the audit checks this.
3. **Check the image path.** Chapters live in `chapters/`, so confirm the header's `/graphics/memes/<slug>.png` is rewritten per page like body images (the scratch test used a same-folder path).
4. **Style:** a width that fits the sidebar (about 250 px at 1280) and a little space above the table of contents, in a small stylesheet listed under `format: html: css:`.
5. **Update the records:** `tools/chapter-meme/README.md`, "Chapter memes" in `AGENTS.md`, and the note in `CONTRIBUTING.md` about opening "On this page", which becomes unnecessary.

## 4. Decisions needed from the maintainer

1. **Option A?** (Recommended.)
2. **Sticky or scrolling meme.** The sidebar sticks as you scroll, so the meme stays visible beside the text, above the table of contents. On an 800-px-tall screen, a long table of contents then runs below the fold sooner. Keep it sticky (simplest), or let the meme scroll away and the table of contents move up (a little CSS)?
3. **Size.** The sidebar is about 250–300 px wide. Keep memes at full sidebar width, or smaller?

## 5. Acceptance test

- `tools/layout-audit/audit.py toc` exits 0: the table of contents is visible at load on 41 of 41 pages at 1280×800, 1440×900, and 1920×1080, and the meme is displayed at every size, including 390×844.
- *Edit this page* and *Report an issue* are visible at load without clicking anything.
- `quarto render --to html` finishes with zero warnings; all 37 memes render from the committed PNGs (no regeneration).
- A before-and-after look at a few chapters at desktop and phone widths, attached to the pull request.

## 6. Interactions

- Screenshots placed in Quarto's wider columns (the relaxed screenshot tier) also cover the table of contents while on screen, and trigger the same collapse there. See [`2026-09-24-screenshots.md`](2026-09-24-screenshots.md), §8 item 9.
- Chapters without a meme (the Introduction, the Conclusion, the appendices) are unaffected.
