# 33  Automation

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-terminal](#sec-terminal), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).
>
> **See also:** [sec-git-github](#sec-git-github), [sec-remote-computing](#sec-remote-computing).

## Purpose

Automation is how you turn ‘I can do this once’’ into ‘we can do this reliably.’’ In data science and computing projects, automation reduces errors, makes work reproducible, and enables collaboration by ensuring that the same steps run the same way on every machine. This chapter introduces a practical automation ladder: (1) scripts, (2) task runners and rebuild tools, (3) scheduling, and (4) continuous integration (CI). It also shows how to incorporate AI tools responsibly to speed up routine work without weakening verification.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Identify tasks worth automating and write them as repeatable scripts.

2.  Use a task runner / build tool (e.g., [`make`](https://www.gnu.org/software/make/manual/)) to create named, repeatable commands.

3.  Understand incremental rebuilds (targets and dependencies) and why they save time.

4.  Schedule scripts to run automatically ([cron](https://crontab.guru/) on Unix-like systems; [Task Scheduler](https://learn.microsoft.com/en-us/windows/win32/taskschd/task-scheduler-start-page) on Windows).

5.  Explain what CI is and set up a basic CI workflow that runs on pushes and pull requests.

6.  Add common CI checks: formatting, linting, tests, and artifact collection.

7.  Manage automation hygiene: logs, exit codes, idempotence, and safe failure.

8.  Use AI tools to draft automation artifacts (Makefiles, YAML workflows, docs) while maintaining human verification.

## Running theme: make the correct path the easy path

If running checks and builds is one command, people will do it. If it is a long checklist, people will skip it.

## 33.1 A mental model: the automation ladder

It helps to think of automation as a ladder with five rungs, each one strictly more capable than the last and each one worth climbing only when the rung below has become a real chore.

The bottom rung is **Level 0: manual commands.** You type the same sequence by hand every time you need to do a task. This works fine when the task is rare and small, but it has the obvious failure mode: as soon as the sequence has more than two or three steps, you start forgetting them in stressful moments, and the risk of an inconsistent run grows.

The next rung is **Level 1: scripts.** You put the sequence into a `.py`, `.sh`, or `.ps1` file and run that file instead of the individual commands. The benefit is enormous and basically free: the sequence is now repeatable, shareable, and reviewable.

``` bash
#!/usr/bin/env bash
# scripts/build_report.sh
set -e
python src/clean.py --input data/raw/sales.csv --output data/processed/sales.parquet
python src/analyze.py --input data/processed/sales.parquet --output reports/q3.html
echo "report ready: reports/q3.html"
```

**Level 2: task runners and rebuild tools.** Once you have several scripts, you start wanting *named* tasks rather than long file paths. `make test`, `make report`, `make clean`. A task runner lets you label common workflows with short names and (in the case of build tools like `make`) lets you skip work whose inputs have not changed. This is the level where “rebuild only the parts that changed” becomes possible.

**Level 3: schedulers.** Once a task is scripted and named, you can run it on a time-based schedule — every night at 2 AM, every hour, every Monday morning — without anyone being at the keyboard. This is the level where unattended operation becomes possible. `cron` on macOS and Linux and Task Scheduler on Windows are the basic tools.

**Level 4: continuous integration (CI).** The top rung is having checks run *automatically on every push and pull request* to your repository, with the results visible to your collaborators. CI — most commonly [GitHub Actions](https://docs.github.com/en/actions) for students — is what catches integration errors before they land on `main`, and it is what creates the “shared quality gate” that lets a team move faster than any one person could alone.

![](graphics/PLACEHOLDER-github-actions-run.png)

Figure 33.1: ALT: GitHub Actions tab on a repository, showing a workflow run with a green checkmark beside each step of the job (checkout, setup-python, install dependencies, run tests).

The right level depends on what you are doing. Solo coursework lives happily at Level 1. A team project usually wants Level 4 for the things that matter most (tests, linting, build) and Level 1 for everything else. Climbing the ladder before you need to is busywork; refusing to climb it after a chore has bitten you is a slow form of procrastination.

## 33.2 Deciding what to automate (student-friendly heuristics)

### Automate if

A useful rule of thumb: automate something the third time you do it. The first time, you are still figuring out the steps; the second time, you might do them differently; by the third, the sequence is stable enough that writing it down repays the investment. Beyond that, four signs argue strongly for automation: you repeat the task more than twice, you need it done the *same way* every time, the cost of getting it wrong is real (grading, publication, anything other people depend on), or your teammates need a one-command workflow they can run without your help.

### Do not automate (yet) if

The opposite is also true. Automation has its own cost — writing it, debugging it, maintaining it — and you can pay that cost prematurely. Hold off if the process is still unclear (you do not know what the right steps *are* yet), if the task is changing every hour (you will spend more time updating the automation than running the task), or if automating away the manual version would hide learning you actually need. There is no virtue in automating an analysis you do not yet understand.

### The “minimum viable automation” set

For most student projects, three commands cover almost everything. **One command to set up the environment** (creating a venv or conda env and installing dependencies). **One command to run a smoke test** (a small check that the code can load, the data is reachable, and nothing is wildly broken). **One command to build the core outputs** (whichever scripts produce the figures, tables, or report you care about). Once those three exist, your project is reproducible by anyone who clones it, including future you.

## 33.3 Automation fundamentals: scripts that behave well

A handful of properties separate scripts that automate cleanly from scripts that automate “almost.” Get into the habit of building all of them in from the start.

The first is **clean exit codes and failure modes**. By long Unix convention, a successful script exits with code `0` and a failing script exits with any nonzero code. Schedulers, task runners, and CI systems all read that exit code to decide whether the run succeeded — so if your script swallows errors and exits 0 anyway, every downstream system thinks everything is fine when it is not. In bash, `set -e` makes the script exit immediately on any error; in Python, raise an exception or call `sys.exit(1)` on failure rather than just printing a warning.

``` bash
#!/usr/bin/env bash
set -e                       # exit on first error
python src/clean.py          # if this fails, the script stops
python src/analyze.py        # only runs if clean.py succeeded
```

The second is **idempotence**, which is a fancy word for “running this twice produces the same result as running it once.” An idempotent script can be safely re-run after a partial failure without manual cleanup. A non-idempotent script appends to a log file every run, or fails the second time because it tries to create a directory that already exists. Aim for the first kind: use `mkdir -p` instead of plain `mkdir`, write outputs by overwriting rather than appending, and design so that “rerun the whole thing” is always safe.

The third is **explicit inputs and outputs**. Treat file paths and parameters as first-class arguments rather than constants buried in the middle of the script. Write outputs to predictable, named locations (`data/processed/`, `reports/`, `logs/`). Never overwrite raw data — the rule from [sec-tabular-data](#sec-tabular-data) still applies: raw is sacred, derivatives go elsewhere.

The fourth is **logging and observability**. For a script that runs unattended, you cannot watch its terminal — so print useful progress markers as it goes, and save them somewhere you can read after the fact. For long tasks, mark the start and end of each stage. For scheduled or CI runs, redirect stdout and stderr to a log file so you can investigate what happened when something fails:

``` bash
python src/run_pipeline.py >> logs/pipeline.log 2>&1
```

The combination of clean exits, idempotence, explicit I/O, and logging is what turns “a script that works on my machine when I babysit it” into “a script my teammates can rely on.”

## 33.4 Repeatable tasks with `make` (and the idea of rebuilds)

### Why use a task runner

The single-sentence pitch for `make`: it turns “remember to run these five commands in this order, from this directory, with these flags” into `make report`. That is the whole value proposition, and it is enough on its own to justify learning it for any project that runs more than two scripts.

Three benefits compound as a project grows. **Memorability** — `make test`, `make lint`, `make report` are short, consistent names you will actually remember a month later. **Standardization** — everyone on the team runs the same commands with the same flags, so “it works on your machine but not mine” stops happening. **Incremental rebuilds** — the `make` tool was originally designed for compiling large C programs where rebuilding everything takes hours, and its core feature is “do not rebuild outputs whose inputs have not changed.” For a data pipeline, this is exactly the behavior you want: change one script and only the affected parts of the pipeline rerun.

`make` is not the only task runner (`just`, `invoke`, `task`, and npm scripts all solve similar problems), but it is the one that is already installed on essentially every Unix machine you will ever touch, and it has been doing this job for forty years without breaking.

### Makefile concepts: targets, prerequisites, recipes

A `Makefile` is a plain text file listing **rules**. Each rule has three parts:

``` make
target: prerequisites
    recipe
```

A **target** is what you want to produce — a file like `reports/q3.html`, or a named command like `test`. **Prerequisites** are the files (or other targets) that the target depends on; `make` rebuilds the target whenever any prerequisite is newer than the target itself. The **recipe** is the shell commands that build the target — one command per line, each line indented with a literal **tab character** (not spaces — this is `make`’s most notorious pitfall).

Here is a minimal real Makefile for a small data pipeline:

``` make
# Makefile
data/processed/sales.parquet: data/raw/sales.csv src/clean.py
    python src/clean.py --input data/raw/sales.csv --output data/processed/sales.parquet

reports/q3.html: data/processed/sales.parquet src/analyze.py
    python src/analyze.py --input data/processed/sales.parquet --output reports/q3.html
```

Run `make reports/q3.html` and `make` figures out the dependency chain: to build the report, it needs `sales.parquet`; to build `sales.parquet`, it needs the raw CSV and `clean.py`. If the parquet file is already newer than both inputs, `make` skips the clean step entirely. If you change `clean.py`, `make` reruns both steps. This is the magic.

### Phony targets for “commands”

Not every target corresponds to a file. `make test` and `make clean` are commands that do not produce a file named `test` or `clean` — they are just named shortcuts. To tell `make` “this target is a command, not a file,” declare it as `.PHONY`:

``` make
.PHONY: test clean format lint help

test:
    pytest tests/ -q

clean:
    rm -rf data/processed/ reports/ __pycache__/

help:
    @echo "Usage: make <target>"
    @echo "  setup   — create venv and install dependencies"
    @echo "  format  — auto-format code with ruff"
    @echo "  lint    — static checks with ruff"
    @echo "  test    — run unit and smoke tests"
    @echo "  run     — execute the full pipeline"
    @echo "  report  — generate figures and final report"
    @echo "  clean   — remove generated artifacts"
```

Without `.PHONY`, if you accidentally create a file or directory literally named `test`, `make` will think the target is already up to date and refuse to run it. Marking it `.PHONY` prevents that surprise.

### A recommended student target set

Convention matters more than cleverness here. Use these seven target names across your projects, and you will stop thinking about “what did I call this?” and just start typing:

``` make
.PHONY: setup format lint test run report clean

setup:
    python -m venv .venv
    . .venv/bin/activate && pip install -r requirements.txt

format:
    ruff format src/ tests/

lint:
    ruff check src/ tests/

test:
    pytest tests/ -q

run:
    python src/pipeline.py

report: data/processed/results.parquet
    python src/report.py

clean:
    rm -rf data/processed/ reports/ .pytest_cache/
```

With those seven names in every project, a new contributor who clones the repository can get productive in minutes: “`make setup`, then `make test`, then `make run`.” They do not need to read the whole README to find the incantation; the Makefile *is* the incantation.

### Incremental builds for data pipelines

The pattern that pays off most for data work is one target per stage of the pipeline, with each stage declaring its inputs as prerequisites:

``` make
RAW       := data/raw/sales.csv
CLEAN     := data/processed/sales.parquet
FEATURES  := data/processed/features.parquet
REPORT    := reports/q3.html

$(CLEAN): $(RAW) src/clean.py
    python src/clean.py --input $(RAW) --output $(CLEAN)

$(FEATURES): $(CLEAN) src/features.py
    python src/features.py --input $(CLEAN) --output $(FEATURES)

$(REPORT): $(FEATURES) src/report.py
    python src/report.py --input $(FEATURES) --output $(REPORT)

.PHONY: all
all: $(REPORT)
```

Run `make all` and `make` walks the dependency chain in order. Now the magic kicks in:

- Change `src/features.py`: `make` rebuilds features and report, but skips `clean` (because `sales.parquet` is still newer than its inputs).
- Change the raw CSV: `make` rebuilds everything.
- Change nothing: `make` says “Nothing to do for ‘all’” and exits in milliseconds.

The `$(CLEAN)` syntax defines a variable — it saves you from retyping the file path every time and makes the pipeline easier to read. On a small project this feels like overkill; on a mid-sized project it saves you minutes or hours per iteration and prevents the “I forgot to rerun the cleaning step after I changed the raw data” bug entirely.

## 33.5 Scheduling scripts

Once a task is scripted, the next capability is running it without you — every morning at 6 AM, every hour, every first-of-the-month. Both Unix and Windows ship with built-in schedulers that cover everything a student project will need.

### Scheduling on macOS and Linux: `cron`

`cron` is the long-running background service that reads a “crontab” (a list of scheduled jobs) and runs each job when its time fields match the current time. Every user on a Unix system has their own crontab. Edit yours with:

``` bash
crontab -e      # opens your crontab in an editor
crontab -l      # prints your current crontab
```

The format of each line is five time fields followed by the command to run:

``` text
# ┌────── minute (0 - 59)
# │ ┌──── hour (0 - 23)
# │ │ ┌── day of month (1 - 31)
# │ │ │ ┌── month (1 - 12)
# │ │ │ │ ┌── day of week (0 - 6, Sunday = 0)
# │ │ │ │ │
  0 6 * * *   /home/agandler/projects/sales/run_pipeline.sh
```

That line runs the script every day at 6:00 AM. `*` means “any value.” `*/15 * * * *` means “every 15 minutes.” `0 * * * *` means “at the top of every hour.” There are many cheat-sheets for writing cron expressions; <https://crontab.guru> will let you type an expression and explain in plain English when it will fire.

**The single most common cron bug is environment.** When `cron` runs your script, it does *not* inherit your interactive shell’s environment — it runs with a minimal `PATH`, no `PYTHONPATH`, no conda activation, no `LANG` — and a script that works perfectly when you run it by hand can fail mysteriously under `cron`. The symptom is usually “command not found” or “ModuleNotFoundError” for something that is clearly installed.

The fix is to be explicit about everything the script needs. Write a wrapper script rather than calling Python directly from cron:

``` bash
#!/usr/bin/env bash
# ~/projects/sales/run_pipeline.sh
set -euo pipefail

# Be explicit about the working directory
cd /home/agandler/projects/sales

# Be explicit about the environment
source .venv/bin/activate
export PATH="/usr/local/bin:/usr/bin:/bin:$PATH"

# Run the actual job, redirecting all output to a dated log
mkdir -p logs
timestamp=$(date +%Y%m%d-%H%M%S)
python src/pipeline.py >> "logs/pipeline-${timestamp}.log" 2>&1
```

Then the crontab entry just runs the wrapper:

``` text
0 6 * * *   /home/agandler/projects/sales/run_pipeline.sh
```

Three things are going right here: the wrapper `cd`s to a known directory, it activates the virtual environment so `python` finds the right packages, and it redirects both stdout and stderr to a log file you can read afterward. If the job fails at 6 AM tomorrow, the log file is what tells you why.

### Scheduling on Windows: Task Scheduler

Windows has its own equivalent, the **Task Scheduler**, which is both a GUI app and a command-line tool (`schtasks.exe`). The GUI is the friendlier place to start.

Open “Task Scheduler” from the Start menu, click “Create Basic Task…”, give it a name, pick a trigger (Daily, Weekly, When the computer starts…), pick an action (“Start a program”), and point it at the script you want to run. The two settings students most often get wrong are:

- **“Start in (optional)”** — this is the working directory the task runs from. Leave it blank and your script runs from `C:\Windows\System32`, which is almost certainly not what you want. Set it explicitly to your project directory.
- **“Run whether user is logged on or not”** and **“Run with highest privileges”** — these control whether the task runs in the background when you are logged out, and whether it has admin rights. For most student projects you want “Run whether user is logged on or not” (so it runs at 6 AM while you are asleep) and you do *not* want elevated privileges unless you have a specific reason.

For scripted creation, `schtasks` on the command line does the same thing:

``` powershell
schtasks /Create `
  /TN "SalesPipeline" `
  /TR "C:\Users\agandler\projects\sales\run_pipeline.bat" `
  /SC DAILY /ST 06:00 `
  /SD 04/10/2026
```

The `.bat` wrapper plays the same role as the `.sh` wrapper on Unix: set the working directory, activate the environment, run the script, and redirect output to a log file.

``` batch
REM run_pipeline.bat
cd /d C:\Users\agandler\projects\sales
call .venv\Scripts\activate.bat
python src\pipeline.py >> logs\pipeline.log 2>&1
```

### Scheduling hygiene

Three habits make scheduled jobs maintainable:

**Write logs to a known folder, and rotate them.** Every scheduled job should write its output somewhere you can find it later. A `logs/` directory in the project root is fine. If the job runs frequently, add a timestamp to the filename so you do not overwrite yesterday’s log, and set up some kind of cleanup so the folder does not grow without bound — either a monthly `find logs/ -mtime +30 -delete`, or use `logrotate` on Linux.

**Add timestamps to outputs and include them in the log.** Start each log line with the date and time, so that when you look at a log a week later you can correlate events:

``` bash
echo "$(date -Iseconds) starting cleaning step"
python src/clean.py
echo "$(date -Iseconds) cleaning done"
```

**Prevent overlapping runs with a lock file.** If your script sometimes takes longer than the interval between runs — a cron that fires hourly but a slow job that takes an hour and ten minutes — you can end up with two copies running at once and corrupting each other. Use a lock file to detect and refuse the overlap:

``` bash
LOCK="/tmp/sales-pipeline.lock"
if [ -e "$LOCK" ]; then
    echo "$(date -Iseconds) another run is in progress; exiting" >&2
    exit 0
fi
trap 'rm -f "$LOCK"' EXIT
touch "$LOCK"
# ...run the pipeline...
```

Finally, **decide what happens when the job fails.** The minimum is “write the failure to a log I actually read.” A step up is “send me an email or a Slack message” — many small utilities like `mail` or webhook-based alert services can do this from a wrapper script. The worst pattern is “the job fails silently and I notice three weeks later,” which is what happens when nobody is reading the logs.

## 33.6 Rebuilds and repeatable workflows beyond `make`

### Task runners as interfaces

The most important thing `make` gives a project is not the incremental rebuild logic — it is the **stable command interface**. `make test`, `make lint`, and `make report` become the canonical way to run those actions, and you can put that same vocabulary everywhere: in the README, in the CI workflow, in the PR template, in your own muscle memory. Any newcomer to the project learns six short commands and becomes productive.

You do not need `make`’s dependency-graph features to get that benefit. Plenty of projects use `make` purely as a task runner — every target is `.PHONY`, none of them declare prerequisites, and the whole Makefile is just a list of named shortcuts. That is a completely reasonable use of the tool.

If `make`’s syntax annoys you (the tab-vs-space rule genuinely trips people up), newer alternatives offer the same task-runner benefit without the historical baggage:

- **`just`** — a standalone task runner with a friendlier syntax, essentially “Makefile without the traps.” Targets are listed in a `justfile` and run with `just <target>`.
- **`invoke`** — a Python task runner where tasks are Python functions. Useful if you want complex logic inside a task.
- **npm scripts** — if your project has a `package.json`, `npm run <script>` runs whatever is in the `scripts` block.

Pick one and commit to it. The value is in having *a* standard interface for the project; the specific tool matters much less. For a Python data project where the only task-runner need is named shortcuts, `make` is the path of least resistance precisely because every machine already has it.

### Artifacts vs caches

As you start using CI and more complex workflows, you will run into two related concepts that are easy to confuse: **caches** and **artifacts**.

A **cache** is a store of intermediate files you want to reuse across runs to make things faster. The canonical example is a pip package cache: instead of downloading and installing pandas from scratch every time CI runs, you cache the installed packages keyed on `requirements.txt`, so unchanged dependencies are restored from cache in seconds. Caches are optimizations — nothing breaks if the cache is empty, it is just slower.

``` yaml
# GitHub Actions example — cache the pip download directory
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: pip-${{ hashFiles('requirements.txt') }}
```

An **artifact** is an output of a run that you want to save, inspect, or share with other jobs or people. A PDF report, a CSV of results, a directory of logs, a wheel file for a package — these are all artifacts. Unlike caches, artifacts are meant to be consumed: you download them after the run, attach them to a release, or feed them into a later job.

``` yaml
# GitHub Actions example — upload the built report as an artifact
- uses: actions/upload-artifact@v4
  with:
    name: sales-report
    path: reports/q3.html
```

The quick rule of thumb: **cache** the things you do not want to rebuild, **artifact** the things you want to look at. Confuse them and you will either waste space storing ephemeral build caches as long-lived artifacts or silently lose outputs that you assumed would be saved.

## 33.7 Continuous Integration (CI): automation as a quality gate

### What CI is, in one paragraph

**Continuous integration** is the practice of having every change integrated into a shared branch be automatically verified by a build-and-test run. The two parts matter equally: *frequent integration*, which means small changes that land often (not month-long branches that merge in a single giant squash), and *automated verification*, which means that every push and every pull request triggers a workflow that runs your tests, your linter, and whatever other checks you care about. The result is a shared quality gate that everyone on the team passes through before their code reaches `main`, which catches breakages while they are still easy to fix — at the moment they are introduced, in the context of one small change, by the person who wrote the code.

CI is the biggest single quality improvement most projects can make, and on GitHub it is free for public repositories.

### CI events and triggers

CI systems run *workflows* in response to *events*. The two events that matter for students are **push** (code was pushed to any branch) and **pull_request** (a pull request was opened or updated). Almost every project wants both: push runs catch problems on long-running branches, and pull-request runs catch problems before code merges into `main`.

``` yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
```

The configuration above says: “run this workflow whenever something is pushed to `main`, or whenever a pull request targets `main`.” That is the baseline every small project should start with.

For larger repositories, **path filters** let you skip CI runs that cannot possibly affect the outcome — for example, skip Python tests when only the README changed:

``` yaml
on:
  pull_request:
    paths:
      - 'src/**'
      - 'tests/**'
      - 'requirements.txt'
      - '.github/workflows/ci.yml'
```

Path filters are an optimization, not a correctness feature. Do not add them until you have a real “CI is too slow” problem.

### Jobs, steps, and runners

A **workflow** is a YAML file. It contains one or more **jobs**, which run independently (in parallel, by default). Each job runs on a **runner** — a fresh virtual machine that GitHub provisions for the duration of the job — and consists of **steps**, each of which is either a shell command or a reusable “action” from the marketplace.

``` text
workflow ─── job: "test" ───── runner: ubuntu-latest
                │                   │
                │                   ├── step: checkout the code
                │                   ├── step: set up Python
                │                   ├── step: install dependencies
                │                   └── step: run pytest
                │
                └── job: "lint" ──── runner: ubuntu-latest
                                    ├── step: checkout the code
                                    ├── step: set up Python
                                    └── step: run ruff
```

Each job starts from a clean machine — nothing carries over from your previous run unless you explicitly restore a cache or download an artifact. This is a feature: CI enforces “does this work from scratch?” on every run, which is what catches “works on my machine” problems.

### A minimal CI workflow for students

Here is a complete, working GitHub Actions workflow for a small Python project. Drop it in `.github/workflows/ci.yml` and commit; the next push runs the checks automatically.

``` yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Check out the code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          cache: pip

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install ruff pytest

      - name: Lint
        run: ruff check src/ tests/

      - name: Format check
        run: ruff format --check src/ tests/

      - name: Run tests
        run: pytest tests/ -q

      - name: Upload logs on failure
        if: failure()
        uses: actions/upload-artifact@v4
        with:
          name: logs
          path: logs/
```

Six real steps, each one named so that the CI results page tells you exactly which step failed. The lint, format-check, and test steps are your actual quality gate; the `if: failure()` at the end uploads your logs directory so you can download it and investigate when something breaks. That template is enough for 90% of student projects.

### CI performance hygiene

A slow CI is a CI people learn to ignore, and an ignored CI is worse than no CI at all. Three habits keep it fast:

**Cache your dependencies.** The `cache: pip` line in the `setup-python` action above restores your pip cache from a previous run keyed on `requirements.txt`. An install that took 90 seconds from scratch takes 5 seconds from cache. Do the same for conda caches, node_modules, or any other dependency store — every major action has a built-in cache option or works with the generic `actions/cache`.

**Use matrix builds sparingly.** A matrix lets you run the same job across multiple versions of Python or multiple operating systems:

``` yaml
strategy:
  matrix:
    python-version: ["3.10", "3.11", "3.12"]
```

This is powerful for library authors who need to support many versions, but it multiplies your CI minutes. For a student project with one supported Python version, just pick that version and skip the matrix.

**Aim for under five minutes per run.** If CI takes fifteen minutes, people push a change, switch to something else, and never come back to check. If it takes three minutes, they wait for it. The exact target depends on your tolerance, but “measure it and feel bad when it grows” is the right discipline. Common interventions when CI is slow: cache more aggressively, split slow tests into a separate job that only runs on `main`, or prune tests that take too long for what they prove.

### CI security basics

Three rules are enough for student projects:

**Never print secrets in logs.** If you read an environment variable that contains a token and `echo` it to the terminal, CI logs capture it forever — and CI logs for public repositories are readable by anyone on the internet. Tokens and API keys should be passed to programs that need them, not logged. When you suspect a secret was leaked in a log, rotate it immediately.

``` yaml
# Bad:
- run: echo "API key is $MY_API_KEY"

# Good:
- run: python deploy.py
  env:
    MY_API_KEY: ${{ secrets.MY_API_KEY }}
```

**Understand untrusted pull requests.** When a pull request comes from a fork, GitHub runs the PR’s code inside CI — which means a malicious PR can, in principle, access anything the CI job has access to. By default, GitHub restricts this: secrets are *not* passed to workflows triggered by pull requests from forks, precisely to prevent this attack. Do not work around that restriction without understanding exactly what you are exposing.

**Use least privilege for tokens.** GitHub Actions gives each workflow run a `GITHUB_TOKEN` with permissions to read the repository. If your workflow only needs to *read* the repo, set the permissions explicitly to read-only at the top of the workflow:

``` yaml
permissions:
  contents: read
```

That one line prevents a compromised action from, say, pushing commits to your repo. Tighten permissions further as you learn what your workflow actually needs.

## 33.8 Local quality gates: pre-commit hooks

CI is the team’s safety net, but it only runs *after* you push. The local equivalent is a **git hook**: a small check that runs automatically right before every `git commit` and aborts the commit if something looks wrong. The most common tool for managing these is [`pre-commit`](https://pre-commit.com), a small framework that takes a config file and runs a pipeline of checks on the files you are about to commit ([pre-commit contributors, n.d.](#ref-precommit_framework)).

You do not need pre-commit to do good work, and for solo coursework you can skip it entirely. But once you start collaborating, the same class of small mistakes will keep landing on `main`: trailing whitespace in a diff, an accidentally committed `.env` file, an unformatted Python file someone forgot to run through their linter (see [sec-linting](#sec-linting)). A pre-commit hook is a tripwire that catches each of these at the earliest possible moment — before they ever become a commit.

The setup is two commands and one file. Install the tool into your project’s environment and wire it into git:

``` bash
python -m pip install pre-commit
pre-commit install
```

Then drop a `.pre-commit-config.yaml` at the repo root listing the checks you want. A reasonable starter set for a Python data-science project is just two upstream “repos”:

``` yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.7
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

The first block catches the file-hygiene mistakes: trailing whitespace, missing final newlines, broken YAML, files larger than 500 KB, and private SSH keys that wandered into the repo. The second block runs `ruff` (your linter and formatter) on every staged Python file. Together they handle most of the small things that would otherwise show up in a code review.

When you `git commit`, the hooks run. If a hook auto-fixes a file, the commit aborts so you can re-stage and re-commit:

``` text
$ git commit -m "Add cleaning helper"
trim trailing whitespace.................................................Failed
- files were modified by this hook
ruff.....................................................................Passed

$ git add src/cleaning.py
$ git commit -m "Add cleaning helper"
trim trailing whitespace.................................................Passed
ruff.....................................................................Passed
[main a1b2c3d] Add cleaning helper
```

This “commit twice” rhythm feels weird for a day, then becomes invisible. A few practical points worth knowing. `git commit --no-verify` skips the hooks entirely — treat it as an emergency exit, not a daily convenience. The config is versioned with the code, so when a teammate clones the repo they only need to run `pre-commit install` once and they pick up all the same checks. And you can run every hook against every file at any time with `pre-commit run --all-files`, which is what you want when you first add pre-commit to an existing project. Anything beyond that — debugging individual hooks, writing your own, wiring pre-commit into CI as a redundant check — you can pick up from the official documentation at <https://pre-commit.com> when the need arises.

## 33.9 Incorporating AI tools into automation (responsibly)

Automation configuration files — Makefiles, GitHub Actions YAML, Dockerfiles, cron wrappers — are some of the highest-leverage uses of AI assistance for students. They are repetitive, their syntax is unforgiving, and small errors are tedious to debug. LLMs are surprisingly good at producing a reasonable first draft. They are also capable of producing confident nonsense, and the consequences of nonsense in a workflow file are higher than in regular application code, because a workflow file can run with write access to your repository, your cloud account, or your production environment. Use AI carefully here. See [sec-ai-llm](#sec-ai-llm) for the broader treatment.

### What AI is good for

A handful of tasks where AI assistance is genuinely useful:

- **Drafting boilerplate.** A blank CI YAML file in front of you is intimidating; “write me a GitHub Actions workflow that runs pytest on Python 3.11 with pip caching” produces a starting point in seconds. The draft will usually be roughly right and obviously wrong in a few specific ways, which is exactly the situation where a draft is easier to edit than a blank page.
- **Explaining unfamiliar syntax.** You see a `${{ steps.foo.outputs.bar }}` expression in someone else’s workflow and have no idea what it means; ask the AI to explain it. Cross-reference against the actual docs for the final word, but the AI explanation usually points you at the right section faster than a cold web search.
- **Generating test cases and edge checks.** “Here’s my `clean_sales_data` function; what edge cases should I test?” gets you a decent list of candidates — empty input, duplicate rows, null values in the key columns — that you then implement and verify.
- **Summarizing PRs and surfacing risk areas.** A short “what did this PR actually change?” summary from an AI can be useful as a starting point for a reviewer, as long as the reviewer still reads the diff.

### What AI is not good for

An equally important list of things AI assistance is *not* reliable for:

- **Inventing correct tool flags or syntax without testing.** LLMs regularly hallucinate command-line flags, action names, and API methods that do not exist. A Makefile target or a `sbatch` directive that “looks right” but is silently wrong is a special kind of time sink.
- **Making security decisions.** Whether to grant a token `write` access, whether a `secrets` value is safe to expose in a particular context, whether a permission model is least-privilege — these are judgment calls where an AI’s confidence is not calibrated to the real risk. Make security decisions yourself, after consulting the official docs.
- **“Fixing” failing CI by random changes.** A tight feedback loop of “CI failed, ask the AI to fix it, push, CI failed again, ask again” is one of the fastest ways to end up with a workflow that technically passes but does not actually test anything. If CI is failing, understand *why* before letting the AI propose fixes.

### Guardrails for AI-assisted automation

Five habits make AI assistance safer:

**Always run locally before trusting CI changes.** If an AI suggests changes to a Makefile or a `run_pipeline.sh`, run them on your own machine first and verify the behavior matches what you expected. Do not commit changes whose behavior you have not observed at least once.

**Keep diffs small.** One automation change per PR. If the AI proposes a sweeping refactor, break it into multiple PRs so each change can be reviewed in isolation.

**Require “how to test” in PR descriptions.** A PR that changes automation should include a short “how I verified this works” section: the commands you ran, the output you expected, what you saw. This is useful regardless of whether AI was involved, but it becomes essential when the code was partly generated.

``` markdown
## How I tested this

- Ran `make test` locally; 42 tests passed.
- Ran `make run` with the small dataset; output matches `reports/expected_q3.html`.
- Pushed a draft branch; CI completed in 3:14 and green.
```

**Treat AI output as a draft; confirm against docs.** The relevant docs for a workflow change are the official GitHub Actions docs, the `make` manual, the cron documentation, and so on. When an AI suggests a specific flag or setting, search the docs for it before trusting it. If the flag does not appear in the docs, assume it is hallucinated and find the real one.

**Never paste secrets into prompts.** LLM providers log your prompts. Pasting an API key or a password into a chat window is functionally equivalent to leaking it on a public pastebin. When you need to show the AI a file that contains secrets, redact them first.

### A practical workflow: AI as a junior assistant

Treat the AI like a capable junior teammate who has read every tutorial on the internet but has never actually worked on your specific project. The responsibilities stay with you, and the sequence looks like this:

1.  **You specify the intent and constraints.** “I need a GitHub Actions workflow that installs from `requirements.txt`, runs `ruff check` and `pytest`, caches pip, and uploads logs on failure. Python 3.11, Ubuntu, runs on push to main and pull_request to main.”
2.  **AI drafts the file.** You get a YAML workflow, probably about eighty percent right.
3.  **You validate against documentation.** Open the official GitHub Actions docs, cross-check each `uses: …` action against its README, confirm that syntax the AI used (`cache:`, `if: failure()`, `permissions:`) is real and means what you think it means.
4.  **You run a smoke test.** Push the workflow to a feature branch and watch it run end-to-end. Does it actually cache pip? Does the test step actually fail when you break a test? Does the “upload on failure” step actually produce an artifact?
5.  **You open a PR and request review.** Describe what the automation does, how you tested it, and any places you are uncertain. Reviewers still review. Nothing about “AI helped me write this” removes the human accountability for the result.

The whole process is a few minutes longer than just having the AI write the file and merging blind. That extra time is the entire point.

## 33.10 Common failure modes and fixes

The failure modes below are the ones that bite every student project eventually. Knowing what they look like in advance makes them much cheaper to fix.

### “Works on my machine” automation

**Symptom.** Your Makefile runs perfectly on your laptop. On a teammate’s laptop — or in CI — it fails with an import error, a missing command, or a subtly different output.

**Root cause.** Something about your local environment is different and your automation depends on it implicitly: a Python package you installed globally months ago, a tool in your `PATH` that is not on the new machine, an environment variable you set once and forgot, a data file in a location unique to your setup, even the version of `awk` being GNU vs BSD.

**Fix.** Make every assumption explicit. Pin your Python dependencies in `requirements.txt` or `environment.yml` with exact versions (see [sec-pkg-mgmt](#sec-pkg-mgmt)). Record any other system prerequisites in the README. And run the whole pipeline at least once in CI or a fresh container — the “clean environment” is what catches assumptions you did not know you were making.

``` bash
# A useful habit: rebuild from scratch periodically
make clean
rm -rf .venv/
make setup
make run
# If this works, your project is reproducible. If not, you just found a bug.
```

### Scheduling failures from wrong `PATH` or wrong working directory

**Symptom.** Your script works fine when you run it interactively, but under `cron` or Task Scheduler it fails with “command not found,” “No such file or directory,” or “ModuleNotFoundError.”

**Root cause.** Schedulers do not inherit your interactive shell’s environment. `PATH` is minimal, the working directory is your home directory (not the project), environment variables you set in `.bashrc` are not loaded, and the virtual environment you “activated this morning” is not active.

**Fix.** Write a wrapper script that is explicit about everything: `cd` to the project directory with an absolute path, activate the environment, set any `PATH` additions you need, and redirect output to a log. Then schedule the wrapper, not the raw script. The wrapper pattern from earlier in this chapter is the template.

### CI failures due to missing files or secrets

**Symptom.** CI fails with “file not found” or “authentication failed” for something that works perfectly on your laptop.

**Root cause.** Your code depends on a file or secret that exists on your laptop but was never committed to the repo or made available to CI. Common culprits: a data file sitting in `data/raw/` that is gitignored, a `.env` file with an API token, a config file that was never checked in, a Python package installed manually and not listed in `requirements.txt`.

**Fix.** For files, either commit them (if they are small and non-sensitive) or write your automation so it can fetch them at runtime from a URL or a data store. For secrets, use your CI system’s secrets mechanism — in GitHub Actions, that is `secrets.MY_TOKEN` referenced from environment variables. In CI, the golden rule is: if a human can only reproduce the run by having access to something that only exists on your laptop, the automation is broken.

``` yaml
# GitHub Actions: pass a secret into the environment of a step
- name: Deploy
  run: python deploy.py
  env:
    API_TOKEN: ${{ secrets.DEPLOY_TOKEN }}
```

### Slow CI that everyone ignores

**Symptom.** Your team treats the CI check as a suggestion. Pull requests get merged red. People stop looking at CI results.

**Root cause.** CI takes long enough that waiting for it is painful, so people stop waiting. Once the habit of “merge anyway” sets in, every green-or-red distinction is lost and CI becomes decorative.

**Fix.** Measure the runtime and attack the slowest steps. Common wins: cache dependencies aggressively, split slow tests into a separate job that only runs on `main` (so PR CI stays fast), run independent jobs in parallel, and prune tests that take longer than their value justifies. A CI that finishes in under three minutes will be trusted; a CI that takes fifteen will be worked around.

### Automation that overwrites important artifacts

**Symptom.** You run your pipeline and it happily overwrites a previously generated report — or worse, touches your raw data.

**Root cause.** The script writes to a path without checking what was there, and nothing stops it from clobbering something important.

**Fix.** Three habits. First, **keep raw data immutable**: the cleaning pipeline reads from `data/raw/` and writes to `data/processed/`, never the other way around (see [sec-tabular-data](#sec-tabular-data)). Second, **write outputs to dedicated folders** named after the run, so a new run cannot stomp an old one — `reports/2026-04-10/q3.html` is safer than `reports/q3.html`. Third, **for genuinely destructive steps, require explicit confirmation**: a `make clean` target that nukes `data/processed/` should at minimum be a distinct target from `make run`, so no one runs it by accident.

``` make
# Give destructive targets scary names and require them to be explicit
.PHONY: clean distclean

clean:
    rm -rf data/processed/ reports/

distclean: clean
    @echo "WARNING: this will remove .venv and all caches. Ctrl-C to abort."
    @sleep 3
    rm -rf .venv/ .pytest_cache/ __pycache__/
```

The three-second pause before the `rm -rf` is not going to stop a determined mistake, but it is enough to catch the “wait, wrong terminal” moment before the damage is irreversible.

> **NOTE:**
>
> - [GitHub Actions documentation](https://docs.github.com/en/actions) — the authoritative reference for building CI workflows on GitHub.
> - [GNU Make manual](https://www.gnu.org/software/make/manual/) — the classic reference for `make`, targets, and incremental rebuilds.
> - [crontab.guru](https://crontab.guru/) — an interactive explainer for cron expressions that removes most of the mystery.

## 33.11 Worked examples (outline)

### Turn a 6-step checklist into `make` targets

- Create `make format`, `make test`, `make report`.

- Add a default target `make all`.

### Schedule a daily pipeline run

- Create a script with logs.

- Add a cron entry (macOS/Linux) or Task Scheduler entry (Windows).

- Verify outputs and failure behavior.

### Add GitHub Actions CI

- Run on push and pull request.

- Install deps, run tests.

- Upload artifacts on failure.

### Speed up CI with caching

- Add dependency caching.

- Compare runtimes before/after.

### Add pre-commit hooks + CI enforcement

- Run lightweight checks before commit.

- Ensure CI runs the same checks.

### Use AI to draft a workflow, then validate

- Draft YAML with AI.

- Verify triggers/permissions.

- Run locally and via PR.

## 33.12 Templates

### Template A: Makefile skeleton (task interface)

    .PHONY: help format lint test run report clean

    help:
    @echo "make format | lint | test | run | report | clean"

    format:
    ...

    lint:
    ...

    test:
    ...

    run:
    ...

    report:
    ...

    clean:
    ...

### Template B: Cron entry (conceptual)

    # minute hour day month weekday  command

    # redirect stdout/stderr to a log file

### Template C: Windows scheduled task (conceptual)

    # schtasks /create ...

    # run a script at a scheduled time with a named task

### Template D: GitHub Actions workflow skeleton

    name: CI
    on:
    push:
    pull_request:

    jobs:
    test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Set up runtime
    ...
    - name: Install deps
    ...
    - name: Run checks
    ...

### Template E: PR checklist for automation changes

    * What problem does this automation solve?
    * How do I test it locally?
    * What does it do on failure?
    * Any permissions/secrets involved?
    * Links to documentation

## 33.13 Exercises

1.  Identify three repeated tasks in your project and turn them into `make` targets.

2.  Create a script that writes logs and exits nonzero on failure.

3.  Schedule the script (cron or Task Scheduler) and confirm it runs.

4.  Add a CI workflow that runs tests on every pull request.

5.  Add dependency caching and measure CI runtime change.

6.  Add pre-commit hooks; mirror the same checks in CI.

7.  Use an AI tool to draft a workflow file, then validate it against official docs and run a test PR.

## 33.14 One-page checklist

- I can turn multi-step tasks into one-command targets.

- My scripts have clear inputs/outputs and safe re-run behavior.

- Scheduled jobs use explicit paths, working directory, and logging.

- CI runs on pushes/PRs and includes a minimal quality gate.

- CI is fast enough to be used continuously; caching is used appropriately.

- Automation changes are documented and reviewed like code.

- AI assistance is used to draft, not to bypass verification.

## 33.15 Quick reference: common automation concepts

- Targets, prerequisites, recipes (rebuild logic).

- Schedulers: cron fields and Windows task schedules.

- CI: triggers, runners, jobs, artifacts, caches.

- Hygiene: idempotence, exit codes, logs, secrets.

pre-commit contributors. n.d. *Pre-Commit: A Framework for Managing and Maintaining Multi-Language Pre-Commit Hooks*. Project documentation. <https://pre-commit.com/>.
