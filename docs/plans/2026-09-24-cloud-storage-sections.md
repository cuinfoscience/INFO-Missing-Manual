# Plan: cloud storage, sync, and your disk (#34)

**Status:** proposed, 2026-09-24. Addresses [#34](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/34) with new sections in chapter 9 (Operating System, `chapters/operating-system.qmd`) and chapter 10 (Local File System, `chapters/file-system.qmd`), not a new chapter.

## 1. What the issue asks

The report, from a student: starting out with Python, they never realized how much space the files, instructions, and applications for their classes would take on their computer. They ask for a guide to getting set up, and for the free services the university offers students, which many don't know about. A comment adds: a short setup section for Python and Jupyter users that shows how to check how much space each download uses, which tools the school provides, and a checklist of the software students actually need, so they stop installing programs they don't need and have one place to troubleshoot setup.

The maintainer asked for sections in chapters 9 and/or 10 on remote and cloud file systems, access, and sync.

## 2. What the book already says

- **Chapter 9** has "Check storage health early and often" (disk space, the 15–20% free rule), "Understand local vs synced storage" (files-on-demand, "Always keep on this device"), and "Storage cleanup (do no harm)" (built-in cleanup tools, disk visualizers, never delete what you don't recognize).
- **Chapter 10** covers OneDrive sync inside "Access and navigation on Windows", iCloud Drive optimization inside "Access and navigation on macOS", and "confusing cloud sync with local storage" as its second pitfall.
- The same advice ("mark the folder Always keep on this device") appears **four times** across the two chapters.
- Chapter 10 ends with two sections left over from before the chapter template, after its Quick reference: "Why can't I find a file I downloaded from Canvas?" and "What does it mean to unzip a file?" (a follow-up in [`../roadmap.md`](../roadmap.md)).

Nothing yet covers how much space development tools take, what never to put in a synced folder, conflicts, sharing, network drives, or what happens to university storage when a student leaves.

## 3. Proposed changes

### Chapter 9: a new subsection, "How much space your tools take"

It goes under "Know your system: version, storage, and constraints", after "Check storage health early and often".

- **Why it surprises people.** Every course environment, dataset, and tool adds up. Give real, dated numbers, measured on the day of writing. For example, measured on Linux in September 2026: a virtual environment with JupyterLab 4.6.4 and its 97 packages takes 390 MB, so five projects with one such environment each come to about 2 GB; pip's download cache had reached 154 MB after a single day's installs in a fresh machine.
- **Where the space goes:** Python distributions (a full Anaconda install against Miniforge or python.org), conda's package cache, pip's cache, one virtual environment per project, editor extensions, container images, and datasets. Sizes are measured at writing time, not quoted from memory.
- **How to measure it:** the built-in storage views the chapter already shows, then the terminal: `du -sh <folder>`, `df -h`, `pip cache info`, and `conda clean --all --dry-run`, with the Windows equivalents. Cross-reference @sec-terminal.
- **How to reclaim it safely:** `pip cache purge`, `conda clean --all`, deleting an old project's environment after `pip freeze > requirements.txt` (it can be rebuilt, @sec-virtual-environments), and leaving everything else to "Storage cleanup (do no harm)".
- **What you actually need** (the comment's checklist): one Python distribution, not three (@sec-pkg-mgmt); one editor (@sec-text-editors); Git (@sec-git-github); JupyterLab inside a project environment (@sec-jupyter); and whatever a specific course asks for, installed when it asks. Short, with links, not a new install guide.
- **Trim "Understand local vs synced storage"** to two sentences and a pointer to the new chapter 10 section, removing one of the four repetitions.

### Chapter 10: a new section, "Files in the cloud: sync, access, and sharing"

It goes after "File operations and safety" and before "Common student pitfalls".

- **Sync, backup, and share are different things.** A small table: sync mirrors your deletions (so it isn't a backup), a backup keeps history (@sec-os-management's backup section), and sharing gives someone else access.
- **Online-only files.** The one full explanation of placeholders (OneDrive Files On-Demand, iCloud's Optimize Mac Storage, Google Drive's streaming mode), how to tell a placeholder from a real file (status icons, Get Info, the size check), and how to keep a folder local. The navigation sections and the pitfall keep one sentence each and point here.
- **Conflicts.** What a "conflicted copy" is, why editing the same file on two machines creates one, and how to resolve it.
- **What never to put in a synced folder:** virtual environments, `node_modules`, a Git repository's working copy (let Git's own remote do the syncing; @sec-git-github), caches, and large data that changes often. Why: thousands of small files, partial syncs, and conflicted copies inside tools that expect a consistent folder.
- **When your Documents folder is really in OneDrive** ("Known Folder Move"): why paths look like `C:\Users\you\OneDrive - <institution>\Documents`, and why a space in that name breaks unquoted paths in the terminal (@sec-terminal).
- **Mounted, synced, or web-only.** Network drives (`\\server\share`, `smb://`), synced folders, and files you only reach in a browser; how each behaves offline and how fast code can read from it. For data on a server, point to @sec-remote-computing (`scp`, `rsync`, JupyterHub-style services that keep files on the server).
- **Sharing links and permissions:** "anyone with the link" against "people in your organization" against named people, and why data about people should never go out on an anyone-link. This ties into the chapter's Stakes and politics section.
- **University accounts don't last forever.** Storage quotas, and what happens to your files when you graduate or leave: move what you want to keep before then.

### A dated callout for CU Boulder students (if the maintainer wants one)

A short `callout-note`, headed with the month it was checked, linking the university's own pages for: the cloud storage that comes with a student account and its quota, the software available to students at no cost, and university-run computing for coursework and research (JupyterHub-style services). **Every detail is checked against the Office of Information Technology's current pages at writing time, with links, and nothing is written from memory.** The callout is the only institution-specific part; the rest of both sections stays general.

### Alongside

- **Learning objectives, exercises, checklists:** one objective, one exercise, and one or two checklist lines per chapter, for example "Find the three biggest folders your coursework created, and decide which can be rebuilt."
- **Glossary:** sync client, online-only file (placeholder), and network drive, with anchors, per `AGENTS.md`.
- **Screenshots:** the sync-status icons are operating-system screens, so they are hand captures (route E in [`2026-09-24-screenshots.md`](2026-09-24-screenshots.md)). The sections work without them.
- **Optional:** fold chapter 10's two trailing sections into the body while the chapter is open: "downloaded from Canvas" into "Organizing work", "unzip" into "File operations and safety".

## 4. Decisions needed from the maintainer

1. **Sections, not a new chapter?** The report proposed a new topic; sections in chapters 9 and 10 fit the book's scope rule and avoid renumbering everything after them. Recommended: sections.
2. **The CU callout:** include it (dated, sourced from OIT pages) or keep the book institution-neutral with a prompt to check your own university's IT pages?
3. **Consolidate the four repetitions** of the files-on-demand advice into the new chapter 10 section?
4. **Fold the two trailing sections of chapter 10** in the same pull request, or separately?

## 5. Sources to use at writing time

Official documentation, cited in each chapter's Further reading where useful: Microsoft's OneDrive Files On-Demand and Known Folder Move pages; Apple's iCloud Drive and Optimize Mac Storage support pages; Google Drive for desktop's streaming and mirroring pages; pip's `pip cache` and conda's `conda clean` documentation; and the university's OIT pages for the callout.

## 6. Done when

- Both chapters have the new sections in the canonical style, with dated numbers measured at writing time and no institution-specific claim without a link.
- The files-on-demand advice is explained once, and referred to elsewhere.
- `quarto render --to html` has zero warnings, and every new `@sec-` reference resolves.
- The issue forms' chapter list is unchanged (no chapter was added), and `tools/issue-forms/sync_issue_chapters.py --check` passes.
