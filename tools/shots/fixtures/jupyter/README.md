# JupyterLab fixture

The JupyterLab that the book's Jupyter screenshots show: a pinned version, serving a small made-up project on this machine only. The recipes in `tools/shots/recipes/jupyter.yml` and `pandas-basics.yml` capture from it.

```bash
bash tools/shots/fixtures/jupyter/start.sh     # install (first time), copy the project, start on :8899
tools/shots/run capture jupyter                # first: its overview shows the kernel count
tools/shots/run capture pandas-basics
bash tools/shots/fixtures/jupyter/stop.sh      # always stop it afterwards
```

Run `start.sh` again before each full set of captures. It stops a running server first and starts from a fresh copy of the project, which clears what earlier captures left behind (see below).

| File | What it is |
|---|---|
| `requirements.txt` | JupyterLab 4.6.4, ipykernel, nbconvert, pandas 3.0.6, and numpy, pinned so a retake shows the same interface and the same output |
| `overrides.json` | JupyterLab settings: the light theme, and no news or update prompts (a news toast appeared over the page in the first trial) |
| `project/` | The project the screenshots show, laid out like the chapter's example: `data/raw/sales.csv` (84 made-up rows: two stores, three products, two weeks), `notebooks/explore.ipynb`, `notebooks/dataframe.ipynb` (the pandas chapter's own DataFrame), `src/clean.py`, and a `README.md`, because the chapter says the file browser shows one |
| `start.sh`, `stop.sh` | Start and stop the server |

What `start.sh` does, and why:

1. **Installs the pinned packages** into `.venv` beside this file (ignored by git) and copies `overrides.json` into JupyterLab's settings directory there.
2. **Copies `project/` to `tools/shots/out/fixtures/jupyter/Project`**, so running notebooks, checkpoints, and JupyterLab's saved layout never change the committed files. The folder is named `Project` to match the chapter's `~/Courses/INFO-3010/Project`.
3. **Runs every notebook** with `nbconvert`, so the outputs are exactly what this pandas produces, and **trusts** it, so JupyterLab renders its HTML output without warnings.
4. **Serves it** on `127.0.0.1:8899` with no token, with its own config, data, workspace, and settings directories under `out/`. It passes `--allow-root` only when run as root (as in a cloud container).

The data is synthetic: no people, no real sales. Don't replace it with real data; see "No student names or work" in `AGENTS.md`.

## Things that bit the pilot

These are in the recipes as comments too; the full list is in "Patterns and pitfalls" in [`../../README.md`](../../README.md).

- **Saved layout carries over between captures.** JupyterLab remembers the last layout (folded sidebar, open tabs) on the server. Every recipe URL ends in `?reset`, which starts from the default layout.
- **The file browser moves itself.** About a second after a notebook opens, JupyterLab moves the file browser into the notebook's folder. A click on the home icon before that is undone, so the overview recipe waits for the `notebooks` breadcrumb first.
- **The active cell draws a blue border and a toolbar,** which leak into crops. The recipes click another cell first so the active one is outside the crop.
- **The notebook scrolls inside the page,** not the page itself, so content below the fold isn't on screen to capture. Use a taller window than the crop and let the crop decide what shows.
- **Changing folder selects the first item.** After the overview goes home, JupyterLab selects and focuses `data`, a blue row. Clicks elsewhere and Escape leave it selected; the recipe waits for the selection, presses Ctrl+Space (which toggles the focused item), and waits for the selection to go.
- **Kernels outlive captures.** Each notebook a capture opens starts a kernel that keeps running on the server, and the status bar counts them: after a `pandas-basics` capture, the overview showed two. `?reset` doesn't stop kernels; a fresh `start.sh` does. Capture `jupyter` first, so its overview shows the one kernel a reader would have.
