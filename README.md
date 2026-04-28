# Missing Manual for Information Scientists

[![Render and Publish](https://github.com/cuinfoscience/INFO-Missing-Manual/actions/workflows/build-book.yml/badge.svg)](https://github.com/cuinfoscience/INFO-Missing-Manual/actions/workflows/build-book.yml)

A reference book for the skills that fall between knowing what to type and working like a professional. The *Missing Manual for Information Scientists* teaches the "hidden curriculum" of computing: the tools, practices, and mental models that most courses assume you already know.

**Author:** Brian C. Keegan

## Who this is for

Undergraduate students in data science, social science, humanities, and adjacent fields who use Python and computing as tools. No prior CS background assumed. The handbook covers what happens around the code — environments, documentation, debugging, collaboration, and automation — and is designed to be **used as reference documentation** rather than read front-to-back. Drop into any chapter that matches your current problem; each chapter opens with a "Prerequisites and see-also" callout linking to related material if you need more context.

## Building the book

### Prerequisites

- **Quarto ≥ 1.9.0** — https://quarto.org/docs/download/ (the `llms-txt` feature requires 1.9.0+)
- **TinyTeX** (optional) — only needed if you want to render the PDF locally (`quarto install tinytex`). CI renders HTML only.

### Commands

From the repo root:

```bash
# Interactive preview with live reload
quarto preview

# Render HTML (matches CI)
quarto render --to html

# Render PDF locally (requires TinyTeX)
quarto render --to pdf
```

Output lands in `book/`:

- `book/index.html` — landing page for the HTML book
- `book/llms.txt` and per-chapter `*.llms.md` — machine-readable versions designed to be ingested by LLMs (see https://quarto.org/docs/websites/website-llms.html)
- `book/*.pdf` — only if you rendered `--to pdf` locally

## Project structure

```
INFO-Missing-Manual/
│
├── _quarto.yml                      # book configuration
├── index.qmd                        # landing page / introduction
├── conclusion.qmd                   # final chapter
├── references.bib                   # BibTeX bibliography
│
├── parts/
│   ├── part-1-practice/             # Part I   — Practice of Technical Work
│   ├── part-2-environment/          # Part II  — Computing Environment
│   ├── part-3-python/               # Part III — Python Management
│   ├── part-4-data/                 # Part IV  — Working with Data
│   ├── part-5-communication/        # Part V   — Communication
│   ├── part-5-projects/             # Part VI  — Project Management (directory slug retained)
│   ├── part-6-algorithmic/          # Part VII — Algorithmic Systems (directory slug retained)
│   └── appendix/
│       ├── appendix-glossary.qmd        # Appendix A — Glossary
│       └── appendix-ai-disclosure.qmd   # Appendix B — AI Disclosure
│
├── graphics/                        # images used in chapters
│   └── memes/                       # generated chapter memes (PNG + .spec hash)
├── scripts/
│   ├── generate_chapter_meme.py     # thin wrapper around memeplotlib
│   └── requirements.txt             # Python deps for the meme generator
├── _extensions/cuinfo/chapter-meme/ # Quarto shortcode that drives the generator
└── .github/workflows/build-book.yml # CI: renders + publishes to GitHub Pages
```

### Chapter memes

Each chapter declares an optional meme in its YAML frontmatter:

```yaml
meme:
  template: "fine"           # memegen template id
  lines:
    - ""
    - "MY CODE IS ON FIRE BUT THIS IS FINE"
  alt: "Short caption for screen readers."
  rationale: "humor — optional source-only note explaining the choice"
  # fontsize: 192            # optional override; default 192 (≈2.7× memeplotlib's default of 72)
```

The chapter then invokes the shortcode at the desired location (conventionally just below the `## Purpose` heading):

```markdown
{{< chapter-meme >}}
```

A Lua shortcode in `_extensions/cuinfo/chapter-meme/` reads the frontmatter, calls `scripts/generate_chapter_meme.py`, and caches the result at `graphics/memes/<slug>.png` with a sidecar `.spec` hash for change detection. The generator is a thin wrapper around the [memeplotlib](https://github.com/brianckeegan/memeplotlib) library (≥0.2.0); install Python deps via `pip install -r scripts/requirements.txt`. The cache key includes the template id, the `fontsize`, and the lines, so editing any of the three invalidates the cached PNG on the next render.

To force a regeneration of every meme (e.g. after changing the default font size):

```bash
rm graphics/memes/*.png graphics/memes/*.spec
quarto render --to html
```

## Book contents

| Part | Chapters | Theme |
|------|----------|-------|
| **I — Practice of Technical Work** | Asking Questions, Documentation, Common Text Formats, Reading Docs, Debugging, Reading Tracebacks, Artifacts Have Politics | Human and cognitive skills that underpin all technical work |
| **II — Computing Environment** | OS, File System, Terminal, Text Editors, Remote Computing | The infrastructure you work inside |
| **III — Python Management** | Package Management, Virtual Environments, Jupyter, Scripting, Regex, Linting | The Python working context |
| **IV — Working with Data** | Data File Formats, Tabular Data, Pandas Basics, SQL Basics, HTTP and APIs | Getting data in, out, and into shape |
| **V — Communication** | Reading Scholarship, Writing Manuscripts, Writing a Thesis, Presenting, LaTeX | The genres an information scientist is asked to produce |
| **VI — Project Management** | Project Management, Version Control, Collaboration, Automation, Secrets | Shipping and sustaining work with others |
| **VII — Algorithmic Systems** | Using AI Tools, LLM Internals, AI Agents, Evaluating AI | Working with AI tools deliberately |

## Contributing

Before contributing, read `CLAUDE.md` for the full style guide, chapter structure template, cross-reference syntax, and conventions.

The short version:

- Each content chapter follows the canonical 8-section structure (Purpose → Learning objectives → Running theme → numbered content sections → Worked examples → Templates → Exercises → One-page checklist → optional Quick reference).
- Every chapter begins with a `::: {.callout-tip}` "Prerequisites and see-also" block so readers know what to read first and what to read next.
- Tone: friendly guide, second-person ("you"), empathetic but rigorous.
- Cross-references: `@sec-<slug>` (see the label table in `CLAUDE.md`).
- Citations: `[@bibkey]`, with entries in `references.bib`.
- Formatting: `**bold**`, `*italic*`, `` `code` ``, fenced code blocks with language hints.

## CI

Every push to `main` triggers `.github/workflows/build-book.yml`, which renders the book and publishes it to GitHub Pages via the `gh-pages` branch (`quarto-dev/quarto-actions/publish@v2`). Pull requests against `main` run a render-only job for validation but do not publish. The workflow can also be triggered manually from the Actions tab. PDF rendering is local-only — install TinyTeX and run `quarto render --to pdf` if you want one.

## Rendered book

The latest build is published to <https://cuinfoscience.github.io/INFO-Missing-Manual/>.

## Citation

If you use this book in teaching or research, please cite:

```bibtex
@book{keegan_2026_missing_manual,
  author    = {Keegan, Brian C.},
  title     = {Missing Manual for Information Scientists: The Hidden Curriculum of Computing Technologies},
  year      = {2026},
  publisher = {Department of Information Science, University of Colorado Boulder},
  url       = {https://github.com/cuinfoscience/INFO-Missing-Manual}
}
```

## License

Released under the [MIT License](LICENSE).

## AI Disclosure

Portions of this book were drafted with assistance from large language model tools, including Claude. All content has been reviewed and edited by the author. See the [AI Disclosure appendix](parts/appendix/appendix-ai-disclosure.qmd) for the full statement.

## Acknowledgments

This book grew out of teaching undergraduate data science and information science students at the University of Colorado Boulder. It reflects the questions, frustrations, and feedback of many cohorts who pushed back on what was missing from the standard curriculum.
