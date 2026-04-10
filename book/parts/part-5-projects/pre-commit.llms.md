# 30  Pre-commit Hooks

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-git-github](#sec-git-github), [sec-linting](#sec-linting).
>
> **See also:** [sec-testing](#sec-testing), [sec-automation](#sec-automation), [sec-secrets](#sec-secrets).

## Purpose

You have a formatter configured in your editor (see [sec-linting](#sec-linting)) and you run tests before pushing (see [sec-testing](#sec-testing)). You are already 80% of the way to high code hygiene. The remaining 20% is the *forgetting* problem: the day you are in a hurry and push code without running the formatter, or you accidentally commit a `.env` file, or a merge introduces trailing whitespace nobody noticed.

Pre-commit hooks are the fix. A pre-commit hook is a small check that runs *automatically* right before every `git commit`. If the check fails, the commit is aborted and you get a chance to fix the problem. If it passes, the commit goes through as normal. The checks are cheap — typically milliseconds to seconds — and they catch exactly the class of mistake that would otherwise land on your main branch and make someone’s day worse.

This chapter introduces [pre-commit](https://pre-commit.com), the framework most projects use. It is a small tool that takes a config file and runs a pipeline of checks on the files you are about to commit. You will learn enough to install it, configure it with the hooks you actually want, and wire it into a team project.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what a git hook is and when it runs.
2.  Install `pre-commit` and initialize it in a repository.
3.  Write a `.pre-commit-config.yaml` with the five most useful hooks for a Python project.
4.  Run hooks manually with `pre-commit run --all-files`.
5.  Skip hooks temporarily (with `--no-verify`) — and know why this is almost always a bad idea.
6.  Wire pre-commit into CI so every PR is guaranteed to pass the same checks.
7.  Debug a failing hook by reading its output and rerunning it on a single file.

## Running theme: make the computer enforce the things humans keep forgetting

If a mistake has landed on main before, it will land there again. A pre-commit hook is a tripwire that stops it at the earliest possible moment — before it is even in a commit.

## 30.1 1. What a git hook is

Git has a built-in feature called **hooks**: scripts that run automatically at specific points in the git workflow. The ones that exist are listed in any repo under `.git/hooks/` as example files. The interesting ones for daily development are:

| Hook         | Runs when                                                |
|--------------|----------------------------------------------------------|
| `pre-commit` | right before `git commit` — abort to cancel the commit   |
| `commit-msg` | after you write the commit message — validate its format |
| `pre-push`   | before `git push` — last-chance checks                   |

Writing your own hooks as shell scripts is possible but awkward: every teammate has to install them manually, and the scripts do not version with the code. The `pre-commit` tool solves both problems by shipping a config file in the repo that automatically installs itself once per developer.

## 30.2 2. Installing `pre-commit`

``` bash
python -m pip install pre-commit
```

Install it into your repo (this creates `.git/hooks/pre-commit`):

``` bash
pre-commit install
```

Verify:

``` bash
pre-commit --version
```

From now on, every `git commit` in this repo triggers the hooks listed in `.pre-commit-config.yaml`.

## 30.3 3. The config file

Create `.pre-commit-config.yaml` at the repo root. Here is a reasonable starting set for a Python data-science project:

``` yaml
repos:
  # Basic file hygiene
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: detect-private-key

  # Python linting and formatting
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.7
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  # Strip Jupyter notebook outputs before committing
  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout
```

Three repos, three categories of check. Let’s unpack each.

### File hygiene (pre-commit-hooks)

| Hook | Catches |
|----|----|
| `trailing-whitespace` | trailing spaces that make diffs noisy |
| `end-of-file-fixer` | ensures every text file ends with a newline |
| `check-yaml` | unparseable YAML in `_quarto.yml`, GitHub Actions, etc. |
| `check-added-large-files` | accidental commits of giant files |
| `check-merge-conflict` | forgotten `<<<<<<<` markers after a bad merge |
| `detect-private-key` | SSH / PGP private keys that leaked into the repo |

These are cheap and always-useful. Add them first.

### Python linting and formatting (ruff)

Ruff’s pre-commit hook runs `ruff check --fix` and `ruff format` on every Python file in the commit. You already had this configured to run on save in your editor (see [sec-linting](#sec-linting)), but the pre-commit hook is the backstop — it runs even when someone commits from the command line, a teammate’s IDE, or an LLM-generated patch.

### Notebook output stripping (nbstripout)

Jupyter notebooks store cell outputs by default. For data-science projects this causes three problems: secrets embedded in cell output (see [sec-secrets](#sec-secrets)), huge diffs every time a plot re-renders, and merge conflicts on base64-encoded image blobs. `nbstripout` deletes cell outputs on commit. You still see outputs locally; git just does not store them.

## 30.4 4. Running hooks

### On every commit (the default)

After `pre-commit install`, hooks run automatically whenever you `git commit`. If any hook fails, the commit is aborted.

Some hooks *auto-fix* the files (ruff, trailing whitespace) — in that case pre-commit aborts the commit, leaves the fixed files in your working tree, and you run `git add` + `git commit` again.

    $ git commit -m "Add feature"
    trim trailing whitespace.................................................Failed
    - hook id: trailing-whitespace
    - exit code: 1
    - files were modified by this hook

    Fixing src/analysis.py

    ruff.....................................................................Passed

Now:

``` bash
git add src/analysis.py
git commit -m "Add feature"
```

The second commit passes because the file is already clean. This “commit-twice” rhythm feels weird for a day, then becomes invisible.

### On everything at once

When you first set pre-commit up on an existing project, you want to run every hook on every file (not just the staged ones) to clean the initial state:

``` bash
pre-commit run --all-files
```

Commit the resulting changes as one “Apply pre-commit to existing code” commit.

### On one hook at a time

To debug a single failing hook, run just that one:

``` bash
pre-commit run ruff --all-files
```

## 30.5 5. Skipping hooks (rarely)

Git lets you skip hooks with `--no-verify`:

``` bash
git commit --no-verify -m "WIP emergency fix"
```

**Use this only in true emergencies.** Every `--no-verify` is a promise that the problem you skipped is acceptable, and it is almost never acceptable. Common legitimate uses:

- A CI system is broken and you need to commit a config change to fix it.
- A hook itself has a bug you will fix in the next commit.

Common illegitimate uses:

- “The formatter is annoying today.”
- “I’ll fix the lint errors later.”

If you find yourself reaching for `--no-verify` regularly, either the hooks are misconfigured (turn off the noisy ones) or the code is in bad shape (fix the code, not the hooks).

## 30.6 6. Pre-commit in CI

The biggest risk with pre-commit is that it only runs *locally*, on developers’ machines. Someone who hasn’t installed it can push code that would have failed the checks. The fix is to run pre-commit in CI as part of your build workflow:

``` yaml
# .github/workflows/build-book.yml (or any project workflow)
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install pre-commit
        run: python -m pip install pre-commit
      - name: Run pre-commit
        run: pre-commit run --all-files
```

Now every PR is guaranteed to pass the same checks that run locally. This closes the “I forgot to install the hooks” loophole for good. See [sec-automation](#sec-automation) for more on wiring up CI.

## 30.7 7. Updating hook versions

Hook repos release new versions over time. Periodically update them with:

``` bash
pre-commit autoupdate
```

This bumps every `rev:` in your config to the latest release, which you then commit. Do this every few weeks or when a new version of ruff / etc. ships a bug fix or rule you want.

## 30.8 8. Debugging a failing hook

When a hook fails, read the output carefully. It tells you:

1.  **Which hook failed** (the second column).
2.  **The exit code** (non-zero means failure).
3.  **The relevant file(s) and line(s)** from the tool’s own error output.

Common issues and fixes:

| Symptom | Fix |
|----|----|
| “hook id: ruff: files were modified” | `git add` the fixed files and commit again |
| “hook id: check-added-large-files” | the file is \>500kB by default; either don’t commit it, use git-lfs, or raise the threshold in config |
| “hook id: detect-private-key” | you (or a library) generated a test key in the repo — move it out, rotate it, or exclude it |
| “hook id: nbstripout: failed to parse” | the notebook JSON is corrupted; open in Jupyter and re-save |
| “No module named X” | run `pre-commit clean` then `pre-commit install` again; the hook’s virtualenv is stale |

## 30.9 9. Worked examples

### Example 1: adding pre-commit to an existing project

``` bash
cd my-project
source .venv/bin/activate
python -m pip install pre-commit

# Write the config
cat > .pre-commit-config.yaml <<'EOF'
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
EOF

# Install the git hook
pre-commit install

# Clean up existing code in one big pass
pre-commit run --all-files

# Commit the config and the cleanup together
git add .pre-commit-config.yaml
git add -u
git commit -m "Set up pre-commit and apply to existing code"
```

### Example 2: a teammate clones the repo

``` bash
git clone git@github.com:you/my-project.git
cd my-project
python -m venv .venv
source .venv/bin/activate
python -m pip install pre-commit
pre-commit install
```

From this point on the teammate’s commits will pass through the same hooks as yours. The config is versioned with the code, so whenever the rules change, everyone picks them up on the next `git pull`.

### Example 3: auto-fix workflow

``` bash
$ git add src/analysis.py
$ git commit -m "Add analysis helper"

trim trailing whitespace.................................................Failed
- files were modified by this hook

Fixing src/analysis.py

ruff.....................................................................Failed
- files were modified by this hook

1 file reformatted

ruff-format..............................................................Passed
```

Both hooks auto-fixed the file. Re-stage and re-commit:

``` bash
$ git add src/analysis.py
$ git commit -m "Add analysis helper"

trim trailing whitespace.................................................Passed
ruff.....................................................................Passed
ruff-format..............................................................Passed
[main a1b2c3d] Add analysis helper
```

Two commands, three hooks enforced. This is the rhythm you want.

## 30.10 10. Templates

**A starting `.pre-commit-config.yaml` for any Python project:**

``` yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
        args: [--maxkb=500]
      - id: check-merge-conflict
      - id: detect-private-key
      - id: mixed-line-ending

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.5.7
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/kynan/nbstripout
    rev: 0.7.1
    hooks:
      - id: nbstripout
```

**CI snippet** (GitHub Actions):

``` yaml
- uses: pre-commit/action@v3.0.1
```

This official action installs pre-commit and runs `pre-commit run --all-files` in one line.

## 30.11 11. Exercises

1.  Install `pre-commit` in a Python venv and run `pre-commit --version`.
2.  Add the starter config from section 10 to one of your projects and run `pre-commit install`.
3.  Run `pre-commit run --all-files` on that project. How many issues did it find? Commit the fixes as one commit.
4.  Deliberately introduce trailing whitespace to a file, try to commit, and observe the hook abort. Re-add and re-commit.
5.  Add a secret-looking string to a file (but not a real secret) and see if `detect-private-key` catches it.
6.  Commit a 2 MB file and watch `check-added-large-files` fail. Then raise the threshold to 3 MB in your config and try again.
7.  Add a pre-commit job to your CI. Push a commit that would fail a local hook (if you had bypassed it with `--no-verify`) and confirm CI catches it.

## 30.12 12. One-page checklist

- Install `pre-commit` in every project’s venv; commit `.pre-commit-config.yaml` to the repo.
- Run `pre-commit install` once to wire up the git hook.
- Start with the five basics: `trailing-whitespace`, `end-of-file-fixer`, `check-yaml`, `check-added-large-files`, `detect-private-key`.
- Add `ruff` and `ruff-format` as your Python hooks.
- Add `nbstripout` for any project with Jupyter notebooks.
- Run `pre-commit run --all-files` once when adding hooks to an existing project, and commit the cleanup.
- Wire pre-commit into CI so developers cannot skip it by accident.
- Run `pre-commit autoupdate` every few weeks to keep hook versions fresh.
- Use `--no-verify` only in genuine emergencies.
