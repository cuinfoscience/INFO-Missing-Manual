# Paratechnical Computing Handbook

[![Build book](https://github.com/brianckeegan/ParatechnicalComputingHandbook/actions/workflows/build-book.yml/badge.svg)](https://github.com/brianckeegan/ParatechnicalComputingHandbook/actions/workflows/build-book.yml)

A reference book for the skills that fall between knowing what to type and working like a professional. The *Paratechnical Computing Handbook* teaches the "hidden curriculum" of computing: the tools, practices, and mental models that most courses assume you already know.

**Authors:** Brian C. Keegan & Abram Handler

---

## Who this is for

Undergraduate students in data science, social science, humanities, and adjacent fields who use Python and computing as tools. No prior CS background assumed. The handbook covers what happens around the code — environments, documentation, debugging, collaboration, and automation — and is designed to be **used as reference documentation** rather than read front-to-back. Drop into any chapter that matches your current problem; each chapter opens with a "Prerequisites and see-also" callout linking to related material if you need more context.

---

## Building the book

### Prerequisites

- **Quarto ≥ 1.9.0** — https://quarto.org/docs/download/ (the `llms-txt` feature requires 1.9.0+)
- **TinyTeX** for PDF rendering — run `quarto install tinytex` after installing Quarto

### Commands

From the repo root:

```bash
# Interactive preview with live reload
quarto preview

# Full render to HTML + PDF
quarto render

# HTML only (much faster iteration)
quarto render --to html

# PDF only
quarto render --to pdf
```

Output lands in `_book/`:

- `_book/index.html` — landing page for the HTML book
- `_book/Paratechnical-Computing-Handbook.pdf` — printable PDF
- `_book/llms.txt` and per-chapter `*.llms.md` — machine-readable versions designed to be ingested by LLMs (see https://quarto.org/docs/websites/website-llms.html)

---

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
└── .github/workflows/build-book.yml # CI: renders HTML + PDF
```

---

## Book contents

| Part | Chapters | Theme |
|------|----------|-------|
| **I — Practice of Technical Work** | Asking Questions, Documentation, Debugging, Reading Tracebacks, AI Tools | Human and cognitive skills that underpin all technical work |
| **II — Computing Environment** | OS, File System, Terminal, Text Editors, Remote Computing | The infrastructure you work inside |
| **III — Python Management** | Package Management, Virtual Environments, Jupyter, Scripting, Testing | The Python working context |
| **IV — Working with Data** | Data File Formats | Moving data from files into your analysis |
| **V — Project Management** | Project Management, Version Control, Collaboration, Automation | Shipping and sustaining work with others |
| **VI — Algorithmic Systems** | LLM Internals, AI Agents, Evaluating AI | Working with AI tools deliberately |

---

## Contributing

Before contributing, read `CLAUDE.md` for the full style guide, chapter structure template, cross-reference syntax, and conventions.

The short version:

- Each content chapter follows the canonical 8-section structure (Purpose → Learning objectives → Running theme → numbered content sections → Worked examples → Templates → Exercises → One-page checklist → optional Quick reference).
- Every chapter begins with a `::: {.callout-tip}` "Prerequisites and see-also" block so readers know what to read first and what to read next.
- Tone: friendly guide, second-person ("you"), empathetic but rigorous.
- Cross-references: `@sec-<slug>` (see the label table in `CLAUDE.md`).
- Citations: `[@bibkey]`, with entries in `references.bib`.
- Formatting: `**bold**`, `*italic*`, `` `code` ``, fenced code blocks with language hints.

---

## CI

Every push and pull request triggers `.github/workflows/build-book.yml`, which runs `quarto render` in an Ubuntu runner with a pinned Quarto version and TinyTeX. The rendered `_book/` output is uploaded as an artifact named `paratechnical-computing-handbook` and retained for 30 days.
