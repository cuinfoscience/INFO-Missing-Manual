"""Blur parts of a page before it is captured: names, faces, anything that identifies someone.

A figure's `blur:` lists CSS selectors, e.g. for a GitHub review thread:

    blur: ['.author', 'img.avatar']

Each selector must match at least one element, or the take fails. A selector
that stops matching after a site redesign would otherwise leave a name in
frame without a word. Blurred text stays in the page, so text measurements
still count it; only the pixels change.
"""
RADIUS = 6  # CSS pixels: enough to make 14-pixel text and a 20-pixel avatar unreadable


def apply(page, selectors):
    """Blur each selector's elements; return problems (selectors that matched nothing)."""
    problems = []
    for sel in selectors:
        if page.locator(sel).count() == 0:
            problems.append(f"blur: `{sel}` matched nothing, so whatever it should hide is in frame")
    page.add_style_tag(content=", ".join(selectors) + f" {{ filter: blur({RADIUS}px) !important; }}")
    return problems
