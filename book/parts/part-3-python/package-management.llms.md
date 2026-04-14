# 14  Package Management

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-terminal](#sec-terminal).
>
> **See also:** [sec-virtual-environments](#sec-virtual-environments), [sec-jupyter](#sec-jupyter), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).

## Purpose

Package management is the discipline of installing and updating third-party software (libraries) in a way that is consistent, reproducible, and unlikely to break your work. For novices, the most common failure mode is mixing global installs, different Python interpreters, and ad-hoc updates until nothing imports. This chapter teaches a stable workflow using project-level environments, clear dependency records, and a conflict-resolution playbook.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what a **package**, **dependency**, and **environment** are.

2.  Choose between [`conda`](https://docs.conda.io/en/latest/) and [`pip`](https://pip.pypa.io/en/stable/) for a given situation.

3.  Create, activate, and remove isolated environments (conda environments and/or [`venv`](https://docs.python.org/3/library/venv.html)).

4.  Install packages with good hygiene (no ‘random global installs’’, avoid base/root env).

5.  Record dependencies for reproducibility (`environment.yml`, `requirements.txt`, optional lockfiles).

6.  Diagnose ‘it worked yesterday’’ failures: wrong interpreter, wrong environment, conflicts.

7.  Resolve dependency conflicts using solver output, pinning, and environment recreation.

8.  Apply maintenance practices: updates, audits, and cleaning without breaking environments.

## Running theme: environments are disposable, projects are not

Your project should be stable because it describes what it needs. If an environment breaks, you should be able to recreate it.

## 14.1 Mental models and vocabulary

A **package** is third-party code you install — `pandas`, `numpy`, `requests`. A **dependency** is another package that your package needs to function: pandas depends on numpy, and matplotlib depends on Pillow, so installing pandas pulls in numpy and installing matplotlib pulls in Pillow. Each dependency relationship can carry a **version constraint**, expressed with operators like `>=`, `<`, `==`, `!=`. A line like `numpy>=1.24,<2.0` means “any 1.x version greater than or equal to 1.24, but not 2.0 or above.” When you install a package, the package manager has to find a set of versions that satisfies *every* constraint involved at once — and that is where conflicts come from.

A Python **interpreter** is the actual `python` executable that runs your code, and where it lives on disk determines where packages get installed. An **environment** is an isolated set of installed packages bound to one specific interpreter. You can have many environments on the same computer — one for each project — and they will not interfere with each other, because each one has its own copy of the interpreter and its own folder of installed packages.

``` bash
# How many environments are typical for a serious user
~/projects/q3-analysis/.venv/        # one project's venv
~/projects/thesis/.venv/             # another project's venv
~/miniconda3/envs/ds101/             # a conda env for one course
~/miniconda3/envs/research/          # another conda env
```

The way you make environments **reproducible** is by writing down what is installed in them, in a small text file you commit alongside your code. Conda’s version of that file is `environment.yml`; pip’s version is `requirements.txt`. Both list package names and (optionally) version constraints. A more rigorous version is a **lockfile**, which records the *exact* version of every package and every transitive dependency that was actually resolved — so that installing from the lockfile gives you a bit-for-bit identical environment, even months later. For coursework, `environment.yml` or `requirements.txt` is usually enough; lockfiles are more common in production teams.

## 14.2 Choosing tools: `conda` vs `pip` vs `venv`

The Python ecosystem has two major package management traditions, and you will encounter both. **conda** comes from the scientific Python world; it manages not only Python packages but also non-Python compiled libraries, system dependencies like CUDA, and even other languages like R and C++ libraries. It is the right choice for projects with heavy compiled dependencies — anything that involves GPU acceleration, GIS tools, bioinformatics stacks, or scientific libraries that are hard to install via pip. Its solver is also better at untangling complex dependency graphs across compiled packages.

**pip** is the standard installer that ships with Python itself, and it installs packages from [PyPI](https://pypi.org/) (the Python Package Index). Combined with the standard-library `venv` module, it gives you lightweight isolated environments using just what comes with Python. For pure-Python work — most web development, most data analysis with no exotic libraries — pip + venv is simpler, lighter, and works identically on every machine.

The practical guidance for a student is straightforward. If your course provides a conda environment file, use conda — your instructor has thought about which channel to use and which versions to pin. If you need a library that exists only on PyPI (which is most of them), use pip inside an active environment. And no matter which tool you pick, **never install packages globally** for course work — every project gets its own environment, period.

## 14.3 Baseline hygiene rules (non-negotiable)

A small number of rules will save you from almost all of the package management pain you would otherwise inflict on yourself. They are not optional, and ignoring them is the most reliable way to spend an entire afternoon untangling an environment.

**Rule 1: never work in the base or root conda environment.** When you install Anaconda or Miniconda, it creates a default environment called `base`. That environment is for conda itself and a handful of utilities; it is *not* where your project packages should live. The moment you start `pip install`-ing things into `base`, you risk breaking conda’s own machinery, and you have no isolation between projects. Create a fresh environment for each project and leave base alone.

**Rule 2: one project, one environment.** It is tempting to maintain one giant “everything I do” environment because creating a new one feels like overhead. Resist the temptation. Two projects with different requirements will eventually conflict, and untangling a giant shared environment is much more work than recreating two clean small ones. Give each environment a clear, project-specific name (`ds101-week3`, `housing-audit`, `thesis-cleaning`) so you can tell at a glance which one is which.

**Rule 3: prefer explicit specs over memory.** Whatever you install, record it in a file (`environment.yml` or `requirements.txt`) inside the project repository. If your install steps live only in your head, your project is not reproducible — not on a teammate’s machine, not on a server, not even on your own laptop in three months when you have forgotten which packages mattered.

**Rule 4: avoid mixing conda and pip casually.** Combining them in the same environment is officially supported but practically fragile. If you must mix, install everything you can with conda *first*, and then use pip for the few packages that conda does not have. Once you have pip-installed something into a conda environment, treat that environment as more brittle: if you need to add more conda packages later, the safer move is usually to recreate the environment from scratch with the new spec rather than to keep adding to it.

## 14.4 Core workflows with conda

### Create and activate an environment

Every conda project starts by creating a fresh environment with a pinned Python version. Pinning the Python version is not optional — leaving it unpinned means conda picks whatever it thinks is best, and your environment drifts across machines. Give the environment a project-specific name so you can tell it apart from the ten other environments you will eventually accumulate.

``` bash
conda create -n housing-audit python=3.12
conda activate housing-audit
```

After activation, your shell prompt should change to show the active environment name in parentheses: `(housing-audit) $`. If it does not, something is wrong — either the activation did not take effect or your shell’s prompt is suppressing it, and you should verify with `conda info --envs` that the right environment has the active marker next to it. **Never install packages without confirming the correct environment is active first.** Installing into the wrong environment — or worse, into `base` — is how most “it worked yesterday” stories begin.

### Install, update, remove

Once the environment is active, you install packages with `conda install`, passing one or more package names. You can pin specific versions with `=`, and you can install several packages at once so the solver sees the full set of constraints and picks a consistent combination:

``` bash
conda install pandas numpy scikit-learn matplotlib
conda install "pandas=2.2" "numpy>=1.26,<2.0"
```

Updates and removals are symmetric:

``` bash
conda update pandas         # upgrade a single package
conda update --all          # upgrade everything (use cautiously)
conda remove matplotlib     # uninstall a package
```

Be cautious with `conda update --all` — a wholesale upgrade in the middle of a project is a good way to turn a working environment into a broken one. Upgrade deliberately, package by package, and only when you have a reason.

### Search and inspect

Two commands answer the question *“what is in this environment, and what else could be?”* `conda list` shows every package currently installed in the active environment, with versions and the channel it came from. `conda search <package>` asks the configured channels what versions are available for installation. Together they are the tools you reach for whenever you are about to touch an environment.

``` bash
conda list                        # everything installed, with versions
conda list pandas                 # just the pandas row
conda search "pandas>=2.0"        # what pandas versions are available
conda info --envs                 # list every environment on this machine
which python                      # confirm the python executable path
python -c "import sys; print(sys.executable)"
```

The last two are the “am I actually where I think I am” checks, and they are worth running whenever an install behaves unexpectedly. If `which python` returns a path outside your environment’s directory, your shell is using a different Python than the one you activated — and nothing else you do will work until you fix that.

### Channels and channel priority (why you should care)

Conda gets packages from **channels** — named sources of pre-built binaries. The default channel ships with Anaconda/Miniconda, but most scientific packages live on **conda-forge**, a community channel with vastly more packages and faster updates. Mixing channels casually is a common source of conflicts, because the same package (say, `numpy`) can exist on both channels with slightly different builds, and conda gets confused about which one to prefer when other packages depend on it.

The fix is **strict channel priority**: configure conda to prefer one channel over all others, so that when a package exists in multiple channels, conda always takes it from the higher-priority channel. For a new project that uses conda-forge, set it up once and commit the configuration:

``` bash
conda config --add channels conda-forge
conda config --set channel_priority strict
```

Do that *before* you create the environment, not after. Once you have mixed-channel packages in an environment, switching to strict priority may require re-creating the environment from scratch. For coursework, pick a channel strategy at the start of the project and stick with it for the duration.

### Exporting and sharing environments

An environment that only exists on your machine is not reproducible. The fix is to **export the environment spec** to a YAML file, commit that file to version control, and teach teammates to recreate the environment from it.

``` bash
conda env export --from-history > environment.yml
```

The `--from-history` flag matters. Without it, `conda env export` dumps every single package and version — including every transitive dependency and platform-specific build string — which produces a long, fragile file that may not install on a different operating system. With `--from-history`, conda records only the packages you explicitly asked for, leaving the solver free to figure out the rest on the target machine. The resulting `environment.yml` is short, portable, and survives OS differences:

``` yaml
name: housing-audit
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pandas=2.2
  - numpy
  - scikit-learn
  - matplotlib
  - jupyter
```

A collaborator who clones the repo recreates the environment with:

``` bash
conda env create -f environment.yml
conda activate housing-audit
```

Commit the `environment.yml`; never commit the environment directory itself.

### Cleaning and cache hygiene (cautious)

Conda caches downloaded package tarballs so that if you install the same package in a second environment, it does not have to re-download. Over months, those caches can grow to several gigabytes. When you need the disk space, `conda clean` removes cached tarballs, unused packages, and index metadata — but it has side effects, so run it intentionally and only when needed.

``` bash
conda clean --dry-run           # preview what would be removed
conda clean --tarballs          # remove cached package tarballs only
conda clean --all               # remove everything cleanable
```

Run `--dry-run` first so you know what the command is about to delete. Avoid running `conda clean --all` right before a demo or deadline — if a package needs to be reinstalled and conda has to re-fetch it, you have turned a zero-second operation into a minute of waiting. Clean when you have time to recover, not under pressure.

## 14.5 Core workflows with `venv` + `pip`

### Create and activate a `venv`

`venv` is Python’s built-in environment tool. It does not need conda; it is part of the standard library, which means any Python install can create one. The convention is to put the environment inside your project directory in a folder called `.venv`, and to make sure that folder is in your `.gitignore` so you never accidentally commit it.

``` bash
cd housing-audit
python -m venv .venv
```

Activation is the only platform-specific step. On macOS and Linux, you source the activation script; on Windows, you run a different script depending on whether you are in PowerShell or cmd.exe:

``` bash
# macOS / Linux (bash, zsh)
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1

# Windows cmd.exe
.venv\Scripts\activate.bat
```

After activation, your prompt should show `(.venv)` or `(venv)` at the start of the line. To leave the environment, run `deactivate` from any prompt. If you ever see `(.venv)` but `which python` points outside the `.venv` folder, something is wrong — the activation script did not actually switch your `PATH`, and you should investigate before installing anything.

### Install and record dependencies

Once the venv is active, upgrade pip itself (old pip versions have slower solvers and miss packages), then install what you need. Always invoke pip through `python -m pip` rather than `pip` directly — that guarantees you are using the pip belonging to the *active* Python, not some system pip that might install into the wrong place.

``` bash
python -m pip install --upgrade pip
python -m pip install pandas scikit-learn matplotlib
python -m pip install "requests>=2.31,<3.0"
```

> **WARNING:**
>
> The two most common failures are **“permission denied”** and **“externally-managed-environment”**. Both mean the same thing: pip is trying to install into a system Python that your user account (rightly) does not own. The fix is never `sudo pip install` — the fix is to activate your virtual environment first (`source .venv/bin/activate`) and run the install from there. Confirm the venv is active by checking that `which python` points inside `.venv/`.
>
> If pip reports `ResolutionImpossible` with a wall of conflicting constraints, you have hit a dependency conflict. Do not try one-at-a-time manual fixes — instead, delete `.venv/`, recreate it from scratch, and install packages together so the solver sees all constraints at once. See [sec-asking-questions](#sec-asking-questions) if you need to escalate.

![](graphics/PLACEHOLDER-pip-install-success.png)

Figure 14.1: ALT: Terminal output from a successful `pip install pandas` command. The output shows the download progress bar, the list of dependencies being collected (numpy, python-dateutil, pytz, six), and a final “Successfully installed” line listing the installed package versions.

Record what you installed in a `requirements.txt` file so a teammate (or future-you) can recreate the environment. The simplest way is `pip freeze`:

``` bash
python -m pip freeze > requirements.txt
```

That produces a file listing every installed package, including transitive dependencies, with exact pins:

``` text
numpy==1.26.4
pandas==2.2.1
python-dateutil==2.9.0
pytz==2024.1
scikit-learn==1.4.1
```

`pip freeze` output is precise but verbose. For smaller, more portable files, many projects instead keep a **hand-maintained** `requirements.txt` with only the packages they explicitly asked for, pinned to the exact versions that work. Either approach is fine; the important thing is that the file is committed to version control and updated whenever you install something new.

### Recreate an environment from a requirements file

The whole point of `requirements.txt` is that someone else — or you, on a new machine — can rebuild the environment from it with two commands:

``` bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If the install fails partway through, resist the urge to install packages one at a time until something works. Read the error, figure out which package is the problem, and either loosen its pin or update the requirements file. Ad-hoc fixes inside a venv that do not make it back into `requirements.txt` are how environments silently become non-reproducible.

### Sanity checks

Two checks catch most environment-misconfiguration problems before they become confusing bugs. First, confirm the active `python` is the one inside your environment:

``` bash
which python                  # macOS/Linux
where python                  # Windows
python -c "import sys; print(sys.executable)"
```

The path you see should be inside your `.venv/` folder. If it is not, activation did not work and anything you install will go somewhere else. Second, ask pip to verify that the installed packages are mutually consistent:

``` bash
python -m pip check
```

`pip check` reports any installed packages with unmet or incompatible dependencies. A clean environment produces `No broken requirements found`. If it reports problems, do not ignore them — they will surface later as confusing runtime errors, and fixing them now (usually by upgrading or pinning a specific package) is much easier than debugging them after the fact.

## 14.6 Dependency conflicts: what they are and why they happen

### The conflict pattern

Dependency conflicts have a single underlying shape. You ask the package manager to install package A and package B. Package A depends on a range of versions of C — say, `C>=1.0,<2.0`. Package B depends on a *different* range — say, `C>=2.5`. There is no version of C that satisfies both constraints simultaneously, so the solver gives up and reports a conflict. That is almost every dependency conflict you will ever see, distilled.

The trick is that C is often a package you have never heard of, deep in the dependency graph. You asked for `pandas` and `some-specialty-library`, and somewhere three levels down they both depend on `numpy` with incompatible constraints. The solver’s error message points at `numpy`, not at pandas, and a novice reader wonders why numpy is even involved. The answer is “transitive dependencies” — the dependencies of your dependencies — and any non-trivial Python project has a lot of them.

### Symptoms novices see

Conflicts manifest in three characteristic ways. **Install fails outright**, with pip reporting `ResolutionImpossible` and a long list of constraints it could not satisfy, or with conda’s solver spinning for minutes before giving up with `UnsatisfiableError`.

``` text
ERROR: Cannot install A and B because these package versions have
conflicting dependencies.

The conflict is caused by:
    A 1.4.0 depends on C<2.0
    B 3.1.0 depends on C>=2.5
```

**Imports fail after an upgrade**. The install appears to succeed, but when you try to `import pandas` in a notebook you get an `ImportError` or an `AttributeError` from deep inside the library. This usually means a dependency was upgraded to a version that removed or renamed something another package depended on. **Runtime errors with incompatible versions** are the sneakiest: everything imports, the code starts running, and then you get a cryptic `TypeError` or `ValueError` when two packages disagree about an object’s interface. The symptom looks like a bug in your code but is actually a dependency mismatch.

## 14.7 Conflict-resolution playbook (a disciplined sequence)

When a conflict appears, the worst thing you can do is start mashing random `conda install` and `pip install` commands until something seems to work. That path leads to an environment that “installed” but is actually half-broken, with every step making it harder to diagnose. Instead, follow a disciplined sequence.

### Step 0: stop making it worse

Put your hands on the table. Do not run another install command. Do not try a different version at random. **Copy the exact error output to a text file** — every line, the full traceback, the list of conflicting constraints. That output is the single most important piece of diagnostic information you have, and nothing is more frustrating than discovering you scrolled past it after running another command that pushed it out of your terminal’s buffer.

### Step 1: verify you are in the right environment

Before spending any more effort on the conflict, confirm you are actually working in the environment you think you are. A surprising number of “conflicts” are really “I installed into the wrong environment”:

``` bash
conda info --envs             # which envs exist, which is active
which python                  # macOS/Linux
where python                  # Windows
python -c "import sys; print(sys.executable)"
```

The output should show your project’s environment as active and the `python` executable living inside it. If they do not match, activate the correct environment and re-run the install. You may not have a conflict at all.

### Step 2: reduce the problem

Conflicts are easier to solve when you shrink them. Try to install the **smallest set of packages that reproduces the failure**, rather than your full requirements list. If installing `A` and `B` together fails but installing either alone works, the conflict is between A and B, and you have narrowed the search dramatically.

Install multiple packages in a single command when you can, because that lets the solver see all the constraints at once and find a consistent combination. Installing A first, then B, forces the solver to commit to A’s dependency versions before it even knows B is coming — which can produce a solvable situation that looks unsolvable because of the order:

``` bash
# Less effective: solver commits to A's deps first.
conda install pandas
conda install scikit-learn

# More effective: solver sees both and picks consistent versions.
conda install pandas scikit-learn
```

### Step 3: read the solver’s explanation

Both pip and conda now produce readable conflict explanations. Read them. The key piece of information in any conflict message is **which shared package has incompatible constraints, and which top-level packages are forcing those constraints**. Pip’s `ResolutionImpossible` lists the constraint chains explicitly:

``` text
The conflict is caused by:
    pandas 2.2.0 depends on numpy<2.0,>=1.22.4
    some-library 0.5.0 depends on numpy>=2.0
```

In this example, `numpy` is the contested package, and `pandas 2.2.0` and `some-library 0.5.0` are the two top-level packages fighting over it. That is enough information to move to the next step.

### Step 4: choose a strategy

Once you know which package is contested and which packages are forcing the constraints, you have five practical strategies.

**Pin a compatible version** of one of the top-level packages to a release that uses a compatible version of the shared dependency. In the example above, downgrading `some-library` to an older release that accepted `numpy<2.0` would resolve the conflict.

``` bash
python -m pip install "pandas==2.2.0" "some-library<0.5.0"
```

**Relax an unnecessary constraint**. If *you* are the one who pinned `pandas==2.2.0` for no particular reason, unpin it (`pandas>=2.2`) and let the solver pick a version that works with `some-library`.

**Change channels or builds** (conda only). If you are mixing `defaults` and `conda-forge` casually, switching to strict conda-forge priority often dissolves the conflict because the two channels’ builds differ subtly.

**Split environments**. Sometimes two tools genuinely cannot coexist — a GPU library pinned to one CUDA version and another library pinned to a different one. The right answer is two environments, one for each tool, and scripts that call the correct environment for each step of the pipeline.

**Recreate the environment from scratch**. Once an environment is messy — half-upgraded, half-downgraded, with a bunch of pip-into-conda packages layered on — the fastest fix is often to throw it away and rebuild it from the spec file. You lose nothing if your `environment.yml` or `requirements.txt` is up to date (and if it is not, that is the real problem to fix).

### Step 5: verify with a smoke test

After every attempted fix, verify that the environment actually works — do not trust “install succeeded” as proof. The smoke test is a minimal sequence that exercises the packages that conflicted:

``` bash
python -c "import pandas, some_library; print(pandas.__version__, some_library.__version__)"
python scripts/smallest_pipeline.py
```

If the smoke test passes, pin the working versions in your spec file, commit the change, and write yourself a one-line note in `DECISIONS.md` about why the pins exist — so the next time someone asks “why is pandas stuck at 2.2.0?” the answer is on the record.

## 14.8 Mixing conda and pip safely (when you must)

Mixing conda and pip in the same environment is officially supported and practically fragile. The problem is that conda and pip do not know about each other’s package registries. After you `pip install` something into a conda environment, the next `conda install` or `conda update` may silently overwrite the pip-installed package, corrupt its metadata, or break its dependencies. On a good day you get a confusing import error; on a bad day the environment is unrepairable.

Sometimes you cannot avoid mixing — a specific package lives only on PyPI, not on any conda channel. When that happens, there is a recommended order that minimizes the damage.

### The recommended order

1.  **Create a new conda environment** for the project. Do not try to patch an existing messy one.
2.  **Install as many dependencies as possible with conda first**, all in one command so the solver can pick a consistent set.
3.  **Use pip for the packages conda cannot provide**, always invoked as `python -m pip` so you know it is the conda environment’s pip.
4.  **If you later need to add more conda packages**, treat the environment as brittle. Your safest option is to update the spec file and recreate the environment from scratch, rather than continuing to layer conda and pip installs on top of each other.

``` bash
conda create -n housing-audit python=3.12
conda activate housing-audit

# 1. Install everything conda can provide first.
conda install -c conda-forge pandas scikit-learn matplotlib jupyter

# 2. Then use pip (invoked via python -m) for pip-only packages.
python -m pip install some-specialty-library
```

### Recording mixed dependencies

A mixed environment is fully specified by a single `environment.yml` with a `pip:` sub-section. The conda `dependencies` list includes `pip` itself as a package, followed by a nested list of pip-installable packages. This keeps the spec in one file and ensures that `conda env create -f environment.yml` recreates the entire environment — conda parts and pip parts — in the right order.

``` yaml
name: housing-audit
channels:
  - conda-forge
dependencies:
  - python=3.12
  - pandas=2.2
  - scikit-learn
  - matplotlib
  - jupyter
  - pip
  - pip:
      - some-specialty-library>=0.4,<0.5
      - another-pip-only-package
```

Commit the `environment.yml`, and do not maintain a parallel `requirements.txt` that might drift from it. One file, one source of truth. If you later discover you need a package that is available from conda-forge, move it from the `pip:` list into the main `dependencies:` list and recreate the environment — this is cleaner than leaving it pinned under pip indefinitely.

## 14.9 Reproducible environments: pins, constraints, and lockfiles

### Pins vs ranges

You have a choice every time you specify a dependency: pin it to an exact version (`pandas==2.2.1`) or allow a range (`pandas>=2.2,<3.0`). Both are valid, and the right choice depends on what you are optimizing for.

**Exact pins** maximize repeatability. Two installs of the same `requirements.txt` produce the exact same package versions, every time, on every machine — which is what you want for a paper’s final results, a homework submission, or any deliverable where reproducibility is the point. The downside is that exact pins do not receive bug fixes or security patches automatically; when you need an update, you have to edit the pin.

**Version ranges** allow updates within a compatible window. A range like `pandas>=2.2,<3.0` says “any pandas 2.2 or later, but not 3.0 — avoid a major version jump that might break things.” This is a good default for libraries and for projects you actively develop, because it lets bug fixes flow in without breaking compatibility. The downside is **drift**: two installs a month apart may produce different exact versions, which is a problem if one of them happens to pull in a broken release.

``` text
# requirements.txt, with tighter pins for a reproducible deliverable
pandas==2.2.1
numpy==1.26.4
scikit-learn==1.4.1
matplotlib==3.8.3

# Or with ranges for a more flexible working environment
pandas>=2.2,<3.0
numpy>=1.26,<2.0
scikit-learn>=1.4,<1.5
matplotlib>=3.8,<4.0
```

For student work, **tighter pins are usually the right default**, especially for homework submissions, thesis chapters, or code that accompanies a report. The cost of over-constraining is small (you edit the pin when you need to); the cost of drift right before a deadline is enormous.

### Constraints files (pip concept)

Pip has a distinction worth knowing about between “what to install” and “what versions are allowed.” Your `requirements.txt` says *what* to install. A separate `constraints.txt` says *which versions are allowed* for any package — including transitive dependencies you did not ask for directly. Pip reads both and combines them.

This matters when a transitive dependency is the thing causing trouble and you cannot directly name it in `requirements.txt` because you do not import it. A constraints file lets you pin it anyway:

``` bash
# requirements.txt — what you actually use
pandas
scikit-learn

# constraints.txt — version caps for anything that gets pulled in
numpy<2.0
urllib3<2.0

# install with both
python -m pip install -r requirements.txt -c constraints.txt
```

Constraints files are an advanced tool; most student projects do not need them. But when you hit “a transitive dependency I do not import is breaking everything,” they are exactly the right lever.

### Lockfiles

A **lockfile** is a file that records the exact resolved version of every package and every transitive dependency in an environment. Unlike a hand-maintained `requirements.txt`, a lockfile is generated by tooling after the solver has run, and it captures the precise state of a working environment — down to the hash of each downloaded wheel, in some cases. Installing from a lockfile is fast and guaranteed: no resolution happens at install time, because the answer is already written down.

Lockfiles matter because they avoid the “it solved differently on my machine” problem. Two collaborators can install the same lockfile and get bit-for-bit identical environments, even months apart.

In the conda ecosystem, tools like `conda-lock` generate platform-specific lockfiles (one each for Linux, macOS, Windows) from a single `environment.yml`. In the pip ecosystem, tools like `pip-tools` (`pip-compile` produces `requirements.txt` from `requirements.in`), `pipenv`, `poetry`, and `uv` each offer their own lockfile format. For coursework, a plain `requirements.txt` with exact pins is usually enough, and lockfiles are overkill. Understand the concept, and know when your course or lab adopts one.

## 14.10 Package management hygiene over time

### Updates (intentional, not accidental)

Upgrade dependencies on purpose, not by accident. Every upgrade is a small risk that something subtle will break — an API rename, a default behavior change, a tightened type check — and accumulating many upgrades at once multiplies the risk. Before running any update, ask yourself *why*: a security advisory, a needed bug fix, a new feature, or just “it’s been a while”? If the answer is the last one, consider whether the update is actually needed right now.

When you do update, do it somewhere recoverable. **Create a fresh environment or work on a branch**, install the upgraded packages there, and run your smoke tests before you touch the environment you depend on for real work. If something breaks, you throw away the new environment and keep using the old one while you investigate. Upgrading in place, then discovering a breakage, often leaves you with no working state at all.

``` bash
# Safer upgrade pattern: branch + fresh environment.
git switch -c try-pandas-2.3
conda env remove -n housing-audit-test 2>/dev/null || true
conda env create -n housing-audit-test -f environment.yml
conda activate housing-audit-test
conda update pandas
python scripts/smoke_test.py
pytest
```

If the smoke test and tests pass, merge the branch and update the spec file for real. If they fail, you have a diagnostic to work from without having broken anything important.

### Auditing your environment

Once a month (or at the start of a new milestone), take five minutes to audit what is installed and whether any of it has gone wrong. The two most useful commands are:

``` bash
python -m pip check              # report unmet/broken dependency constraints
conda list                       # list every package with its version
```

`pip check` is fast and catches the “something is installed but its dependencies are not” problem before it surfaces as a confusing import error. `conda list` (or `pip list`) is your snapshot of the environment, which you can compare against your `environment.yml` or `requirements.txt` to see whether anything has drifted.

Keep your dependency list **minimal**. Every package you install is a package someone has to keep working; every package you remove is one fewer source of future conflicts. Periodically review the spec file and ask whether each entry is still needed — a library you imported once for an experiment that you have since removed no longer belongs.

### Avoiding common foot-guns

A handful of mistakes cause most “my environment is broken” emails, and they are all easy to avoid once you have been bitten by them.

**Do not use `pip install --user`** for project work. `--user` installs into a per-user directory outside any virtual environment, which means the package is shared across every project on your machine and is invisible to your venv/conda environment. It is the fastest way to recreate exactly the global-install mess that environments are supposed to prevent. Always install into an active environment instead.

**Do not run pip outside an active environment.** If you open a terminal, forget to activate your environment, and type `pip install pandas`, that pandas goes somewhere — usually into your system Python or a default user directory — and now you have a pandas that *might* be the one your project is using, or *might not* be, depending on which `python` you happen to run. Activate first, verify with `which python`, then install.

**Do not reinstall random versions until imports succeed.** When an import fails, the first instinct is often “let me try `pip install --upgrade <package>` and see if that fixes it,” followed by “let me try a different version,” followed by “let me try uninstalling and reinstalling everything.” This path turns a small problem into a big one. Stop, read the error, and figure out what is actually wrong before you change anything. The conflict-resolution playbook above is built exactly for this.

**Do not rely on “works on one machine.”** If the only place your project runs is your laptop, it does not really work — it works *today*, *there*. The fix is always the same: commit an `environment.yml` or `requirements.txt`, test recreating the environment from it, and treat the spec file as the single source of truth. The environment is disposable; the spec is not.

## 14.11 Troubleshooting guide (novice-oriented)

### “ModuleNotFoundError”

You run a notebook or script, and Python reports `ModuleNotFoundError: No module named 'pandas'` — but you *know* you installed pandas. This is the single most common package-management bug for students, and it is almost always one of two things: the package was installed into a different environment than the one you are running, or your IDE or notebook kernel is pointing at the wrong interpreter.

``` bash
# Diagnostic: confirm which Python is actually running your code.
python -c "import sys; print(sys.executable)"
python -m pip list | grep pandas
```

If `sys.executable` is not the path inside your active environment, you have an activation mismatch — activate the right environment and try again. If pandas is missing from `pip list`, you installed it into a different environment entirely. If you are in Jupyter and the problem appears only in notebooks, the notebook **kernel** may be bound to a different Python than the one in your terminal; the fix is to register a kernel for the right environment (see [sec-jupyter](#sec-jupyter)). Once you know which interpreter is running, reinstall the package into that environment.

### “It installed, but now something else broke”

You install a new package successfully, then something that used to work starts failing — a notebook that imported fine now errors, or a test that passed yesterday fails. What almost always happened is that the new install upgraded or downgraded a shared dependency, and something else in the environment depended on the old version.

``` bash
python -m pip check              # see if pip reports any broken requirements
conda list | grep numpy          # check the version of the suspected package
```

If `pip check` reports broken requirements, that is your culprit. The fix is either to pin the shared dependency back to its previous version (if you can find it in your history) or — often faster — to recreate the environment from a clean spec file and accept the one-minute rebuild. This is exactly the situation that committed `environment.yml` / `requirements.txt` files are meant to rescue you from.

### Conda solver is slow or failing

Conda’s classic solver can take many minutes on complex environments, and sometimes it appears to hang forever. The usual cause is too many channels being considered at once, or inconsistent channel priority forcing the solver to compare builds across channels for every package. The fix is to configure conda for strict channel priority and use only the channels you actually need:

``` bash
conda config --set channel_priority strict
conda config --show channels
```

If the solver still struggles, switch to the faster `libmamba` solver, which ships with modern conda installations and is dramatically faster on large environments:

``` bash
conda install -n base conda-libmamba-solver
conda config --set solver libmamba
```

A failing (not just slow) conda solver usually means you have genuine conflicts. Simplify your requirements, install fewer packages at once, and re-read the solver’s error output — it is more informative than it looks on first glance.

### Pip is backtracking forever

Pip’s resolver sometimes prints `INFO: This is taking longer than usual` and then grinds on for many minutes. What is happening is **backtracking**: pip is trying one combination of versions, failing, trying another, and so on, searching for a consistent set. If your constraints are loose (no pins anywhere), pip can consider hundreds of possible versions of each package, and the search space explodes.

``` bash
python -m pip install -r requirements.txt --verbose
```

The verbose output tells you which package pip is currently wrestling with — often one package deep in the dependency graph. The fix is to **add constraints or pins** so pip has less to search. Pinning the top-level packages to specific versions (`pandas==2.2.1`) or adding a `constraints.txt` file that caps known-problematic dependencies (`numpy<2.0`) usually collapses the search space to something solvable. If pip is still backtracking after you have pinned aggressively, the fastest recovery is to delete the `.venv`, start from a clean environment, and install packages in the smallest groups that let the solver find a consistent answer.

> **NOTE:**
>
> - [Python Packaging User Guide](https://packaging.python.org/en/latest/) — the authoritative reference on pip, virtual environments, and PyPI.
> - [Conda User Guide: Managing environments](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html) — the official walk-through for `conda create`, `activate`, and `export`.
> - [Real Python: Managing Python Packages](https://realpython.com/installing-python/) — a beginner-friendly overview of installation and package management patterns.

## 14.12 Worked examples

### Creating a clean conda environment for a project

You are starting a new analysis project that needs pandas, scikit-learn, and matplotlib. The full lifecycle:

``` bash
# Create a fresh environment with a specific Python version
conda create -n housing-audit python=3.12 pandas scikit-learn matplotlib jupyter
conda activate housing-audit

# Confirm you are using the new environment's Python, not base
which python
python -c "import sys; print(sys.executable)"

# Export the spec so a teammate can reproduce it
conda env export --from-history > environment.yml
```

The `--from-history` flag matters: it tells conda to record only the packages you explicitly asked for, rather than every transitive dependency. The resulting `environment.yml` is short, portable, and works across operating systems. Commit it to git. To recreate the environment on another machine:

``` bash
conda env create -f environment.yml
conda activate housing-audit
```

That is the entire reproducibility loop.

### Using pip inside a venv for a small script

For a project with no exotic dependencies, the venv + pip workflow is even simpler:

``` bash
mkdir tiny-script && cd tiny-script
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install requests beautifulsoup4
python -m pip freeze > requirements.txt
echo ".venv/" > .gitignore
```

The `requirements.txt` file is what you commit; the `.venv/` directory itself stays out of git. To verify the environment works, run a smoke test that imports your packages:

``` bash
python -c "import requests, bs4; print(requests.__version__, bs4.__version__)"
```

If both imports succeed and print versions, you are ready to work.

### Diagnosing a dependency conflict

You try to install two packages and pip refuses, printing a long “ResolutionImpossible” error. The fix is not to keep retrying — it is to read the error and find the constraint that is causing the trouble.

``` bash
$ pip install package-a==1.0 package-b==2.0
ERROR: Cannot install package-a==1.0 and package-b==2.0 because these
package versions have conflicting dependencies.

The conflict is caused by:
    package-a 1.0 depends on shared-dep>=2.0,<3.0
    package-b 2.0 depends on shared-dep>=3.0,<4.0
```

Pip is telling you exactly what is wrong: both `package-a` and `package-b` depend on `shared-dep`, but they want incompatible versions of it. The resolutions are limited and clearly defined. You can pin one of the two packages to a different version that uses a compatible `shared-dep`. You can split the work into two separate environments, one for each package. Or you can find out whether a newer release of either package has loosened its constraint. None of those is satisfying, but all are better than retrying the same install hoping the universe changes.

### Diagnosing a notebook/IDE kernel mismatch

The classic confusing failure: you have pandas working perfectly in your terminal, you open a Jupyter notebook in the same directory, type `import pandas`, and Python tells you `ModuleNotFoundError: No module named 'pandas'`. The cause is almost always that the notebook is running in a different Python interpreter than the one your terminal is using.

The diagnostic is one cell:

``` python
import sys
print(sys.executable)
```

If the path it prints contains your project’s `.venv/bin/python`, the notebook is using the right interpreter and the bug is something else (perhaps you forgot to install pandas into this environment). If the path is something like `/usr/bin/python3` or `/opt/anaconda3/bin/python`, the notebook is running a *different* Python — usually because the Jupyter kernel was registered against the system Python before you ever created the project venv. The fix is to register your project’s venv as a Jupyter kernel and switch to it; see [sec-jupyter](#sec-jupyter) for kernel management in detail.

## 14.13 Templates

### Template A: Minimal `environment.yml` (conceptual)

    name: myproj
    channels:

    * conda-forge
    * defaults
      dependencies:
    * python=3.12
    * pandas
    * numpy
    * pip
    * pip:

      * some-pypi-only-package

### Template B: Environment “smoke test”

    python -c "import sys; print(sys.version)"
    python -c "import pandas as pd; print(pd.**version**)"
    python -m pip check

### Template C: Project dependency policy (student-friendly)

    * Every project has an environment file.
    * No installs in base/root.
    * All installs happen through conda (preferred) or pip (only in an env).
    * If the environment breaks, recreate it.
    * Before submission, restart kernel/run all notebooks to confirm the env works.

## 14.14 Exercises

1.  Create a new conda environment, install two packages, and export an environment spec.

2.  Create a new `venv`, install one package, write `requirements.txt`, and recreate it.

3.  Intentionally install conflicting requirements in a fresh env; read the error and identify the conflicting dependency.

4.  Fix the conflict by pinning one package version or splitting into two envs.

5.  Demonstrate a kernel/interpreter mismatch and then correct it.

6.  Write a one-page “environment README”: how to create, activate, and verify the environment.

## 14.15 One-page checklist

- I do not install packages globally for projects.

- I can create and activate a project environment.

- I can confirm which `python` and `pip` I am using.

- I record dependencies in a file tracked with the project.

- I understand how conflicts arise and can read solver output.

- I can resolve conflicts by pinning, simplifying, or recreating an environment.

- I use conda channels deliberately and prefer strict priority when appropriate.

- I verify environments with a small smoke test before important work.

## 14.16 Quick reference: commands students use most

### conda

    conda create -n NAME python=3.12
    conda activate NAME
    conda install PKG
    conda update PKG
    conda env export > environment.yml
    conda env remove -n NAME

### pip (inside an env)

    python -m pip install PKG
    python -m pip install -r requirements.txt
    python -m pip freeze > requirements.txt
    python -m pip check

The steps for downloading, installing, using, and maintaining Python with `conda` will differ based on your operating system. `conda` can be used by Macs running macOS (OS X), PCs running Windows, and PCs running Linux. `conda` cannot be installed or used on managed operating systems like ChromeOS (*e.g.*, Chromebooks) or iOS (*e.g.*, iPads). It is unlikely that you will be able to install or configure `conda` yourself on “managed” computers like those found in libraries or computer labs.

`conda` is only a package manager: it does not include Python or any of its libraries for data retrieval, analysis, visualization, *etc*. At this stage you can either (1) install Anaconda Individual Edition[^1] that includes hundreds of popular libraries and their dependencies or (2) install “miniconda”[^2] and choose which libraries you want installed. In either case, `conda` will be the package manager that helps you install and maintain these libraries. [Figure fig-conda-mini-ana](#fig-conda-mini-ana) captures the relationships between `conda`, miniconda, and Anaconda. Anaconda is easier to install and harder to keep up-to-date while miniconda is harder to install and a easier to keep up-to-date.

![](graphics/conda_mini_ana.png)

Figure 14.2: Relationships between `conda`, miniconda, and Anaconda.

## 14.17 Downloading

## 14.18 Installation

### Testing

### Updating

### Common problems

## 14.19 Installing libraries

like `numpy`, `matplotlib`, `pandas`, `scikit-learn`, and `networkx`

## 14.20 Maintaining libraries

## 14.21 Removing libraries

## 14.22 Environments

[^1]: <https://www.anaconda.com/products/individual>

[^2]: <https://docs.conda.io/en/latest/miniconda.html>
