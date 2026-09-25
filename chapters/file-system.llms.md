# 10  Local File System

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-os-management](#sec-os-management).
>
> **See also:** [sec-terminal](#sec-terminal), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks), [sec-git-github](#sec-git-github), [sec-project-management](#sec-project-management).

## Purpose

![No Idea Dog Meme: Where Did I Save That File?](../graphics/memes/file-system.png)

It’s 11 p.m., the lab is due at midnight, and your notebook ran fine on Sunday. Since then you’ve done something responsible: you moved the lab out of `Downloads` into a tidy new `Courses` folder. Now the first cell fails with `FileNotFoundError`, and you can see the data file sitting right there in Finder. Nothing is wrong with the file, and nothing is wrong with the code. What changed is *where the code was looking from*, and nobody ever told you that was a thing.

If that has happened to you, you’re in good company. Most of the frustration beginners run into with computers isn’t about code at all. It’s losing track of files, not knowing where a download went, and breaking things by moving or renaming them.

This chapter fills that gap, on **Windows** (File Explorer) and **macOS** (Finder): how files, folders, and paths fit together; how to get around quickly; how to organize work so it scales from one assignment to a semester-long project; how to find things, copy and delete safely, and live with cloud sync; and how all of it connects to your code. It doesn’t teach the terminal itself (that’s [sec-terminal](#sec-terminal)) or operating-system settings and backups ([sec-os-management](#sec-os-management)).

## Why read this chapter

- You saved a handout from Canvas five minutes ago, and now you can’t find it anywhere on your computer.
- Your notebook worked yesterday, and today it says `No such file or directory: 'data/raw/survey.csv'` even though you can see the file right there.
- You renamed `data.csv` and it quietly became `data.csv.txt`, or `data` with no extension at all, and now nothing opens it properly.
- A path you copied, like `C:\Users\you\OneDrive - Example University\Documents`, breaks the moment you paste it into a terminal.
- Your project lives inside OneDrive or iCloud Drive, and your code hangs or fails whenever you’re offline.
- You have `final.docx`, `final-2.docx`, and `final-final-USE-THIS.docx`, and you honestly aren’t sure which one you turned in.
- You’re graduating soon and don’t know what happens to everything in your university Google Drive and OneDrive.
- Your instructor keeps saying “use relative paths” and “run it from the project root,” and you’d like to know why it matters.

## Running theme: “Location is a dependency”

Your scripts, notebooks, and apps all quietly assume that files are in particular places, so good file habits are really about making those assumptions visible and keeping them true.

## 10.1 A beginner mental model

Almost everything in this chapter rests on two words, **file** and **folder**, and on how they fit together. A file is a single named piece of stored data: a `report.docx` document, a `data.csv` table, a `cleaning.py` script. A folder (also called a [*directory*](https://en.wikipedia.org/wiki/Directory_(computing)); the two words mean the same thing) is a container that holds files and other folders. Folders inside folders form a tree, and your computer’s whole [file system](../chapters/appendix-glossary.llms.md#term-file-system) is one big tree growing out of a single root.

Every file in that tree has a [**path**](https://en.wikipedia.org/wiki/Path_(computing)), which is its address. Paths come in two flavors, and mixing them up is behind a lot of the “but it’s right there!” moments. An **absolute path** starts from the very root of the tree, so it points to the same file no matter where you are. A **relative path** starts from wherever you happen to be right now: it’s shorter, but it means something different depending on where you stand. Both kinds separate each step down the tree with a separator character, and here Windows and macOS disagree. Windows uses a backslash (`\`) and usually starts with a drive letter, like `C:\Users\you\Documents`; network locations start with `\\server\share` instead. macOS (and Linux) use a forward slash (`/`), the root is just `/`, and your home folder is `/Users/you`.

``` text
Absolute path (Windows):   C:\Users\you\Documents\project\data.csv
Absolute path (macOS):     /Users/you/Documents/project/data.csv
Relative path (either):    project/data.csv         (from inside Documents)
Relative path (either):    ../data.csv              (one folder up)
```

The `..` in that last line means “the folder above this one,” and you’ll see it constantly. One Windows quirk is worth knowing too: Windows has long [limited paths to 260 characters](https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation), and some tools still trip over longer ones. The fix is the one you’d want for readability anyway: keep project paths short, and don’t bury things ten folders deep.

The last piece of the name is the [**extension**](https://en.wikipedia.org/wiki/Filename_extension): the `.csv`, `.py`, or `.docx` after the final dot. Your operating system uses it to decide which program opens the file, so a `.csv` opens in Excel, a `.py` in your code editor, and a `.docx` in Word. When you get to choose a format, prefer plain-text ones like `.csv`, `.txt`, and `.md` over binary ones like `.xlsx`, `.docx`, and `.pdf`. Any tool can read plain text, `git diff` can show you exactly what changed in it, and you can rescue it with a text editor when something goes wrong. Binary formats do none of those things well.

## 10.2 Access and navigation on Windows

When you open File Explorer (the manila-folder icon, usually pinned to the taskbar), three parts of the window are worth learning by name. The **sidebar** down the left has shortcuts to places like Quick Access and This PC. The **main pane** shows what’s inside the folder you’ve selected. And the **address bar** across the top shows where you are as a row of clickable segments called *breadcrumbs*. Click any segment to jump straight back to that folder: deep inside `C:\Users\you\Documents\project\notebooks\drafts`, one click on `Documents` saves you five clicks of the Back button. Click the empty space at the end of the address bar and the breadcrumbs turn into the full path as text, which you can copy, or replace with a path you type and `Enter` to jump there. To copy a file’s own path for a script, right-click it and choose **Copy as path** (on Windows 10, hold `Shift` while you right-click).

A few File Explorer skills pay off quickly. **Search** can cover the current folder or the whole computer, and that difference matters: searching all of This PC for `data.csv` finds every CSV you’ve ever saved, while searching from inside your project folder finds the one you meant. **Sort and view** options (right-click in the main pane, or use the View menu) order files by name, date modified, type, or size, and sorting by date modified is the fastest answer to “what did I save yesterday?”

Two View settings deserve special mention, because newcomers usually discover them the hard way. **File name extensions** is off by default, which is how `data.csv` and `data.csv.txt` can look identical to you while being completely different files to your code. Turn it on and leave it on; Microsoft’s page on [common file name extensions](https://support.microsoft.com/en-us/windows/common-file-name-extensions-in-windows-da4a4430-8e76-89c5-59f7-1cdbbc75cb01) shows where the switch lives. **Hidden items** reveals [hidden files and folders](https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory), such as `.env` files and `.git` folders, which you’ll occasionally need while troubleshooting. Turn that one on only for the diagnosis and off again afterwards, so you don’t delete a system file by accident.

One more thing to know about Windows: if you sign in with a Microsoft or school account, your `Documents` folder may not really live on your laptop. **OneDrive** can keep it in the cloud and leave placeholders on your disk that download only when you open them. The small icons next to each file tell you which is which, and they matter for code, because a script that reads a placeholder has to wait for a download first. [sec-filesystem-cloud](#sec-filesystem-cloud) explains the icons and how to keep a folder fully on your computer.

## 10.3 Access and navigation on macOS

Finder plays the same role on a Mac. Click the smiley-face icon in the Dock and you’ll see a **sidebar** with Favorites and iCloud Drive, a **toolbar** with view buttons across the top, and the **main pane** in the middle. The four views each have a job: icon view for browsing photos, list view for sorting by date or size, gallery view for media, and column view for drilling down through folders. Column view is the Mac’s best answer to “where am I?”: each column shows the next level down, so you never lose your place in a deep hierarchy.

Here’s the part that confuses people coming from Windows: Finder hides the full path by default. Turn on **View → Show Path Bar** and it appears along the bottom of every window. To copy a file’s full path for a script, select it and press `Option + Command + C`.

Finder’s search box (top right, or `Command + F`) searches your whole Mac unless you tell it otherwise, so click the current folder’s name in the bar under the search field to limit it. You can narrow results further by kind, date, and other details, which is the easiest way to find “that report from last week” whose name you’ve forgotten. Macs also have [**tags**](https://support.apple.com/guide/mac-help/tag-files-and-folders-mchlp15236/mac), the colored dots you sometimes see beside file names. A tag works like a label: mark a file “INFO 3010” or “needs review” without moving it, then click the tag in the sidebar to see everything that has it. Tags are an underused habit that pays off on long projects.

A few folders are hidden by default: the Mac’s system folders, your `~/Library` folder, and anything whose name starts with a dot. Treat them as off-limits unless you have a reason to be there, because they hold settings for macOS and your apps, and a stray edit can break things in ways that are hard to trace. When you do need to see them (most often `~/.ssh`, for SSH keys; see [sec-remote-computing](#sec-remote-computing)), press `Command + Shift + .` in any Finder window to toggle hidden items. Look at what you came to see, then toggle them off again so you don’t drag the wrong thing to the Trash.

The Mac has its own version of OneDrive’s placeholders. With **Optimize Mac Storage** on, macOS moves iCloud Drive files you haven’t opened lately to the cloud when your disk gets full, leaving placeholders that download again when you open them. It’s the same problem with the same fix, both in [sec-filesystem-cloud](#sec-filesystem-cloud): for any folder where you run code, make sure the files are really on your Mac.

## 10.4 Organizing work: conventions that scale

The single biggest improvement most students can make is to **stop working out of `Downloads` and `Desktop`**. Make one stable home for everything school-related instead. The name doesn’t matter (`Courses`, `School`, `Coursework`); what matters is that there’s exactly one, so every assignment, lab, and project has a predictable parent. Inside it, give each course a folder, and inside each course, separate folders for assignments, labs, and the project. When you come back to the work three weeks later, you won’t have to remember where anything went, because it’s where it always is.

``` text
~/Courses/
├── INFO-3010/
│   ├── Assignments/
│   ├── Labs/
│   └── Project/
└── INFO-4040/
    ├── Assignments/
    └── Project/
```

Part of that habit is knowing where your browser puts downloads, because this is where most “vanished” files go. Depending on its settings, a handout from Canvas may land in `Downloads`, on the Desktop, or in whatever folder you saved the last file to. Every browser lets you fix this: point it at your `Downloads` folder, or tell it to ask where to save each file, and then move each download into its course folder as soon as it arrives. The official instructions for [Chrome](https://support.google.com/chrome/answer/95759), [Safari](https://support.apple.com/guide/safari/download-items-from-the-web-sfri40598/mac), [Firefox](https://support.mozilla.org/en-US/kb/where-find-and-manage-downloaded-files-firefox), and [Edge](https://support.microsoft.com/en-us/microsoft-edge/change-the-downloads-folder-location-in-microsoft-edge-4049e93b-0ef6-e44f-aca0-7d5f37a39294) stay current as the menus change. Some files never reach `Downloads` at all: a PDF may open in a browser tab, and a Word or Excel file may open straight from a temporary folder you’ll never find again. Use **Save as** (in the browser, the PDF viewer, or the Office app) to put a copy somewhere you can find it.

Data projects deserve a bit more structure, and one layout has become close to a standard. Adopt it from day one and you’ll save yourself grief. At the project root goes a `README.md` saying what the project is and how to run it. Your inputs go in `data/raw/`, and they’re **read-only**: never edit raw data in place, however tempting it is. Anything you make from them (cleaned versions, joined tables, summaries) goes in `data/processed/`. Reusable Python code lives in `src/`, exploratory notebooks in `notebooks/`, and finished figures and tables in `reports/` or `figures/`. The point of the layout is that anyone, including future you, can delete `data/processed/`, run one command, and rebuild it, and that only works if you respect the read-only rule on `data/raw/`.

``` text
project/
├── README.md
├── data/
│   ├── raw/         # immutable inputs — never overwrite
│   └── processed/   # rebuildable outputs
├── src/             # importable Python code
├── notebooks/       # exploration only, not production
└── reports/         # figures and tables for sharing
```

Good names pay you back over and over. Describe what’s in the file: `clean-survey-2026-01.csv`, not `data2.csv`. Start anything dated with the date in `YYYY-MM-DD` form (the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) order), so files sort into time order in every tool: `2026-01-15-pilot-results.csv` always lands right before `2026-01-22-pilot-results.csv`. Keep spaces and special characters out of any name your code will touch, because `survey results.csv` is an invitation to quoting bugs while `survey-results.csv` or `survey_results.csv` works everywhere. And don’t fall into the `final.docx`, `final-final.docx`, `final-final-USE-THIS.docx` trap: track versions with dates or numbers, not adjectives.

The same idea applied to data is called [provenance](https://en.wikipedia.org/wiki/Provenance), or knowing where every file came from. Keep raw files read-only. If you need a variant (a subset, a renamed column, an encoding fix), save it under a new name in `data/processed/`, and write down in your README or a changelog *what* you changed and *why*. The week you do it, this feels like overkill. Six weeks later, when you can’t reproduce your own results, it’s the difference between five minutes of checking and an afternoon of guessing.

## 10.5 Search, metadata, and “finding it later”

### Search strategies that work

Whether you’ll ever find a file again is mostly decided the moment you name it. A search for `report.docx` turns up a dozen files; `info3010-project1-cleaned-2026-02-15.csv` practically jumps out at you. So take a second at save time to pick a name you could find from memory in three weeks.

When you do search and can’t remember the name, narrow by **file type and date** instead. On Windows, File Explorer’s search box understands [Advanced Query Syntax](https://learn.microsoft.com/en-us/windows/win32/lwef/-search-2x-wds-aqsreference): `ext:.csv` finds only CSV files, and adding `modified:last week` keeps only the ones you changed recently. On a Mac, Finder understands a few keywords such as `kind:pdf`, and for everything else there’s the **+** button under the search field, which adds rules like “Kind” and “Last modified date” ([Apple’s guide](https://support.apple.com/guide/mac-help/narrow-search-results-in-finder-mh15155/mac) walks through it). Typing `.csv` and choosing the *Name contains* suggestion is a quick way to find CSVs. Either way, check your search scope first: search inside the folder you care about, not the whole drive, or you’ll wait a long time for results you didn’t want.

Folders you open every day deserve a shortcut. On a Mac, drag a folder into the Finder sidebar and it’s one click away from any window. On Windows, right-click a folder and choose **Pin to Quick access**. Once your course folders are one click away, saving to the Desktop “just for now” stops being tempting.

### Sort and view for diagnosis

When something goes wrong (a script writes an empty output, a download stalls, a notebook can’t find yesterday’s file), your first move should be to sort the folder by **date modified, newest first**. The most recently touched files rise to the top, and you can see at a glance whether the file you expected exists, whether it was written a minute ago, and whether an old copy is still hanging around confusing your code.

The second view worth knowing shows **size** and **type** as columns: Finder’s list view (`Command + 2`) or File Explorer’s Details view, with Size and Type added if they’re missing. A 0-byte `data.csv` almost always means a failed download, or a script that opened the file for writing and crashed before it wrote anything. A `dataset.csv` that’s suddenly 12 GB instead of 200 MB means something, probably a runaway loop, appended far more than it should have. Neither problem shows up in icon view; both are obvious the moment you look at the size column.

``` text
# What "sort by date modified" typically reveals
data/processed/   2026-03-14  10:42   <DIR>
  cleaned.csv     2026-03-14  10:42      5,418,220   <-- what you just wrote
  cleaned.csv~    2026-03-14  10:39         12,004   <-- editor backup, ignore
  cleaned.csv.tmp 2026-03-14  10:41              0   <-- aborted write, delete
```

## 10.6 File operations and safety

### Copy vs move vs rename

Copy, move, and rename look almost the same in a file manager, and they have very different consequences for any code that uses the file. **Copy** leaves the original where it was and makes a second, independent file, so changing one doesn’t touch the other. That makes it the safe choice for experiments: copy `dataset.csv` to `dataset-experiment.csv`, mangle the copy however you like, and if it goes wrong you throw the copy away. **Move** keeps a single file but changes where it lives. **Rename** leaves it in the same folder but changes its name, which is exactly what every script and notebook knows it by.

So copy is almost always safe, while move and rename break any code that mentions the old path. A notebook cell that says `pd.read_csv("data/raw/survey.csv")` stops working the moment you rename `survey.csv` to `survey-2026.csv`, and the `FileNotFoundError` you get next time gives no hint that the file is fine and the *code* is what went stale. Before you move or rename something your code depends on, search the project for the old name (in VS Code, [search across files](https://code.visualstudio.com/docs/editing/codebasics#_search-across-files) finds it in seconds), and update every reference in the same commit as the rename.

``` bash
# Copy: safe, makes a second independent file
cp data/raw/survey.csv data/raw/survey-backup.csv

# Move: single file, new location (may break code that references old path)
mv data/raw/survey.csv data/archive/survey-2025.csv

# Rename: single file, new name in the same folder (same risk)
mv data/raw/survey.csv data/raw/survey-2026-01.csv
```

### Delete and recover

The Trash on a Mac and the Recycle Bin on Windows aren’t deletion; they’re a holding area. A file you drag there stays on disk, taking up the same space, until you empty the bin. That’s deliberate forgiveness: realize five minutes later that you needed `important.csv`, and you can right-click it and choose **Put Back** (Mac) or **Restore** (Windows). Only emptying the bin, or a command that skips it (`Shift + Delete` on Windows, [**Delete Immediately**](https://support.apple.com/guide/mac-help/delete-files-and-folders-on-mac-mchlp1093/mac) in Finder), makes a file genuinely hard to get back. Treat “Empty Trash” as the destructive step it is, and look at what’s in there before you confirm.

Some deletions skip the bin without asking, and it’s worth knowing which ones before one surprises you. On a USB stick or a network drive, Windows usually deletes files outright, because the Recycle Bin belongs to your own disk. In the terminal, `rm` (macOS and Linux) and `del` (Windows) never use the bin: the file is gone the moment the command finishes. And every sync service, from OneDrive to iCloud to Dropbox, copies a deletion to all your devices within seconds, which is great until it isn’t. When in doubt, delete in the file manager, where you can undo, and slow down in the terminal.

``` bash
# GUI trash: reversible
# macOS:    drag to Trash, then "Put Back" if needed
# Windows:  Delete key or drag to Recycle Bin, then "Restore"

# Terminal: NOT reversible on most systems
rm data/processed/old-output.csv   # gone immediately
```

### Unzipping an archive

Course materials and datasets often arrive as a [`.zip` file](https://en.wikipedia.org/wiki/ZIP_(file_format)): one or more files bundled and compressed into a single package. Your programs can’t read what’s inside until you **extract** (unzip) it. On Windows, right-click the file in File Explorer and choose **Extract All…** ([Microsoft’s steps](https://support.microsoft.com/en-us/windows/zip-and-unzip-files-8d28fa72-f2f9-712f-67df-f80cf89fd4e5)); on a Mac, double-click it in Finder ([Apple’s steps](https://support.apple.com/guide/mac-help/zip-and-unzip-files-and-folders-on-mac-mchlp2528/mac)). Either way you get a folder with the same name next to the archive.

Here’s the snag that catches Windows users: File Explorer lets you open a zip file and browse inside it as though it were a folder, so it’s easy to think you’ve already unzipped it. You haven’t, and a notebook pointed at a path inside the zip won’t find its data. Extract first, and work from the extracted folder. Put that folder in your course or project folder (never a system folder), and never run a program from an archive you don’t trust. Once you’ve checked that everything came out, delete the `.zip`, or keep it in `data/raw/` if you need the original exactly as you received it.

``` bash
unzip lab-03.zip -d lab-03/        # macOS and Linux terminal
```

### Permissions basics (just enough)

Every file carries [permissions](https://en.wikipedia.org/wiki/File-system_permissions): a short record of who may read it, change it, and (for programs) run it. You rarely notice them, because you own everything in your home folder. They show up only when something goes wrong, usually as `Permission denied`, `Access is denied`, or `Operation not permitted`. All three are the operating system saying, “You, specifically, aren’t allowed to do that to this file.”

There are only a few likely causes. **You’re writing outside your home folder,** into `/Applications` on a Mac or `C:\Program Files` on Windows, where changes need administrator rights; move the work into your home folder and the problem disappears. **The file came from somewhere else,** such as a USB stick, a download, or a shared drive, and carries ownership settings that don’t match your account; copying it (not moving it) into your own folder usually fixes that. **On a Mac, [Gatekeeper](https://en.wikipedia.org/wiki/Gatekeeper_(macOS)) is refusing to run something you downloaded,** and the fix for that is in [sec-os-management](#sec-os-management).

The habit that prevents nearly all of this is to **do your real work inside your home folder** and treat everything outside it as read-only. `~/Courses/`, `~/Projects/`, `~/Documents/`: all fine. `/usr/local/`, `C:\Windows\`, `/System/`: leave them alone. If a tutorial tells you to [`sudo`](https://en.wikipedia.org/wiki/Sudo) something while you’re still learning, pause. There’s almost always a way that doesn’t need administrator rights, and using them casually is the fastest way to break your computer.

## 10.7 Files in the cloud: sync, access, and sharing

Much of what feels like “your computer” now lives somewhere else too, and that’s where a lot of the most baffling file problems come from. A [**sync client**](../chapters/appendix-glossary.llms.md#term-sync-client) (OneDrive, iCloud Drive, Google Drive, Dropbox) keeps a folder on your disk matched to a copy in the cloud. Your university gives you storage you reach through a browser or a network drive. A course’s JupyterHub keeps your notebooks on its own server. Each of these behaves differently when the network drops, when two computers edit the same file, and when your account ends, so it’s worth knowing which one you’re using and choosing on purpose.

### Sync, backup, and sharing are different jobs

People use these three words as if they meant the same thing, and that mix-up is how students lose work they thought was safe. **Sync** keeps the same files on every device signed in to your account. A [**backup**](https://en.wikipedia.org/wiki/Backup) keeps earlier versions in a copy that’s separate from your working files. **Sharing** gives other people access to a file or folder. Each protects you from different things:

| Job | Protects you from | Doesn’t protect you from |
|----|----|----|
| **Sync** | A lost or broken laptop, once the files have finished syncing | Your own mistakes: a deletion or a bad edit reaches every device within seconds |
| **Backup** | Deletions, overwritten files, a bad edit last week, ransomware | Anything, if you’ve never tested a restore ([sec-os-management](#sec-os-management)) |
| **Sharing** | Emailing attachments back and forth | Losing control: anyone you share with can make their own copy |

Sync services do keep some history of their own (you can usually restore an earlier version of a file, or a deleted one, for a limited time), which is better than nothing. A real backup is still a separate copy you can restore even when the sync account is the thing that broke.

### Online-only files: the name is here, the contents are not

This one is genuinely confusing, because your computer shows you a file that, in a sense, isn’t there. To save disk space, sync clients can leave a [**placeholder**](../chapters/appendix-glossary.llms.md#term-online-only-file) on your disk: the file’s name and icon appear in File Explorer or Finder, but its contents stay in the cloud until something opens it. OneDrive on Windows does this with [Files On-Demand](https://support.microsoft.com/en-us/office/save-disk-space-with-onedrive-files-on-demand-for-windows-0e6860d3-d9f3-4971-b321-7092438fb38e), and macOS does it for iCloud Drive when *Optimize Mac Storage* is on. For documents it’s convenient. For code it’s a trap: your script asks for `data/raw/survey.csv`, the operating system has to download it first, and the read stalls or fails with a confusing error, especially when you’re offline.

Each service marks the state with an icon (here’s [what OneDrive’s icons mean](https://support.microsoft.com/en-us/office/what-do-the-onedrive-icons-mean-11143026-8000-44f8-aaa9-67c985aa49b3)), and each lets you pin a folder so everything in it stays downloaded:

| Service | Online-only looks like | To keep a folder on your computer |
|----|----|----|
| OneDrive (Windows) | a blue cloud | Right-click → **Always keep on this device**. A green circle with a white check means it’s pinned; **Free up space** undoes it. |
| iCloud Drive (macOS) | the *In iCloud* cloud icon | Control-click → **Keep Downloaded**. For a single file, **Download Now**. |
| Google Drive for desktop | a cloud, in *Stream files* mode | Right-click → **Offline access** → **Available offline**, or switch Drive to [*Mirror files*](https://support.google.com/drive/answer/13401938), which keeps everything on your computer. |
| Dropbox | a cloud (“online-only”) | Right-click → **Make available offline** ([Dropbox’s guide](https://help.dropbox.com/sync/make-files-online-only)). |

The quickest check from the terminal compares the size a file claims with the space it really takes up on disk:

``` bash
# macOS and Linux
ls -lh data/raw/survey.csv   # the size the file reports, e.g. 4.2M
du -h data/raw/survey.csv    # space really used: 0, or nearly, if online-only
```

On Windows, right-click the file, choose **Properties**, and compare **Size** with **Size on disk**; an online-only file takes 0 bytes on disk. The sure fix is not to run projects from a synced folder at all (see “What not to keep in a synced folder” below). If a project has to live there, pin its whole folder before you run anything.

### When your Documents folder is really in the cloud

Both operating systems can move your everyday folders into the sync service, and it’s easy to click “yes” during setup without noticing. On Windows, OneDrive’s [folder backup](https://support.microsoft.com/en-us/office/back-up-your-documents-pictures-and-desktop-folders-with-onedrive-d61a7930-a6fb-4b95-b28a-6552e77c3057) (OneDrive’s settings → **Sync and backup** → **Manage backup**) can move Desktop, Documents, Pictures, and other folders into OneDrive, so `Documents` now lives at a path like `C:\Users\you\OneDrive\Documents`, or, for a school account, `C:\Users\you\OneDrive - <your university>\Documents`. On a Mac, iCloud’s [Desktop & Documents Folders](https://support.apple.com/en-us/109344) option moves both folders into iCloud Drive.

That has two consequences for technical work. First, everything you save in Documents is synced, including project folders you never meant to sync. Second, the path now contains spaces and punctuation, which breaks any command that doesn’t quote it ([sec-terminal](#sec-terminal)):

``` powershell
# Fails: the spaces split the path into several arguments
cd C:\Users\you\OneDrive - Example University\Documents

# Works: the quotes keep it together
cd "C:\Users\you\OneDrive - Example University\Documents"
```

You can switch folder backup off for a folder in the same **Manage backup** screen. One thing Microsoft notes that surprises people: files already backed up *stay in the OneDrive folder*, and you move them back yourself. The simplest arrangement is to leave Documents synced for documents and keep projects somewhere else, as below.

### Conflicts: when two copies disagree

If you edit the same file on two computers before they sync, or while one of them is offline, the sync client can’t know which version should win, so it keeps both. The second one shows up as a copy with the computer’s name or the words “conflicted copy” in its name, such as `report-DESKTOP-4J2K.docx` or `report (Alex's conflicted copy 2026-09-24).docx`. Nothing is lost, but nothing is merged either: you compare the two and keep one. You can avoid most conflicts by closing a file before you switch computers, and letting sync finish (watch the icon) before you shut the lid.

### What not to keep in a synced folder

Sync clients are built for documents: a few hundred files that change now and then. Programming projects produce thousands of small files that change constantly, and some tools assume nothing else is writing to their folders. Keep these out of OneDrive, iCloud Drive, Google Drive, and Dropbox:

- **Virtual environments** (`.venv/`, conda environments). They hold tens of thousands of files and are tied to the computer that made them, so they sync slowly and break on the other machine. You can rebuild them from `requirements.txt` anyway ([sec-virtual-environments](#sec-virtual-environments)).
- **Git repositories.** Git and the sync client each assume they’re in charge of the folder. When they disagree (two computers, a half-finished sync), you can get conflicted copies inside the hidden `.git/` folder and a damaged repository. Let GitHub be how a repository moves between computers ([sec-git-github](#sec-git-github)).
- **Caches and generated files**, such as `__pycache__/` and `node_modules/`: they’re regenerated automatically and useless on another machine.
- **Large data files that change often.** Every change uploads the whole file again.

A layout that works: keep active projects in a folder outside sync, such as `~/Projects/` (on Windows, `C:\Users\you\Projects\`, which OneDrive’s folder backup doesn’t touch), put their code under Git with a GitHub remote, and use the synced folder for finished documents you want on every device.

### Mounted, synced, or web-only

Not all remote storage behaves like a sync folder, and the difference shows up the moment the network goes away. A **synced folder** is the kind we’ve been talking about. A [**network drive**](../chapters/appendix-glossary.llms.md#term-network-drive) is a folder on another computer, usually a department file server, that your computer mounts as if it were local: **Map network drive** in File Explorer on Windows (`\\server\share`), or **Go → Connect to Server** in Finder on a Mac (`smb://server/share`). **Web-only** storage is anything you reach through a browser, such as OneDrive or Google Drive on the web, or files attached in Canvas.

| Kind | Works offline? | Can you run code from it? |
|----|----|----|
| Synced folder | Pinned files only | Pinned files only, and never environments or repositories |
| Network drive | No | Slowly: every read crosses the network, and the drive vanishes when the network (or the VPN) does |
| Web-only | No | No: download a copy into your project first |

Files on a server you log in to, such as a lab machine, a research cluster, or a course’s JupyterHub, are a fourth case. They stay on that server, and you move copies back and forth with `scp`, `rsync`, or the hub’s download button ([sec-remote-computing](#sec-remote-computing)). Anything you want to keep from such a server, download before the course ends.

### Sharing links and permissions

When you share from [OneDrive](https://support.microsoft.com/en-us/office/share-onedrive-files-and-folders-9fcc2f7d-de0c-4cec-93b0-a82024800c07) or [Google Drive](https://support.google.com/drive/answer/2494822), you choose who the link works for, and that choice matters more than the friendly button suggests:

- **Anyone with the link:** no sign-in needed; the link can be forwarded, pasted into a group chat, or found by someone you never meant to reach.
- **People in your organization:** anyone with an account at your university.
- **Specific people:** only the accounts you name. This is the safe default.

Choose view or edit access as well. Never share data about people (survey responses, grades, interview notes) through an anyone-link: a link is not a password. When a project ends, open its sharing settings and remove the links you no longer need.

### Your university account will not last forever

University storage is generous while you’re enrolled, and it goes away soon after you leave. Quotas change, too: in February 2021 [Google announced](https://blog.google/products-and-platforms/products/education/google-workspace-for-education/) that its free unlimited storage for schools would end in favor of a pooled limit, and universities set their own quotas in response. Before your last term ends, copy anything you want to keep (projects, writing, and any data you’re allowed to keep) to storage you control, and move your code to a personal GitHub account.

> **NOTE:**
>
> - **OneDrive** comes with every current student account: 5 TB, with files up to 250 GB. OIT notes the quota may change as Microsoft moves to pooled storage. ([OIT: OneDrive](https://oit.colorado.edu/services/messaging-collaboration/microsoft-365/applications/onedrive))
> - **Google Drive** on your CU account is limited to 5 GB, and OIT points you to OneDrive for large files. ([OIT: Google storage limits](https://oit.colorado.edu/services/messaging-collaboration/google-workspace/google-storage-limitations))
> - **After graduation,** you have “approximately 90 days after your degree conferral date” to save files from your CU Google and Microsoft accounts. After that you lose access and the files are deleted, and OIT can’t move them for you. Your CU email lasts one year after your degree posts. ([OIT: alumni FAQ](https://oit.colorado.edu/accounts/alumni/faq))
> - **Off campus,** the campus VPN, free to students, gets you to resources that only work on the campus network, such as some department file servers. ([OIT software catalog](https://oit.colorado.edu/software-hardware/software-catalog))
> - Some courses and departments run their own JupyterHub; your instructor will tell you if yours does. Its files live on the server, so download what you want to keep.
>
> Details change, and OIT’s pages are the source of truth. If something here no longer matches them, please [report it](https://github.com/cuinfoscience/INFO-Missing-Manual/issues/new?template=something-is-wrong.yml).

## 10.8 Common student pitfalls (and how to avoid them)

A handful of mistakes cause nearly all the file pain beginners go through. You’ve met each one earlier in the chapter; here they are together, so you’ll recognize them when they happen.

**Working out of `Downloads` or `Desktop` forever.** Duplicates pile up, `final-2.csv` sits next to `final-3.csv` next to `data.csv`, and three weeks later nothing can be found. Make a stable home under `Courses` or `Projects` and move work there the moment it arrives.

**Confusing cloud sync with local storage.** A notebook hangs on, or can’t find, a data file you can plainly see, because the file is a placeholder your code reached before it downloaded. Keep projects out of synced folders, or pin them so they stay downloaded ([sec-filesystem-cloud](#sec-filesystem-cloud)).

**Changing an extension by accident.** You rename `data.csv` to `data` because the extension was hidden, or save a CSV “as text” and get `data.csv.txt`; now the file opens in the wrong program, or your code can’t find it. Turn on file extensions in File Explorer, or in Finder’s settings ([Apple’s steps](https://support.apple.com/guide/mac-help/show-or-hide-filename-extensions-on-mac-mchlp2304/mac)), and leave them on.

**Moving folders after you’ve written code that depends on them.** Pick your project root early and don’t move it casually, and inside the project use *relative* paths, so everything keeps working as long as the project stays together. If you need an absolute path, build it at run time from `__file__` (next section) rather than typing `/Users/alex/...` into your code: a hard-coded path breaks the moment anyone else runs the project, including you on a new laptop.

## 10.9 Bridging to the terminal and programming

### Why file habits matter for code

When you run a script or a notebook, it quietly receives one piece of context that controls nearly every path it reads or writes: the [**current working directory**](https://en.wikipedia.org/wiki/Working_directory), or CWD. A relative path like `data/raw/survey.csv` isn’t an address on disk. It’s an instruction: “start from the current working directory, find a folder called `data`, then a folder inside it called `raw`, then a file called `survey.csv`.” Change the CWD and the same path means something completely different, or nothing at all.

This is the answer to the 11 p.m. mystery in the Purpose, and it’s why “keep a stable project root and launch your code from it” is more than tidiness. A notebook that works perfectly when you start Jupyter from `~/Courses/INFO-3010/Project/` fails on the very same line if you start Jupyter from `~/Courses/INFO-3010/`, because from one level up there’s no `data/` folder in sight. So when a path breaks, check the CWD before you touch the code:

``` bash
# macOS / Linux, and Windows PowerShell (where pwd is short for Get-Location)
pwd
```

``` python
# From inside Python or a notebook cell
import os
print(os.getcwd())
```

The flip side is that **hard-coded, machine-specific absolute paths are a [code smell](https://en.wikipedia.org/wiki/Code_smell)**: a sign that something will break later. A line like `pd.read_csv("/Users/alex/Downloads/survey.csv")` works on exactly one laptop, until the day its owner moves the file. Nobody else who gets the project, including you in six months on a new machine, can run it without editing the code. Relative paths from the project root are portable for free, so use them.

### Cross-platform path handling (conceptual)

If you only ever use one operating system, path handling mostly stays out of sight. The moment you share code with someone on the other one, the separator (`/` vs `\`) and the shape of the root (`/Users/...` vs `C:\Users\...`) start causing bugs that are hard to track down. The safe habit is to stop writing paths as plain strings and let Python build them for you, with [`pathlib`](https://docs.python.org/3/library/pathlib.html), which is worth learning in your first week:

``` python
from pathlib import Path

import pandas as pd

# This file is src/clean.py, so the project root is two levels up
project_root = Path(__file__).resolve().parent.parent
raw_data = project_root / "data" / "raw" / "survey.csv"
df = pd.read_csv(raw_data)

# Risky: a Windows-only separator (on a Mac this is one odd file name)
df = pd.read_csv("data\\raw\\survey.csv")

# Works on both systems, but only if you launch from the project root
df = pd.read_csv("data/raw/survey.csv")
```

`Path(__file__).resolve().parent` is the trick that lets a script find its own folder no matter where it’s launched from. [`__file__`](https://docs.python.org/3/reference/datamodel.html#module.__file__) is the path of the script’s own source file, `.resolve()` turns it into a full absolute path, and each `.parent` steps up one folder, so a script in `src/` needs two to reach the project root. From there, the `/` operator joins the pieces, and `pathlib` writes them with whatever separator your operating system wants. (Forward slashes in a plain string also work on Windows, which is why the last line runs on both; what makes it fragile is that it depends on the CWD.)

One thing that trips people up: `__file__` exists only in scripts. In a Jupyter notebook it isn’t defined, and using it gives `NameError: name '__file__' is not defined`. In a notebook, launch Jupyter from the project root so relative paths work, or use `Path.cwd()` and check what it says. [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks) covers when to move code from notebooks into scripts, and [sec-git-github](#sec-git-github) covers how this layout fits with version control (`data/raw/` usually belongs in `.gitignore`; `src/` and `notebooks/` don’t).

Two small habits make the rest go smoothly. **Keep paths short,** since deep project trees run into the Windows path limit and make every error message harder to read. And **avoid special characters** in any file name your code will touch: spaces, parentheses, accented letters, and curly quotes all work fine in the file manager and all occasionally break in a terminal or a script. Stick to letters, digits, hyphens, and underscores, and you’ll never have to learn which layer of which tool mangled the quoting.

## 10.10 Stakes and politics

CU Boulder gives you “approximately 90 days” after your degree is conferred to save your files from your university Google and Microsoft accounts; after that they’re deleted (see the callout above). It’s easy to find that out only when you go looking for an old project and it’s gone. The storage felt like yours for four years. It was always on someone else’s terms.

The same is true every day you use a synced folder. Deletion, recovery, account suspension, and quota changes are decisions made by the vendor and your university, not by you, and a setup screen that moves Documents into OneDrive with one click makes that choice before you know there was one. When sync fails, with a conflicted copy or a placeholder where your script needed real bytes, the cost of figuring out the gap between what the screen shows and what the disk holds falls on you, usually without anyone having explained that the gap exists.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: when you decide where a project lives, ask whose rules the storage runs under and what happens when the network, or your account, is gone.

## 10.11 Worked examples

### Building a course workspace from scratch

You’re starting a semester with three classes. Before you download a single handout, make the home that will hold all of them. Open a terminal in your home folder and run:

``` bash
mkdir -p ~/Courses/INFO-3010/{Assignments,Labs,Project}
mkdir -p ~/Courses/INFO-4040/{Assignments,Project}
mkdir -p ~/Courses/STAT-2010/{Labs,Assignments}
```

The `-p` makes any missing parent folders along the way, and the braces are a shell shortcut: `{Assignments,Labs,Project}` expands into three folders. That works in bash and in zsh (the Mac’s default shell) but not in PowerShell, so on Windows use PowerShell’s [`New-Item -ItemType Directory -Force -Path`](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.management/new-item) with each full path, or just right-click in File Explorer and choose **New → Folder**. Then pin `Courses` to your Finder sidebar or Quick access, and every assignment is two clicks away.

### Turning a messy Downloads folder into a clean project

A month ago you started a project by downloading a few CSVs into `~/Downloads/` and writing some throwaway code. Now there are seventeen files mixed in with a semester’s worth of unrelated downloads, and the project is starting to matter. Time to rescue it.

**First, make the project root and its standard folders:**

``` bash
mkdir -p ~/Courses/INFO-3010/Project/{data/raw,data/processed,src,notebooks,reports}
cd ~/Courses/INFO-3010/Project
touch README.md
```

**Second, move the project’s files out of `Downloads`.** Sort `Downloads` by date or name to spot them, then move each into place: data files into `data/raw/`, notebooks into `notebooks/`, scripts into `src/`.

**Third, fix the paths.** Open every script and notebook, find each path pointing at `~/Downloads/something.csv`, and change it to a relative path like `data/raw/something.csv`, so the project no longer depends on where your old Downloads folder was. Run the code once from the project root to confirm it all still works. Now the project is portable, reproducible, and very hard to lose.

### Diagnosing “file not found”

You run a script and Python says `FileNotFoundError: [Errno 2] No such file or directory: 'data/input.csv'`. Resist the urge to start editing the path. Gather evidence first, in three quick checks.

**First, confirm the file exists where you think it does** by listing the folder:

``` bash
ls -la data/        # macOS / Linux
dir data\           # Windows
```

If `input.csv` isn’t in the listing, the bug isn’t in the code: the file is missing or has a slightly different name (a trailing space, a typo, a `.csv.txt` extension you can’t see). Fix the file or its name, not the code.

**Second, if the file is there but Python still can’t find it, check your working directory:**

``` bash
pwd                 # macOS / Linux, and Windows PowerShell
```

A relative path like `data/input.csv` is read from wherever you launched Python. From the project root it works; from inside `notebooks/` or `src/` it doesn’t. Either `cd` to the project root before running, or build the path from `__file__` as shown above.

**Third, only if both of those pass, check whether the file is stranded in the cloud:** a placeholder is on your disk, but its contents aren’t. On Windows the sync icon beside the file tells you; on a Mac, look for the cloud icon in Finder, or use **Get Info** (`Command + I`) to see how much of it is on disk. Download it (or pin its folder) and try again. One of these three checks solves most “file not found” errors; only after all three pass should you go looking in the code.

## 10.12 Exercises

1.  Create a project folder structure and explain (in one paragraph) why each folder exists.

2.  Rename 10 files using a consistent naming convention; justify the convention.

3.  Find all `.csv` files in your course workspace using your operating system’s search.

4.  Make a “raw data is immutable” rule: copy raw data, produce processed data, and document the transformation.

5.  Break and fix: move a folder referenced by a notebook or script; then repair it using relative paths.

6.  Find out whether your Documents folder is synced (OneDrive’s folder backup on Windows, iCloud’s Desktop & Documents Folders on macOS). If it is, choose a folder outside sync for your projects, write down its full path, and check one data file with the size comparison in [sec-filesystem-cloud](#sec-filesystem-cloud).

## 10.13 One-page checklist

- I know where my project root is.

- My project uses a consistent folder structure.

- Raw data is preserved and not edited in place.

- Filenames are descriptive, stable, and machine-friendly.

- I can find files by search (extension, date, keyword).

- I understand whether files are local or cloud-on-demand.

- My projects, environments, and Git repositories live outside synced folders, and my code moves between computers through Git.

- I share files with specific people, not “anyone with the link,” when they contain data about people.

- I know when my university account ends, and I keep my own copy of anything I want after that.

- I can show extensions and hidden items when troubleshooting, and hide hidden items afterward.

- I avoid working in system directories and respect permissions.

## 10.14 Quick reference: key locations

### Windows (typical)

- User home: `C:\Users\<you>\`

- Documents, Downloads, and Desktop under your user home (or inside OneDrive, if its folder backup is on)

- OneDrive: `C:\Users\<you>\OneDrive\` for a personal account, `C:\Users\<you>\OneDrive - <organization>\` for a school or work account

- Google Drive for desktop: its own drive letter, usually `G:\`

### macOS (typical)

- User home: `/Users/<you>/`

- Documents, Downloads, and Desktop under your user home (or inside iCloud Drive, if Desktop & Documents Folders is on)

- iCloud Drive: `~/Library/Mobile Documents/com~apple~CloudDocs/`, shown as *iCloud Drive* in the Finder sidebar

- OneDrive, Google Drive, and Dropbox: folders under `~/Library/CloudStorage/`

> **NOTE:**
>
> - Microsoft, [File Explorer in Windows](https://support.microsoft.com/en-us/windows/file-explorer-in-windows-ef370130-1cca-9dc5-e0df-2f7416fe1cb1) — the official walk-through of File Explorer, from the address bar to the View options.
> - Apple, [Use the Finder on Mac](https://support.apple.com/guide/mac-help/organize-your-files-in-the-finder-mchlp2605/mac) — Apple’s guide to Finder’s windows, views, sidebar, and search.
> - Software Carpentry, [The Unix Shell: Navigating Files and Directories](https://swcarpentry.github.io/shell-novice/02-filedir.html) — a gentle, hands-on lesson on paths, `..`, and the working directory, from the terminal’s side.
> - Hadley Wickham and Jenny Bryan, [What They Forgot to Teach You About R: project-oriented workflow](https://rstats.wtf/projects) — the classic short essay on why hard-coded paths and `setwd()` cause trouble; every lesson carries over to Python.
> - The Turing Way, [Advanced Structure for Data Analysis](https://book.the-turing-way.org/project-design/pd-overview/project-repo/project-repo-advanced) — a community-maintained guide to laying out a research project’s folders so others can reproduce it.
> - Cookiecutter Data Science, [Directory structure](https://drivendata.github.io/cookiecutter-data-science/) — a widely adopted template for `data/`, `src/`, `notebooks/`, and `reports/` layouts, useful as a reference even if you never use the generator.
