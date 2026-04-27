# 34  Environment Variables and Secrets

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-terminal](#sec-terminal), [sec-git-github](#sec-git-github).
>
> **See also:** [sec-http-apis](#sec-http-apis), [sec-virtual-environments](#sec-virtual-environments), [sec-pkg-mgmt](#sec-pkg-mgmt).

## Purpose

Sooner or later — usually the first time you use an API — you will need to put a secret in your code. An API key, a database password, an access token, a private URL. The question is *where*, and the answer is almost always “not in the source file, and definitely not in git.”

This chapter teaches you the small set of habits that will keep you from committing a credential to a public repository and getting an urgent email from GitHub at 2 a.m. telling you your AWS key is being used to mine cryptocurrency. (This happens. Regularly.) You will learn what environment variables are, how `.env` files work, how to use [`python-dotenv`](https://pypi.org/project/python-dotenv/) to load them, how to keep secrets out of git, and what to do if you do accidentally leak one.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what an environment variable is and how a Python program reads one.
2.  Set environment variables in your shell and read them back.
3.  Use a `.env` file to store project-specific secrets and load them with `python-dotenv`.
4.  Explain why `.env` must be in `.gitignore` and why a `.env.example` should be committed.
5.  Load secrets in a notebook without echoing them into cell output.
6.  Recognize the signs that you have leaked a secret into git and take the right emergency steps.
7.  Choose between a `.env` file, a system environment variable, and a password manager for different situations.

## Running theme: a secret in a source file is already leaked

If a credential is in a file tracked by git, you should treat it as compromised the moment you stage it. Rotate it, remove it, and put the new one in an environment variable.

## 34.1 What an environment variable is

Every running process on your computer has a set of key-value pairs called its **environment**. These are inherited from the shell that started the process. Typical entries include `PATH` (where to find executables), `HOME` (your home directory), and `USER` (your login name). You can add anything else you like.

Python reads environment variables through the [`os`](https://docs.python.org/3/library/os.html) module:

``` python
import os

api_key = os.environ["GITHUB_TOKEN"]         # raises KeyError if missing
api_key = os.environ.get("GITHUB_TOKEN")     # returns None if missing
api_key = os.getenv("GITHUB_TOKEN", "")      # returns default if missing
```

Use the `os.environ[...]` form when the program *requires* the variable — the `KeyError` will tell you immediately that something is misconfigured, instead of silently passing `None` to `requests` and failing with a confusing 401.

> **WARNING:**
>
> Three failure modes cover 90% of “my secret isn’t being read.” First, the **`.env` file is not in the working directory the program is launched from** — `load_dotenv()` looks for `.env` in the current directory, not the file’s directory. Launch from your project root, or call `load_dotenv(dotenv_path="path/to/.env")` explicitly. Second, the **variable name has a typo** — `GITHUB_TOEKN` looks fine at a glance. Print `list(os.environ.keys())` to see what actually loaded. Third, the variable is **set in a different shell session** — environment variables set with `export` only apply to the shell they were set in, so a variable set before `jupyter lab` won’t be visible in a notebook started from a different terminal.
>
> If you ever see the value itself in a traceback or log, **rotate the secret immediately** — assume it is compromised. Do not just remove the log line.

## 34.2 Setting environment variables in your shell

You can set them on the command line before running your program:

**macOS / Linux (bash, zsh):**

``` bash
export GITHUB_TOKEN=ghp_abc123...
python fetch_issues.py
```

**Windows (PowerShell):**

``` powershell
$env:GITHUB_TOKEN = "ghp_abc123..."
python fetch_issues.py
```

**Windows (cmd):**

    set GITHUB_TOKEN=ghp_abc123...
    python fetch_issues.py

These set the variable for the current shell session only. Close the terminal and it is gone.

For a variable you want every time you open a shell, add the `export` line to your shell profile (`~/.bashrc`, `~/.zshrc`, or `~/.profile`). This is fine for truly personal, always-needed secrets. For project-scoped secrets, prefer a `.env` file so they stay with the project.

## 34.3 `.env` files

A `.env` file is a plain-text file in your project directory that contains `KEY=value` lines. It is the de facto standard for project-scoped environment variables.

    # .env
    GITHUB_TOKEN=ghp_abc123xyz...
    OPENWEATHER_API_KEY=abc987def...
    DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
    DEBUG=1

A few rules:

- **One variable per line**, `KEY=value` with no spaces around the `=`.
- Lines starting with `#` are comments.
- Values are strings. Do not quote them unless they contain spaces.
- Do not put secrets in comments. (Yes, people do this.)

## 34.4 `python-dotenv`: loading a `.env` file into your program

The `python-dotenv` package reads a `.env` file and populates `os.environ` from it, so the rest of your code can just read environment variables as usual.

Install it in your venv (see [sec-virtual-environments](#sec-virtual-environments)):

``` bash
python -m pip install python-dotenv
```

At the top of your script or notebook:

``` python
from dotenv import load_dotenv
load_dotenv()    # reads .env from the current directory by default

import os
token = os.environ["GITHUB_TOKEN"]
```

Conventions:

- Call `load_dotenv()` **once**, at the very top of your entry-point script, before any module that reads environment variables.
- It is a no-op if `.env` does not exist — your program still runs, it just relies on system environment variables instead.
- By default, `load_dotenv` does *not* overwrite variables that are already set in the environment. This is the behavior you want for CI — production overrides `.env`.

## 34.5 `.gitignore`: the line that matters most in this chapter

**Every project that uses `.env` must have this line in `.gitignore`:**

    .env

Before you add a single secret to the file, run:

``` bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ignore .env"
```

Verify:

``` bash
git status
```

`.env` should not appear. If it does, `.gitignore` is wrong.

Equally important: commit a `.env.example` with the *variable names* but not the values:

    # .env.example — copy to .env and fill in real values
    GITHUB_TOKEN=
    OPENWEATHER_API_KEY=
    DATABASE_URL=
    DEBUG=

This file is safe to commit and tells collaborators (and future you) which secrets a project needs. A new contributor runs `cp .env.example .env`, fills in their own keys, and is off to the races.

See [sec-git-github](#sec-git-github) for the full `.gitignore` story.

## 34.6 Secrets in Jupyter notebooks

Notebooks have a special trap: cell output gets saved with the notebook. If you `print(os.environ["API_KEY"])` in a cell, the key is now embedded in the `.ipynb` file and will be committed on your next `git add`.

Three rules for notebooks:

1.  **Never print a secret.** Even to check. If you must verify, print `len(api_key)` or the first 4 characters (`api_key[:4]`).
2.  **Clear outputs before committing.** `Cell → All Output → Clear` in Jupyter Lab, or set up a git pre-commit hook with `nbstripout` to strip outputs automatically (the pre-commit framework is covered briefly in [sec-automation](#sec-automation)).
3.  **Load secrets in the first cell** and do not reference them by value again; pass them into function calls so they never become a standalone cell result.

``` python
# First cell
from dotenv import load_dotenv
load_dotenv()
import os
API_KEY = os.environ["OPENWEATHER_API_KEY"]
# Do NOT add `API_KEY` as the last expression in a cell.
```

## 34.7 What if I already leaked a secret?

The bad news: if you committed and pushed a secret to a public repository, assume it is compromised. People actively scan GitHub for exposed credentials within seconds of a push.

The right emergency response, in order:

1.  **Rotate the credential immediately.** Go to the service that issued it (GitHub, AWS, OpenWeather, etc.) and generate a new one. Revoke the old one. This is the only step that actually stops the damage; everything else is cleanup.

2.  **Update your local `.env` with the new value.** Verify the program still works.

3.  **Remove the secret from the commit.** If it is the most recent commit and you have not pushed:

    ``` bash
    git reset HEAD~1     # unstages the commit
    # edit the file to remove the secret
    git add .
    git commit -m "Your message"
    ```

    If you have already pushed, the secret is in the public history and removing it from future commits does not erase it. You can rewrite history with tools like `git filter-repo` or BFG Repo-Cleaner, but this rewrites every commit SHA and forces every collaborator to re-clone. In practice, rotating the credential is almost always the right move and you can leave the old one in history.

4.  **Add `.gitignore` entries so it cannot happen again.**

5.  **Think about scope.** If the key had broad access (a root AWS key, a production database URL), you may have more cleanup to do: check access logs, look for unauthorized usage, notify your team.

GitHub also offers **secret scanning** for public repos — it detects known secret formats and emails you (and sometimes the issuing service) automatically. Do not rely on it as your only line of defense, but it is a useful last-ditch safety net.

> **NOTE:**
>
> - [The Twelve-Factor App: Config](https://12factor.net/config) — the source of the “environment variables for secrets” convention.
> - [`python-dotenv` documentation](https://pypi.org/project/python-dotenv/) — the library most projects use to load `.env` files into process environments.
> - [GitHub: Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) — the official guide to rotating and erasing leaked credentials.

## 34.8 Worked examples

### A new project from scratch

``` bash
mkdir weather-dashboard && cd weather-dashboard
python -m venv .venv
source .venv/bin/activate
python -m pip install requests python-dotenv

# Set up secrets hygiene BEFORE writing any code
echo ".env" >> .gitignore
echo ".venv/" >> .gitignore

# Record which variables the project needs
cat > .env.example <<'EOF'
OPENWEATHER_API_KEY=
EOF

# Create the real .env (git will ignore it)
cp .env.example .env
# Now edit .env and paste your real key

git init
git add .gitignore .env.example
git commit -m "Initial project with secrets hygiene"
```

The first commit has no secrets in it, and cannot accidentally grow any because `.env` is ignored from the start.

### A script that uses the secret

``` python
# fetch_weather.py
import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ["OPENWEATHER_API_KEY"]

def current_weather(city):
    resp = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params={"q": city, "appid": API_KEY, "units": "metric"},
        timeout=10,
    )
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    data = current_weather("Boulder,US")
    print(f"{data['name']}: {data['main']['temp']}°C")
```

Run it:

``` bash
python fetch_weather.py
```

The script works on your machine because `.env` is there. When a collaborator clones the repo, they will get a `KeyError` telling them exactly which variable is missing. That is the error message you want.

### Verifying without printing

``` python
api_key = os.environ["OPENWEATHER_API_KEY"]
print(f"loaded key: length={len(api_key)}, starts with {api_key[:4]}...")
```

Now you can tell the key loaded correctly without broadcasting it.

## 34.9 Templates

**A minimal `.env.example`:**

    # Copy to .env and fill in. Never commit .env.
    # API keys
    OPENWEATHER_API_KEY=

    # Database
    DATABASE_URL=

    # Feature flags
    DEBUG=0

**A safe “load and verify” snippet for the top of any script:**

``` python
import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = ["OPENWEATHER_API_KEY", "DATABASE_URL"]
missing = [v for v in REQUIRED_VARS if not os.environ.get(v)]
if missing:
    raise RuntimeError(
        f"Missing required environment variables: {missing}. "
        f"Copy .env.example to .env and fill them in."
    )
```

This gives you a useful error on day one instead of a confusing 401 on day three.

## 34.10 Exercises

1.  Create a new project folder, initialize a git repo, and set up `.env`, `.env.example`, and `.gitignore` in the right order. Confirm with `git status` that `.env` does not appear.
2.  Write a `check_secrets.py` that loads `.env`, reads a variable, and prints its length (not its value). Run it and confirm the length matches your key.
3.  Accidentally stage a `.env` file (`git add -f .env`), then recover: unstage it with `git restore --staged .env`, and verify `git status` is clean again.
4.  Write a script that requires two environment variables and fails with a clear error message if either is missing. Use the template from section 9.
5.  In a Jupyter notebook, load an API key from `.env` and use it in a `requests` call. Do not let the key appear in any cell output. Save the notebook and open the `.ipynb` file in a text editor to verify the key is not in there.
6.  Find a GitHub repo that has accidentally committed a `.env` (they exist — search for `filename:.env DB_PASSWORD`). Read the comments from other users. Note how the maintainer responded. Do not copy the credentials.
7.  Set an environment variable in your shell profile and a conflicting one in `.env`. Run a program and observe which one wins (hint: by default, system env wins over `load_dotenv`).

## 34.11 One-page checklist

- `.env` goes in `.gitignore` **before** you add any secrets.
- Commit a `.env.example` with variable names but no values.
- Use `load_dotenv()` at the top of your entry-point script.
- Read secrets with `os.environ["KEY"]` so missing values fail loudly.
- Never `print` a secret. In notebooks, never let a secret be a cell’s last expression.
- If a secret leaks, *rotate first*, clean up history second.
- For shared team secrets, use a password manager or a dedicated secret store, not a shared `.env` in chat.
- Keep separate `.env` files per project; do not reuse one across projects.
- When in doubt, `grep -ri "password\|token\|key" .` before every `git add`.
