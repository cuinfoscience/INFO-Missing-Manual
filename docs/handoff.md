# Hand-off note

**Updated 2026-09-24,** after #47 merged. This note describes the present state. Rewrite it when a session stops or the state changes, and don't let it grow into a history: history lives in git, in [`decisions.md`](decisions.md), and in the AARs.

## Where things stand

- **The book** has 39 chapters and appendices in seven parts, and renders with zero warnings.
- **Merged 2026-09-24:** #35 (`AGENTS.md`, `docs/`, `tools/`, `CONTRIBUTING.md`), #36 (cloud storage; closed #34), #37 (the meme above the table of contents, closing #30; the JupyterLab screenshot pilot), and #38 (the repository-page screenshot, the contact-address User-Agent, the issue-forms check in CI, "Illustration:" captions). Each deploy passed.
- **Order of work** ([`decisions.md`](decisions.md)): the screenshots first, then polish of the existing chapters, then new sections in the roadmap's new priority order. One pull request at a time; the maintainer merges.
- **Merged since:** #39 (the `automation` screenshot, the reordered roadmap), #40 (the maintainer's hand capture for `http-apis`), #41 (the two VS Code screenshots, from a code-server fixture), #42 (the stranded trailing sections of `file-system` and `terminal`, folded in), #43 (`package-management`'s empty stubs, `jupyter`'s empty quick reference, `presenting`'s duplicate table), #44 (the glossary terms linked on first use), #45 (three Stakes openings rewritten), #46 (interactive debuggers in `debugging`), and #47 (second-week Git in `version-control`). The polish of existing chapters is done.
- **Open pull request from `claude/markdown-chapter-expansion-difpcc`:** hosted notebooks (Colab, Kaggle, Codespaces) in `jupyter`, which also fills its empty Exercises heading.

## Waiting on the maintainer

| Item | What to do |
|---|---|
| A review comment for the diff figure | Leave a real line comment on a merged pull request in this repository (for example, #37's *Files changed*). The `version-control` diff figure shows it; replied to and resolved, it can later serve `collaboration`. The session watches #37 for it. |
| The open pull request | Review and merge (agents don't merge unless asked). |
| Community files | A `CODE_OF_CONDUCT.md` (for example, the Contributor Covenant). |

## Known issues

- **Seventeen images in `graphics/` are used by no chapter:** the eight orphans the screenshot plan listed, plus nine the `file-system` polish left behind (four outdated browser download-settings screenshots, the Finder and File Explorer icons, and three menu icons). They stay until the maintainer decides otherwise (`decisions.md`).
- **Four `PLACEHOLDER-*` images** don't exist, in three chapters (`operating-system` 2, `version-control` 1, `collaboration` 1), so those figures render broken. All four wait on the maintainer: a review thread, and two hand captures on real machines.
- **Wide figures hide the table of contents** while on screen (the JupyterLab overview is the one so far); accepted, per the decision above.
- **`tools/shots/run doctor <chapter>`** warns for a fixture chapter (`localhost: not reachable now`) and, in a cloud session, for GitHub (`robots.txt answered 403`, which is the session's proxy, not GitHub). "Patterns and pitfalls" in `tools/shots/README.md` says how to check each instead.
- **Old `/parts/...` chapter URLs 404,** by design ([`decisions.md`](decisions.md), 2026-08-28).
- **Quarto 1.9 can't build the book locally:** 1.9.15 rejects `website: llms-txt`. The docs say 1.10 or later.

## Notes for cloud sessions

- **Quarto** isn't installed system-wide. Download a 1.10 release into the session's scratch directory. With 1.9.x, comment out the `website:` block to render, and restore `_quarto.yml` exactly afterwards.
- **`tools/shots`:** `bash tools/shots/bootstrap.sh --headed --tex` works in the container; then `tools/shots/run doctor`. Never run `playwright install`, and never turn off TLS verification. `tools/layout-audit/` runs on the toolkit's Python.
- **JupyterLab:** use the fixture, `bash tools/shots/fixtures/jupyter/start.sh`, and stop it with `stop.sh`.
- **VS Code:** use the code-server fixture, `bash tools/shots/fixtures/code-server/start.sh` (it downloads code-server from GitHub releases and extensions from Open VSX, both reachable from a cloud session), and stop it with `stop.sh`. Its README lists the settings that keep a take honest.
- **Chrome and long paths:** don't point `TMPDIR` at the long scratch path; Chrome's `SingletonSocket` path overflows.
- **`pkill -f <pattern>`** also matches the shell running it; use `pgrep -f '[j]upyter'` and kill each PID.
- **Merged branches can't be deleted** from a cloud session. This session reuses one branch, fast-forwarded to `main` after each merge.

## Next, when work resumes

1. **Screenshots, when the maintainer is ready:** the `version-control` diff and `collaboration` (after the review comment on a merged pull request), and the operating-system panels (hand captures on macOS and Windows, recorded with `adopt`). M6, a CI check for screenshots, can come any time.
2. **New sections, next for agents,** in the roadmap's order, one pull request each: out-of-memory data (chunked reads, Polars, DuckDB) in `data-file-formats`, then data dictionaries and data ethics.
3. **Tooling:** teach `doctor` to check a fixture chapter's local server; a CI check for screenshots (plan M6).
4. Re-check the "At CU Boulder" callouts in chapters 9 and 10 against OIT's pages each fall, and the hosted-notebook limits in `jupyter` (Colab, Kaggle, Codespaces) against their docs.
