# 21  Tabular Data

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-data-file-formats](#sec-data-file-formats).
>
> **See also:** [sec-pandas-basics](#sec-pandas-basics), [sec-sql-basics](#sec-sql-basics), [sec-tracebacks](#sec-tracebacks).

## Purpose

Before you can analyze a dataset, you have to shape it, clean it, and convince yourself it is what you think it is. Novices skip this step constantly — load a CSV, call `.describe()`, and start plotting. The results look fine. A week later, a subtle bug reveals that half the rows were duplicated by a bad merge, or a date column was parsed as strings, or a “total” column is the sum of all the other columns plus itself. The analysis is wrong and the rewrites are painful.

This chapter is a field guide to the practices that catch those bugs early. It covers what shape your data should be in (wide vs. tidy), how to clean it without corrupting it, how to validate it with lightweight checks, and the specific friction points that burn the most student hours. It deliberately does not teach pandas syntax — that is [sec-pandas-basics](#sec-pandas-basics) — or SQL — that is [sec-sql-basics](#sec-sql-basics). Instead it teaches the *principles* that apply regardless of tool, so that when you pick up a new library you already know what good looks like.

Read this chapter before the first time you work with a dataset you did not generate yourself. It is short, but it will save you hours of “why is my answer wrong?” later.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Define wide vs. tidy (long) data and explain when each is appropriate.
2.  Recognize the three rules of tidy data (one variable per column, one observation per row, one type of observational unit per table).
3.  List the standard moves of a data-cleaning pipeline and their order.
4.  Write lightweight validation checks — shape, dtypes, null counts, key uniqueness, value ranges — that catch the most common bugs.
5.  Identify the seven most common sources of friction when loading a new dataset and apply the standard fix for each.
6.  Explain why cleaning should be reproducible, not a one-off manual process in a notebook.
7.  Distinguish between raw data (never modify) and cleaned data (derived, regenerable).

## Running theme: data you have not validated is data you cannot trust

Every dataset looks reasonable at first glance. Every dataset has problems. A ten-line validation block at the top of your analysis is cheaper than a week of wrong conclusions.

## 21.1 Wide vs. tidy data

The single most useful concept for working with tabular data is the distinction between **wide** and **tidy** (also called “long”) formats. The idea was popularized by Hadley Wickham’s [Tidy Data paper](https://vita.had.co.nz/papers/tidy-data.pdf) and has since shaped every major data analysis library.

### Wide

In a **wide** dataset, each row is an entity and each column is a measurement *of* that entity. Classrooms, spreadsheets, and government reports usually give you wide data because it is easy for humans to read.

| student | math | reading | science |
|---------|------|---------|---------|
| Alice   | 92   | 88      | 95      |
| Bob     | 78   | 84      | 80      |

### Tidy (long)

In a **tidy** dataset, each row is a single observation — one measurement of one attribute of one entity — and there are only as many columns as there are *kinds* of thing (variable name, value, entity identifiers).

| student | subject | score |
|---------|---------|-------|
| Alice   | math    | 92    |
| Alice   | reading | 88    |
| Alice   | science | 95    |
| Bob     | math    | 78    |
| Bob     | reading | 84    |
| Bob     | science | 80    |

Same information, more rows, fewer columns. So why tidy? Because once your data is tidy:

- Every statistic you want is a group-by: `df.groupby("subject")["score"].mean()`.
- Plots are a single call: `sns.boxplot(data=df, x="subject", y="score")`.
- New subjects can be added without adding new columns.
- Filtering is trivial: `df[df["subject"] == "math"]`.

Wide data resists all of these. You end up writing repetitive code, adding columns every time a new measurement type appears, and dealing with an ever-widening table.

### The three rules of tidy data

Tidy data obeys three rules:

1.  **Each variable forms a column.** A variable is a measured property: height, price, date, category.
2.  **Each observation forms a row.** An observation is a single unit of measurement: one customer on one day, one test score for one student.
3.  **Each type of observational unit forms a separate table.** If your data has students *and* classes, they belong in two tables (with a join key), not one flattened table.

### When to use wide

Tidy is the right shape for analysis and reshaping. Wide is the right shape for:

- **Human reading.** Nobody wants to scroll through 60 rows when a 3x20 table would fit on the page.
- **Certain modeling tasks** where each “feature” is a column.
- **Output / reporting.** Pivot tidy data back to wide at the last step, for presentation.

The rule of thumb: **clean and analyze in tidy; pivot to wide only for display**.

### Converting between the two

In pandas, the functions are `melt` (wide → long) and `pivot` / `pivot_table` (long → wide):

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

Learn these two functions early. They turn a “help me reshape my data” question into a one-liner.

## 21.2 The standard cleaning pipeline

Most real datasets need roughly the same sequence of moves before they are usable. Do them in order; skipping steps or reordering them causes subtle bugs.

1.  **Load the raw file without modifying it.** Never overwrite the source file. The raw data is the ground truth you reproduce from. See [sec-data-file-formats](#sec-data-file-formats).
2.  **Normalize column names.** Strip whitespace, lowercase, replace spaces and punctuation with underscores. A reproducible helper is better than hand-fixing. `df.columns = df.columns.str.strip().str.lower().str.replace(r"\W+", "_", regex=True)`
3.  **Fix dtypes.** Make sure numeric columns are numeric, dates are dates, categoricals are categorical. Do this right after loading, before anything else, because downstream operations silently misbehave on wrong dtypes.
4.  **Handle missing values explicitly.** Decide whether to drop rows, drop columns, fill with a sentinel, or leave as NaN. Never let the default “drop NaN” behavior of a function be your policy — make the decision yourself.
5.  **Deduplicate.** Check for and drop exact duplicate rows. Check for duplicates on your key column(s) — these almost always indicate a bad upstream join or a data-entry error.
6.  **Filter out-of-range values.** Heights of 0 or 1000, ages of -5, dates in 2099. Use domain knowledge to decide what to drop or flag.
7.  **Reshape to tidy.** If the input was wide, melt it now, once.
8.  **Derive new columns.** Calculated fields (ratios, categories, flags) come last, after the base columns are trustworthy.
9.  **Save the cleaned output to a separate file.** Use Parquet (see [sec-data-file-formats](#sec-data-file-formats)). Never save the cleaned data on top of the raw file.

Put every step in a script or notebook that runs end-to-end, from raw to cleaned, in one pass. If someone (including future you) ever needs to know “what did we do to this data?”, the answer should be “read this script.”

## 21.3 Raw vs. cleaned data

Adopt this rule early: **raw data is immutable.** You never modify it. You never save over it. You keep it in a folder called `data/raw/` and treat it like a read-only museum exhibit.

Cleaned data is a *derivative* of raw data, produced by a script. It lives in `data/processed/` or `data/cleaned/`. Anyone can delete it and regenerate it by rerunning the script.

    project/
    ├── data/
    │   ├── raw/              # never modify
    │   │   └── sales.csv
    │   ├── interim/          # optional: intermediate results
    │   └── processed/        # cleaned, validated, analysis-ready
    │       └── sales.parquet
    ├── src/
    │   └── clean_sales.py    # the script that turns raw into processed
    └── notebooks/
        └── analysis.ipynb    # reads only from processed/

This separation does three things: it makes cleaning reproducible, it makes the lineage of any number in your report traceable, and it prevents the dreaded “I don’t remember which version of this file is the good one” situation. See [sec-project-management](#sec-project-management) for how this fits into overall project structure.

## 21.4 Validation: lightweight checks that catch the most bugs

Validation does not have to be fancy. A ten-line block at the top of your analysis catches 90% of the problems you will encounter. Paste this pattern into every notebook or cleaning script:

``` python
assert df.shape[0] > 0, "Empty DataFrame"
assert list(df.columns) == EXPECTED_COLUMNS, f"Columns changed: {df.columns.tolist()}"
assert df["order_id"].is_unique, "Duplicate order IDs"
assert df["date"].notna().all(), "Missing dates"
assert (df["quantity"] > 0).all(), "Non-positive quantities"
assert df["price"].dtype.kind in "if", f"Price is {df['price'].dtype}, expected numeric"
```

This is cheap, self-documenting, and fails loudly at the exact line that is wrong. Libraries like `pandera` and `great_expectations` offer more sophisticated schema validation, but for student work the plain `assert` pattern is plenty.

### What to validate

A useful mental model: validate five axes of every dataset you load.

1.  **Shape.** Number of rows and columns, both lower and upper bounds.
2.  **Columns.** The expected column names, in the expected order.
3.  **Dtypes.** Numeric columns are numeric; date columns are dates.
4.  **Keys and uniqueness.** The column that should uniquely identify rows actually does. If you have a join key, it has the expected cardinality.
5.  **Values.** Ranges, categories, missingness. Ages in 0-120, percentages in 0-1 (or 0-100, pick one), dates within your study window.

Run these checks at the top of every analysis, even when you “know” the data is fine. You do not know until you have checked.

## 21.5 The seven most common friction points

Here are the specific problems you will hit most often with real data, and the standard fix for each.

### 1. Column names with spaces, caps, and punctuation

**Symptom:** `df["Total Revenue"]` works but `df.Total Revenue` doesn’t, and the mixed-case names make every line uglier than it needs to be.

**Fix:** normalize column names immediately after loading.

``` python
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(r"\W+", "_", regex=True)
    .str.strip("_")
)
```

### 2. Numeric columns read as strings

**Symptom:** `df["price"].sum()` concatenates strings instead of adding numbers.

**Fix:** one bad value somewhere (a `"N/A"` or a `"$"` or a stray footnote) is making pandas treat the whole column as `object`. Use `pd.to_numeric(..., errors="coerce")` to convert and flag the culprits:

``` python
df["price_num"] = pd.to_numeric(df["price"], errors="coerce")
bad = df[df["price_num"].isna() & df["price"].notna()]
print(f"Unconvertible prices: {len(bad)}")
print(bad[["price"]].drop_duplicates().head())
```

Then fix the source: use `na_values=` at read time (see [sec-data-file-formats](#sec-data-file-formats)) or strip the junk explicitly.

### 3. Dates read as strings

**Symptom:** `.dt.year` fails with `AttributeError: Can only use .dt accessor with datetimelike values`.

**Fix:** parse the column explicitly.

``` python
df["date"] = pd.to_datetime(df["date"], errors="coerce")
```

If the format is ambiguous (US `MM/DD/YYYY` vs. EU `DD/MM/YYYY`), pass `format=` explicitly — do not rely on inference for dates you care about.

### 4. Missing-value sentinels

**Symptom:** a numeric column contains `-999`, `"unknown"`, or an empty string and your statistics are nonsense.

**Fix:** catch them at read time:

``` python
df = pd.read_csv("data.csv", na_values=["-999", "unknown", "", "-"])
```

Or clean them after loading:

``` python
df["temp"] = df["temp"].replace({-999: pd.NA})
```

### 5. Silent duplication from a bad merge

**Symptom:** after a join, your row count doubled and none of your aggregates match.

**Fix:** merge with `validate=`:

``` python
merged = df_a.merge(df_b, on="customer_id", validate="one_to_one")
```

Pandas will raise immediately if the join is not the cardinality you claimed. Use `"one_to_one"`, `"one_to_many"`, `"many_to_one"`, or `"many_to_many"` as appropriate. Make the choice explicit every time.

### 6. Implicit dropping of NaN rows

**Symptom:** your row count keeps shrinking as you chain operations, because functions like `.groupby`, `.dropna`, and `.merge` silently drop rows with missing keys.

**Fix:** check the shape before and after every operation during cleaning:

``` python
print(f"before: {df.shape}")
df = df.dropna(subset=["customer_id"])
print(f"after:  {df.shape}")
```

For groupby, pass `dropna=False` if you want NaN groups included.

### 7. Mixed types in a “numeric” column

**Symptom:** a column has integers, floats, and a few strings (“N/A”, “n/a”, “unknown”). Reads as `object`. Operations are slow and error-prone.

**Fix:** `pd.to_numeric(..., errors="coerce")` as in problem 2, then decide what to do with the NaNs. Do not silently `.dropna()` — that is the row you should be investigating.

> **NOTE:**
>
> - Hadley Wickham, [*Tidy Data*](https://vita.had.co.nz/papers/tidy-data.pdf) — the canonical paper on long/wide formats.
> - [pandas User Guide: Reshaping](https://pandas.pydata.org/docs/user_guide/reshaping.html) — the official guide to `melt`, `pivot`, `stack`, and `unstack`.
> - [Great Expectations](https://docs.greatexpectations.io/) — a popular library for writing the validation checks this chapter advocates.

## 21.6 Worked examples

### Turning wide survey data into tidy

You have a survey export in wide format:

| respondent | q1_agree | q2_agree | q3_agree |
|------------|----------|----------|----------|
| r001       | 5        | 3        | 4        |
| r002       | 2        | 4        | 3        |

You want to count how many “agree” (4 or 5) responses each question got.

Wide: ugly, repetitive.

``` python
for q in ["q1_agree", "q2_agree", "q3_agree"]:
    print(q, (df[q] >= 4).sum())
```

Tidy: one-liner.

``` python
tidy = df.melt(id_vars="respondent", var_name="question", value_name="score")
tidy.groupby("question")["score"].apply(lambda s: (s >= 4).sum())
```

Adding a `q4_agree` later requires zero code changes in the tidy version.

### A full cleaning pipeline

``` python
import pandas as pd

EXPECTED_COLUMNS = ["order_id", "date", "customer_id", "sku", "quantity", "revenue"]

def load_and_clean(path: str) -> pd.DataFrame:
    # 1. Load raw, treating common missing sentinels
    df = pd.read_csv(path, na_values=["", "-", "N/A", "NA", "n/a"])

    # 2. Normalize column names
    df.columns = df.columns.str.strip().str.lower().str.replace(r"\W+", "_", regex=True)

    # 3. Fix dtypes
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")

    # 4. Drop rows missing a key
    df = df.dropna(subset=["order_id", "date"])

    # 5. Deduplicate
    df = df.drop_duplicates(subset="order_id")

    # 6. Filter out-of-range values
    df = df[(df["quantity"] > 0) & (df["revenue"] >= 0)]

    # 7. Validate
    assert df.shape[0] > 0, "Empty after cleaning"
    assert list(df.columns) == EXPECTED_COLUMNS, f"Column drift: {df.columns.tolist()}"
    assert df["order_id"].is_unique, "Duplicate order_ids leaked through"
    assert df["date"].notna().all(), "Null dates leaked through"

    return df

cleaned = load_and_clean("data/raw/sales.csv")
cleaned.to_parquet("data/processed/sales.parquet")
```

This is reproducible, self-documenting, and will crash loudly if the source changes shape. Every project you do should have something like it.

### Catching a bad merge

``` python
orders = pd.read_parquet("data/processed/orders.parquet")
customers = pd.read_parquet("data/processed/customers.parquet")

# Without validate: you might not notice a doubled row count
merged = orders.merge(customers, on="customer_id", validate="many_to_one")
# Raises MergeError if customer_id is NOT unique in `customers`.
```

Five extra characters (`validate="many_to_one"`) catches the bug that would otherwise silently double every revenue figure in your final report.

## 21.7 Templates

**A “load, clean, validate” skeleton to paste into every cleaning script:**

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
    # Add dataset-specific checks below
```

## 21.8 Exercises

1.  Take a wide dataset from your own work (a survey, a grade book, a classroom export) and write a one-line `melt` that converts it to tidy. Verify by counting rows.
2.  Write the reverse: take a tidy dataset and `pivot` it back to wide. Confirm the two are equivalent after reshaping.
3.  Pick a real CSV and write a 10-line validation block (shape, columns, dtypes, key uniqueness, one range check). Run it. Did anything fail?
4.  Intentionally break your validation block by adding a bad row (wrong dtype, missing key, out-of-range value). Confirm each type of failure produces a clear error.
5.  Take an analysis notebook of yours and move the cleaning logic into a separate script (`clean_foo.py`) that writes to `data/processed/foo.parquet`. Update the notebook to read only from the processed file.
6.  Write a `pandas` merge that you *expect* to be `one_to_one`, then add `validate="one_to_one"`. Now introduce a duplicate into the right-hand DataFrame and confirm pandas raises.
7.  Find a dataset with missing-value sentinels. Load it twice — once with default options, once with `na_values=`. Compare `.describe()`. How many of your statistics changed?

## 21.9 One-page checklist

- **Never modify raw data.** Keep it in `data/raw/`, read-only.
- **Cleaning is a script, not a notebook.** Reproducible and rerunnable, top to bottom.
- **Load, normalize, fix dtypes, handle nulls, deduplicate, filter, reshape, derive, save.** In that order.
- **Reshape to tidy for analysis; pivot to wide only for display.**
- **Validate five axes:** shape, columns, dtypes, keys/uniqueness, values.
- **Pass `validate=` on every merge.**
- **Catch missing-value sentinels at read time** with `na_values=`.
- **Parse dates explicitly.** Do not rely on inference for load-bearing columns.
- **Paste a `assert` validation block at the top of every analysis.**
- **If row counts change silently, stop and investigate.** It is almost always a bug.
