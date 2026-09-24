# chapter-meme

Puts a meme in the margin beside each chapter's Purpose section. The chapter says what the meme is in its frontmatter; this folder turns that into a PNG and places it.

| File | Role |
|---|---|
| `chapter-meme.lua` | The Quarto shortcode `{{< chapter-meme >}}`. Reads the chapter's `meme:` frontmatter, decides whether the cached PNG is current, calls the generator if it isn't, and emits a `.column-margin` block with the image and its alt text. |
| `generate_chapter_meme.py` | Fetches one meme from the [memegen.link](https://memegen.link) API and writes it to disk. Standard library only. |

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
- **Image path.** The shortcode emits `/graphics/memes/<slug>.png` with a leading slash so the path does not depend on how deep the chapter sits; Quarto rewrites it per page.

## History

The shortcode was a Quarto extension at `_extensions/cuinfo/chapter-meme/` (title "Chapter Meme", version 0.1.0, requiring Quarto 1.9 or later) and the generator lived in `scripts/`. Both moved here in September 2026 so that the shortcode sits beside the script it calls; the project-level `shortcodes:` key replaces the extension's `_extension.yml`. The first generator used memeplotlib, which drew captions outside many templates' text boxes; see `docs/decisions.md` (2026-04-28).
