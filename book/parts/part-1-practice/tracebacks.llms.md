# 6  Reading Python Tracebacks

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-debugging](#sec-debugging).
>
> **See also:** [sec-testing](#sec-testing), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks), [sec-asking-questions](#sec-asking-questions).

## Purpose

When your Python code crashes, Python prints a wall of red text ending with something like `KeyError: 'date'` or `ValueError: could not convert string to float: 'N/A'`. Many novices glance at this wall, feel a jolt of dread, and scroll past to the error message at the bottom — losing most of the information the interpreter is trying to give them for free.

That wall of text is a [traceback](../../appendix-glossary.llms.md#term-traceback), and it is the single most useful piece of evidence you will get when something breaks. A traceback tells you exactly which file, which line, which function call, and which value caused the crash. Learning to parse one quickly turns most bug-hunting sessions from “I have no idea what is wrong” into “I know which line to look at and roughly why.” This chapter teaches you how.

It is a short chapter on purpose: reading tracebacks is a focused skill you can learn in 30 minutes and then reuse for the rest of your career. It pairs with [sec-debugging](#sec-debugging) (which teaches the investigative loop) and [sec-testing](#sec-testing) (which teaches how to prevent the same error from coming back).

## Learning objectives

By the end of this chapter, you should be able to:

1.  Identify the parts of a Python traceback: the error type, the error message, the stack, and each frame’s file, line number, and code snippet.
2.  Read a traceback top-down and bottom-up and explain when each direction is useful.
3.  Distinguish between an error raised in *your* code and one raised inside a third-party library like pandas or numpy.
4.  Translate the ten most common Python exception types into plain English and know where to look first when you see them.
5.  Read a chained traceback (*“during handling of the above exception, another exception occurred”*) and find the root cause.
6.  Read tracebacks that appear inside Jupyter notebook cells, where the “file” is a cell index.
7.  Search for an error message online in a way that returns useful hits rather than noise.

## Running theme: the last line tells you *what*, the stack tells you *where*

A traceback has two jobs: tell you what went wrong (the exception type and message on the last line) and tell you where it happened (the stack of frames above it). Most of the time you need both — the “what” is a label, and the “where” is the evidence.

## 6.1 1. The anatomy of a traceback

Here is a minimal traceback from a small script:

    Traceback (most recent call last):
      File "/home/you/project/src/analysis.py", line 42, in <module>
        total = compute_mean(values)
      File "/home/you/project/src/analysis.py", line 17, in compute_mean
        return sum(xs) / len(xs)
    ZeroDivisionError: division by zero

Walk through it piece by piece:

- **`Traceback (most recent call last):`** — the header. Python is announcing that an exception propagated all the way up without being caught, and it is about to list the call chain.
- **Each `File ..., line ..., in ...` block is a *frame*.** A frame is a single function call in progress at the moment the error happened. The topmost frame is the entry point (the script you ran, or the notebook cell you executed). The bottommost frame is the innermost function — the one that actually raised the error.
- **The line printed under each frame header is the source code** at that line. Python literally reads your source file back and shows you the offending line, which is enormously helpful.
- **The last line is the exception type and message.** Here it is `ZeroDivisionError: division by zero`. Everything before the colon is the class name; everything after is the string the programmer (or library) passed to explain what went wrong.

The phrase **“most recent call last”** is the single most important thing to understand. Python prints the stack in execution order: the first frame is what you started with, and the last frame is what was running when the crash happened. If you want to know *what code actually crashed*, look at the **bottom**. If you want to know *how the program got there*, read the frames **top-to-bottom** like a trail of breadcrumbs.

## 6.2 2. Top-down vs. bottom-up reading

Both directions are useful; pick based on the question you are trying to answer.

**Read bottom-up when the error is in *your* code.** Start at the last line (`ZeroDivisionError: division by zero`) and then jump to the bottommost frame. That frame almost always points at a line in your source that is wrong in some small way — an empty list, an off-by-one index, a typo in a column name.

**Read top-down when the error is deep inside a library.** If the bottommost frame is in a file like `/site-packages/pandas/core/indexing.py`, the line shown will be pandas’s internal code, and staring at it will not help you. Instead, scan top-down until you find the last frame whose file path is inside your project (for example `src/analysis.py` or `notebooks/exploration.ipynb`). That frame is the last bit of code *you wrote* before handing control over to pandas, and that is where the bug almost certainly lives.

A useful heuristic: **scan for the first file path that belongs to you, from the bottom up.** That frame is where your change lives. The lines below it are the library doing its job correctly with bad input you provided.

## 6.3 3. The ten exceptions you will see most often

These are the error types you will encounter 90% of the time in a first data science course, with a plain-English translation and the first place to look.

### `NameError: name 'foo' is not defined`

**Plain English:** you used a variable or function that Python has never heard of.

**First place to look:** typos (`datafame` vs `dataframe`), forgetting to run the cell that defined `foo`, or importing under a different name than you expected (`import pandas as pd` then typing `pandas.read_csv` instead of `pd.read_csv`).

### `ModuleNotFoundError: No module named 'foo'` / `ImportError`

**Plain English:** Python cannot find a package you are trying to import.

**First place to look:** is the package installed in the *active* environment? Check with `pip list | grep foo` or `conda list foo`. If you are in a Jupyter notebook, make sure the kernel matches the environment you installed into. See [sec-virtual-environments](#sec-virtual-environments) and [sec-pkg-mgmt](#sec-pkg-mgmt).

### `SyntaxError: invalid syntax`

**Plain English:** Python cannot parse your code. The error is usually on the line the traceback points at or on the *previous* line (an unclosed bracket or string).

**First place to look:** unclosed `(`, `[`, `{`, or `"`; a missing colon at the end of a `def`, `for`, `if`, or `while`; Python 2 `print` syntax.

### `IndentationError: unexpected indent`

**Plain English:** Python’s whitespace rules have been broken. Every block must be indented consistently.

**First place to look:** mixed tabs and spaces (the worst offender), or pasting code that had different indentation than the surrounding block.

### `TypeError: ... takes ... arguments but ... were given` or `TypeError: unsupported operand type(s) for +: 'int' and 'str'`

**Plain English:** you called a function with the wrong number of arguments, or you tried an operation on values of the wrong type.

**First place to look:** the line at the bottom of the traceback. Check what each argument actually is (`print(type(x))` just before the failing line) — a string you expected to be a number, or a list you expected to be a dict.

### `ValueError: could not convert string to float: 'N/A'`

**Plain English:** the type was right but the value was wrong. Here, pandas got the string `'N/A'` when it expected a number.

**First place to look:** missing-value sentinels in your CSV. See [sec-data-file-formats](#sec-data-file-formats) for how `pd.read_csv` handles them with `na_values=...`.

### `KeyError: 'date'`

**Plain English:** you asked a dictionary (or a DataFrame, which is dict-like for columns) for a key that does not exist.

**First place to look:** column name typos (`'date '` with a trailing space is a classic), or a column that was dropped earlier in your notebook but the cell that uses it is still running. Print `df.columns.tolist()` to see what is actually there.

### `IndexError: list index out of range`

**Plain English:** you asked a list for element number *N* but the list has fewer than *N+1* items.

**First place to look:** off-by-one errors in loops, empty lists you did not expect to be empty, or data that has fewer rows than you assumed.

### `AttributeError: 'NoneType' object has no attribute 'foo'`

**Plain English:** you called `.foo()` on something that is `None`. Usually a function you called returned `None` when you expected it to return an object.

**First place to look:** a preceding line that assigned from a function that can return `None` (for example, `re.match` when nothing matches, or `dict.get` with no default).

### `FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'`

**Plain English:** Python cannot find the file at the path you gave it.

**First place to look:** the *current working directory*. Print `import os; os.getcwd()` — the path is relative to that. In Jupyter, the current directory is usually the directory containing the `.ipynb` file, not the project root. See [sec-filesystem](#sec-filesystem).

## 6.4 4. Chained tracebacks: “during handling of the above exception”

Sometimes a traceback has two sections joined by a line that says:

    During handling of the above exception, another exception occurred:

or

    The above exception was the direct cause of the following exception:

This means the code caught an exception and raised a *new* one while handling it. Pandas does this constantly: it catches a low-level `ValueError` from numpy and re-raises it as a more helpful `pandas.errors.ParserError` with a better message. To debug, **read the original (top) exception first** — that is the root cause — and use the second one as context about how it manifested.

## 6.5 5. Tracebacks in Jupyter notebooks

Jupyter adds some noise of its own. A traceback from a failing notebook cell looks something like:

    ---------------------------------------------------------------------------
    KeyError                                  Traceback (most recent call last)
    Cell In[7], line 3
          1 import pandas as pd
          2 df = pd.read_csv("sales.csv")
    ----> 3 df["date"].dt.year
          4
          5 print(df.head())

    File ~/envs/project/lib/python3.11/site-packages/pandas/core/frame.py:3893, in DataFrame.__getitem__(self, key)
       3891 if self.columns.nlevels > 1:
       3892     return self._getitem_multilevel(key)
    -> 3893     indexer = self.columns.get_loc(key)
    ...
    KeyError: 'date'

A few things worth knowing:

- **The `Cell In[7]` header names the cell by its execution number**, not by the cell’s position in the notebook. If you re-run cells out of order, these numbers can get confusing fast — see [sec-jupyter](#sec-jupyter) for why you should re-run from the top periodically.
- **The `---->` arrow marks the exact line inside that cell** that Python was executing. The arrow plus the line contents is effectively the same as a `File ..., line ...` frame in a script traceback.
- **Frames in libraries are printed in full**, same as in a script traceback. The “your code, bottom up” heuristic still applies.

## 6.6 6. Searching for errors online

When you paste an error message into a search engine, include the **exception type** and the **static part of the message**. Strip out things that are specific to your machine: file paths, variable values, line numbers. For example, do not search

> `FileNotFoundError: [Errno 2] No such file or directory: '/Users/alex/project/data/sales_2024_q3.csv'`

search instead for

> `FileNotFoundError No such file or directory pandas read_csv`

The static part plus the library is usually enough to land you on a Stack Overflow answer with your exact problem.

If the exception is from a library, add the library name. If the exception is a `SyntaxError` or `IndentationError`, don’t bother searching — those are almost always typos in your own code that you will spot faster by re-reading.

## 6.7 7. Worked examples

### Example 1: `KeyError` in pandas

You run:

``` python
import pandas as pd
df = pd.read_csv("sales.csv")
print(df["date"].dt.year.value_counts())
```

and see:

    KeyError: 'date'

**Read the traceback bottom-up.** The last line is `KeyError: 'date'`. The bottommost frame is inside pandas (`pandas/core/indexes/base.py`), which is not helpful. Scan upward until you hit a frame in *your* file — in this case, the `Cell In[7]` or script frame. That frame points at `df["date"]`. The problem is not the date arithmetic; it is that pandas cannot find a column called `date` at all.

**Next step:** run `df.columns.tolist()` and look for similar names. You will probably find `'Date'`, `' date'`, or `'date '`. Fix the column name (or normalize with `df.columns = df.columns.str.strip().str.lower()`) and the error goes away.

### Example 2: `ValueError: could not convert string to float`

You run:

``` python
import pandas as pd
df = pd.read_csv("measurements.csv")
df["reading"].mean()
```

and see:

    ValueError: could not convert string to float: 'N/A'

**Read the traceback bottom-up.** The exception is in numpy, several frames deep inside pandas. Your frame is the `.mean()` call. The problem is not `.mean()` itself; it is that the `reading` column contains the string `'N/A'` which pandas read as a string rather than a missing value, and numpy can’t take the mean of strings.

**Next step:** tell `read_csv` to treat `'N/A'` as missing:

``` python
df = pd.read_csv("measurements.csv", na_values=["N/A"])
```

See [sec-data-file-formats](#sec-data-file-formats) for the full list of ways missing values can hide in CSVs.

### Example 3: Chained traceback

    Traceback (most recent call last):
      File "fetch.py", line 12, in <module>
        data = load_user(42)
      File "fetch.py", line 6, in load_user
        return json.loads(resp.text)
      File ".../json/decoder.py", line 337, in decode
        raise JSONDecodeError("Expecting value", s, err.value) from None
    json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

    The above exception was the direct cause of the following exception:

    Traceback (most recent call last):
      File "fetch.py", line 14, in <module>
        raise RuntimeError("failed to load user profile") from e
    RuntimeError: failed to load user profile

**Read the top block first.** The original problem is `JSONDecodeError: Expecting value: line 1 column 1 (char 0)` — the response body was empty or not valid JSON. The `RuntimeError` is your own code wrapping the library error with a friendlier message.

**Next step:** print `resp.status_code` and `resp.text[:200]` before the `json.loads` call. You will probably find an HTML error page or an empty response.

## 6.8 8. Exercises

1.  Take a working Python script of your own and deliberately break it in four ways: misspell a variable name, delete an `import`, index past the end of a list, and call a method on `None`. Read each traceback and write down, in a single sentence, what the “what” and “where” are.
2.  Find a traceback in your own recent course work (a screenshot or a notebook cell output). Without re-running the code, write down your best guess at the root cause based only on the traceback. Then re-run to confirm.
3.  Pick a library you use often (pandas, numpy, matplotlib). Deliberately trigger an error inside it and follow the “bottom-up to your code” heuristic to find which line of yours caused the bad input.
4.  In a Jupyter notebook, run cells in a deliberately-wrong order so that a variable is `None` when the next cell uses it. Read the resulting traceback and practice reading the `Cell In[N]` header.
5.  Pick the most confusing error message you encountered in the last week, strip out the machine-specific parts, paste the static part into a search engine, and write down the first Stack Overflow answer you found. Was it helpful? If not, what made the message hard to search for?

## 6.9 9. One-page checklist

- Look at the **last line** first: exception type and message = *what*.
- Look at the **bottommost frame** inside *your* code: file and line = *where*.
- If the bottommost frame is in a library, scan **upward** until you hit a frame from your project.
- For chained tracebacks, read the **top block** first: that is the root cause.
- In Jupyter, the `Cell In[N]` header names the cell by execution number, and the `---->` arrow marks the exact offending line.
- Before asking for help, paste the traceback in full — never just the error message. The stack is half the information. See [sec-asking-questions](#sec-asking-questions).
- When searching online, include the exception type and the static part of the message; strip file paths, values, and line numbers.

## 6.10 10. Quick reference: common exceptions → first suspect

| Exception                    | First suspect                              |
|------------------------------|--------------------------------------------|
| `NameError`                  | typo or unrun cell                         |
| `ModuleNotFoundError`        | wrong environment or kernel                |
| `SyntaxError`                | unclosed bracket on this or previous line  |
| `IndentationError`           | tabs vs. spaces                            |
| `TypeError`                  | wrong argument type or count               |
| `ValueError`                 | wrong value (e.g., missing-value sentinel) |
| `KeyError`                   | dict or DataFrame column typo              |
| `IndexError`                 | off-by-one, empty list                     |
| `AttributeError: 'NoneType'` | a function returned `None` earlier         |
| `FileNotFoundError`          | current working directory mismatch         |
