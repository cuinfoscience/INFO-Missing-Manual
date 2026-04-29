# 12  Text Editors

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-filesystem](#sec-filesystem).
>
> **See also:** [sec-terminal](#sec-terminal), [sec-git-github](#sec-git-github), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).

## Purpose

![Mordor Meme: One Does Not Simply Exit Vim.](../../graphics/memes/text-editors.png)

Text editors are the primary tool for writing code, configuring tools, inspecting logs, and fixing small problems quickly. For beginners, the main challenge is not typing—it is developing reliable workflows: opening the right file, editing safely, finding and replacing correctly, and understanding the trade-offs between terminal editors, GUI editors, and full IDEs.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what makes a file “text” (vs binary) and why encoding and line endings matter.

2.  Use essential editor operations: open/save, undo/redo, find/replace, multi-file search, and navigation.

3.  Debug common file problems: wrong path, wrong extension, hidden characters, encoding issues, and line-ending mismatches.

4.  Choose an appropriate editor class for a task (terminal editor vs GUI editor vs IDE).

5.  Use a GUI editor for simple scripting: run scripts, read errors, and iterate.

6.  Apply safe refactoring habits with find/replace and version control.

7.  Configure an editor minimally: indentation, formatting, linting, and extensions.

## Running theme: editors are tools, not identities

Choose an editor that fits the task, and build habits that transfer across editors: paths, file formats, search, safe edits, and reproducibility.

## 12.1 A beginner mental model

A surprising amount of computing happens inside plain text files. Your code is plain text. Your configuration files (`.gitignore`, `pyproject.toml`, `_quarto.yml`, `requirements.txt`) are plain text. Your data, when it is in a friendly format like CSV or JSON, is plain text. Your logs are plain text. Your README is plain text. The text editor is the universal workbench you use to read and modify all of those, and learning to drive one well pays back across every other tool in this book.

What an editor actually *does* under the hood is conceptually simple. It reads bytes from disk and interprets them as characters using an **encoding** (usually UTF-8 in modern projects). It displays those characters on your screen with line breaks and whitespace where they belong, and it lets you change them. When you save, it writes the bytes back to disk in the same encoding. Most editor problems — strange characters, files that look fine in one tool and broken in another, mysterious “invalid syntax” errors — come from a mismatch somewhere in that pipeline: wrong encoding, wrong line endings, or invisible whitespace where the language did not expect it.

A small vocabulary will save you a lot of confusion. **Encoding** is the rule for turning raw bytes into characters; UTF-8 is the modern default and you should not save files in anything else unless you have a specific reason. **Line endings** are the invisible characters that mark the end of each line; macOS and Linux use a single newline (LF, byte `\n`), while Windows uses a carriage-return-then-newline pair (CRLF, bytes `\r\n`), and projects shared between OSes can produce noisy diffs and parser errors when they get mixed. **Whitespace** is the catch-all term for spaces, tabs, and newlines, and it matters more in some languages than others — Python, YAML, and Makefiles in particular treat whitespace as significant and will fail on tabs-vs-spaces confusion. **Syntax highlighting** is when an editor colors keywords, strings, and comments differently so the structure of the code is visually obvious. **Linting and formatting** are automated tools that check style and normalize it (see [sec-linting](#sec-linting)). And an **IDE** (“integrated development environment”) is a heavier kind of editor that bundles a build system, a debugger, and language tooling into one package — useful for some ecosystems, overkill for others.

## 12.2 Choosing your tool: three editor classes

Editors come in three rough sizes, and it is worth knowing which size fits which job.

The smallest are **terminal editors** like [`nano`](https://www.nano-editor.org/docs.php), [`vim`](https://www.vim.org/docs.php), and [`emacs`](https://www.gnu.org/software/emacs/documentation.html). They run inside a terminal window, so they work over SSH on any server you can log into, they have almost no startup time, and they are always available — even on the most stripped-down Linux box. Their downside is the learning curve: `vim`’s modal editing in particular feels alien for a few days before it clicks. Most students do not need to live in a terminal editor, but every student should learn enough `nano` to confidently open a file, change one line, and save and exit. That single skill turns “I have to fix one character on a remote server and I cannot do it” from an impasse into a thirty-second task.

The middle tier is **GUI code editors** — [VS Code](https://code.visualstudio.com/docs) is by far the most popular today, with [Sublime Text](https://www.sublimetext.com/docs/) and [Cursor](https://docs.cursor.com/) as alternatives.

![](graphics/PLACEHOLDER-vscode-overview.png)

Figure 12.1: ALT: VS Code window with a Python file open, showing the file-explorer sidebar on the left, the editor pane in the centre with a code block and a Run button, and an integrated terminal docked at the bottom.

These run as desktop apps, give you a multi-tab interface with a file tree on the left, and combine the best of a text editor (fast, lightweight, language-agnostic) with the convenient parts of an IDE (find-across-files, an integrated terminal, formatting on save, linter integration, Git integration). For day-to-day coursework, scripting, notebooks, and lightweight projects, this is the right default. Pick one — almost everyone picks VS Code — and invest in learning it well.

The largest tier is **IDEs**: [Visual Studio](https://learn.microsoft.com/en-us/visualstudio/) for C# and .NET work, [IntelliJ](https://www.jetbrains.com/idea/) for Java, [Xcode](https://developer.apple.com/documentation/xcode) for Swift and iOS, [RStudio](https://posit.co/products/open-source/rstudio/) for R, and so on. IDEs win when you are working in an ecosystem with a heavy build system, a complicated project model, or specialized debugging needs. They are powerful but heavy, and their project configuration can be fragile in ways that occasionally eat hours of your day.

The decision rule for a typical Python data student is straightforward. For a quick edit on a remote server, use `nano` (or `vim` if you are comfortable with it). For everything else — Python scripting, notebooks, small projects — use a GUI editor with an integrated terminal, defaulting to VS Code. Reach for a full IDE only if your course or project specifically requires it.

## 12.3 Essential editor skills (transfer across tools)

The operations in this section are the ones that transfer across every editor you will ever use. Learn them once, in whichever editor is your daily driver, and you will recognize their equivalents in `nano`, `vim`, VS Code, and any IDE a future job puts in front of you.

### Open, save, and “where did it go?”

The single most common beginner confusion is not *how* to save, it is *where* a save went. A typical failure looks like this: you hit Save, you run the script, and the error you were fixing is still there. The problem is almost never the editor — it is that the file you edited is not the file your program loaded. Maybe you opened a copy from your Downloads folder instead of the project copy. Maybe you hit “Save As” and accidentally created a new file with a slightly different name. Maybe you were editing an older snapshot that your editor restored from a previous session.

The fix is a habit: every time you save a file for the first time in a session, read the file path in your editor’s title bar and confirm it matches where you think you are. VS Code shows the full path in the tab’s hover tooltip; most editors display the directory next to the filename in the window title. Learn the difference between **Save** (write to the existing file path) and **Save As** (write to a new path), and treat “Save As” as a deliberate rename — never as a substitute for Save. When you edit a file that the operating system considers read-only — a system config file, a file inside a protected directory — the editor will warn you and may prompt for an administrator password. Do not click through that prompt without thinking about why it appeared: you are being asked to modify something that normal users are not supposed to modify, and that is usually a sign you should double-check your plan.

### Undo/redo and safe experimentation

Undo (`Ctrl+Z` / `Cmd+Z`) is your first safety net. It lets you try something, see it fail, and back out immediately. Redo (`Ctrl+Y` / `Cmd+Shift+Z`) reverses an undo, which is useful when you hit Undo one step too many. Every editor has these, and you should reach for them without thinking.

Undo has limits, though. It usually only spans the current session — close the file and reopen it, and your undo history is gone. It also does not help when a bad edit has already been overwritten by subsequent edits. That is where your *second* safety net comes in: version control. Commit small, focused changes as you work, and you can always `git diff` to see exactly what changed since the last commit, or `git checkout` a file to throw away the current changes and return to the committed version. See [sec-git-github](#sec-git-github) for the mechanics. The habit to build is: commit before you start a risky change, so that if the change goes wrong, the worst case is losing a few minutes of work instead of an afternoon.

### Indentation and whitespace

Pick an indentation style for a project and stick to it. For Python, the community standard is four spaces per level; for YAML and most web files, two spaces is common. Whatever you pick, **do not mix tabs and spaces** — it is the most common cause of mysterious parser errors in Python and the single most common cause of broken YAML. Configure your editor to insert spaces when you hit the Tab key (in VS Code: `"editor.insertSpaces": true`), and to treat a file’s existing indentation as the source of truth when you open it (`"editor.detectIndentation": true`).

When a whitespace-related bug appears, turn on visible whitespace. In VS Code the command is `View → Render Whitespace → All`, and in most other editors it is labeled similarly. Once visible, spaces render as faint dots and tabs as faint arrows, and a line that *looks* correctly indented but is actually using a tab becomes immediately obvious:

``` text
def greet(name):
····print(f"hello, {name}")   ← spaces, correct
——→ print(f"hello again")     ← tab, will break in Python
```

Python cares about whitespace because the language uses indentation to delimit blocks — there are no curly braces, and a block ends when the indentation shrinks. If one line is four spaces and the next is a tab, Python sees two different indentation levels and raises `IndentationError: unindent does not match any outer indentation level`. YAML is the same story: a tab where the parser expected spaces breaks the file silently, and the error message rarely points at the tab itself.

### Find, replace, and refactoring safety

Find and replace is a power tool. Used carelessly, it can rewrite hundreds of lines across dozens of files in the time it takes to regret it. The safe protocol is always the same. **Find first, replace second:** start with a plain “Find” so you can see *every* match and confirm that each one is actually what you intended to change. A search for `mean` will also match `meaning`, `demean`, `mean_squared`, and every docstring that contains the word “mean” — if you jump straight to Replace, you will corrupt unrelated code.

Learn the difference between the **scopes** your editor offers:

- **Current selection** — replace only inside the highlighted text. Useful when a function has one local variable you want to rename.
- **Current file** — replace everywhere in the file you are editing. The default.
- **Entire workspace / project** — replace across every file the editor is aware of. The most powerful and the most dangerous.

For any nontrivial change, use “Replace with confirmation” (sometimes called “Replace one at a time”), which lets you step through each match and decide whether to apply the replacement. In VS Code, the workspace-wide search panel (`Cmd+Shift+F` / `Ctrl+Shift+F`) shows every match grouped by file, and each individual match has its own Replace button so you can rewrite them selectively.

Learn the basics of **regular expressions**, because many real find/replace jobs need them. At minimum, learn anchors (`^` for start of line, `$` for end of line), wildcards (`.` for any character, `.*` for any run of characters), and capture groups (`(...)` to capture text you want to reuse in the replacement as `$1`, `$2`, and so on). See [sec-regex](#sec-regex) for a fuller treatment. A concrete example: to rename every `print("foo: " + x)` to `print(f"foo: {x}")`, you can search for `print\("foo: " \+ (\w+)\)` and replace with `print(f"foo: {$1}")` — but only after confirming the matches look right.

After any replace, re-run the code or the tests. The whole point of the protocol is that you treat the change as experimental until you have verified it did not break anything.

### Multi-file search and navigation

A project of any size contains more files than you can hold in your head. Your editor’s **workspace search** (`Cmd+Shift+F` / `Ctrl+Shift+F`) is how you find things across all of them — every mention of a function name, every occurrence of a string, every place a config variable is referenced. Get comfortable with it early; it is the single biggest productivity difference between students who spend time navigating projects and students who spend time getting lost in them.

Three navigation commands are worth learning on day one of any new editor:

- **Go to file** (`Cmd+P` / `Ctrl+P` in VS Code): type a fragment of a filename and jump straight there. Much faster than clicking through the file tree.
- **Go to line** (`Ctrl+G` in VS Code): when an error message says “line 147,” you want to get there in one keystroke.
- **Go to definition** (`F12` in VS Code): click a function name and jump to where it is defined, even if it is in a different file. Especially powerful once a project has multiple modules.

Keep a clear mental model of the **project root** — the folder that contains your `README.md`, `pyproject.toml`, or `.git/` directory. Your editor’s file tree starts here, your terminal commands usually run from here, and relative paths in your code are resolved from here. “Where is the root?” is one of the first questions to answer whenever you open a project; if the answer is unclear, open the editor on the wrong folder and half of your search and navigation commands will silently miss things that live outside the opened folder.

## 12.4 Simple scripting workflows in an editor (novice level)

### The write-run-read-repeat loop

Most of what you do in an editor for the first year of coursework is the same tight loop, repeated hundreds of times a day:

1.  Write or change a small piece of code (usually 10–50 lines).
2.  Run it from an integrated terminal, side-by-side with the editor.
3.  Read the output — especially any error message — carefully, without skimming.
4.  Jump straight to the file and line the error mentions.
5.  Make **one** change, save, and re-run.

The discipline that matters here is step 5: *one change at a time*. When something breaks, every student’s instinct is to change three things at once — “maybe it’s the import, maybe it’s the type, maybe it’s the path” — and re-run, hoping one of them works. This is the fastest known way to create new bugs while pretending to fix the old ones. If the first change does not fix the problem, undo it, think again, and try a different single change. Slow is fast; a minute of “did I actually change only what I intended?” beats an hour of backing out a tangled attempted-fix.

Keep the integrated terminal visible while you work. In VS Code, `Ctrl+~` (or \`Ctrl+\`\` on US keyboards) opens a terminal docked at the bottom of the window, so the edit-run gap is under a second:

``` bash
$ python analyze.py
Traceback (most recent call last):
  File "analyze.py", line 12, in <module>
    df = pd.read_csv("data/raw/sales.csv")
FileNotFoundError: [Errno 2] No such file or directory: 'data/raw/sales.csv'
```

The error tells you exactly which line and exactly what the problem is. `Cmd`-click (or `Ctrl`-click) the file path in the traceback and VS Code jumps to `analyze.py` line 12. Fix one thing (maybe you forgot to download the data, or the file is in `data/processed/` instead), save, and rerun. The goal of the integrated terminal is to make this cycle so fast that “try it and see” becomes a cheap question.

### Editor features that help beginners

Modern GUI editors quietly do a lot of the work that beginners used to have to do by hand. Four of them are worth knowing by name so you can turn them on and rely on them:

- **Syntax highlighting and bracket matching.** Keywords, strings, and comments are each colored differently, and when your cursor touches a bracket, the editor highlights its match. If you type an open paren and the editor does *not* highlight a matching close paren anywhere, you know you have an unbalanced expression before you even run the code.
- **Auto-indentation and format-on-save.** Press Enter inside a Python `def` and the editor indents the next line for you. Save a file and a formatter like `black` can normalize the whitespace automatically, so you never have to argue with yourself about where to put a comma or a space. See [sec-linting](#sec-linting).
- **Linting messages as early warnings.** A linter runs as you type and underlines problems it finds — undefined variable, unused import, wrong number of arguments. Treat the squiggly underlines as a draft of the error messages you would have gotten at runtime, but delivered five seconds sooner.
- **Inline documentation and jump-to-definition.** Hover over a function name and a tooltip shows its signature and docstring. Press `F12` on a function call and the editor jumps to where that function is defined. These two features turn “I wonder what this does” from a fifteen-minute side quest into a two-second lookup.

None of these features are magic; they are all things you could do by hand. But each one removes a small source of friction, and the compound effect across a semester is enormous.

### When a full debugger helps

Most small bugs are fastest to find with `print()` statements: drop a line that prints the variable you suspect, re-run, and read the output. A full debugger is worth reaching for when `print` becomes awkward — you need to inspect a complicated nested data structure, step through a loop one iteration at a time, or see the state of several variables at once at a specific point in execution.

The minimum debugger vocabulary is small. A **breakpoint** is a marker on a line that tells Python to stop *before* executing that line and hand control back to you. “Step over” runs the current line and moves to the next one. “Step into” dives inside a function call to see what it does. “Variable inspection” shows you the current value of every variable in the current scope. In VS Code, click the gutter to the left of a line number to set a breakpoint, press `F5` to run the file in the debugger, and use the debug panel to step through code and watch variables change.

Do not feel obligated to learn a debugger on day one. Plenty of professional data scientists go entire projects with just `print` and tests. Reach for the debugger when `print`-debugging has stopped feeling fast, not before.

## 12.5 Debugging files (common student failure modes)

### Wrong file, wrong place

The most disorienting editor failure is when your edits seem to have no effect — you save, you rerun, and the program behaves as if you changed nothing. The cause is almost always one of two things: you edited a *different copy* of the file from the one your code is actually loading, or you ran the code from a directory where the file you edited does not live. Both are failures of “where am I” awareness rather than failures of the editor. The fix is to confirm your working directory (`pwd`), search the project for any duplicate filenames so you know which copy you are looking at, and — as a temporary diagnostic — switch to absolute paths in the failing code so the question of “which file?” is unambiguous. Once the bug is found, you can usually go back to relative paths.

### Wrong extension or hidden extension

A file that opens in the wrong program, or that “isn’t a Python file” even though you saved it as Python, is almost always a victim of a hidden or wrong extension. The classic version: you save `script.py` in an editor that adds `.txt` for you, end up with `script.py.txt`, and your file manager’s “hide extensions” setting makes it look identical to a real `script.py`. The fix is to turn on **show file extensions** in your file manager (see [sec-filesystem](#sec-filesystem)) and to look at the actual filename in your editor’s title bar, which always shows the truth.

### Encoding and invisible characters

When you see weird symbols (`â€™` where a curly apostrophe should be, or boxes where letters should be), parser errors that mention “invalid character,” or sudden Python `SyntaxError`s on lines that look fine, the cause is almost always an encoding mismatch or an invisible character. The fix is to re-save the file explicitly as UTF-8 (every modern editor has a “Save with Encoding” or similar option), and to turn on visible whitespace so non-printing characters become visible. A common culprit is a non-breaking space (`U+00A0`) that crept in from a copy-paste — it looks like a space but Python treats it as something else entirely.

### Line endings (Windows/macOS collaboration)

When a project is shared between Windows and macOS or Linux developers, you can hit a class of bugs that show up as scripts failing with strange “command not found” errors, diffs that look enormous because every line “changed,” or tools complaining about CRLF vs LF. The cause is the line-ending convention: Windows uses `\r\n` and Unix systems use `\n`, and tools that expect one and find the other will misbehave. The fix is to configure your editor to use a consistent style (LF is the cross-platform-friendly default), and to let Git normalize line endings on commit if your repository has a `.gitattributes` file — most well-set-up repositories do.

### Config files and indentation-sensitive formats

YAML, Python, and Makefiles all care about the difference between tabs and spaces, and YAML in particular breaks in subtle ways when you mix them. The symptom is usually a parser error pointing at a line that looks correct to your eyes. The fix is to turn on visible whitespace so you can *see* whether a line is using tabs or spaces, and to validate the file with the tool that reads it — `python -c "import yaml; yaml.safe_load(open('config.yml'))"` will tell you immediately whether your YAML is parseable.

## 12.6 Terminal editors: survival skills

You do not need to become fluent in a terminal editor. You do need to know enough to open a file, change one line, and save and exit without calling a friend — because sooner or later you will SSH into a server and discover that a terminal editor is the only tool available. This section covers the minimum for each of the three most common terminal editors.

### `nano` essentials (minimum viable)

`nano` is the friendliest terminal editor. It prints its common keystrokes at the bottom of the screen, uses arrow keys for navigation, and behaves mostly like a GUI editor’s no-frills cousin. If you only learn one terminal editor, make it this one.

``` bash
nano config.conf       # open (or create) config.conf
# ...arrow keys to navigate, type to edit...
# Ctrl+O   write out (save); nano prompts for confirmation, press Enter
# Ctrl+X   exit nano (if unsaved changes, it will ask first)
# Ctrl+W   where is (search); type the text and press Enter
# Ctrl+\   replace; type search text, then replacement text
# Ctrl+_   go to line number
```

The `^` character in the on-screen help means “Control key,” so `^X` is `Ctrl+X`. That is the entire confusing-to-newcomers notation. Practice the open-save-exit sequence once on a throwaway file, and `nano` stops being scary forever.

### `vim` essentials (minimum viable)

`vim` is the editor that terrifies new users because it starts in **normal mode** — a mode where typing letters does *not* insert them into the file, but instead runs commands. This is the source of every “how do I exit vim?” meme. The survival rules are simple:

- `vim file.txt` opens the file in normal mode.
- Press `i` to enter **insert mode**; now typing works the way you expect.
- Press `Esc` to return to **normal mode** from anywhere.
- In normal mode, `:w` writes (saves), `:q` quits, and `:wq` does both.
- If you panic and want to throw away your changes, type `:q!` to quit without saving.

That is enough to edit a file. A couple more commands will cover almost every emergency:

``` text
/pattern<Enter>      search forward for "pattern"
n                    jump to next match
:%s/old/new/gc       replace "old" with "new" everywhere, with confirmation for each match
:42                  jump to line 42
u                    undo last change (in normal mode)
Ctrl+r               redo
```

Why do people love `vim` despite the learning curve? In normal mode, keystrokes compose like grammar: `d` means “delete,” `w` means “word,” so `dw` means “delete word.” `3dw` deletes three words. `ci"` means “change inside double quotes” — it deletes the text between the next pair of quotes and drops you into insert mode to type the replacement. For users who live in terminals, this compositional model is genuinely faster than using a mouse. You do not need to learn any of it to survive `vim`; but if you find yourself in a terminal all day, it is worth investing a week.

### `emacs` essentials (minimum viable)

`emacs` is `vim`’s philosophical opposite: instead of modes, it uses long `Ctrl`- and `Alt`-based key chords. The survival set is:

``` text
emacs file.txt       open file.txt (or start emacs and then Ctrl+x Ctrl+f)
Ctrl+x Ctrl+s        save
Ctrl+x Ctrl+c        exit
Ctrl+s               incremental search forward
Ctrl+x b             switch buffer (between open files)
Ctrl+x Ctrl+f        open another file
Ctrl+g               cancel current operation (if you get stuck mid-command)
```

The Emacs notation is `C-x C-s` for “hold Ctrl, press x, release, hold Ctrl, press s.” Most tutorials use that form. As with `vim`, you do not need to be an Emacs power user; you need to be able to edit and save a file without panic.

## 12.7 GUI editors: practical configuration (keep it minimal)

Most GUI editors ship with hundreds of settings and thousands of available extensions. The temptation is to configure extensively; the right move is to configure *minimally*. A lightly configured editor is easier to reproduce on a new machine, easier to explain to a collaborator, and much less likely to break in confusing ways after an update.

### The minimal settings that matter

Four settings genuinely earn their keep. The rest you can add later if you discover you want them.

**Indentation and visible whitespace.** Set your default indentation to match your project conventions (four spaces for Python) and enable visible whitespace so you can see tabs and trailing spaces at a glance. In VS Code, that looks like this in `settings.json`:

``` json
{
  "editor.tabSize": 4,
  "editor.insertSpaces": true,
  "editor.renderWhitespace": "all",
  "files.trimTrailingWhitespace": true,
  "files.insertFinalNewline": true
}
```

The last two lines (trim trailing whitespace on save, end files with a newline) fix two categories of “why is my diff noisy?” problems before they ever happen.

**Format on save.** Install a formatter appropriate to the language — `black` or `ruff format` for Python, `prettier` for web files — and turn on “Format On Save.” The formatter rewrites the file to a consistent style every time you save, so you never have to think about spacing, quote style, or line length again. See [sec-linting](#sec-linting) for the fuller discussion.

``` json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "ms-python.black-formatter"
  }
}
```

**A linter for early feedback.** A linter marks problems with squiggly underlines as you type. For Python, `ruff` is the current community favorite — fast, opinionated, and nearly zero-config. Install its VS Code extension and you will get error feedback without running your code.

**An integrated terminal.** Not strictly a “setting” but worth emphasizing: use the editor’s built-in terminal rather than a separate terminal window. It runs in the same working directory as your project, stays docked next to your code, and makes the write-run-read loop fast. In VS Code, `` Ctrl+` `` toggles it.

### Extensions and plugins: a controlled approach

Every GUI editor has a plugin ecosystem, and every plugin ecosystem will happily sell you productivity you do not need. The rule to follow is: **install only what you can explain.** If you cannot say in one sentence why an extension is installed and what it does, uninstall it. Extensions are not free — they consume memory, slow down startup, occasionally interact badly with each other, and sometimes (rarely, but sometimes) introduce security issues.

Prefer extensions that are widely used and actively maintained. In VS Code, the marketplace shows install counts and “last updated” dates; anything under a few thousand installs or not updated in over a year deserves extra scrutiny. Avoid installing two extensions that do the same thing — two linters for the same language, two formatters, two Git UIs — because they will fight each other in ways that waste your time.

For a typical Python data student, a reasonable starting set is: Python (Microsoft), Ruff, Jupyter, GitLens (optional), and a Quarto extension if you are writing Quarto documents. That is enough. You can add more as specific needs arise, but you do not need to start a project with a dozen extensions installed.

Record your essentials somewhere — even just in a `README` section titled “Recommended extensions” — so a collaborator or a future-you on a new laptop can reproduce the setup quickly.

### Workspace settings vs global settings

Most editors distinguish between **global (user) settings**, which apply everywhere you open the editor, and **workspace (project) settings**, which only apply inside a specific folder. The rule is: keep global settings minimal and put project-specific behavior in workspace settings. In VS Code, workspace settings live in `.vscode/settings.json` inside the project root, and you can commit that file to version control so everyone working on the project gets the same behavior.

``` json
// .vscode/settings.json — committed to the repo
{
  "python.defaultInterpreterPath": "./.venv/bin/python",
  "editor.formatOnSave": true,
  "editor.rulers": [88]
}
```

This particular file tells VS Code to use the project’s own virtual environment as the Python interpreter, to format files on save, and to draw a vertical ruler at column 88 (the `black` default). It does not say anything about your personal color theme or font size — those belong in your global settings, where they do not affect collaborators. Keeping global settings light is what makes your setup portable: when you borrow a friend’s laptop for half an hour, you can install VS Code, open the project, and be productive in a few minutes.

## 12.8 IDEs: fundamentals without overwhelm

A full IDE — IntelliJ, PyCharm, Visual Studio, Xcode, RStudio — is a heavier tool than a GUI code editor. It is worth understanding IDEs at a conceptual level even if you do not use one day-to-day, because eventually a course or a job will put you in front of one.

### The project model

The biggest conceptual shift from a simple editor to an IDE is the **project model**. A GUI editor like VS Code treats “the project” as whatever folder you opened — the editor does not really care what is in it, and it reads files off disk when you ask. An IDE, in contrast, builds and maintains its own model of the project: what source files belong to it, how they depend on each other, which Python interpreter or JDK to use, which files are generated artifacts vs. hand-written source, and how to run the project from scratch. This model lives in hidden files inside the project (for example, `.idea/` for IntelliJ/PyCharm, `.Rproj` for RStudio, `.xcodeproj` for Xcode), and the IDE re-indexes the project whenever it detects a change.

The upside is that the IDE can offer features a dumb editor cannot: precise “find all usages,” safe rename-across-project, automatic import insertion, type-aware autocomplete, and so on. The downside is that the project model can drift out of sync with reality — you add a file outside the IDE, or you change a dependency, or a setting gets corrupted, and suddenly the IDE is showing errors that do not exist or missing files that do.

Two survival skills matter here. First, learn where your IDE stores its project settings and *do not edit those files by hand* unless you know what you are doing. Second, learn how to trigger a reset or reimport — “File → Invalidate Caches / Restart” in IntelliJ, “File → Reload Project” in many others — so that when the project model goes sideways you can get back to a clean state without deleting the whole project.

### Refactoring and code navigation

IDE refactoring tools are the main reason some developers refuse to work without one. A rename refactor, done right, updates every reference to a symbol across the entire project — imports, function calls, type annotations, even docstrings — in a single atomic operation. An “extract method” refactor lifts a block of code into a new function and replaces the original block with a call to it. “Inline” does the opposite.

These tools are powerful and they can still go wrong. Refactors that cross module boundaries or touch dynamic code (reflection, string-based attribute access, plugin loading) can miss references or update things they should not. The habit to build is: **treat every refactor as a change that needs to be verified.** Run your tests immediately afterward. If you do not have tests, run the program end-to-end on a representative example. Commit before the refactor so that if something broke in a way you cannot see, you can roll back cleanly.

Code navigation in an IDE is the same story as in a GUI editor, just more precise: “go to definition” jumps to the declaration, “find usages” lists every call site, and “go to symbol” lets you jump to any function or class in the project by name. Learn the keyboard shortcuts for these three commands in whichever IDE you use — they will become some of the keys you press most often.

### Debugging integration

IDE debuggers are where the tool really shines. Setting a breakpoint is a single click in the gutter next to the line number. Running the file in debug mode pauses execution at the breakpoint, drops you into an interactive view of every variable in scope, and lets you step through the code one line at a time:

``` text
Run → Debug  (or F5 in most IDEs)

[step over]  execute current line, move to the next line in the same function
[step into]  execute current line, diving into any function call
[step out]   run to the end of the current function and return to the caller
[continue]   run until the next breakpoint (or end of program)
```

A watch panel shows the values of variables you want to keep an eye on. A call stack panel shows the chain of function calls that led to the current line. Most IDEs also let you change a variable’s value during a paused run, which is enormously useful when you want to test “what if this list were empty here?” without re-running from the start.

As with the GUI-editor debugger, you do not have to learn this on day one. Many students go through an entire intro sequence on `print`-debugging and tests alone, and that is fine. But when you hit the bug where you need to understand the state of a complicated object at a specific iteration of a loop, the debugger will save you hours and you should know it is there.

## 12.9 Best practices: habits that prevent pain

The habits in this section are cheap to build and expensive to learn the hard way.

### Pick a primary editor and a fallback

Your **primary editor** is the one you live in day-to-day: a GUI editor for most students, an IDE if a course requires one. Commit to it. Learn its keyboard shortcuts, its search commands, its formatting settings. Editor fluency compounds — every week you spend in the same tool makes you faster in it forever, and jumping between editors constantly keeps you at beginner speed everywhere.

Your **fallback editor** is for when you cannot use your primary. That almost always means “I’m SSH’d into a server and need to change one file.” For this, learn just enough `nano` to open a file, edit it, save, and exit. Optionally learn just enough `vim` that if a server has `vim` but not `nano` you are not stranded. This is genuinely a ten-minute skill — practice it once and then occasionally refresh it, and you will always have a way to edit files on any machine you can reach.

``` bash
# On any Unix machine you log into:
which nano    # is nano installed?
which vim     # is vim installed?
# whichever is present, you should know the basics of
```

### Treat find/replace as a power tool

The find/replace protocol from earlier in this chapter deserves to be a habit, not a one-time lesson. Every large replace follows the same sequence:

1.  **Narrow scope.** Default to “in the current file” unless you explicitly need “in the entire workspace.” When you do go workspace-wide, look at the list of matching files first — you may discover the scope is different from what you expected.
2.  **Preview changes.** Use “Replace with confirmation” or step through matches one at a time. Never trust a one-shot global replace for anything important.
3.  **Commit first.** Before a large replace, make sure your working tree is clean and that the last change you made is committed. If the replace goes wrong, `git checkout .` restores the files instantly and you lose nothing.
4.  **Verify after.** Run the tests, or re-run the script, or at minimum open a few of the edited files and glance at the diffs. A replace that compiled and ran successfully can still be semantically wrong in ways the compiler cannot see.

The rule is: the blast radius of find/replace should always be matched by the strength of the safety net.

### Keep text files boring

A “boring” text file is one that all your tools agree about. That means **UTF-8 encoded** (most modern editors default to UTF-8, but it is worth confirming in your settings); **Unix line endings (LF)** unless you have a specific reason to use CRLF; and **no trailing whitespace or stray tabs**. Configure your editor to enforce all three on save, and most cross-platform collaboration headaches disappear before they happen.

Avoid editing **generated files** by hand. If a file has a banner at the top that says `# This file was automatically generated by ...` or `# DO NOT EDIT`, take it seriously — your change will be overwritten the next time the generator runs, and in the meantime the file will be inconsistent with its source. The right move is to find and edit the *source* (a template, a schema, a script), then re-run the generator.

Prefer putting configuration in version control rather than leaving it on individual laptops. Editor settings in `.vscode/settings.json`, linting rules in `pyproject.toml` or `.ruff.toml`, and formatting rules in the same place mean everyone on the project gets the same behavior and nobody has to debug “but it works on my machine.”

### Use version control as an editor safety net

Version control is your backstop. When a risky edit is about to happen, commit first. When an experiment works, commit. When an experiment fails, `git diff` to see what you changed, `git checkout <file>` to throw away unwanted changes, or `git stash` to set changes aside temporarily while you try something else.

``` bash
# Before a risky refactor:
git status                      # are my working changes clean?
git commit -am "before refactor"

# Do the refactor in the editor. If it went wrong:
git diff                        # what did I actually change?
git checkout .                  # throw everything away; back to the commit
```

The habit to build: **commit small, commit often, and commit before anything that scares you.** Commits are cheap, and the safety they provide is enormous. See [sec-git-github](#sec-git-github) for the mechanics and [sec-project-management](#sec-project-management) for how commit hygiene fits into broader project discipline.

## 12.10 Stakes and politics

Editors look like the most neutral tool in the kit, but the editor industry has consolidated dramatically in the last decade and the consequences are worth seeing. Visual Studio Code, the dominant editor for new programmers, is a Microsoft product; it ships with telemetry enabled by default, its Python extension is published by Microsoft, and the same company owns GitHub and a substantial stake in OpenAI. None of that makes VS Code a bad editor — it is, by most measures, an excellent one — but the situation in which the default editor, the default code host, and the default AI coding assistant are all owned by a single company is new, and it concentrates an unusual amount of influence over how programming gets taught and learned. The community fork VSCodium exists precisely because some users want the editor without the telemetry and proprietary marketplace.

A second, sharper concern: editor extensions are code that runs with full access to your filesystem and your network. Installing a popular-looking extension from an unfamiliar publisher is the same shape of decision as installing a random binary from the internet, and the major extension marketplaces have repeatedly hosted malicious or compromised packages.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: when you choose an editor and its extensions, ask whose code is now running every time you open a file, and what defaults you have inherited without choosing.

## 12.11 Worked examples

### Writing and running a tiny script

The simplest possible loop: write a small Python script in your editor, run it from the integrated terminal, and fix the first error you hit. Open VS Code (or your editor of choice) in your project folder, create a new file called `hello.py`, and type:

``` python
def greet(name):
    print(f"hello, {name}!"

greet("world")
```

(Yes, the missing closing parenthesis on the `print` call is intentional.) Save the file and open the integrated terminal (``` Ctrl+\`` in VS Code, or ```View → Terminal\`). Run it:

``` bash
$ python hello.py
  File "hello.py", line 3
    greet("world")
    ^^^^^
SyntaxError: '(' was never closed
```

The error message points at line 3, but it says “‘(’ was never closed” — Python is telling you that an open parenthesis somewhere *before* line 3 was never matched. Click on the file in your editor and look at line 2: there is the missing `)`. Add it, save, and rerun:

``` bash
$ python hello.py
hello, world!
```

That is the entire write-run-read-fix loop. It will run thousands of times over the course of your degree, and the editor’s job is to make each iteration as fast as possible.

### Debugging a broken config file

A teammate sends you a `config.yml` and says “Quarto won’t load it.” You open it and it looks fine to your eyes. The problem is almost always invisible whitespace. Turn on visible whitespace in your editor (`View → Render Whitespace` in VS Code) and look again — now you can see whether each indentation step is a tab or a space. YAML requires spaces, and a single tab character can break the entire file. Fix the offending tabs by replacing them with the same number of spaces, save, and validate from the terminal:

``` bash
python -c "import yaml; yaml.safe_load(open('config.yml'))"
```

If the command produces no output, the YAML now parses. If it raises a `YAMLError`, the message will name the line and column of the next problem. Repeat until clean.

### A safe find/replace across a project

You decide to rename a function from `compute_mean` to `weighted_mean` everywhere in your project. The unsafe version is to use a one-shot global replace and hope. The safe version is three steps. First, search for the old name across the project (`Cmd+Shift+F` in VS Code) and look at every match — confirm that they all really are references to the function, not, say, a variable named `compute_mean_squared`. Second, replace with confirmation: VS Code’s search panel has a “Replace” button on each individual match, so you can step through them one at a time. Third, run your tests immediately afterward:

``` bash
pytest tests/ -q
```

If anything broke, the tests catch it while the change is still small enough to undo. The whole protocol takes longer than a one-shot replace by maybe a minute, and it has saved many people from very long days.

### A remote emergency edit over SSH

You SSH into a server and discover that one config file has a wrong value that is keeping a service from starting. You do not have time to set up a full remote-development workflow. The minimal sequence is:

``` bash
ssh you@server
nano /etc/myservice/config.conf
# arrow keys to navigate; type the change; Ctrl+O to save; Ctrl+X to exit
sudo systemctl restart myservice
exit
```

The whole interaction is under a minute if you know the basic `nano` keystrokes. The reason the chapter recommended learning `nano` for emergencies is exactly this scenario: you want a tool that is already installed on every Unix box you might log into and that you can drive without a tutorial open in front of you.

## 12.12 Templates

### Template A: Editor setup checklist (first week)

    Editor:

    * Installed and updated
    * Default indentation configured
    * Visible whitespace toggle known
    * Format-on-save configured (if course uses it)
    * Linter installed (if course uses it)
    * Integrated terminal enabled
      Fallback editor:
    * nano basics practiced (open/save/exit/search)

### Template B: Safe find/replace protocol

    1. Search (no replace) and inspect matches
    2. Narrow scope (file/selection/project)
    3. Replace with confirmation
    4. Save and review diff
    5. Run tests or rerun script
    6. Commit with a message describing the change

## 12.13 Exercises

1.  Configure your editor to show line numbers and visible whitespace; explain what you changed.

2.  Write a short script and fix two intentional errors using editor cues.

3.  Perform a multi-file search in a small project; report where a function name appears.

4.  Run a safe find/replace with confirmation and verify by running tests.

5.  Open and edit a file in nano; save and exit confidently.

6.  Optional: learn a minimal vim workflow (insert, save, quit, search).

## 12.14 One-page checklist

- I can open, save, and locate files reliably.

- I can use find/replace safely, including across multiple files.

- I can debug common file issues (paths, extensions, encoding, line endings).

- I understand when to use terminal editors vs GUI editors vs IDEs.

- My editor is minimally configured (indentation, formatting, linting).

- I use version control to review and recover from editing mistakes.

- I have a fallback editor skill for remote/emergency use.

## 12.15 Quick reference: terminal editor survival commands (optional handout)

### nano

- Open: `nano file`

- Save: (document the keystroke)

- Exit: (document the keystroke)

- Find/replace: (document the keystroke)

### vim

## 12.16 Quick reference: GUI/IDE search

- Find in file, replace in file

- Find in workspace, replace in workspace

- Go to line, go to file, go to definition

> **NOTE:**
>
> - Microsoft, [VS Code documentation](https://code.visualstudio.com/docs) — the official guide, including the Python extension walk-through.
> - Microsoft, [VS Code Python tutorial](https://code.visualstudio.com/docs/python/python-tutorial) — a focused introduction to running and debugging Python in VS Code.
> - [VSCodium](https://vscodium.com/) — the community-maintained build of VS Code without Microsoft’s telemetry and proprietary marketplace; useful when you want the editor and the freedoms separately.
> - Drew Neil, [*Practical Vim*](https://pragprog.com/titles/dnvim2/practical-vim-second-edition/) — the standard book for learning Vim well; pairs nicely with the built-in `vimtutor` for hands-on practice.
> - GNU, [Emacs Tutorial](https://www.gnu.org/software/emacs/tour/) — an interactive tour of Emacs, the other long-lived editor tradition; worth a half-hour even if you never adopt it, just to see the alternative model.
> - nano, [Cheat sheet](https://www.nano-editor.org/dist/latest/cheatsheet.html) — every keystroke you need for quick edits over SSH.
> - JetBrains, [PyCharm documentation](https://www.jetbrains.com/help/pycharm/) — if you outgrow VS Code’s built-in Python features, PyCharm is the canonical Python IDE; its educational edition is free for students.
