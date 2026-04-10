# 11  Text Editors

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-filesystem](#sec-filesystem).
>
> **See also:** [sec-terminal](#sec-terminal), [sec-git-github](#sec-git-github), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).

## Purpose

Text editors are the primary tool for writing code, configuring tools, inspecting logs, and fixing small problems quickly. For beginners, the main challenge is not typing—it is developing reliable workflows: opening the right file, editing safely, finding and replacing correctly, and understanding the trade-offs between terminal editors, GUI editors, and full IDEs.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what makes a file “text” (vs binary) and why encoding and line endings matter.

2.  Use essential editor operations: open/save, undo/redo, find/replace, multi-file search, and navigation.

3.  Debug common file problems: wrong path, wrong extension, hidden characters, encoding issues, and line-ending mismatches.

4.  Choose an appropriate editor class for a task (terminal editor vs GUI editor vs IDE).

5.  Use a GUI editor for simple scripting: run scripts, read errors, and iterate.

6.  Apply safe refactoring habits with find/replace and version control.

7.  Configure an editor minimally: indentation, formatting, linting, and extensions.

## Running theme: editors are tools, not identities

Choose an editor that fits the task, and build habits that transfer across editors: paths, file formats, search, safe edits, and reproducibility.

## 11.1 A beginner mental model

### Text files are infrastructure

- Code, configuration, logs, and data dictionaries are often plain text.

- Editors are the "workbench" for these artifacts.

### What an editor does (conceptually)

- Reads bytes from disk and interprets them as text using an **encoding** (often UTF-8).

- Displays text with line breaks and whitespace.

- Writes bytes back to disk when you save.

### Key terms

Encoding  
How bytes become characters (UTF-8, etc.).

Line endings  
Newline conventions (LF vs CRLF) that affect cross-platform projects.

Whitespace  
Spaces/tabs/newlines that can change program behavior.

Syntax highlighting  
Visual cues based on language rules.

Linting/formatting  
Automated checks and style normalization.

IDE  
Integrated Development Environment: editor + build + run + debug + tooling.

## 11.2 Choosing your tool: three editor classes

### Terminal editors (nano, vim, emacs)

- Best for: remote servers, quick config edits, minimal environments.

- Strengths: always available, low overhead, works over SSH.

- Trade-offs: steeper learning curve (especially modal editing), fewer visual affordances.

- Recommended student baseline: learn **nano** for emergencies; optionally learn **vim** motions over time.

### GUI code editors (VS Code, Sublime, etc.)

- Best for: daily coursework, scripting, notebooks, lightweight projects.

- Strengths: search across files, integrated terminal, extensions, formatting, linting.

- Trade-offs: can become plugin-heavy; configuration drift across machines.

- Recommended student default: choose one primary GUI editor and learn it well.

### IDEs (Visual Studio, Eclipse, Xcode, etc.)

- Best for: large language ecosystems and complex build systems (Java, C#, Swift, etc.).

- Strengths: deep refactoring, project models, integrated debugging/build tooling.

- Trade-offs: heavier setup; more concepts up front; project configuration can be fragile.

### A decision table (student version)

- **Quick edit on a remote server:** terminal editor.

- **Python scripting + small projects:** GUI editor.

- **Course uses a specific ecosystem (e.g., Java/C#/iOS):** IDE.

- **When unsure:** GUI editor with an integrated terminal.

## 11.3 Essential editor skills (transfer across tools)

### Open, save, and "where did it go?"

- Always know the **file path** you are editing.

- Understand "Save" vs "Save As".

- Recognize read-only files and permission prompts.

- Build a habit: confirm the directory and filename after saving.

### Undo/redo and safe experimentation

- Undo is your first safety net; version control is your second.

- Save small, frequent changes; keep commits focused.

### Indentation and whitespace

- Choose a consistent indentation style for a project.

- Configure your editor to show or make visible whitespace when debugging.

- Understand tabs vs spaces and why Python cares.

### Find, replace, and refactoring safety

- Use "Find" before "Replace".

- Prefer "Replace with confirmation" for nontrivial changes.

- Learn scope: current selection, current file, entire workspace.

- Learn regular expressions (basic level): anchors, wildcards, capture groups.

- After replacing: run tests or re-run the script.

### Multi-file search and navigation

- Use workspace search to locate symbols and strings.

- Learn quick navigation: go to file, go to line, go to definition.

- Keep a mental model of your project root.

## 11.4 Simple scripting workflows in an editor (novice level)

### Write-run-read-repeat loop

1.  Write a small script (10–50 lines).

2.  Run it from the integrated terminal.

3.  Read the error message carefully.

4.  Jump to the referenced file/line.

5.  Make one change at a time and re-run.

### Editor features that help beginners

- Syntax highlighting and bracket matching.

- Auto-indentation and formatting-on-save.

- Linting messages as "early warnings".

- Inline documentation (hover tooltips) and jump-to-definition.

### When a full debugger helps

- Use a debugger when print/logging is too slow or you need to inspect state.

- Learn the minimum: breakpoints, step over/into, variable inspection.

## 11.5 Debugging files (common student failure modes)

### Wrong file, wrong place

- Symptom: edits do not change program behavior.

- Cause: you edited a duplicate file or ran from a different directory.

- Fix: confirm the working directory; search for duplicates; use absolute paths temporarily.

### Wrong extension or hidden extension

- Symptom: file opens in the wrong program or fails to run.

- Fix: show file extensions; confirm `.py`, `.csv`, `.txt`.

### Encoding and invisible characters

- Symptom: weird symbols, parsing errors, or "invalid character" errors.

- Fix: re-save as UTF-8; inspect for non-printing characters; normalize line endings.

### Line endings (Windows/macOS collaboration)

- Symptom: scripts fail, diffs look huge, or tools complain about CRLF/LF.

- Fix: configure editor to use consistent line endings; rely on repo configuration if provided.

### Config files and indentation-sensitive formats

- YAML and similar formats can break with tabs or incorrect indentation.

- Use visible whitespace; validate with the tool that reads the config.

## 11.6 Terminal editors: survival skills

### nano essentials (minimum viable)

- Open, save, exit without panic.

- Search and replace.

- Go to line number.

### vim essentials (minimum viable)

- Modes: normal vs insert; how to get back to normal.

- Save and quit.

- Search and substitute (with confirmation).

- Why vim feels fast: motions + operators (optional preview).

### emacs essentials (minimum viable)

- Open/save/exit.

- Search.

- Basic multi-buffer navigation.

## 11.7 GUI editors: practical configuration (keep it minimal)

### The minimal settings that matter

- Indentation and whitespace display.

- Format on save (using a formatter appropriate to your language).

- A linter for early feedback.

- Integrated terminal.

### Extensions/plugins: a controlled approach

- Install only what you can explain.

- Prefer widely used, well-maintained extensions.

- Avoid overlapping extensions that fight each other.

- Document your essential extensions for reproducibility.

### Workspace settings vs global settings

- Use workspace settings for project-specific behavior.

- Keep global settings simple so you can reproduce work on another machine.

## 11.8 IDEs: fundamentals without overwhelm

### Project model

- IDEs often manage build configuration, dependencies, and run targets.

- Learn where the IDE stores project settings and how to reset or re-import.

### Refactoring and code navigation

- IDE refactors are powerful but must be reviewed.

- Always run tests/build after refactors.

### Debugging integration

- IDEs make breakpoints and stepping easy.

- Learn the minimum and rely on it when print-debugging is not enough.

## 11.9 Best practices: habits that prevent pain

### Pick a primary editor and a fallback

- Primary: your daily GUI editor or required IDE.

- Fallback: nano (and optionally vim) for remote/emergency edits.

### Treat find/replace as a “power tool"

- Narrow scope.

- Preview changes.

- Make a commit before large replacements.

- Verify with tests or a run.

### Keep text files boring

- Use UTF-8.

- Normalize line endings.

- Avoid editing generated files by hand.

- Prefer configuration in version control.

### Use version control as an editor safety net

- Commit logical steps.

- Use diffs to review changes before running.

- Revert when experiments go wrong.

## 11.10 Worked examples (outline)

### Example 1: Write and run a tiny script

- Create `hello.py`.

- Run from the terminal.

- Fix a syntax error using the editor’s line/column cues.

### Example 2: Debug a broken config file

- Identify indentation and invisible-character issues.

- Turn on visible whitespace.

- Validate by re-running the tool.

### Example 3: Safe rename/refactor with find/replace

- Use multi-file search.

- Replace with confirmation.

- Run tests.

### Example 4: Remote emergency edit over SSH

- Open a config file in nano.

- Make a minimal change.

- Save/exit; verify.

## 11.11 Templates

### Template A: Editor setup checklist (first week)

    Editor:

    * Installed and updated
    * Default indentation configured
    * Visible whitespace toggle known
    * Format-on-save configured (if course uses it)
    * Linter installed (if course uses it)
    * Integrated terminal enabled
      Fallback editor:
    * nano basics practiced (open/save/exit/search)

### Template B: Safe find/replace protocol

    1. Search (no replace) and inspect matches
    2. Narrow scope (file/selection/project)
    3. Replace with confirmation
    4. Save and review diff
    5. Run tests or rerun script
    6. Commit with a message describing the change

## 11.12 Exercises

1.  Configure your editor to show line numbers and visible whitespace; explain what you changed.

2.  Write a short script and fix two intentional errors using editor cues.

3.  Perform a multi-file search in a small project; report where a function name appears.

4.  Run a safe find/replace with confirmation and verify by running tests.

5.  Open and edit a file in nano; save and exit confidently.

6.  Optional: learn a minimal vim workflow (insert, save, quit, search).

## 11.13 One-page checklist

- I can open, save, and locate files reliably.

- I can use find/replace safely, including across multiple files.

- I can debug common file issues (paths, extensions, encoding, line endings).

- I understand when to use terminal editors vs GUI editors vs IDEs.

- My editor is minimally configured (indentation, formatting, linting).

- I use version control to review and recover from editing mistakes.

- I have a fallback editor skill for remote/emergency use.

## 11.14 Quick reference: terminal editor survival commands (optional handout)

### nano

- Open: `nano file`

- Save: (document the keystroke)

- Exit: (document the keystroke)

- Find/replace: (document the keystroke)

### vim

## 11.15 Quick reference: GUI/IDE search

- Find in file, replace in file

- Find in workspace, replace in workspace

- Go to line, go to file, go to definition
