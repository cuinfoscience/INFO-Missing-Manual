#!/usr/bin/env python3
"""Generate the annotated terminal figures used across the handbook.

These are illustrations, not captured screenshots: the chapters need pictures
of prompt anatomy and command output that are legible at print size, carry
numbered callouts, and stay stable across macOS and Windows releases. A real
screen capture is none of those things. Each figure is drawn as a small HTML
page and rendered to PNG with headless Chromium at 2x scale, on a 4:3 card.

Usage:

    python tools/terminal-figures/generate_terminal_figures.py            # write graphics/*.png
    python tools/terminal-figures/generate_terminal_figures.py --check    # fail if PNGs differ

Chromium is located via $CHROME, then $PLAYWRIGHT_BROWSERS_PATH, then the usual
system paths; a headless-shell build is preferred (see find_chromium). Standard
library only, no pip install needed. The PNGs are committed, so CI never runs
this script — it is an authoring tool, like tools/chapter-meme/generate_chapter_meme.py.

To add a figure: append an entry to FIGURES and run the script. Annotation
offsets are character positions into the unescaped line text; `where` places the
callout above the line (only sensible on the first line, which has padding above
it) or below it (only sensible on the last line, which has empty screen below).
"""

from __future__ import annotations

import argparse
import html
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GRAPHICS_DIR = REPO_ROOT / "graphics"

SCALE = 2
CARD_WIDTH = 1100
CARD_HEIGHT = 825  # 4:3 with CARD_WIDTH

# DejaVu Sans Mono advances 0.60205 em per character, so a monospace column maps
# cleanly onto pixels and callouts can be placed by character offset.
CHAR_ADVANCE = 0.60205

# Annotation accent colors, chosen to stay legible on the dark card in both the
# light and dark book themes.
ACCENTS = ["#7dd3fc", "#a5b4fc", "#86efac", "#fcd34d", "#f0abfc"]

SCREEN_PAD_LEFT = 20
SCREEN_PAD_TOP = 56  # room above the first line for a callout row
BADGE = 26

CSS = """
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  width: %(width)spx;
  height: %(height)spx;
  background: #16181d;
  font-family: "DejaVu Sans", sans-serif;
  -webkit-font-smoothing: antialiased;
}

.card {
  display: flex;
  flex-direction: column;
  height: 100%%;
  padding: 26px 30px 22px;
}

.window {
  display: flex;
  flex: 1;
  flex-direction: column;
  min-height: 0;
  background: #1e2127;
  border: 1px solid #333842;
  border-radius: 10px;
  overflow: hidden;
}

/* --- title bars ------------------------------------------------------- */

.titlebar {
  display: flex;
  flex: none;
  align-items: center;
  gap: 9px;
  height: 40px;
  padding: 0 13px;
  background: #2b2f36;
  border-bottom: 1px solid #333842;
  font-size: 17px;
  color: #9aa4b2;
}

.dot { width: 13px; height: 13px; border-radius: 50%%; }
.dot.r { background: #ff5f57; }
.dot.y { background: #febc2e; }
.dot.g { background: #28c840; }
.titlebar .title { flex: 1; text-align: center; padding-right: 56px; }

.tabbar {
  display: flex;
  flex: none;
  align-items: stretch;
  height: 44px;
  background: #2b2f36;
  border-bottom: 1px solid #333842;
  font-size: 17px;
  color: #9aa4b2;
}

.tab {
  display: flex;
  align-items: center;
  padding: 0 20px;
  border-right: 1px solid #333842;
}

.tab.active { background: #1e2127; color: #e6e6e6; }
.tabbtn { display: flex; align-items: center; padding: 0 16px; font-size: 19px; }
.tabbtn.caret { position: relative; color: #e6e6e6; }

/* --- screen ----------------------------------------------------------- */

.screen {
  position: relative;
  flex: 1;
  min-height: 0;
  padding: %(screen_top)spx %(pad_left)spx 18px;
  font-family: "DejaVu Sans Mono", monospace;
  font-size: %(font_size)spx;
  color: #e6e6e6;
}

.line {
  height: %(line_height)spx;
  line-height: %(line_height)spx;
  white-space: pre;
}

.line.dim { color: #9aa4b2; }
.cursor { background: #e6e6e6; color: #1e2127; }

/* --- annotations ------------------------------------------------------ */

.badge {
  position: absolute;
  width: %(badge)spx;
  height: %(badge)spx;
  margin-left: -%(badge_half)spx;
  border-radius: 50%%;
  font-family: "DejaVu Sans", sans-serif;
  font-size: 16px;
  font-weight: bold;
  line-height: %(badge)spx;
  text-align: center;
  color: #16181d;
}

.tick { position: absolute; width: 2px; margin-left: -1px; }
.bar { position: absolute; height: 3px; border-radius: 2px; }

/* --- legend ----------------------------------------------------------- */

.legend {
  display: grid;
  flex: none;
  grid-template-columns: repeat(%(legend_cols)s, 1fr);
  gap: 13px 26px;
  margin-top: 22px;
  font-size: 19px;
  color: #cbd5e1;
}

.legend .item { display: flex; align-items: center; gap: 11px; }

.legend .n {
  flex: none;
  width: 25px;
  height: 25px;
  border-radius: 50%%;
  font-size: 15px;
  font-weight: bold;
  line-height: 25px;
  text-align: center;
  color: #16181d;
}
"""


def render_lines(lines, line_height):
    out = []
    for line in lines:
        classes = "line dim" if line.get("dim") else "line"
        text = html.escape(line.get("text", ""))
        if line.get("cursor"):
            text += '<span class="cursor"> </span>'
        out.append(f'<div class="{classes}">{text}</div>')
    return "".join(out)


def render_annotations(annotations, font_size, line_height):
    """Place badge / tick / bar overlays for callouts on the terminal screen."""
    char_w = font_size * CHAR_ADVANCE
    parts = []
    for ann in annotations:
        color = ACCENTS[ann["n"] - 1]
        left = SCREEN_PAD_LEFT + ann["start"] * char_w
        width = ann["len"] * char_w
        center = left + width / 2
        line_top = SCREEN_PAD_TOP + ann["line"] * line_height

        if ann.get("where", "above") == "above":
            bar_y = line_top - 10
            tick_y, tick_h = bar_y - 14, 14
            badge_y = bar_y - 14 - BADGE
        else:
            bar_y = line_top + line_height + 7
            tick_y, tick_h = bar_y + 3, 14
            badge_y = bar_y + 17

        parts.append(
            f'<div class="bar" style="left:{left:.1f}px;top:{bar_y:.1f}px;'
            f'width:{width:.1f}px;background:{color}"></div>'
        )
        parts.append(
            f'<div class="tick" style="left:{center:.1f}px;top:{tick_y:.1f}px;'
            f'height:{tick_h}px;background:{color}"></div>'
        )
        parts.append(
            f'<div class="badge" style="left:{center:.1f}px;top:{badge_y:.1f}px;'
            f'background:{color}">{ann["n"]}</div>'
        )
    return "".join(parts)


def render_legend(entries):
    items = []
    for entry in entries:
        color = ACCENTS[entry["n"] - 1]
        items.append(
            f'<div class="item"><span class="n" style="background:{color}">'
            f'{entry["n"]}</span><span>{html.escape(entry["label"])}</span></div>'
        )
    return "".join(items)


def render_chrome(spec):
    if spec["chrome"] == "windows":
        tabs = "".join(
            f'<span class="tab{" active" if i == 0 else ""}">{html.escape(t)}</span>'
            for i, t in enumerate(spec["tabs"])
        )
        marker = ""
        if spec.get("tab_badge"):
            n = spec["tab_badge"]
            color = ACCENTS[n - 1]
            # The badge sits to the right of the caret, in the empty stretch of
            # tab bar: directly below it would collide with the prompt callouts.
            marker = (
                f'<span style="position:absolute;left:100%;top:50%;width:15px;'
                f'height:2px;margin-top:-1px;background:{color}"></span>'
                f'<span style="position:absolute;left:100%;top:50%;margin-left:15px;'
                f"margin-top:-{BADGE // 2}px;width:{BADGE}px;height:{BADGE}px;"
                f"border-radius:50%;background:{color};color:#16181d;"
                f"font-family:'DejaVu Sans',sans-serif;font-size:16px;"
                f"font-weight:bold;line-height:{BADGE}px;text-align:center;"
                f'z-index:2">{n}</span>'
            )
        return (
            f'<div class="tabbar">{tabs}<span class="tabbtn">+</span>'
            f'<span class="tabbtn caret">&#8964;{marker}</span></div>'
        )
    return (
        '<div class="titlebar">'
        '<span class="dot r"></span><span class="dot y"></span>'
        '<span class="dot g"></span>'
        f'<span class="title">{html.escape(spec["title"])}</span></div>'
    )


def build_page(spec):
    font_size = spec["font_size"]
    line_height = spec["line_height"]
    css = CSS % {
        "width": CARD_WIDTH,
        "height": CARD_HEIGHT,
        "font_size": font_size,
        "line_height": line_height,
        "screen_top": SCREEN_PAD_TOP,
        "pad_left": SCREEN_PAD_LEFT,
        "legend_cols": spec["legend_cols"],
        "badge": BADGE,
        "badge_half": BADGE // 2,
    }
    legend_entries = spec["annotations"]
    if spec.get("tab_legend"):
        legend_entries = [spec["tab_legend"]] + legend_entries
    body = (
        '<div class="card"><div class="window">'
        f'{render_chrome(spec)}'
        f'<div class="screen">'
        f'{render_annotations(spec["annotations"], font_size, line_height)}'
        f'{render_lines(spec["lines"], line_height)}'
        "</div></div>"
        f'<div class="legend">{render_legend(legend_entries)}</div></div>'
    )
    return f"<!doctype html><meta charset='utf-8'><style>{css}</style>{body}"


def text(s, dim=False, cursor=False):
    return {"text": s, "dim": dim, "cursor": cursor}


# --------------------------------------------------------------------------
# Figure specifications
# --------------------------------------------------------------------------

FIGURES = {
    # Chapter 11 — prompt anatomy on macOS.
    "macos-terminal-annotated": {
        "chrome": "macos",
        "title": "you — -zsh — 80×24",
        "font_size": 26,
        "line_height": 38,
        "legend_cols": 3,
        "lines": [
            text("you@MacBook-Air Project % ls -l data/"),
            text("total 24", dim=True),
            text("-rw-r--r--  1 you  staff  8421 Apr 10 12:34 input.csv", dim=True),
            text("you@MacBook-Air Project % pwd"),
            text("/Users/you/Courses/INFO-3010/Project", dim=True),
            text("you@MacBook-Air Project % echo $?"),
            text("0", dim=True),
            text("you@MacBook-Air Project % ", cursor=True),
        ],
        # Offsets into "you@MacBook-Air Project % ls -l data/".
        "annotations": [
            {"n": 1, "line": 0, "start": 0, "len": 3, "label": "your username"},
            {
                "n": 2,
                "line": 0,
                "start": 4,
                "len": 11,
                "label": "the machine you are on",
            },
            {"n": 3, "line": 0, "start": 16, "len": 7, "label": "current directory"},
            {"n": 4, "line": 0, "start": 24, "len": 1, "label": "prompt character"},
            {
                "n": 5,
                "line": 0,
                "start": 26,
                "len": 11,
                "label": "command and its arguments",
            },
        ],
    },
    # Chapter 11 — the same anatomy in Windows Terminal, plus the shell picker.
    "windows-terminal-annotated": {
        "chrome": "windows",
        "tabs": ["PowerShell", "Ubuntu (WSL)", "Git Bash"],
        "tab_badge": 1,
        "tab_legend": {
            "n": 1,
            "label": "opens a tab for another shell (WSL, Git Bash)",
        },
        "font_size": 24,
        "line_height": 36,
        "legend_cols": 2,
        "lines": [
            text("PS C:\\Users\\you\\Project> Get-ChildItem data\\"),
            text("", dim=True),
            text("    Directory: C:\\Users\\you\\Project\\data", dim=True),
            text("", dim=True),
            text("Mode      LastWriteTime      Length Name", dim=True),
            text("----      -------------      ------ ----", dim=True),
            text("-a---     4/10/2026 12:34       8421 input.csv", dim=True),
            text("", dim=True),
            text("PS C:\\Users\\you\\Project> ", cursor=True),
        ],
        # Offsets into "PS C:\Users\you\Project> Get-ChildItem data\".
        "annotations": [
            {
                "n": 2,
                "line": 0,
                "start": 0,
                "len": 2,
                "label": "shell indicator (PowerShell)",
            },
            {"n": 3, "line": 0, "start": 3, "len": 20, "label": "current directory"},
            {"n": 4, "line": 0, "start": 23, "len": 1, "label": "prompt symbol"},
            {
                "n": 5,
                "line": 0,
                "start": 25,
                "len": 19,
                "label": "command and its arguments",
            },
        ],
    },
    # Remote computing — the prompt changing is the signal you are on the server.
    "ssh-connected": {
        "chrome": "macos",
        "title": "you — ssh — 80×24",
        "font_size": 24,
        "line_height": 36,
        "legend_cols": 2,
        "lines": [
            text("you@laptop ~ % ssh agandler@server.cs.example.edu"),
            text("agandler@server.cs.example.edu's password:", dim=True),
            text("Last login: Mon Apr 13 09:12:04 2026 from 198.51.100.24", dim=True),
            text("agandler@server ~ $ hostname"),
            text("server.cs.example.edu", dim=True),
            text("agandler@server ~ $ ", cursor=True),
        ],
        "annotations": [
            {
                "n": 1,
                "line": 0,
                "start": 0,
                "len": 10,
                "label": "local prompt: commands run on your laptop",
            },
            {
                "n": 2,
                "line": 0,
                "start": 15,
                "len": 34,
                "label": "the connection command",
            },
            {
                "n": 3,
                "line": 5,
                "where": "below",
                "start": 0,
                "len": 15,
                "label": "remote prompt: you are on the server now",
            },
        ],
    },
    # Virtual environments — the (.venv) prefix is the whole point.
    "venv-prompt": {
        "chrome": "macos",
        "title": "you — -zsh — 80×24",
        "font_size": 24,
        "line_height": 36,
        "legend_cols": 1,
        "lines": [
            text("you@laptop Project % which python3"),
            text("/usr/bin/python3", dim=True),
            text("you@laptop Project % source .venv/bin/activate"),
            text("(.venv) you@laptop Project % which python3"),
            text("/Users/you/Project/.venv/bin/python3", dim=True),
            text("(.venv) you@laptop Project % ", cursor=True),
        ],
        "annotations": [
            {
                "n": 1,
                "line": 0,
                "start": 0,
                "len": 20,
                "label": "before activating: python3 resolves to the system copy",
            },
            {
                "n": 2,
                "line": 5,
                "where": "below",
                "start": 0,
                "len": 7,
                "label": "after activating: the environment name appears in your prompt",
            },
        ],
    },
    # Package management — what a successful install actually prints.
    "pip-install-success": {
        "chrome": "macos",
        "title": "you — -zsh — 80×24",
        "font_size": 20,
        "line_height": 30,
        "legend_cols": 1,
        "lines": [
            text("(.venv) you@laptop Project % pip install pandas"),
            text("Collecting pandas", dim=True),
            text(
                "  Downloading pandas-2.2.3-cp312-cp312-macosx_11_0_arm64.whl (11.3 MB)",
                dim=True,
            ),
            text(
                "     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.3/11.3 MB 8.4 MB/s eta 0:00:00",
                dim=True,
            ),
            text("Collecting numpy>=1.26.0", dim=True),
            text(
                "  Downloading numpy-2.1.2-cp312-cp312-macosx_11_0_arm64.whl (5.4 MB)",
                dim=True,
            ),
            text("Collecting python-dateutil>=2.8.2", dim=True),
            text("Collecting pytz>=2020.1", dim=True),
            text("Collecting tzdata>=2022.7", dim=True),
            text("Collecting six>=1.5", dim=True),
            text(
                "Installing collected packages: pytz, tzdata, six, numpy, python-dateutil, pandas",
                dim=True,
            ),
            # pip prints this as one line; a terminal 80 columns wide wraps it.
            text("Successfully installed numpy-2.1.2 pandas-2.2.3 python-dateutil-2.9.0.post0"),
            text("pytz-2024.2 six-1.17.0 tzdata-2024.2"),
        ],
        "annotations": [
            {
                "n": 1,
                "line": 0,
                "start": 29,
                "len": 18,
                "label": "the one package you asked for",
            },
            {
                "n": 2,
                "line": 12,
                "where": "below",
                "start": 0,
                "len": 36,
                "label": "pip resolved and installed its dependencies too",
            },
        ],
    },
}


def find_chromium():
    """Locate a Chromium binary, preferring the headless shell.

    The headless shell maps --window-size straight onto the viewport. A full
    Chrome build reserves ~87px for browser chrome, so the bottom of the page
    silently goes unpainted while the PNG is still emitted at the full size.
    check_viewport() catches that case for whichever binary we end up with.
    """
    if os.environ.get("CHROME"):
        return os.environ["CHROME"]
    pw_root = Path(os.environ.get("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers"))
    if pw_root.is_dir():
        patterns = (
            "chromium_headless_shell-*/chrome-linux/headless_shell",
            "chromium-*/chrome-linux/chrome",
        )
        for pattern in patterns:
            for candidate in sorted(pw_root.glob(pattern)):
                return str(candidate)
    names = (
        "chromium-headless-shell",
        "headless_shell",
        "chromium",
        "chromium-browser",
        "google-chrome",
        "chrome",
    )
    for name in names:
        found = shutil.which(name)
        if found:
            return found
    sys.exit("Could not find Chromium. Install it, or set $CHROME to the binary path.")


def check_viewport(chromium):
    """Fail loudly if the browser's viewport is shorter than the window size."""
    probe = (
        "<!doctype html><meta charset='utf-8'><body><div id='o'></div>"
        "<script>document.getElementById('o').textContent = "
        "'VIEWPORT:' + window.innerHeight;</script></body>"
    )
    with tempfile.TemporaryDirectory() as tmp:
        src = Path(tmp) / "probe.html"
        src.write_text(probe, encoding="utf-8")
        result = subprocess.run(
            [
                chromium,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                f"--window-size={CARD_WIDTH},{CARD_HEIGHT}",
                "--dump-dom",
                src.as_uri(),
            ],
            check=True,
            capture_output=True,
            text=True,
        )
    marker = "VIEWPORT:"
    if marker not in result.stdout:
        return  # could not measure; fall through rather than block a render
    height = int(result.stdout.split(marker, 1)[1].split("<", 1)[0].strip())
    if height < CARD_HEIGHT:
        sys.exit(
            f"{chromium} renders a {height}px viewport for a {CARD_HEIGHT}px window, "
            f"so the bottom {CARD_HEIGHT - height}px of each figure would be blank. "
            "Point $CHROME at a headless-shell build of Chromium."
        )


def render(chromium, html_text, out_path):
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp)
        src = tmp / "figure.html"
        src.write_text(html_text, encoding="utf-8")
        shot = tmp / "figure.png"
        subprocess.run(
            [
                chromium,
                "--headless",
                "--disable-gpu",
                "--no-sandbox",
                "--hide-scrollbars",
                f"--force-device-scale-factor={SCALE}",
                f"--window-size={CARD_WIDTH},{CARD_HEIGHT}",
                f"--screenshot={shot}",
                src.as_uri(),
            ],
            check=True,
            capture_output=True,
        )
        data = shot.read_bytes()
    if out_path.exists() and out_path.read_bytes() == data:
        return False
    out_path.write_bytes(data)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit nonzero if a committed PNG is out of date",
    )
    args = parser.parse_args()

    chromium = find_chromium()
    check_viewport(chromium)
    GRAPHICS_DIR.mkdir(parents=True, exist_ok=True)

    stale = []
    for slug, spec in FIGURES.items():
        out_path = GRAPHICS_DIR / f"{slug}.png"
        changed = render(chromium, build_page(spec), out_path)
        if changed:
            stale.append(slug)
        print(f"{'wrote' if changed else 'unchanged'} {out_path.relative_to(REPO_ROOT)}")

    if args.check and stale:
        sys.exit(f"out of date: {', '.join(stale)} (re-run without --check)")


if __name__ == "__main__":
    main()
