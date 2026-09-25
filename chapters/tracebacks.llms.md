# 7  Reading Python Tracebacks

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-debugging](#sec-debugging).
>
> **See also:** [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks), [sec-asking-questions](#sec-asking-questions), [sec-latex](#sec-latex).

## Purpose

![Fry from Futurama Meme: Not Sure If My Bug Or The Library’s Bug.](../graphics/memes/tracebacks.png)

You run a cell that worked yesterday, and the screen fills with thirty lines of red text: file paths you’ve never seen, function names with underscores on both sides, rows of `^^^^^^`, and at the very bottom, `KeyError: 'date'`. Your stomach drops a little. You scroll past the whole thing, stare at your code, and start changing things until the red goes away.

If that’s how errors have gone for you so far, you’re in good company, and you’re also leaving most of the help on the table. That wall of text is a [traceback](../chapters/appendix-glossary.llms.md#term-traceback) (the general name is a [stack trace](https://en.wikipedia.org/wiki/Stack_trace)), and it’s the best evidence you’ll ever get when something breaks. It names the file, the line, the chain of function calls that led there, and usually the exact value that caused the trouble. Once you can read one, most bug hunts go from “I have no idea what’s wrong” to “I know which line to look at, and roughly why.”

This chapter teaches you to read them. It’s short on purpose: reading tracebacks is a focused skill you can pick up in half an hour and use for the rest of your life with Python. It covers the parts of a traceback, how to find the line that’s yours among the library’s, the ten errors you’ll meet most, chained tracebacks, and how tracebacks look in Jupyter. What to do *after* the traceback has pointed you somewhere, the investigative loop of hypotheses and experiments, is [sec-debugging](#sec-debugging). Every traceback shown here is real output from Python 3.11 and pandas 3, with only the file paths changed.

## Why read this chapter

- You see a screen of red text and your first move is to scroll past it, and you’d like to know what it was trying to tell you.
- The last line says `KeyError: 'date'` but every file named in the error is somewhere inside pandas, and you can’t tell whether the bug is yours or the library’s.
- You got a traceback with two sections and the line *“During handling of the above exception, another exception occurred,”* and you don’t know which error to fix.
- Python says `ModuleNotFoundError: No module named 'seaborn'` right after you installed seaborn, and you’re starting to doubt your sanity.
- Your notebook says the problem is in `Cell In[7]`, and there is no cell 7 that you can find.
- You pasted an error into a search engine and got nothing useful back, or a hundred pages that are almost, but not quite, your problem.
- You’d like to ask a classmate, a TA, or an AI assistant for help and give them what they need to answer on the first try.

## Running theme: the last line tells you *what*, the stack tells you *where*

Every traceback answers two questions. The last line says what went wrong, and the frames above it say where it happened and how the program got there. You’ll usually need both: the “what” is a label, and the “where” is the evidence.

## 7.1 The anatomy of a traceback

The best way to stop fearing tracebacks is to take one apart. Here’s a small script that reads numbers from a file and averages them:

``` python
# analysis.py
def compute_mean(xs):
    return sum(xs) / len(xs)


def summarize(path):
    with open(path) as f:
        values = [float(line) for line in f if line.strip()]
    return compute_mean(values)


print(summarize("readings.txt"))
```

It works fine until the day `readings.txt` arrives empty. Then `python analysis.py` prints this:

``` text
Traceback (most recent call last):
  File "/Users/you/project/analysis.py", line 11, in <module>
    print(summarize("readings.txt"))
          ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/analysis.py", line 8, in summarize
    return compute_mean(values)
           ^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/analysis.py", line 2, in compute_mean
    return sum(xs) / len(xs)
           ~~~~~~~~^~~~~~~~~
ZeroDivisionError: division by zero
```

It looks like a lot, but it has only three parts. The first line, `Traceback (most recent call last):`, is a header. It means an [exception](https://en.wikipedia.org/wiki/Exception_handling) (Python’s word for an error that stops the normal flow of the program) made it all the way up without anything catching it, and Python is about to show you how it got there.

The middle is the **stack**, a list of **frames**. Each frame is one function call that was still in progress when the error happened: the program’s [call stack](https://en.wikipedia.org/wiki/Call_stack), frozen at the moment of the crash. Every frame starts with a line of the form `File "...", line N, in name`, giving the file, the line number, and the function the program was inside (`<module>` means “the top level of the file, not inside any function”). Under it, Python prints that line of your source code, so you don’t have to go find it.

The last line is the **exception type** and **message**: `ZeroDivisionError: division by zero`. The part before the colon is the kind of error, here a [`ZeroDivisionError`](https://docs.python.org/3/library/exceptions.html#ZeroDivisionError). The part after the colon is a message written for you, and it’s often the most useful sentence on the screen.

The phrase that trips people up is **“most recent call last.”** Python prints the stack in the order things happened, so the top frame is where your program started and the bottom frame is where it was when it crashed. Read the frames top to bottom and you get the story: line 11 called `summarize`, `summarize` called `compute_mean` on line 8, and `compute_mean` tried to divide on line 2. Read the bottom line and you get the ending: it divided by zero, because `len(xs)` was 0, because the file was empty. Notice that the line that crashed isn’t really the line that’s wrong. `compute_mean` did exactly what it was told; the fix belongs in `summarize`, or wherever you decide an empty file should be handled. A traceback tells you where the program *noticed* the problem, and part of your job is walking back up the stack to where the problem *started*.

The `^^^^^` and `~~~~^~~~` marks under each line are new in Python 3.11 ([what’s new in 3.11](https://docs.python.org/3/whatsnew/3.11.html#whatsnew311-pep657) has the details). They underline the exact piece of the line that was running. On line 2, the `~` marks cover the two sides of the division and the lone `^` points at the `/` itself, which tells you the division failed, not the `sum` or the `len`. On a line with several things happening, like `df["price"].astype(float).mean()`, that pointer saves you from guessing which step blew up. If you’re on an older Python, you just won’t see them; everything else here still applies.

## 7.2 Reading up, reading down: finding the frame that’s yours

The traceback above lives entirely in your own file, so it’s easy. The ones that make people give up are the ones that wander into someone else’s code. Here’s a cleaning script that adds a year column to a table of sales:

``` python
# src/cleaning.py
import pandas as pd


def add_year(df):
    df["year"] = df["date"].dt.year
    return df


sales = pd.read_csv("sales.csv")
sales.columns = sales.columns.str.lower()
sales = add_year(sales)
```

and here’s what Python says:

``` text
Traceback (most recent call last):
  File "/Users/you/project/src/cleaning.py", line 11, in <module>
    sales = add_year(sales)
            ^^^^^^^^^^^^^^^
  File "/Users/you/project/src/cleaning.py", line 5, in add_year
    df["year"] = df["date"].dt.year
                 ^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/generic.py", line 6194, in __getattr__
    return object.__getattribute__(self, name)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/accessor.py", line 230, in __get__
    return self._accessor(obj)
           ^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/indexes/accessors.py", line 698, in __new__
    raise AttributeError("Can only use .dt accessor with datetimelike values")
AttributeError: Can only use .dt accessor with datetimelike values. Did you mean: 'at'?
```

The bottom three frames are inside pandas, in files you’ve never opened, and the code they show (`object.__getattribute__(self, name)`) means nothing to you. That’s normal, and it doesn’t mean pandas is broken. It means your code handed pandas something it couldn’t work with, and pandas went a few calls deep before it gave up. Staring at `accessors.py` won’t help. What helps is finding the last moment the program was in *your* code.

The trick is to learn the shape of paths that aren’t yours. Anything under `site-packages/` is a [library](../chapters/appendix-glossary.llms.md#term-library) you installed. Anything under a path like `lib/python3.11/` without `site-packages` is Python’s own standard library. File names ending in `.pyx` or `.pxi` are compiled parts of a library. Anything with `frozen importlib` in it is Python’s import machinery. Your files are the ones inside your project folder:

``` text
File ".../site-packages/pandas/core/indexes/accessors.py", line 698   # not yours
File ".../site-packages/pandas/core/accessor.py", line 230            # not yours
File ".../site-packages/pandas/core/generic.py", line 6194            # not yours
File "/Users/you/project/src/cleaning.py", line 5, in add_year        # yours: start here
```

So the rule of thumb is: **start at the bottom and scan up until you reach the first frame from your own project.** That frame is where your code handed over the bad input, and it’s almost always the line to fix. Here it’s line 5, `df["date"].dt.year`, and together with the message the story is clear. The [`.dt` accessor](https://pandas.pydata.org/docs/user_guide/basics.html#basics-dt-accessors) only works on columns of real dates, and `date` came out of `read_csv` as plain text. The fix is to convert the column with [`pd.to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html) first.

Two directions, then, for two different questions. When the bottom frame is in your code, **read bottom-up**: the crash site is right there, and you’ve probably found the bug. When the bottom frame is in a library, **keep scanning up** until the paths turn familiar. And when you want to know *how* the program got somewhere surprising, **read top-down**, like a trail of breadcrumbs from where you started.

One more thing to notice in that last line: *Did you mean: ‘at’?* Recent versions of Python add these suggestions to `NameError` and `AttributeError` messages by looking for a similarly spelled name. When you’ve made a typo, they’re wonderful. Here the suggestion is nonsense (the problem was never the spelling of `dt`), so treat them as hints, not diagnoses.

## 7.3 The ten exceptions you’ll see most often

A handful of error types account for most of what you’ll meet in a first data course. Each one below comes with a real example, what it means in plain English, and the first place to look. Every exception name links to its entry in Python’s own documentation.

### NameError: a name Python has never seen

``` text
Traceback (most recent call last):
  File "/Users/you/project/report.py", line 2, in <module>
    print(datafame)
          ^^^^^^^^
NameError: name 'datafame' is not defined. Did you mean: 'dataframe'?
```

A [`NameError`](https://docs.python.org/3/library/exceptions.html#NameError) means you used a variable or function Python has never heard of. The usual causes are a typo (`datafame` for `dataframe`), a notebook cell you never ran (or ran before the kernel restarted), or an import under a different name than the one you’re typing: after `import pandas as pd`, writing `pandas.read_csv` gets you `NameError: name 'pandas' is not defined`, because the name you created was `pd`.

### ModuleNotFoundError and ImportError: a package Python can’t find

``` text
Traceback (most recent call last):
  File "/Users/you/project/plots.py", line 1, in <module>
    import seaborn
ModuleNotFoundError: No module named 'seaborn'
```

A [`ModuleNotFoundError`](https://docs.python.org/3/library/exceptions.html#ModuleNotFoundError) means Python looked everywhere it knows to look (its module search path) and didn’t find the package. The maddening version is when you’re *sure* you installed it. Almost always, you did, just into a different environment than the one running your code. Ask the Python that’s running which one it is with `import sys; print(sys.executable)` ([`sys.executable`](https://docs.python.org/3/library/sys.html#sys.executable) is the path to the interpreter), and ask that same environment whether the package is there with `python -m pip show seaborn` ([`pip show`](https://pip.pypa.io/en/stable/cli/pip_show/) prints `WARNING: Package(s) not found` if it isn’t) or `conda list seaborn`. In a Jupyter notebook, the environment that matters is the kernel’s, and running [`%pip install seaborn`](https://ipython.readthedocs.io/en/stable/interactive/magics.html#magic-pip) in a cell installs into it directly. [sec-virtual-environments](#sec-virtual-environments) and [sec-pkg-mgmt](#sec-pkg-mgmt) explain why there’s more than one Python on your computer in the first place.

Its cousin, [`ImportError`](https://docs.python.org/3/library/exceptions.html#ImportError), means the package was found but the thing you asked for inside it wasn’t: `from pandas import read_cvs` fails with `ImportError: cannot import name 'read_cvs' from 'pandas'`. Check the spelling, then check that the function exists in the version you have installed.

### SyntaxError: code Python can’t read

``` text
  File "/Users/you/project/totals.py", line 1
    total = sum([1, 2, 3]
               ^
SyntaxError: '(' was never closed
```

A [`SyntaxError`](https://docs.python.org/3/library/exceptions.html#SyntaxError) is different from every other error in this list, and you can see it in the output: there’s no `Traceback (most recent call last)` header and no stack. Python couldn’t even read the file, so nothing ran. Recent versions of Python give much friendlier messages here than older ones did. You’ll see things like `'(' was never closed`, `expected ':'` (a `def`, `for`, `if`, or `while` line missing its colon), and `Missing parentheses in call to 'print'. Did you mean print(...)?`, which is what you get from old Python 2 code like `print "hello"`. Sometimes all you get is a plain `SyntaxError: invalid syntax`. Look at the caret first, then at the line or two above it: an unclosed bracket or quote on one line often isn’t noticed until the next.

### IndentationError: whitespace that doesn’t line up

``` text
  File "/Users/you/project/greet.py", line 2
    print("hi", name)
    ^
IndentationError: expected an indented block after function definition on line 1
```

Python uses indentation to decide which lines belong to which block (the fancy name is the [off-side rule](https://en.wikipedia.org/wiki/Off-side_rule)), so whitespace that doesn’t line up is a real error. [`IndentationError`](https://docs.python.org/3/library/exceptions.html#IndentationError) is a special kind of `SyntaxError`, and like it, it stops the file before anything runs. You’ll see `expected an indented block` (a `def` or `if` with nothing indented under it), `unexpected indent` (a line indented for no reason, which happens a lot when you paste code), and the sneakiest one, [`TabError`](https://docs.python.org/3/library/exceptions.html#TabError): `inconsistent use of tabs and spaces in indentation`. Tabs and spaces look identical on screen, which is why this one is so frustrating. Turn on your editor’s “render whitespace” option to see them, and set it to insert four spaces when you press Tab, as [PEP 8](https://peps.python.org/pep-0008/#tabs-or-spaces) recommends ([sec-text-editors](#sec-text-editors) shows where the setting lives).

### TypeError: the wrong kind of value

``` text
Traceback (most recent call last):
  File "/Users/you/project/label.py", line 2, in <module>
    print("Age: " + age)
          ~~~~~~~~^~~~~
TypeError: can only concatenate str (not "int") to str
```

A [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError) means you tried an operation on a kind of value that doesn’t support it, like adding a number to a piece of text. The same exception covers calling a function with the wrong number of arguments: `f() takes 2 positional arguments but 3 were given`. Look at the line the bottom frame (or your last frame) points to, and check what each value really is by printing `type(x)` just before it. The usual surprise is a number that’s secretly a string, or a list you thought was a dictionary.

### ValueError: the right kind, the wrong value

``` text
Traceback (most recent call last):
  File "/Users/you/project/convert.py", line 1, in <module>
    float("N/A")
ValueError: could not convert string to float: 'N/A'
```

A [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError) means the type was fine but this particular value wasn’t: `float` accepts strings, just not the string `'N/A'`. In data work the usual culprit is a [sentinel value](https://en.wikipedia.org/wiki/Sentinel_value), a code like `"N/A"`, `"-"`, or `"no reading"` that someone typed where a number should go. pandas’ `read_csv` already treats a standard set of codes, including `N/A`, `NA`, `NULL`, and empty cells, as missing, and you can add your own with [`na_values=`](https://pandas.pydata.org/docs/user_guide/io.html#na-values). Anything not on the list comes in as text, and the error shows up later when you try to use the column as numbers (see [sec-data-file-formats](#sec-data-file-formats), and worked example 2 below). Handily, the message quotes the offending value, so you know exactly what to search your file for.

### KeyError: a key or column that isn’t there

``` text
Traceback (most recent call last):
  File "/Users/you/project/lookup.py", line 2, in <module>
    print(row["date"])
          ~~~^^^^^^^^
KeyError: 'date'
```

A [`KeyError`](https://docs.python.org/3/library/exceptions.html#KeyError) means you asked a dictionary for a key it doesn’t have, and a DataFrame counts as a dictionary of columns here, so a missing column raises the same thing. The message is just the key you asked for, in quotes. Look closely at those quotes: `'date '` with a trailing space and `'Date'` with a capital D are both classics. Print `df.columns.tolist()` to see the names that are really there, and check whether an earlier cell dropped or renamed the column. A `KeyError` raised inside pandas also comes as a two-part chained traceback, which worked example 1 walks through.

### IndexError: past the end of a list

``` text
Traceback (most recent call last):
  File "/Users/you/project/scores.py", line 2, in <module>
    print(scores[3])
          ~~~~~~^^^
IndexError: list index out of range
```

An [`IndexError`](https://docs.python.org/3/library/exceptions.html#IndexError) means you asked for item number *N* of a list that doesn’t have that many. Python counts from 0, so a list of three scores has positions 0, 1, and 2, and `scores[3]` is one past the end: a textbook [off-by-one error](https://en.wikipedia.org/wiki/Off-by-one_error). The other usual causes are a list that’s empty when you didn’t expect it to be, and data with fewer rows than you assumed.

### AttributeError: ‘NoneType’ object has no attribute …

``` text
Traceback (most recent call last):
  File "/Users/you/project/extract.py", line 3, in <module>
    print(m.group())
          ^^^^^^^
AttributeError: 'NoneType' object has no attribute 'group'
```

An [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError) means you asked a value for a method or attribute it doesn’t have. When the value is `None` (Python’s “nothing here”), the real problem is almost never on this line. It’s on an earlier line that assigned from a function that returned `None` when you expected something. Here `m` came from [`re.match`](https://docs.python.org/3/library/re.html#re.match), which returns `None` when the pattern doesn’t match. Other common sources are [`dict.get`](https://docs.python.org/3/library/stdtypes.html#dict.get) with no default, and your own function that forgot its `return` statement. Walk back up to the assignment and ask why it came back empty.

### FileNotFoundError: a path that doesn’t lead anywhere

``` text
Traceback (most recent call last):
  File "/Users/you/project/load.py", line 1, in <module>
    with open("data.csv") as f:
         ^^^^^^^^^^^^^^^^
FileNotFoundError: [Errno 2] No such file or directory: 'data.csv'
```

A [`FileNotFoundError`](https://docs.python.org/3/library/exceptions.html#FileNotFoundError) means there’s no file at the path you gave. “But it’s right there!” is the usual reaction, and the answer is usually the [working directory](https://en.wikipedia.org/wiki/Working_directory). A relative [path](../chapters/appendix-glossary.llms.md#term-path) like `"data.csv"` is looked up relative to wherever Python is running, not relative to your script. Print [`os.getcwd()`](https://docs.python.org/3/library/os.html#os.getcwd) (after `import os`) to see where that is. In Jupyter, it’s usually the folder that contains the `.ipynb` file, not your project’s top folder, so a notebook in `notebooks/` needs `"../data/data.csv"`. [sec-filesystem](#sec-filesystem) covers paths properly.

## 7.4 Chained tracebacks: when one error leads to another

Sooner or later you’ll get a traceback that seems to contain two tracebacks, joined by one of these lines:

``` text
During handling of the above exception, another exception occurred:
```

``` text
The above exception was the direct cause of the following exception:
```

Both mean the same basic thing: some code caught the first error and, while dealing with it, a second error was raised. Python shows you both, oldest first, so the block at the top is where the trouble began and the block at the bottom is where it ended. The two phrases tell you *how* the second error came about, and that changes which one you fix.

**“During handling of the above exception”** usually means the error-handling code itself had a bug. This script tries to turn price strings into numbers and fall back to “not a number” when it can’t:

``` python
# prices.py
raw_prices = ["12.50", "89.25", "call for price"]

prices = []
for raw in raw_prices:
    try:
        prices.append(float(raw))
    except ValueError:
        prices.append(flaot("nan"))

print(prices)
```

``` text
Traceback (most recent call last):
  File "/Users/you/project/prices.py", line 6, in <module>
    prices.append(float(raw))
                  ^^^^^^^^^^
ValueError: could not convert string to float: 'call for price'

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/Users/you/project/prices.py", line 8, in <module>
    prices.append(flaot("nan"))
                  ^^^^^
NameError: name 'flaot' is not defined. Did you mean: 'float'?
```

The first `ValueError` was expected: that’s what the `try`/`except` was there for. The real bug is the second block, a typo in the `except` branch. Fix `flaot` and the script works. The general lesson is to read both blocks and ask which one is the surprise.

**“The above exception was the direct cause”** means someone deliberately raised a new error on top of the old one, using [`raise ... from ...`](https://docs.python.org/3/reference/simple_stmts.html#the-raise-statement). Libraries do this to translate a low-level error into one that makes more sense to you, and you may do it yourself to add context. Here the top block usually holds the underlying cause, and the bottom block holds the friendlier summary. pandas does this every time you ask for a column that doesn’t exist, and in that case it’s the *bottom* block that contains your code, while the top block is pandas’ internal lookup. Worked example 1 reads one of those line by line, and worked example 3 reads the other kind, where your own code wraps an error from a library.

Whichever phrase you see, the approach is the same as for any traceback. Read the very last line to see how things ended, find the frames from your own project in either block, and then read the other block for context on why.

## 7.5 Tracebacks in Jupyter notebooks

Jupyter prints tracebacks in its own style, with more source code and less punctuation, and the first time you see one it can look like a different language. The bones are the same. Here’s the [notebook](../chapters/appendix-glossary.llms.md#term-notebook) version of a very common mistake, asking for a `date` column in a file whose column is really called `Date`:

``` text
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
File ~/project/.venv/lib/python3.11/site-packages/pandas/core/indexes/base.py:3641, in Index.get_loc(self, key)
   3640 try:
-> 3641     return self._engine.get_loc(casted_key)
   3642 except KeyError as err:

File pandas/_libs/index.pyx:168, in pandas._libs.index.IndexEngine.get_loc()
--> 168 'Could not get source, probably due dynamically evaluated source code.'
File pandas/_libs/index.pyx:197, in pandas._libs.index.IndexEngine.get_loc()
--> 197 'Could not get source, probably due dynamically evaluated source code.'
File pandas/_libs/hashtable_class_helper.pxi:7668, in pandas._libs.hashtable.PyObjectHashTable.get_item()
-> 7668 'Could not get source, probably due dynamically evaluated source code.'
File pandas/_libs/hashtable_class_helper.pxi:7676, in pandas._libs.hashtable.PyObjectHashTable.get_item()
-> 7676 'Could not get source, probably due dynamically evaluated source code.'
KeyError: 'date'

The above exception was the direct cause of the following exception:

KeyError                                  Traceback (most recent call last)
Cell In[7], line 3
      1 import pandas as pd
      2 df = pd.read_csv("sales.csv")
----> 3 years = df["date"].dt.year
      5 print(years.value_counts())

File ~/project/.venv/lib/python3.11/site-packages/pandas/core/frame.py:4378, in DataFrame.__getitem__(self, key)
   4374
   4375         if is_single_key:
   4376             if self.columns.nlevels > 1:
   4377                 return self._getitem_multilevel(key)
-> 4378             indexer = self.columns.get_loc(key)
   4379             if is_integer(indexer):
   4380                 indexer = [indexer]
   4381         else:

File ~/project/.venv/lib/python3.11/site-packages/pandas/core/indexes/base.py:3648, in Index.get_loc(self, key)
   3643     if isinstance(casted_key, slice) or (
   3644         isinstance(casted_key, abc.Iterable)
   3645         and any(isinstance(x, slice) for x in casted_key)
   3646     ):
   3647         raise InvalidIndexError(key) from err
-> 3648     raise KeyError(key) from err
   3649 except TypeError:
   3650     # If we have a listlike key, _check_indexing_error will raise
   3651     #  InvalidIndexError. Otherwise we fall through and re-raise
   3652     #  the TypeError.
   3653     self._check_indexing_error(key)

KeyError: 'date'
```

Fifty lines for a one-letter mistake, and nearly all of it is pandas. Here’s how to cut it down to size.

Each block starts with the exception type on the left and `Traceback (most recent call last)` on the right, and each frame starts with `File ...:line, in function`, the same information as a script traceback in a different layout. Instead of one line of source per frame, Jupyter shows a few lines around it, with an arrow (`->` or `---->`) pointing at the line that was running. The lines saying *Could not get source* come from the parts of pandas written in [Cython](https://en.wikipedia.org/wiki/Cython) and compiled, where there’s no Python source to show; skip them.

The frame that’s yours is the one that starts with `Cell In[7], line 3`: that’s your notebook cell, and the `---->` arrow points at `years = df["date"].dt.year`. It’s in the second block, as usual for a `raise ... from` chain inside a library, so the bottom-up rule still works: start at the bottom, pass the two pandas frames, and stop at the first cell.

The one genuinely confusing part is the number. `In[7]` is the cell’s *execution count*, the number that appears in the brackets next to the cell after it runs, not its position in the notebook. If you’ve been running cells out of order, re-running some and skipping others, cell 7 might be the second cell on the page or the twentieth. That’s why “there is no cell 7” happens. When the numbers stop matching what you see, restart the [kernel](../chapters/appendix-glossary.llms.md#term-kernel) and run everything from the top (in [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html), that’s **Restart Kernel and Run All Cells…** in the Kernel menu), and see [sec-jupyter](#sec-jupyter) for why out-of-order state causes so much grief.

## 7.6 Searching for an error online

Most errors you’ll ever hit, someone else has hit first and asked about. The trick is searching for their error, not yours. Your message is full of details only you have, such as your user name, your file names, and your data values, and a search engine will dutifully try to match all of them. So don’t search for

> `FileNotFoundError: [Errno 2] No such file or directory: '/Users/alex/project/data/sales_2024_q3.csv'`

Search instead for the exception type, the part of the message that would be the same on anyone’s computer, and the library or function involved:

> `FileNotFoundError No such file or directory pandas read_csv`

That’s usually enough to land you on a [Stack Overflow](https://en.wikipedia.org/wiki/Stack_Overflow) question with your exact problem. Two cautions. Check the dates on what you find: error messages change between versions, and pandas 3 changed how it stores text columns, giving them their own `str` type, so some errors about text columns now read differently (the [pandas 3 string migration guide](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html) explains the change), so an answer from 2019 may quote a message you’ll never see. And for a `SyntaxError` or `IndentationError`, don’t bother searching; it’s a typo in your own file, and you’ll find it faster by rereading the line the caret points to and the one above.

When you ask a person or an AI assistant instead, flip the rule: give them the *whole* traceback, not just the last line, plus the code that produced it. The stack is half the information, and “I got a KeyError” alone can’t be answered. The best questions come with a [minimal reproducible example](https://en.wikipedia.org/wiki/Minimal_reproducible_example), the smallest bit of code that still shows the error; [sec-asking-questions](#sec-asking-questions) shows how to build one, and [sec-ai-llm](#sec-ai-llm) covers working with AI tools.

## 7.7 Stakes and politics

Look at the first frame of a traceback from your own laptop. It might read `File "/Users/maria.lopez/Documents/counseling-intake/clean_2026.py"`, and in one line it has told a stranger your name, what project you’re on, and what the data is about, before anyone reads the error. The message can say more: a `ValueError` quotes the bad value, and a `KeyError` quotes the key, so a traceback can carry a piece of the data itself. Paste it into a public forum or a chatbot and all of that goes too. When the data concerns other people, that can be [personal data](https://en.wikipedia.org/wiki/Personal_data) you had promised to protect.

There’s a second cost, easy to miss if English is your first language. Exception names, messages, and nearly every answer you’ll find by searching them are in English, so a student who reads English as a second language does a translation step on every bug that a native speaker doesn’t. Tools like `friendly_traceback` (see Further reading) show that the default could be otherwise.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: before you paste a traceback anywhere, read it once as a stranger would, and redact whatever isn’t part of the bug.

## 7.8 Worked examples

### 1. A KeyError in pandas

You have a small file of sales, `sales.csv`, whose first line is `Date,store,amount`. You run this script:

``` python
# sales_report.py
import pandas as pd

df = pd.read_csv("sales.csv")
print(df["date"].dt.year.value_counts())
```

and get:

``` text
Traceback (most recent call last):
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/indexes/base.py", line 3641, in get_loc
    return self._engine.get_loc(casted_key)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pandas/_libs/index.pyx", line 168, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/index.pyx", line 197, in pandas._libs.index.IndexEngine.get_loc
  File "pandas/_libs/hashtable_class_helper.pxi", line 7668, in pandas._libs.hashtable.PyObjectHashTable.get_item
  File "pandas/_libs/hashtable_class_helper.pxi", line 7676, in pandas._libs.hashtable.PyObjectHashTable.get_item
KeyError: 'date'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/you/project/sales_report.py", line 4, in <module>
    print(df["date"].dt.year.value_counts())
          ~~^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/frame.py", line 4378, in __getitem__
    indexer = self.columns.get_loc(key)
              ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/indexes/base.py", line 3648, in get_loc
    raise KeyError(key) from err
KeyError: 'date'
```

**Read the last line first.** `KeyError: 'date'`: something asked for a key called `date` and didn’t find it.

**Find your frame.** The top block is entirely pandas: its first frame is in `site-packages`, and the rest are compiled `.pyx` files. That block is pandas looking the name up internally, and you can skip it. In the bottom block, scanning up from the bottom, you pass `base.py` and `frame.py` and reach `sales_report.py`, line 4. The markers under that line (`~~^^^^^^^^`) point at `df["date"]`, not at `.dt.year` or `.value_counts()`. So the problem isn’t the date handling at all; pandas can’t find a column called `date`.

**Look at what’s really there.** Run `print(df.columns.tolist())`, and you’ll see `['Date', 'store', 'amount']`. The column has a capital D. You could type `df["Date"]`, but it’s more durable to clean every name once, right after loading, so the next file’s `" Date "` doesn’t bite you either:

``` python
df.columns = df.columns.str.strip().str.lower()
```

**Expect the next error.** With the name fixed, the same line now fails with `AttributeError: Can only use .dt accessor with datetimelike values`, the error from earlier in this chapter, because the column is still text. Convert it, and the script prints the year counts:

``` python
df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d")
print(df["date"].dt.year.value_counts())
```

Fixing one error and meeting the next is normal. It’s progress, not failure: each traceback is further down the script than the last.

### 2. A “numeric” column that won’t average

Your file `measurements.csv` has a `reading` column of numbers, with a few gaps. You run:

``` python
# measurements_report.py
import pandas as pd

df = pd.read_csv("measurements.csv")
print(df["reading"].mean())
```

and get:

``` text
Traceback (most recent call last):
  File "/Users/you/project/measurements_report.py", line 4, in <module>
    print(df["reading"].mean())
          ^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/util/_decorators.py", line 336, in wrapper
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/series.py", line 8113, in mean
    return NDFrame.mean(
           ^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/generic.py", line 11819, in mean
    return self._stat_function(
           ^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/generic.py", line 11773, in _stat_function
    return self._reduce(
           ^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/series.py", line 7480, in _reduce
    result = delegate._reduce(name, skipna=skipna, **kwds)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/you/project/.venv/lib/python3.11/site-packages/pandas/core/arrays/string_arrow.py", line 564, in _reduce
    raise TypeError(f"Cannot perform reduction '{name}' with string dtype")
TypeError: Cannot perform reduction 'mean' with string dtype
```

**Read the last line first.** pandas can’t take the mean of a column whose type is *string*. That’s surprising, because `reading` is supposed to hold numbers.

**Find your frame.** Six frames are pandas; one is yours, at the very top: line 4, the `.mean()` call. But `.mean()` isn’t the mistake. It’s doing its job on a column that came out of `read_csv` as text, so the problem started one line earlier, when the file was read.

**Find the value that made it text.** `print(df.dtypes)` confirms that `reading` is `str`. To see which values couldn’t be read as numbers, convert with [`pd.to_numeric`](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html) and look at what turned into missing:

``` python
as_numbers = pd.to_numeric(df["reading"], errors="coerce")
print(df[as_numbers.isna() & df["reading"].notna()])
```

This prints one row, site `D`, whose reading is the text `no reading`. (The file also has an `N/A`, but `read_csv` already treats that as missing, so it doesn’t show up.) One stray string was enough to make the whole column text.

**Fix it where the file is read.** Tell `read_csv` that `no reading` means missing, and the mean works (it prints `3.65` for this file):

``` python
df = pd.read_csv("measurements.csv", na_values=["no reading"])
print(df["reading"].mean())
```

If you’d tried `df["reading"].astype(float)` instead, you’d have gotten `ValueError: could not convert string to float: 'no reading'`, which names the culprit directly. Different route, same cause. See [sec-data-file-formats](#sec-data-file-formats) for the other ways missing values hide in files.

### 3. A chained traceback from a web request

This script asks a web server for a user’s profile and parses the reply as [JSON](../chapters/appendix-glossary.llms.md#term-json), wrapping any parsing failure in an error of its own:

``` python
# fetch.py
import json

import requests


def load_user(user_id):
    resp = requests.get(f"https://example.com/users/{user_id}", timeout=10)
    return json.loads(resp.text)


try:
    data = load_user(42)
except json.JSONDecodeError as e:
    raise RuntimeError("failed to load user profile") from e
```

It prints:

``` text
Traceback (most recent call last):
  File "/Users/you/project/fetch.py", line 12, in <module>
    data = load_user(42)
           ^^^^^^^^^^^^^
  File "/Users/you/project/fetch.py", line 8, in load_user
    return json.loads(resp.text)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/usr/lib/python3.11/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/Users/you/project/fetch.py", line 14, in <module>
    raise RuntimeError("failed to load user profile") from e
RuntimeError: failed to load user profile
```

**Read the last line, then the top block.** The final error is a [`RuntimeError`](https://docs.python.org/3/library/exceptions.html#RuntimeError) that your own code raised on line 14, and all it says is that loading failed. It’s “the direct cause” phrase, so the reason is in the block above: a [`JSONDecodeError`](https://docs.python.org/3/library/json.html#json.JSONDecodeError) from [`json.loads`](https://docs.python.org/3/library/json.html#json.loads), on line 8 of your file. `Expecting value: line 1 column 1 (char 0)` means the very first character of the reply wasn’t valid JSON, which in practice means the reply was empty or wasn’t JSON at all.

**Look at what the server sent.** Before the `json.loads` line, print the status and the start of the body:

``` python
print(resp.status_code)
print(resp.text[:60])
```

It prints `404`, then `<!doctype html><html lang="en"><head><title>Example Domain</`. The server answered with an [HTTP 404](https://en.wikipedia.org/wiki/HTTP_404) “not found” page written in HTML (unsurprisingly: [example.com](https://en.wikipedia.org/wiki/Example.com) is a domain reserved for examples and has no user profiles). Nothing was wrong with the JSON parser; you were feeding it a web page. The durable fix is to check [`resp.status_code`](https://requests.readthedocs.io/en/latest/user/quickstart/#response-status-codes) before parsing, so the error you get says “the server said 404” instead of something about line 1, column 1. [sec-http-apis](#sec-http-apis) covers status codes and how to handle them.

## 7.9 Exercises

1.  Take a working Python script of your own and break it four ways: misspell a variable name, delete an `import`, index past the end of a list, and call a method on `None`. For each traceback, write one sentence naming the “what” and the “where.”
2.  Find a traceback in your own recent course work (a screenshot or a notebook cell’s output). Without rerunning anything, write down your best guess at the cause from the traceback alone. Then rerun and check.
3.  Pick a library you use often (pandas, numpy, matplotlib) and trigger an error inside it on purpose. Scan up from the bottom to the first frame of yours, and write down which line of your code supplied the bad input.
4.  Write a `try`/`except` block with a deliberate typo in the `except` branch, as in `prices.py` above. Read the chained traceback and say which of the two blocks holds the bug.
5.  In a Jupyter notebook, run cells in the wrong order so that a variable is `None` (or undefined) when a later cell uses it. Read the traceback, find the `Cell In[N]` header, and work out which cell on the page that number refers to.
6.  Pick the most confusing error message you’ve met in the last week. Strip out the parts specific to your machine, search for what’s left, and note whether the first result was helpful. If it wasn’t, what made the message hard to search for?

## 7.10 One-page checklist

- Read the **last line** first: the exception type and message tell you *what*.
- Find the **bottom frame** in your own code: its file and line tell you *where*.
- If the bottom frame is in a library (`site-packages`, `.pyx`, the standard library), scan **up** until you reach a file from your project.
- Use the `^^^^` markers to see which part of a long line failed.
- Remember that the line that crashed isn’t always the line that’s wrong; walk back up the stack to where the bad value came from.
- For chained tracebacks, read both blocks. “During handling” often means a bug in the error handler; “direct cause” means the top block holds the underlying reason.
- A `SyntaxError` or `IndentationError` has no stack: nothing ran, so look at the caret and the line above it.
- In Jupyter, `Cell In[N]` is the execution count, not the cell’s position, and the arrow marks the line that ran.
- When searching, keep the exception type and the part of the message anyone would see; drop paths, values, and line numbers.
- When asking for help, paste the whole traceback plus the code, after removing anything private (see [sec-asking-questions](#sec-asking-questions)).

## 7.11 Quick reference: common exceptions → first suspect

| Exception | First suspect |
|----|----|
| `NameError` | typo, or a cell you haven’t run |
| `ModuleNotFoundError` | installed into a different environment or kernel |
| `ImportError` | misspelled name, or a different package version |
| `SyntaxError` | unclosed bracket or quote on this line or the one above |
| `IndentationError` / `TabError` | tabs mixed with spaces, or pasted code |
| `TypeError` | wrong kind of value (often a number stored as text), or wrong number of arguments |
| `ValueError` | right type, bad value (often a missing-value code) |
| `KeyError` | misspelled key or column name, or a stray space or capital |
| `IndexError` | off-by-one, or an empty list |
| `AttributeError: 'NoneType'` | an earlier function returned `None` |
| `FileNotFoundError` | the working directory isn’t where you think |

> **NOTE:**
>
> - **Python docs**, [Built-in Exceptions](https://docs.python.org/3/library/exceptions.html) — every exception class Python has, arranged as a family tree; worth skimming once so the names start to ring bells.
> - **Python docs**, [Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html) — the official tutorial on raising, catching, and chaining exceptions, for when you want to write `try`/`except` blocks of your own.
> - **Python docs**, [`traceback` module](https://docs.python.org/3/library/traceback.html) — the standard-library tools for capturing and formatting tracebacks yourself, useful when you start logging errors from longer-running scripts.
> - **Pablo Galindo Salgado, Batuhan Taskaya, and Ammar Askar**, [PEP 657: Include Fine Grained Error Locations in Tracebacks](https://peps.python.org/pep-0657/) — the proposal behind the `^^^^` markers in Python 3.11, with examples of the guesswork they replace.
> - **Software Carpentry**, [Errors and Exceptions](https://swcarpentry.github.io/python-novice-inflammation/09-errors.html) — a beginner-friendly lesson on reading tracebacks, with exercises, from a community that teaches researchers to code.
> - **André Roberge**, [`friendly_traceback`](https://aroberge.github.io/friendly-traceback-docs/docs/html/) — a library that explains tracebacks in plain language, in English or French; useful as a learning aid and as a glimpse of error messages that don’t assume English.
