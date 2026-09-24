# Hand-off note

**Updated 2026-09-24,** at the end of the session that set up `docs/`, `tools/`, the screenshot toolkit, and `CONTRIBUTING.md`. This note describes the present state. Rewrite it when a session stops or the state changes, and don't let it grow into a history: history lives in git, in [`decisions.md`](decisions.md), and in the AARs.

## Where things stand

- **The book** has 39 chapters and appendices in seven parts, and renders with zero warnings. Recent merged work: Markdown in Common Text Formats (#27), "Opening a terminal" (#28), generated terminal figures and the `/graphics/` path fix (#29), flat `/chapters/<slug>.html` URLs (#32), and five reader issue forms (#33).
- **Open pull request from `claude/markdown-chapter-expansion-difpcc`**, not merged. Six commits:
  1. `CLAUDE.md` renamed to `AGENTS.md` (`CLAUDE.md` imports it); this `docs/` folder, with `REVIEW.md` moved to `aar/` and the backlog moved to [`roadmap.md`](roadmap.md).
  2. `scripts/` and the meme shortcode moved into `tools/`, one folder per tool with a README; the shortcode now loads through `_quarto.yml`'s `shortcodes:` key; a new `tools/layout-audit/`.
  3. `tools/shots` vendored from *Web Data Science*, unchanged.
  4. `tools/shots` adapted: `graphics/<slug>/`, the measured 678-px column, an explicit `--disable-infobars` with a bars guard, and the relaxed 1024×768 tier. Selftest 68 of 68.
  5. `CONTRIBUTING.md`, linked from the README, the issue chooser and forms, a new pull request template, and `AGENTS.md`.
  6. Three plans in [`plans/`](plans/): screenshots, #30, and #34.
- **Verification so far:** a full render (Quarto 1.9.15 with the `llms-txt` key set aside, see below) matched the previous render except for the pages whose text changed, with all 37 memes identical; the issue-form and terminal-figure checks pass; `tools/shots/run check` is clean. CI renders with Quarto 1.10.18.

## Waiting on the maintainer

| Item | What to decide |
|---|---|
| This pull request | Review and merge (agents don't merge unless asked). |
| Screenshots ([plan](plans/2026-09-24-screenshots.md) §8) | Capture identity (User-Agent); pilot chapter (`jupyter` recommended); how to capture VS Code; the source of a real review thread; the Actions run view; "Illustration" in the terminal figures' captions; deleting eight orphaned images; the merge policy; wider columns against the table of contents. |
| #30 ([plan](plans/2026-09-24-toc-below-meme.md) §4) | Option A (meme above the table of contents, via `margin-header`); a sticky or scrolling meme; its size. |
| #34 ([plan](plans/2026-09-24-cloud-storage-sections.md) §4) | Sections rather than a chapter; a dated CU callout or not; consolidating the repeated files-on-demand advice; folding chapter 10's trailing sections. |
| Community files | A `CODE_OF_CONDUCT.md` (for example, the Contributor Covenant). `CONTRIBUTING.md` has a short "Be kind" section, but no formal policy exists. |

## Known issues

- **Twelve `PLACEHOLDER-*` images** don't exist, so those figures render broken. The screenshot plan covers them.
- **The table of contents is collapsed at load on 37 of 41 pages** (#30), and with it the *Edit this page* and *Report an issue* links. `CONTRIBUTING.md` tells readers to open "On this page" until #30 is fixed.
- **Old `/parts/...` chapter URLs 404,** by design ([`decisions.md`](decisions.md), 2026-08-28).
- **Quarto 1.9 can't build the book locally:** 1.9.15 rejects `website: llms-txt` in `_quarto.yml`. The docs now say 1.10 or later. `AGENTS.md`'s note that `llms-txt` only works under `website:` in Quarto 1.9 predates this finding and hasn't been re-checked against 1.10.

## Notes for cloud sessions

- **Quarto** isn't installed system-wide. Download a 1.10 release into the session's scratch directory. With 1.9.x, comment out the `website:` block to render, and restore `_quarto.yml` exactly afterwards.
- **`tools/shots`:** `bash tools/shots/bootstrap.sh --headed --tex` works in the container (Chrome for Testing 154 comes through Selenium Manager); then `tools/shots/run doctor`. Never run `playwright install`, and never turn off TLS verification. HTTPS goes through the session's proxy.
- **Chrome and long paths:** don't point `TMPDIR` at the long scratch path; Chrome's `SingletonSocket` path overflows. VS Code needs a short `--user-data-dir` for the same reason (a 107-character limit), and an unset `NODE_OPTIONS`.
- **JupyterLab as root** needs `--allow-root`; turn news notifications off before capturing.
- **`pkill -f <pattern>`** also matches the shell running it; use `pgrep -f '[j]upyter'` and kill each PID.
- **Merged branches can't be deleted** from a cloud session (the git proxy refuses). This session reuses one branch, restarted from `main` after each merge.

## Next, when work resumes

1. Merge this pull request if the maintainer approves it.
2. Settle the decisions above, and record each in [`decisions.md`](decisions.md).
3. #30, since it also hides the *Edit* and *Report* links: implement option A, and prove it with `tools/layout-audit/audit.py toc`.
4. The screenshot pilot (`jupyter`), then one chapter per pull request.
5. #34's sections, with the university details checked against OIT's pages on the day of writing.
