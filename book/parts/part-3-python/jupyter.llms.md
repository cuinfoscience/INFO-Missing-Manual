# 15  Jupyter

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-pkg-mgmt](#sec-pkg-mgmt), [sec-virtual-environments](#sec-virtual-environments).
>
> **See also:** [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks), [sec-tracebacks](#sec-tracebacks).

## Purpose

Jupyter notebooks are an effective medium for exploratory analysis because they combine code, results, and narrative. The same flexibility can also create confusion: wrong working directories, out-of-order execution, hidden state, and notebooks that cannot be reproduced. This chapter teaches novices how to launch Jupyter correctly, navigate files, use cells effectively, run shell commands safely, and adopt notebook discipline so work remains interpretable and reproducible.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Launch Jupyter Notebook or JupyterLab from the command line in the correct folder.

2.  Diagnose the common “Jupyter has no files” problem (wrong working directory).

3.  Explain kernels, sessions, and the difference between Notebook and JupyterLab.

4.  Use cell types (code/markdown/raw), move cells, and manage execution order.

5.  Use IPython magics and run shell commands inside a notebook safely.

6.  Structure a notebook for readability: headings, narrative, and controlled outputs.

7.  Make notebooks reproducible: restart-and-run-all, environment capture, and data provenance.

8.  Convert notebooks into scripts/reports when appropriate.

## Running theme: notebooks are documents *and* programs

A notebook should read like a report and execute like a program. The discipline is to ensure both.

## 15.1 Mental models: what Jupyter is doing

### Notebook vs JupyterLab

- **Jupyter Notebook** (classic) is a single-document interface.

- **JupyterLab** is a multi-document environment (files, terminals, notebooks, consoles).

- Both run on the same concepts: a server, a browser UI, and kernels.

### Server, browser, kernel

- **Server:** the process you start (the thing listening on `localhost:8888`).

- **Browser UI:** where you edit and run cells.

- **Kernel:** the language runtime executing your code (Python, R, etc.).

### State and order

- Notebooks allow executing cells out of order.

- The kernel remembers variables from prior cells.

- “It works on my notebook” often means hidden state.

## 15.2 Launching Jupyter the right way

### The rule: start from your project folder

- Open a terminal.

- **Navigate** to the folder containing your notebooks (your project root).

- Start Jupyter there.

### Launch commands (conceptual)

- `jupyter lab`

- `jupyter notebook`

- Common pattern: pass a directory path if you are not already in it.

### Verifying you launched in the correct directory

- In the terminal: confirm the current directory before launching.

- In the UI: confirm the file browser shows your expected folder tree.

- Create a small marker file (e.g., `PROJECT_ROOT.txt`) so you can tell when you are in the right place.

### Launching from an environment (important for students)

- Ensure you started the correct environment (conda/venv) before launching Jupyter.

- Know how to confirm which Python/kernel is in use (kernel name, version cell).

## 15.3 The common failure: “Jupyter shows no notebooks”

### Symptom

- The Jupyter file browser is empty or shows a different folder than expected.

- Your notebook cannot find `data/` even though it exists.

### Root cause: wrong working directory / wrong server

- You launched Jupyter from a different folder.

- You have multiple Jupyter servers running and you opened the wrong tab.

- You launched from the wrong environment, so kernels and paths differ.

### Fix checklist

1.  Stop Jupyter (Ctrl+C in the terminal) and close the browser tab.

2.  In the terminal: **navigate** to the correct folder.

3.  Relaunch Jupyter.

4.  If still wrong: check for other running Jupyter servers and shut them down.

5.  Add a first cell in notebooks that prints the working directory.

## 15.4 Notebook mechanics: cells and execution

### Cell types

Code  
Executes in the kernel.

Markdown  
Narrative text, headings, equations, images.

Raw  
Passed through without formatting (rare; use intentionally).

### Running cells

- Run one cell vs run all.

- Interrupt vs restart kernel.

- Understand the execution count as evidence of order.

### Moving and organizing cells

- Move cells to keep the story and the computation aligned.

- Use headings to create a navigable outline.

- Keep imports and configuration near the top.

### Output management

- Avoid printing entire datasets.

- Prefer summaries (shape, head, descriptive stats).

- Clear and re-run outputs as part of reproducibility checks.

## 15.5 Running shell commands inside notebooks (responsibly)

### Why this is useful

- Quick checks: list files, inspect paths, verify data presence.

- Lightweight automation: download a file, decompress, run a command-line tool.

### Two mechanisms: “bang” and magics

### Common magics for students

### Safety rules for shell commands in notebooks

- Treat shell commands as potentially destructive.

- Avoid `sudo` from notebooks.

- Never embed secrets (tokens, passwords) in notebook cells.

- Record what the command does and why (markdown cell above).

- Prefer reproducible commands over manual clicking.

## 15.6 Notebook style and discipline (how to write a notebook that survives)

### Structure: a notebook template

- Title + one-paragraph purpose.

- Setup: imports, configuration, paths.

- Data acquisition and provenance.

- Cleaning and validation checks.

- Analysis/modeling.

- Results and interpretation.

- Next steps / limitations.

### Narrative: make the notebook readable

- Use markdown headings and short explanatory paragraphs.

- Explain assumptions and decisions (why this filter? why this join?).

- Use captions on plots and tables.

### Reproducibility discipline

- Use a consistent top-to-bottom execution order.

- Periodically: **Restart kernel and Run All**.

- Avoid hidden dependencies on prior interactive state.

- Prefer functions over repeated copy/paste code.

- Prefer relative paths inside a project.

### Environment capture (student level)

- Record: Python version, key package versions, and OS.

- Store environment files (e.g., `environment.yml`) when using conda.

- Keep datasets and generated artifacts in well-labeled folders.

### Outputs and size control

- Large outputs make notebooks slow and hard to version.

- Avoid embedding huge binary blobs.

- Prefer saving outputs to files (`data/processed`, `figures/`).

## 15.7 Notebook pitfalls and how to prevent them

### Out-of-order execution

- Prevention: restart-and-run-all checks.

- Signal: execution counts jump around; variables appear “from nowhere.”

### Wrong kernel / wrong environment

- Symptom: imports fail or versions differ from expectations.

- Prevention: name kernels clearly; confirm versions in a top cell.

### File not found (paths)

- Symptom: `FileNotFoundError` despite file existing.

- Prevention: print working directory; use project-relative paths.

### Long-running or stuck cells

- Learn: interrupt vs restart.

- Add progress indicators or timing.

- Move expensive work to scripts or batch runs when appropriate.

## 15.8 When to move from notebooks to scripts (and back)

[sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks) covers the scripting workflow in full; this section explains how notebooks and scripts fit together.

### Notebook strengths

- Exploration, explanation, and sharing results.

### Script strengths

- Production runs, automation, CI testing, and parameterized workflows.

### A practical boundary for students

- Keep exploration in notebooks.

- Extract stable logic into `src/` as functions.

- Keep the notebook as a narrative driver calling those functions.

## 15.9 Worked examples (outline)

### Example 1: Launch Jupyter in the right place

- Navigate to a project folder.

- Start JupyterLab.

- Create a notebook and verify the working directory.

### Example 2: Debug “no files” / wrong directory

- Demonstrate launching from the wrong folder.

- Diagnose and fix by relaunching from the correct path.

- Add a working-directory check cell.

### Example 3: Shell commands for file checks

### Example 4: Make a notebook reproducible

- Add headings and narrative.

- Extract repeated code into functions.

- Restart kernel and run all; fix hidden-state bugs.

## 15.10 Templates

### Template A: Notebook header block

    Title:
    Author:
    Date:
    Purpose:
    Data sources:
    Environment:

    * Python:
    * Key packages:
      How to run:
    * Restart kernel and Run All
      Outputs:
    * Where figures/tables are saved

### Template B: Reproducibility checklist cell

    # Reproducibility check

    # 1) print working directory

    # 2) print python and package versions

    # 3) confirm data files exist

    # 4) run a small smoke test

## 15.11 Exercises

## 15.12 One-page checklist

- I launch Jupyter from the correct project folder (or pass the correct directory).

- I can diagnose “no files” as a working-directory/server mix-up.

- I understand kernels and can choose the correct one.

- I use markdown headings to structure the notebook.

- I keep a top-to-bottom execution order and periodically restart-and-run-all.

- I use shell commands and magics sparingly, with explanations and no secrets.

- I record environment details and keep data provenance explicit.

- I keep outputs controlled and store large artifacts outside the notebook.

## 15.13 Quick reference: common launch and debugging moves

- Confirm working directory before launching.

- If you see the wrong files: stop server, relaunch in correct directory.

- If imports fail: check kernel/environment.

- If execution hangs: interrupt; then restart if needed.

## 15.14 Quick reference: IPython conveniences
