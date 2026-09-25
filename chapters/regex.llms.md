# 18  Regular Expressions

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).
>
> **See also:** [sec-data-file-formats](#sec-data-file-formats), [sec-terminal](#sec-terminal), [sec-debugging](#sec-debugging).

## Purpose

![Headaches Meme: Writing Regex.](../graphics/memes/regex.png)

Your supervisor hands you 3,000 customer-service notes and asks for a column of the order numbers mentioned in them. The notes say things like “Customer called about Order \#4829, refund requested,” but no two are worded alike, so you can’t split on a comma or slice off the first ten characters. You could read all 3,000. Or you could describe what an order number *looks like*, a `#` followed by digits, and let the computer find every one in under a second.

That description is a [regular expression](https://en.wikipedia.org/wiki/Regular_expression), or regex: a small pattern language for matching shapes in text. It has a reputation as write-once, read-never line noise, and if you’ve ever stared at `^\(?\d{3}\)?[-. ]?\d{3}[-. ]?\d{4}$` and felt your eyes slide off it, that’s fair. But the patterns you’ll need for data work are short, and each piece means one simple thing.

This chapter teaches that working core in Python, pandas, and grep, along with the snags that trip almost everyone at first. It skips the theory and rarer features such as lookarounds; Further reading points you to both.

## Why read this chapter

- You ran `re.match(r"\d+", "Order 42")`, got `None`, and stared at the screen, because there’s obviously a 42 right there.
- You tried to grab one quoted phrase with `".*"` and got everything from the first quote on the line to the last.
- You searched a column for `3.5` and got `Room 305` back too, or searched for `C++` and pandas threw an error.
- You have phone numbers typed five different ways, or order numbers buried in free-text notes, and you need them in a clean column today.
- You pasted a pattern that works in Python into grep or your editor, and it quietly found nothing.
- Python printed `SyntaxWarning: invalid escape sequence '\d'`, and you’re not sure whether to care.
- Someone told you never to parse HTML with regex, and you’d like to know why, and what to use instead.

## Running theme: match shapes, not meaning

A regex matches the *shape* of text (three digits, a dot, four digits), never what it means, so it’s perfect for finding patterns of characters and the wrong tool when you need to understand structure, like HTML, real email addresses, or whether a date exists.

## 18.1 The characters that don’t mean themselves

Most characters in a regex match themselves: the pattern `cat` finds c, a, t in a row. The rest of the language comes from a few [metacharacters](https://en.wikipedia.org/wiki/Metacharacter) that mean something else (the `*`, for instance, has a name: the [Kleene star](https://en.wikipedia.org/wiki/Kleene_star)). Learn these seven and you can read most patterns you’ll meet:

| Symbol | Meaning                                               |
|--------|-------------------------------------------------------|
| `.`    | any single character except newline                   |
| `*`    | zero or more of the preceding item                    |
| `+`    | one or more of the preceding item                     |
| `?`    | zero or one of the preceding item (makes it optional) |
| `^`    | start of string (or line, with `re.MULTILINE`)        |
| `$`    | end of string (or line)                               |
| `\|`   | alternation: `cat\|dog` matches either                |

Two more handle grouping and escaping:

| Symbol  | Meaning                                                    |
|---------|------------------------------------------------------------|
| `(...)` | capture group: saves what matched for later extraction     |
| `\`     | escape: `\.` means a literal dot, `\\` a literal backslash |

The one that catches everyone is `.`. You search for version `3.5` and get `Room 305` too, because an unescaped `.` means “any character,” and `0` is a character. To match a real dot, put a backslash in front of it, and do the same for any metacharacter you mean literally: `\$`, `\(`, `\+`. For a whole string you want matched exactly, [`re.escape`](https://docs.python.org/3/library/re.html#re.escape) adds the backslashes for you: `re.escape("$5.00")` gives `\$5\.00`.

``` python
import re

re.findall("3.5", "Room 305, version 3.5")     # ['305', '3.5']
re.findall(r"3\.5", "Room 305, version 3.5")   # ['3.5']
```

## 18.2 Character classes: one character from a set

Often you know only the *kind* of character you want: a digit, a letter, some whitespace. A **character class** matches exactly one character from a set:

| Syntax           | Matches                                        |
|------------------|------------------------------------------------|
| `[abc]`          | `a`, `b`, or `c`                               |
| `[a-z]`          | any lowercase ASCII letter                     |
| `[A-Za-z0-9]`    | any ASCII letter or digit                      |
| `[^abc]`         | any character *except* `a`, `b`, or `c`        |
| `\d`             | any digit                                      |
| `\w`             | any “word” character: letters, digits, and `_` |
| `\s`             | any whitespace (space, tab, newline)           |
| `\D`, `\W`, `\S` | the opposites                                  |

Notice that `^` does two unrelated jobs: at the start of square brackets it means “not,” and outside them it means “start of the string.” It confuses nearly everyone once.

Tutorials often say `\d` equals `[0-9]` and `\w` equals `[A-Za-z0-9_]`. That’s true for [ASCII](https://en.wikipedia.org/wiki/ASCII), but in Python 3 these classes cover all of [Unicode](https://en.wikipedia.org/wiki/Unicode): `\w` matches `é` and `李`, and `\d` matches the [Eastern Arabic digits](https://en.wikipedia.org/wiki/Eastern_Arabic_numerals) in `٣٤٥`. That’s usually what you want. For only 0 to 9, write `[0-9]` or pass the [`re.ASCII`](https://docs.python.org/3/library/re.html#re.ASCII) flag:

``` python
re.findall(r"\d+", "Room ٣٤٥ and 42")      # ['٣٤٥', '42']
re.findall(r"[0-9]+", "Room ٣٤٥ and 42")   # ['42']
```

A class matches one character; a quantifier after it says how many:

| Syntax    | Matches                |
|-----------|------------------------|
| `\d+`     | one or more digits     |
| `\d{3}`   | exactly 3 digits       |
| `\d{3,5}` | between 3 and 5 digits |
| `\d{2,}`  | 2 or more digits       |

## 18.3 Anchors and word boundaries

Anchors pin a match to a position. They match a *place* between characters, not a character:

| Syntax    | Matches                                      |
|-----------|----------------------------------------------|
| `^foo`    | string starts with `foo`                     |
| `foo$`    | string ends with `foo`                       |
| `\bfoo\b` | `foo` as a whole word, not `food` or `tofoo` |

The word boundary `\b` is the most underused feature in data work. It’s the difference between finding `cat` in `"the cat sat"` and also in `"concatenate"`. If a search returns suspiciously many hits, wrapping the word in `\b` is often the whole fix.

## 18.4 Greedy and lazy: why `.*` eats too much

Nearly everyone hits this in their first week. You want every quoted phrase in a line, so you write a quote, anything, a quote, and get one long match instead of two:

``` python
line = 'She said "hi" and then "bye"'
re.findall(r'".*"', line)      # ['"hi" and then "bye"']
re.findall(r'".*?"', line)     # ['"hi"', '"bye"']
re.findall(r'"[^"]*"', line)   # ['"hi"', '"bye"']
```

Nothing is broken. Quantifiers are **greedy**: `.*` takes as much as it can and gives back only enough for the rest of the pattern to match, so it runs to the *last* quote. A `?` after a quantifier (`*?`, `+?`) makes it **lazy**, taking as little as it can. The third version is usually the better habit, because it says exactly what may appear between the quotes. The HOWTO covers this in [Greedy versus non-greedy](https://docs.python.org/3/howto/regex.html#greedy-versus-non-greedy).

Greed has a darker side. When a match fails, the engine [backtracks](https://en.wikipedia.org/wiki/Backtracking) to try other ways of dividing the text among the quantifiers, and with one quantifier nested inside another, like `(a+)+b`, the ways multiply: on the machine this chapter was tested on, `re.fullmatch(r"(a+)+b", "a" * 24)` took nearly a second to fail, roughly doubling with each extra `a`. That’s how a [ReDoS](https://en.wikipedia.org/wiki/ReDoS) attack works, and how one firewall regex [took down much of Cloudflare for 27 minutes](https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/) in July 2019. So don’t nest quantifiers, and prefer `[^"]*` to `.*`.

## 18.5 Python’s `re` module

In Python, regex lives in the standard library’s `re` module. Import it once at the top of a script or notebook; these five functions cover nearly everything:

``` python
re.search(pattern, text)            # first match anywhere, or None
re.match(pattern, text)             # a match only at the very start, or None
re.fullmatch(pattern, text)         # a match only if the pattern covers all of text
re.findall(pattern, text)           # list of all non-overlapping matches
re.sub(pattern, replacement, text)  # replace every match
```

### search, match, or fullmatch?

The name `match` sounds like “does this match anywhere?”, but [`re.match`](https://docs.python.org/3/library/re.html#re.match) only looks at the *start* of the string:

``` python
re.match(r"\d+", "Order 42")              # None
re.search(r"\d+", "Order 42")             # <re.Match object; span=(6, 8), match='42'>
re.fullmatch(r"\d+", "42 is the answer")  # None
```

Use [`re.search`](https://docs.python.org/3/library/re.html#re.search) to find something, [`re.fullmatch`](https://docs.python.org/3/library/re.html#re.fullmatch) to check that a whole string has the right shape, and `re.match` rarely. The docs explain the difference in [search() vs. match()](https://docs.python.org/3/library/re.html#search-vs-match).

### Raw strings, always

Python strings have their own backslash codes, like `\n` for newline, and Python processes them *before* the regex engine sees your pattern. Often you get lucky: `"\d"` isn’t a Python escape, so the backslash survives and the pattern works. Python 3.12 and later grumble with `SyntaxWarning: invalid escape sequence '\d'`; older versions say nothing. The unlucky case is `\b`, which *is* a Python escape, meaning backspace, so `"\bcat\b"` silently matches nothing:

``` python
re.search("\bcat\b", "the cat sat")     # None
re.search(r"\bcat\b", "the cat sat")    # <re.Match object; span=(4, 7), match='cat'>
```

The `r` prefix makes a [raw string](https://docs.python.org/3/reference/lexical_analysis.html#raw-strings), in which a backslash is just a backslash. Put `r` in front of every pattern and this whole class of bug (the HOWTO calls it [the backslash plague](https://docs.python.org/3/howto/regex.html#the-backslash-plague)) disappears.

### Flags

[Flags](https://docs.python.org/3/library/re.html#flags) change how a whole pattern behaves. Two come up constantly, and you can combine them with `|`:

``` python
text = "alpha one\nbeta two\ngamma three"
re.findall(r"^\w+", text)                       # ['alpha']
re.findall(r"^\w+", text, re.MULTILINE)         # ['alpha', 'beta', 'gamma']
re.search(r"python", "Python", re.IGNORECASE)   # matches 'Python'
```

## 18.6 Capture groups: pulling out the parts

Finding a date is nice; getting its year, month, and day separately is usually the point. Parentheses group part of a pattern and *capture* what it matched:

``` python
text = "Order placed on 2024-03-15 for $29.99"
match = re.search(r"(\d{4})-(\d{2})-(\d{2})", text)
if match:
    year, month, day = match.group(1), match.group(2), match.group(3)
    print(year, month, day)    # 2024 03 15
```

Keep the `if match:`. When nothing matches, `re.search` returns `None`, and calling `.group()` on it gives `AttributeError: 'NoneType' object has no attribute 'group'`, one of the most common regex errors there is.

In a [`re.sub`](https://docs.python.org/3/library/re.html#re.sub) replacement, `\1` means “whatever group 1 matched”:

``` python
re.sub(r"(\w+)@(\w+)", r"\2.\1", "alice@example")
# 'example.alice'
```

Once a pattern has several groups, name them, so you don’t have to count parentheses later:

``` python
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", text)
m.group("year")   # '2024'
```

## 18.7 Regex in pandas

Your text usually lives in a DataFrame column, and pandas’ [string methods](https://pandas.pydata.org/docs/user_guide/text.html) take patterns directly, with a few defaults that surprise people.

**[`.str.contains`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.contains.html)** gives a True/False mask for filtering rows:

``` python
mask = df["note"].str.contains(r"refund|chargeback", case=False, na=False)
df[mask]
```

The surprise is that it treats your search text as a regex *by default*. That’s why `3.5` also finds `Room 305`, and why, with PyArrow installed, searching a skills column for `C++` fails with `ArrowInvalid: Invalid regular expression: bad repetition operator: ++`. For literal text, say so with `regex=False` (or use `re.escape`):

``` python
skills.str.contains("C++", regex=False)
```

Keep `na=False`, too. pandas 3 already gives `False` for missing text, but in a mixed-type `object` column (or older pandas) a missing value stays missing, and the filter fails with `ValueError: Cannot mask with non-boolean array containing NA / NaN values`.

**[`.str.extract`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.extract.html)** pulls capture groups into columns. It returns a DataFrame, even for one group; pass `expand=False` for a plain column, and name groups to name the columns:

``` python
df["order_id"] = df["note"].str.extract(r"Order #(\d+)", expand=False)
parts = df["date"].str.extract(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})")
```

What comes back is text (`'4829'`, not `4829`), so use `pd.to_numeric` before doing arithmetic. Rows with no match get `NaN`, and only the *first* match counts; [`.str.findall`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.findall.html) returns every match as a list.

**[`.str.replace`](https://pandas.pydata.org/docs/reference/api/pandas.Series.str.replace.html)** flips the default: since pandas 2.0 it treats the pattern as plain text unless you pass `regex=True`. Forget it and the column comes back unchanged, with no error:

``` python
df["phone"] = df["phone"].str.replace(r"[^\d]", "", regex=True)
```

That strips every non-digit, turning both `(303) 555-1212` and `303.555.1212` into `3035551212`.

## 18.8 Same idea, different dialects

Regex is a family of dialects, or *flavors*, that agree on the basics and differ in the details ([Wikipedia compares many of them](https://en.wikipedia.org/wiki/Comparison_of_regular_expression_engines)). That’s why a pattern tested in Python can find nothing somewhere else.

**grep** (see [sec-terminal](#sec-terminal)) uses *basic* syntax by default, where `|`, `+`, `?`, and parentheses are ordinary characters unless backslashed, so `grep -rn 'TODO|FIXME' src/` looks for the literal text `TODO|FIXME`. Add `-E` for *extended* syntax, close to this chapter’s. Neither knows `\d`: GNU grep reads `grep -E '\d+'` as a plain `d`, matching `odd` and skipping `42`. Use `[0-9]` or `[[:digit:]]`, or `-P` on GNU grep. The [GNU grep manual](https://www.gnu.org/software/grep/manual/grep.html#Basic-vs-Extended) lists the differences. macOS ships a BSD grep with its own quirks; POSIX classes like `[[:digit:]]` and `[[:space:]]` work in both.

**pandas 3**, when PyArrow is installed, stores text with PyArrow and sends most patterns to its engine, Google’s RE2 ([per Arrow’s docs](https://arrow.apache.org/docs/cpp/compute.html)), falling back to `re` for features RE2 lacks. Everyday patterns behave the same, with exceptions: `C++` is legal in Python 3.11 and later but an error in RE2, and RE2’s `\w` and `\d` match only ASCII.

**Editors and spreadsheets** vary too: a [VS Code regex replace](https://code.visualstudio.com/docs/editing/codebasics#_search-and-replace) writes a group as `$1`, not `\1`, and Google Sheets’ [`REGEXMATCH`](https://support.google.com/docs/answer/3098292) uses RE2.

When a pattern misbehaves, paste it into [regex101](https://regex101.com/), pick your tool’s flavor (Python is one), and it explains every piece.

## 18.9 When not to use regex

Regex is a hammer, and some jobs aren’t nails:

- **Parsing HTML or XML.** Use [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) or [lxml](https://lxml.de/). HTML nests tags to any depth, which a true regular expression can’t track (it isn’t a [regular language](https://en.wikipedia.org/wiki/Regular_language)).
- **Parsing JSON.** Use the [`json`](https://docs.python.org/3/library/json.html) module. See [sec-data-file-formats](#sec-data-file-formats).
- **Validating real email addresses or URLs.** A regex that follows the old email standard (RFC 822) [runs past 6,000 characters](https://pdw.ex-parrot.com/Mail-RFC822-Address.html) and still can’t handle everything the standard allows. Use a library such as [email-validator](https://pypi.org/project/email-validator/), split URLs with [`urllib.parse`](https://docs.python.org/3/library/urllib.parse.html), or settle for “contains an `@` and a dot.”
- **Anything where you need structure, not shape.** Nested elements, balanced brackets, and recursion call for a real [parser](https://en.wikipedia.org/wiki/Parsing).

A good rule of thumb: if your regex is longer than one line or has more than three groups, reconsider. Write plain Python instead, or at least use the [`re.VERBOSE`](https://docs.python.org/3/library/re.html#re.VERBOSE) flag, which lets you spread a pattern over several lines with a comment on each piece.

## 18.10 Stakes and politics

If a web form has ever told you your name contains invalid characters, you’ve met a regex written by someone whose name it fits. Often the culprit is a pattern like `^[A-Za-z]+$`, which accepts Smith and rejects José, Nguyễn, O’Brien, Mary-Jane, and 李, leaving each of those people to misspell their own name to get through. Python’s `\w` is kinder, counting accented letters and Chinese characters as word characters, but that depends on the engine. With pandas 3.0.6 and PyArrow, `re.fullmatch(r"\w+", "José")` succeeds, while `.str.fullmatch(r"\w+")` on a column holding the same name returns `False`, because PyArrow’s engine treats `\w` as ASCII only.

The politics sits in the defaults. Which alphabet counts as “letters” was decided by whoever wrote the class or built the engine, and the cost falls on the people it leaves out, who rarely see the pattern that turned them away.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: before you validate or filter text that people write about themselves, test your pattern on names from outside your own alphabet, and ask whether you need to validate them at all.

## 18.11 Worked examples

### Extracting order IDs from free-text notes

You have a column of customer-service notes and need the order ID in each one.

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
    3   NaN

Row 3 came back empty, though it plainly mentions two orders: the pattern wants `Order #`, and row 3 says `Orders #`. A regex does what you wrote, not what you meant, so look at the `NaN` rows before you trust an extraction. `r"Orders? #(\d+)"` fixes it, returning `9999` for row 3, but `.str.extract` still takes only the first match. For every order in every row, `notes.str.findall(r"#(\d+)")` gives a list per row, with `['9999', '1000']` for row 3.

### Normalizing phone numbers

``` python
phones = ["(303) 555-1212", "303.555.1212", "+1 303 555 1212", "3035551212"]
cleaned = [re.sub(r"[^\d]", "", p) for p in phones]
# ['3035551212', '3035551212', '13035551212', '3035551212']
```

`[^\d]` means “anything that isn’t a digit” (so does `\D`). Now you can compare the numbers, once you decide what to do about the leading country code on the third.

### Simple validation with `re.fullmatch`

``` python
def looks_like_us_zip(s: str) -> bool:
    return bool(re.fullmatch(r"\d{5}(-\d{4})?", s))

looks_like_us_zip("80301")         # True
looks_like_us_zip("80301-1234")    # True
looks_like_us_zip("803011")        # False
looks_like_us_zip("80301 ")        # False (trailing space)
```

`re.fullmatch` requires the pattern to cover the *entire* string. With `re.match`, `"803011"` would pass, because its first five characters look fine.

### grep from the terminal

The same patterns work in the terminal ([sec-terminal](#sec-terminal)), minding the dialect differences above:

``` bash
grep -E '^def [a-z_]+' src/*.py        # every top-level function definition
grep -rnE 'TODO|FIXME' src/            # every TODO or FIXME, with line numbers
grep -vE '^[[:space:]]*#' config.cfg   # the file without its comment lines
```

Without the `-E` in the second line, grep would look for the literal text `TODO|FIXME`.

## 18.12 Templates

**A cheat sheet for the patterns you’ll reuse most often:**

``` python
r"\d+"                  # one or more digits
r"\d{3}-\d{4}"          # 3 digits, dash, 4 digits
r"[A-Za-z]+"            # one or more ASCII letters (misses é, ñ, 李)
r"\s+"                  # a run of whitespace (for splitting or cleanup)
r"^\s+|\s+$"            # leading or trailing whitespace (an alternative to .strip())
r"\b\w+\b"              # whole words
r"[A-Z][a-z]+"          # a capitalized ASCII word
r"#\w+"                 # hashtag
r"@\w+"                 # mention or username
r"\d{4}-\d{2}-\d{2}"    # ISO 8601-style date (shape only, not validation)
r'"[^"]*"'              # a double-quoted phrase that stops at the closing quote
```

## 18.13 Exercises

1.  Write a regex that matches a US phone number written as `(xxx) xxx-xxxx`, `xxx-xxx-xxxx`, or `xxx.xxx.xxxx`. Test it on five variations.
2.  You have a log file with lines like `2024-03-15 14:22:03 ERROR Failed to connect`. Write a regex with capture groups that extracts the date, time, level, and message.
3.  Given a pandas Series of URLs, use `.str.extract` to pull out the domain (the part between `://` and the next `/`).
4.  Write a regex that matches words of 4–7 letters from a block of English text. Use `\b`. Find a short paragraph to test on.
5.  Use `re.sub` to redact credit card numbers from a string, replacing any 16-digit run with `XXXX-XXXX-XXXX-XXXX`.
6.  Using the terminal, run `grep -E` with a regex to find every line in your Python source files that starts with `def` or `class`: a quick index of your code.
7.  Take a regex you find confusing and rewrite it on paper, breaking it into pieces and explaining each. If you can’t, it’s probably too clever, and a simpler approach exists.

## 18.14 One-page checklist

- Use raw strings (`r"..."`) for every Python regex.
- Escape metacharacters you mean literally (`\.`, `\$`), or use `re.escape`.
- Start simple; add complexity only when a test fails.
- Anchor with `\b`, `^`, or `$` when you want exact boundaries.
- Prefer a specific class like `[^"]*` to `.*`, and don’t nest quantifiers.
- Use `re.fullmatch` to validate, `re.search` to find, `re.findall` for all matches, `re.sub` to replace.
- In pandas: `regex=False` for literal text in `.str.contains`, `na=False` for filtering, `regex=True` in `.str.replace`.
- Test on input that should match and input that shouldn’t, and look at the rows that came back empty.
- Moving a pattern to grep, an editor, or a spreadsheet? Check its flavor.
- Reach for a parser (Beautiful Soup, `json`) when the text has structure.

> **NOTE:**
>
> - Python docs, [`re` module reference](https://docs.python.org/3/library/re.html) — the authoritative list of pattern syntax and functions in Python’s regex engine.
> - Python docs, [Regular Expression HOWTO](https://docs.python.org/3/howto/regex.html) — a friendly, longer tutorial that builds intuition before you reach for the reference.
> - Jeffrey Friedl, [*Mastering Regular Expressions*](https://www.oreilly.com/library/view/mastering-regular-expressions/0596528124/) — the standard book on regex internals across languages; worth knowing about when a complex pattern is fighting you.
> - Unicode Consortium, [UTS \#18: Unicode Regular Expressions](https://www.unicode.org/reports/tr18/) — the technical standard for what “regex over Unicode” should mean; useful context for the alphabet question in “Stakes and politics” above.
> - Patrick McKenzie, [Falsehoods Programmers Believe About Names](https://www.kalzumeus.com/2010/06/17/falsehoods-programmers-believe-about-names/) — a short, much-cited list of assumptions about names that validation code gets wrong.
> - Steven Levithan and Jan Goyvaerts, [Regular-Expressions.info](https://www.regular-expressions.info/) — a deep, language-agnostic reference for regex syntax and how the flavors differ.
