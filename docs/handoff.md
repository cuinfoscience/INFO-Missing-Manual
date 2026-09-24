# Hand-off note

**Updated 2026-09-24,** after #35 merged and the #34 sections were written. This note describes the present state. Rewrite it when a session stops or the state changes, and don't let it grow into a history: history lives in git, in [`decisions.md`](decisions.md), and in the AARs.

## Where things stand

- **The book** has 39 chapters and appendices in seven parts, and renders with zero warnings.
- **Merged 2026-09-24:** #35, which added `AGENTS.md` and this `docs/` folder, moved supporting code into `tools/` (with the screenshot toolkit and the layout audit), added `CONTRIBUTING.md`, and added the plans for screenshots, #30, and #34. The build and the GitHub Pages deploy after the merge both passed.
- **Open pull request from `claude/markdown-chapter-expansion-difpcc`,** closing #34: a chapter 9 subsection on how much space programming tools take (measured sizes) and a chapter 10 section on cloud storage (`@sec-filesystem-cloud`), each with a dated CU callout sourced from OIT's pages; the repeated files-on-demand advice consolidated; three glossary terms; and these records.

## Waiting on the maintainer

| Item | What to decide |
|---|---|
| The open pull request | Review and merge (agents don't merge unless asked). |
| Screenshots ([plan](plans/2026-09-24-screenshots.md) §8) | Capture identity (User-Agent); pilot chapter (`jupyter` recommended); how to capture VS Code; the source of a real review thread; the Actions run view; "Illustration" in the terminal figures' captions; deleting eight orphaned images; the merge policy; wider columns against the table of contents. |
| #30 ([plan](plans/2026-09-24-toc-below-meme.md) §4) | Option A (meme above the table of contents, via `margin-header`); a sticky or scrolling meme; its size. |
| Chapter 10's trailing sections | Fold "downloaded from Canvas" and "unzip" into the body (a review follow-up in [`roadmap.md`](roadmap.md)). |
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

1. Merge the open pull request (#34's sections) if the maintainer approves it.
2. Settle the decisions above, and record each in [`decisions.md`](decisions.md).
3. #30, since it also hides the *Edit* and *Report* links: implement option A, and prove it with `tools/layout-audit/audit.py toc`.
4. The screenshot pilot (`jupyter`), then one chapter per pull request.
5. Re-check the "At CU Boulder" callouts in chapters 9 and 10 against OIT's pages each fall; update the month in their headings.
