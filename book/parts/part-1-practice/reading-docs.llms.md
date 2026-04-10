# 4  Reading Official Documentation

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-asking-questions](#sec-asking-questions).
>
> **See also:** [sec-documentation](#sec-documentation), [sec-debugging](#sec-debugging), [sec-ai-llm](#sec-ai-llm).

## Purpose

A huge fraction of the frustration novices experience with programming comes from the same moment: you are stuck, you search the error online, you land on a tutorial blog post that almost-but-not-quite matches your situation, you copy a line, and it breaks something else. After two hours of this you feel like the tools are hostile. Meanwhile, the answer was three clicks away on the official documentation — but you either did not know the docs existed, did not know how to navigate them, or tried to read them like a novel and bounced off.

This chapter teaches you to read official documentation — pandas docs, Python docs, library README files, docstrings — in a way that actually answers your question. It is about the skill, not about any one library. Documentation is a reference medium: you dip into it for the answer to a specific question and then you leave. Once you learn to do that, the official docs become the fastest source of help you have, faster than Stack Overflow and much more reliable than a tutorial blog.

This chapter complements [sec-documentation](#sec-documentation), which is about *writing* documentation. This one is about *reading* it.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain the four genres of documentation (tutorials, how-tos, references, explanations) and pick the right one for your question.
2.  Navigate the pandas and Python standard library docs to find a function’s signature, parameters, return value, and examples.
3.  Read a function signature, including type hints, default values, and `*args` / `**kwargs`.
4.  Read a docstring in Python with `help()`, `?`, and `??`.
5.  Extract a minimal working example from a reference page.
6.  Recognize when a blog post or tutorial is misleading and fall back to the official docs.
7.  Read release notes / changelogs to diagnose “it worked last year” problems.

## Running theme: start from the docs, not from the search results

For any question about a library function, the official docs should be your first stop, not your last. Blog posts are for discovery; docs are for correctness.

## 4.1 1. The four genres of documentation

Not all documentation is for the same kind of question. The [Diátaxis framework](https://diataxis.fr/) (worth a bookmark) divides docs into four genres:

| Genre | Purpose | When you want it |
|----|----|----|
| **Tutorials** | learning-oriented | “I am new; show me the basics hands-on.” |
| **How-to guides** | task-oriented | “I know roughly what I want; tell me the steps.” |
| **Reference** | information-oriented | “I know what function I want; tell me the exact arguments.” |
| **Explanations** | understanding-oriented | “Why does this work the way it does?” |

Most novices reach for tutorials first and stop there. The real superpower is knowing when to switch. If you want `pd.merge` to treat nulls as matching, reading a tutorial on merges will waste your time — jump to the reference page for `pandas.DataFrame.merge` and find the parameter. If you want to know whether pandas can ever drop columns silently, an explanation-oriented essay will teach you more than ten tutorials.

The official docs of major libraries usually include all four genres. pandas has a “Getting Started” (tutorials), “User Guide” (explanations), “Cookbook” (how-tos), and “API Reference.” Python itself has a tutorial, a library reference, a language reference, and a “HOWTOs” section. Learn where each lives for the libraries you use most.

## 4.2 2. Reading a function signature

Every library reference page starts with a signature. Read it slowly — it tells you most of what you need.

From the pandas docs, here is the signature of `pandas.read_csv` (abridged):

    pandas.read_csv(
        filepath_or_buffer,
        *,
        sep=',',
        header='infer',
        names=None,
        index_col=None,
        usecols=None,
        dtype=None,
        parse_dates=None,
        na_values=None,
        encoding=None,
        ...
    )

Things to notice:

- **Positional vs keyword-only.** Everything after the `*,` is keyword-only — you must pass it as `sep=";"`, not as a positional. This is common in modern Python APIs.
- **Default values.** `sep=','` tells you that if you don’t pass `sep`, it will be a comma. The default is part of the contract.
- **Sentinel defaults.** `header='infer'` is not the same as `header=None` (no header) or `header=0` (first row is header). Read the parameter description.
- **`None` is not “nothing.”** It usually means “use the library’s default behavior,” which might be “no filter” or “infer from data” depending on the parameter.

Each parameter has a description below the signature. Read the ones you use; skim the rest until you need them.

## 4.3 3. Reading a return value

Every reference page tells you what the function returns — its type and shape. For a pandas DataFrame method, the return is usually another DataFrame (or Series, or scalar). The important question is always: **is this operation in-place, or does it return a new object?**

``` python
df.sort_values("date")        # returns a new DataFrame; df is unchanged
df.sort_values("date", inplace=True)   # modifies df directly, returns None
```

Many pandas operations historically had an `inplace` parameter; the modern convention is to avoid it and use the return value. If your code sorts a DataFrame and then operates on the original unsorted one, you probably forgot to assign: `df = df.sort_values("date")`.

## 4.4 4. Reading docstrings from Python itself

You do not have to open a browser to read documentation. Every function, method, and class has a docstring you can read inline.

In the REPL or a script:

``` python
help(pd.read_csv)
```

In Jupyter or IPython, append a `?`:

``` python
pd.read_csv?
```

To see the *source* of the function, append `??`:

``` python
pd.read_csv??
```

Use `dir(obj)` to list all the attributes and methods on an object — a good way to discover what you can do with a DataFrame if you don’t remember:

``` python
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3]})
[m for m in dir(df) if not m.startswith("_")][:20]
# ['a', 'abs', 'add', 'add_prefix', 'add_suffix', 'agg', 'aggregate', 'align',
#  'all', 'any', 'apply', 'applymap', 'asfreq', 'asof', 'assign', 'astype', ...]
```

For built-in functions and methods, `help` is fast and always available, even on an airplane.

## 4.5 5. Reading a docstring: the canonical shape

Most Python docstrings follow a structured format with the same sections:

``` python
def resample(self, rule, ...):
    """Resample time-series data.

    Convenience method for frequency conversion and resampling of time
    series. The object must have a datetime-like index (DatetimeIndex,
    PeriodIndex, or TimedeltaIndex).

    Parameters
    ----------
    rule : DateOffset, Timedelta or str
        The offset string or object representing target conversion.

    Returns
    -------
    pandas.api.typing.Resampler
        An object that can be used to perform resampling operations.

    See Also
    --------
    groupby : Group by mapping, function, label, or list of labels.

    Examples
    --------
    Start by creating a series with 9 one minute timestamps.

    >>> index = pd.date_range('1/1/2000', periods=9, freq='min')
    >>> series = pd.Series(range(9), index=index)
    >>> series.resample('3min').sum()
    ...
    """
```

The sections you will read most often:

- **Summary line.** One sentence, at the top. Read it first; often it answers your question.
- **Parameters.** Each parameter named, typed, and described. Find the one you care about.
- **Returns.** What you get back.
- **Examples.** A working mini-tutorial you can copy. These are almost always the fastest way to understand a function.

If you only have time to read two sections, read the summary line and the examples.

## 4.6 6. Extracting a minimal example from the docs

The examples in a reference page are designed to be self-contained. They usually import everything they need, create any sample data inline, and run top to bottom. Your workflow for a new function is:

1.  Find the example closest to what you want.
2.  Copy it into a notebook cell or a throwaway script.
3.  Run it. Confirm it works unchanged.
4.  Modify it one variable at a time toward your real use case.

This workflow beats “try to guess the right incantation” every time.

## 4.7 7. Release notes and changelogs

Sometimes the docs on the site match a newer version than the one installed in your environment. The library has a release note page (sometimes called “What’s New” or “Changelog”) that lists the behavior changes in each release. Whenever you hit:

- “This worked last year and doesn’t now”
- “The tutorial uses an argument my version doesn’t have”
- “A deprecation warning I do not understand”

… the changelog is the right place to look. For pandas it is [pandas.pydata.org/docs/whatsnew](https://pandas.pydata.org/docs/whatsnew). For Python it is [docs.python.org/3/whatsnew](https://docs.python.org/3/whatsnew).

Check your installed version first:

``` python
import pandas as pd
print(pd.__version__)
```

Then go to the “What’s new in X.Y” page for that version and scan for the function you are using.

## 4.8 8. When a blog post is wrong

Blog posts are wonderful for discovery — “I didn’t know I could do that” — and dangerous for reference. Two warning signs that a blog is leading you astray:

1.  **No date, or a date older than two years.** APIs change. An answer that was right in 2018 may be wrong today.
2.  **The code doesn’t match the function signature in the docs.** Always sanity-check a blog’s code against `help(func)` or the official reference page for your version.

A useful workflow: discover an approach from a blog or Stack Overflow, then open the docs for every function in the snippet and verify the signature matches your installed version. If the blog post uses `pd.read_csv(..., skipfooter=1, engine='python')` and your docs say `skipfooter` is supported, you are fine. If the docs say otherwise, trust the docs.

## 4.9 9. Worked examples

### Example 1: “what does `how='outer'` do in `pd.merge`?”

**Wrong approach:** Google “pandas merge outer example,” read four blog posts, get confused by inconsistent examples.

**Right approach:** Open `help(pd.merge)` or the pandas docs for `pandas.DataFrame.merge`. Find the `how` parameter. Read:

> how : {‘left’, ‘right’, ‘outer’, ‘inner’, ‘cross’}, default ‘inner’
>
> Type of merge to be performed.
>
> - left: use only keys from left frame, similar to a SQL left outer join;
> - right: use only keys from right frame, similar to a SQL right outer join;
> - outer: use union of keys from both frames, similar to a SQL full outer join;
> - inner: use intersection of keys from both frames, similar to a SQL inner join.

Thirty seconds, definitive answer.

### Example 2: “why is my `.apply` so slow?”

**Wrong approach:** find a tutorial on speeding up pandas, try several unrelated tricks.

**Right approach:** go to the pandas User Guide → “Enhancing performance.” That’s an **explanation** page, and it directly answers “why is .apply slow and what should I do.” It will recommend vectorized operations, `.map`, `numba`, or `pyarrow` depending on your case.

### Example 3: “what arguments does `requests.get` actually take?”

From within a Jupyter cell:

``` python
import requests
requests.get?
```

You get a docstring listing every keyword argument (`params`, `headers`, `timeout`, `auth`, `cookies`, `allow_redirects`, `verify`, `stream`, `cert`) with descriptions — no browser required.

### Example 4: reading the Python language reference

If you find yourself wondering “does Python’s `in` operator work on a dict?”, the fastest answer is the **Python Language Reference** (distinct from the tutorial). The reference for `in` lives under “Expressions → Comparisons → Membership test operations” and tells you that `in` on a dict checks the *keys*, not the values.

The language reference is dense — it is for people who want precise answers to precise questions. You will not read it cover to cover, but you will increasingly rely on it as you get comfortable.

## 4.10 10. Templates

**A “read the docs before asking for help” pre-flight checklist:**

1.  Can I find the function in the official reference?
2.  Did I read the summary line?
3.  Did I read the description of the parameter I am using?
4.  Did I read the Returns section?
5.  Did I copy the official Example and run it?
6.  Did I check which version I have installed vs. the version the docs describe?

If yes to all five, then it is time to ask a question (see [sec-asking-questions](#sec-asking-questions)).

## 4.11 11. Exercises

1.  Using `help()` in a Python REPL, read the docstring for `sorted`. What does the `key` parameter do? What does `reverse=True` do?
2.  In a Jupyter notebook, type `pd.read_csv?` and scroll through every parameter. Pick three you have never used and read their descriptions.
3.  Open the pandas “API reference” and navigate to `pandas.DataFrame.merge`. Find the `indicator` parameter. Write one sentence explaining what it does.
4.  Find a stale blog post (older than three years) that uses a pandas function you know. Read the code and find one thing it does that is now discouraged or deprecated. Cross-check against the current docs.
5.  Check your installed pandas version with `pd.__version__`. Open the “What’s new in X.Y” page for that version. List two behaviors that changed in that release.
6.  For a library you use often but have not read the docs of (e.g., `matplotlib`, `scikit-learn`), find the entry page for the four Diátaxis genres: tutorial, how-to, reference, explanation. Bookmark each.
7.  The next time you hit a confusing error message, before searching online, open the docs for the function that raised the error. Read the Parameters and Examples sections. Time how long it took to find the answer.

## 4.12 12. One-page checklist

- **Docs first, blog posts second.** Official documentation is almost always faster and more reliable.
- Know the four genres: tutorials (learn), how-tos (do), references (look up), explanations (understand).
- Use `help()`, `?`, and `??` in Python to read docstrings inline.
- Read function signatures carefully: defaults, keyword-only arguments, and return types matter.
- Copy the reference-page example first, then modify toward your use case.
- Always check library version against the docs version: `pd.__version__`.
- Check the “What’s new” / changelog for release-to-release behavior changes.
- Docs are reference, not novels — dip in and out, don’t try to read top to bottom.
- Bookmark the four main entry points of your favorite libraries for future speed.
