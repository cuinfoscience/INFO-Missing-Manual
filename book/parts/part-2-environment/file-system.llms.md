# 9  Local File System

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-os-management](#sec-os-management).
>
> **See also:** [sec-terminal](#sec-terminal), [sec-project-management](#sec-project-management).

## Purpose

Most beginner frustration in computing is not “coding’’—it is losing track of files, confusing locations, and breaking workflows by moving or renaming things. This chapter builds durable habits for accessing, navigating, organizing, and managing files and folders on **Windows** (File Explorer) and **macOS** (Finder).

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain the difference between **files**, **folders/directories**, **paths**, and **extensions**.

2.  Navigate reliably in File Explorer and Finder using core affordances (sidebar, breadcrumbs, search, recent, tags).

3.  Use absolute vs relative paths and understand key path conventions on Windows and macOS.

4.  Adopt naming and organization conventions that scale from one assignment to a multi-month project.

5.  Recognize hidden files, sync-folder behaviors (OneDrive/iCloud), and common pitfalls.

6.  Apply basic safety practices: avoid destructive moves, manage duplicates, and preserve provenance.

## Running theme: “Location is a dependency’’

A script, notebook, or application often assumes files are in specific locations. Good file management makes those dependencies explicit and stable.

## 9.1 A beginner mental model

### Files vs folders

- **File:** a named unit of stored data (e.g., `report.docx`, `data.csv`).

- **Folder/directory:** a container that holds files and other folders.

- **Hierarchy:** folders inside folders form a tree.

### Paths: how the computer points to a location

- **Absolute path:** full location from a root.

- **Relative path:** location relative to your current folder.

- **Separators:** Windows uses backslashes (`\`); macOS uses forward slashes (`/`).

### Windows vs macOS path conventions (what novices must know)

- **Windows:** drive letters and fully-qualified paths like `C:\Users\name\Documents`; also network (UNC) paths like `\server \share`.

- **macOS:** volume-and-directory paths like `/Users/name/Documents` (POSIX-style).

- **Path length and odd edge cases:** Windows has historical maximum path-length constraints and special path forms; you should keep project paths short and avoid deeply nested folders when possible.

### Extensions and file types

- Extensions (e.g., `.csv`, `.py`) help your OS and apps guess how to open a file.

- For reproducible work, prefer stable, plain formats (`.csv`, `.txt`, `.md`) over opaque or proprietary formats when possible.

## 9.2 Access and navigation on Windows (File Explorer)

### Opening and orienting

- Open File Explorer; identify the sidebar (Quick access/Home), main pane, and address bar.

- Learn the breadcrumbs: click segments in the path bar to jump to parent folders.

### Core navigation skills

- Move up/down the hierarchy, open in new tabs/windows, and return to recent locations.

- Use search correctly: search within the current folder vs across the whole machine.

- Use sort and view options: by name, date modified, type, size.

### Make file extensions and hidden items visible (when troubleshooting)

- Toggle viewing extensions to avoid confusion (`data.csv` vs `data.csv.txt`).

- Toggle hidden items when necessary for diagnostics.

### Local vs synced locations (OneDrive)

- Understand sync status indicators and what they imply about local availability.

- Recognize online-only” vs always keep on this device’’ behaviors, especially when working offline.

## 9.3 Access and navigation on macOS (Finder)

### Opening and orienting

- Open Finder; identify the sidebar (Favorites, iCloud Drive), toolbar, and path location.

- Understand view modes: icons, list, columns, gallery (choose based on task).

### Core navigation skills

- Use the hierarchy: parent folders, column view for rapid browsing.

- Use Finder search and filters; search this Mac vs this folder.

- Use tags to create lightweight categories without moving files.

### Hidden files and system folders (what to avoid)

- Finder hides some system locations by default; treat hidden/system folders as “do not edit unless you know why.’’

- If you must inspect hidden files for troubleshooting, do so carefully and revert the view when done.

### Local vs iCloud behavior

- macOS can optimize storage by moving less-used files to iCloud and downloading them on demand.

- Implication for projects: ensure critical files are actually present locally before running analyses.

## 9.4 Organizing work: conventions that scale

### A default structure for students

Recommend a stable home for course work:

- `School/` or `Courses/`

- `CourseName/`

- `Assignments/`, `Labs/`, `Project/`

### A default structure for data projects

- `README.md` (how to run, where things are)

- `data/raw/` (immutable inputs)

- `data/processed/` (derived outputs)

- `src/` (scripts and reusable code)

- `notebooks/` (exploration, not production)

- `reports/` or `figures/`

### Naming conventions

- Use meaningful, stable names: `YYYY-MM-DD` prefixes for dated artifacts.

- Avoid spaces and special characters when files will be used in code.

- Prefer lowercase with hyphens/underscores: `clean-survey-2026-01.csv`.

- Never use `final.docx`, `final-final.docx`; use semantic versioning or dates.

### Provenance and duplicates

- Keep raw files read-only; do not edit original data in place.

- When you must create variants, record why and how (notes in README or a changelog).

- Learn to detect duplicates (same name, different content; same content, different name).

## 9.5 Search, metadata, and “finding it later’’

### Search strategies that work

- Search by extension (`.csv`, `.ipynb`) and by date modified.

- Use unique keywords in filenames so search works.

- Use tags (macOS) or pinned/Quick Access folders (Windows) for frequently used locations.

### Sort and view for diagnosis

- Sort by date modified to find what changed.

- View details (size, type) to spot suspicious zero-byte or unexpectedly large files.

## 9.6 File operations and safety

### Copy vs move vs rename

- **Copy:** duplicates content; safer when experimenting.

- **Move:** changes location; can break code/notebooks that reference the old path.

- **Rename:** changes identity; can break references and links.

### Delete and recover

- Understand Trash/Recycle Bin behavior.

- Treat permanent deletion as destructive; verify before emptying.

### Permissions basics (just enough)

- Errors like Access denied” or Permission denied’’ usually mean you lack rights to read/write/execute.

- Prefer working in your user home directory; avoid system directories.

## 9.7 Common student pitfalls (and how to avoid them)

### Pitfall: working from Downloads/Desktop forever

- Symptom: files disappear, duplicates accumulate, paths break.

- Fix: move projects into a stable `Courses/` or `Projects/` location.

### Pitfall: confusing cloud-sync with local storage

- Symptom: notebook cannot find data, or files are not available offline.”

- Fix: confirm local availability; understand sync icons and on demand’’ downloads.

### Pitfall: accidental extension changes

- Symptom: file opens in the wrong program or fails to load.

- Fix: show extensions when working with data/code; avoid manual extension edits unless you understand the effect.

### Pitfall: moving folders after writing code

- Symptom: scripts break because paths are hard-coded.

- Fix: keep a stable project root; use relative paths inside projects.

## 9.8 Bridging to the terminal and programming

### Why file habits matter for code

- Your “current working directory’’ controls how relative paths resolve.

- Cross-platform projects should avoid hard-coded, machine-specific absolute paths.

### Cross-platform path handling (conceptual)

- Prefer path-join utilities (e.g., language path libraries) rather than manual concatenation.

- Keep paths short, avoid special characters, and standardize folder structure.

## 9.9 Worked examples (outline)

### Example 1: Build a course workspace on Windows and macOS

- Create the `Courses/` directory.

- Create an assignment folder with a consistent template.

- Pin/favorite the folder for quick access.

### Example 2: Turn a messy Downloads folder into a clean project

- Identify project files by extension and date.

- Move into a new project root.

- Create `data/raw` vs `data/processed` and update references.

### Example 3: Diagnose “file not found’’

- Confirm the file exists, the name matches exactly, and the extension is correct.

- Confirm you are searching/running from the intended directory.

- Confirm cloud-sync availability and permissions.

## 9.10 Exercises

1.  Create a project folder structure and explain (in one paragraph) why each folder exists.

2.  Rename 10 files using a consistent naming convention; justify the convention.

3.  Find all `.csv` files in your course workspace using OS search.

4.  Make a “raw data is immutable’’ rule: copy raw data, produce processed data, and document the transformation.

5.  Break and fix: move a folder referenced by a notebook/script; then repair it using relative paths.

## 9.11 One-page checklist

- I know where my project root is.

- My project uses a consistent folder structure.

- Raw data is preserved and not edited in place.

- Filenames are descriptive, stable, and machine-friendly.

- I can find files by search (extension/date/keyword).

- I understand whether files are local or cloud-on-demand.

- I can show extensions/hidden items when troubleshooting and hide them afterward.

- I avoid working in system directories and respect permissions.

## 9.12 Quick reference: key locations

### Windows (typical)

- User home: `C:\Users\\`

- Documents/Downloads/Desktop under user home

- OneDrive folder (if enabled): typically under user home

### macOS (typical)

- User home: `/Users//`

- Documents/Downloads/Desktop under user home

- iCloud Drive appears in Finder sidebar; local availability may vary with storage settings

Your computer’s “file system” is the hierarchy of folders and files where programs and documents are saved as well as the software and hardware for storing and retrieving these data. Windows and macOS are very different operating systems with very different underlying file systems. It is really important that you are able to access and navigate through your computer’s file system for everything from downloading files to configuring options. This section will cover how to familiarize yourself with your computer’s file system, the location of some important folders, and navigating to new folders you create. In this section, you will do this using the graphical user interfaces (GUI) in macOS or Windows.

![](graphics/macos_finder_icon.png)

The macOS Finder icon.

##### macOS Finder.

The “Finder” application is the primary graphical user interface for interacting with the macOS file system.[^1] Finder is always running in the background when you are using macOS. A few core actions will help you orient yourself:

1.  **Open a Finder window.** Click the Finder smiley face icon in the Dock. If Finder is already active but no window is visible, choose `File`→`New Finder Window` from the menu bar or press `Command + N`.

2.  **Navigate via the sidebar.** The sidebar lists common locations (Favorites, iCloud Drive, Downloads, Applications). Clicking a folder shows its contents in the main pane. Use the back and forward buttons to move through history.

3.  **Choose a view.** Use the toolbar buttons or `View`→ menu to switch between icon, list, column, and gallery views. Column view is especially useful for seeing the folder hierarchy and previewing files without opening them.

4.  **See the full path.** Enable the path bar via `View`→`Show Path Bar`. You can also right‑click the window title to copy the folder’s full path for use in scripts.

5.  **Search effectively.** Press `Command + F` to search. Use the scope buttons to limit search to the current folder or your entire Mac, and refine results by kind, date, or name.

![](graphics/windows_explorer_icon.png)

The Windows File Explorer icon.

##### Windows File Explorer.

Windows File Explorer is the graphical tool for navigating the file system on Windows. Open it by clicking the folder icon in the taskbar, pressing `Windows + E`, or selecting `File Explorer` from the Start menu. Key concepts include:

1.  **Navigation pane.** The left‑hand pane contains Quick Access (pinned and recent folders), This PC (drives and user folders), and network locations. Click an entry to display its contents in the main pane. Pin frequently used folders to Quick Access by right‑clicking and choosing “Pin to Quick access.”

2.  **Address bar and breadcrumbs.** The address bar shows your current path as clickable segments (breadcrumbs). You can type a path (e.g., `C:\Users\name\Documents`) and press `Enter` to jump directly. Right‑click the bar to copy the full path.

3.  **Views and sorting.** Use the `View` tab or the layout buttons to switch between details, list, tiles, or large icons. Sort by name, date modified, type, or size to locate files quickly.

4.  **Search box.** The search box in the top‑right corner searches within the current folder by default. Combine it with filters like kind or date (via the Search tab) to narrow results. Remember that searching the entire drive can take time.

##### File paths.

A “file path” is an address that describes where a folder or file lives on your computer. The file paths for Windows and macOS use different formats and the commands for navigating and accessing each are not compatible. I am going to use my personal Mac and PC computers as an example; the file paths on your computer will be different. My “Downloads” folder on my Windows has a file path of `C:\Users\Brian\Downloads`. The `C:\` is the name of the primary hard drive on almost every PC.[^2] My “Downloads” folder on my macOS has a file path of `/Users/Brian/Downloads`.

**Note on drives and separators.** Windows may assign other drive letters (`D:`, `E:`, etc.) if you have multiple hard drives or partitions. Replace `C:\` with the correct letter when constructing paths. Also remember that Windows uses backslashes (`\`) to separate path components, whereas macOS and Linux use forward slashes (`/`). This difference matters when typing paths in the terminal or code.

## 9.13 Why can’t I find a file I downloaded from Canvas? Where did it go?

Building on the ideas about your computer’s file system from the previous section, it is important to know where to find the files we download using our web browser. Depending on the defaults and other preferences of your web browser, downloaded folders might go to your Desktop, a Downloads folder, or some other place. The steps below will make sure that your browser is downloading the folders to a consistent location: your Downloads folder. Instructions for changing the download location of the most popular web browsers (Chrome, Safari, Firefox, and Edge) are listed below with links to their official documentation or other tutorials.

![](graphics/download-location-chrome.png)

Figure 9.1: Changing the Chrome download location.

##### Chrome.

[^3] Open Chrome, click the ![hamburger menu icon](graphics/hamburger_trail.png) button in the upper right corner, select “Settings”, and scroll to the bottom and click “Advanced”. Under the “Downloads” section, click “Change”. Use the Finder (macOS) or File Explorer (Windows) window that pops up to navigate to your “Downloads” folder and click “Select Folder”. See [Figure fig-download-location-chrome](#fig-download-location-chrome).

![](graphics/download-location-safari.png)

Figure 9.2: Changing the Safari download location.

##### Safari.

[^4] This should be set to your “Downloads” folder by default but here are the steps to change it. Open Safari, select “Safari” from the menu bar, and click “Preferences…”. In the “General” tab, click the drop-down next to “File download location. User the Finder window that pops up to navigate to your”Downloads” folder. See [Figure fig-download-location-safari](#fig-download-location-safari).

##### Mozilla.

[^5] Open Firefox, click the ![hamburger menu icon](graphics/hamburger_menu.png) button in the upper-right, and select “Settings”. In the “General” panel, scroll down to the “Files and Applications” section, and click the “Browse…” button. Use the Finder (macOS) or File Explorer (Windows) window that pops up to navigate to your “Downloads” folder and click “Select Folder”. See [Figure fig-download-location-mozilla](#fig-download-location-mozilla).

![](graphics/download-location-mozilla.png)

Figure 9.3: Changing the Firefox download location.

##### Edge.

[^6] Open Edge, slick the ![three-dot menu icon](graphics/three_dots.png) button in the upper-right, and click “Settings”. Select “Downloads” in the menu on the left and in the “Location” area click the click the “Change” button. Use the File Explorer window that pops up to navigate to your “Downloads” folder and click “Select Folder”. See [Figure fig-download-location-edge](#fig-download-location-edge).

##### File types.

Note that some file types like PDFs may open by default in your web browser rather than saving to your Downloads folder. Some other types of files like DOC or XLS may open in Word or Excel by default and are saved in arcanely-named and impossible-to-find temporary folders. If you want to be able to work with these files after you have downloaded them, make sure to use the “Save as” functionality in the browser, PDF reader, Office application, *etc.* to move it to a more appropriate location like a “Downloads” or class-specific folder. The details on how to do this are specific to that application: use the documentation links provided for the browsers in the previous section to search for information and tutorials if you are having trouble.

![](graphics/download-location-edge.png)

Figure 9.4: Changing the Edge download location.

## 9.14 What does it mean to unzip a file? How do I do that?

Compressed zip files are archives that bundle one or more files into a single package and reduce their size. Before you can work with the contents, you need to *unzip* (extract) the archive. Both Windows and macOS provide built‑in tools to handle zip files, and many third‑party tools exist. The basic workflow is the same:

##### On Windows.

Locate the `.zip` file in File Explorer. Right‑click the file and choose “Extract All…” from the context menu. A dialog will ask where to extract the files; by default it creates a folder with the same name as the zip file in the current directory. You can browse to choose a different location. After extraction completes, open the new folder to access the files. It is safe to delete the original zip file once you have verified that the extraction succeeded.

##### On macOS.

Double‑click the `.zip` file in Finder or select it and choose `File`→`Open`. Archive Utility will automatically decompress the archive into a folder alongside the zip file. If you need more control, you can right‑click and select “Open With → Archive Utility” or use a third‑party app such as The Unarchiver. After unzipping, a folder with the same name appears; open it to access the extracted files. You can move this folder into your project structure and delete the original zip file.

##### Safety tips.

Never run executables from a zip file you downloaded unless you trust the source. Always choose a destination folder you can locate easily (for example, your “Downloads” folder or a course project folder), and avoid unzipping directly into system folders. Keep raw zipped archives if you need to preserve the original state for provenance, but otherwise deleting them saves space.

[^1]: <https://support.apple.com/en-us/HT201732>

[^2]: If you have multiple hard drives,

[^3]: <https://support.google.com/chrome/answer/95759>

[^4]: <https://www.macrumors.com/how-to/change-safari-download-save-location-mac/>

[^5]: <https://support.mozilla.org/en-US/kb/where-find-and-manage-downloaded-files-firefox>

[^6]: <https://support.microsoft.com/en-us/microsoft-edge/change-the-downloads-folder-location-in-microsoft-edge-4049e93b-0ef6-e44f-aca0-7d5f37a39294>
