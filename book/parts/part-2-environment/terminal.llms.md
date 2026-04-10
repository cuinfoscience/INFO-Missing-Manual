# 10  Command Line

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-os-management](#sec-os-management), [sec-filesystem](#sec-filesystem).
>
> **See also:** [sec-text-editors](#sec-text-editors), [sec-git-github](#sec-git-github), [sec-automation](#sec-automation).

## Purpose

The terminal (command line) is a fast, precise interface for navigating files, running programs, and automating repetitive work. For novices, it can also be intimidating and risky because small mistakes can delete or overwrite work. This chapter builds confident, safe habits for everyday command-line use.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what a **terminal** and a **shell** are, and how commands run.

2.  Navigate the file system reliably (absolute/relative paths, current directory).

3.  Create, view, copy, move, and delete files and directories safely.

4.  Use help tools (`–help`, `man`) and interpret usage/syntax.

5.  Combine commands with pipes and redirection to build small workflows.

6.  Understand exit codes, errors, and common failure messages.

7.  Use permissions and `sudo` responsibly (least privilege, when *not* to use it).

8.  Apply basic security hygiene: protect secrets, avoid unsafe pastes, and reduce accidental damage.

## Scope note

This chapter focuses on Unix-like shells (macOS Terminal, Linux, and Windows via WSL). An appendix maps concepts to Windows PowerShell where relevant.

## 10.1 A beginner mental model

### Terminal vs shell

- **Terminal:** the application window you type in.

- **Shell:** the command interpreter (often `bash` or `zsh`) that runs programs.

- **Command:** a program + arguments you ask the shell to run.

### What happens when you press Enter

1.  The shell reads your command line.

2.  It expands shortcuts (globs, variables).

3.  It locates the program (via `PATH`).

4.  It runs the program in a process and prints output.

5.  It returns an **exit code**: 0 usually means success.

### Why the command line matters

- High action-to-keystroke ratio (fast for repetitive work).

- Composability (small tools + pipes).

- Automation (scripts; reproducible workflows).

- Remote access (SSH; see [sec-remote-computing](#sec-remote-computing)).

## 10.2 Orientation and safety first

### Know where you are (the current working directory)

- Use `pwd` to print the current directory.

- Use `ls` to list contents.

- Use `cd` to change directories.

### The “guardrails” mindset

- Prefer **read-only** commands first: `pwd`, `ls`, `cat`, `head`.

- Before destructive actions: do a dry run (list the targets).

- When in doubt: copy instead of move; move instead of delete.

### Common irreversible mistakes

- Deleting the wrong directory (especially with recursive delete).

- Running a command in the wrong directory.

- Overwriting files with redirection (`>`).

- Using `sudo` to “fix” permission problems without understanding them.

## 10.3 Command anatomy and help

### Basic syntax

    command [options] [arguments]

### Flags and options

- Short flags: `-l`, `-a`

- Long flags: `–all`, `–help`

- Some flags take values: `-o filename` or `–output=filename`

### Built-in help

- `command –help`

- `man command`

- Skim `SYNOPSIS` first; then `OPTIONS`; then `EXAMPLES`.

### Quoting and spaces

- Spaces separate arguments. Use quotes for filenames with spaces.

- Single quotes usually prevent expansions; double quotes allow some expansions.

- Rule: quote variables and paths unless you deliberately want splitting/globbing.

## 10.4 File system navigation

### Key path concepts

- `/` root directory; ` ` your home directory.

- `.` current directory; `..` parent directory.

- Absolute vs relative paths ([sec-filesystem](#sec-filesystem) covers file system organization in depth).

### Core navigation commands

- `pwd` (where am I?)

- `ls` (what’s here?) and useful flags (`-l`, `-a`, `-h`)

- `cd` (go there)

### Tab completion and history

- Use **Tab** to complete commands and paths.

- Use **Up Arrow** (and reverse search if taught) to reuse commands.

- Best practice: edit a recalled command instead of retyping.

## 10.5 Creating, viewing, and editing files

### Creating directories and empty files

- `mkdir` for directories (and `-p` for nested directories).

- `touch` to create a file or update its timestamp.

### Viewing file contents safely

- Small files: `cat`

- Large files: `less` (scroll/search)

- Previews: `head`, `tail`

### Creating small files from the command line

- Redirection to create simple text files.

- Prefer a text editor for multi-line content.

### Editors in the terminal

- Use a beginner-friendly editor flow (e.g., `nano`) for quick edits.

- Know how to exit without panic.

- For longer-term work, use a full editor (VS Code, etc.).

## 10.6 File operations: copy, move, delete (with safety)

### Copy and move

- `cp source dest` (copy)

- `mv source dest` (move/rename)

- Use interactive flags where available to prevent overwrites.

### Deleting files and directories

- `rm file` deletes a file.

- `rm -r dir` deletes a directory tree.

- **High-risk:** `rm -rf`. Teach why it is dangerous.

- Safe practice: `ls` the targets first; consider `rm -i`.

### Globbing (wildcards) and why it matters

- `*` matches many characters; `?` matches one.

- Globs expand *before* the command runs.

- Safety: run `echo *.csv` to preview what a glob matches.

## 10.7 Searching and inspecting

### Finding files

- `find` for locating files by name, type, time.

- Use carefully; start in a narrow directory scope.

### Searching within files

- `grep` for finding patterns in text.

- Teach minimal flags: recursive search, case-insensitive search.

### Inspecting file metadata

- `ls -l` for permissions, size, timestamps.

- `file` to identify file types.

- Checksums concept (optional): how to compare transfers.

## 10.8 Pipes and redirection: building workflows

### Standard streams

- `stdin` (input), `stdout` (output), `stderr` (errors).

### Redirection

- `>` overwrite output to a file; `>>` append.

- Safety: avoid accidental overwrite; teach creating backups.

### Pipes

- `|` sends output of one command into the next.

- Common patterns: `ls | less`, `grep pattern file | head`.

### Exit codes and “did it work?”

- Teach the idea: commands signal success/failure.

- Encourage checking outputs, not assuming.

## 10.9 Environment basics: `PATH`, variables, and reproducibility

### Environment variables

- What they are and why tools use them.

- Basic operations: `echo $VAR`, setting variables (conceptual).

### PATH and locating commands

- `PATH` controls where the shell searches for programs.

- Use `which` (or equivalent) to see which program will run.

- Common pitfall: multiple versions of a tool installed.

### Working directory as a dependency

- Relative paths depend on where you run the command.

- Best practice: adopt a stable project root and use relative paths within it.

## 10.10 Permissions, ownership, and `sudo`

### The permission model (just enough)

- Users, groups, and “other.”

- Read/write/execute bits and what they mean for files vs directories.

- Recognizing permission errors.

### When to use `sudo` (and when not to)

- `sudo` runs a single command with elevated privileges.

- Use it for system-level changes (installing software, editing system configs) when appropriate.

- Do **not** use `sudo` to fix a broken project folder or to run routine scripts.

### Safe `sudo` practices

- Read the command twice before running.

- Prefer explicit paths over wildcards.

- Avoid piping into `sudo` unless you understand the implications.

- Never run unreviewed copy-pasted commands with `sudo`.

### Recovering from permission issues

- First identify ownership/permissions and the target directory.

- If you created a mess with `sudo`, stop and ask for help.

## 10.11 Security hygiene for terminal users

### Secrets and command history

- Your shell history may record commands.

- Never put passwords/tokens directly on the command line if avoidable.

- Prefer environment variables, config files with correct permissions, or secret managers (conceptual).

### Copy/paste safety

- Understand that copied commands may include hidden characters.

- Always inspect commands before running; avoid running multi-line scripts you do not understand.

- Prefer official documentation sources.

### Least privilege

- Work in your home directory as a normal user.

- Elevate privileges only for specific administrative tasks.

## 10.12 Workflow patterns for students

### Pattern 1: “enter a project, run, exit”

1.  `cd` into a project folder.

2.  List files; confirm you are in the right place.

3.  Run a command (script, notebook server, tests).

4.  Save outputs into a clear directory.

5.  Exit cleanly.

### Pattern 2: creating a reproducible command log

- Keep a `README.md` or `notes.txt` with the commands needed to reproduce results.

- Record inputs, outputs, and environment assumptions.

### Pattern 3: safe cleanup

- Identify targets with search and preview.

- Archive important outputs.

- Delete with care; verify afterward.

## 10.13 Troubleshooting playbook

### Common errors and what they mean

`command not found`  
Program not installed or PATH misconfigured.

`No such file or directory`  
Wrong path, wrong working directory, or typo.

`Permission denied`  
Insufficient rights; avoid reflexive `sudo`.

`Is a directory`  
Command expected a file.

### A disciplined response

1.  Re-run the command slowly; check spelling.

2.  Print current directory; list files.

3.  Confirm paths and file extensions.

4.  Consult `–help` or `man`.

5.  If still stuck: create a minimal reproduction and ask a precise question.

## 10.14 Worked examples (outline)

### Example 1: Build a course workspace

- Create directories for `courses/`, `assignments/`, `project/`.

- Practice navigation and listing.

### Example 2: Create and inspect a dataset file

- Download/move a `.csv`.

- Preview with `head` and `less`.

- Search for a column name with `grep`.

### Example 3: Build a small pipeline

- Combine commands with pipes.

- Redirect output to a file.

- Verify results.

### Example 4: Diagnose and fix a “file not found” error

- Identify working directory mismatch.

- Repair using relative paths and project root conventions.

## 10.15 Templates

### Template A: Safe destructive action checklist

    Before deleting/moving:

    1. pwd
    2. ls (confirm context)
    3. Preview targets (echo glob / ls targets)
    4. Copy/backup if uncertain
    5. Execute with least privilege (no sudo unless required)
    6. Verify after

### Template B: Reproducible command log

    Project:
    Date:
    Goal:
    Commands:

    * ...
      Inputs:
    * ...
      Outputs:
    * ...
      Notes/assumptions:
    * ...

## 10.16 Exercises

1.  Navigate from your home directory to a course folder using only `cd`, `pwd`, `ls`.

2.  Create a project directory structure with `mkdir -p`.

3.  Create a text file, preview it with `head`, then open it in `less`.

4.  Copy a directory; rename the copy; explain the difference between copy and move.

5.  Use a wildcard to list only `.csv` files; preview the expansion with `echo`.

6.  Build a pipeline that searches within a file and writes matching lines to an output file.

7.  Trigger a permission error intentionally (in a safe location) and explain why `sudo` is not the first fix.

## 10.17 One-page checklist

- I can explain terminal vs shell, and command + arguments.

- I can navigate with `pwd`, `ls`, `cd` and understand paths.

- I can create files/directories and view contents safely.

- I can copy/move/delete with caution and preview wildcards.

- I can use `–help` and `man`.

- I can use pipes and redirection and understand overwrite vs append.

- I understand permissions and use `sudo` only when appropriate.

- I avoid leaking secrets in commands and history.

## 10.18 Windows notes: PowerShell and WSL (optional)

### Two common paths

- **WSL** gives a Linux-like shell where `sudo` and Unix commands apply.

- **PowerShell** uses different command names and syntax (but the same mental models: paths, pipes, permissions).

### Concept mapping (high level)

- Navigation: `cd`, `pwd` (`Get-Location`), listing (`ls`/`dir`).

- Help: `–help`/`man` vs `Get-Help`.

- Pipes exist in both, but objects vs text differ.

## 10.19 What is a terminal?

A terminal is a tool for interacting with your computer by issuing commands. A terminal launches a shell (e.g. `bash` or `zsh`), so sometimes you will hear a “terminal” also described as a “shell”.

## 10.20 What terminal commands should I know, as a basic foundation?

The exact syntax of terminal commands will be slightly different on Windows and Mac. So to keep things consistent, we are only going to detail high-level descriptions of terminal commands in this guide. You can Google the exact commands for your specific system; it is good practice to learn to search for the terminal commands you will need online.

To get started with the terminal for your INFO classes, you should memorize the commands for each of the following:

- Activate/deactivate a conda environment

- Change your directory

- Install a specific version of a package with conda

- Inspect the location of a program to the terminal (e.g. `which Python`)

- Print your working directory
