# terminal-figures

Draws the book's pictures of terminal sessions: a prompt, a command, its output, and numbered callouts that the caption explains. These are **illustrations, not screenshots.** Each figure is written as a small HTML page and rendered to PNG by headless Chromium at 2× scale, on a 4:3 card.

```bash
python tools/terminal-figures/generate_terminal_figures.py           # write graphics/<slug>.png
python tools/terminal-figures/generate_terminal_figures.py --check   # exit 1 if a committed PNG is stale
```

Standard library only. The PNGs are committed and CI never runs this script.

## Figures

| Figure | Used in |
|---|---|
| `macos-terminal-annotated` | Command Line (`chapters/terminal.qmd`) |
| `windows-terminal-annotated` | Command Line (`chapters/terminal.qmd`) |
| `ssh-connected` | Remote Computing (`chapters/remote.qmd`) |
| `venv-prompt` | Virtual Environments (`chapters/virtual-environments.qmd`) |
| `pip-install-success` | Package Management (`chapters/package-management.qmd`) |

Each is an entry in the script's `FIGURES` dict: the window chrome to draw (macOS or Windows Terminal), the lines on screen, and callouts positioned by character offset into a line. To add or change a figure, edit `FIGURES` and re-run the script, then check the PNG by eye at the size the book shows it.

## Constraints

- **Use a headless-shell build of Chromium.** A full Chrome build reserves about 87 px of the window for browser chrome, so the bottom of every figure comes out blank while the PNG is still written at full size. `check_viewport()` fails loudly instead of letting that ship. The script looks for Chromium in `$CHROME`, then under `$PLAYWRIGHT_BROWSERS_PATH`, then in the usual system paths, preferring a headless shell; set `$CHROME` if it picks the wrong binary.
- **Callout offsets are character positions,** which works only because the figures use DejaVu Sans Mono. Changing the font family means re-deriving `CHAR_ADVANCE`.
- **Put figures in the body column, not the margin.** Callouts are illegible at margin width.

## Why not record a real terminal?

Recorders such as [terminalizer](https://github.com/faressoft/terminalizer) and [asciinema](https://asciinema.org) emit animated GIF or SVG, which the PDF build can't embed; they can't draw the numbered callouts that carry the teaching; and a recording can't show a Windows Terminal without a Windows machine to record on. [charmbracelet/freeze](https://github.com/charmbracelet/freeze) is the closest static alternative, worth revisiting if the book ever wants many unannotated output figures, at the cost of a Go dependency. See `docs/decisions.md` (2026-08-28).

Screenshots of graphical programs (VS Code, JupyterLab, GitHub) are a different matter: a hand-built look-alike of a real interface is not a record of it. Those are captured with [`../shots/`](../shots/).
