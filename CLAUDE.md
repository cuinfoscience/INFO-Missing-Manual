# CLAUDE.md — Paratechnical Computing Handbook

This file guides Claude Code sessions working on this repository. Read it before making any changes.

---

## Project Overview

The **Paratechnical Computing Handbook** is a LaTeX textbook for undergraduate non-CS majors — students in social science, humanities, data science, and adjacent fields who use computing as a tool but haven't learned the systematic practices that surround it. The handbook fills the "hidden curriculum" gap: the skills that fall between knowing what to type and understanding how to work professionally.

**Authors:** Brian C. Keegan & Abram Handler
**Format:** LaTeX using the Tufte-book class
**Main file:** `!main.tex` (the exclamation mark makes it sort to the top)

---

## How to Build

### Prerequisites
- TeX Live Full (Linux/macOS) or MacTeX (macOS) or MiKTeX (Windows)
- Packages used: `amsmath`, `enumitem`, `booktabs`, `titlesec`, `listings`, `fvextra`, `xcolor`, `hyperref`, `geometry`, `mdframed`, `fontenc`, `inputenc`, `microtype`, `datetime`, `graphicx`
- Custom Tufte-book class files in the repo root: `tufte-book.cls`, `tufte-common.def`, `tufte.bst`

### Compile
Run `pdflatex` **twice** to resolve cross-references and the table of contents:

```bash
pdflatex "!main.tex"
pdflatex "!main.tex"
```

Run a third time if cross-reference page numbers in the output show `??`.

### Verify
After compilation, check:
- No `Undefined reference` warnings
- Table of contents renders correctly
- All `\ref{}` commands resolve (no `??` in PDF)

---

## Repository Structure

```
ParatechnicalComputingHandbook/
│
├── !main.tex                        # Master document: preamble, \input order
├── ch00_introduction.tex            # Introduction (no label needed)
├── ch20_conclusion.tex              # Conclusion chapter
├── ch99_appendices.tex              # Appendices (glossary / how-tos)
├── references.bib                   # BibTeX bibliography
│
├── tufte-book.cls                   # Tufte book class — DO NOT EDIT
├── tufte-common.def                 # Tufte common definitions — DO NOT EDIT
├── tufte.bst                        # Tufte bibliography style — DO NOT EDIT
│
├── Part I - Practice of Technical Work/
│   ├── questions.tex                # Asking Technical Questions (ch:asking-questions)
│   ├── documentation.tex            # Technical Documentation (ch:documentation)
│   ├── debugging.tex                # Debugging (ch:debugging)
│   └── ai_llm.tex                   # Using AI Tools (ch:ai-llm)
│
├── Part II - Computing Environment/
│   ├── operating_system.tex         # Operating System (ch:os-management)
│   ├── file_system.tex              # Local File System (ch:filesystem)
│   ├── terminal.tex                 # Command Line (ch:terminal)
│   ├── text_editors.tex             # Text Editors (ch:text-editors)
│   └── remote.tex                   # Remote Computing (ch:remote-computing)
│
├── Part III - Python Management/
│   ├── package_management.tex       # Package Management (ch:pkg-mgmt)
│   ├── jupyter.tex                  # Jupyter (ch:jupyter)
│   └── scripting.tex                # Scripting (ch:scripts-vs-notebooks)
│
├── Part IV - Project Management/
│   ├── project_management.tex       # Project Management (ch:project-management)
│   ├── version_control.tex          # Version Control (ch:git-github)
│   ├── collaboration.tex            # Collaboration Mechanics (ch:collaboration)
│   └── automation.tex               # Automation (ch:automation)
│
└── graphics/                        # PNG images referenced in chapters
```

---

## Chapter Labels (for \ref{})

Every content chapter already has a `\label{}` immediately after `\chapter{}`. Use these labels for cross-references:

| Chapter | Label |
|---------|-------|
| Asking Technical Questions | `\ref{ch:asking-questions}` |
| Technical Documentation | `\ref{ch:documentation}` |
| Debugging | `\ref{ch:debugging}` |
| Using AI Tools | `\ref{ch:ai-llm}` |
| Operating System | `\ref{ch:os-management}` |
| Local File System | `\ref{ch:filesystem}` |
| Command Line | `\ref{ch:terminal}` |
| Text Editors | `\ref{ch:text-editors}` |
| Remote Computing | `\ref{ch:remote-computing}` |
| Package Management | `\ref{ch:pkg-mgmt}` |
| Jupyter | `\ref{ch:jupyter}` |
| Scripting | `\ref{ch:scripts-vs-notebooks}` |
| Project Management | `\ref{ch:project-management}` |
| Version Control | `\ref{ch:git-github}` |
| Collaboration Mechanics | `\ref{ch:collaboration}` |
| Automation | `\ref{ch:automation}` |

**Inline reference format:**
```latex
(see Chapter~\ref{ch:debugging})
```

**Margin note format** (use when the reference is supplementary, not essential):
```latex
\marginnote{Debugging techniques are covered in Chapter~\ref{ch:debugging}.}
```

---

## Style Guide

### Tone and Voice
- **Friendly guide** — warm, second-person, like a knowledgeable senior colleague
- Always address the reader as **"you"** (not "the user", "the student", "one", or "a reader")
- Empathetic about frustration; high expectations about capability
- Direct and imperative for instructions: "Run this command", "Check the version"
- Non-judgmental about mistakes and questions

### Chapter Structure (canonical — every content chapter follows this)
1. `\section*{Purpose}` — one to three paragraphs explaining why this chapter exists
2. `\section*{Learning objectives}` — numbered list; intro always: *"By the end of this chapter, you should be able to:"*
3. `\section*{Running theme: <short phrase>}` — one-sentence principle for the chapter
4. `\section{...}` — numbered content sections
5. `\section{Worked examples (outline)}` — subsections with bullet-list outlines
6. `\section{Templates}` — subsections with `\begin{verbatim}` blocks (not all chapters)
7. `\section{Exercises}` — numbered list with `[noitemsep]`
8. `\section{One-page checklist}` — bulleted list with `[noitemsep]`
9. `\section{Quick reference: ...}` — optional; named consistently as "Quick reference: ..."

### Formatting Rules

**Lists:**
```latex
\begin{itemize}[noitemsep,topsep=0pt]
  \item ...
\end{itemize}

\begin{enumerate}[noitemsep,topsep=0pt]
  \item ...
\end{enumerate}
```

**Code — multi-line blocks:**
```latex
\begin{verbatim}
code goes here
\end{verbatim}
```

**Code — inline:**
```latex
\texttt{command-name}
```

**Bold / emphasis:**
```latex
\textbf{important term}    % bold for first definitions
\emph{concept}             % italic for emphasis
```

**Section headings by level:**
```latex
\section{Top-level numbered content section}
\subsection{Sub-topic}
\paragraph{Named inline break.}  % no extra space below
```

**Unnumbered sections (Purpose, Learning objectives, Running theme only):**
```latex
\section*{Purpose}
\section*{Learning objectives}
\section*{Running theme: phrase here}
```

**Cross-references:**
```latex
Chapter~\ref{ch:label}   % tilde prevents line break between "Chapter" and number
```

**Citations:**
```latex
\cite{key}
\cite{key1,key2}
```

**Links:**
```latex
\href{https://example.com}{link text}
```

**Margin notes** (Tufte feature):
```latex
\marginnote{Short supplementary note.}
\sidenote{Numbered footnote in the margin.}
```

### What Not to Change
- **`tufte-book.cls`, `tufte-common.def`, `tufte.bst`** — template files; never edit these
- **`!main.tex` preamble** — only add `\input{}` lines at the bottom when adding chapters; do not change package imports without a clear reason
- **`\kibitz{}` and `\abe{}` comment macros** — these are author annotation macros that can be toggled on/off; leave them in place

---

## Common Tasks

### Add a new chapter
1. Create `Part X - Name/new_chapter.tex`
2. Add `\chapter{Title}\label{ch:slug}` at the top of the file
3. Follow the canonical 8-section structure above
4. Add `\input{Part X - Name/new_chapter}` in `!main.tex` at the correct position
5. Run `pdflatex` twice to update the ToC

### Add a cross-reference
1. Confirm the target chapter has a `\label{ch:slug}` (all current chapters do)
2. In the source chapter, add: `(see Chapter~\ref{ch:slug})`
3. Run `pdflatex` twice; verify no `??` warnings

### Add a figure
1. Place the PNG in `graphics/`
2. Use the Tufte margin figure for small images:
   ```latex
   \begin{marginfigure}
     \includegraphics[width=\textwidth]{graphics/filename.png}
     \caption{Caption text.}
     \label{fig:slug}
   \end{marginfigure}
   ```

### Add a bibliography entry
1. Add the BibTeX entry to `references.bib`
2. Cite with `\cite{key}` in the text
3. The `\nobibliography` style is used — entries appear as inline citations only

---

## Gap Analysis (Known Missing Content)

The following paratechnical topics are absent or under-served. These are candidates for future chapters or section additions:

**High priority:**
- Testing (`pytest` basics, what a test is) — strongest case for a new `testing.tex` chapter in Part III
- Reading Python tracebacks — new section in `debugging.tex`
- Regular expressions — new section in `terminal.tex` under "Searching"
- HTTP/APIs/`requests` — new section in Part III (`scripting.tex` or new chapter)
- `.env` files and secrets hygiene — expand `terminal.tex` or `package_management.tex`

**Medium priority:**
- Code style/linting (`black`, `ruff`) — add to `scripting.tex` or `collaboration.tex`
- How to read official documentation / docstrings — new section in `documentation.tex`
- Data file formats (CSV vs JSON vs Parquet) — new section in `file_system.tex`
- `venv` workflow — add subsection in `package_management.tex`
- `pre-commit` hooks — add to `version_control.tex` or `automation.tex`

**Lower priority:**
- Shell scripting (bash `.sh`) — expand `automation.tex`
- Profiling/performance (`%%timeit`, `cProfile`) — add to `jupyter.tex`
- Containers/Docker intro — add to `automation.tex`
- Markdown syntax — add to `documentation.tex`

---

## CI/CD

A GitHub Actions workflow at `.github/workflows/build-pdf.yml` runs `pdflatex` on every push and PR using `xu-cheng/latex-action@v3`. The compiled PDF is uploaded as a build artifact named `handbook-pdf`. Check the Actions tab on GitHub to verify builds pass after edits.
