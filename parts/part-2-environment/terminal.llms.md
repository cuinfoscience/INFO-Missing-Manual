# 11  Command Line

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-os-management](#sec-os-management), [sec-filesystem](#sec-filesystem).
>
> **See also:** [sec-text-editors](#sec-text-editors), [sec-git-github](#sec-git-github), [sec-automation](#sec-automation).

## Purpose

![What Year Is It? Meme: First Time Opening Terminal, What Year Is It?](../../graphics/memes/terminal.png)

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

## Running theme: see before you act

The shell trades safety for speed: a single command can move, overwrite, or delete more work than an afternoon of clicking. Almost every command-line disaster is one keystroke away from being prevented by a `pwd`, an `ls`, or a dry-run preview before the destructive command runs.

## 11.1 A beginner mental model

The first piece of vocabulary worth getting right is the difference between a **terminal** and a **shell**, because the words are often used interchangeably and the distinction matters when you read documentation. The **terminal** is the application window you type in — Terminal.app on macOS, [Windows Terminal](https://learn.microsoft.com/en-us/windows/terminal/) or [PowerShell](https://learn.microsoft.com/en-us/powershell/) on Windows, GNOME Terminal or Konsole on Linux. The **shell** is the program running *inside* that window — usually [`bash`](https://www.gnu.org/software/bash/manual/) or [`zsh`](https://zsh.sourceforge.io/Doc/) on macOS and Linux, `pwsh` (PowerShell) or `cmd.exe` on Windows. The terminal is the dumb pipe that handles fonts and key presses; the shell is the smart program that interprets what you type. A **command** is the actual thing you ask the shell to run: a program name followed by some arguments, like `ls -l data/`.

When you press Enter on a command line, a small choreographed sequence happens. The shell reads the line of text you typed. It expands any shortcuts you used — globs like `*.csv`, variables like `$HOME`, command substitutions like `$(date)`. It searches a list of folders called `PATH` to find the program you named. It launches that program as a new process, hands it the arguments you provided, and shows you whatever the program prints. When the program finishes, it returns a small integer called an **exit code** — `0` conventionally means “everything worked,” and any nonzero value means “something went wrong.” The shell then displays a prompt and waits for your next command.

``` bash
$ ls -l data/             # 1. read the line
                           # 2. expand any shortcuts (none here)
                           # 3. find 'ls' on PATH
                           # 4. run it with the argument 'data/'
                           # 5. print output, return exit code 0
total 16
-rw-r--r-- 1 you staff 8421 Apr 10 12:34 input.csv
$ echo $?                  # check the exit code of the previous command
0
```

![](graphics/PLACEHOLDER-macos-terminal-annotated.png)

Figure 11.1: ALT: macOS Terminal window at a fresh prompt, annotated to label the username, hostname, current directory, and prompt character. The window shows an `ls -l data/` command at the top and its output underneath.

![](graphics/PLACEHOLDER-windows-terminal-annotated.png)

Figure 11.2: ALT: Windows Terminal with a PowerShell tab open, annotated to label the equivalent parts: current directory, prompt symbol, and command-line input area.

The reason any of this is worth learning, when GUI file managers are right there, is that the command line gives you four things the GUI cannot. It has a high **action-to-keystroke ratio** for repetitive work — moving fifty files into the right folders is one short command at the prompt and a fifteen-minute drag-and-drop session in the GUI. It is **composable**: small focused tools combined with pipes and redirection give you a flexible toolkit instead of fifty single-purpose buttons. It is **automatable**: anything you can type once, you can save in a script and run again on a schedule. And it is **remote-friendly**, which is the entire reason you can do real work on a server you have never physically seen (see [sec-remote-computing](#sec-remote-computing)). None of those properties are nice-to-haves; they are the difference between doing a job once and doing it reliably for an entire semester.

## 11.2 Orientation and safety first

The single most useful habit at the command line is to always know where you are. Three commands give you the answer at any time: `pwd` prints your current working directory, `ls` lists the contents of that directory, and `cd` changes you to a different one. Before you do anything that touches files, run `pwd` and `ls` so you can confirm the world is what you think it is.

``` bash
$ pwd
/Users/you/Courses/INFO-3010/Project
$ ls
README.md   data/   notebooks/   src/
$ cd data
$ pwd
/Users/you/Courses/INFO-3010/Project/data
```

The mindset that prevents most beginner disasters is what experienced users call **guardrails first**. When you are not sure what a command is going to do, prefer the read-only commands (`pwd`, `ls`, `cat`, `head`, `wc`, `file`) before you reach for anything that modifies the filesystem. When you are about to do something destructive like delete or move files, do a dry run first by listing the targets so you can see exactly what is about to be affected. When you can copy instead of move, copy. When you can move instead of delete, move. Each of these habits costs nothing and protects you from the small number of irreversible mistakes that account for almost all command-line tragedies.

``` bash
# Dry run before destructive action: list, then act
$ ls *.tmp                 # see exactly what *.tmp expands to
file1.tmp  file2.tmp  notes.tmp
$ rm *.tmp                 # only after the listing looked right
```

The mistakes worth being paranoid about are a short list. The first is **deleting the wrong directory**, especially with `rm -rf`, which removes everything underneath a directory and gives you no chance to take it back. The second is **running a command in the wrong directory** — most often a destructive one — because you forgot to `cd` first. The third is **overwriting a file with output redirection**: `python script.py > results.csv` will silently obliterate any existing `results.csv`, with no prompt and no undo. And the fourth is **reflexive `sudo`**, where you use elevated privileges to “fix” a permission problem you do not yet understand. Each of these has cost real students real assignments. Build the habit of pausing for one extra second before any of them, and the disasters never happen.

## 11.3 Command anatomy and help

### Basic syntax

Nearly every Unix-like command follows the same three-part shape, and internalizing it once makes every new tool feel familiar:

``` bash
command [options] [arguments]
```

The **command** is the name of the program. **Options** (also called flags or switches) modify how the command behaves — whether it is quiet or verbose, whether it is recursive, which output format to use. **Arguments** are the things the command acts on, usually filenames or paths. Most commands accept zero or more of each, and the order is usually: command first, then options, then arguments. So `ls -la ~/Courses` says “run `ls`, with options `-l` and `-a`, on the target `~/Courses`.”

The reason this shape is worth memorizing is that every error message and every help page uses the same vocabulary. When a tool says `usage: ls [OPTION]... [FILE]...`, it is telling you where options go, where file arguments go, and that both are repeatable. Once you can read that line, you can pick up a brand-new command from its man page in under a minute.

### Flags and options

Options come in two styles, and almost every modern tool accepts both. **Short flags** are a single dash followed by one letter: `ls -l`, `grep -i`, `rm -r`. Short flags can almost always be combined into one token — `ls -l -a -h` is the same as `ls -lah` — which is where most of the terse-looking commands you see in documentation come from. **Long flags** are two dashes followed by a word: `ls --all`, `grep --ignore-case`, `rm --recursive`. Long flags take more typing but are self-documenting, which makes them the right choice in scripts and tutorials where someone else (or future you) will read the code.

``` bash
ls -l             # short flag: long listing
ls --all          # long flag: include hidden files
ls -lah           # three short flags combined
```

Some options take a **value**. For short flags, the value usually follows after a space: `grep -o output.txt` (the `-o` flag with an `output.txt` argument). For long flags, the convention is to join them with an equals sign: `grep --output=output.txt`. A few tools accept both forms for both styles; when in doubt, the `--help` output tells you.

``` bash
curl -o page.html https://example.com
curl --output page.html https://example.com
tar --file=archive.tar.gz --extract    # equals form
```

The single most useful habit when you hit an unfamiliar command is to try its help flag *before* you try to use it. `command --help` prints a short usage summary on stdout for nearly every modern tool, and it is often the fastest way to answer “what does this flag do?”

### Built-in help

Every Unix system ships with two help mechanisms, and the instinct worth building is to reach for them before you reach for a web search.

``` bash
ls --help          # quick summary, usually one screen
man ls             # full manual page
```

The `--help` flag is the fast version: it usually prints a one-screen summary with the usage line, a list of options, and sometimes a few examples. It is the right first stop for “I know this command, I just forgot the flag I need.” The `man` (manual) command is the full reference: it opens a multi-page document in a pager, with sections for synopsis, description, options, and examples. You navigate it like `less` — arrow keys to scroll, `/pattern` to search, `q` to quit. Man pages can look dense, but they follow a reliable order, and once you know where to look, you can extract what you need quickly.

The discipline for reading a man page under time pressure is **skim, don’t read**. Go to `SYNOPSIS` first — that is the one-line usage pattern showing which options and arguments are available. Then skip to `OPTIONS` and search (`/flag_name`) for the specific flag you care about. Only if that fails should you look at `DESCRIPTION`. Many man pages end with an `EXAMPLES` section, which is often the fastest way to see what a realistic invocation looks like — jump there directly when you are stuck on “how do I use this at all?”

``` bash
# Fast workflow for an unfamiliar command
$ tar --help | head -20      # quick summary
$ man tar                     # open the manual
  /-x                         # jump to the -x option
  /EXAMPLES                   # jump to the examples section
  q                           # quit
```

### Quoting and spaces

Spaces in a command line are not cosmetic — they are how the shell decides where one argument ends and the next begins. `rm my file.txt` is a request to delete *two* files, one called `my` and one called `file.txt`, not a single file called `my file.txt`. To pass a single argument that contains a space, you have to tell the shell to treat the whole thing as one token by wrapping it in quotes:

``` bash
rm my file.txt         # WRONG: tries to delete two files
rm "my file.txt"       # RIGHT: single filename with a space
rm 'my file.txt'       # also right: single quotes work too
```

Single quotes and double quotes are almost interchangeable for the simple case, but they differ in one important way: **double quotes let the shell expand certain special constructs inside them; single quotes do not.** Variable references like `$HOME`, command substitutions like `$(date)`, and backtick expressions all expand inside double quotes and are left as literal text inside single quotes.

``` bash
$ NAME=Alice
$ echo "Hello, $NAME"
Hello, Alice
$ echo 'Hello, $NAME'
Hello, $NAME
```

The rule of thumb to take away is: **quote variables and paths by default**, and use double quotes unless you specifically need the “no expansion” behavior of single quotes. The most common bug that comes from forgetting this is a variable that is empty or unset — `rm $TARGET_DIR/*` turns into `rm /*` if `$TARGET_DIR` is empty, which is the kind of afternoon nobody wants. `rm "$TARGET_DIR"/*` at least fails loudly instead of silently destroying things.

## 11.4 File system navigation

A handful of single characters carry most of the load in command-line paths, and learning them is the difference between fluent and stuck. The forward slash `/` at the start of a path is the **root directory** — the very top of your filesystem. The tilde `~` is shorthand for **your home directory** (`/Users/you` on macOS, `/home/you` on Linux). A single dot `.` means **the current directory**, and two dots `..` mean **the parent directory**, one level up. With these, you can build any path you need:

``` bash
~/Courses/INFO-3010/Project/data/input.csv   # absolute, from your home
./data/input.csv                              # relative, from cwd
../data/input.csv                             # one folder up, then into data/
/Users/you/Documents                          # absolute, from filesystem root
```

Absolute paths always work no matter where you are; relative paths depend on your current directory. ([sec-filesystem](#sec-filesystem) covers the broader file-system mental model in depth.)

The three workhorse navigation commands are `pwd`, `ls`, and `cd`. You already know `pwd` prints your current location. `ls` lists the contents of a directory, and a few flags make it dramatically more useful: `-l` shows the long format (permissions, owner, size, date), `-a` includes hidden files (those starting with a dot), and `-h` makes file sizes human-readable. Combine them: `ls -lah` is the listing you want when you are inspecting a folder for the first time. `cd` changes directories — `cd ~` or just `cd` takes you home, `cd ..` goes up one level, `cd -` returns to the previous directory.

``` bash
$ ls -lah
total 32K
drwxr-xr-x  6 you staff  192B Apr 10 12:34 .
drwxr-xr-x  4 you staff  128B Apr 09 10:12 ..
-rw-r--r--  1 you staff  1.2K Apr 10 12:34 README.md
drwxr-xr-x  4 you staff  128B Apr 10 12:34 data
drwxr-xr-x  3 you staff   96B Apr 10 12:34 src
```

Once you are typing commands and paths, the two keyboard tricks that pay off most are **Tab completion** and **command history**. When you start typing a filename or a command, hit **Tab** and the shell will fill in the rest if there is exactly one match (and beep if there is not — hit Tab twice to see the candidates). This is not just a convenience; it eliminates a huge fraction of typo bugs, because if Tab refuses to complete, the file you are reaching for does not exist by that name. **Up Arrow** scrolls back through commands you have already run, and `Ctrl+R` lets you search the history for a substring — both let you reuse a slightly-modified version of a command rather than retyping it from scratch.

## 11.5 Creating, viewing, and editing files

To make a new directory, use `mkdir`. The flag worth knowing on day one is `-p`, which creates any missing parent directories along the way and silently does nothing if the target already exists — both conveniences that make `mkdir -p` safe to use in scripts. To create an empty file (or to update the timestamp on an existing one), use `touch`.

``` bash
mkdir -p ~/Courses/INFO-3010/Project/data/raw
touch README.md
touch data/raw/.gitkeep
```

To look at a file without opening it in an editor, the right command depends on the file’s size. For small text files, `cat file` dumps the whole thing to your terminal in one shot — fine for a 30-line config file, terrible for a 50,000-line CSV. For files of any meaningful size, `less file` opens a scrolling viewer where you can move with arrow keys, search forward with `/pattern`, and quit with `q`. For just the first or last few lines of a file, `head file` and `tail file` show you ten lines by default; use `head -n 5` or `tail -n 20` to control how many. The combination `head` and `tail` is the fastest way to peek at a CSV without waiting for the whole thing to render.

``` bash
cat config.yml             # small files only
less data/raw/sales.csv    # any size; q to quit
head data/raw/sales.csv    # first 10 lines
tail -n 20 logs/run.log    # last 20 lines
```

To create a small text file directly from the command line, you can use **redirection** with `echo` — `echo "hello" > greeting.txt` writes one line into a new file. This is useful for one-line files, but for anything multi-line you should use a real text editor. The terminal-friendly options are `nano` (the most beginner-friendly — its keyboard shortcuts are listed at the bottom of the screen, and `Ctrl+X` exits) or `vim` (much more powerful, much steeper learning curve). For longer-term work, a GUI editor like VS Code is almost always the right choice (see [sec-text-editors](#sec-text-editors)). The main reason to know `nano` exists is so that when you SSH into a server and need to fix a single line in a config file, you have a tool you can drive without panic.

``` bash
nano notes.txt    # opens nano; Ctrl+O to save, Ctrl+X to exit
```

## 11.6 File operations: copy, move, delete (with safety)

The three commands you will use most are `cp`, `mv`, and `rm`. `cp source dest` copies a file from one place to another. `mv source dest` moves it (or renames it, which is just moving from one name to another in the same folder). `rm file` deletes a file. All three accept either a single source or multiple sources, and all three accept the `-i` flag, which makes them prompt you before they overwrite or delete anything. For the first few weeks of using the terminal, using `-i` by default is a sensible safety net.

``` bash
cp data/raw.csv data/raw-backup.csv      # copy a file
mv old-name.py new-name.py               # rename a file
mv old-name.py ../backup/                # move it to another folder
rm scratch.txt                            # delete a file
rm -i scratch.txt                        # delete with confirmation prompt
```

Deleting a *directory* needs the `-r` flag, which means “recursive”: delete everything inside it as well as the directory itself. `rm -r build/` removes a build folder and all of its contents. This is genuinely useful, but it is also where every cautionary tale starts. The version with both `-r` and `-f` together — `rm -rf` — recursively deletes *and* suppresses every confirmation prompt and error message, which means a single typo can vaporize huge amounts of work without any chance to stop it. The most famous version of this is `rm -rf /` (delete everything starting from the root), but the more common real disaster is `rm -rf $VAR/something` where `$VAR` is unset and silently expands to nothing, leaving `rm -rf /something` — which can delete a system directory you needed. The defense is always the same: list the targets with `ls` *before* you `rm` them, and never combine `-r` and `-f` unless you can articulate exactly what is about to be removed.

``` bash
# Safe: confirm what will be deleted, then delete
$ ls -d build/
build/
$ rm -r build/

# Dangerous: skips all confirmations and error messages
$ rm -rf $SOME_DIR/   # if SOME_DIR is empty, this becomes rm -rf /
```

Closely related are **globs** — the wildcard patterns the shell expands into lists of filenames before passing them to a command. `*` matches any number of characters (so `*.csv` matches every CSV in the current directory), and `?` matches exactly one character. The crucial thing to understand is that globs are expanded by the *shell*, not by the command, and they are expanded *before* the command runs. That means `rm *.tmp` is not “remove any file matching `*.tmp`” from `rm`’s perspective; it is “remove `file1.tmp`, `file2.tmp`, `notes.tmp`” — `rm` has no idea you used a glob at all. The safety habit that follows from this is to preview what a glob will match by running `echo` with it first:

``` bash
$ echo *.tmp
file1.tmp file2.tmp notes.tmp
$ rm *.tmp                # only run this after the echo looked right
```

Two seconds of preview prevents the entire category of “I deleted way more than I meant to” disasters.

## 11.7 Searching and inspecting

### Finding files

The `find` command is how you locate files by their attributes rather than by their exact path. Its shape is a little unusual at first — you give it a starting directory, then a chain of predicates that describe what you are looking for — but once it clicks, it replaces a dozen one-off searches with a single dependable tool. The most common form is `find <where> -name <pattern>`, and you read it left-to-right as “starting here, find anything whose name matches this pattern”:

``` bash
find . -name "*.csv"              # every CSV under the current directory
find ~/Courses -name "lab*.py"    # every lab*.py under ~/Courses
find data/ -name "*.json" -type f # only regular files, not directories
```

The first gotcha is that `find` is *genuinely recursive*: if you run `find / -name "*.csv"` it will happily walk your entire filesystem, including system folders you should not be touching, and you will wait a long time for a result full of things you did not want. **Always start `find` in the narrowest directory that could possibly contain the answer.** If you think the file is somewhere in your project, start from the project root, not from `~`. If you think it is somewhere in your home folder, start from `~`, not from `/`. The fastest `find` is the one that has the smallest haystack to search.

The second gotcha is that `find` has many more predicates than `-name`, and a few are worth knowing even if you rarely use them. `-type f` limits the results to regular files (skipping directories); `-type d` does the opposite. `-mtime -7` restricts to files modified in the last seven days, which is the fastest way to answer “what did I change this week?” And `-size +10M` finds files larger than 10 megabytes, which is the easiest way to hunt down what is filling up your disk.

``` bash
find . -type f -mtime -1            # modified in the last 24 hours
find ~ -size +100M -type f          # files over 100 MB in your home
find . -name "*.pyc" -delete        # delete all matching files (careful!)
```

The last line is a warning in disguise: `-delete` tells `find` to remove each matching file, and combined with a broad pattern it can do real damage. Preview first by running the same command without `-delete` and confirming the listing is exactly what you meant to remove.

### Searching within files

While `find` searches by filename and metadata, `grep` searches by the *contents* of files. The basic form is `grep <pattern> <file>`, which prints every line in the file that contains the pattern. Give it multiple files and it also tells you which file each match came from, which is the piece that makes it useful at scale.

``` bash
grep "TODO" src/cleaning.py          # lines containing TODO
grep "TODO" src/*.py                 # every .py in src/
grep -n "error" logs/run.log         # also show line numbers
```

The flags that matter most on day one are `-i` for **case-insensitive** matching (so `grep -i error` finds `Error`, `ERROR`, and `error` all at once) and `-r` for **recursive** search through a directory tree. `grep -r "TODO" src/` walks every file under `src/` and prints every line containing `TODO`, with filenames and line numbers included — that one command is often all you need to audit a whole project for leftover stubs.

``` bash
grep -i "warning" app.log            # case-insensitive
grep -r "deprecated" src/            # recursive over a directory
grep -rn "api_key" .                 # recursive with line numbers
grep -v "INFO" app.log               # invert: lines that do NOT match
```

Two more habits pay off quickly. `grep -v` **inverts** the match, showing lines that do *not* contain the pattern — this is how you filter out noise like `INFO` lines to see only the warnings and errors that are left. And piping `grep` into another `grep` is a natural way to narrow a search: `ps aux | grep python | grep -v grep` is the canonical one-liner for “show me the currently running Python processes, minus the grep command itself.” (See “Pipes and redirection” below for the fuller story on how these chains work.)

### Inspecting file metadata

Before you do anything to a file you are not sure about, inspect it. The first command is one you already know: `ls -l` shows a long listing with permissions, owner, size, and modification time for each file in a directory. Add `-h` for human-readable sizes and `-a` for hidden files, and `ls -lah` becomes your default “tell me about this folder” command:

``` bash
$ ls -lah
-rw-r--r--  1 you  staff   1.2K Apr 10 12:34 README.md
drwxr-xr-x  4 you  staff   128B Apr 10 12:34 data
-rw-r--r--  1 you  staff   8.4M Apr 10 12:34 dataset.csv
```

From that single listing you can see that `dataset.csv` is 8.4 MB (big, but not suspicious), owned by you, and last modified today. A `dataset.csv` of `0B` would tell you the file exists but is empty — almost always a sign of a failed download or a crashed write. A `dataset.csv` whose owner is `root` instead of your username would tell you something was run with `sudo` that should not have been.

The second command is `file`, which looks at the actual bytes of a file and tells you what kind of content it contains, regardless of the extension:

``` bash
$ file dataset.csv
dataset.csv: ASCII text, with very long lines
$ file report.pdf
report.pdf: PDF document, version 1.5
$ file mystery.dat
mystery.dat: gzip compressed data, was "sales.csv", from Unix
```

`file` is invaluable when an extension is missing, wrong, or suspicious. The last example is a common one: a file you thought was plain data turns out to be a gzipped CSV that will never parse until you decompress it.

Finally, when you transfer a file from one machine to another and you want to be *sure* it arrived intact, you use a **checksum** — a short fingerprint computed from the file’s bytes. If the fingerprint on both sides matches, the bytes match. On macOS and Linux, the common tools are `md5` or `md5sum` for MD5 checksums, and `shasum -a 256` for SHA-256:

``` bash
$ shasum -a 256 dataset.csv
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  dataset.csv
```

You do not need checksums for everyday work, but they are the right answer whenever you find yourself asking, “did that big download actually finish, or did it silently truncate?” Compare the checksum the source publishes to the one your file computes. If they match, the file is good; if they do not, transfer again.

## 11.8 Pipes and redirection: building workflows

The reason the command line composes so well is that almost every Unix tool is built around the same three streams of data: **stdin** (where input comes from), **stdout** (where normal output goes), and **stderr** (where error messages go). By default stdin is your keyboard and stdout/stderr are your terminal, but you can redirect any of them to a file or to another command, and that is where the power lives.

Output redirection uses `>` to send stdout to a file. The catch is that `>` *overwrites* whatever was already in that file, with no warning and no undo. If you want to append instead, use `>>`. Both are extremely useful; both bite people who confuse them.

``` bash
ls > files.txt          # overwrite files.txt with the listing
ls >> files.txt         # append the listing instead
python script.py > output.csv      # save script output to a CSV
python script.py 2> errors.log     # save stderr to a separate log
```

The tool that turns redirection into a programming model is the **pipe**, written `|`. A pipe takes the stdout of one command and feeds it as the stdin of the next, so you can chain small focused programs into larger ones without ever writing a temporary file. Two of the most common patterns are sending a long listing through a pager (`ls -la | less`) and filtering one tool’s output through `grep` to keep only the lines you care about (`grep ERROR app.log | head`). A pipe can have any number of stages, and each stage runs as soon as it has data — which is why pipes can process gigabyte files using almost no memory.

``` bash
ls -la | less                              # paginate a long directory
grep ERROR logs/*.log | head -20           # first 20 ERROR lines
ps aux | grep python | grep -v grep        # currently running python
```

Every command that runs at the prompt finishes by returning an **exit code** — a small integer where `0` conventionally means success and any nonzero value means something went wrong. You can check the exit code of the most recent command with `echo $?`, and you can chain commands so that one only runs if the previous one succeeded with `&&`, or only if the previous one failed with `||`. This is the foundation for writing little shell scripts that fail safely instead of barreling onward after an error.

``` bash
$ python clean.py && python analyze.py     # only analyze if clean succeeded
$ make build || echo "build failed"        # message on failure
$ command1; echo $?                        # see exit code explicitly
0
```

The habit that follows from this is to always check that your commands actually succeeded, not to assume they did because the prompt came back. Pay attention to error output, look at exit codes when you are scripting, and treat any nonzero result as evidence to investigate before you move on.

## 11.9 From commands to scripts

The natural next step after typing the same command sequence twice is to put it in a file you can rerun. A **shell script** is a text file containing one or more shell commands, marked at the top with a special line called a [shebang](https://en.wikipedia.org/wiki/Shebang_(Unix)) that tells the operating system which interpreter to use:

``` bash
#!/usr/bin/env bash
# greet.sh — print a friendly greeting

echo "Hello, $USER!"
echo "Today is $(date +%A)."
```

Save that as `greet.sh`, mark it as executable, and run it:

``` bash
chmod +x greet.sh        # one-time: grant execute permission
./greet.sh               # the ./ tells the shell to look in the current directory
```

The two pieces that surprise newcomers are why you need `chmod +x` and why `./` is required. The execute bit is what tells the OS this file is meant to be *run* rather than just read; without it, the kernel refuses to launch the file even though the contents are perfectly valid. The `./` prefix is needed because the current directory is not on your `$PATH` by default (this is a deliberate security choice), so a bare `greet.sh` produces `command not found`. Putting the script in a directory that *is* on your `$PATH` — `~/bin` or `~/.local/bin` are common — lets you call it by name from anywhere.

This is the entire premise of shell scripting in one paragraph. The rest — control flow, error handling, exit-code conventions, and patterns for building real automation pipelines — lives in [sec-automation](#sec-automation), which treats scripts as the bottom rung of a longer ladder. Read that chapter when you are ready to write scripts that other people will run.

## 11.10 Environment basics: `PATH`, variables, and reproducibility

### Environment variables

Every process on your computer — your shell, every script it launches, every program — runs with a small bag of named values attached called the **environment**. Each name-value pair is an **environment variable**, and they are how programs pick up settings that are not part of the command line: where your home directory is (`$HOME`), what your username is (`$USER`), what language to use (`$LANG`), which editor to open (`$EDITOR`), and so on. When you launch a program, it inherits the environment of the shell that launched it, and most tools read a handful of specific variables to decide how to behave.

Reading the current value of a variable is straightforward — prefix the name with a `$` and ask the shell to print it:

``` bash
$ echo $HOME
/Users/you
$ echo $USER
you
$ echo $SHELL
/bin/zsh
```

Setting a variable for the current shell is just as simple, but the `export` keyword matters: without it, the variable only exists for the shell itself; with it, the variable is exported into the environment of any program the shell launches.

``` bash
$ MY_VAR=hello              # visible in this shell only
$ export MY_VAR=hello       # visible to any command launched from this shell
$ echo $MY_VAR
hello
```

The practical reason this matters is that many tools — databases, APIs, cloud SDKs — are configured through environment variables rather than through command-line flags. You do not type your database password on every command; you set `DATABASE_URL` once, and every tool that looks for it finds it. The discipline around secrets in environment variables (never commit them, never echo them into a shared log) lives in [sec-secrets](#sec-secrets).

### `PATH` and locating commands

There is one environment variable that matters more than any other for day-to-day command-line work, and its name is `PATH`. `PATH` is a colon-separated (or semicolon-separated on Windows) list of directories that the shell searches, in order, whenever you type a command name. When you run `python`, the shell walks each directory in `$PATH` looking for an executable file called `python`, and it runs the first one it finds. Any executable that is not in one of those directories is effectively invisible — typing its name will produce `command not found`.

``` bash
$ echo $PATH
/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin
```

To see *which* specific program the shell would actually run when you type a command, use `which` (or `type -a` for a more verbose answer that shows every match, not just the first):

``` bash
$ which python
/Users/you/miniconda3/bin/python
$ type -a python
python is /Users/you/miniconda3/bin/python
python is /usr/bin/python3
```

The second line of that output illustrates the most common `PATH` pitfall: **multiple versions of the same tool are installed, and the shell is finding a different one than you expect.** A student installs a new Python, writes code that depends on it, and then gets weird errors because a different Python earlier in `$PATH` is the one actually running. When a tool is behaving strangely — wrong version, missing package, unexpected paths — the first diagnostic move is always `which <tool>` to confirm which binary is being run, and then `<tool> --version` to confirm it is the version you think it is. This is especially important for Python and conda environments (see [sec-pkg-mgmt](#sec-pkg-mgmt) and [sec-virtual-environments](#sec-virtual-environments)), where it is very easy to “install” a package into a Python that is not the one actually on your `PATH`.

### Working directory as a dependency

Every command you run has an invisible but consequential input: the **current working directory**, or CWD. Any relative path in the command — `data/input.csv`, `./clean.sh`, `../notes.md` — is resolved starting from the CWD, so the same command can succeed or fail depending only on where you were standing when you ran it. This is so central to reproducibility that it is worth treating the CWD as a first-class dependency of every script.

``` bash
$ pwd
/Users/you/Courses/INFO-3010/Project
$ python src/clean.py          # reads data/input.csv relative to Project/
$ cd src
$ python clean.py              # BROKEN: data/input.csv is now relative to src/
```

The fix is the habit you already met in [sec-filesystem](#sec-filesystem): adopt a stable project root, always `cd` there before running your code, and write the code so that every path is either absolute (anchored at that root) or relative to a file the code can find reliably. In Python, `Path(__file__).resolve().parent` computes a script’s own folder regardless of where it was launched from; in shell scripts, the idiomatic trick is `cd "$(dirname "$0")"` at the top to change into the script’s own directory.

``` bash
#!/usr/bin/env bash
cd "$(dirname "$0")"    # change into the script's own folder
python clean.py         # now all relative paths resolve predictably
```

A project whose scripts all start with this pattern is much harder to break by accident, because the code no longer depends on the CWD the user happened to be in.

## 11.11 Permissions, ownership, and `sudo`

### The permission model (just enough)

- Users, groups, and “other.”

- Read/write/execute bits and what they mean for files vs directories.

- Recognizing permission errors.

### When to use `sudo` (and when not to)

`sudo` runs a single command with elevated (root) privileges. It exists for one specific purpose: to let you make changes that affect the whole system, like installing software through a system package manager or editing a system configuration file. When you genuinely need that, `sudo` is the right tool. The trap is using `sudo` reflexively to “fix” a permission problem you do not yet understand, because the elevated command will succeed whether or not it was the right thing to do — and if it was the wrong thing, you have just made the problem harder to undo.

A reliable rule of thumb: never use `sudo` on anything inside your project folder. If a script in `~/Courses/INFO-3010/Project/` is failing with a permission error, the cause is almost certainly that the file is owned by someone other than you (often root, because of an earlier accidental `sudo`), and the fix is to restore correct ownership — *not* to add another `sudo`. Adding `sudo` to “make it work” usually creates files owned by root in the middle of your project, which you will then trip over for weeks afterward.

``` bash
# Reasonable uses of sudo (system-level changes)
sudo apt update && sudo apt install build-essential   # Linux: install system packages
sudo systemctl restart nginx                           # Linux: restart a service

# Bad uses (you should never need these)
sudo python my_script.py        # never run your own code as root
sudo rm -rf ~/project/data       # using sudo on your own files is a code smell
```

### Safe `sudo` practices

When you do reach for `sudo`, treat it like a loaded tool. Read the command twice before pressing Enter, especially the parts you copy-pasted from somewhere. Prefer explicit paths to wildcards (`sudo rm /var/log/old.log` is fine; `sudo rm -rf /var/log/*` is one wrong character away from disaster). Avoid piping random output into `sudo` from the internet unless you are willing to commit to understanding what each step does (`curl ... | sudo bash` is the canonical example of the wrong reflex). And the firmest rule is the simplest: never paste a command containing `sudo` from a forum or AI assistant without first reading every flag and confirming the path it operates on.

### Recovering from permission issues

When you hit a permission error, the first move is *not* to add `sudo`. The first move is to figure out what the actual ownership and permissions are with `ls -l`:

``` bash
$ ls -l data/output.csv
-rw-r--r--  1 root  staff  1234 Apr 10 12:34 output.csv
                  ^^^^
                  owned by root, not you
```

If a file in your project ends up owned by `root` (because an earlier command was run with `sudo`), the fix is to restore your ownership: `sudo chown $(whoami) data/output.csv`. If you have created a tangle of root-owned files inside a project — which is a not-uncommon way for a debugging session to go sideways — stop, do not run any more `sudo` commands, and ask for help. Untangling root-owned files is a small task when you catch it early and a much larger one if you keep adding more.

## 11.12 Security hygiene for terminal users

### Secrets and command history

Your shell keeps a running log of every command you type, usually in a file called `.bash_history` or `.zsh_history` in your home directory. That log is a convenience — it is what powers the up arrow and `Ctrl+R` — but it is also a durable record of everything that passed through your terminal. Anyone who gets access to that file, whether through a backup, a shared account, or a compromised machine, can read it. That means **anything you type literally on the command line is effectively written down**, and the place you never want a password or API token written down is a plaintext file with no access controls.

The rule that follows is simple: **never put a secret directly on the command line if you can avoid it.** The obvious bad form is something like `curl -H "Authorization: Bearer sk-REAL-TOKEN" ...`, which parks the real token in your history forever and also in the process list while the command runs (where any other user on the machine can see it with `ps`). The better form is to load the secret from an environment variable that was set earlier, from a config file with strict permissions, or from a dedicated secret manager:

``` bash
# BAD: the token goes into your shell history
curl -H "Authorization: Bearer sk-1234567890abcdef" https://api.example.com

# BETTER: load the token from an environment variable
export API_TOKEN=$(cat ~/.secrets/api-token)
curl -H "Authorization: Bearer $API_TOKEN" https://api.example.com
```

The even better form uses a `.env` file, a password manager, or a cloud secret store, which [sec-secrets](#sec-secrets) covers in full. On the rare occasion you do need to type a secret interactively, use a tool that reads it without echoing it to the screen (`read -s PASSWORD`, `ssh-add` for keys) and never paste it into a command. If you ever realize you accidentally typed a secret on the command line, rotate the secret immediately and then edit your history file to remove the entry — in that order, because the rotation is the only thing that actually makes you safe.

### Copy/paste safety

The second category of terminal-specific security bugs is the pasted command. You see a command on Stack Overflow, a blog post, or in a chat with an AI assistant; you copy it; you paste it into your terminal; and you press Enter because the prompt came back and everything seemed fine. That reflex has cost real people real systems, because **pasting a command is morally the same as running a program you did not read first.** A malicious blog could include a command like:

    echo "totally normal command"; rm -rf ~

where the semicolon and the destructive second command are hidden off-screen in a narrow code block, or embedded in invisible characters that only show up once you paste. Many modern terminals now refuse to auto-execute multi-line pastes for exactly this reason, but the defense you control is to **always read a pasted command before you press Enter**. Look at every flag, confirm every path, and if the command contains a pipe into `bash` or `sh` (`curl ... | sudo bash` is the classic form), stop and ask whether you are willing to run that script sight-unseen.

The supporting habit is to prefer official documentation for install commands. A vendor’s own install guide is not perfect, but it is accountable — they lose reputation if it breaks things. A random fix posted in a forum thread by a stranger has no accountability at all. When both exist, always go with the official source.

### Least privilege

The single habit that prevents the most catastrophic terminal mistakes is **least privilege**: do your real work as a normal user, inside your own home directory, and only elevate to administrator rights for specific, well-scoped tasks that genuinely require them. Every command you run without `sudo` is bounded by what your normal account is allowed to touch, which means a typo can mess up your own files but cannot destroy the operating system, delete other users’ data, or leave the machine unbootable.

In practice, “least privilege” means three things. First, **keep your project folders under your home directory**, never in system locations. `~/Courses/` and `~/Projects/` are yours to do whatever you like with; `/System/`, `C:\Windows\`, `/usr/local/` are not. Second, **resist the reflex to `sudo` a command that fails with a permission error**; ninety-nine percent of the time the error is telling you to move the work somewhere you own, not to override the check. Third, **when you do need `sudo`, use it for exactly the command that needs it, not as a blanket on a whole session.** `sudo apt install <package>` is reasonable; opening a root shell with `sudo -i` and forgetting you are in it is how accidents happen.

``` bash
# Reasonable: specific elevated task, then immediately back to normal
$ sudo apt install ripgrep
$ rg "TODO" .

# Risky: an entire session running as root
$ sudo -i           # now every command is running as root
# ... hours later, you forget and run something destructive
```

If you make a habit of running as your normal user by default, the rare occasions you do need `sudo` will stand out, and you will give them the care they deserve.

## 11.13 Workflow patterns for students

### Pattern 1: “enter a project, run, exit”

Almost every command-line session on a project follows the same shape, and giving that shape a name makes it easier to do the same way every time. The pattern is *enter, confirm, run, save, exit*, and it looks like this:

``` bash
$ cd ~/Courses/INFO-3010/Project        # 1. enter the project
$ pwd                                    # 2. confirm where you are
/Users/you/Courses/INFO-3010/Project
$ ls                                     # 3. confirm what's there
README.md   data/   notebooks/   src/
$ python src/clean.py                    # 4. run the command
$ ls data/processed/                     # 5. verify the output
cleaned.csv
```

Every step exists for a reason. The `cd` pins you to a stable project root so that every relative path in every script resolves the same way. The `pwd` and `ls` are a thirty-seconds-of-paranoia check that catches “wrong directory” before it turns into “file not found” or, worse, “overwrote the wrong file.” Running the command is the actual work; listing the output directory afterward confirms that the command actually produced the files it promised instead of failing silently. And exiting cleanly — closing the terminal or running `deactivate` on any active virtual environment — leaves the next session with a clean slate instead of carrying state you will forget about.

The value of having a habitual pattern is that it does not depend on whether you are tired or distracted. Once the pattern is muscle memory, you do it even when you are not paying attention, and the small disasters that come from skipping steps stop happening.

### Pattern 2: creating a reproducible command log

After you run a command successfully, write down what you ran. This sounds like overkill until the first time you try to reproduce a result three weeks later and discover that “the script I ran on Tuesday” is not the same as “the script I ran on Wednesday with a slightly different flag.” The fix is to keep a plain-text log of the commands that produced each meaningful artifact, either in the project’s `README.md` or in a dedicated `notes.txt` next to the output.

``` markdown
## How to reproduce data/processed/cleaned.csv

1. Ensure the virtual environment is active:
   ```bash
   source .venv/bin/activate
```

2.  Confirm raw input exists:

    ``` bash
    ls data/raw/survey.csv
    ```

3.  Run the cleaning script:

    ``` bash
    python src/clean.py --input data/raw/survey.csv --output data/processed/cleaned.csv
    ```

Produces: `data/processed/cleaned.csv` (expected ~5 MB, ~18,000 rows).


    A reproducible log has three pieces. It records the **inputs** (which files the command reads, which environment is active), the **command itself** including every flag, and the **outputs** (what should exist afterward, and ideally how big it should be). With those three pieces, any future reader — including you — can retrace the work without guessing. The log belongs in version control alongside the code, because a script is only as reproducible as the instructions for running it.

    ### Pattern 3: safe cleanup

    Cleanup is the operation where beginner command-line disasters cluster, because it combines "I am about to delete something" with "I am not fully sure what I am deleting." The safe-cleanup pattern is designed to separate those two steps: figure out what you are about to remove, *then* remove it, and never let a single command do both.

    ```bash
    # 1. Identify and preview: what would be removed?
    $ find . -name "*.tmp" -type f
    ./notebooks/draft.tmp
    ./data/processed/intermediate.tmp

    # 2. Archive anything you might want later
    $ mkdir -p archive/2026-04-10
    $ cp data/processed/*.csv archive/2026-04-10/

    # 3. Delete with care, using the exact list from step 1
    $ find . -name "*.tmp" -type f -delete

    # 4. Verify the delete did what you expected
    $ find . -name "*.tmp" -type f
    $           # empty output: no more .tmp files

The four steps are: identify, archive, delete, verify. Identification uses search and preview (`ls`, `find`, `echo *glob*`) so you can see the targets as a list before anything irreversible happens. Archiving copies anything you think you might want later into a dated folder — it costs almost nothing and prevents the “oh no, I needed that” moment. Deletion runs the actual removal, ideally against the exact same list the identification step produced. Verification runs the identification step again to confirm the targets are gone and nothing extra has joined them. Follow this pattern even on “obvious” cleanups, and the worst case of a mistake is that you have to restore a file from the archive folder rather than from a backup you hope exists.

## 11.14 Troubleshooting playbook

### Common errors and what they mean

A few error messages account for the overwhelming majority of everyday terminal problems, and once you recognize them, most of the time you can fix the issue yourself in under a minute. The key is to read the error literally — the shell is telling you exactly what went wrong — and match it to the right diagnostic move.

**`command not found`** means the shell searched every directory on your `$PATH` and could not find a program with the name you typed. There are three reasons this happens, roughly in order of likelihood. First, you might have a typo (`pthon` instead of `python`). Second, the program might not be installed — a fresh machine, a new virtual environment, or a tool you forgot to `pip install`. Third, the program is installed but the directory that contains it is not on your `PATH`, which is especially common after installing a new Python or a language version manager.

``` bash
$ pthon --version
zsh: command not found: pthon       # typo — fix the spelling

$ python --version                   # confirm python is actually there
$ which python                       # confirm where it resolves to
```

**`No such file or directory`** means the command ran but it cannot find the file you pointed it at. The culprit is almost always one of three things: the file name is spelled wrong (case-sensitive on macOS and Linux!), you are in the wrong directory so a relative path does not resolve where you expect, or the file has a hidden extension like `.csv.txt` that the GUI was disguising.

``` bash
$ python src/Clean.py
python: can't open file 'src/Clean.py': [Errno 2] No such file or directory
$ ls src/                             # what's actually in src/?
clean.py    __init__.py
$ python src/clean.py                 # lowercase filename
```

**`Permission denied`** means the file exists and the command tried to access it, but the operating system refused. The right response is almost *never* to prepend `sudo`. The right response is to run `ls -l` on the file and figure out *why* you do not have permission. Is it owned by a different user? Then fix the ownership instead of running as root. Is it in a system directory you should not be writing to? Then move the work into your own home folder.

``` bash
$ ./deploy.sh
zsh: permission denied: ./deploy.sh
$ ls -l deploy.sh                     # is it marked executable?
-rw-r--r-- 1 you staff 1234 Apr 10 deploy.sh
$ chmod +x deploy.sh                  # make it executable — no sudo needed
```

**`Is a directory`** means the command expected a regular file but you gave it a directory. The fix is to add the filename inside the directory, or to use a flag like `-r` (for `cp` and `rm`) that tells the command to operate recursively on everything beneath the directory.

``` bash
$ cat data/                           # cat expects a file
cat: data/: Is a directory
$ cat data/survey.csv                 # point it at a file
$ ls data/                            # or use the right tool for a directory
```

### A disciplined response

When a command fails and the error message is not immediately obvious, the temptation is to guess — retype the command with a small tweak and hope. That guessing spiral is where most stuck sessions happen. The alternative is a short, disciplined sequence you run every time, in order, without skipping steps:

1.  **Re-read the command and the error.** Literally read what you typed aloud and what came back. A surprising fraction of bugs are typos that become obvious the moment you slow down.

2.  **Print your current directory and list its contents.** `pwd` tells you where you are; `ls` (or `ls -la` for more detail) tells you what is there. Ninety percent of “file not found” errors are resolved by this one step — either you are in the wrong place, or the file has a name you did not expect.

3.  **Confirm paths and file extensions explicitly.** If the error mentions a file, use `ls` to verify the file exists with exactly the name and extension the command is expecting. Pay special attention to hidden extensions (`.csv.txt`), case-sensitivity, and trailing spaces.

4.  **Consult `--help` or `man` for the command.** When you are sure the inputs are right but the command is still failing, the problem might be that you are using a flag incorrectly. `command --help` usually answers this in one screen; `man command` gives the full reference.

5.  **If you are still stuck, build a minimal reproduction and ask a precise question.** Strip the problem down to the shortest possible command that still shows the error, capture the exact error message, and include the output of `pwd`, `ls`, and `<tool> --version`. A question posed that way is almost always answerable, whether you are asking a classmate, a forum, or an AI assistant — and often the act of assembling it is enough to make the answer obvious on its own. ([sec-asking-questions](#sec-asking-questions) covers this in more depth.)

``` bash
# A minimal reproduction template to share when asking for help
$ pwd
/Users/you/Courses/INFO-3010/Project
$ python --version
Python 3.11.8
$ ls src/clean.py
src/clean.py
$ python src/clean.py
Traceback (most recent call last):
  File "src/clean.py", line 12, in <module>
    ...
```

Disciplined debugging is not glamorous, but it is reliable, and it is what separates people who lose an hour to a mystery error from people who spend two minutes and keep working.

## 11.15 Stakes and politics

The command line is the most overtly cultural artifact in this entire handbook. Two things to notice. First, *who is “supposed” to use it*. A culture has grown up around the terminal — descended from Unix at Bell Labs in the 1970s and hardened in academic CS departments through the 1980s and 1990s — that treats command-line fluency as the marker of real technical competence and graphical interfaces as scaffolding for people who do not know any better. That hierarchy has consequences: hiring funnels, open-source contribution norms, and the implicit “if you have to ask, you do not belong” tone of many tutorials all use terminal fluency as a gate. The skills are genuinely valuable — that is why this chapter exists — but the gatekeeping is a separate phenomenon worth naming.

Second, *which terminal is normal*. Almost every tutorial, including this one, assumes a Unix-like shell (`bash` or `zsh`), which means Windows users without WSL and Chromebook users with restricted shells either translate every example into PowerShell or get told to “just use a real OS.” That assumption is a deliberate choice, made by a community whose members already had the right hardware and operating systems for it. People learning on locked-down school laptops, on phones, on cheap Chromebooks, or on shared library terminals carry the cost of that choice.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: the terminal is a powerful tool *and* a status marker; you can learn it well without pretending the gatekeeping around it is not real.

## 11.16 Worked examples

### Building a course workspace from the terminal

You are starting a new semester with three courses, and you want one stable home for everything. From the terminal, the whole setup is one command:

``` bash
mkdir -p ~/Courses/INFO-3010/{Assignments,Labs,Project}
mkdir -p ~/Courses/INFO-4040/{Assignments,Project}
mkdir -p ~/Courses/STAT-2010/{Assignments,Labs}
```

The `{...}` part is shell **brace expansion**, which is shorthand for “create one directory for each name inside the braces.” After running it, navigate and list to confirm:

``` bash
$ cd ~/Courses
$ ls -l
total 0
drwxr-xr-x  5 you staff  160 Apr 10 12:34 INFO-3010
drwxr-xr-x  4 you staff  128 Apr 10 12:34 INFO-4040
drwxr-xr-x  4 you staff  128 Apr 10 12:34 STAT-2010
$ ls -l INFO-3010
total 0
drwxr-xr-x  2 you staff  64 Apr 10 12:34 Assignments
drwxr-xr-x  2 you staff  64 Apr 10 12:34 Labs
drwxr-xr-x  2 you staff  64 Apr 10 12:34 Project
```

Three lines of terminal input replace several minutes of clicking through a file manager.

### Inspecting a dataset file you have not seen before

A new CSV lands in your `data/raw/` folder. Before you load it into pandas, look at it from the terminal — sometimes the answer is faster there. The first thing you want is the *shape* of the file: how big is it, how many lines, what does the first row look like?

``` bash
$ ls -lh data/raw/sales.csv
-rw-r--r--  1 you staff  4.2M Apr 10 12:34 data/raw/sales.csv
$ wc -l data/raw/sales.csv
   42103 data/raw/sales.csv
$ head -n 3 data/raw/sales.csv
order_id,date,customer_id,amount
1001,2026-01-15,C-447,28.50
1002,2026-01-15,C-098,140.00
```

Now you know the file is 4.2 MB, has 42,103 lines (which is roughly the row count), and uses commas with a header row. To check whether a particular column name actually exists, you can search the header row directly:

``` bash
$ head -n 1 data/raw/sales.csv | grep -o "customer_id"
customer_id
```

If `grep` finds nothing, the column is not there — and you have just saved yourself a `KeyError` debugging session.

### Building a small pipeline

A small pipeline that counts how many distinct customers placed orders on a given day, using nothing but standard tools:

``` bash
$ grep "2026-01-15" data/raw/sales.csv | cut -d, -f3 | sort -u | wc -l
142
```

The pipeline reads as a sequence of small steps: `grep` filters the file to lines containing the date; `cut -d, -f3` extracts the third comma-separated field (the customer id); `sort -u` removes duplicates; and `wc -l` counts the remaining lines. That is your answer: 142 distinct customers ordered that day. The same calculation in pandas is one line, but the terminal version is faster to write when you do not yet trust the data and are still inspecting it.

You can also save the result for later with redirection:

``` bash
grep "2026-01-15" data/raw/sales.csv | cut -d, -f3 | sort -u > customers-jan15.txt
```

### Diagnosing a “file not found” error

You run a Python script and it crashes with `FileNotFoundError: data/input.csv`. Walk through three checks before changing the code. First, confirm where you are:

``` bash
$ pwd
/Users/you/Courses/INFO-3010/Project/notebooks
```

If `pwd` says you are in `notebooks/` and your script expects to find `data/input.csv` relative to the project root, then the path it is computing is `notebooks/data/input.csv` — which does not exist. Two fixes: either `cd ..` to the project root and rerun, or rewrite the path in the script to be computed from `__file__`. Second, confirm the file actually exists where you think it does:

``` bash
$ ls -lh ../data/
total 8.3M
-rw-r--r--  1 you staff  4.2M Apr 10 12:34 input.csv
```

If `input.csv` does not appear in the listing, the bug is *not* in the code — the file is genuinely missing. If it appears with a different name (a trailing space, an extra `.txt` extension), fix the filename. Third, confirm there are no Unicode lookalikes or hidden characters in the name:

``` bash
$ ls ../data/ | od -c | head -3
0000000   i   n   p   u   t   .   c   s   v  \n
```

If the bytes look like the filename you expected, you are good. If they include surprises, that is the bug. With those three checks, “file not found” becomes diagnosable in under a minute.

## 11.17 Templates

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

## 11.18 Exercises

1.  Navigate from your home directory to a course folder using only `cd`, `pwd`, `ls`.

2.  Create a project directory structure with `mkdir -p`.

3.  Create a text file, preview it with `head`, then open it in `less`.

4.  Copy a directory; rename the copy; explain the difference between copy and move.

5.  Use a wildcard to list only `.csv` files; preview the expansion with `echo`.

6.  Build a pipeline that searches within a file and writes matching lines to an output file.

7.  Trigger a permission error intentionally (in a safe location) and explain why `sudo` is not the first fix.

## 11.19 One-page checklist

- I can explain terminal vs shell, and command + arguments.

- I can navigate with `pwd`, `ls`, `cd` and understand paths.

- I can create files/directories and view contents safely.

- I can copy/move/delete with caution and preview wildcards.

- I can use `–help` and `man`.

- I can use pipes and redirection and understand overwrite vs append.

- I understand permissions and use `sudo` only when appropriate.

- I avoid leaking secrets in commands and history.

## 11.20 Windows notes: PowerShell and WSL (optional)

### Two common paths

- **WSL** gives a Linux-like shell where `sudo` and Unix commands apply.

- **PowerShell** uses different command names and syntax (but the same mental models: paths, pipes, permissions).

### Concept mapping (high level)

- Navigation: `cd`, `pwd` (`Get-Location`), listing (`ls`/`dir`).

- Help: `–help`/`man` vs `Get-Help`.

- Pipes exist in both, but objects vs text differ.

## 11.21 What is a terminal?

A terminal is a tool for interacting with your computer by issuing commands. A terminal launches a shell (e.g. `bash` or `zsh`), so sometimes you will hear a “terminal” also described as a “shell”.

## 11.22 What terminal commands should I know, as a basic foundation?

The exact syntax of terminal commands will be slightly different on Windows and Mac. So to keep things consistent, we are only going to detail high-level descriptions of terminal commands in this guide. You can Google the exact commands for your specific system; it is good practice to learn to search for the terminal commands you will need online.

To get started with the terminal for your INFO classes, you should memorize the commands for each of the following:

- Activate/deactivate a conda environment

- Change your directory

- Install a specific version of a package with conda

- Inspect the location of a program to the terminal (e.g. `which Python`)

- Print your working directory

> **NOTE:**
>
> - GNU, [The Bash Reference Manual](https://www.gnu.org/software/bash/manual/) — the canonical reference for bash syntax, built-ins, and scripting.
> - Software Carpentry, [The Unix Shell](https://swcarpentry.github.io/shell-novice/) — a complete beginner tutorial with hands-on exercises and small datasets.
> - William Shotts, [*The Linux Command Line*](https://linuxcommand.org/tlcl.php) — a 500-page free PDF that is the best single book for going from “I can `cd` and `ls`” to “I can write a real shell script.”
> - Michael Kerrisk, [`man7.org` Linux man pages](https://man7.org/linux/man-pages/) — searchable, current copies of every standard man page; faster to read in a browser than `man` in some terminals.
> - Julia Evans, [Bite Size Command Line](https://wizardzines.com/zines/bite-size-command-line/) — a short illustrated zine on the everyday commands and the mental moves around them.
> - [ExplainShell](https://explainshell.com/) — paste any command and get a breakdown of every flag and argument; great for understanding a one-liner you copied from a tutorial.
> - [ShellCheck](https://www.shellcheck.net/) — a linter for shell scripts that catches the quoting and globbing mistakes nobody catches by eye; run it on every shell script you write.
