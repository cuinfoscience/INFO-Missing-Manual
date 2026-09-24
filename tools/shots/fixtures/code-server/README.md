# code-server fixture

VS Code in the browser ([code-server](https://github.com/coder/code-server)), pinned, serving a small made-up project on this machine only. The editor screenshots in `text-editors` and `linting` capture from it (`tools/shots/recipes/text-editors.yml`, `linting.yml`). The maintainer chose the browser version over the desktop app (`docs/decisions.md`); captions say so.

```bash
bash tools/shots/fixtures/code-server/start.sh     # download (first time), set up, start on :8898
tools/shots/run capture text-editors               # and linting
bash tools/shots/fixtures/code-server/stop.sh      # always stop it afterwards
```

Run `start.sh` again before each full set of captures: it stops a running server and starts from a fresh profile and a fresh copy of the project.

| File | What it is |
|---|---|
| `versions.env` | The pinned code-server release (4.138.0, VS Code 1.138.0) and extensions: Python and Ruff, from [Open VSX](https://open-vsx.org). The Python extension also installs its debugger and environments extensions, at whatever version Open VSX serves; `out/fixtures/code-server/extensions.log` records them. |
| `settings.json` | VS Code's user settings for the fixture (see below for why each is there) |
| `bashrc` | The terminal's `~/.bashrc`: the project's `.venv` active and the prompt `(.venv) Project $` |
| `requirements.txt` | pandas and numpy for the project's `.venv`, pinned |
| `project/` | The project: `analyze.py` (the Text Editors chapter's example: `pd.read_csv` on line 12), `lint_demo.py` (exactly three Ruff problems under the chapter's configuration), `pyproject.toml` (that configuration), the JupyterLab fixture's made-up `data/raw/sales.csv`, and a README |
| `start.sh`, `stop.sh` | Start and stop the server |

What `start.sh` does: downloads the release once into `tools/shots/out/fixtures/code-server/`; fetches each pinned extension's `.vsix` from Open VSX and installs the file (code-server's own `--install-extension id@version` misses Open VSX's per-platform builds, Ruff's among them); writes a fresh profile with `settings.json` and its own config file, so nothing lands in `~/.config`; copies the project with a new `.venv`; and serves it on `127.0.0.1:8898` with no password, under its own `HOME` so the terminal reads `bashrc`, not the capture machine's.

## Things that bit the first captures (September 2026)

These are in the recipes as comments too; "Patterns and pitfalls" in [`../../README.md`](../../README.md) has the general lessons.

- **The capture machine leaked into the terminal.** The default prompt showed `root@vm:` and the full path under `tools/shots/out/`, and the Python extension's Run button typed absolute paths. Hence the fixture's own `HOME` and `bashrc`, `python.terminal.activateEnvironment: false`, and a recipe that types `python analyze.py` itself (the toolkit's `type` step, headless since this capture).
- **Terminal text is drawn on a canvas,** so a text wait never sees it. `terminal.integrated.gpuAcceleration: off` renders it as page text.
- **A warning sign on the terminal's tab** meant extensions changed the terminal's environment after it opened. The recipe waits for the Python extension to finish starting (interpreter shown, "Initializing" gone) before opening the terminal.
- **"Initializing virtual environments" came back and stayed** in the status bar: the Python environments extension kept rescanning. `python.useEnvironmentsExtension: false` stops it; the `.venv` is activated by `bashrc` anyway.
- **Squiggles take no pointer events,** so a `hover` step on one times out and scrolls the editor. The Ruff recipe moves the cursor there (Ctrl+G, `4:8`) and opens the hover from the keyboard (Ctrl+K Ctrl+I).
- **The hover filled half the editor** with the language server's documentation for `os`. `python.languageServer: None` leaves Ruff's diagnostic alone.
- **"A git repository was found in the parent folders":** the scratch project sits inside this book's repository. `git.openRepositoryInParentFolders: never`.
- The empty right-hand panel (the secondary side bar) is hidden with `workbench.secondarySideBar.defaultVisibility: hidden`; the welcome page, tips, telemetry, update checks, and AI panels are off.

The data is synthetic, and the code is written for the book; don't replace either with anyone's real work.
