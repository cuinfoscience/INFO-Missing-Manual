# Missing Manual for Information Scientists

[![Render and Publish](https://github.com/cuinfoscience/INFO-Missing-Manual/actions/workflows/build-book.yml/badge.svg)](https://github.com/cuinfoscience/INFO-Missing-Manual/actions/workflows/build-book.yml)

A reference book for the skills that fall between knowing what to type and working like a professional. The *Missing Manual for Information Scientists* teaches the "hidden curriculum" of computing: the tools, practices, and mental models that most courses assume you already know.

**Author:** Brian C. Keegan

> **Help improve this book.** Found a mistake, got stuck, or have an idea? You don't need to know Git or how to fix it.
> **[Read the contributing guide](CONTRIBUTING.md)**, or go straight to
> [reporting a problem](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new/choose) ·
> [fixing a typo in your browser](CONTRIBUTING.md#fix-it-yourself-in-your-browser) ·
> [suggesting a topic](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=suggestion.yml).

## Who this is for

Undergraduate students in data science, social science, humanities, and adjacent fields who use Python and computing as tools. No prior CS background assumed. The handbook covers what happens around the code — environments, documentation, debugging, collaboration, and automation — and is designed to be **used as reference documentation** rather than read front-to-back. Drop into any chapter that matches your current problem; each chapter opens with a "Prerequisites and see-also" callout linking to related material if you need more context.

## Building the book

### Prerequisites

- **Quarto 1.10 or later** — https://quarto.org/docs/download/ (CI uses 1.10.18; Quarto 1.9.15 rejects the `llms-txt` setting in `_quarto.yml`)
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
├── CONTRIBUTING.md                  # how to report a problem or contribute (start here)
├── AGENTS.md                        # instructions for AI agents and contributors
├── CLAUDE.md                        # imports AGENTS.md, for Claude Code
├── docs/                            # project records: decisions, hand-off, roadmap, AARs, plans
│
├── chapters/                        # every chapter and appendix, one flat directory
│                                    # part grouping and reading order live in _quarto.yml
│
├── styles/layout.css                # the same column widths on every chapter
├── graphics/                        # images used in chapters
│   ├── memes/                       # generated chapter memes (PNG + .spec hash)
│   └── <chapter>/                   # screenshots for one chapter, with provenance.json
├── tools/                           # supporting code, one folder per tool, each with a README
│   ├── chapter-meme/                # the {{< chapter-meme >}} shortcode and its generator
│   ├── terminal-figures/            # annotated terminal illustrations
│   ├── issue-forms/                 # keeps the issue forms' chapter list in step with the book
│   ├── shots/                       # screenshot toolkit (recipes, capture, provenance, checks)
│   └── layout-audit/                # browser checks on a rendered copy of the book
├── .github/ISSUE_TEMPLATE/          # issue forms readers use to report problems
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
  # width: 1000              # optional override; default 1000 (output width in pixels)
  # font: "impact"           # optional override; default "impact"
```

The chapter then invokes the shortcode at the desired location (conventionally just below the `## Purpose` heading):

```markdown
{{< chapter-meme >}}
```

A Lua shortcode in `tools/chapter-meme/` (loaded by the `shortcodes:` key in `_quarto.yml`) reads the frontmatter, calls the generator beside it, and caches the result at `graphics/memes/<slug>.png` with a sidecar `.spec` hash for change detection. The generator hits the public [memegen.link](https://memegen.link) API; no Python dependencies are required beyond the stdlib. The cache key includes the template id, the `width`, the `font`, and the lines, so editing any of the four invalidates the cached PNG on the next render.

To force a regeneration of every meme (e.g. after changing the default width or font):

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
| **Appendices** | Glossary, AI Disclosure | Terms defined once, and how AI was used to write the book |

The introduction opens the book and a conclusion closes it, 41 pages in all.

## Where the book is going

In September 2026 every chapter was rewritten in the book's current voice (informal, welcoming, honest about what confuses people, and linked to official tutorials and Wikipedia), with every code example run and every fact re-checked. Ten simulated peer reviews of the whole book followed, and a plan to revise it from them: fix what they found wrong, reconsider the order of a few chapters, add a setup appendix and one running project, and perhaps new chapters on charts, on sharing and archiving data, and on writing at work. The plan waits on the author's decisions. The [roadmap](docs/roadmap.md) tracks it, and [`docs/handoff.md`](docs/handoff.md) says where work stands today.

## Contributing

Contributions of every size are welcome, from a typo report to a new chapter, and most need no programming. **Start with [CONTRIBUTING.md](CONTRIBUTING.md)**: it walks through reporting a problem with the [issue forms](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new/choose), fixing something in your browser with no installs, and making larger changes on your own computer. The full style guide is in [`AGENTS.md`](AGENTS.md), and topics already wanted are in the [roadmap](docs/roadmap.md).

The short version of the style:

- Each content chapter follows the same outline: Purpose → Why read this chapter → Running theme → numbered content sections → Stakes and politics → Worked examples → Templates → Exercises → One-page checklist → optional Quick reference → Further reading.
- Every chapter begins with a `::: {.callout-tip}` "Prerequisites and see-also" block so readers know what to read first and what to read next.
- Voice: a knowledgeable friend talking you through it, not technical documentation. Second person ("you"), narrative rather than lists of facts, honest about what confuses people, and still authoritative. `chapters/tabular-data.qmd` is the model.
- Every code block runs, every fact holds, and every reference is real.
- Cross-references: `@sec-<slug>` (see the label table in `AGENTS.md`).
- Citations: `[@bibkey]`, with entries in `references.bib`.
- Formatting: `**bold**`, `*italic*`, `` `code` ``, fenced code blocks with language hints.

## For AI agents

Instructions for AI coding agents — Claude Code, Codex, and others — are in [`AGENTS.md`](AGENTS.md). If your agent looks for its own instructions file (`CLAUDE.md`, `GEMINI.md`, `.cursorrules`, and so on), point it at `AGENTS.md`: the repository keeps one set of instructions, and `CLAUDE.md` only imports it.

Project records are in [`docs/`](docs/): the hand-off note ([`docs/handoff.md`](docs/handoff.md)) that says where work stands, the decision log ([`docs/decisions.md`](docs/decisions.md)), the roadmap, after-action reports, and plans. Read the hand-off note and the decision log before starting, and update them when you stop.

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

Portions of this book were drafted with assistance from large language model tools, including Claude. In September 2026, AI coding agents (Claude Code) rewrote every chapter in the book's current voice, running the code examples and checking links and facts as they went; each part of the book came to the author as a pull request, and the author merged each one. The ten peer reviews in [`docs/`](docs/aar/2026-09-25-peer-review.md) were also written by AI agents, and say so. See the [AI Disclosure appendix](chapters/appendix-ai-disclosure.qmd) for the full statement.

## Acknowledgments

This book grew out of teaching undergraduate data science and information science students at the University of Colorado Boulder. It reflects the questions, frustrations, and feedback of many cohorts who pushed back on what was missing from the standard curriculum.
