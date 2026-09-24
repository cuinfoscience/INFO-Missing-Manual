# chapter-meme

Puts a meme at the top of each chapter: on wide screens at the head of the right sidebar, directly above the table of contents, and on narrow screens at the top of the Purpose section. The chapter says what the meme is in its frontmatter; this folder turns that into a PNG and places it.

| File | Role |
|---|---|
| `chapter-meme.lua` | The Quarto shortcode `{{< chapter-meme >}}`. Reads the chapter's `meme:` frontmatter, decides whether the cached PNG is current, calls the generator if it isn't, and emits the image with its alt text: in HTML an inline copy for narrow screens, in other formats a `.column-margin` block. |
| `generate_chapter_meme.py` | Fetches one meme from the [memegen.link](https://memegen.link) API and writes it to disk. Standard library only. |
| `sync_margin_header.py` | Writes each chapter's `margin-header` (the sidebar copy) from its `meme:` block; `--check` exits 1 if any chapter is stale. Standard library only. |
| `chapter-meme.css` | Sizes both copies: the sidebar copy up to 15rem tall, the inline copy up to 20rem wide. Loaded by `_quarto.yml` (`format: html: css:`). |

## How it is wired

`_quarto.yml` loads the shortcode for every page:

```yaml
shortcodes:
  - tools/chapter-meme/chapter-meme.lua
```

A chapter declares its meme in frontmatter and calls the shortcode, conventionally just below `## Purpose {.unnumbered}`:

```yaml
meme:
  template: "fine"           # memegen template id
  lines:                     # one per text region in the template, in order
    - ""
    - "MY CODE IS ON FIRE BUT THIS IS FINE"
  alt: "Short caption for screen readers."   # required
  rationale: "humor — why this meme"         # optional, never rendered
  # width: 1000              # optional; output width in pixels
  # font: "impact"           # optional; memegen font id
```

```markdown
{{< chapter-meme >}}
```

The shortcode hashes `template + width + font + lines` and compares the hash with `graphics/memes/<slug>.spec`. If the PNG is missing or the hash differs, it runs the generator, writes `graphics/memes/<slug>.png`, and updates the `.spec`. Otherwise it renders offline from the committed PNG.

### Two copies, one for each screen width (issue #30)

Until September 2026 the shortcode put the meme in the margin, and Quarto collapses the table of contents whenever margin content overlaps it, so the table of contents was hidden at load on every chapter with a meme. Now:

- **Wide screens (992 px and up):** the meme is the chapter's `margin-header`, which Quarto places at the top of the right sidebar, above the table of contents. Quarto reads `margin-header` from the front matter *before* any filter runs (a Lua filter that set it did nothing), so `sync_margin_header.py` writes it there, under a "do not edit" comment:

  ```yaml
  # margin-header: generated from meme: by tools/chapter-meme/sync_margin_header.py; do not edit
  margin-header: |
    ![](/graphics/memes/questions.png){.chapter-meme fig-alt="…"}
  ```

  Run `python tools/chapter-meme/sync_margin_header.py` after adding, removing, or editing a `meme:` block. CI runs it with `--check`.
- **Narrow screens,** where Quarto hides the right sidebar: the shortcode emits an inline copy (`.chapter-meme-inline`), which Bootstrap's `d-lg-none` hides at 992 px and up. It is deliberately not margin content.
- **Other formats** (the PDF) keep the old `.column-margin` placement.

`tools/layout-audit/audit.py toc` checks the result on every page: the table of contents open at load at three desktop sizes, and exactly one meme showing at every size.

## Running the generator by hand

```bash
python tools/chapter-meme/generate_chapter_meme.py \
    --template fine \
    --line "" --line "MY CODE IS ON FIRE BUT THIS IS FINE" \
    --out graphics/memes/debugging.png
```

Options: `--width` (default 1000), `--font` (default `impact`), and `--skip-template-check`, which skips the check that the template has as many caption boxes as you gave lines. Use it only when memegen's `/templates` endpoint is down but the image endpoint is not.

To regenerate every meme, for example after changing a default:

```bash
rm graphics/memes/*.png graphics/memes/*.spec
quarto render --to html
```

The defaults live in two places that must agree: the argparse defaults in `generate_chapter_meme.py` and the `or "1000"` / `or "impact"` fallbacks in `chapter-meme.lua`.

## Things that have gone wrong before

- **Captions missing.** memegen's documented `?text[]=` query form doesn't fill captions on the image endpoint ([memegen#993](https://github.com/jacebrowning/memegen/issues/993)), so the generator builds path-style URLs and escapes memegen's reserved characters itself.
- **Captions silently dropped.** memegen truncates extra lines without complaint, which is why the generator checks the template's line count first.
- **Push fails after a full regeneration.** All 37 PNGs are about 23 MB, more than git's default HTTP buffer. Push with `git -c http.postBuffer=524288000 push`.
- **Image path.** The shortcode and the margin header both use `/graphics/memes/<slug>.png` with a leading slash so the path does not depend on how deep the chapter sits; Quarto rewrites it per page, in the margin header too.
- **Margin notes near the top** of a chapter (a footnote in Purpose, with `reference-location: margin`) collapse the table of contents at load, just as the margin meme did. Link inline instead.

## History

The shortcode was a Quarto extension at `_extensions/cuinfo/chapter-meme/` (title "Chapter Meme", version 0.1.0, requiring Quarto 1.9 or later) and the generator lived in `scripts/`. Both moved here in September 2026 so that the shortcode sits beside the script it calls; the project-level `shortcodes:` key replaces the extension's `_extension.yml`. The first generator used memeplotlib, which drew captions outside many templates' text boxes; see `docs/decisions.md` (2026-04-28).
