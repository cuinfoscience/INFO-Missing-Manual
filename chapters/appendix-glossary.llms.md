# Appendix A — Glossary

You’re halfway through a chapter, you hit a word like “kernel” or “PATH,” and nobody ever told you what it means. This page is for that moment. The terms are in alphabetical order, each with a short, plain definition and a pointer to the chapter that teaches it properly, so you can look one up and get straight back to what you were doing. When a chapter uses one of these words for the first time, it usually links here (a mention of a **package** in [sec-pkg-mgmt](#sec-pkg-mgmt), for example, jumps straight to its entry below).

A lot of these words name layers of the software on your computer: the operating system at the bottom, then the file system, the shell, Python, its packages, and finally your own code. Together they’re sometimes called the [technology stack](https://en.wikipedia.org/wiki/Solution_stack). When something breaks, figuring out *which layer* is misbehaving is half the battle, and knowing its name makes the other half, searching for help or asking someone, a lot easier.

### Algorithmic audit

A close look at an AI or algorithmic system to find out whether it’s fair, safe, or accurate for the people it affects, including the failures nobody planned for. Who runs it matters: a **first-party** audit is done by the company that built the system, a **second-party** audit by the organization using it, and a **third-party** audit by an independent group with the access and the reason to find problems. Most audits in practice are first-party, so “we audited it” doesn’t by itself mean much. See [sec-evaluating-ai](#sec-evaluating-ai), and [sec-artifacts-politics](#sec-artifacts-politics) for why who holds the power matters.

### Application

A program you open to get something done, like Microsoft Word, Excel, Google Chrome, or Apple Mail. Applications are built separately for each operating system, which is why a Mac app won’t run on Windows, and they need your permission to read and save files in some places.

### Breakpoint

A line where a running program pauses so you can look around inside it with a debugger: the values of your variables, the chain of calls that got you there, and what happens as you run it one line at a time. You set one by writing `breakpoint()` in Python code or by clicking beside a line number in your editor; a *conditional* breakpoint pauses only when an expression you give it is true, such as `row_id == 1047`. See [sec-debugging](#sec-debugging) and [sec-text-editors](#sec-text-editors).

### Channel

A named place [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/channels.html) downloads packages from. Anaconda and Miniconda start with Anaconda’s own `defaults` channel, while Miniforge starts with **conda-forge**, a community channel with far more packages. If conda says it can’t find a package, or two packages won’t install together, the channel is one of the first things to check. See [sec-pkg-mgmt](#sec-pkg-mgmt).

### Command line interface (CLI)

A way of using your computer by typing commands instead of clicking, such as `ls` to list the files in a folder or `python analyze.py` to run a script. It looks bare at first, but it’s often faster than clicking, it can be scripted, and it’s the only option on many servers. On a Mac you get to it through the Terminal app; on Windows, through Windows Terminal running PowerShell, Command Prompt, or (the one the book recommends) WSL or Git Bash. See [sec-terminal](#sec-terminal).

### CSV (Comma-Separated Values)

A plain-text file format for tables: each row is a line, and the columns are separated by a delimiter, usually a comma (sometimes a tab or a semicolon). Because a CSV stores everything as text, the program that reads it has to guess what’s a number, a date, or a missing value, and it sometimes guesses wrong. See [sec-data-file-formats](#sec-data-file-formats) for how to read one reliably.

### Data dictionary

A small table that explains a dataset one column at a time: each column’s name, its type, what it means in plain words, its units, the values it’s allowed to take, and how missing values are marked. Keep it as a file next to the data, and someone else (or you, six months from now) can use the data correctly, and a short script can check new data against it. A *codebook* is the survey-research version, which adds each question’s exact wording and what its answer codes mean (`1` = “strongly disagree”). See [sec-project-management](#sec-project-management).

### Driver

A small program that lets the operating system talk to a piece of hardware, such as your Wi-Fi card, printer, graphics card, or trackpad. Your operating system keeps most drivers up to date through its own updates, so install drivers only from the operating system or the hardware’s maker, never from a “driver updater” site. See [sec-os-management](#sec-os-management).

### Environment

Everything your code runs *inside* of, beyond the code itself. In Python talk it usually means one Python interpreter and the packages installed for it, and you can have many on the same computer, one per project. More broadly, a program’s environment also includes its environment variables (like `PATH`) and the folder it was started from. When code works on one computer and fails on another, a different environment is the usual suspect. See [sec-pkg-mgmt](#sec-pkg-mgmt) and [sec-virtual-environments](#sec-virtual-environments).

### File system

The part of your computer that stores your files and folders, keeps track of where each one is, and decides who’s allowed to read or change it. Every file has an address in it, called a *path*, like `Documents/thesis/data/survey.csv`. See [sec-filesystem](#sec-filesystem).

### Graphical user interface (GUI)

The windows, icons, menus, and buttons you click to use a computer, as opposed to typing commands. Finder on macOS and File Explorer on Windows are GUIs for your file system. You’ll sometimes hear GUI pronounced “gooey.”

### JSON (JavaScript Object Notation)

A plain-text format for structured data, built from `{ }` objects (named fields) and `[ ]` lists that can nest inside each other, like `{"name": "Ada", "courses": ["INFO 1201", "STAT 2010"]}`. It’s what most web APIs send back, what many tools use for settings, and even what a Jupyter notebook is underneath. See [sec-common-formats](#sec-common-formats) and [sec-data-file-formats](#sec-data-file-formats).

### Jupyter kernel

The separate program that actually runs the code in your Jupyter notebook; for a Python notebook, it’s a Python interpreter. The kernel remembers every variable you’ve created until it restarts, even ones whose cells you’ve since deleted, which is why a notebook can “work” only because of something still in memory. It also decides which Python (and so which installed packages) your code sees, so if an import fails in a notebook but works in the terminal, check the kernel first. See [sec-jupyter](#sec-jupyter) and [sec-virtual-environments](#sec-virtual-environments).

### Large language model (LLM)

The kind of AI model behind ChatGPT, Claude, Gemini, and GitHub Copilot. It’s a neural network trained on huge amounts of text, and it writes by predicting, over and over, which small piece of text (a *token*) should come next. That makes it good at producing text that sounds right, which isn’t the same as text that is right. See [sec-ai-llm](#sec-ai-llm) and [sec-llm-internals](#sec-llm-internals).

### Library

Code someone else wrote that adds abilities to a programming language. Python on its own covers the basics; libraries like `numpy`, `pandas`, and `matplotlib` add fast math, data tables, and plotting. In Python, “library” and “package” are used almost interchangeably. When a traceback shows a path containing `site-packages/`, that’s a library you installed. See [sec-pkg-mgmt](#sec-pkg-mgmt).

### Markdown

A simple way to format plain text with ordinary characters: `#` for a heading, `**bold**` for bold, `-` for a list item, and backticks for `code`. The raw file stays readable, and tools turn it into a nicely formatted page. It’s how README files, GitHub issues, Jupyter text cells, and Quarto books like this one are written. See [sec-common-formats](#sec-common-formats).

### Matilda effect

The pattern of women’s contributions to research being under-cited and credited to someone else, often a male colleague. The historian of science Margaret Rossiter named it in 1993, after the suffragist Matilda Joslyn Gage, as a counterpart to the [Matthew effect](https://en.wikipedia.org/wiki/Matthew_effect), in which people who already have credit get more of it. The same pattern shows up for scholars of color and scholars outside the most powerful institutions and countries. See [sec-writing-manuscripts](#sec-writing-manuscripts) and [Wikipedia’s article](https://en.wikipedia.org/wiki/Matilda_effect).

### Network drive

A folder on another computer, usually a department file server, that your computer connects to over the network and shows as if it were local: a mapped drive on Windows (`\\server\share`), or a server you connect to from Finder on a Mac (`smb://server/share`). Every read and write crosses the network, so it’s slow for big files and it vanishes when you go offline. See [sec-filesystem-cloud](#sec-filesystem-cloud).

### Notebook

A document that mixes code you can run, the output it produces (tables, charts, errors), and written notes, all in one file. The Jupyter notebook (a `.ipynb` file) is the most common kind in Python. Great for exploring, but the order you ran the cells in isn’t always the order on the page, so restart and run everything from the top before you trust the results. See [sec-jupyter](#sec-jupyter).

### Online-only file

A placeholder a sync client leaves on your disk to save space: the file’s name and icon are there, but its contents stay in the cloud until something opens it. OneDrive calls this Files On-Demand, and iCloud Drive does it when *Optimize Mac Storage* is on. It’s handy for documents, but code that reads an online-only file has to wait for a download, and fails if you’re offline. See [sec-filesystem-cloud](#sec-filesystem-cloud).

### Open access (OA)

Research that anyone can read for free online, with no subscription or paywall. *Gold* OA means the journal itself publishes the article openly, sometimes paid for by a fee from the author or their university; *green* OA means the author has posted a free copy somewhere else, such as arXiv or their university’s repository. See [sec-reading-scholarship](#sec-reading-scholarship) and the [Directory of Open Access Journals](https://doaj.org/).

### Operating system

The software between your apps and your hardware: macOS, Windows, and Linux are all operating systems. It launches and stops programs, runs the file system, keeps user accounts and their permissions separate, and talks to your keyboard, screen, Wi-Fi, and storage through drivers. See [sec-os-management](#sec-os-management).

### Package

Code that someone else has already written and published for you to install and use, such as [numpy](https://numpy.org/), [pandas](https://pandas.pydata.org/), or `requests`. The word has a second, narrower meaning in Python: a folder of your own `.py` files that you import as one unit, usually marked by an `__init__.py` file inside it. See [sec-pkg-mgmt](#sec-pkg-mgmt) and [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).

### Package manager

A tool that installs, updates, and removes packages for you, and works out which versions of everything they depend on can live together. `pip` and `conda` are the two you’ll meet most in Python data work, and `uv` is a fast newer one. See [sec-pkg-mgmt](#sec-pkg-mgmt).

### Parquet

A file format for tables that’s built for analysis. It stores data column by column, compresses it, and remembers each column’s type, so dates stay dates. You can’t read it in a text editor, but it’s usually much smaller and faster to load than the same data as a CSV. See [sec-data-file-formats](#sec-data-file-formats).

### PATH

An environment variable holding the [list of folders](https://en.wikipedia.org/wiki/PATH_(variable)) your shell searches, in order, when you type a command like `python`. `command not found` means the program isn’t in any of those folders, and running the “wrong” Python usually means a different one comes first on the list. (Don’t confuse it with a lowercase *path*, the address of a file, like `data/survey.csv`.) See [sec-terminal](#sec-terminal).

### `pip`

Python’s built-in package manager, which installs packages from the [Python Package Index (PyPI)](https://pypi.org/): `pip install pandas`. Run it inside an activated virtual environment, so packages land in your project and not in some other Python on your computer. See [sec-pkg-mgmt](#sec-pkg-mgmt) and [sec-virtual-environments](#sec-virtual-environments).

### Programming language

A language for writing instructions a computer can carry out, like Python, R, JavaScript, Java, or C++. Most share the same big ideas (variables, loops, functions), so learning a second one is much easier than the first, even though the exact way you write things differs.

### REPL (Read–Eval–Print Loop)

An interactive prompt that reads a line of code, runs it, prints the result, and waits for the next one (the [name](https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop) spells out that loop). Type `python` with nothing after it in a terminal and you’re in Python’s REPL; type `exit()` to leave. A Jupyter kernel works the same way, which is why it remembers everything you’ve run. See [sec-jupyter](#sec-jupyter).

### RLHF (Reinforcement Learning from Human Feedback)

One of the training steps that turns a raw text predictor into a helpful chat assistant, usually after it has first been trained on example conversations. People compare pairs of the model’s answers and pick the better one; those choices train a *reward model*, and the language model is then tuned to write answers that model scores highly. Much of that rating work is done by low-paid contract workers, sometimes reviewing disturbing material, which is one of the hidden costs behind AI tools. See [sec-ai-llm](#sec-ai-llm), [sec-ai-agents](#sec-ai-agents), and [Wikipedia’s article](https://en.wikipedia.org/wiki/Reinforcement_learning_from_human_feedback).

### Schema

The blueprint of a table or database: which columns it has, what type each one is, and what rules the values must follow (for example, “every order has a customer ID”). A schema is also a set of choices about the world. Once a `gender` column allows only two values, or a form offers only a fixed list of race categories, anyone who doesn’t fit gets squeezed in or left out, and the choice tends to stick because everything downstream depends on it. See [sec-sql-basics](#sec-sql-basics), and [sec-artifacts-politics](#sec-artifacts-politics) for the bigger picture.

### Script

A file of code you run as a program from start to finish, like `python analyze.py`. Unlike a notebook, a script runs the same way every time, top to bottom, which makes it the better choice for anything you’ll repeat or share. See [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).

### Sync client

A program, such as OneDrive, iCloud Drive, Google Drive for desktop, or Dropbox, that keeps a folder on your computer matched to a copy in the cloud and on your other devices. Syncing isn’t a backup: if you delete a file or save a bad edit, that syncs everywhere too. See [sec-filesystem-cloud](#sec-filesystem-cloud).

### Terminal

The application window you type commands into, such as Terminal on macOS or Windows Terminal. People often say “terminal” when they mean the *shell*, but they’re two things: the terminal is the window, and the shell (`zsh`, `bash`, or PowerShell) is the program inside it that reads and runs what you type. See [sec-terminal](#sec-terminal).

### Text editor

A program for writing and editing plain-text files, such as code, data, and configuration. Unlike a word processor, it saves exactly the characters you type and nothing else, which is what code needs. VS Code is the common all-purpose choice; `nano` and `vim` run inside a terminal, so they work on any server. See [sec-text-editors](#sec-text-editors).

### Traceback

The block of text Python prints when your code crashes. It lists the chain of calls that led to the error, from your code down to the line that failed, and ends with the error’s type and message. Start reading at the last line, which says what went wrong, then look up the list for the last line that’s in *your* code. See [sec-tracebacks](#sec-tracebacks).

### Version

A label, usually something like `2.2.3`, that marks one specific release of a package or of Python itself. Many packages follow [semantic versioning](https://semver.org/), where a change in the first number warns you that code written for the old version might break. Writing down the exact versions a project uses (*pinning* them) is what lets it run the same way later. See [sec-pkg-mgmt](#sec-pkg-mgmt).

### Virtual environment

A private Python setup for one project, with its own folder of installed packages, so what you install for one project can’t break another. `python -m venv .venv` creates one. You then *activate* it, with `source .venv/bin/activate` on macOS or Linux or `.venv\Scripts\Activate.ps1` in Windows PowerShell, and your prompt starts with `(.venv)` while it’s on. See [sec-virtual-environments](#sec-virtual-environments).

### YAML

A plain-text format for settings files, written as `key: value` lines with indentation to show what belongs inside what. The indentation has to be spaces, never tabs, and a stray colon or tab is behind most YAML errors. Quarto, GitHub Actions, and conda’s `environment.yml` all use it. See [sec-common-formats](#sec-common-formats).
