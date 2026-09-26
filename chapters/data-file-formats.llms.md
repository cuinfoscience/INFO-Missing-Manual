# 20  Data File Formats

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-filesystem](#sec-filesystem), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).
>
> **See also:** [sec-jupyter](#sec-jupyter), [sec-pkg-mgmt](#sec-pkg-mgmt), [sec-tracebacks](#sec-tracebacks).

## Purpose

![Noah Meme: CSV, JSON, Parquet, What is this?](../graphics/memes/data-file-formats.png)

Here’s a scene from every intro data course. You get a dataset and type the line every [pandas](https://pandas.pydata.org/docs/) tutorial promises will work: `pd.read_csv("data.csv")`. Sometimes it does. Other times you get a wall of red text about a “codec,” or a DataFrame with one enormous column, or, worst of all, a table that loads without complaint and is quietly wrong: prices stored as text, dates that are only strings, a `-999` dragging every average below zero.

None of that means you’re bad at this. pandas has to guess at the habits of whoever made the file (which character separates columns, which values mean “nothing here”), and when it guesses wrong, the fix is almost always one argument, once you know which one to reach for. This chapter is a field guide to the formats you’ll meet most: [CSV](../chapters/appendix-glossary.llms.md#term-csv) (and its cousin TSV), [JSON](../chapters/appendix-glossary.llms.md#term-json), Excel, Stata and SPSS files, and [Parquet](../chapters/appendix-glossary.llms.md#term-parquet), plus the text encodings underneath them and what to do when a file is too big to load. It doesn’t cover cleaning a table once it’s loaded (that’s [sec-tabular-data](#sec-tabular-data)), pandas itself ([sec-pandas-basics](#sec-pandas-basics)), fetching JSON from an API ([sec-http-apis](#sec-http-apis)), or JSON as a configuration format ([sec-common-formats](#sec-common-formats)).

## Why read this chapter

- Your CSV loaded as a single column with a name like `'name;price;city'`, and you can’t see what went wrong.
- `pd.read_csv` stopped with `UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9`, and you have no idea what a codec is.
- You averaged a temperature column and got −233 °C, because nothing told pandas that `-999` means “no reading.”
- Boston ZIP codes lost their leading zero, or 3 April turned into March 4, and nothing warned you either time.
- An API gave you nested JSON, and `pd.read_json` answered with `ValueError: Mixing dicts with non-Series may lead to ambiguous ordering`.
- Someone emailed you a spreadsheet with a title banner, merged cells, and five sheets, and you need one clean table out of it.
- The survey you need came from an archive as a `.dta` or `.sav` file, and you don’t have Stata or SPSS.
- Your notebook’s kernel keeps dying on a big file, and you want to know whether Parquet, DuckDB, or Polars would help.

## Running theme: never trust a file you just read

Look at the shape, the columns, the types, and the first and last rows in the cell right after every `read_*` call. Most data bugs are loading bugs in disguise, and they’re cheapest to catch the moment the file comes in.

## 20.1 CSV: the workhorse, and its quirks

A [CSV](https://en.wikipedia.org/wiki/Comma-separated_values) file is about as simple as a data format gets: plain text, one row per line, commas between the values. That’s why everything can write one, and why they cause so much trouble: there’s a short standard (RFC 4180, in Further reading), but nothing enforces it, so every program has its own ideas about separators, quoting, and encodings. pandas’ [guide to reading CSV files](https://pandas.pydata.org/docs/user_guide/io.html#io-read-csv-table) documents every option; this section covers the ones you’ll need.

### The simple case

``` python
import pandas as pd
df = pd.read_csv("sales.csv")
```

On a file you didn’t make, this often fails the first time, and that’s normal. Before reaching for arguments, look at the raw text in a text editor (see [sec-text-editors](#sec-text-editors)), not Excel, which reformats what it shows, or with `head -5 sales.csv` in a terminal (see [sec-terminal](#sec-terminal)). Thirty seconds tells you the separator, whether there’s a header, and whether junk sits above it.

### Delimiters other than comma

Here’s a classic surprise: the DataFrame has one column.

``` python
df = pd.read_csv("european.csv")
print(df.shape)
print(df.columns.tolist())
```

``` text
(2, 1)
['name;price;city']
```

The file uses semicolons, common where the comma is the [decimal separator](https://en.wikipedia.org/wiki/Decimal_separator) (three and a half euros is `3,50`). A `.csv` extension is only part of a name; it promises nothing about what’s inside. Tell pandas the separator, and the decimal mark while you’re at it:

``` python
df = pd.read_csv("european.csv", sep=";", decimal=",")
print(df)
```

``` text
               name  price    city
0      Café Lumière    3.5   Paris
1  Bäckerei Schmidt    2.1  Berlin
```

Without `decimal=","`, the prices would load as the text `'3,50'`. Tabs (`sep="\t"`) and pipes (`sep="|"`) are the other separators you’ll meet. pandas can also sniff the separator with `sep=None, engine="python"`, but that’s slower and occasionally wrong, so treat it as a last resort.

### Encoding: `UnicodeDecodeError`

Sooner or later you’ll see this:

``` text
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 18: invalid continuation byte
```

It looks terrifying and is usually easy. pandas assumes the bytes follow [UTF-8](https://en.wikipedia.org/wiki/UTF-8), the modern standard, and this file uses another rule, most often [Windows-1252](https://en.wikipedia.org/wiki/Windows-1252) (`cp1252` to Python), long used by Windows programs for Western European text. There, byte `0xe9` is `é`; in UTF-8 it can’t stand alone. Try `cp1252` first:

``` python
df = pd.read_csv("legacy.csv", encoding="cp1252")
```

You’ll also see advice to use `encoding="latin-1"`, which has a catch: it never raises an error, even on the wrong file. “Text encoding in general” below explains.

### Missing values: the many faces of “nothing”

Files say “no value here” in many ways: empty cells, `NA`, `NULL`, a dash, `unknown`, or codes like `-999` that only make sense if you’ve read the documentation. These stand-ins are called [sentinel values](https://en.wikipedia.org/wiki/Sentinel_value). pandas already reads a standard set as missing, including empty cells, `NA`, `N/A`, `n/a`, `NULL`, `null`, and `None` (the [`na_values` section](https://pandas.pydata.org/docs/user_guide/io.html#na-values) has the full list). Anything else comes in as text:

``` python
df = pd.read_csv("survey.csv")
print(df)
```

``` text
   id  age   income
0   1   34    52000
1   2    -  unknown
2   3  NaN    61000
3   4  NaN       --
4   5  NaN    48000
```

The file’s `n/a`, `NULL`, and empty cell became `NaN`, pandas’ marker for missing. The `-`, `unknown`, and `--` didn’t, so both columns are text, and the error shows up later, far from its cause: `df["income"].mean()` fails with `TypeError: Cannot perform reduction 'mean' with string dtype` (see [sec-tracebacks](#sec-tracebacks)). Add the file’s own codes to pandas’ defaults:

``` python
df = pd.read_csv("survey.csv", na_values=["-", "--", "unknown"])
```

Now both columns are numbers. Numeric codes like `-999` are sneakier, because they *are* numbers: nothing fails, and every average is wrong. Worked example 2 shows one.

### Dtypes: the “everything is a string” trap

Every column has one type, its [dtype](https://pandas.pydata.org/docs/user_guide/basics.html#basics-dtypes), and pandas picks it from the values. One cell it can’t read as a number (a footnote, a `$`, a note like `call for price`) and the whole column becomes text. You usually find out when a sum glues strings together instead of adding them. A column holding `12.50`, `$8`, and `9.25`:

``` python
df = pd.read_csv("revenue.csv")
df["revenue"].sum()
```

``` text
'12.50$89.25'
```

> **NOTE:**
>
> pandas 3.0 and later read a text column as `str`; pandas 2 and earlier read it as `object`. Tutorials and answers written for older versions say `object`, so check which version you have with `pd.__version__` (pandas’ [guide to the new string type](https://pandas.pydata.org/docs/user_guide/migration-3-strings.html) explains the change). To ask whether a column is numeric in either version, ask directly: `pd.api.types.is_numeric_dtype(df["revenue"])` returns `False` for the column above in both.

There are two ways out. If the bad values are missing-value codes, use `na_values=` at read time. Otherwise, convert after loading with [`pd.to_numeric`](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html):

``` python
# Option 1: handle missing values at read time, as above
df = pd.read_csv("revenue.csv", na_values=["-", ""])

# Option 2: coerce after loading
df["revenue"] = pd.to_numeric(df["revenue"], errors="coerce")
```

`errors="coerce"` turns what it can’t convert into `NaN`, so `df["revenue"].isna().sum()` counts the failures, and you can inspect those rows ([sec-tabular-data](#sec-tabular-data) shows how). Either way, run `df.dtypes` after every load: an expected number column that shows up as `str` (or `object` in pandas 2) has a non-number hiding in it.

Guessing goes wrong the other way, too. Codes made of digits, like [ZIP codes](https://en.wikipedia.org/wiki/ZIP_Code) and student IDs, look like numbers, so Boston’s `02134` loads as `2134`, and the zero is gone for good. If you’d never do arithmetic on it, read it as text:

``` python
df = pd.read_csv("addresses.csv", dtype={"zip": "str"})
```

### Dates

pandas leaves dates as text unless you ask, and the first sign is often `AttributeError: Can only use .dt accessor with datetimelike values`. Ask at read time:

``` python
df = pd.read_csv("sales.csv", parse_dates=["date"])
```

That’s reliable on unambiguous [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) dates like `2026-03-04`, the form to use when you write dates yourself. On `03/04/2026` (March 4 in the United States, 3 April in much of the world), pandas guesses month first and fails quietly. If every date could be month first, a British file’s 3 April becomes March 4. If some can’t (`13/04/2026`), the whole column stays text. Neither comes with a warning; `df.dtypes` catches the second, and only knowing the file’s origin catches the first. When you know the format, give it in Python’s [format codes](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes):

``` python
df = pd.read_csv(
    "sales.csv",
    parse_dates=["date"],
    date_format="%d/%m/%Y",
)
```

### Headers, index columns, and junk at the top

pandas assumes the first line is a header. If there isn’t one, a first row of `Alice,34` becomes the column names, and Alice vanishes from the data. Say so, and name the columns:

``` python
df = pd.read_csv("data.csv", header=None, names=["name", "age"])
```

If the first column should become the index (the row labels), use `index_col=0`. And a title or timestamp above the header produces an error that sounds unrelated: `ParserError: Error tokenizing data. C error: Expected 1 fields in line 4, saw 2`. Count the lines above the header and skip them:

``` python
df = pd.read_csv("export.csv", skiprows=3)       # skip 3 lines, then header
```

### Large files: don’t read what you don’t need

If a CSV is too big to load comfortably, don’t read all of it. Read only the columns you need (`usecols=`), read it in pieces (`chunksize=`), convert it to Parquet once, or let DuckDB or Polars answer the question without loading the whole file. “Data bigger than memory” below walks through each, with measurements.

## 20.2 TSV and other delimited formats

A [TSV](https://en.wikipedia.org/wiki/Tab-separated_values) file is a CSV with tabs instead of commas, which is a little friendlier: tabs almost never appear inside a value, so quoting rarely comes up. Read one with `pd.read_csv("data.tsv", sep="\t")`. Everything in the CSV section applies, including the one-giant-column symptom when a tab-separated file arrives named `.csv`.

## 20.3 JSON: when the structure is nested

[JSON](https://en.wikipedia.org/wiki/JSON) is how most web APIs send data (see [sec-http-apis](#sec-http-apis)). Unlike a CSV’s grid, a JSON record can hold other records and lists, like a user whose address has a city and a ZIP code, so most of working with JSON in pandas is deciding how to flatten it. Python’s built-in [`json` module](https://docs.python.org/3/library/json.html) reads any JSON file into dictionaries and lists, and pandas’ [JSON guide](https://pandas.pydata.org/docs/user_guide/io.html#io-json-reader) covers reading it straight into a DataFrame.

### Flat JSON

If the file is a list of records with no nesting, [`pd.read_json`](https://pandas.pydata.org/docs/reference/api/pandas.read_json.html) reads it directly:

``` python
df = pd.read_json("people.json")
```

JSON has no date type. `read_json` converts columns whose names look like dates (`date`, or names ending in `_at` or `_time`, among others) and leaves the rest, so `signup_date` stays text until you run `pd.to_datetime` on it.

### Nested JSON

Real API responses are rarely flat. A typical one wraps the records in an envelope:

``` json
{
  "data": [
    {"id": 1, "name": "Alice", "address": {"city": "Boulder", "zip": "80301"}},
    {"id": 2, "name": "Bob",   "address": {"city": "Denver",  "zip": "80202"}}
  ],
  "meta": {"page": 1, "total": 2}
}
```

Hand that to `pd.read_json` and you get `ValueError: Mixing dicts with non-Series may lead to ambiguous ordering`, pandas’ way of saying it can’t tell which part is the table. Load it as Python data, pick out the list you want, and flatten it with [`pd.json_normalize`](https://pandas.pydata.org/docs/reference/api/pandas.json_normalize.html):

``` python
import json
import pandas as pd

with open("users.json") as f:
    payload = json.load(f)

df = pd.json_normalize(payload["data"])
print(df)
```

``` text
   id   name address.city address.zip
0   1  Alice      Boulder       80301
1   2    Bob       Denver       80202
```

Each nested dictionary becomes columns with dot-separated names. (The ZIP codes stayed text because the JSON put them in quotes, a distinction CSV can’t make.)

### Newline-delimited JSON (NDJSON / JSONL)

Logs and big exports often use [JSON Lines](https://jsonlines.org/): one complete JSON object per line, with no surrounding list.

``` text
{"id": 1, "name": "Alice"}
{"id": 2, "name": "Bob"}
```

`json.load` rejects the file as a whole, but pandas reads it with one extra argument, and can read it in chunks too (see “Data bigger than memory”):

``` python
df = pd.read_json("events.jsonl", lines=True)
```

### When JSON won’t parse

JSON is strict, and two mistakes cause most failures. Strings need double quotes, so single quotes (the way Python prints a dictionary) fail with `JSONDecodeError: Expecting property name enclosed in double quotes`. And no comma may follow the last item. Python 3.13 and later say so plainly (`Illegal trailing comma before end of object`), but 3.12 and earlier give the *same* “expecting property name” message, sending people hunting for quotes that are fine. The line and column in the message point at the spot. pandas is vaguer (`ValueError: Expected object or value`), so try `json.load` for the better message.

## 20.4 Excel: the format you cannot escape

Sooner or later someone sends you a spreadsheet. An `.xlsx` file is a zip archive of XML ([Office Open XML](https://en.wikipedia.org/wiki/Office_Open_XML)) holding one or more *sheets*, with formulas, formatting, and merged cells. pandas reads it through [openpyxl](https://openpyxl.readthedocs.io/en/stable/) (old `.xls` files need xlrd), which doesn’t come with pandas. If you see `` ImportError: `Import openpyxl` failed. ``, install it into your environment (see [sec-pkg-mgmt](#sec-pkg-mgmt)):

``` bash
python -m pip install openpyxl
```

pandas’ [Excel guide](https://pandas.pydata.org/docs/user_guide/io.html#io-excel) has every option; these are the ones you’ll use.

### Basic usage

``` python
df = pd.read_excel("report.xlsx")              # reads the first sheet
```

### Multiple sheets

``` python
df = pd.read_excel("report.xlsx", sheet_name="Sales")           # one sheet by name
df = pd.read_excel("report.xlsx", sheet_name=0)                 # one sheet by index
sheets = pd.read_excel("report.xlsx", sheet_name=None)          # dict of all sheets
sheets = pd.read_excel("report.xlsx", sheet_name=["Sales","Q4"])# dict of some sheets
```

With `sheet_name=None` or a list, you get a dictionary mapping each sheet’s name to a DataFrame, not a DataFrame, so `sheets.head()` fails. Pick one with `sheets["Sales"]`, or loop over `sheets.items()`.

### Dealing with messy layouts

Spreadsheets are made for people to read, and it shows.

**Title rows above the header.** If your columns come out as `Unnamed: 0`, `Unnamed: 1`, and the report’s title, pandas took the title for the header. Skip the rows above the real one with `skiprows=` (worked example 4 skips four).

**Two header rows**, such as a year above each group of columns: `header=[0, 1]` makes each column name a pair, like `('2025', 'units')`.

**Merged cells.** A value merged down four rows is stored only in the top cell, so pandas gives `NaN` below it. Fill it down with `df["region"] = df["region"].ffill()`.

**Formulas.** pandas reads the value Excel last calculated, not the formula, so a file written by a program that never calculated its formulas (a script using openpyxl, say) gives `NaN` in every formula cell. Opening and saving it in Excel stores the results. Worked example 4 shows these problems in one file.

### Save back to Excel

``` python
df.to_excel("cleaned.xlsx", index=False)
```

Pass `index=False` (to `to_csv`, too), or whoever reads the file finds a mystery first column called `Unnamed: 0`. And a sheet holds at most 1,048,576 rows ([Microsoft’s limits](https://support.microsoft.com/en-us/excel/excel-specifications-and-limits)); the old `.xls` format holds 65,536, a limit that once mattered a great deal (see “Stakes and politics”).

## 20.5 Stata and SPSS files: data that carries its codebook

Download survey data from an archive like [ICPSR](https://en.wikipedia.org/wiki/Inter-university_Consortium_for_Political_and_Social_Research) and you’ll often be offered a Stata file (`.dta`) or an SPSS file (`.sav`), the formats of two statistics programs long popular in the social sciences. You don’t need either program to read them. What makes these files worth knowing is that they carry part of their own codebook: alongside the numbers, they store **value labels**, the words each code stands for (1 means “Not at all,” 3 means “A great deal”).

pandas reads Stata files with [`pd.read_stata`](https://pandas.pydata.org/docs/user_guide/io.html#io-stata-reader), and by default (`convert_categoricals=True`) it turns each labeled column into a category that shows the labels instead of the codes. Here’s a made-up four-person survey with a labeled `trust` question:

``` python
df = pd.read_stata("survey.dta")
print(df)
print(df["trust"].cat.categories.tolist())
```

``` text
   id         trust  age
0   1    Not at all   34
1   2  A great deal   51
2   3      Somewhat   28
3   4  A great deal   45
['Not at all', 'Somewhat', 'A great deal']
```

The categories keep the order of their codes, so sorting, grouping, and cross-tabulating put “Not at all” first instead of alphabetizing. When you need the numbers, say to average a scale, read the codes instead: `pd.read_stata("survey.dta", convert_categoricals=False)` gives `1, 3, 2, 3` for the same column. The question wording, which Stata calls a *variable label*, is in the file too:

``` python
with pd.io.stata.StataReader("survey.dta") as reader:
    print(reader.variable_labels())
```

``` text
{'id': '', 'trust': 'Trust in local news', 'age': ''}
```

[`pd.read_spss`](https://pandas.pydata.org/docs/user_guide/io.html#io-spss-reader) works the same way, value labels and all, but it needs a package that doesn’t come with pandas, [pyreadstat](https://ofajardo.github.io/pyreadstat_documentation/_build/html/index.html). Without it, you get `` ImportError: `Import pyreadstat` failed. ``; install it with `python -m pip install pyreadstat`. Expect one difference: SPSS stores every number as a floating-point number, so the same survey’s IDs and ages come back as `1.0` and `34.0`. (SAS files have `pd.read_sas`, which brings back the codes without their labels.) If you convert any of these files to CSV to share, the labels become plain text and the codes are gone, so write both into your data dictionary (see “When not to use Parquet” below).

## 20.6 Parquet: the format for real data work

[Parquet](https://en.wikipedia.org/wiki/Apache_Parquet) is a binary format built for analysis. It stores data column by column ([columnar storage](https://en.wikipedia.org/wiki/Column-oriented_DBMS)), compresses each column, and records each column’s type. You can’t read it in a text editor, and don’t need to: you’ll mostly write it yourself, as a faster, more faithful copy of data you’ve loaded and cleaned. pandas reads and writes it with the pyarrow library (`python -m pip install pyarrow` if it’s missing).

### Reading and writing

``` python
df = pd.read_parquet("sales.parquet")
df.to_parquet("sales.parquet")
```

### Why Parquet instead of CSV

**It keeps your types.** A CSV stores everything as text, so every read repeats all the guessing above, and dates you converted come back as strings. Parquet stores the types: dates stay dates, and text ZIP codes stay text.

**It’s smaller and faster.** In the test in “Data bigger than memory,” a 184 MB CSV became a 24 MB Parquet file. On a similar file, reading the Parquet took about a second; reading the CSV took about nine.

**You can read only the columns you need.** `pd.read_parquet("f.parquet", columns=["date", "revenue"])` reads just those columns from disk; a CSV has to be read through to find them. pandas’ [Parquet guide](https://pandas.pydata.org/docs/user_guide/io.html#io-parquet) has the other options.

### When not to use Parquet

Stick with CSV when someone needs to open the file in a spreadsheet or text editor (Parquet shows up as gibberish), when a collaborator’s tools can’t read Parquet, or when the dataset is a few hundred rows. A pattern that works well: keep the raw file as you received it, convert it to Parquet once at the start of your pipeline, and do every later read from the Parquet file ([sec-tabular-data](#sec-tabular-data) explains the folder layout).

``` python
raw = pd.read_csv("data/raw/sales.csv", parse_dates=["date"], na_values=["-"])
raw.to_parquet("data/processed/sales.parquet")

# From now on, every notebook starts with:
df = pd.read_parquet("data/processed/sales.parquet")
```

Sharing and archiving are the other times to reach for CSV. Parquet is a fine working format, but when you hand data to someone else, post it with a paper, or deposit it in an archive, the safest choice is still a UTF-8 CSV with a data dictionary beside it. Anyone can open plain text with whatever program they have, now and very likely decades from now; a Parquet file needs a library that understands it. Archives agree: the UK Data Service lists CSV among its [recommended formats](https://ukdataservice.ac.uk/learning-hub/research-data-management/format-your-data/recommended-formats/) for tabular data. What a CSV loses is what makes Parquet pleasant, the types and what each column means, and the data dictionary puts those back in a form a person can read ([sec-project-management](#sec-project-management) shows how to write one). So keep Parquet inside your pipeline, and export a CSV and its dictionary for whoever comes after you.

## 20.7 Data bigger than memory

Sooner or later a file is too big for the tools above. In a notebook, the cell runs for a while and then Jupyter says *“The kernel appears to have died. It will restart automatically.”* In a script, you get a `MemoryError`, or your whole computer slows to a crawl as it starts using the disk as memory. The file isn’t broken. It just doesn’t fit, and the fix is to change how you read it, not to buy a new laptop. pandas’ guide to [scaling to large datasets](https://pandas.pydata.org/docs/user_guide/scale.html) covers the same ground.

### How much memory a file needs

A DataFrame usually takes more memory than the file it came from, and how much more depends on your pandas version. To find out, we loaded a 184 MB CSV of five million sales records (date, store, product, quantity, revenue, and a short note):

``` python
import pandas as pd

df = pd.read_csv("sales.csv")
print(pd.__version__)
print(f"{df.memory_usage(deep=True).sum() / 1e6:.0f} MB in memory")
```

With pandas 3.0 (the current release in September 2026), the DataFrame took 368 MB, twice the file, and the Python process peaked at about 680 MB while reading it. With pandas 2.3, which stores text as general Python objects, the same DataFrame took 1,241 MB, nearly seven times the file. So if your laptop has 8 GB of memory, a 1 GB CSV can be comfortable, tight, or impossible depending on its columns and your pandas version. Check `pd.__version__`, measure with `memory_usage(deep=True)` on a sample, and work up the steps below in order, stopping at the first one that fits.

### Step 1: read less

Most analyses use a few columns of a wide file. Read only those, and tell pandas when a text column repeats a small set of values, so it can store each value once as a [category](https://pandas.pydata.org/docs/user_guide/categorical.html):

``` python
df = pd.read_csv(
    "sales.csv",
    usecols=["date", "store", "revenue"],
    dtype={"store": "category"},
    parse_dates=["date"],
)
```

That DataFrame took 90 MB instead of 368. Before any of this, `pd.read_csv("sales.csv", nrows=1000)` reads just the first thousand rows, which is enough to see the columns and choose.

### Step 2: read in chunks

When even the columns you need won’t fit, read the file a piece at a time. With `chunksize`, `read_csv` hands you one ordinary DataFrame of that many rows at a time, and you keep only a small summary of each:

``` python
parts = []
for chunk in pd.read_csv("sales.csv", usecols=["store", "revenue"], chunksize=500_000):
    parts.append(chunk.groupby("store")["revenue"].agg(["sum", "count"]))

totals = pd.concat(parts).groupby(level=0).sum()
mean_revenue = totals["sum"] / totals["count"]
```

Notice what each chunk keeps: a sum and a count, not a mean. Sums and counts can be added up across chunks; means can’t. Averaging the chunk averages here gives answers off by up to 0.004, which is small enough to miss and wrong all the same. When you summarize in chunks, keep pieces that combine by adding: sums, counts, minimums, and maximums.

Line-delimited JSON (see “Newline-delimited JSON” above) reads in chunks the same way: `pd.read_json("events.jsonl", lines=True, chunksize=100_000)` gives you a reader to loop over inside a `with` block.

### Step 3: convert to Parquet once

If you will read the same large file again and again, convert it to Parquet once (see “Parquet” above) and read from that. The 184 MB CSV became a 24 MB Parquet file, and `pd.read_parquet("sales.parquet", columns=["store", "revenue"])` reads only the two columns it names from disk.

### Step 4: let a query engine do the work

Two libraries answer questions about a large file without loading all of it into a DataFrame. They read only the columns a question needs, process the file in pieces, and use every core of your computer. You install them like any other package (`python -m pip install duckdb polars`).

[DuckDB](https://duckdb.org/docs/current/clients/python/overview.html) runs SQL directly on a CSV or Parquet file and gives you back a small pandas DataFrame:

``` python
import duckdb

result = duckdb.sql("""
    SELECT store, avg(revenue) AS mean_revenue, count(*) AS n
    FROM 'sales.csv'
    GROUP BY store
    ORDER BY store
""").df()
```

``` text
       store  mean_revenue      n
0  store-000     11.963152  24984
1  store-001     11.919008  25150
2  store-002     11.985570  24942
...
```

[Polars](https://docs.pola.rs/user-guide/) is a DataFrame library in the spirit of pandas. Its `scan_csv` builds a plan instead of reading the file, and `collect()` runs the plan, reading only what the plan needs:

``` python
import polars as pl

result = (
    pl.scan_csv("sales.csv")
    .group_by("store")
    .agg(pl.col("revenue").mean().alias("mean_revenue"), pl.len().alias("n"))
    .sort("store")
    .collect()
)
```

Both gave the same means as the chunked pandas code above. Pick DuckDB if you know SQL or want to learn it (see [sec-sql-basics](#sec-sql-basics)); pick Polars if you’d rather stay in Python method chains. Either way, the result is usually small, and `.df()` (DuckDB) or `.to_pandas()` (Polars) turns it into a pandas DataFrame for plotting and the rest of your analysis.

### What each step cost

[Table tbl-bigger-than-memory](#tbl-bigger-than-memory) shows what computing the mean revenue for each store took on one computer, a four-core Linux machine with 16 GB of memory. Peak memory is for the whole Python process, libraries included. Your numbers will differ; the pattern is what to take away.

| Approach                                   | Time  | Peak memory |
|--------------------------------------------|-------|-------------|
| pandas, whole file                         | 8.4 s | 680 MB      |
| pandas, two columns, `store` as a category | 2.4 s | 235 MB      |
| pandas, chunks of 500,000 rows             | 2.9 s | 205 MB      |
| pandas, two columns from Parquet           | 1.7 s | 445 MB      |
| DuckDB, on the CSV                         | 1.0 s | 245 MB      |
| DuckDB, on the Parquet file                | 0.5 s | 150 MB      |
| Polars, lazy scan of the CSV               | 0.5 s | 390 MB      |

Table 20.1: Computing mean revenue per store from a 184 MB CSV of five million rows, in September 2026 (pandas 3.0, DuckDB 1.5, Polars 1.44).

### When none of this is enough

If a question still doesn’t fit, work on a sample while you figure out what you’re asking. DuckDB can draw one as it reads (`SELECT * FROM 'sales.csv' USING SAMPLE 1%` returns roughly 1% of the rows). Then run the final version on a bigger computer: your university’s research computing cluster or a cloud machine (see [sec-remote-computing](#sec-remote-computing)).

## 20.8 Text encoding in general

Encoding problems confuse people because they’re invisible: a file looks fine in one program and garbled in another, and nothing says why. The idea is simple, though. A computer stores text as bytes, and a [character encoding](https://en.wikipedia.org/wiki/Character_encoding) is the rule for turning bytes into characters. [Unicode](https://en.wikipedia.org/wiki/Unicode) gives every character in every writing system a number, and UTF-8 is the standard way to write those numbers as bytes; make it your default. Older encodings like Windows-1252 and [Latin-1](https://en.wikipedia.org/wiki/ISO/IEC_8859-1) use one byte per character, so they have room for only 256: enough for Western European languages, and nothing for Greek, Cyrillic, Chinese, or most of the world’s writing.

Read bytes with the wrong rule and you get an error, or something worse: [mojibake](https://en.wikipedia.org/wiki/Mojibake), text that decodes without complaint into nonsense. Read a UTF-8 file as Latin-1, and `José Muñoz` comes out as `JosÃ© MuÃ±oz`. That’s why Latin-1 is a risky guess: it assigns a character to every possible byte, so it never fails, even on the wrong file. Read a Windows-1252 file as Latin-1 and it looks fine until you notice the curly quotes have become invisible control characters (`'\x93Smart\x94 quote'`). An error-free read isn’t proof you picked the right encoding, so look at a few rows with accented names. And if you see `Ã©` where `é` should be, don’t find-and-replace the damage; read the file again with the right encoding.

To find out what a file is, the `file` command guesses from its bytes: `file -i data.csv` on Linux, `file -I data.csv` on macOS (lowercase `-i` means something else there). On Linux, a Latin-1 file comes back as `charset=iso-8859-1`, and a Windows-1252 file with curly quotes as `charset=unknown-8bit`. On any system, you can look at the raw bytes in Python:

``` python
with open("data.csv", "rb") as f:
    raw = f.read(1000)
print(raw[:60])   # look at the raw bytes
```

``` text
b'id,name,city\n1,Jos\xe9 Mu\xf1oz,San Jos\xe9\n2,Zo\xeb Bront\xeb,Montr\xe9al\n3,\x93'
```

A lone `\xe9` (é in Windows-1252 and Latin-1) is the telltale of a file that isn’t UTF-8, where é takes two bytes, `\xc3\xa9`. If the error names byte `0xff` or `0xfe` in position 0, the file is probably UTF-16; try `encoding="utf-16"`.

One more invisible thing: some programs, including Excel’s “CSV UTF-8” option, start a file with three bytes called a [byte order mark](https://en.wikipedia.org/wiki/Byte_order_mark) (BOM). pandas skips it, but Python’s `csv` module glues it to the first column name as `'\ufeffid'`, which looks like `id` and won’t match it. Open such files with `encoding="utf-8-sig"`. When you write a file yourself, write UTF-8:

``` python
df.to_csv("out.csv", index=False, encoding="utf-8")
```

If someone will double-click it open in Excel, use `encoding="utf-8-sig"` instead: Excel [opens a UTF-8 CSV correctly when it starts with a BOM](https://support.microsoft.com/en-us/excel/opening-csv-utf-8-files-correctly-in-excel), and without one may show them mojibake.

## 20.9 Stakes and politics

In the autumn of 2020, nearly 16,000 positive COVID-19 tests in England went unreported for days. The labs’ CSV files were fine. The failure came when Public Health England pulled them into Excel templates saved in the old `.xls` format, which holds only about 65,000 rows. Each test took several rows, so a template filled up at around 1,400 cases, and, as the [BBC reported](https://www.bbc.com/news/technology-54423988), further cases were simply left off, with no error. Contact tracing for those people started late while the virus kept spreading. Nobody decided to drop those cases. A file format did, and its limit stayed invisible until someone went looking.

Most format decisions have smaller stakes, but the pattern repeats: defaults serve the people they were designed around, and the costs land on whoever doesn’t fit. A name like Muñoz or Nguyễn survives a pipeline only if every step agrees on the encoding, so it’s names from outside English that turn to mojibake or fail to match. Because a CSV carries no types, ZIP codes that start with 0, which cover every New England state, lose the zero and stop matching anything. And flattening nested JSON decides which parts of a record count as data. Each looks like a technical detail, and each decides whose records reach the analysis intact.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: when you choose or accept a data format, ask whose data it holds cleanly and whose it will truncate, garble, or drop without telling you.

## 20.10 Worked examples

### A “normal” CSV that is not normal

You run `df = pd.read_csv("sales.csv")` and get:

``` text
ParserError: Error tokenizing data. C error: Expected 5 fields in line 237, saw 6
```

**Diagnosis:** line 237 has one field too many, usually because a value contains an unquoted comma. pandas counts the header as line 1, so the number matches your text editor’s.

**Fix:** open the file, jump to line 237, and look. Here it reads `236,2026-01-13,Acme, Inc.,SKU-5,12.50`. A program following the CSV standard would have written `"Acme, Inc."` in double quotes, which pandas reads correctly, so the best fix is a properly quoted export. If you can’t get one, skip bad lines, loudly:

``` python
df = pd.read_csv("sales.csv", on_bad_lines="warn")
```

``` text
ParserWarning: Skipping line 237: expected 5 fields, saw 6
```

The Acme order is now gone from your data, so note every skipped line and check that losing them doesn’t change your answer.

### Silent missing-value corruption

You load eight days of temperature readings and take the average:

``` python
df = pd.read_csv("weather.csv")
df["temp_c"].mean()
```

``` text
np.float64(-233.4375)
```

No error, and an average colder than anywhere on Earth has ever been. `df["temp_c"].describe()` shows why: the minimum is `-999.0`, this file’s code (as in a lot of weather data) for “no reading.” It’s a perfectly good number, so pandas averaged it in.

**Fix:** tell pandas the code means missing:

``` python
df = pd.read_csv("weather.csv", na_values=["-999"])
df["temp_c"].mean()   # 21.75: the two missing readings are now NaN
```

### Nested JSON from a web API

You saved a response from GitHub’s repository search API: a `total_count`, and an `items` list with one record per repository, each with a nested `owner`:

``` python
import json
with open("repos.json") as f:
    data = json.load(f)

df = pd.json_normalize(data, record_path="items", meta=["total_count"])
print(df)
```

``` text
    id      full_name  stargazers_count owner.login    owner.type total_count
0  101  example/alpha              1520     example  Organization           2
1  102   example/beta                87     example  Organization           2
```

`record_path="items"` tells pandas which nested list holds the rows; `meta=["total_count"]` copies a top-level value onto every row, and `owner` became two dotted columns.

### Excel with a four-row banner

A report’s sheet has a title, a “Generated” date, and two blank rows above the real header, which starts in column B. Region names are merged down across each region’s stores, and revenue is a formula.

``` python
df = pd.read_excel(
    "quarterly_report.xlsx",
    sheet_name="Q4 Sales",
    skiprows=4,                  # skip the title, date, and blank rows
    header=0,                    # first row after skipping is the header
    usecols="B:G",               # only these columns (Excel letters!)
)
print(df)
```

``` text
  region    store  units  price  revenue  notes
0   West  Boulder     10    2.5      NaN    NaN
1    NaN   Denver      4    3.0      NaN    NaN
2   East   Boston      7    2.0      NaN    NaN
3    NaN      NYC      3    4.0      NaN    NaN
```

The header is right, and two messy-layout problems show. The `NaN`s in `region` are merged cells (fix with `ffill()`), and the empty `revenue` column means a script wrote this file without calculating its formulas; open and save it in Excel, or compute `units * price` yourself.

## 20.11 Templates

**A defensive `read_csv` that handles the common quirks:**

``` python
df = pd.read_csv(
    "data.csv",
    sep=",",
    encoding="utf-8",
    na_values=["-", "--", "-999"],   # added to pandas' defaults; use your file's own codes
    parse_dates=["date"],            # adjust to your date columns
    dtype={"zip": "str"},            # keep codes like ZIP codes as text
)
```

**A validation snippet to run after every load:**

``` python
print("shape:", df.shape)
print("columns:", df.columns.tolist())
print(df.dtypes)
print(df.head())
print("nulls per column:")
print(df.isna().sum())
```

## 20.12 Exercises

1.  Take a CSV file from a real data source (a government open-data portal, a Kaggle dataset, or your course). Open it in a text editor and note the delimiter, the header row, and any missing-value codes. Then load it with `pd.read_csv`, passing the right parameters the first time.
2.  Save a small CSV with accented names using `encoding="cp1252"`. Read it with the default UTF-8 and read the `UnicodeDecodeError`. Then read it correctly, and once more with `encoding="latin-1"`: did anything change, and would you have noticed?
3.  Find a dataset with numeric codes for missing values (temperatures, survey responses). Load it once without `na_values` and once with, and run `.describe()` on both. How far did the averages move?
4.  Load a nested JSON file (an API response you saved, for example). Use `pd.json_normalize` to flatten the records you care about.
5.  Load an Excel file with several sheets. Use `sheet_name=None` to get a dictionary, then loop over it to print the shape of each sheet.
6.  Convert a CSV you use often to Parquet. Compare file sizes, load times (`%time df = pd.read_csv(...)` vs `%time df = pd.read_parquet(...)`), and `df.dtypes` after each load.
7.  Take the largest CSV you have (or make one by repeating a small file many times). Measure its memory with `df.memory_usage(deep=True).sum()`, then compute one grouped mean three ways: pandas on the whole file, pandas in chunks, and DuckDB. Check that the answers match.
8.  Turn the validation snippet in Templates into a reusable function `validate(df)` that prints the report. Put it in a module you can import from any notebook.

## 20.13 One-page checklist

- Open unfamiliar CSVs in a text editor first; note the delimiter, encoding, and header layout.
- Default to UTF-8. On a `UnicodeDecodeError`, try `cp1252`; `latin-1` never errors, even when it’s wrong.
- Pass `na_values=` with the file’s own missing-value codes; pandas already handles `NA`, `N/A`, `NULL`, and empty cells.
- Read ID-like codes (ZIP codes, phone numbers) as text with `dtype=`.
- Use `parse_dates=` at read time, with `date_format=` when dates might be day first.
- Check `df.shape`, `df.columns`, `df.dtypes`, and `df.head()` in the cell right after every `read_*`.
- If a numeric column shows up as `str` (pandas 3) or `object` (pandas 2), you have hidden strings. Use `pd.to_numeric(..., errors="coerce")` to find them.
- Use Parquet for intermediate files and anything over ~100 MB; share and archive a UTF-8 CSV with a data dictionary.
- Read Stata and SPSS files with `pd.read_stata` and `pd.read_spss` (which needs pyreadstat); value labels arrive as categories.
- If a file won’t fit in memory: read fewer columns, read in chunks (keeping sums and counts, not means), or query it with DuckDB or Polars.
- Always pass `index=False` when writing a CSV or Excel file unless you want the row index as a column.
- When in doubt, `df.head()` and `df.tail()`, and trust your eyes over your assumptions.

> **NOTE:**
>
> - **pandas**, [`read_csv` reference](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) — every parameter with notes on each; the `na_values`, `parse_dates`, `dtype`, and `encoding` entries alone reward a careful read.
> - **IETF**, [RFC 4180: Common Format and MIME Type for CSV Files](https://www.rfc-editor.org/rfc/rfc4180) — the short, official CSV specification; handy for settling arguments about quoting and line endings.
> - **json.org**, [Introducing JSON](https://www.json.org/json-en.html) — the whole JSON syntax on one page, drawn as diagrams you can check a stubborn file against.
> - **Apache**, [Parquet documentation](https://parquet.apache.org/docs/) — the format’s own documentation; the overview and file-format pages are short and explain why columnar files are so fast.
> - **Joel Spolsky**, [The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets](https://www.joelonsoftware.com/2003/10/08/the-absolute-minimum-every-software-developer-absolutely-positively-must-know-about-unicode-and-character-sets-no-excuses/) — a 2003 essay that’s still the best half-hour introduction to encodings; read it after your first `UnicodeDecodeError`.
> - **ECMA International**, [Office Open XML File Formats (ECMA-376)](https://ecma-international.org/publications-and-standards/standards/ecma-376/) — the standard underneath `.xlsx` files, for when you want to know what’s really inside one (a zip of XML).
> - **Tom Augspurger**, [Modern Pandas (Part 1)](https://tomaugspurger.net/posts/modern-1-intro/) — the start of an intermediate series that opens by downloading and reading a real, messy government dataset; written in 2016, so some code is dated, but the habits hold.
