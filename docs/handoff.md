# Hand-off note

**Updated 2026-09-24.** This note describes the present state. Rewrite it when a session stops or the state changes, and don't let it grow into a history: history lives in git, in [`decisions.md`](decisions.md), and in the AARs.

## Where things stand

- The book renders cleanly (`quarto render --to html`, zero warnings) with 39 chapters and appendices in seven parts.
- Recent merged work: deeper Markdown coverage (#27), "Opening a terminal" (#28), generated terminal figures and the `/graphics/` path fix (#29), flat `/chapters/<slug>.html` URLs (#32), and five reader issue forms (#33).
- **In progress on branch `claude/markdown-chapter-expansion-difpcc`:** this `docs/` folder, and the rename of `CLAUDE.md` to `AGENTS.md`.

## Known issues

- Twelve chapters reference `PLACEHOLDER-*` screenshots that don't exist, so they render as broken images.
- Old `/parts/...` chapter URLs 404 by design; see [`decisions.md`](decisions.md) (2026-08-28).
- Open issues [#30](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/30) (the table of contents collapses beside the chapter meme) and [#34](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/34) (cloud and remote storage).

## Notes for cloud sessions

- Quarto isn't installed system-wide. Download a release (1.9 or later) into the session's scratch directory.
- Don't run `playwright install`; the container already has Chromium.
- HTTPS goes through the session's proxy. Never turn off TLS verification.
