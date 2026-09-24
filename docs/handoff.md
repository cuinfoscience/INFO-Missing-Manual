# Hand-off note

**Updated 2026-09-24,** after #37 merged and the maintainer settled the screenshot plan's open decisions. This note describes the present state. Rewrite it when a session stops or the state changes, and don't let it grow into a history: history lives in git, in [`decisions.md`](decisions.md), and in the AARs.

## Where things stand

- **The book** has 39 chapters and appendices in seven parts, and renders with zero warnings.
- **Merged 2026-09-24:** #35 (`AGENTS.md`, `docs/`, `tools/` with the screenshot toolkit, `CONTRIBUTING.md`), #36 (cloud storage in chapters 9 and 10; closed #34), and #37 (the chapter meme above the table of contents, closing #30; the screenshot pilot, three JupyterLab figures). The deploy after #37 passed, and the live site shows both changes.
- **Decided after #37** ([`decisions.md`](decisions.md), "The screenshot plan's open decisions, settled"): captures send a contact address; wider columns are allowed sparingly; the Actions figure is the signed-out summary; VS Code is captured in the browser (code-server); terminal figures are captioned "Illustration:"; the eight orphaned images stay; one pull request per chapter; CI checks the issue forms.
- **Open pull request from `claude/markdown-chapter-expansion-difpcc`:** screenshot milestone M2 begins with `version-control`. It adds the repository-page figure, and puts those decisions into effect: the User-Agent, the CI check, and the captions.

## Waiting on the maintainer

| Item | What to do |
|---|---|
| A review comment for the diff figure | Leave a real line comment on a merged pull request in this repository (for example, #37's *Files changed*). The `version-control` diff figure shows it; replied to and resolved, it can later serve `collaboration`. Until then, that placeholder stays. |
| The open pull request | Review and merge (agents don't merge unless asked). |
| Chapter 10's trailing sections | Fold "downloaded from Canvas" and "unzip" into the body (a review follow-up in [`roadmap.md`](roadmap.md)). |
| Community files | A `CODE_OF_CONDUCT.md` (for example, the Contributor Covenant). |

## Known issues

- **Eight `PLACEHOLDER-*` images** don't exist, in seven chapters (`operating-system` 2, and one each in `version-control`, `automation`, `collaboration`, `http-apis`, `linting`, `text-editors`), so those figures render broken.
- **Wide figures hide the table of contents** while on screen (the JupyterLab overview is the one so far); accepted, per the decision above.
- **`tools/shots/run doctor <chapter>`** warns for a fixture chapter (`localhost: not reachable now`) and, in a cloud session, for GitHub (`robots.txt answered 403`, which is the session's proxy, not GitHub). "Patterns and pitfalls" in `tools/shots/README.md` says how to check each instead.
- **Old `/parts/...` chapter URLs 404,** by design ([`decisions.md`](decisions.md), 2026-08-28).
- **Quarto 1.9 can't build the book locally:** 1.9.15 rejects `website: llms-txt`. The docs say 1.10 or later.

## Notes for cloud sessions

- **Quarto** isn't installed system-wide. Download a 1.10 release into the session's scratch directory. With 1.9.x, comment out the `website:` block to render, and restore `_quarto.yml` exactly afterwards.
- **`tools/shots`:** `bash tools/shots/bootstrap.sh --headed --tex` works in the container; then `tools/shots/run doctor`. Never run `playwright install`, and never turn off TLS verification. `tools/layout-audit/` runs on the toolkit's Python.
- **JupyterLab:** use the fixture, `bash tools/shots/fixtures/jupyter/start.sh`, and stop it with `stop.sh`.
- **Chrome and long paths:** don't point `TMPDIR` at the long scratch path; Chrome's `SingletonSocket` path overflows.
- **`pkill -f <pattern>`** also matches the shell running it; use `pgrep -f '[j]upyter'` and kill each PID.
- **Merged branches can't be deleted** from a cloud session. This session reuses one branch, fast-forwarded to `main` after each merge.

## Next, when work resumes

1. The `version-control` diff figure, once the review comment exists: a recipe for the pull request's *Files changed* view, scrolled to the thread.
2. The rest of M2, one pull request each: `http-apis` (Chrome's JSON view of the chapter's GitHub API example, moved out of the margin) and `automation` (the signed-out Actions run summary).
3. M3, `collaboration`, from the same review thread once it has a reply and is resolved.
4. M4, the editors: a code-server fixture (pinned, local, like JupyterLab), then `text-editors` and `linting`.
5. Teach `doctor` to check a fixture chapter's local server; a CI check for screenshots (plan M6).
6. Re-check the "At CU Boulder" callouts in chapters 9 and 10 against OIT's pages each fall.
