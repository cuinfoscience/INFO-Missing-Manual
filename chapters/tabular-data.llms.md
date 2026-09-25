# 21  Tabular Data

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-data-file-formats](#sec-data-file-formats).
>
> **See also:** [sec-pandas-basics](#sec-pandas-basics), [sec-sql-basics](#sec-sql-basics), [sec-tracebacks](#sec-tracebacks).

## Purpose

![What’s in the box meme: What’s in the file?](../graphics/memes/tabular-data.png)

Here’s a story that happens every semester. You download a dataset, load it into pandas, run `.describe()`, and everything looks reasonable, so you start making charts. A week later, a number in your results looks odd. You dig in and discover that a merge quietly doubled half the rows, or that the date column was never really dates, or that the “total” row at the bottom of the spreadsheet got averaged in with everything else. Now every chart is wrong, and you have to redo the week.

If that has happened to you, you’re in good company: it happens to experienced analysts too. The data wasn’t hiding anything. A file that opens without an error *feels* trustworthy, and that feeling is exactly how most data bugs get in. The old line for this is [garbage in, garbage out](https://en.wikipedia.org/wiki/Garbage_in,_garbage_out), and the fix is a handful of habits that take minutes and catch these problems while they’re still cheap.

This chapter is about those habits: what shape a table should be in, how to clean one without damaging it, how to check it before you trust it, and the specific snags that eat the most student hours. It doesn’t teach pandas syntax from scratch (that’s [sec-pandas-basics](#sec-pandas-basics)) or SQL ([sec-sql-basics](#sec-sql-basics)). The ideas here hold whichever tool you use, so they’ll still be useful the next time you pick up a new one.

## Why read this chapter

- You made a chart from a CSV, then found out later that half the rows were duplicated, and you’d rather never lose a week that way again.
- You summed a price column and got `'12.50$89.25'` instead of a number, and you can’t see why pandas thinks prices are text.
- You merged two tables and ended up with more rows than you started with, and every total in your report quietly grew.
- Your data has one column per month or per survey question, and every analysis turns into a loop over column names.
- You fixed a file by hand in Excel, and now you can’t say what you changed or redo it when the next version arrives.
- Your instructor keeps saying “tidy data,” “validate,” and “primary key,” and you’d like to know what they mean in practice.
- You want a few lines of checks you can paste into any project, so bad data stops you at the start instead of at the end.

## Running theme: data you haven’t checked is data you can’t trust

Every dataset looks fine at first glance, and almost every real one has problems. A few lines of checks at the top of your analysis cost minutes; a week of wrong conclusions costs a week.

## 21.1 Wide and tidy: the shape of a table

Before cleaning anything, it helps to know what shape you’re aiming for, because the same information can be laid out in two very different ways.

Most tables you receive from a teacher, a government website, or a spreadsheet look like this. Each row is a thing (here, a student), and each column is a measurement of that thing:

| student | math | reading | science |
|---------|------|---------|---------|
| Alice   | 92   | 88      | 95      |
| Bob     | 78   | 84      | 80      |

That’s **wide** data, and it’s built for human eyes: you can take in a whole student at a glance. Here is the same information in **tidy** (or long) form, where each row is a single observation, one score for one student in one subject:

| student | subject | score |
|---------|---------|-------|
| Alice   | math    | 92    |
| Alice   | reading | 88    |
| Alice   | science | 95    |
| Bob     | math    | 78    |
| Bob     | reading | 84    |
| Bob     | science | 80    |

The tidy version looks worse at first: it’s longer, it repeats names, and it’s harder to read. It pays off the moment you start asking questions. The average score in each subject is one line, `df.groupby("subject")["score"].mean()`. A chart comparing subjects is one line too, with [`sns.boxplot(data=df, x="subject", y="score")`](https://seaborn.pydata.org/generated/seaborn.boxplot.html). And when history scores arrive next month, they’re just more rows: no new columns, no code to change. With the wide table, every one of those questions means writing a loop over column names, and every new subject means editing the code again.

The idea has a name, [tidy data](https://en.wikipedia.org/wiki/Tidy_data), from a 2014 paper by the statistician Hadley Wickham, and it has shaped how nearly every modern data library expects its input. It comes down to three rules. **Each variable gets its own column:** `subject` and `score` are two different things, so they’re two columns, not one column per subject. **Each observation gets its own row:** one score for one student in one subject. And **each kind of thing gets its own table:** if you also have information about the classes (teacher, room, time), that goes in a second table, joined to the first by a key, rather than repeated on every row of the scores.

Wide still has its place. It’s the right shape for a table a person will read in a report, and some statistical models want one column per feature. The rule of thumb is to *clean and analyze in tidy form, and turn it wide only at the end, for display*. pandas moves between the two with [`melt`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.melt.html) (wide to tidy) and [`pivot`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.pivot.html) (tidy to wide):

``` python
# wide -> tidy
tidy = wide.melt(
    id_vars="student",
    value_vars=["math", "reading", "science"],
    var_name="subject",
    value_name="score",
)

# tidy -> wide
wide_again = tidy.pivot(index="student", columns="subject", values="score")
```

If you remember one thing from this section, remember those two functions. A surprising number of “how do I…?” questions about tables turn into one line once the data is tidy.

## 21.2 Keep the raw file untouched

The first habit sounds almost too simple: **never change the file you were given.** Put it in a folder called `data/raw/`, and from then on treat it like a museum exhibit. You can look, but you don’t touch.

It’s tempting to open the CSV in Excel, fix the obvious typo in a header, delete the junk rows at the bottom, and save. Everyone does it once. The trouble comes a month later, when someone asks what you changed, or a new version of the data arrives and you have to make the same fixes again from memory. So instead, write every change down as code: a script reads the raw file, cleans it, and saves the result somewhere else. The cleaned file is then a *product* of the raw file and the script, and you can delete it and remake it at any time.

``` text
project/
├── data/
│   ├── raw/              # exactly as you received it; never edited
│   │   └── sales.csv
│   └── processed/        # made by the script; safe to delete and rebuild
│       └── sales.parquet
├── src/
│   └── clean_sales.py    # the only thing that turns raw into processed
└── notebooks/
    └── analysis.ipynb    # reads only from processed/
```

Laid out this way, “what did we do to this data?” always has an answer: read `clean_sales.py`. Every number in your report can be traced back through the script to the original file, which is what people mean by [data lineage](https://en.wikipedia.org/wiki/Data_lineage). And you never again have to wonder which of `sales_final.csv` and `sales_final_v2_REAL.csv` is the good one. [sec-project-management](#sec-project-management) covers how this fits into a whole project.

## 21.3 Cleaning, one decision at a time

[Data cleaning](https://en.wikipedia.org/wiki/Data_cleansing) sounds like a chore you get through before the real work starts. It’s better to think of it as a series of decisions, each of which changes what your results will say. The order matters too, because each step makes the next one easier and safer. Most real datasets go through roughly the same sequence.

**Start by loading the raw file as it is,** and immediately **tidy up the column names.** Headers like `" Total Revenue ($)"`, with a stray space and punctuation, make every line of code clumsier. Convert them once to lowercase words joined by underscores (sometimes called [snake case](https://en.wikipedia.org/wiki/Snake_case)), and you’ll never type the dollar sign again.

**Next, fix the types.** pandas guesses each column’s [type](https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes) when it reads a file, and it guesses wrong more often than you’d expect: one stray `"N/A"` makes a whole column of prices into text, and dates usually arrive as text too. Fix types right away, because almost everything later (sums, comparisons, sorting, date math) quietly does the wrong thing on the wrong type.

**Then decide what missing values mean.** A blank cell can mean “the answer is zero,” “nobody asked,” “the sensor failed,” or “this row is from before we collected that.” pandas’ [guide to missing data](https://pandas.pydata.org/docs/user_guide/missing_data.html) explains the mechanics; the decision is yours. Drop the row, fill in a value, or keep the blank, but choose deliberately, and write down why. Don’t let some function’s default behavior make the choice for you.

**Then look for duplicates,** both rows that repeat exactly and rows that repeat the value that should be unique, such as an order number. A duplicated order number almost always means something went wrong upstream: an export ran twice, or a join matched more rows than it should have.

**Then deal with impossible values:** ages of −5, heights of 1,000 cm, dates in 2099. Your knowledge of the subject is what tells you what’s impossible, and whether to drop the value, fix it, or flag it for a closer look.

**Only now reshape and derive.** Melt the table to tidy form if it arrived wide, and add calculated columns such as ratios, categories, and flags. They come last because they’re only as trustworthy as the columns they’re built from.

**Finally, save the result to a new file,** ideally Parquet, which keeps your carefully fixed types (see [sec-data-file-formats](#sec-data-file-formats)). Never save it on top of the raw file.

Put all of this in one script that runs from top to bottom without you touching anything. It feels slower than clicking around the first time. By the third time the data changes, it’s much faster.

## 21.4 Check your data before you trust it

Once you have a cleaned table, don’t take it on faith. A handful of checks, run every time, catches the large majority of problems while they’re still easy to fix. Python has a built-in tool that’s perfect for this, the [`assert` statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement): it does nothing when a condition is true, and stops everything, with your message, when it’s false.

``` python
assert df.shape[0] > 0, "Empty DataFrame"
assert list(df.columns) == EXPECTED_COLUMNS, f"Columns changed: {df.columns.tolist()}"
assert df["order_id"].is_unique, "Duplicate order IDs"
assert df["date"].notna().all(), "Missing dates"
assert (df["quantity"] > 0).all(), "Non-positive quantities"
assert pd.api.types.is_numeric_dtype(df["price"]), f"Price is {df['price'].dtype}, expected numeric"
```

Each line checks one thing you believe about the data, and says so in plain words. Start with the easy questions. Does the table have rows at all, and the columns you expected? Did each column come out as the right type, or is the price column secretly text? Then the subtler ones. Does the column that should identify each row, the table’s [primary key](https://en.wikipedia.org/wiki/Primary_key), actually have no repeats? And do the values make sense, with no ages of 212 and no percentages of 140?

It can feel silly to check things you “know” are true. But you don’t know until you’ve checked, and the day a new export arrives with a renamed column, you’ll be glad the check stopped you at line 2 instead of letting you find out at the end. This kind of [data validation](https://en.wikipedia.org/wiki/Data_validation) scales up, too: libraries like pandera and Great Expectations do the same job for bigger projects (see Further reading), and [sec-project-management](#sec-project-management) shows how to check data against a written data dictionary.

## 21.5 Seven snags you’ll meet (and how to get past them)

Some problems come up so often with real data that they’re worth recognizing on sight. None of them means you did something wrong; they’re simply what data from the real world looks like.

### 1. Column names with spaces and punctuation

You’ll know this one when `df["Total Revenue ($)"]` works but typing it gets old fast, and `df.total_revenue` doesn’t exist. Rename every column once, right after loading, with pandas’ [string methods](https://pandas.pydata.org/docs/user_guide/text.html):

``` python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\W+", "_", regex=True)
    .str.strip("_")
)
```

### 2. Numbers that are secretly text

The giveaway is `df["price"].sum()` gluing strings together (`'12.50$89.25'`) instead of adding them. Somewhere in the column there’s a value pandas couldn’t read as a number, such as a `"N/A"`, a `$`, or a footnote marker, and one is enough to turn the whole column into text (`str` in pandas 3, `object` in pandas 2). [`pd.to_numeric`](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html) with `errors="coerce"` converts what it can and turns the rest into missing values, which lets you find the culprits:

``` python
df["price_num"] = pd.to_numeric(df["price"], errors="coerce")
bad = df[df["price_num"].isna() & df["price"].notna()]
print(f"Unconvertible prices: {len(bad)}")
print(bad[["price"]].drop_duplicates().head())
```

Look at what it prints before deciding what to do. Often the fix belongs at read time, with `na_values=` (see [sec-data-file-formats](#sec-data-file-formats)), or in one line that strips the `$`.

### 3. Dates that are secretly text

The error message is the clue here: `AttributeError: Can only use .dt accessor with datetimelike values`. The column looks like dates, but pandas is holding strings. Convert it with [`pd.to_datetime`](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html):

``` python
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y", errors="coerce")
```

Always give the `format=` when you know it. Is `03/04/2026` March 4 or April 3? It depends on [where the file came from](https://en.wikipedia.org/wiki/Date_format_by_country), and guessing wrong silently shuffles your months. If you control how dates are written, use the unambiguous [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) form, `2026-03-04`. pandas’ [time series guide](https://pandas.pydata.org/docs/user_guide/timeseries.html) has much more on working with dates once they’re real dates.

### 4. Codes that stand for “missing”

Averages that make no sense (an average temperature of −380) often mean the column uses a stand-in for “no data,” such as `-999`, `"unknown"`, or `0`. That’s a [sentinel value](https://en.wikipedia.org/wiki/Sentinel_value): useful to whoever made the file, poison to your statistics until you convert it to a real missing value. Catch them as you read the file:

``` python
df = pd.read_csv("data.csv", na_values=["-999", "unknown", "", "-"])
```

or replace them afterwards with `df["temp"] = df["temp"].replace({-999: pd.NA})`. The file’s documentation, if it has any, usually lists its codes; checking it takes a minute and can save the analysis.

### 5. A merge that quietly multiplies rows

You join two tables and suddenly have more rows than you started with, and every total is too big. This happens when the key you joined on isn’t unique on the side where you assumed it was: two customer records share an ID, so every order for that customer matches twice. The fix is to tell pandas what kind of relationship you expect (its [cardinality](https://en.wikipedia.org/wiki/Cardinality_(data_modeling))) and let it check for you, using the `validate=` option of [`merge`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html):

``` python
merged = orders.merge(customers, on="customer_id", validate="many_to_one")
```

That line reads: many orders can share a customer, but each customer appears once. If that’s not true, pandas stops with an error instead of quietly inflating your numbers. The [merging guide](https://pandas.pydata.org/docs/user_guide/merging.html#merging-validation) lists the options: `"one_to_one"`, `"one_to_many"`, `"many_to_one"`, and `"many_to_many"`. Saying which one you mean, every time, is one of the cheapest habits in this book.

### 6. Rows that disappear along the way

Your table started with 5,000 rows, and somewhere along the chain of steps it became 4,812, and you’re not sure where. Some operations drop rows without saying so: [`groupby`](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) leaves out rows whose group key is missing unless you pass `dropna=False`, an inner merge drops rows that have no match, and a filter drops whatever doesn’t pass. Each might be exactly what you want. The problem is not knowing. While you’re cleaning, print the shape before and after each step:

``` python
print(f"before: {df.shape}")
df = df.dropna(subset=["customer_id"])
print(f"after:  {df.shape}")
```

If a count changes and you can’t say why, stop and find out before you go on.

### 7. A column with a bit of everything

Mostly numbers, but also `"N/A"`, `"n/a"`, `"unknown"`, and a stray `"12 (est.)"`: the column reads as text and everything you do with it is slow and fragile. Use the `pd.to_numeric(..., errors="coerce")` approach from snag 2, then look at the values that became missing before you decide what to do with them. Resist the urge to `.dropna()` them away. The row that doesn’t fit is often the one that tells you something about how the data was made.

## 21.6 Stakes and politics

Suppose your survey dataset has 400 respondents, and 60 of them skipped the income question. One `.dropna()` later, you have a tidy table of 340, and every result you report describes those 340 people. But the people who skip an income question are rarely a random slice of respondents: they may be wary of how the answer will be used, or have an income that’s hard to put in one number, and they tend to differ from the people who answer in ways that matter. Dropping them didn’t clean the data; it changed who the data is about.

Every step in this chapter carries that kind of decision. What counts as [missing](https://en.wikipedia.org/wiki/Missing_data): a declined answer, a question that didn’t apply, and a software failure are three different things that look identical as `NaN`. What counts as an [outlier](https://en.wikipedia.org/wiki/Outlier): in a dataset of incomes, the extreme row might be a billionaire who skews the mean, or a family in deep poverty who is exactly who a policy analysis is supposed to be about. What counts as a duplicate: the same person can appear twice for good reasons, such as two visits, two purchases, or two enrollments, and collapsing them quietly rewrites what happened. Cleaning looks technical, but each of these choices decides whose experience stays in the analysis.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: every cleaning step is a claim that the rows you removed do not matter. Write down which rows you removed and *why* — that note is part of your analysis, not separate from it.

## 21.7 Worked examples

### Turning wide survey data into tidy

A course survey arrives in wide form, one column per question, with answers from 1 (strongly disagree) to 5 (strongly agree):

| respondent | q1_agree | q2_agree | q3_agree |
|------------|----------|----------|----------|
| r001       | 5        | 3        | 4        |
| r002       | 2        | 4        | 3        |

You want to know how many people agreed (answered 4 or 5) with each question. With the wide table, you end up looping over column names:

``` python
for q in ["q1_agree", "q2_agree", "q3_agree"]:
    print(q, (df[q] >= 4).sum())
```

That works until the survey gains a fourth question and you have to remember to edit the list. Melt it to tidy form first, and the question becomes a group-by that doesn’t care how many questions there are:

``` python
tidy = df.melt(id_vars="respondent", var_name="question", value_name="score")
tidy.groupby("question")["score"].apply(lambda s: (s >= 4).sum())
```

When `q4_agree` shows up next term, this code handles it without a single change.

### A full cleaning pipeline

Here is everything from “Cleaning, one decision at a time” and “Check your data before you trust it” in one function, for an export of online orders. Read it top to bottom and notice that each step is one of the decisions described above, in the same order, and that the checks at the end stop the script if any of them went wrong:

``` python
import pandas as pd

EXPECTED_COLUMNS = ["order_id", "date", "customer_id", "sku", "quantity", "revenue"]

def load_and_clean(path: str) -> pd.DataFrame:
    # Load, treating the file's usual "no data" codes as missing
    df = pd.read_csv(path, na_values=["", "-", "N/A", "NA", "n/a"])

    # Tidy column names
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\W+", "_", regex=True)

    # Fix types
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # An order without an ID or a date can't be used
    df = df.dropna(subset=["order_id", "date"])

    # One row per order
    df = df.drop_duplicates(subset="order_id")

    # Remove impossible values (a missing revenue fails this test too: see snag 6)
    df = df[(df["quantity"] > 0) & (df["revenue"] >= 0)]

    # Check before handing it on
    assert df.shape[0] > 0, "Empty after cleaning"
    assert list(df.columns) == EXPECTED_COLUMNS, f"Column drift: {df.columns.tolist()}"
    assert df["order_id"].is_unique, "Duplicate order_ids leaked through"
    assert df["date"].notna().all(), "Null dates leaked through"

    return df

cleaned = load_and_clean("data/raw/sales.csv")
cleaned.to_parquet("data/processed/sales.parquet")
```

Rerun it whenever the raw file changes, and it either produces a clean table or tells you exactly which belief about the data stopped being true.

### Catching a bad merge

You have a table of orders and a table of customers, and you want the customer’s city on every order. You’re sure each customer appears once in the customer table, so say so:

``` python
orders = pd.read_parquet("data/processed/orders.parquet")
customers = pd.read_parquet("data/processed/customers.parquet")

merged = orders.merge(customers, on="customer_id", validate="many_to_one")
```

If someone’s customer record was entered twice, this raises a `MergeError` right here, naming the problem, instead of letting that customer’s orders count twice in every revenue figure you report. One extra argument, and a whole class of bug is gone.

## 21.8 Templates

**A “load, clean, check” skeleton to start every cleaning script from:**

``` python
import pandas as pd

EXPECTED_COLUMNS = [...]
KEY_COLUMN = "..."

def load_raw(path: str) -> pd.DataFrame:
    return pd.read_csv(
        path,
        na_values=["", "-", "N/A", "NA", "n/a", "null"],
        parse_dates=[...],
    )

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"\W+", "_", regex=True)
        .str.strip("_")
    )
    return df

def validate(df: pd.DataFrame) -> None:
    assert df.shape[0] > 0
    assert list(df.columns) == EXPECTED_COLUMNS
    assert df[KEY_COLUMN].is_unique
    # Add checks for this dataset below
```

## 21.9 Exercises

1.  Take a wide table from your own work (a survey export, a grade book) and turn it tidy with one `melt`. Check the result by counting rows: it should have (rows × measured columns) of them.
2.  Go the other way: `pivot` a tidy table back to wide and confirm you get the original values.
3.  Pick a real CSV and write a check block of about ten lines: shape, columns, types, key uniqueness, and one range check. Run it. Did anything fail? Were you surprised?
4.  Break your check block on purpose: add a row with text in a number column, one with a missing key, one with an impossible value. Does each failure give you a message you’d understand at 2 a.m.?
5.  Move the cleaning code from one of your notebooks into a script, `clean_something.py`, that writes to `data/processed/`. Change the notebook to read only the processed file.
6.  Write a merge you *expect* to be one-to-one and add `validate="one_to_one"`. Then duplicate a row in the right-hand table and watch pandas catch it.
7.  Find a dataset that uses a code like `-999` for missing values. Load it with and without `na_values=` and compare `.describe()`. How much did the averages move?

## 21.10 One-page checklist

- Keep the raw file untouched in `data/raw/`; every change lives in a script.
- Tidy the column names as soon as you load.
- Fix types right away: numbers as numbers, dates as dates.
- Decide what missing values mean, and write the decision down.
- Check for duplicates, especially in the column that should be unique.
- Clean and analyze in tidy form; go wide only for display.
- Give `format=` when you parse dates you care about.
- Catch “no data” codes with `na_values=` when you read the file.
- Pass `validate=` to every merge.
- Run a block of `assert` checks before every analysis.
- If a row count changes and you can’t say why, stop and find out.

> **NOTE:**
>
> - Hadley Wickham, [*Tidy Data*](https://vita.had.co.nz/papers/tidy-data.pdf) — the canonical paper on long/wide formats; under 25 pages and shapes how the rest of the field thinks about table shape.
> - pandas, [User Guide: Reshaping](https://pandas.pydata.org/docs/user_guide/reshaping.html) — the official guide to `melt`, `pivot`, `stack`, and `unstack`.
> - Catherine D’Ignazio and Lauren F. Klein, [*Data Feminism*](https://data-feminism.mitpress.mit.edu/) — the standard book-length treatment of who gets counted, who counts, and how the technical decisions of data work encode power; pairs directly with the “Stakes and politics” framing above.
> - Great Expectations, [Documentation](https://docs.greatexpectations.io/) — a popular library for writing the validation checks this chapter advocates; treats data quality assertions as first-class artifacts.
> - Pandera, [Documentation](https://pandera.readthedocs.io/) — a lighter-weight schema and validation library for pandas DataFrames; useful when Great Expectations feels too heavy.
> - The Turing Way, [Reproducible Research: Open Data](https://book.the-turing-way.org/reproducible-research/open/open-data) — community-maintained chapter on documenting datasets, including data dictionaries and provenance notes.
> - Timnit Gebru et al., [*Datasheets for Datasets*](https://arxiv.org/abs/1803.09010) — proposes a documentation standard answering “who collected this, why, and what is missing” for any dataset; lightweight to apply to your own work.
