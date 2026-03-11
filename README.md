# Paratechnical Computing Handbook

[![Build PDF](https://github.com/brianckeegan/ParatechnicalComputingHandbook/actions/workflows/build-pdf.yml/badge.svg)](https://github.com/brianckeegan/ParatechnicalComputingHandbook/actions/workflows/build-pdf.yml)

A textbook for the skills that fall between knowing what to type and working like a professional. The *Paratechnical Computing Handbook* teaches the "hidden curriculum" of computing: the tools, practices, and mental models that most courses assume you already know.

**Authors:** Brian C. Keegan & Abram Handler

---

## Who this is for

Undergraduate students in social science, humanities, data science, and adjacent fields who use Python and computing as tools. No prior CS background assumed. The handbook covers what happens around the code — environments, documentation, debugging, collaboration, and automation.

---

## Building the PDF

### Prerequisites

Install a full TeX Live distribution:

| Platform | Installer |
|----------|-----------|
| Linux | `sudo apt install texlive-full` |
| macOS | [MacTeX](https://www.tug.org/mactex/) |
| Windows | [MiKTeX](https://miktex.org/) or WSL + `texlive-full` |

### Compile

Run `pdflatex` twice from the repository root (two passes are required to resolve the table of contents and cross-references):

```bash
pdflatex "!main.tex"
pdflatex "!main.tex"
```

The output file is `!main.pdf`.

If cross-reference page numbers show as `??`, run a third pass:

```bash
pdflatex "!main.tex"
```

---

## Project Structure

```
ParatechnicalComputingHandbook/
│
├── !main.tex                          # Master document
├── ch00_introduction.tex              # Introduction
├── ch20_conclusion.tex                # Conclusion
├── ch99_appendices.tex                # Glossary and appendices
├── references.bib                     # Bibliography
│
├── Part I - Practice of Technical Work/
│   ├── questions.tex                  # Asking Technical Questions
│   ├── documentation.tex              # Technical Documentation
│   ├── debugging.tex                  # Debugging
│   └── ai_llm.tex                     # Using AI Tools
│
├── Part II - Computing Environment/
│   ├── operating_system.tex           # Operating System
│   ├── file_system.tex                # Local File System
│   ├── terminal.tex                   # Command Line
│   ├── text_editors.tex               # Text Editors
│   └── remote.tex                     # Remote Computing
│
├── Part III - Python Management/
│   ├── package_management.tex         # Package Management
│   ├── jupyter.tex                    # Jupyter
│   └── scripting.tex                  # Scripting
│
├── Part IV - Project Management/
│   ├── project_management.tex         # Project Management
│   ├── version_control.tex            # Version Control
│   ├── collaboration.tex              # Collaboration Mechanics
│   └── automation.tex                 # Automation
│
└── graphics/                          # Images used in chapters
```

---

## Handbook Contents

| Part | Chapters | Theme |
|------|----------|-------|
| **I — Practice of Technical Work** | Asking Questions, Documentation, Debugging, AI Tools | Human and cognitive skills that underpin all technical work |
| **II — Computing Environment** | OS, File System, Terminal, Text Editors, Remote Computing | The infrastructure you work inside |
| **III — Python Management** | Package Management, Jupyter, Scripting | The Python working context |
| **IV — Project Management** | Project Management, Version Control, Collaboration, Automation | Shipping and sustaining work with others |

---

## Contributing

Before contributing, read `CLAUDE.md` for the full style guide, chapter structure template, LaTeX conventions, and cross-reference patterns.

The short version:
- Each content chapter follows an 8-section structure (Purpose → Learning objectives → Running theme → Content → Worked examples → Exercises → One-page checklist → optional Quick reference)
- Tone: friendly guide, second-person ("you"), empathetic but rigorous
- Lists use `[noitemsep,topsep=0pt]`; code blocks use `\begin{verbatim}` (multi-line) and `\texttt{}` (inline)
- Cross-references use `Chapter~\ref{ch:label}` — see `CLAUDE.md` for the full label table

---

## CI

Every push and pull request triggers a GitHub Actions workflow that compiles the handbook to PDF using `xu-cheng/latex-action`. The compiled PDF is available as a build artifact in the Actions tab.
