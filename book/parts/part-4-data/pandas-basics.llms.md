# 22  pandas Basics

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks), [sec-data-file-formats](#sec-data-file-formats), [sec-tabular-data](#sec-tabular-data).
>
> **See also:** [sec-jupyter](#sec-jupyter), [sec-sql-basics](#sec-sql-basics), [sec-tracebacks](#sec-tracebacks).

## Purpose

[`pandas`](https://pandas.pydata.org/docs/) is the library that turns Python into a practical data-analysis tool. If you are taking a data science course and someone hands you a CSV, `pandas` is the thing you use to load it, poke at it, clean it, reshape it, and summarize it. It is usable from the first day, which is both its biggest strength and the reason it is easy to misuse.

This chapter is an orientation for students who have literally never used `pandas` — or who have copied notebook cells from an instructor but never sat down to understand the pieces. The goal is not to teach every method (there are thousands, and the official reference in [sec-reading-docs](#sec-reading-docs) is where you look them up). The goal is to give you the vocabulary and the mental model: what a Series and a DataFrame actually are, how indexing and selection work, how the common operations compose, and how to avoid the classic novice traps.

If you know SQL, several sections will feel like translation. That is a feature — once you see pandas as “SQL against an in-memory table,” a lot of it clicks. See [sec-sql-basics](#sec-sql-basics) for the SQL side.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what a Series and a DataFrame are, and how the index relates to them.
2.  Create a DataFrame from a dict, a list of dicts, or a file.
3.  Select rows and columns using `[]`, `.loc`, `.iloc`, and boolean masks — and know when to use each.
4.  Use `.head`, `.tail`, `.info`, `.describe`, `.shape`, and `.dtypes` to inspect a new dataset in under a minute.
5.  Apply the core data operations: filter, sort, add a column, aggregate, group-by, and join (merge).
6.  Recognize and avoid the three classic pandas gotchas: chained assignment, `SettingWithCopyWarning`, and forgetting that most operations return a copy.
7.  Know when to vectorize vs. when to write a Python loop (almost always vectorize).

## Running theme: pandas rewards vectorized thinking, and punishes loops

Almost every pandas operation is a set-wise verb: “filter these rows,” “add this column to all rows,” “group by this and take the mean.” When you find yourself writing `for row in df.itertuples()`, stop and think about the vectorized equivalent. Your code will be shorter, faster, and easier to read.

## 22.1 The two data structures

Everything in pandas is built on two data structures.

![](graphics/PLACEHOLDER-dataframe-render.png)

Figure 22.1: ALT: Jupyter cell output showing a rendered pandas DataFrame. The rendering includes the row index on the left, bold column headers along the top, and several rows of data, illustrating the tabular structure a DataFrame provides.

### Series: a labeled 1-D array

A **Series** is like a Python list, except every element has a label (the index). Think of it as a single column in a spreadsheet.

``` python
import pandas as pd

prices = pd.Series(
    [9.99, 14.50, 7.25, 22.00],
    index=["apple", "bread", "milk", "cheese"],
    name="price",
)
print(prices)
# apple      9.99
# bread     14.50
# milk       7.25
# cheese    22.00
# Name: price, dtype: float64
```

You access values by label: `prices["bread"]` returns `14.50`. You also get vectorized operations for free: `prices * 1.1` returns a new Series with every price marked up 10%, without a loop.

### DataFrame: a labeled 2-D table

A **DataFrame** is a dict of Series that share an index. Every column is a Series; every row is identified by the shared index.

``` python
df = pd.DataFrame({
    "price":    [9.99, 14.50, 7.25, 22.00],
    "quantity": [3,    1,     2,    5],
    "in_stock": [True, True,  False, True],
}, index=["apple", "bread", "milk", "cheese"])

print(df)
#         price  quantity  in_stock
# apple    9.99         3      True
# bread   14.50         1      True
# milk     7.25         2     False
# cheese  22.00         5      True
```

The `index` is *not* a column — it’s the row labels, and it is carried through most operations. You can always reset it to a default integer index with `df.reset_index()`, and promote a column to the index with `df.set_index("column_name")`.

## 22.2 Creating a DataFrame

Four common ways, in rough order of frequency:

**From a file** (the most common):

``` python
df = pd.read_csv("sales.csv")
df = pd.read_parquet("sales.parquet")
df = pd.read_excel("report.xlsx", sheet_name="Q4")
```

See [sec-data-file-formats](#sec-data-file-formats) for the quirks.

**From a dict of columns:**

``` python
df = pd.DataFrame({
    "name": ["Alice", "Bob", "Carol"],
    "age":  [30, 25, 35],
})
```

**From a list of dicts (one per row):**

``` python
df = pd.DataFrame([
    {"name": "Alice", "age": 30},
    {"name": "Bob",   "age": 25},
    {"name": "Carol", "age": 35},
])
```

This is what you usually get from a JSON API response (see [sec-http-apis](#sec-http-apis)).

**From a list of lists, plus column names:**

``` python
df = pd.DataFrame(
    [["Alice", 30], ["Bob", 25]],
    columns=["name", "age"],
)
```

## 22.3 Inspecting a new DataFrame

The first thing you should do with any new DataFrame is run these six commands, in a cell by themselves:

``` python
df.shape        # (rows, columns) — is it the size you expected?
df.columns      # column names
df.dtypes       # inferred types per column — any surprises?
df.head()       # first 5 rows
df.tail()       # last 5 rows
df.info()       # summary: counts, dtypes, memory usage
df.describe()   # summary statistics for numeric columns
```

This takes ten seconds and catches 90% of “why is my analysis wrong?” bugs. See [sec-tabular-data](#sec-tabular-data) for why validation is so important.

## 22.4 Selecting columns and rows

### Columns

Select a single column by name. The result is a Series.

``` python
df["price"]             # Series of prices
df.price                # same (attribute access — works only for simple names)
```

Select multiple columns with a list. The result is a DataFrame.

``` python
df[["price", "quantity"]]
```

**Gotcha:** `df["price", "quantity"]` (no inner list) raises `KeyError`. The single brackets need a list for multiple columns.

### Rows: `.loc` vs `.iloc`

`.loc` selects by **label** (the index). `.iloc` selects by **integer position** (0-based).

``` python
df.loc["bread"]          # row labeled "bread"
df.iloc[1]               # second row, regardless of label
```

Both can take a range:

``` python
df.loc["apple":"milk"]   # inclusive of both endpoints
df.iloc[0:3]             # Python slice, excludes index 3
```

Both can take a list:

``` python
df.loc[["apple", "cheese"]]
df.iloc[[0, 3]]
```

Both accept a second argument for columns:

``` python
df.loc["apple", "price"]              # single cell, by label
df.loc["apple":"milk", "price"]       # a Series
df.loc[:, ["price", "quantity"]]      # all rows, two columns
df.iloc[0, 1]                         # single cell, by position
```

Rule of thumb: **use `.loc` almost always**, because your index is usually meaningful and labels survive sorting and filtering. Use `.iloc` when you genuinely need the first/last N rows or you are working with an unlabeled integer index.

### Boolean masks

The most powerful selection is a boolean mask: a Series of `True`/`False` that filters rows.

``` python
df[df["price"] > 10]                     # rows where price > 10
df[(df["price"] > 10) & (df["in_stock"])] # conjunction — note the parentheses
df[df["name"].isin(["Alice", "Bob"])]    # membership
df[df["note"].str.contains("refund", na=False)]  # regex-enabled string match
```

Three things to remember about boolean masks:

1.  **Use `&` and `|`, not `and` / `or`.** The Python keywords operate on scalars, not arrays.
2.  **Parenthesize every sub-condition.** `df[df["x"] > 1 & df["y"] < 2]` misbehaves because of operator precedence.
3.  **Use `na=False`** on `.str.contains` to make NaNs behave like `False`.

## 22.5 Adding, modifying, and dropping columns

``` python
df["revenue"] = df["price"] * df["quantity"]        # new column from arithmetic
df["price"] = df["price"] * 1.1                     # overwrite a column
df["discount_tier"] = pd.cut(df["price"], bins=[0, 10, 20, 100])   # derived categorical
df = df.drop(columns=["discount_tier"])             # drop a column
df = df.rename(columns={"price": "unit_price"})     # rename
```

`assign` returns a new DataFrame with added columns — useful in chained expressions:

``` python
(df
  .assign(revenue=lambda d: d["price"] * d["quantity"])
  .assign(profit=lambda d: d["revenue"] - d["cost"])
)
```

## 22.6 The classic novice traps

### Chained assignment and `SettingWithCopyWarning`

This is the most confusing warning in pandas:

``` python
df[df["price"] > 10]["in_stock"] = False
# SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame.
```

The problem is that `df[df["price"] > 10]` returns a *temporary* slice, and you are modifying the temporary, not the original. Sometimes it works, sometimes it silently does nothing. Do not rely on it.

**Fix:** use `.loc` in one step.

``` python
df.loc[df["price"] > 10, "in_stock"] = False
```

This says “for rows matching this condition, set this column,” in a single expression pandas understands.

### Forgetting that most methods return a copy

``` python
df.sort_values("price")    # returns a sorted copy; df is unchanged
```

If you want to keep the result, assign it:

``` python
df = df.sort_values("price")
```

Most methods (`sort_values`, `drop`, `rename`, `dropna`, `reset_index`, …) work this way. The `inplace=True` parameter exists on many of them but is discouraged in modern pandas — assigning back is clearer.

### Mutating while iterating

``` python
for i, row in df.iterrows():
    df.loc[i, "adjusted"] = row["price"] * 1.1    # slow and error-prone
```

This works but defeats the point of pandas. Vectorize instead:

``` python
df["adjusted"] = df["price"] * 1.1
```

A good rule: if you wrote `iterrows` or `itertuples`, your first instinct should be “how can I do this as a vectorized operation or a `.apply`?” There is almost always a way.

## 22.7 Aggregation and group-by

Group-by is pandas’s single most important verb. It splits the data into groups, applies a function to each group, and combines the results.

``` python
df.groupby("category")["revenue"].sum()
df.groupby("category")["revenue"].agg(["sum", "mean", "count"])
df.groupby(["category", "region"])["revenue"].mean().unstack()
```

A worked example: find the top three products by revenue within each category.

``` python
(df
  .groupby("category", group_keys=False)
  .apply(lambda g: g.nlargest(3, "revenue"))
)
```

If you find yourself writing complex group-by logic, that is the moment to read the pandas User Guide chapter on `groupby` — see [sec-reading-docs](#sec-reading-docs).

## 22.8 Merging (joining) DataFrames

`merge` is the pandas equivalent of a SQL JOIN (see [sec-sql-basics](#sec-sql-basics)).

``` python
merged = orders.merge(customers, on="customer_id", how="left")
```

Parameters to care about:

- `on`: the column name(s) to join on. Or use `left_on=` / `right_on=` if the column names differ.
- `how`: `"inner"` (default, keeps only matching rows), `"left"`, `"right"`, `"outer"` (union).
- **`validate`**: specify the expected cardinality (`"one_to_one"`, `"one_to_many"`, `"many_to_one"`, `"many_to_many"`). Use this *every time*. It catches bad merges immediately. See [sec-tabular-data](#sec-tabular-data).

## 22.9 Sorting

``` python
df.sort_values("price")                        # ascending by one column
df.sort_values("price", ascending=False)       # descending
df.sort_values(["category", "price"])          # multi-column
df.sort_index()                                # sort by index (labels)
```

> **NOTE:**
>
> - [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) — conceptual explanations of indexing, merging, and reshaping.
> - [pandas API reference](https://pandas.pydata.org/docs/reference/index.html) — every method and parameter, with examples.
> - [pandas Cheat Sheet (PDF)](https://pandas.pydata.org/Pandas_Cheat_Sheet.pdf) — a printable one-pager covering the most common operations.

## 22.10 Worked examples

### A one-minute exploration of a new dataset

``` python
import pandas as pd

df = pd.read_csv("data/raw/iris.csv")

# Inspect
print(df.shape)
print(df.dtypes)
print(df.head())
print(df.describe())

# A first question: average petal length per species?
print(df.groupby("species")["petal_length"].mean())
```

### Filter, sort, derive, aggregate

``` python
# Load a cleaned dataset
df = pd.read_parquet("data/processed/sales.parquet")

top_customers = (
    df
    .query("date >= '2024-01-01'")               # filter
    .assign(revenue=lambda d: d["price"] * d["quantity"])   # derive
    .groupby("customer_id")["revenue"]           # group
    .sum()                                       # aggregate
    .sort_values(ascending=False)                # sort
    .head(10)                                    # top 10
)
print(top_customers)
```

The method-chain pattern (pandas calls this “fluent interface”) makes long transformations readable top-to-bottom.

### A join with validation

``` python
orders = pd.read_parquet("data/processed/orders.parquet")
customers = pd.read_parquet("data/processed/customers.parquet")

merged = orders.merge(
    customers,
    on="customer_id",
    how="left",
    validate="many_to_one",     # one customer per order; crashes on bad data
)
assert len(merged) == len(orders), "Merge changed row count"
```

The `validate` + assert pattern prevents the silent-duplication class of bugs.

## 22.11 Templates

**A “first look” block for any new DataFrame:**

``` python
print("shape:", df.shape)
print("columns:", df.columns.tolist())
print("dtypes:")
print(df.dtypes)
print("\nhead:")
print(df.head())
print("\nnulls per column:")
print(df.isna().sum())
print("\nnumeric summary:")
print(df.describe())
```

**A clean filter-derive-aggregate pipeline:**

``` python
result = (
    df
    .query("date >= '2024-01-01' and region == 'west'")
    .assign(profit=lambda d: d["revenue"] - d["cost"])
    .groupby("product_id")["profit"]
    .sum()
    .sort_values(ascending=False)
    .head(20)
)
```

## 22.12 Exercises

1.  Load a CSV from an open-data source into a DataFrame. Run the six inspection commands from section 3. Write one sentence for each about what you learned.
2.  From the same DataFrame, select a single column as a Series and a list of two columns as a DataFrame. Confirm the types with `type()`.
3.  Write three different ways to select the top 10 rows: by `.head(10)`, by `.iloc[:10]`, and by sort-then-head. Compare performance on a big DataFrame with `%timeit`.
4.  Use `.loc` with a boolean mask to update a subset of rows in-place. Confirm no `SettingWithCopyWarning` appears.
5.  Write a group-by that answers a real question about your data (“average price per category,” “max revenue per customer”). Add a second aggregation to the same call.
6.  Perform a `merge` and then `validate="one_to_one"`. Intentionally break it by duplicating a row in the right-hand DataFrame and confirm pandas raises.
7.  Take a notebook cell you wrote as a for-loop over `iterrows` and rewrite it as a vectorized operation. Time both. Write down the speedup.

## 22.13 One-page checklist

- Every new DataFrame: run shape / dtypes / head / describe / isna before anything else.
- Use `.loc` for label-based selection, `.iloc` for integer-based, and boolean masks for filters.
- Boolean masks use `&` and `|`, not `and` / `or`. Parenthesize every sub-condition.
- Most methods return a copy; assign the result (`df = df.sort_values(...)`).
- Never chain assignment (`df[mask]["col"] = value`). Use `df.loc[mask, "col"] = value`.
- Vectorize first; reach for `iterrows` only when you truly cannot.
- Merge with `validate="..."` every time.
- For reshaping and validation, read [sec-tabular-data](#sec-tabular-data) first.
- For anything beyond this chapter, the pandas User Guide and API Reference are your friends — see [sec-reading-docs](#sec-reading-docs).
