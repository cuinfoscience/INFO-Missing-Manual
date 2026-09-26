# 34  Environment Variables and Secrets

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-terminal](#sec-terminal), [sec-git-github](#sec-git-github).
>
> **See also:** [sec-http-apis](#sec-http-apis), [sec-virtual-environments](#sec-virtual-environments), [sec-pkg-mgmt](#sec-pkg-mgmt).

## Purpose

![Gone meme: I’ll just commit this file, …and now everyone can use my account.](../graphics/memes/secrets.png)

The first time you use a real [API](../chapters/appendix-glossary.llms.md#term-api), you get a key. You paste it into your notebook, the request works, and a week later you push the notebook to GitHub. Then one of three things happens. GitHub refuses the push with a wall of `remote:` lines about a secret. Or you get word that the key has been revoked. Or nothing happens, and the key sits in public where anyone can use it. That last one isn’t rare: a 2019 study found [secrets leaked in more than 100,000 public repositories](https://www.ndss-symposium.org/ndss-paper/how-bad-can-it-git-characterizing-secret-leakage-in-public-github-repositories/), with thousands more every day.

If you’ve done this, you’re in good company: pasting the key into the code is the obvious move, and nothing warns you the file is about to be published. The fix is a few habits that keep secrets ([API keys](https://en.wikipedia.org/wiki/API_key), passwords, [access tokens](https://en.wikipedia.org/wiki/Access_token)) out of your source files: your code names the secret, and something outside the code supplies it. This chapter covers [environment variables](../chapters/appendix-glossary.llms.md#term-environment-variable), `.env` files, keeping secrets out of git and notebooks, where they live beyond your laptop, and what to do when one leaks. Sending a key to an API is in [sec-http-apis](#sec-http-apis).

## Why read this chapter

- You pasted an API key into a notebook to get it working, and now you’re not sure how to get it out without breaking everything.
- `os.environ.get("OPENWEATHER_API_KEY")` gives you `None`, even though the key is right there in your `.env` file.
- Your script found its key when you ran it one way and raised `KeyError: 'OPENWEATHER_API_KEY'` when you ran it another.
- `git push` was refused with a wall of `remote:` lines about a “GitHub Personal Access Token,” or GitHub told you a token you committed had been revoked.
- A failed request printed its full URL, key included, into a notebook output you were about to commit.
- You changed the key in `.env`, reran the cell, and your code kept using the old one.
- You want to share a project with your group, or run it on GitHub Actions, without mailing everyone your password.

## Running theme: a secret in a source file is already leaked

Once a credential is in a file git tracks, treat it as public from the moment you stage it: rotate it, remove it, and let an environment variable carry the new one.

## 34.1 What an environment variable is

Every running program (a [process](https://en.wikipedia.org/wiki/Process_(computing))) carries a small set of name-value pairs called its **environment**: [`PATH`](https://en.wikipedia.org/wiki/PATH_(variable)) tells your shell where to find programs, `HOME` names your home folder. A program started from your terminal gets a *copy* of the terminal’s environment. That makes an [environment variable](https://en.wikipedia.org/wiki/Environment_variable) the natural home for a secret: the code mentions only the variable’s name, so it’s safe to share, and each person who runs it supplies their own value. Python reads the environment through [`os.environ`](https://docs.python.org/3/library/os.html#os.environ), which behaves like a dictionary:

``` python
import os

api_key = os.environ["GITHUB_TOKEN"]         # raises KeyError if missing
api_key = os.environ.get("GITHUB_TOKEN")     # returns None if missing
api_key = os.getenv("GITHUB_TOKEN", "")      # returns the default if missing
```

The choice decides how confusing your next bug is. When a program *needs* the variable, use square brackets: if it isn’t set, the script stops right there with `KeyError: 'GITHUB_TOKEN'`. The `.get()` form hands you `None`, and you find out three functions later from a [401 Unauthorized](https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401). Save `.get()` for optional settings.

## 34.2 Setting environment variables in your shell

The quickest way to set a variable is in the terminal, right before you run your program (see [sec-terminal](#sec-terminal) for the shells):

**macOS / Linux (bash, zsh):**

``` bash
export GITHUB_TOKEN=ghp_not_a_real_token
python fetch_issues.py
```

**Windows (PowerShell):**

``` powershell
$env:GITHUB_TOKEN = "ghp_not_a_real_token"
python fetch_issues.py
```

**Windows (Command Prompt):**

    set GITHUB_TOKEN=ghp_not_a_real_token
    python fetch_issues.py

Here’s what trips people up: the variable exists only in *that* window, until you close it, and a program that was already running never sees it. The classic case is Jupyter: run `export` after starting `jupyter lab`, and your notebook can’t see the variable. Stop Jupyter, set the variable, and start it again from that terminal.

For a key you want in every terminal, put the `export` line in your shell’s startup file (`~/.zshrc` for zsh, the macOS default; `~/.bashrc` for bash), or on Windows use [`setx`](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/setx); only windows opened afterward see it. Remember that every program you run can then read it, and that a key typed at the prompt lands in your shell’s [command history](https://en.wikipedia.org/wiki/Command_history). For a project’s keys, use a `.env` file.

## 34.3 `.env` files

Most projects keep their variables in a plain-text file named `.env` in the project folder, one `NAME=value` per line:

    # .env
    GITHUB_TOKEN=ghp_not_a_real_token
    OPENWEATHER_API_KEY=not-a-real-key
    DATABASE_URL=postgresql://user:pass@localhost:5432/mydb
    DEBUG=1

Lines starting with `#` are comments (don’t keep an old key in one), and every value is a string, even `1`. `python-dotenv` forgives spaces around the `=` and strips quotes, but other tools are stricter, so write the plain form and quote only values with spaces.

Two snags catch nearly everyone. The leading dot makes it a [hidden file](https://en.wikipedia.org/wiki/Hidden_file_and_hidden_directory), so the file you just made seems to vanish from Finder or File Explorer. And an editor that saves “as text” can name it `.env.txt`, which looks the same with extensions hidden and is invisible to every tool looking for `.env`. `ls -a` (`dir -Force` in PowerShell) shows the real name; [sec-filesystem](#sec-filesystem) shows how to reveal both.

## 34.4 `.gitignore`: the line that matters most in this chapter

A `.env` file keeps a secret out of your code only if git never picks it up, so tell git to ignore it *before* you put anything real in it:

``` bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Ignore .env"
```

Then check. `git status` shouldn’t mention `.env`, and [`git check-ignore`](https://git-scm.com/docs/git-check-ignore) names the rule that’s doing the ignoring:

``` text
$ git check-ignore -v .env
.gitignore:1:.env   .env
```

If it prints nothing, there are two usual suspects. `>>` appends to the last line, so if that line had no newline you’ve written something like `*.pyc.env`; put `.env` on a line of its own. Or `.env` was already committed, and ignoring affects only files git isn’t tracking yet: [`git rm --cached .env`](https://git-scm.com/docs/git-rm) stops tracking it and keeps your copy, and “What if I already leaked a secret?” covers the old commit.

Beside the ignored `.env`, commit a `.env.example` with names and no values, so a new teammate knows which keys the project needs, runs `cp .env.example .env`, and fills in their own:

    # .env.example: copy to .env and fill in real values
    GITHUB_TOKEN=
    OPENWEATHER_API_KEY=
    DATABASE_URL=
    DEBUG=

The [patterns](https://git-scm.com/docs/gitignore) `.env.*` and `!.env.example` also cover any `.env.local` you add later. [sec-git-github](#sec-git-github) has the rest of the `.gitignore` story.

## 34.5 `python-dotenv`: loading a `.env` file into your program

Nothing reads a `.env` file automatically. The [`python-dotenv`](https://pypi.org/project/python-dotenv/) package copies its variables into `os.environ`, so the rest of your code reads them as if you’d set them in the shell. Install it in your project’s virtual environment (see [sec-virtual-environments](#sec-virtual-environments)), then call `load_dotenv()` once, at the top of the script or notebook you run:

``` bash
python -m pip install python-dotenv
```

``` python
import os
from dotenv import load_dotenv

load_dotenv()
token = os.environ["GITHUB_TOKEN"]
```

With no `.env` file, `load_dotenv()` quietly does nothing, which is deliberate (on a server, variables come from elsewhere) and is also why a missing file is easy to miss.

### Where `load_dotenv()` looks

It’s natural to assume `load_dotenv()` reads `.env` from the folder you ran the command in. It doesn’t, quite. In a script, it starts in the folder of *the file that calls `load_dotenv()`* and walks up through parent folders until it finds a `.env`. In a notebook or interactive session it starts from the current working directory (for a notebook, usually its own folder) and walks up the same way. Here’s `scripts/where.py` in a project called `weather-dashboard`, with `.env` at the project root:

``` python
from dotenv import find_dotenv, load_dotenv

print("found:", find_dotenv() or "nothing")
print("loaded:", load_dotenv())
```

Run from the project root or your home folder, it finds the same file, because the search starts at the script:

``` text
$ python scripts/where.py
found: /Users/you/weather-dashboard/.env
loaded: True
```

It fails when the calling file lives *outside* the project, such as a script in a shared `~/tools` folder or a helper module elsewhere, even if you’re standing next to the `.env`:

``` text
$ cd ~/weather-dashboard
$ python ../tools/where.py
found: nothing
loaded: False
```

To search from the folder you’re in, pass `find_dotenv(usecwd=True)`; to skip the search, give the path:

``` python
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(usecwd=True))        # search from the current folder

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")           # or name the file outright
```

Notice `loaded: False`: `print(load_dotenv())` is the quickest test of whether it found your file. (One oddity from the package’s source: under a debugger it searches from the current folder, as in a notebook.)

### It won’t overwrite what’s already set

By default (`override=False`), `load_dotenv()` leaves alone any variable already in the environment, so a server’s real settings beat a stray `.env`. That surprises people twice: an old key you once `export`ed beats the new one in `.env`, and in a notebook, editing `.env` and rerunning `load_dotenv()` changes nothing. Restart the kernel, or use `load_dotenv(override=True)`.

## 34.6 When your key loads as `None`

It’s maddening, because the key is *right there* in the file. Check these in order.

**Did `load_dotenv()` find the file?** If it returns `False`, check the file’s real name with `ls -a`: `.env.txt` and `env` both look right at a glance.

**Do the names match?** `OPENWEATHER_KEY` in the code never meets `OPENWEATHER_API_KEY` in the file, and `GITHUB_TOEKN` is hard to spot. List the names, not the values: `print(sorted(k for k in os.environ if "WEATHER" in k))`.

**Is the value empty?** A copied `.env.example` you forgot to fill in gives `''`: no `KeyError`, just a 401.

**Is an older value winning, or was it set where your program can’t see it?** See “It won’t overwrite what’s already set” and the shell section above.

And if the key’s *value* ever shows up in a traceback, log, or cell output, don’t just delete the line: rotate the key, because anything printed may have been seen.

## 34.7 Secrets in Jupyter notebooks

Notebooks have a trap scripts don’t: the `.ipynb` file saves every cell’s output, so a key that shows up in an output goes wherever the file goes. It gets there in ways that are easy to miss:

- **A cell ending in `API_KEY`,** which displays the value just as `print(API_KEY)` would.
- **A traceback.** When the key goes in the URL, a failed `raise_for_status()` prints it: `401 Client Error: Unauthorized for url: https://api.openweathermap.org/data/2.5/weather?q=Boulder%2CUS&appid=not-a-real-key&units=metric`. ([sec-http-apis](#sec-http-apis) shows how to avoid this.)
- **IPython’s [`%env` magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-env).** Listing everything, current versions hide values whose names contain “key,” “token,” or “secret,” but show `DB_PASSWORD` in full; `%env OPENWEATHER_API_KEY` prints the key itself.

So load secrets in the first cell, pass them straight into the calls that need them, and to confirm one loaded, print its length (see “Verifying without printing”). For a one-off key you’d rather not store, Python’s [`getpass`](https://docs.python.org/3/library/getpass.html) asks for it without echoing what you type.

``` python
# First cell
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ["OPENWEATHER_API_KEY"]
# Don't end this cell, or any other, with API_KEY on a line by itself.
```

Then **clear outputs before you commit**: *Edit → Clear Outputs of All Cells* in JupyterLab, or `jupyter nbconvert --clear-output --inplace notebook.ipynb`. [nbstripout](https://pypi.org/project/nbstripout/) can do it on every commit from a [pre-commit](https://pre-commit.com) hook (see [sec-automation](#sec-automation)). Then search the `.ipynb` for your key in a text editor; ten seconds settles it. On Colab or Kaggle, use the platform’s secrets panel (see [sec-jupyter](#sec-jupyter)).

## 34.8 Where secrets live beyond `.env`

A `.env` file suits one project on one computer. Once a second person or machine needs the key, the tempting move, pasting it into a group chat, copies it into places you can never clean up. [Table tbl-secret-homes](#tbl-secret-homes) lists better homes.

| Where | Good for | Watch out for |
|----|----|----|
| A `.env` file | One project on your computer | It must be in `.gitignore` |
| Shell startup file | A personal key every project uses | Every program you run can read it |
| Password manager | The master copy; sharing with a group | Share per person, not one login |
| GitHub Actions secrets | Code that runs in CI | Only as safe as the workflow |

Table 34.1: Where each kind of secret belongs

A [password manager](https://en.wikipedia.org/wiki/Password_manager) keeps the master copy safe from a lost laptop, and many can share an entry with a group and revoke it later. Code on GitHub’s machines can’t read your `.env`, so use [GitHub Actions secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets): add one under *Settings → Secrets and variables → Actions*, and a workflow passes it to your code as an environment variable with `${{ secrets.OPENWEATHER_API_KEY }}`. GitHub redacts secrets from logs and withholds them from workflows triggered by forks. Your code still reads `os.environ`; [sec-automation](#sec-automation) has a full workflow.

Wherever a key lives, give it as little power as the job needs (the [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege)). A [personal access token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) that can read one repository and expires next month is an afternoon’s cleanup if it leaks.

Protect the accounts that hand out keys, too. Anyone who signs in as you can mint fresh keys, so a guessed or phished password beats the most careful `.env` file. [Two-factor authentication](https://en.wikipedia.org/wiki/Multi-factor_authentication) (2FA) closes that gap by asking for a code from your phone or a security key as well as the password. [Turn it on for GitHub](https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication), which began requiring it for accounts that contribute code in 2023, and for every account that issues keys: your cloud console, the API services you use, and the password manager itself. Save the recovery codes it gives you somewhere safe, such as that password manager, or a lost phone locks you out.

Some secrets are on your disk already, put there by tools rather than by you. Run `aws configure`, and the AWS command-line tool saves your access key [in a plain-text file named `credentials`](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html#cli-configure-files-where) in a hidden `.aws` folder in your home folder (`~/.aws/credentials`). Google Cloud’s `gcloud auth application-default login` writes [`application_default_credentials.json`](https://cloud.google.com/docs/authentication/application-default-credentials) under `~/.config/gcloud/` (`%APPDATA%\gcloud\` on Windows). Treat these files like `.env`: never copy one into a project folder, never `cat` one in a notebook cell, and never commit one. The Uber breach in “Stakes and politics” began with a leaked cloud access key.

## 34.9 What if I already leaked a secret?

Take a breath: this happens to careful people, and it’s fixable. How much work it takes depends on how far the secret got.

**If the key got out and isn’t only yours, tell someone first.** A key that belongs to a lab, a class, a project, or an employer has a person responsible for it: your PI or project lead, and for anything that touches university systems or other people’s data, your school’s IT security office. Tell them before you start fixing things, or while you rotate, not after. They may need to check access logs for what the key was used for while those logs still exist, and they’d much rather hear about a leak in five minutes than discover a quiet cleanup a month later.

**If GitHub refused your push,** that’s the good outcome. [Push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection), on by default for pushes to public repositories, recognized the key, and its message names the secret’s kind, commit, and file. The secret never reached GitHub, so don’t bypass the block. If it’s in your latest commit (here, a committed `.env`), fix that commit and push again:

``` bash
git rm --cached .env
echo ".env" >> .gitignore
git add .gitignore
git commit --amend --no-edit
git push
```

For an older commit, GitHub’s page on [resolving a blocked push](https://docs.github.com/en/code-security/secret-scanning/working-with-secret-scanning-and-push-protection/working-with-push-protection-from-the-command-line) walks through the rebase. The same fix works if you catch it yourself before pushing.

**If the secret was pushed,** you may hear from GitHub’s [secret scanning](https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning), which checks the whole history of public repositories and tells partner services about their keys so they can revoke them (a GitHub token pushed to a public repository is [revoked automatically](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/token-expiration-and-revocation)). Or you notice it yourself. Either way:

**Rotate the key right away.** At the service that issued it, revoke the old key and create a new one. It’s the only step that stops the damage: once the old key is dead, it doesn’t matter who copied it. Do it even if the repository is private, and even if you deleted the file a minute later, because the key is still in the history.

**Then put the new key in `.env`,** check that `.env` is ignored, and confirm your code runs.

**Then decide about history.** A new commit deleting the file leaves the key in every earlier one. Erasing it means rewriting history with [git filter-repo](https://pypi.org/project/git-filter-repo/) (GitHub’s guide in Further reading), which gives commits new IDs, makes collaborators discard their copies, and can’t reach forks; GitHub says rotating may be enough on its own. For a class project, a dead key left in history is usually fine; for other people’s data, ask whoever runs the project.

**Finally, think about what the key could reach.** A weather key costs a quota. A write token, a cloud key, or a database URL may mean checking access logs and billing, which is why the people responsible for it needed to hear first.

## 34.10 What if I leaked personal data?

Sometimes what gets out isn’t a key but people: a CSV of survey participants’ names and emails committed to a public repository, or a spreadsheet of interview notes pasted into an AI chatbot to tidy up. It feels like the same mistake, and the first instinct is the same quiet fix. It isn’t the same, because the fix that makes a leaked key harmless doesn’t exist here. You can rotate a key; you can’t rotate a person’s name, email address, or health history.

**Tell the people responsible, promptly.** That’s your PI or project lead, and for research with people, your [institutional review board](https://en.wikipedia.org/wiki/Institutional_review_board) (IRB). If you aren’t sure who that is, start with your school’s privacy or IT security office. Depending on the data, your IRB protocol, a data use agreement, or privacy law may require the incident to be reported, sometimes within a set time. They can’t meet an obligation they don’t know about.

**Remove it, and assume it’s been copied.** Delete the file, make the repository private if you can, and stop sharing whatever you shared. But a public repository can be cloned or forked within minutes, and you can’t recall text you pasted into an online service (see [sec-ai-llm](#sec-ai-llm)), so act as though a copy exists somewhere.

**Know that a new commit doesn’t erase it.** As with a key, deleting the file leaves it in every earlier commit. Purging it means rewriting history, and on GitHub it can still show up in cached views and pull requests until you [ask GitHub Support to remove them](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository#fully-removing-the-data-from-github). Do that with the people you told, not ahead of them, since they may first need to know exactly what was exposed and when.

## 34.11 Stakes and politics

In 2016, intruders downloaded files from Uber’s cloud storage holding more than 25 million names and email addresses, 22 million names and phone numbers, and 600,000 driver’s license numbers. According to the [U.S. Federal Trade Commission](https://www.ftc.gov/news-events/news/press-releases/2018/04/uber-agrees-expanded-settlement-ftc-related-privacy-security-claims), they got in with “an access key an Uber engineer had posted on a code-sharing website,” and Uber didn’t disclose the breach for a year. The people who paid were riders and drivers who had never heard of that key.

That’s the shape of most secrets failures. A leaked key on your weather dashboard is your own problem. A leaked key to a learning-management system, a health records database, a city’s permit data, or a lab’s human-subjects survey is somebody else’s problem, and they may never hear about it. The cost of carelessness grows with the sensitivity of the data, and it’s seldom paid by the person who was careless.

The burden of doing this well is unevenly spread, too. Companies in regulated industries have security teams, dedicated secret stores, rotation schedules, and audit trails. Students, small labs, and volunteer open-source projects get the same responsibility with a `.env` file and good intentions. Knowing what your key protects is how you decide how much of the heavier machinery (Further reading lists some) you owe the people behind it.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: when you handle a secret, ask whose data it actually protects, and let the answer set how careful you are.

## 34.12 Worked examples

### A new project from scratch

The safest moment to set up secrets hygiene is before there’s a secret. This order makes it impossible to commit the key by accident:

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

The first commit holds only `.gitignore` and `.env.example`, and `.env` was ignored before it existed.

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
    if resp.status_code == 401:
        raise RuntimeError("OpenWeather rejected the key: check OPENWEATHER_API_KEY in .env")
    resp.raise_for_status()
    return resp.json()

if __name__ == "__main__":
    data = current_weather("Boulder,US")
    print(f"{data['name']}: {data['main']['temp']}°C")
```

It runs from any folder, since `load_dotenv()` searches from the script’s own. [OpenWeather’s API](https://openweathermap.org/current) takes the key in the URL, so the script checks for a 401 before `raise_for_status()`, and a bad key gets a message instead of a traceback that prints it. A collaborator without a `.env` gets `KeyError: 'OPENWEATHER_API_KEY'`; one with an empty key gets the `RuntimeError`. Either says what to do next.

### Verifying without printing

``` python
api_key = os.environ["OPENWEATHER_API_KEY"]
print(f"loaded key: length={len(api_key)}, starts with {api_key[:4]}...")
```

Now you can tell the key loaded, and that it’s the one you expected, without broadcasting it.

## 34.13 Templates

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

It catches empty values as well as missing ones (`RuntimeError: Missing required environment variables: ['DATABASE_URL']. ...`), a useful error on day one instead of a confusing 401 on day three.

## 34.14 Exercises

1.  Create a new project folder, initialize a git repository, and set up `.gitignore`, `.env.example`, and `.env` in the right order. Confirm with `git check-ignore -v .env` that `.env` is ignored.
2.  Write a `check_secrets.py` that loads `.env`, reads a variable, and prints its length (not its value). Confirm the length matches your key.
3.  Accidentally stage a `.env` file (`git add -f .env`), then recover: unstage it with `git restore --staged .env`, and check that `git status` is clean again.
4.  Write a script that requires two environment variables and fails with a clear message if either is missing or empty. Start from the “load and verify” template.
5.  In a notebook, load an API key from `.env` and use it in a `requests` call without letting it appear in any output. Save the notebook, open the `.ipynb` in a text editor, and search for the key.
6.  Put `where.py` from this chapter in a project’s `scripts/` folder, with a `.env` at the project root. Run it from the project root, from your home folder, and as a copy outside the project. Predict each result first, then try `find_dotenv(usecwd=True)`.
7.  Set a variable with `export` and a different value for it in `.env`. Which one does your program see? (Hint: by default, the shell’s.) Then try `override=True`.
8.  In a scratch repository, commit a `.env` holding an obviously fake key (`API_KEY=not-a-real-key-123`), then commit its removal with `git rm .env`. Run `git show HEAD~1:.env`. What’s still there, and what would you have to do if the key had been real? (This is why rotating comes first.)

## 34.15 One-page checklist

- Add `.env` to `.gitignore` **before** any secret goes in it; check with `git check-ignore -v .env`.
- Commit a `.env.example` with variable names but no values.
- Call `load_dotenv()` once, at the top of the script or notebook you run.
- If a key loads as `None`, `print(load_dotenv())`: `False` means no file was found.
- Read required secrets with `os.environ["KEY"]` so missing values fail loudly.
- Never print a secret or leave one as a cell’s last expression; clear outputs before committing.
- Keep the master copy of each key in a password manager, and share through it, not in chat.
- Give each token the least access it needs, and an expiry date.
- Turn on two-factor authentication for GitHub and every account that issues keys.
- If a secret leaks, tell your security contact and *rotate first*, clean up history second.
- Keep a separate `.env` per project.
- Before every commit, read `git diff --staged` for anything that looks like a key.

> **NOTE:**
>
> - **Adam Wiggins**, [The Twelve-Factor App: Config](https://12factor.net/config) — the source of the “keep config in environment variables” convention; the whole manifesto is worth a half-hour even if you only ever build small apps.
> - **Saurabh Kumar and contributors**, [`python-dotenv` documentation](https://saurabh-kumar.com/python-dotenv/) — the library most Python projects use to load `.env` files, including the file syntax it accepts and its command-line tool.
> - **GitHub**, [Removing sensitive data from a repository](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository) — the official guide to rotating a leaked credential and, when you must, erasing it from history with git filter-repo.
> - **OWASP**, [Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html) — practitioner consensus on handling secrets across their whole life; useful when you graduate from “don’t commit secrets” to “design a rotation policy.”
> - **HashiCorp**, [Vault documentation](https://developer.hashicorp.com/vault/docs) — a widely used self-hostable secret store; worth knowing about for when `.env` files stop being enough.
> - **AWS**, [Secrets Manager](https://docs.aws.amazon.com/secretsmanager/), and **Google Cloud**, [Secret Manager](https://cloud.google.com/secret-manager/docs) — the hosted options most cloud teams use, for when secrets need rotation, audit logs, and access control.
> - **Troy Hunt**, [Have I Been Pwned](https://haveibeenpwned.com/) — look up whether your email address appears in known data breaches; not a secrets tool, but a sobering sense of how much leaked data is out there.
