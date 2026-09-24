# Images for jupyter

Figures in `chapters/jupyter.qmd`. `tools/shots` writes the table below from `provenance.json`
and rewrites only what is between the two markers. Notes below the table are
for people: what a figure shows that is easy to miss, and what a retake needs.

<!-- shots:begin: generated from provenance.json by tools/shots; edits between these markers are replaced -->
| File | Kind | Captured | Source | How |
|---|---|---|---|---|
| `jupyter-cell-types.png` | capture | 2026-09-24 | http://localhost:8899/lab/tree/notebooks/explore.ipynb?reset | tools/shots: Google Chrome for Testing 154.0.8037.57, 800×900 at 2× |
| `jupyterlab-overview.png` | capture | 2026-09-24 | http://localhost:8899/lab/tree/notebooks/explore.ipynb?reset | tools/shots: Google Chrome for Testing 154.0.8037.57, 1024×768 at 2× |
<!-- shots:end -->

## Notes

Both figures come from the local JupyterLab fixture, [`tools/shots/fixtures/jupyter/`](../../tools/shots/fixtures/jupyter/): pinned JupyterLab 4.6.4, made-up data, nobody's own machine.

- **To retake,** start the fixture fresh (`bash tools/shots/fixtures/jupyter/start.sh`), capture `jupyter` before `pandas-basics`, review with `sheet`, promote, and stop the fixture. A fresh start matters: kernels from earlier captures keep running, and the overview's status bar counts them.
- **In the overview,** nothing is selected in the file browser (the recipe clears the selection JupyterLab makes whenever it changes folder), the status bar shows one kernel, and `README.md` is listed because the chapter's text names it. It is a relaxed figure, 1024×768, in `.column-page-inset-right`; in the body column its text would fail the legibility check.
- **In the cell types figure,** the crop ends two pixels inside the Markdown cell's blank padding, so the border of the active cell below stays out of it.
