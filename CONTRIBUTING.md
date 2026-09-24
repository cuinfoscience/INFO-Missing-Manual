# Contributing to the Missing Manual

Thank you for helping. This book is written for people who are learning the skills it covers, which makes you, a reader who is learning them, the person best placed to see what is missing or wrong. **You don't need to be an expert, know Git, or know how to fix what you found.** A clear report is a real contribution.

This page explains every way to help, from a two-minute report to a new chapter. Pick the row that fits and follow its link.

| I want to… | Do this | Time |
|---|---|---|
| Report something wrong: a failing command, a dead link, steps that don't match my computer | [Something is wrong](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=something-is-wrong.yml) | 3 min |
| Say where I got stuck, or ask a question the book doesn't answer | [I'm stuck or confused](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=im-stuck.yml) | 3 min |
| Point out a typo | [Typo or quick fix](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=typo.yml), or fix it yourself ([below](#fix-it-yourself-in-your-browser)) | 1 min |
| Suggest an improvement or a new topic | [Suggestion](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=suggestion.yml) | 5 min |
| Report something hard to use with a screen reader, keyboard, zoom, or color | [Accessibility problem](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=accessibility.yml) | 3 min |
| Fix something myself | [Fix it yourself, in your browser](#fix-it-yourself-in-your-browser) (no installs), or [on your own computer](#bigger-changes-on-your-own-computer) | 10 min and up |
| Find something to work on | [Issues labeled `good first issue`](https://github.com/cuinfoscience/INFO-Missing-Manual/issues?q=is%3Aopen+label%3A%22good+first+issue%22), [typo reports](https://github.com/cuinfoscience/INFO-Missing-Manual/issues?q=is%3Aopen+label%3Atypo), or the [roadmap](docs/roadmap.md) | varies |

You'll need a free [GitHub account](https://github.com/signup) for all of these.

## Reporting a problem

Every chapter page has a **Report an issue** link. On a wide screen it sits at the right, under the page's table of contents: if you see only an **On this page** button there, click it. On a phone it is at the bottom of the page. The link opens a menu of the five forms in the table above; each asks only for what it needs.

- **You don't need the fix.** "I got stuck at step 3" is enough.
- **Don't worry about duplicates.** A quick look at the [open issues](https://github.com/cuinfoscience/INFO-Missing-Manual/issues) helps, but a duplicate is easy to close and a missing report is lost.
- **Copy what you saw, exactly.** For an error, paste the whole message as text rather than a screenshot, so it can be searched. The book's chapter on [asking technical questions](https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/questions.html) explains why, and how to write a report someone can act on.
- **Leave out anything private:** passwords, API keys, and personal file paths you'd rather not share. Issues are public.
- **Not sure which form?** Use *I'm stuck or confused*. A report in the wrong form is still useful; it gets relabeled.

## Fix it yourself, in your browser

Small fixes such as a typo, a dead link, or a clumsy sentence can be made entirely on GitHub's website. Nothing to install, and you can't break anything: your change is a *proposal* that someone reviews before it goes live.

1. **Open the chapter** on the [book's website](https://cuinfoscience.github.io/INFO-Missing-Manual/) and click **Edit this page** (next to *Report an issue*; see above for where it is). GitHub opens the chapter's source file, `chapters/<name>.qmd`.
2. **Sign in, and accept the offer to fork.** GitHub says you need your own copy (a *fork*) to propose changes. Click the button to fork the repository; it takes a second and costs nothing.
3. **Make your change.** The file is Markdown with a few Quarto extras. Change only what you meant to; if a line looks strange (`{#sec-…}`, `@sec-…`, `:::`), leave it alone. The book's [Common Text Formats](https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/common-formats.html) chapter explains Markdown.
4. **Commit, then propose.** Click **Commit changes…**, write a short description of what you changed ("Fix typo in virtual environments chapter"), and confirm. GitHub then shows your change next to the original.
5. **Open the pull request.** Click **Create pull request**. Say what you changed and why. If your change fixes a reported issue, write `Fixes #123` (with its number) and the issue will close when your change is accepted.
6. **Wait for the check and the review.** An automatic check builds the whole book with your change; for a first-time contributor, a maintainer may need to start it. A maintainer then reads your change, and may merge it or ask a question. When it merges, the website updates within a few minutes.

That is the whole cycle that the book's chapters on [version control](https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/version-control.html) and [collaboration](https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/collaboration.html) teach, done for real.

## Bigger changes, on your own computer

For anything beyond a line or two (a new section, a rewritten example, a new figure), work on your own computer so you can see the rendered book before you propose it.

**Before you start something big,** such as a new chapter or a large rewrite, open a [Suggestion](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=suggestion.yml) first so we can agree on scope before you spend the time. The [roadmap](docs/roadmap.md) lists topics that are already wanted.

**What you need:**

- [Git](https://git-scm.com/downloads) (the [Command Line](https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/terminal.html) chapter covers opening a terminal).
- [Quarto](https://quarto.org/docs/download/) **1.10 or later.** The book's automatic check uses 1.10.18. Quarto 1.9 (tested: 1.9.15) rejects the `llms-txt` setting in `_quarto.yml` and won't build the book.
- Optional: Python 3.11 or later, only if you work on the tools in [`tools/`](tools/).

**The steps:**

```bash
# 1. Fork the repository on GitHub (the Fork button), then copy your fork to your computer
git clone https://github.com/<your-username>/INFO-Missing-Manual.git
cd INFO-Missing-Manual

# 2. Make a branch for this change, named for what it does
git switch -c clarify-venv-activation

# 3. Preview the book; it rebuilds each time you save a file
quarto preview

# 4. Before you propose the change, build it once the way the check does
quarto render --to html        # should finish with no warnings

# 5. Save your work in Git and send it to your fork
git add chapters/virtual-environments.qmd
git commit -m "Explain what activation changes in the prompt"
git push -u origin clarify-venv-activation
```

Then open your fork on GitHub, where a banner offers **Compare & pull request**. Keep each pull request to one topic: two small pull requests are easier to review than one large one.

## How the book is written

The full style guide is in [`AGENTS.md`](AGENTS.md), which is also what AI coding agents read. The short version:

- **Voice.** Talk to the reader as "you", like a friendly, experienced colleague. Be direct about steps ("Run this command") and never make the reader feel slow.
- **Chapter shape.** Every chapter follows the same outline (Purpose, Learning objectives, numbered sections, Stakes and politics, Worked examples, Exercises, a one-page checklist, Further reading), so readers can jump into any chapter. Match the chapter you're editing.
- **Links between chapters** use `@sec-…` labels, such as `@sec-debugging`. The list is in `AGENTS.md`. Don't write "Chapter" before one; Quarto adds it.
- **Figures** live in `graphics/`, are referenced with a leading slash (`/graphics/name.png`), and always have alt text (`fig-alt="…"`) describing what someone who can't see the image needs to know. Screenshots follow extra rules (real captures only, readable at the size the book shows them); see "Screenshots" in `AGENTS.md` and [`tools/shots/README.md`](tools/shots/README.md).
- **Don't rename or move chapter files.** Each file name is a web address that syllabi and course pages link to ([`docs/decisions.md`](docs/decisions.md) records why).
- **If you add, rename, or reorder a chapter,** register it in `_quarto.yml` and run `python tools/issue-forms/sync_issue_chapters.py`, so the issue forms' chapter list stays right.

## Using AI tools

You're welcome to use AI tools, as the book itself did (see its [AI disclosure](https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/appendix-ai-disclosure.html)). Two conditions: say in your pull request how you used them, and check everything they produced. You are responsible for your contribution being correct. The book's [Using AI Tools](https://cuinfoscience.github.io/INFO-Missing-Manual/chapters/ai-llm.html) chapter covers how to check AI output.

## What happens next

- **Issues** get a label from the form you used (`broken`, `gap`, `typo`, `suggestion`, or `accessibility`), which is how they get sorted. A maintainer may ask a follow-up question. An issue closed with a note ("fixed in #40", "covered in the Jupyter chapter") has been dealt with, not dismissed.
- **Pull requests** need a passing check and a maintainer's review before they merge. Review comments are about the change, not about you; if a request is unclear, ask. It is fine to push more commits to the same branch to respond.
- **The maintainer is one person** who also teaches, so replies can take a while. If a week passes without one, a polite comment on your issue or pull request is welcome.

## Be kind

Assume good intent, explain rather than correct, and remember that everyone here was a beginner at the things this book teaches. Comments that belittle people may be hidden or removed. If something in an issue or pull request makes you uncomfortable, raise it privately with the maintainer, [@brianckeegan](https://github.com/brianckeegan).

## Where things live

| Path | What it is |
|---|---|
| `chapters/` | Every chapter and appendix, one `.qmd` file each |
| `graphics/` | Images, including chapter memes and screenshots |
| `.github/ISSUE_TEMPLATE/` | The five issue forms |
| `tools/` | Helper tools (memes, figures, screenshots, the issue forms' chapter list), each with a README |
| `docs/` | Project records: decisions, the roadmap, plans, and reviews |
| [`AGENTS.md`](AGENTS.md) | The full style guide and maintenance notes, for people and AI agents |
| [`README.md`](README.md) | What the book is, and how to build it |

## License

The book is released under the [MIT License](LICENSE). By contributing, you agree that your contribution is released under the same license.

## A few words, defined

- **Repository (repo):** the project's files and their history, on GitHub.
- **Issue:** a public note about a problem or idea, with a discussion under it.
- **Fork:** your own copy of the repository, where you can make changes freely.
- **Branch:** a named line of work inside a repository, so a change can be made without disturbing the main version.
- **Commit:** a saved snapshot of changes, with a message saying what changed.
- **Pull request (PR):** a proposal to bring your changes into the main book, with a place to discuss them.
- **Check:** an automatic test that runs on every pull request; here, building the book.
- **Merge:** accepting a pull request, so its changes become part of the book.
