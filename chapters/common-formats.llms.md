# 4  Common Text Formats

> **TIP:**
>
> **Prerequisites:** none. This chapter stands on its own.
>
> **See also:** [sec-documentation](#sec-documentation), [sec-data-file-formats](#sec-data-file-formats), [sec-text-editors](#sec-text-editors).

## Purpose

![Running Away Balloon Meme: a balloon labeled ‘CSV’ is running away from a person labeled ‘MD, YAML, JSON’ who are chasing them.](../graphics/memes/common-formats.png)

Before you write your first function, before you open your first dataset, you will encounter configuration files, README documents, and structured data exchanges that are written in formats you are expected to read and edit — but that nobody explicitly teaches you. A `README.md` is Markdown. A `_quarto.yml` or `.github/workflows/build.yml` is YAML. An API response is almost certainly JSON. If you cannot read or edit these formats confidently, you will spend time debugging invisible whitespace errors, misplaced colons, and mismatched brackets instead of doing the work you actually care about.

This chapter introduces the syntax of the three text formats you will encounter most often outside of code itself: **Markdown**, **YAML**, and **JSON**. Markdown gets the deepest treatment because it is more than a file format — it is the default way technical people write *for each other*: READMEs, issues, notebooks, documentation, and this very book. The goal is not to make you a format expert. It is to give you enough fluency to read a config file, write a formatted document, and troubleshoot a broken file without guessing.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Explain why Markdown became the default writing style of technical communication, and name the contexts where you will use it.
2.  Write a Markdown document with headings, lists, links, images, code blocks, and emphasis.
3.  Recognize the major Markdown flavors (original, CommonMark, GitHub Flavored Markdown) and explain why the same file can render differently in different tools.
4.  Read and write a YAML configuration file, including nested keys, lists, and multi-line strings.
5.  Read and write a JSON object, including nested structures and arrays.
6.  Identify common syntax errors in each format and fix them.
7.  Explain when each format is typically used and why.
8.  Validate a YAML or JSON file using a command-line tool or online validator.

## Running theme: know the format before you edit the file

Every file has a format. If you edit it without understanding that format’s rules, you will break things in ways the error messages will not explain well. Learn to recognize which format you are looking at before you start changing things.

## 4.1 Markdown

**Markdown** is a lightweight markup language for writing formatted text using plain characters. John Gruber created it in 2004, with feedback on the syntax from Aaron Swartz, around a single design goal: a Markdown document should be publishable as-is, as plain text, without looking like it has been marked up with tags or formatting instructions. The formatting markers look like what they mean. A heading starts with `#`. A list item starts with `-` or `1.`. Bold text is wrapped in `**`. Even if the file is never rendered into a web page or PDF, a human can read it comfortably.

That design goal is why Markdown outgrew being “a file format” and became a *communication style*. When you write in Markdown you are making a small set of commitments that pay off later: your document is plain text, so it opens in any editor on any machine (see [sec-text-editors](#sec-text-editors)); it diffs line-by-line under version control, so collaborators can see exactly what changed (see [sec-git-github](#sec-git-github)); and it separates content from presentation, so the same source can render as a web page, a PDF, or a slide deck without rewriting a word.

### Where you will write Markdown

Markdown is the lingua franca of technical writing. You will use it — sometimes without realizing it — in:

- **README files and project documentation.** Every repository host renders `README.md` as the project’s front page (see [sec-documentation](#sec-documentation)).
- **GitHub issues, pull requests, and comments.** Bug reports, code reviews, and discussion threads are all written in Markdown (see [sec-git-github](#sec-git-github)).
- **Jupyter notebook text cells.** The prose between your code cells is Markdown (see [sec-jupyter](#sec-jupyter)).
- **Quarto and other publishing systems.** This book is written in Markdown; so are many course sites, blogs, and papers.
- **Chat and forums.** Slack, Discord, and Discourse accept Markdown or a Markdown-like subset for formatting messages.
- **Note-taking apps and static site generators.** Obsidian and Zettlr store notes as Markdown files; Jekyll, Hugo, and MkDocs turn folders of Markdown into websites.

Because the same skill transfers across all of these, the hour you spend learning Markdown syntax repays itself for the rest of your career. GitHub’s [beginner’s guide to Markdown](https://github.blog/developer-skills/github/github-for-beginners-getting-started-with-markdown/) is a good complement to this section if you want a second walkthrough.

### Paragraphs and line breaks

A paragraph is one or more consecutive lines of text, separated from other content by a blank line. A single newline inside a paragraph is *not* a line break — most renderers join the lines with a space:

``` markdown
These two lines
render as one paragraph on one line.

This renders as a second paragraph.
```

To force a line break *without* starting a new paragraph, end a line with two or more spaces, or with a backslash. Because trailing spaces are invisible in most editors, prefer the backslash form — or just use separate paragraphs.

### Headings

Headings use one or more `#` characters at the start of a line:

``` markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```

Use headings hierarchically. Do not skip levels — going from `##` to `####` without a `###` in between confuses readers and screen readers alike. Most tools render up to six levels (`######`), but three is usually enough.

### Emphasis and inline formatting

``` markdown
*italic text* or _italic text_
**bold text** or __bold text__
***bold and italic***
`inline code`
~~strikethrough~~
```

Convention in technical writing: use `*single asterisks*` for italic and `**double asterisks**` for bold. The underscore variants (`_` and `__`) can cause problems inside words and inside filenames, so the asterisk form is safer.

Use `backticks` for anything that is code, a command, a filename, a variable name, or a literal value. This is not optional decoration — it signals to the reader that the text is meant to be taken literally.

### Lists

**Unordered lists** use `-`, `*`, or `+` as bullet markers. Pick one and be consistent:

``` markdown
- First item
- Second item
  - Nested item (indent two spaces)
  - Another nested item
- Third item
```

**Ordered lists** use numbers followed by a period. The actual numbers do not matter to most renderers — they auto-number from whatever you start with:

``` markdown
1. First step
2. Second step
3. Third step
```

> **TIP:**
>
> If you always write `1.` for every item, reordering the list never requires renumbering. Most renderers handle this correctly, though some strict parsers expect sequential numbers.

### Links and images

``` markdown
[link text](https://example.com)
[link text](https://example.com "Optional tooltip")

![Alt text for the image](path/to/image.png)
![Alt text](path/to/image.png "Optional caption")
```

Always write meaningful alt text for images. “Screenshot” is not meaningful. “Error message showing ModuleNotFoundError for pandas” is.

The same accessibility rule applies to link text. Screen readers can jump from link to link, so a page full of links labeled “here” and “click this” is unnavigable. Make the link text describe the destination: write `[the pandas documentation](https://pandas.pydata.org/docs/)`, not `click [here](https://pandas.pydata.org/docs/)`.

### Code blocks

For inline code, use single backticks: `` `pd.read_csv()` ``.

For multi-line code blocks, use triple backticks (a “fenced code block”) with an optional language hint for syntax highlighting:

```` markdown
```python
import pandas as pd
df = pd.read_csv("data.csv")
print(df.head())
```
````

The language hint (`python`, `bash`, `json`, `yaml`, etc.) is not required, but it activates syntax highlighting in most renderers and helps the reader understand what they are looking at.

### Blockquotes

Prefix lines with `>`:

``` markdown
> This is a blockquote.
> It can span multiple lines.
>
> And multiple paragraphs.
```

### Horizontal rules

Three or more hyphens, asterisks, or underscores on a line by themselves:

``` markdown
---
```

### Tables

Markdown tables use pipes and hyphens:

``` markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Data     | More     |
```

The alignment row (the `|---|` line) is required. You can control column alignment with colons:

``` markdown
| Left   | Center  | Right  |
|:-------|:-------:|-------:|
| text   | text    | text   |
```

> **NOTE:**
>
> Markdown tables are painful for anything beyond five or six columns. If you need a serious table, consider generating it from code or using a CSV file and a rendering tool.

### Escaping literal characters

Sometimes you want a literal `*`, `#`, or `_` in your text without it being interpreted as formatting. Put a backslash in front of it:

``` markdown
\*not italic\*     <- renders with visible asterisks, no italics
\# not a heading   <- renders as a literal hash at the start of a line
2\. not a list     <- renders as "2." without starting an ordered list
```

The characters that may need escaping are `` \ ` * _ { } [ ] ( ) # + - . ! ``. You rarely need to escape all of them — only when the character would otherwise trigger formatting in that position.

### Flavors: CommonMark, GFM, and friends

Gruber’s original 2004 spec was short and deliberately informal, which left many details ambiguous — how deeply to indent a nested list, what happens when emphasis markers overlap, and so on. Every tool that adopted Markdown filled those gaps its own way, and the dialects drifted apart. The [history of that drift](https://en.wikipedia.org/wiki/Markdown) explains a fact that will otherwise surprise you: **the same Markdown file can render differently in different tools, and both renderings are “correct.”**

Two names anchor the landscape today:

- **CommonMark** is the community-maintained standard, first published in 2014. It nails down the ambiguities in the original spec and is the base most modern renderers build on.

- **GitHub Flavored Markdown (GFM)** is CommonMark plus a set of extensions you will use constantly on GitHub: tables, strikethrough, autolinked URLs, and task lists:

  ``` markdown
  - [x] Clean the data
  - [ ] Run the analysis
  - [ ] Write it up
  ```

  Task lists render as real checkboxes in issues and pull requests, and collaborators can tick them off without editing the file.

Beyond those two, tools layer on their own conventions: MDN’s documentation project uses GFM plus site-specific extensions and publishes its house rules (see Further reading), Quarto (which renders this book) adds callouts, citations, and cross-references on top of Pandoc’s Markdown, and chat tools like Slack support only a loose subset.

Three practical consequences:

1.  **Preview where your readers will read.** A document destined for GitHub should be previewed on GitHub, not just in your editor.
2.  **Stay near the core when a document travels.** Headings, emphasis, lists, links, and fenced code blocks work everywhere; tables and task lists do not.
3.  **When something renders oddly, suspect a flavor difference** before assuming you made a typo.

### Common Markdown mistakes

1.  **No blank line before a list or heading.** Most renderers require a blank line before a heading or list to recognize it. Without the blank line, the heading or list may be rendered as plain text.
2.  **Expecting a single newline to be a line break.** Inside a paragraph, one newline is joined into a space by most renderers. Use a blank line for a new paragraph, or a trailing backslash for a forced break.
3.  **Inconsistent indentation in nested lists.** Use exactly two or four spaces (pick one) for each nesting level. Tabs can cause unpredictable behavior.
4.  **Forgetting the language hint on code blocks.** The code will still render, but without syntax highlighting it is harder to read.
5.  **Using HTML when Markdown would suffice.** Markdown supports inline HTML, but mixing the two makes the source harder to read and is unnecessary for most formatting.
6.  **Assuming every renderer supports your flavor.** Tables, task lists, and footnotes are extensions, not core Markdown. If a document must travel across tools, stick to the shared core.

If you want hands-on practice, [markdown.org](https://markdown.org/) collects tutorials and live-preview playgrounds, and the [W3Schools Markdown introduction](https://www.w3schools.io/file/markdown-introduction/) offers a step-by-step tour with exercises.

## 4.2 YAML

**YAML** (originally “Yet Another Markup Language,” now recursively “YAML Ain’t Markup Language”) is a human-readable data serialization format. You will encounter it in configuration files for tools like Quarto (`_quarto.yml`), GitHub Actions (`.github/workflows/*.yml`), conda (`environment.yml`), Docker Compose (`docker-compose.yml`), and many others.

YAML’s design philosophy is readability. It uses indentation instead of brackets, which makes it pleasant to read but unforgiving about whitespace.

### Key-value pairs

The basic unit of YAML is a key-value pair, separated by a colon and a space:

``` yaml
name: Brian Keegan
university: University of Colorado Boulder
year: 2026
```

> **WARNING:**
>
> The space after the colon is mandatory. `name:Brian` is not valid YAML. `name: Brian` is.

### Nesting (indentation)

YAML uses indentation to represent structure. Child keys are indented under their parent:

``` yaml
project:
  type: book
  output-dir: _book
  resources:
    - graphics/**
```

The standard indentation is two spaces per level. **Tabs are not allowed in YAML.** If you mix tabs and spaces, you will get a parse error that says something unhelpful like `found character '\t' that cannot start any token`. The fix is always: replace tabs with spaces.

### Lists (sequences)

Lists are written with a leading dash and a space:

``` yaml
fruits:
  - apple
  - banana
  - cherry
```

You can also write short lists inline using square brackets:

``` yaml
fruits: [apple, banana, cherry]
```

### Nested structures

YAML composes freely — you can nest maps inside lists, lists inside maps, and so on:

``` yaml
chapters:
  - part: "Part I — Practice"
    chapters:
      - questions.qmd
      - documentation.qmd
  - part: "Part II — Environment"
    chapters:
      - operating-system.qmd
      - file-system.qmd
```

### Strings, numbers, and booleans

YAML infers types from values:

``` yaml
name: Alice          # string
count: 42            # integer
ratio: 3.14          # float
active: true         # boolean
nothing: null        # null
```

This type inference can surprise you. The value `yes` is interpreted as a boolean `true` in YAML 1.1 (which many tools still use). The value `3.10` is interpreted as the float `3.1`, not the string `"3.10"`. If you need a literal string, wrap it in quotes:

``` yaml
python_version: "3.10"    # string, not float
answer: "yes"             # string, not boolean
```

> **WARNING:**
>
> The `3.10` vs `3.1` trap is one of the most common YAML bugs in Python configuration files. If you are specifying a Python version, *always* quote it.

### Multi-line strings

YAML has two multi-line string operators:

``` yaml
# Literal block (preserves newlines)
description: |
  This is a multi-line string.
  Each newline is preserved exactly.
  Indentation within the block is relative.

# Folded block (joins lines with spaces)
summary: >
  This is a multi-line string
  that gets folded into a single
  paragraph when parsed.
```

The `|` (pipe) preserves line breaks. The `>` (greater-than) folds them into spaces. Both are useful; pick the one that matches what the consuming tool expects.

### Comments

Comments start with `#` and continue to the end of the line:

``` yaml
# This is a full-line comment
name: Alice  # This is an inline comment
```

### Common YAML mistakes

1.  **Tabs instead of spaces.** YAML forbids tabs for indentation. Configure your text editor to insert spaces when you press Tab (see [sec-text-editors](#sec-text-editors)).
2.  **Inconsistent indentation.** If one block uses two-space indent and another uses four, the parser may reject the file or misinterpret the structure.
3.  **Missing space after colon.** `key:value` is invalid. `key: value` is correct.
4.  **Unquoted strings that look like other types.** `version: 3.10` becomes `3.1`. `enabled: yes` becomes `true`. When in doubt, quote it.
5.  **Forgetting that YAML is case-sensitive.** `True` and `true` may behave differently depending on the parser version. Stick with lowercase `true` and `false`.

## 4.3 JSON

[**JSON**](../chapters/appendix-glossary.llms.md#term-json) (JavaScript Object Notation) is a lightweight data interchange format. It is the default language of web APIs, configuration files for tools like VS Code and Jupyter, and many data pipelines. If you have ever looked at the output of a web API call, you were almost certainly looking at JSON.

JSON is stricter than YAML and Markdown. It has a rigid syntax with no room for ambiguity, which makes it excellent for machine-to-machine communication and frustrating to write by hand.

### Objects (key-value pairs)

A JSON object is a set of key-value pairs wrapped in curly braces. Keys must be double-quoted strings:

``` json
{
  "name": "Brian Keegan",
  "university": "University of Colorado Boulder",
  "year": 2026
}
```

### Arrays (lists)

Arrays are ordered lists wrapped in square brackets:

``` json
{
  "fruits": ["apple", "banana", "cherry"]
}
```

### Nesting

JSON composes the same way YAML does — objects inside arrays, arrays inside objects:

``` json
{
  "chapters": [
    {
      "part": "Part I — Practice",
      "files": ["questions.qmd", "documentation.qmd"]
    },
    {
      "part": "Part II — Environment",
      "files": ["operating-system.qmd", "file-system.qmd"]
    }
  ]
}
```

### Data types

JSON supports six types:

| Type    | Example            |
|---------|--------------------|
| String  | `"hello"`          |
| Number  | `42`, `3.14`       |
| Boolean | `true`, `false`    |
| Null    | `null`             |
| Object  | `{"key": "value"}` |
| Array   | `[1, 2, 3]`        |

Note: JSON strings must use double quotes. Single quotes are not valid JSON.

### No comments

JSON does not support comments. This is a deliberate design choice — JSON is a data interchange format, not a configuration language. Some tools (like VS Code’s `settings.json`) extend JSON with comment support (called “JSONC” or “JSON with Comments”), but standard JSON parsers will reject any file containing `//` or `/* */`.

If you need to annotate a JSON file, the conventional workaround is to add a key like `"_comment"`:

``` json
{
  "_comment": "This file configures the development server",
  "port": 8080,
  "debug": true
}
```

### Common JSON mistakes

1.  **Trailing commas.** JSON does not allow a comma after the last item in an object or array. `{"a": 1, "b": 2,}` is invalid. Remove the final comma.
2.  **Single quotes.** `{'name': 'Alice'}` is not valid JSON. Use double quotes: `{"name": "Alice"}`.
3.  **Unquoted keys.** `{name: "Alice"}` is not valid JSON. Keys must be quoted: `{"name": "Alice"}`.
4.  **Comments.** Standard JSON does not support comments. If a parser rejects your file, check for stray `//` or `#` lines.
5.  **Missing or extra brackets.** With deeply nested structures, it is easy to lose track of closing `}` and `]`. Use an editor with bracket matching (see [sec-text-editors](#sec-text-editors)) or a JSON validator.

## 4.4 When to use which format

| Situation | Format | Why |
|----|----|----|
| Documentation, README files, issue descriptions | Markdown | Human-readable, universally rendered on GitHub, GitLab, Jupyter |
| Configuration files (Quarto, GitHub Actions, conda) | YAML | Human-readable, supports comments, widely adopted for config |
| API responses and data interchange | JSON | Strict, unambiguous, universal parser support in every language |
| Settings files (VS Code, Jupyter, npm) | JSON | Tooling expects it; strict syntax prevents ambiguity |
| Data storage for analysis | Neither — use CSV, Parquet, or a database | See [sec-data-file-formats](#sec-data-file-formats) |

The rough heuristic: **Markdown** is for documents humans read. **YAML** is for configuration humans edit. **JSON** is for data machines exchange. There is overlap — some tools use JSON for config, some use YAML for data — but the heuristic holds most of the time.

## 4.5 Validating files

When a YAML or JSON file is broken, the error messages are often cryptic. A linter or validator can point you to the exact line.

**JSON validation from the command line:**

``` bash
# Python's json module doubles as a validator
python -m json.tool myfile.json
```

If the file is valid, this prints the pretty-printed JSON. If it is invalid, it prints an error with a line number.

**YAML validation from the command line:**

``` bash
# Install yamllint (pip install yamllint)
yamllint myfile.yml
```

`yamllint` checks for syntax errors, indentation inconsistencies, and style issues.

**Online validators** are also available for quick checks — search for “JSON validator” or “YAML validator.” Be careful about pasting sensitive configuration (API keys, passwords) into online tools.

> **TIP:**
>
> Many text editors (VS Code, Sublime Text, JetBrains IDEs) have built-in or plugin-based validation for JSON and YAML. If you see red squiggly underlines, the editor is already telling you something is wrong.

## 4.6 Stakes and politics

Markdown, YAML, and JSON look like neutral plumbing — and most of the time they are. The political dimension shows up in two specific places. First, *who maintains the spec*. Markdown was designed by a single individual in 2004 and only acquired a community-driven standard (CommonMark) a decade later; until then, “Markdown” meant whatever the dominant renderers — overwhelmingly run by US tech companies — happened to do, which is why two correct-looking documents can render differently on GitHub and in a Jupyter notebook. YAML and JSON have governance bodies, but the popular subsets and edge cases are still adjudicated by whoever ships the most-used parser. Second, *which character sets and reading directions count*. JSON requires Unicode, but tooling built on top of it routinely assumes ASCII filenames, English-language keys, and left-to-right rendering; right-to-left scripts and combining marks still trip layouts and search indexes in 2026. None of this prevents you from using these formats. It does mean that “the file format” is rarely as universal as the spec suggests.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt: when you choose a format for a config file or data interchange, ask whose tools were assumed when the spec was written, and whether your reader’s tools share that assumption.

## 4.7 Worked examples

### 1. Writing a project README in Markdown

You have just started a class project analyzing campus dining data. Write a README that a teammate can follow:

```` markdown
# Campus Dining Analysis

Analysis of CU Boulder dining hall traffic patterns for INFO 2301.

## Setup

1. Clone this repository.
2. Create a virtual environment: `python -m venv .venv`
3. Activate it: `source .venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`

## Data

The raw data is in `data/raw/dining_traffic.csv` (not tracked in git).
Download it from the shared Google Drive link in the project doc.

## Usage

```bash
python scripts/clean_data.py
python scripts/analyze.py
```

## Team

- **Alice** — data cleaning
- **Bob** — visualization
- **Carol** — statistical analysis
````

Note the fences: because the README itself contains a triple-backtick code block, the example above is wrapped in a *four*-backtick fence. A fenced code block can only be closed by a fence at least as long as the one that opened it, so the inner ```` ``` ```` marks stay inside the example instead of ending it early.

### 2. Reading a Quarto YAML config

Given this snippet from a `_quarto.yml`:

``` yaml
book:
  title: "My Project"
  author: "Alice"
  chapters:
    - index.qmd
    - part: "Part I"
      chapters:
        - intro.qmd
        - methods.qmd
```

You can read this as: the top-level key `book` contains three child keys — `title`, `author`, and `chapters`. The `chapters` key contains a list. The first item is a simple string (`index.qmd`). The second item is itself a map with a `part` key and a nested `chapters` list.

### 3. Fixing a broken JSON file

You receive this JSON from a classmate and it will not parse:

``` text
{
  'name': 'dining_data',
  "columns": ["date", "hall", "count",],
  "rows": 1500
  "source": "CU Dining Services"
}
```

There are three errors:

1.  `'name'` and `'dining_data'` use single quotes — change to double quotes.
2.  `["date", "hall", "count",]` has a trailing comma — remove the comma after `"count"`.
3.  The line `"rows": 1500` is missing a comma before the next key — add a comma at the end.

After fixing all three, the corrected file is:

``` json
{
  "name": "dining_data",
  "columns": ["date", "hall", "count"],
  "rows": 1500,
  "source": "CU Dining Services"
}
```

## 4.8 Exercises

1.  Write a Markdown document with at least one heading, one ordered list, one unordered list, one code block, and one link. Render it on GitHub or in a Markdown previewer and confirm it looks correct.

2.  Take the document from exercise 1 and add a table and a task list. Preview it in two different renderers — for example, your editor’s Markdown preview and a GitHub gist. Note any differences in how the two render it, and identify which of the features you used are GFM extensions rather than core Markdown.

3.  Open a `_quarto.yml` or `environment.yml` file from one of your class projects. Identify every key-value pair, every list, and every nested structure. Draw the tree structure on paper.

4.  Find a public JSON API (for example, `https://api.github.com/users/octocat`) and examine the response. Identify the objects, arrays, strings, numbers, booleans, and nulls in the output.

5.  Deliberately introduce three different errors into a valid JSON file (one trailing comma, one single-quoted string, one missing comma). Use `python -m json.tool` to see the error messages. Note how helpful (or unhelpful) each message is.

6.  Convert the following YAML to equivalent JSON by hand, then validate your JSON with `python -m json.tool`:

    ``` yaml
    project:
      name: "analysis"
      version: "1.0"
      dependencies:
        - pandas
        - numpy
        - matplotlib
      settings:
        debug: true
        output_dir: results
    ```

7.  Find a Markdown document (a GitHub README, a Jupyter notebook, or a Quarto file) that uses at least three different formatting features. Identify each feature and explain what it does.

## 4.9 One-page checklist

- **Markdown:** headings with `#`, emphasis with `*` and `**`, code with backticks, lists with `-` or `1.`, links with `[text](url)`, images with `![alt](path)`. Blank lines separate paragraphs; a single newline is not a line break.
- **Markdown flavors:** core syntax works everywhere; tables, task lists (`- [ ]`), and strikethrough are GFM extensions. Preview your document where your readers will read it.
- **YAML:** key-value pairs with `key: value` (space after colon is mandatory), indentation with spaces only (no tabs), lists with `- item`, comments with `#`, quote strings that look like numbers or booleans.
- **JSON:** objects with `{}`, arrays with `[]`, keys are double-quoted strings, no trailing commas, no comments, no single quotes.
- **When in doubt, validate.** Use `python -m json.tool` for JSON, `yamllint` for YAML, and a Markdown previewer for Markdown.
- **Know which format you are editing** before you start typing. The file extension (`.md`, `.yml`/`.yaml`, `.json`) tells you.

## 4.10 Quick reference: syntax at a glance

| Feature | Markdown | YAML | JSON |
|----|----|----|----|
| Key-value pair | N/A (not a data format) | `key: value` | `"key": "value"` |
| List | `- item` or `1. item` | `- item` | `["item"]` |
| Nesting | Heading levels (`#`, `##`) | Indentation (spaces) | Curly/square brackets |
| Comments | N/A (rendered, not data) | `# comment` | Not supported |
| String quoting | Not applicable | Optional (required for ambiguous values) | Always double quotes |
| Boolean | N/A | `true` / `false` | `true` / `false` |
| Common extension | `.md` | `.yml` or `.yaml` | `.json` |

> **NOTE:**
>
> - John Gruber, [Markdown: Basics](https://daringfireball.net/projects/markdown/basics) — the creator’s own introduction; short, and the clearest statement of the readable-as-plain-text design philosophy.
> - [CommonMark Spec](https://spec.commonmark.org/) — the community-maintained Markdown standard. The reference for what “Markdown” should mean across renderers.
> - [GitHub Flavored Markdown spec](https://github.github.com/gfm/) — extensions GitHub adds on top of CommonMark (tables, task lists, autolinks); the dialect most readers will see your docs in.
> - MDN, [How to write in Markdown](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Howto/Markdown_in_MDN) — a worked example of how a large documentation project pins down its house dialect and style rules.
> - [YAML 1.2 specification](https://yaml.org/spec/1.2.2/) — the official YAML spec; dense, but the place to settle arguments about quoting and indentation.
> - IETF, [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://datatracker.ietf.org/doc/html/rfc8259) — the canonical JSON spec; short and surprisingly readable.
> - Tom Preston-Werner, [TOML specification](https://toml.io/en/) — a fourth format you will encounter in Python packaging (`pyproject.toml`) and Rust tooling; useful to know exists when YAML feels too loose and JSON too strict.
