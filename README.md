# Missing Manual for Information Scientists

[![Render and Publish](https://github.com/brianckeegan/ParatechnicalComputingHandbook/actions/workflows/build-book.yml/badge.svg)](https://github.com/brianckeegan/ParatechnicalComputingHandbook/actions/workflows/build-book.yml)

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
ParatechnicalComputingHandbook/
│
├── _quarto.yml                      # book configuration
├── index.qmd                        # landing page / introduction
├── conclusion.qmd                   # final chapter
├── appendix-glossary.qmd            # Appendix A — Glossary
├── references.bib                   # BibTeX bibliography
│
├── parts/
│   ├── part-1-practice/             # Part I — Practice of Technical Work
│   ├── part-2-environment/          # Part II — Computing Environment
│   ├── part-3-python/               # Part III — Python Management
│   ├── part-4-data/                 # Part IV — Working with Data
│   ├── part-5-projects/             # Part V — Project Management
│   └── part-6-algorithmic/          # Part VI — Algorithmic Systems
│
├── graphics/                        # images used in chapters
└── .github/workflows/build-book.yml # CI: renders + publishes to GitHub Pages
```

## Book contents

| Part | Chapters | Theme |
|------|----------|-------|
| **I — Practice of Technical Work** | Asking Questions, Documentation, Debugging, Reading Tracebacks, AI Tools, Reading Docs | Human and cognitive skills that underpin all technical work |
| **II — Computing Environment** | OS, File System, Terminal, Text Editors, Remote Computing | The infrastructure you work inside |
| **III — Python Management** | Package Management, Virtual Environments, Jupyter, Scripting, Regex, Linting | The Python working context |
| **IV — Working with Data** | Data File Formats, Tabular Data, Pandas Basics, SQL Basics, HTTP and APIs | Getting data in, out, and into shape |
| **V — Project Management** | Project Management, Version Control, Collaboration, Automation, Secrets | Shipping and sustaining work with others |
| **VI — Algorithmic Systems** | LLM Internals, AI Agents, Evaluating AI | Working with AI tools deliberately |

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

The latest build is published to <https://brianckeegan.github.io/ParatechnicalComputingHandbook/>.

## Citation

If you use this book in teaching or research, please cite:

```bibtex
@book{keegan_2026_missing_manual,
  author    = {Keegan, Brian C.},
  title     = {Missing Manual for Information Scientists: The Hidden Curriculum of Computing Technologies},
  year      = {2026},
  publisher = {Department of Information Science, University of Colorado Boulder},
  url       = {https://github.com/brianckeegan/ParatechnicalComputingHandbook}
}
```

## License

Released under the [MIT License](LICENSE).

## AI Disclosure

Portions of this book were drafted with assistance from large language model tools, including Claude. All content has been reviewed and edited by the author. See the [AI Disclosure appendix](appendix-ai-disclosure.qmd) for the full statement.

## Acknowledgments

This book grew out of teaching undergraduate data science and information science students at the University of Colorado Boulder. It reflects the questions, frustrations, and feedback of many cohorts who pushed back on what was missing from the standard curriculum.
