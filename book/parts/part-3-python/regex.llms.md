# 18  Regular Expressions

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).
>
> **See also:** [sec-data-file-formats](#sec-data-file-formats), [sec-terminal](#sec-terminal), [sec-debugging](#sec-debugging).

## Purpose

Sooner or later you will need to extract phone numbers from free-text notes, find every file name that matches a pattern, strip junk out of a column, or validate that a user-entered email address at least *looks* like one. These are all jobs for regular expressions — a small pattern language that matches shapes in text.

Regex has a reputation for being write-once, read-never code. That reputation is earned when people try to express overly clever patterns. For the 90% case you will actually use in data work — finding specific words, extracting substrings, matching digits, cleaning whitespace — regex is a modest, learnable tool. This chapter teaches you enough to use it confidently in pandas, Python scripts, text editors, and the terminal without reaching for a cheat sheet every time.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain what a regular expression is and name three situations where it is the right tool.
2.  Read a short regex and predict what it will match.
3.  Use literal characters, the seven core metacharacters, character classes, and anchors to write patterns.
4.  Use [`re.search`](https://docs.python.org/3/library/re.html#re.search), `re.match`, `re.findall`, and `re.sub` in [Python’s `re` module](https://docs.python.org/3/library/re.html) with sensible defaults.
5.  Use capture groups to extract parts of a match.
6.  Use [`pandas.Series.str.contains`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html), `.str.extract`, and `.str.replace` for regex on DataFrames.
7.  Recognize when a regex is becoming too clever and reach for a real parser instead.

## Running theme: match shapes, not meaning

Regex matches the *shape* of text — three digits, a dot, four digits — not its meaning. If your problem requires understanding what the text *means* (parsing HTML, real emails, code, dates with validation), regex is the wrong tool. If it requires finding a pattern of characters, regex is perfect.

## 18.1 The seven metacharacters you actually need

The entire language is built from a small set of special characters that mean “not themselves.” Here are the ones you will use constantly:

| Symbol | Meaning                                               |
|--------|-------------------------------------------------------|
| `.`    | any single character except newline                   |
| `*`    | zero or more of the preceding item                    |
| `+`    | one or more of the preceding item                     |
| `?`    | zero or one of the preceding item (makes it optional) |
| `^`    | start of string (or line, with `re.MULTILINE`)        |
| `$`    | end of string (or line)                               |
| `\|`   | alternation: `cat\|dog` matches either                |

Plus these two for grouping and escaping:

| Symbol  | Meaning                                                           |
|---------|-------------------------------------------------------------------|
| `(...)` | capture group — saves what matched for later extraction           |
| `\`     | escape — `\.` means a literal dot, `\\` means a literal backslash |

That is most of what you need to know to read 90% of the regexes you encounter in the wild.

## 18.2 Character classes: the shortcut for “one of these”

A character class matches exactly one character from a set:

| Syntax           | Matches                                 |
|------------------|-----------------------------------------|
| `[abc]`          | `a`, `b`, or `c`                        |
| `[a-z]`          | any lowercase letter                    |
| `[A-Za-z0-9]`    | any alphanumeric character              |
| `[^abc]`         | any character *except* `a`, `b`, or `c` |
| `\d`             | any digit (equivalent to `[0-9]`)       |
| `\w`             | any “word” character (`[A-Za-z0-9_]`)   |
| `\s`             | any whitespace (space, tab, newline)    |
| `\D`, `\W`, `\S` | the negations                           |

Combine with `+`, `*`, `?`, or `{n,m}` to repeat:

| Syntax    | Matches                |
|-----------|------------------------|
| `\d+`     | one or more digits     |
| `\d{3}`   | exactly 3 digits       |
| `\d{3,5}` | between 3 and 5 digits |
| `\d{2,}`  | 2 or more digits       |

## 18.3 Anchors: where in the string

| Syntax    | Matches                                                     |
|-----------|-------------------------------------------------------------|
| `^foo`    | string starts with `foo`                                    |
| `foo$`    | string ends with `foo`                                      |
| `\bfoo\b` | word boundary: `foo` as a whole word, not `food` or `tofoo` |

Word boundaries (`\b`) are the most underused regex feature for data work. They are the difference between matching `cat` in `"the cat sat"` (what you want) and also matching it in `"concatenate"` (what you do not).

## 18.4 Python’s `re` module

Import once at the top of your script or notebook:

``` python
import re
```

The four functions you will use most:

``` python
re.search(pattern, text)           # find first match anywhere, or None
re.match(pattern, text)            # match only at the start of text
re.findall(pattern, text)          # list of all non-overlapping matches
re.sub(pattern, replacement, text) # replace all matches
```

**Always use raw string literals for patterns.** Python strings interpret backslashes (`\n` is a newline), and regex uses backslashes for its own special meanings. The raw-string prefix `r""` tells Python not to interpret them:

``` python
# Good
re.search(r"\d+", "order #42")

# Bad: Python sees \d as an invalid escape (or silently a literal 'd')
re.search("\d+", "order #42")
```

Make raw strings a reflex.

### Flags

Two flags come up constantly:

``` python
re.search(r"python", "Python", re.IGNORECASE)   # case-insensitive
re.findall(r"^\w+", big_text, re.MULTILINE)     # ^ matches each line
```

You can combine them: `re.IGNORECASE | re.MULTILINE`.

## 18.5 Capture groups: extracting parts of a match

Parentheses do two jobs: they group a sub-pattern and they *capture* what matched so you can pull it out later.

``` python
text = "Order placed on 2024-03-15 for $29.99"
match = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
if match:
    year, month, day = match.group(1), match.group(2), match.group(3)
    print(year, month, day)    # 2024 03 15
```

You can also reference groups in the replacement string of `re.sub`:

``` python
re.sub(r"(\w+)@(\w+)", r"\2.\1", "alice@example")
# 'example.alice'
```

And you can give groups names for readability:

``` python
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)
m.group("year")   # '2024'
```

## 18.6 Regex in pandas

pandas has regex built into its string methods. Three you will reach for constantly:

**`.str.contains(pattern)`** — boolean mask for rows that match:

``` python
mask = df["note"].str.contains(r"refund|chargeback", case=False, na=False)
df[mask]
```

Always pass `na=False` unless you specifically want `NaN` to propagate; otherwise a missing value becomes a missing mask and the row filter breaks.

**`.str.extract(pattern)`** — pull capture groups into new columns:

``` python
# Extract the order number from a free-text note column
df["order_id"] = df["note"].str.extract(r"Order #(\d+)")
```

If your pattern has multiple groups, you get a DataFrame:

``` python
parts = df["date"].str.extract(r"(\d{4})-(\d{2})-(\d{2})")
parts.columns = ["year", "month", "day"]
```

**`.str.replace(pattern, repl, regex=True)`** — substitute matches:

``` python
df["phone"] = df["phone"].str.replace(r"[^\d]", "", regex=True)
```

That last example strips every non-digit character, normalizing `(303) 555-1212` and `303.555.1212` both to `3035551212`.

## 18.7 When not to use regex

Regex is a hammer. It is not the right tool for:

- **Parsing HTML or XML.** Use `BeautifulSoup` or `lxml`. HTML is not regular, and regex on it is a well-known anti-pattern with many famous rants about it.
- **Parsing JSON.** Use the `json` module. See [sec-data-file-formats](#sec-data-file-formats).
- **Validating real email addresses or URLs.** The official email regex is thousands of characters long. Use a dedicated library (`email-validator`, `urllib.parse`) or a simple “contains an @ and a dot” sanity check.
- **Anything where you need to understand structure, not match shape.** If the text has nested elements, recursion, or balanced brackets, regex will frustrate you. Reach for a real parser.

A good rule of thumb: if your regex is longer than one line or contains more than three `(...)` groups, reconsider.

> **NOTE:**
>
> - [Python `re` module reference](https://docs.python.org/3/library/re.html) — the authoritative list of pattern syntax and functions.
> - [Python Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) — a longer-form tutorial that builds intuition before you reach for the reference.
> - [regex101](https://regex101.com/) — an interactive tester that explains every part of a pattern as you type.

## 18.8 Worked examples

### Extracting order IDs from free-text notes

You have a column of customer service notes and you need the order ID mentioned in each one.

``` python
import pandas as pd

notes = pd.Series([
    "Customer called about Order #4829, refund requested",
    "Order #1337 shipped late",
    "No order mentioned",
    "Orders #9999 and #1000, dispute",
])

orders = notes.str.extract(r"Order #(\d+)")
print(orders)
```

Output:

          0
    0  4829
    1  1337
    2   NaN
    3  9999

Note that row 3 only extracted the first match. If you need all matches per row, use `.str.findall(r"Order #(\d+)")` instead and deal with the list.

### Normalizing phone numbers

``` python
phones = ["(303) 555-1212", "303.555.1212", "+1 303 555 1212", "3035551212"]
cleaned = [re.sub(r"[^\d]", "", p) for p in phones]
# ['3035551212', '3035551212', '13035551212', '3035551212']
```

Now you can compare them (modulo the country code).

### Simple validation with `re.fullmatch`

``` python
def looks_like_us_zip(s: str) -> bool:
    return bool(re.fullmatch(r"\d{5}(-\d{4})?", s))

looks_like_us_zip("80301")         # True
looks_like_us_zip("80301-1234")    # True
looks_like_us_zip("803011")        # False
looks_like_us_zip("80301 ")        # False (trailing space)
```

`re.fullmatch` requires the pattern to cover the *entire* string — much safer than `re.match` for validation.

### Grep from the terminal

The `grep` command uses regex too. From [sec-terminal](#sec-terminal):

``` bash
grep -E '^def \w+' src/*.py          # every function definition
grep -rn 'TODO|FIXME' src/           # all TODO / FIXME markers
grep -vE '^\s*#' config.cfg          # strip comment lines
```

Your regex skill transfers directly.

## 18.9 Templates

**A cheat-sheet for the patterns you will reuse most often:**

``` python
r"\d+"              # one or more digits
r"\d{3}-\d{4}"      # 3 digits, dash, 4 digits
r"[A-Za-z]+"        # one or more letters
r"\s+"              # whitespace run (use for splitting or cleanup)
r"^\s+|\s+$"        # leading or trailing whitespace (alt to .strip())
r"\b\w+\b"          # whole words
r"[A-Z][a-z]+"      # a capitalized word (names, usually)
r"#\w+"             # hashtag
r"@\w+"             # mention / username
r"\d{4}-\d{2}-\d{2}"# ISO-ish date (shape only, not validation)
```

## 18.10 Exercises

1.  Write a regex that matches a US phone number written as `(xxx) xxx-xxxx`, `xxx-xxx-xxxx`, or `xxx.xxx.xxxx`. Test it on five variations.
2.  You have a log file with lines like `2024-03-15 14:22:03 ERROR Failed to connect`. Write a regex with capture groups that extracts the date, time, level, and message.
3.  Given a pandas Series of URLs, use `.str.extract` to pull out the domain (the part between `://` and the next `/`).
4.  Write a regex that matches words of 4–7 letters from a block of English text. Use `\b`. Find a short paragraph to test on.
5.  Use `re.sub` to redact credit card numbers from a string, replacing any 16-digit run with `XXXX-XXXX-XXXX-XXXX`.
6.  Using the terminal, run `grep -E` with a regex to find every line in your Python source files that starts with `def` or `class` — a quick index of your API.
7.  Take a regex you find confusing and rewrite it on paper, breaking it into pieces and explaining each. If you cannot, it is probably too clever and a simpler approach exists.

## 18.11 One-page checklist

- Use raw strings (`r"..."`) for every Python regex.
- Start with the simplest thing that matches what you want; only add complexity when it fails.
- Anchor with `\b`, `^`, or `$` when you want exact boundaries.
- Use character classes (`\d`, `\w`, `\s`) rather than long bracket groups.
- Use `re.fullmatch` for validation, `re.search` for extraction, `re.findall` for all matches, `re.sub` for replacement.
- In pandas, use `.str.contains(..., na=False)`, `.str.extract`, and `.str.replace(..., regex=True)`.
- Test your regex on at least one “expected” and one “unexpected” input before trusting it.
- Reach for a parser (BeautifulSoup, json, etc.) when the text has structure.
- If your regex is over one line or has lots of groups, consider rewriting in Python code.
