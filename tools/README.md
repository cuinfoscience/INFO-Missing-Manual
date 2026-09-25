# tools/

The code that supports the book but isn't part of it: generators for the book's images, a script that keeps the issue forms in step with the chapters, and a screenshot toolkit. Each tool has its own folder and README, and each resolves the repository root from its own location, so you can run it from any directory.

| Folder | What it does | When it runs |
|---|---|---|
| [`chapter-meme/`](chapter-meme/) | The `{{< chapter-meme >}}` shortcode and its generator: turns a chapter's `meme:` frontmatter into `graphics/memes/<slug>.png`, and `sync_margin_header.py`, which puts that meme above the table of contents | The shortcode during every render (it only fetches from memegen.link when a meme changed); the sync script by hand after editing a meme, and with `--check` in CI |
| [`terminal-figures/`](terminal-figures/) | Draws the annotated terminal illustrations (`graphics/*-annotated.png`, `ssh-connected.png`, and others) | By hand, after editing a figure |
| [`issue-forms/`](issue-forms/) | Rebuilds the "Which chapter?" dropdown in every issue form from `_quarto.yml` | By hand, after adding, renaming, or reordering a chapter; with `--check` in CI |
| [`shots/`](shots/) | Screenshot toolkit ported from *Web Data Science*: recipes, guarded capture, provenance, legibility checks, and pinned local fixtures (JupyterLab and VS Code in the browser) to capture programs from. Its README's "Patterns and pitfalls" says what earlier captures taught. | By hand, per chapter |
| [`layout-audit/`](layout-audit/) | Browser checks against a rendered copy of the book: whether the table of contents is visible, how wide the columns are, whether they're the same on every page, and whether any page scrolls sideways (on a desktop, or with `--widths 390` on a phone) | By hand, before and after a layout change, and after rewriting a chapter |

`requirements.txt` here is what CI installs before rendering. It is empty on purpose: the meme generator uses the standard library only. `shots/` has its own `requirements.txt`, installed into its own virtual environment by `shots/bootstrap.sh`, and CI never runs it.

## Conventions

- **Outputs are committed.** Every image a tool makes is checked in, so CI renders the book without network access or a browser. The meme shortcode is the one tool that runs during a render, and only on a cache miss.
- **Every generator can check itself.** `--check` (or `shots/run check`) fails when a committed output no longer matches what the tool would produce. Run it before a pull request that touches a tool or its outputs.
- **Standard library first.** A tool that needs third-party packages keeps them in its own `requirements.txt` and virtual environment, as `shots/` does.
- **A new tool gets a folder and a README** saying what it does, how to run it, what it writes, and what can go wrong. Add a row to the table above, and to the structure tree in `AGENTS.md`.
