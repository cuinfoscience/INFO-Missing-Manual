# Recipes

One YAML file per chapter, named for the chapter's slug: `jupyter.yml` describes the screenshots in `chapters/jupyter.qmd`, and their approved images go in `graphics/jupyter/`. Every key is documented in [`../README.md`](../README.md); which figures to make, and in what order, is in [`docs/plans/2026-09-24-screenshots.md`](../../../docs/plans/2026-09-24-screenshots.md).

There are no recipes yet. The first ones come with the plan's pilot chapter.

## A starter file

```yaml
# Screenshots for chapters/version-control.qmd. See tools/shots/README.md.
chapter: version-control
defaults:
  pause: [8, 30]            # seconds between page loads on one host (the default)
figures:
  - id: github-repo         # -> graphics/version-control/github-repo.png
    kind: capture
    section: "Hosting on GitHub"
    url: https://github.com/cuinfoscience/INFO-Missing-Manual
    steps:
      - wait: {text: '^Go to file$'}
    expect: {text: ['INFO-Missing-Manual']}
    drifts: true            # a live page: the caption says "in <month> <year>"
```

Then, from the repository root:

```bash
tools/shots/run doctor version-control     # can this session reach the hosts, capture, and draw?
tools/shots/run capture version-control    # takes land in tools/shots/out/version-control/
tools/shots/run sheet version-control      # look at each take at the size the book shows it
tools/shots/run promote version-control github-repo
tools/shots/run check version-control
```

And in the chapter, with the leading slash, a caption that dates a live page, and alt text that transcribes what a reader needs:

```markdown
![The repository's page on GitHub, in September 2026.](/graphics/version-control/github-repo.png){#fig-github-repo fig-alt="…"}
```

## Before you write one

- **Scope first, then size.** Crop to what the text discusses. The window is 800×600 CSS pixels unless a figure says otherwise. If a site's narrow layout hides what the text points to, or the crop loses the context a reader needs to find their place, a figure may show up to 1024×768 with `relaxed:` and a reason, as long as its text still passes where it is shown (usually a wider column: `targets: {book: {column: page-inset-right}}`).
- **Waits need visible text.** A site's narrow layout can hide text its desktop layout shows; the wait then times out.
- **One honest identity.** Don't change `user_agent` in a recipe without a reason in the recipe's `notes:`.
- **Nothing private.** No logins, no personal accounts' pages beyond what the book's own repository shows, no student names or work.
