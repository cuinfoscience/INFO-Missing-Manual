"""How tall a figure's text will be where it is shown, and whether that is enough.

A take's log holds the sizes of the text inside its crop, in the take's own
pixels (lib/measure.py). Each place a figure is shown scales it:

- **book:** the HTML book's body column is 678 CSS pixels wide in a
  1280-pixel-wide window (699 at 1440 and wider; `tools/layout-audit/audit.py
  column` measures it); an image narrower than that is shown at its own width.
  Every chapter figure is shown there unless its recipe says
  `targets: {book: false}`. A figure placed in one of Quarto's wider columns
  says so with `targets: {book: {column: page-inset-right}}` (see COLUMNS);
  `check` confirms the chapter's figure carries that class.
- **slides:** `targets: {slides: {width: 0.8}}` is the fraction of the text
  width the figure fills on a 16:9 course slide, judged on a slide shown
  1920 pixels wide.
- **handout:** `targets: {handout: {width_in: 5.04}}` is its printed width.

The size judged is `p20`, the size that four in five characters reach or
exceed, so a copyright line does not fail a figure but small main text does.
The starting thresholds come from the toolkit plan: 11 pixels in the book and
16 on a 1920-pixel slide. Week 08's `infinite_scroll.png`, dropped because no
one could read it on its slide, measures 11.7 there. For print, 6 points is
the usual floor for small print.

Before any of that, a limit on how much of the screen a figure shows, with
two sides to it. Text has to be readable where the figure is shown, and the
figure must not be so crammed (a site's narrow layout, a crop that cuts away
what the reader needs to find their place) that it stops looking like the
screen the reader has. So:

- **800×600 CSS pixels by default** (1600×1200 image pixels at the default
  scale of 2). In the book's 678-pixel column that keeps text at 85% of its
  size on screen.
- **Up to 1024×768 when a larger view reduces clutter,** such as a site's
  desktop layout instead of its narrow one, or enough of the page around the
  thing the text discusses that a reader can find it, **and the text still
  passes at every target.** The recipe says why in `relaxed:`. In the body
  column a 1024-pixel figure's text shrinks to 66%, so ordinary 14–16 pixel
  page text fails; a relaxed figure usually goes in a wider column
  (`targets: {book: {column: page-inset-right}}`), where it keeps 93%.
- **Beyond that,** or over 800×600 for any other reason, the recipe says why
  in `oversize:` and the warning becomes a note.

Going over is a warning, not an error: `check` fails a figure only when its
text is too small (the thresholds above). (Upstream, in *Web Data Science*,
the column is 778 pixels and there is no relaxed tier; see
tools/shots/UPSTREAM.md.)
"""
BOOK_PX = 678                    # the body column at a 1280-pixel window, the narrowest desktop case
SLIDE_PX = 1920
SLIDE_TEXT = 398.34 / 455.24     # the course decks' text width over paper width (beamer, 16:9)
PT_PER_IN = 72.27
THRESHOLDS = {"book": 11.0, "slides": 16.0, "handout": 6.0}
UNITS = {"book": "px", "slides": "px", "handout": "pt"}
SOFT_LIMIT = (800, 600)          # CSS pixels a figure shows, by default, before a warning
RELAXED_LIMIT = (1024, 768)      # ...and at most with `relaxed:`, when its text passes at every target
# Quarto's wider columns, as wide as this book draws them in a 1280-pixel window
# (tools/layout-audit/audit.py). Each reaches into the right margin, over the table of contents.
COLUMNS = {"body-outset-right": 754, "body-outset": 829, "page-inset-right": 954, "page-right": 1004,
           "page": 1229}


def region(entry):
    """The part of the screen a take or an image shows, in CSS pixels: its size over its scale.
    Images made before the toolkit record no scale; they were captured at 1x."""
    scale = entry.get("scale") or 1
    return round(entry["size"][0] / scale), round(entry["size"][1] / scale)


def book_px(setting):
    """How wide the book shows a figure, in CSS pixels, from its `book` target's settings."""
    if "width_px" in setting:
        return setting["width_px"]
    return COLUMNS.get(setting.get("column"), BOOK_PX)


def size_report(fig, entry, results):
    """What to say about how much of the screen a figure shows: (None, ''), ('note', text), or
    ('warn', text). `results` is judge() for the same take or image."""
    width, height = region(entry)
    if width <= SOFT_LIMIT[0] and height <= SOFT_LIMIT[1]:
        return None, ""
    said = f"shows {width}×{height} CSS pixels, over the {SOFT_LIMIT[0]}×{SOFT_LIMIT[1]} soft limit"
    book = targets(fig).get("book")
    if book is not None and width > book_px(book):
        where = f"the {book['column']} column" if book.get("column") else "the book's column"
        said += f"; {where} shows its text at {round(100 * book_px(book) / width)}% of its size on screen"
    relaxed_w, relaxed_h = RELAXED_LIMIT
    if fig.get("relaxed"):
        if width > relaxed_w or height > relaxed_h:
            return "warn", f"{said}, and over the {relaxed_w}×{relaxed_h} relaxed limit too"
        if not results or not all(ok for *_, ok in results):
            return "warn", (f"{said}; `relaxed:` allows up to {relaxed_w}×{relaxed_h} only while the text "
                            "passes at every target, and it doesn't")
        return "note", f"{said}; relaxed to {relaxed_w}×{relaxed_h}, text passing: {fig['relaxed']}"
    if fig.get("oversize"):
        return "note", f"{said}; allowed: {fig['oversize']}"
    return "warn", said


def size_hint(entry):
    """What to try, for a figure over the soft limit whose recipe gives no reason."""
    width, height = region(entry)
    if width <= RELAXED_LIMIT[0] and height <= RELAXED_LIMIT[1]:
        return ("crop to what the text discusses, or zoom DevTools; or, if the larger view reduces clutter "
                f"and its text passes, say why in `relaxed:` (up to {RELAXED_LIMIT[0]}×{RELAXED_LIMIT[1]})")
    return "crop to what the text discusses, or zoom DevTools, rather than widen the window (or say why in `oversize:`)"


def targets(fig):
    """Where this figure is shown: {name: settings}."""
    wanted = dict(fig.get("targets") or {})
    if fig["chapter"] != "course" and "book" not in wanted:
        wanted["book"] = True
    return {name: (setting if isinstance(setting, dict) else {}) for name, setting in wanted.items()
            if setting not in (False, None)}


def scales(fig, width, annotated=None):
    """Image pixels -> the target's unit, for each target. `width` is the image's width in pixels;
    `annotated` is an annotation record, whose figure is shown in the image's place."""
    out = {}
    shown = width
    if annotated:
        shown = annotated["width_in"] / annotated["unit_in"]       # the annotated figure's width, in image pixels
    for name, setting in targets(fig).items():
        if name == "book":
            display = min(book_px(setting), shown)
            out[name] = display / shown
        elif name == "slides":
            out[name] = setting.get("width", 1.0) * SLIDE_PX * SLIDE_TEXT / shown
        elif name == "handout":
            width_in = setting.get("width_in") or (annotated or {}).get("width_in")
            if width_in:
                out[name] = width_in * PT_PER_IN / shown
    return out


def judge(fig, text, width, annotated=None):
    """[(target, size there, threshold, unit, ok)] for a take's or an image's text sizes."""
    if not text or not text.get("chars"):
        return []
    size = text["p20"]
    return [(name, round(size * factor, 1), THRESHOLDS[name], UNITS[name], size * factor >= THRESHOLDS[name])
            for name, factor in scales(fig, width, annotated).items()]


def describe(results):
    return ", ".join(f"{name} {size:g} {unit} ({'ok' if ok else f'under {limit:g}'})"
                     for name, size, limit, unit, ok in results)
