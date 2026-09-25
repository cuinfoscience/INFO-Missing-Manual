# 4  Common Text Formats

> **TIP:**
>
> **Prerequisites:** none. This chapter stands on its own.
>
> **See also:** [sec-documentation](#sec-documentation), [sec-data-file-formats](#sec-data-file-formats), [sec-text-editors](#sec-text-editors).

## Purpose

![Running Away Balloon Meme: a balloon labeled ‘CSV’ is running away from a person labeled ‘MD, YAML, JSON’ who are chasing them.](../graphics/memes/common-formats.png)

Here’s a scene that plays out in every class that uses GitHub or Quarto. You open `_quarto.yml` to add one line, a part title for the new section of your project, `- part: Part II: Results`. You save, run `quarto render`, and get `bad indentation of a mapping entry`, with a squiggle under a colon. You didn’t change any indentation. You didn’t touch any code. You added one line to what looks like a plain list, and the message blames something you never did.

If that’s happened to you, you’re not missing some talent everyone else has. You’ve run into a file format that nobody formally taught you, whose rules are simple but strict. (The problem in that line is the second colon: YAML reads `Part II:` as the start of another key. Put the title in quotes and it works.) The same thing happens with the other two formats you meet constantly outside of code: a README that looks fine in your editor and turns into a wall of text on GitHub, or an API response you edited by hand that Python now refuses to read.

This chapter covers those three formats: **Markdown**, the way technical people write for each other; **YAML**, the way tools are configured; and **JSON**, the way programs pass data around. Markdown gets the most space, because you’ll write it every week for the rest of your career. The goal isn’t to make you a format expert. It’s to give you enough fluency to read a config file, write a formatted document, and fix a broken file by reading the error instead of guessing. It doesn’t cover formats for storing datasets, such as CSV and Parquet (that’s [sec-data-file-formats](#sec-data-file-formats)), or what to put *in* a README ([sec-documentation](#sec-documentation)).

## Why read this chapter

- You added one line to a `_quarto.yml` and the build now fails with `bad indentation of a mapping entry`, even though you didn’t change any indentation.
- Your README looks right in your editor’s preview and like a jumble on GitHub (or the other way around), and you can’t tell which one is “correct.”
- You edited one value in a JSON file and Python now says `Expecting property name enclosed in double quotes`, pointing at a line that looks fine.
- You wrote `python_version: 3.10` in a config file and the tool read it as `3.1`, and you’d like to know why a version number turned into a different number.
- Your nested list won’t nest and your line break won’t break, and you’re tired of adding spaces until it works.
- Everyone around you says “it’s just YAML” or “send me the JSON,” and you’d like to know what actually makes a file one or the other.
- You want a single command that tells you exactly which line of a broken config file is wrong.

## Running theme: know the format before you edit the file

Every text file follows some format’s rules, and most of the confusing errors you’ll see come from breaking a rule you didn’t know existed. Take ten seconds to notice which format you’re in (the extension usually tells you) before you start typing.

## 4.1 Markdown

Picture writing a document where you can’t click a Bold button, and all you have is the keyboard. You’d probably invent something like `**this**` for bold, a `#` in front of a heading, and a `-` in front of each list item, and anyone reading the raw file would still understand you. That’s [**Markdown**](https://en.wikipedia.org/wiki/Markdown), a [lightweight markup language](https://en.wikipedia.org/wiki/Lightweight_markup_language) that [John Gruber](https://en.wikipedia.org/wiki/John_Gruber) created in 2004, with [Aaron Swartz](https://en.wikipedia.org/wiki/Aaron_Swartz) as his sounding board on the syntax. Its whole design rests on one idea: a Markdown file should read comfortably as plain text, even if it’s never turned into a web page or PDF. The formatting marks look like what they mean.

That one idea is why Markdown grew from a file format into the way technical people write to each other. Because a Markdown document is plain text, it opens in any editor on any computer (see [sec-text-editors](#sec-text-editors)). Because it’s line-based, version control can show a [diff](https://en.wikipedia.org/wiki/Diff) of exactly which sentences a collaborator changed (see [sec-git-github](#sec-git-github)), which it can’t do with a Word file. And because the text is separate from how it looks, the same source can become a web page, a PDF, or a slide deck without rewriting a word.

### Where you’ll write Markdown

You’re probably already writing Markdown without calling it that. Every repository host shows a project’s `README.md` as its front page (see [sec-documentation](#sec-documentation)), and every GitHub issue, pull request, and code-review comment is Markdown too (see [sec-git-github](#sec-git-github)). The prose between the code cells of a Jupyter notebook lives in [Markdown cells](https://jupyterlab.readthedocs.io/en/stable/user/notebook.html) (see [sec-jupyter](#sec-jupyter)). This book is written in Markdown and rendered by Quarto, and so are plenty of course sites, blogs, and papers. Chat and forum tools such as Slack, Discord, and Discourse accept Markdown or a loose version of it. Note-taking apps like Obsidian and Zettlr store your notes as Markdown files, and [static site generators](https://en.wikipedia.org/wiki/Static_site_generator) such as Jekyll, Hugo, and MkDocs turn a folder of Markdown files into a website.

Since the same handful of rules works in all of those places, an hour spent learning them pays off for years. If you’d like a second walkthrough alongside this one, GitHub’s [beginner’s guide to Markdown](https://github.blog/developer-skills/github/github-for-beginners-getting-started-with-markdown/) is friendly, and the [CommonMark tutorial](https://commonmark.org/help/tutorial/) lets you practice each piece in the browser in about ten minutes.

### Paragraphs and line breaks

This is the first thing that trips almost everyone. You type two lines, press Enter between them, and the rendered page shows them run together on one line. Markdown isn’t ignoring you; it’s following its rule. A paragraph is one or more lines of text with a blank line before and after, and a single newline inside a paragraph is treated as a space:

``` markdown
These two lines
render as one paragraph on one line.

This renders as a second paragraph.
```

The reasoning is that you should be able to wrap your source text however you like without changing the output. When you do want a new line, you almost always want a new paragraph, so leave a blank line. If you truly need a line break *inside* a paragraph (an address, a line of poetry), end the line with a backslash (`\`). You can also end it with two spaces, but trailing spaces are invisible in most editors and easy to delete by accident, so the backslash is kinder to whoever edits the file next. One caution: the backslash form comes from CommonMark (more on that below), and Gruber’s original Markdown doesn’t support it, so a very old renderer shows the backslash itself.

### Headings

Headings start with one or more `#` characters, one per level:

``` markdown
# Heading 1
## Heading 2
### Heading 3
#### Heading 4
```

Use them like an outline, and don’t skip levels: jumping from `##` straight to `####` makes the structure harder to follow, for sighted readers and even more for people using a [screen reader](https://en.wikipedia.org/wiki/Screen_reader), which lets them navigate a page by its headings. Markdown allows six levels (`######`), but most documents never need more than three.

### Emphasis and inline code

``` markdown
*italic text* or _italic text_
**bold text** or __bold text__
***bold and italic***
`inline code`
~~strikethrough~~
```

You’ll see both the asterisk and the underscore forms in the wild. Stick with `*single asterisks*` for italic and `**double asterisks**` for bold. The underscore forms can surprise you inside words: GitHub leaves `file_name_here` alone, but Gruber’s original Markdown turns the middle of it into italics. Asterisks behave the same everywhere. (Strikethrough, the last line above, is an extension that core Markdown doesn’t have; more on that in “Flavors” below.)

Wrap anything that’s code in backticks: a command, a filename, a variable name, a literal value. That’s not decoration. It tells your reader “type exactly this,” and it stops Markdown from reading the underscores and asterisks in `my_var` or `*.csv` as formatting.

### Lists

For a bulleted list, start each line with `-`, `*`, or `+` and a space. Pick one marker and stick with it:

``` markdown
- First item
- Second item
  - Nested item (two spaces, to line up with "Second")
  - Another nested item
- Third item
```

For a numbered list, use a number and a period. The numbers you type mostly don’t matter: renderers number the list themselves, starting from the first number you wrote:

``` markdown
1. First step
2. Second step
3. Third step
```

> **TIP:**
>
> If you write `1.` for every item, you can reorder the list without renumbering anything, and the output still counts 1, 2, 3.

Nesting is where most list frustration lives, and the rule is simpler than it looks: **indent a nested item so its marker lines up with the text of the item above it.** Under `- Second item`, the text starts two characters in, so two spaces work. Under `1. First step`, the text starts three characters in, so you need three spaces. Two spaces under a numbered item isn’t enough, and the “nested” list comes out as a separate list below it. Tabs make this worse, because different editors show a tab as different widths, so indent with spaces.

### Links and images

``` markdown
[link text](https://example.com)
[link text](https://example.com "Optional tooltip")

![Alt text for the image](path/to/image.png)
![Alt text](path/to/image.png "Optional caption")
```

An image’s [alt text](https://en.wikipedia.org/wiki/Alt_attribute) is what a screen reader reads aloud, and what shows up when the image fails to load. “Screenshot” tells that reader nothing; “Error message showing ModuleNotFoundError for pandas” tells them what you wanted them to see. Write it for someone who can’t see the picture.

Link text follows the same logic. Screen-reader users often jump from link to link, hearing only the link text, so a page full of “here” and “click this” is a page of identical, meaningless stops. Make the text name the destination: write `[the pandas documentation](https://pandas.pydata.org/docs/)`, not `click [here](https://pandas.pydata.org/docs/)`.

### Code blocks

For a bit of code inside a sentence, use single backticks: `` `pd.read_csv()` ``. For several lines, use a **fenced code block**: three backticks on the line before and three on the line after. You can add a language name after the opening fence:

```` markdown
```python
import pandas as pd
df = pd.read_csv("data.csv")
print(df.head())
```
````

The language hint (`python`, `bash`, `json`, `yaml`, and so on) isn’t required, but it turns on [syntax highlighting](https://en.wikipedia.org/wiki/Syntax_highlighting) in most renderers and tells your reader what they’re looking at. (Why four backticks around that example? Worked example 1 explains.)

### Blockquotes and horizontal rules

To quote someone, or a passage from documentation, start each line with `>`:

``` markdown
> This is a blockquote.
> It can span multiple lines.
>
> And multiple paragraphs.
```

And to draw a horizontal line across the page, put three or more hyphens, asterisks, or underscores on a line by themselves:

``` markdown
---
```

### Tables

Tables are drawn with pipes and hyphens, and they look almost like the table they produce:

``` markdown
| Column A | Column B | Column C |
|----------|----------|----------|
| Row 1    | Data     | More     |
| Row 2    | Data     | More     |
```

The second line, the row of hyphens, isn’t optional. Leave it out and you get a paragraph full of pipe characters instead of a table. That row is also where you set each column’s alignment, with colons:

``` markdown
| Left   | Center  | Right  |
|:-------|:-------:|-------:|
| text   | text    | text   |
```

> **NOTE:**
>
> Markdown tables get painful past five or six columns, and every edit means re-lining up the pipes (renderers don’t actually require them to line up, but your future self will want them to). For a serious table, generate it from code or keep the data in a CSV and let a tool render it.

### Escaping literal characters

Sooner or later you’ll want a literal asterisk, hash, or underscore, and Markdown will keep turning it into formatting. Put a backslash in front of the character and Markdown shows it as-is:

``` markdown
\*not italic\*     <- renders with visible asterisks, no italics
\# not a heading   <- renders as a literal hash at the start of a line
2\. not a list     <- renders as "2." without starting an ordered list
```

The characters you might need to escape are `` \ ` * _ { } [ ] ( ) # + - . ! ``, but only where they’d otherwise trigger formatting. A `#` in the middle of a sentence or a `.` after a word is already safe.

### Flavors: CommonMark, GFM, and friends

Here’s a frustration that isn’t your fault. You write a README, check it in your editor’s preview, and it looks right. You push it, and GitHub shows something different. Or it’s fine on GitHub and broken in Quarto. You go looking for your typo, and there isn’t one.

Gruber’s original description of Markdown was short and deliberately informal, which left many details open: how far to indent a nested list, what happens when emphasis markers overlap, whether a heading needs a blank line before it. Every tool that adopted Markdown filled those gaps its own way, and the dialects drifted apart. That history explains a fact that will otherwise drive you up the wall: **the same Markdown file can render differently in different tools, and each tool is following its own rules correctly.**

Two names anchor the landscape today. **[CommonMark](https://commonmark.org/)**, first released in 2014, is a precise, community-maintained standard with a test suite, and it’s the base most modern renderers build on. **GitHub Flavored Markdown (GFM)** is CommonMark plus the extensions you’ll use constantly on GitHub: tables, strikethrough, URLs that become links on their own, and task lists. [GitHub’s formatting guide](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) is the friendliest tour of it. [Task lists](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-tasklists) are the one to know about:

``` markdown
- [x] Clean the data
- [ ] Run the analysis
- [ ] Write it up
```

In an issue or pull request, those become real checkboxes that your teammates can tick off without editing the text.

Other tools add their own layers. Quarto, which renders this book, builds on [Pandoc’s Markdown](https://pandoc.org/MANUAL.html#pandocs-markdown) and adds callouts, citations, and cross-references (its [Markdown basics page](https://quarto.org/docs/authoring/markdown-basics.html) is the place to look them up). MDN’s documentation project uses GFM plus its own house rules (see Further reading). And chat tools like Slack support only a loose subset.

Here’s a concrete case of the drift, and one that bites Quarto users. This source has no blank lines:

``` markdown
Some text
# Heading
- item one
- item two
```

GitHub, following CommonMark, renders a paragraph, a heading, and a two-item list. [Pandoc requires a blank line before a heading](https://pandoc.org/MANUAL.html#extension-blank_before_header) and before a list that follows a paragraph, so Quarto renders all four lines as a single paragraph: `Some text # Heading - item one - item two`. Neither is broken. They disagree. A few habits keep you out of trouble:

**Preview where your readers will read.** A README is read on GitHub, so check it on GitHub, not only in your editor.

**Stay near the core when a document travels.** Headings, emphasis, lists, links, and fenced code blocks work everywhere. Tables, task lists, strikethrough, and footnotes are extensions that some tools don’t support.

**Put blank lines around every heading, list, and code block.** Tools that don’t need them don’t mind them, and tools that need them won’t work without them.

**When something renders oddly, suspect a flavor difference** before you assume you made a typo.

### When Markdown renders wrong

Most Markdown problems come down to a short list of symptoms, and each has a quick fix:

- **A heading or list shows up as plain text.** Add a blank line before it. Quarto (through Pandoc) requires one; GitHub doesn’t, which is why the same file can work in one and not the other.
- **Two lines you typed separately run together.** A single newline is a space. Leave a blank line for a new paragraph, or end the line with `\` for a line break.
- **A nested list won’t nest.** Line the nested marker up with the text of the item above: two spaces under `-`, three under `1.`. Use spaces, not tabs.
- **Code shows up without colors.** Add a language hint after the opening fence (```` ```python ````).
- **The source is hard to read because of HTML tags.** Markdown allows inline HTML, but you rarely need it, and mixing the two makes the file harder for the next person to edit.
- **A table or checkbox works on GitHub but not somewhere else.** Tables, task lists, and footnotes are extensions, not core Markdown. If the document has to travel between tools, stick to the core.

If you want more hands-on practice, [markdown.org](https://markdown.org/) has a guide to the basics and the common extensions, a cheat sheet, and online editors that preview as you type, and the [w3schools.io Markdown introduction](https://www.w3schools.io/file/markdown-introduction/) walks through the syntax step by step.

## 4.2 YAML

Sooner or later, a tool asks you to configure it by editing a text file, and that file is usually YAML. Quarto reads `_quarto.yml`; [GitHub Actions](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax) reads the files in `.github/workflows/`; conda builds an environment from an [`environment.yml`](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html#creating-an-environment-from-an-environment-yml-file); Docker Compose reads `docker-compose.yml`. These are [configuration files](https://en.wikipedia.org/wiki/Configuration_file): text that tells a program what to do, written by people and read by the program.

[**YAML**](https://en.wikipedia.org/wiki/YAML) originally stood for “Yet Another Markup Language.” Its designers soon renamed it to the joke-within-a-name “YAML Ain’t Markup Language,” to make the point that it’s for data, not documents. Technically it’s a [serialization](https://en.wikipedia.org/wiki/Serialization) format: a way to write nested data (settings, lists, lists of settings) as text and read it back. Its big design choice is to show structure with indentation instead of brackets. That makes it pleasant to read and unforgiving to edit, because a misplaced space changes the meaning of the file. Most YAML frustration comes from that trade-off, so it’s worth learning the handful of rules that matter.

### Key-value pairs

The basic unit of YAML is a key, a colon, a space, and a value:

``` yaml
name: Brian Keegan
university: University of Colorado Boulder
year: 2026
```

> **WARNING:**
>
> The space after the colon is what makes it a key. Without it, YAML doesn’t see a key at all: `name:Brian` on its own is read as the single piece of text `"name:Brian"`. Inside a file of other keys, it usually stops the parser with `could not find expected ':'`, pointing at the line *after* the one you need to fix.

### Nesting with indentation

YAML shows that one setting belongs inside another by indenting it. Here, `type`, `output-dir`, and `resources` all belong to `project`:

``` yaml
project:
  type: book
  output-dir: _book
  resources:
    - graphics/**
```

The usual indent is two spaces per level. What matters most is that items at the same level line up exactly: if `type` is indented two spaces, `output-dir` must be too. One space off and the parser either stops with an error (PyYAML, Python’s YAML library, says `mapping values are not allowed here`) or, worse, quietly reads the file with a different structure than you meant.

**YAML doesn’t allow tabs for indentation.** If a tab sneaks in, you get an error like `found character '\t' that cannot start any token`, which is technically accurate and not much help if you don’t know that `\t` means a tab. The fix is always to replace the tab with spaces, and the lasting fix is to set your editor to insert spaces when you press the Tab key (see [sec-text-editors](#sec-text-editors)).

### Lists (sequences)

YAML calls a list a *sequence*. It’s a series of lines that each start with a dash and a space:

``` yaml
fruits:
  - apple
  - banana
  - cherry
```

The space after the dash matters here too: `-apple` is read as text that happens to start with a hyphen, not as a list item. For short lists you can also write everything on one line, in square brackets:

``` yaml
fruits: [apple, banana, cherry]
```

### Nested structures

Keys and lists combine freely: a list of items that each have their own keys, which hold their own lists. Here’s the shape of a Quarto book’s chapter list:

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

Read it from the outside in. `chapters` holds a list with two items (the two dashes at the same indent). Each item has a `part` key and its own `chapters` list. Notice that the part titles are in quotes. These two would work without them, but a title with a colon in it, like the `Part II: Results` from the start of this chapter, would not, and quoting every title is a habit that saves you from ever finding out which ones need it.

### Strings, numbers, and booleans

You never tell YAML what type a value is. It guesses from how the value looks:

``` yaml
name: Alice          # string
count: 42            # integer
ratio: 3.14          # float
active: true         # boolean
nothing: null        # null
```

Usually the guess is right, and that’s convenient. Sometimes it’s wrong in a way that doesn’t raise any error at all, which is much worse. `3.10` looks like a number, so YAML reads it as the number 3.1, and your Python version quietly becomes a different version. `yes`, `no`, `on`, and `off` look like answers, and under the older YAML 1.1 rules, which [PyYAML](https://pyyaml.org/wiki/PyYAML) and many other tools still follow, they’re read as the booleans `true` and `false` (the full list is on [yaml.org](https://yaml.org/type/bool.html)). And a ZIP code with a leading zero, `02134`, comes back from PyYAML as the number 1116, because YAML 1.1 reads a leading zero as [octal](https://en.wikipedia.org/wiki/Octal). You can watch it happen in Python:

``` python
import yaml

print(yaml.safe_load("python_version: 3.10"))  # {'python_version': 3.1}
print(yaml.safe_load("answer: yes"))           # {'answer': True}
print(yaml.safe_load("zip: 02134"))            # {'zip': 1116}
```

The fix for all of these is the same: when a value should be text, put it in quotes.

``` yaml
python_version: "3.10"    # string, not float
answer: "yes"             # string, not boolean
zip: "02134"              # string, not a number
```

> **WARNING:**
>
> The `3.10`-becomes-`3.1` trap is one of the most common YAML bugs in Python projects, and it gets more common as Python versions reach two digits after the dot. Whenever you write a version number in YAML, quote it.

### Multi-line strings

Sometimes a value is a whole paragraph: a description, a message, a short script. YAML gives you two ways to write one across several lines:

``` yaml
# Literal block (keeps the line breaks)
description: |
  This is a multi-line string.
  Each newline is preserved exactly.
  Indentation within the block is relative.

# Folded block (joins the lines with spaces)
summary: >
  This is a multi-line string
  that gets folded into a single
  paragraph when parsed.
```

The `|` (pipe) keeps every line break, which is what you want for a script or a poem. The `>` (greater-than) folds the lines into one paragraph, which is what you want for a long sentence you’ve wrapped to keep the file readable. You’ll see `|` constantly in GitHub Actions workflows, where the `run:` step is often a small shell script.

### Comments

A `#` starts a comment, and everything from there to the end of the line is ignored:

``` yaml
# This is a full-line comment
name: Alice  # This is an inline comment
```

Use comments generously in config files. The person who wonders in six months why a setting is there will probably be you.

### Common YAML mistakes

When a YAML file won’t load, it’s almost always one of these:

- **A tab instead of spaces.** YAML forbids tabs for indentation. Set your editor to insert spaces (see [sec-text-editors](#sec-text-editors)).
- **Items at the same level that don’t line up.** Siblings must start in exactly the same column. Different blocks can use different indent sizes, but two spaces everywhere is easiest to keep straight.
- **No space after a colon or dash.** `key:value` and `-item` are read as plain text, not as a key or a list item.
- **A colon followed by a space inside an unquoted value.** `title: Part II: Results` fails. Quarto calls it `bad indentation of a mapping entry` and PyYAML calls it `mapping values are not allowed here`: two tools, two wordings, one mistake. Quote the value.
- **Unquoted values that look like another type.** `version: 3.10` becomes `3.1`, `enabled: yes` becomes `true`, `zip: 02134` becomes a number. When in doubt, quote it.
- **Keys with different capitalization.** YAML is case-sensitive, so `Title` and `title` are two different keys, and a tool looking for one won’t see the other. For booleans, stick with lowercase `true` and `false`, which every parser reads the same way.

## 4.3 JSON

If you’ve ever looked at what comes back from a web API, you’ve seen JSON. [**JSON**](../chapters/appendix-glossary.llms.md#term-json) ([JavaScript Object Notation](https://en.wikipedia.org/wiki/JSON)) is how programs pass data to each other: it’s what web APIs send (see [sec-http-apis](#sec-http-apis)), what many tools use for settings files, and even what a Jupyter notebook is underneath. Open an `.ipynb` file in a plain text editor and you’ll find every cell, output, and setting stored as JSON, in a [documented format](https://nbformat.readthedocs.io/en/latest/format_description.html).

JSON is much stricter than YAML or Markdown. There’s exactly one way to write each thing, no guessing about types, and no tolerance for small slips. That makes it excellent for programs, which never make typos and love certainty, and a bit frustrating for people editing it by hand. The good news is that the whole language fits on one page (the [json.org](https://www.json.org/json-en.html) home page draws all of it as diagrams), and MDN’s [JSON tutorial](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Scripting/JSON) walks through reading and writing it.

### Objects

A JSON **object** is a set of key-value pairs wrapped in curly braces, with commas between the pairs. Keys must be text in double quotes:

``` json
{
  "name": "Brian Keegan",
  "university": "University of Colorado Boulder",
  "year": 2026
}
```

If you know Python, this looks almost exactly like a dictionary, and when Python reads it, a dictionary is what you get.

### Arrays

An **array** is an ordered list of values in square brackets, like a Python list:

``` json
{
  "fruits": ["apple", "banana", "cherry"]
}
```

### Nesting

Objects and arrays nest inside each other just as YAML’s keys and lists do. Here’s the same chapter list from the YAML section, written as JSON:

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

Compare the two versions and you can see the trade: JSON spells out every level with brackets, so it’s longer and noisier, but there’s no indentation rule to get wrong. The indentation here is only for human eyes; JSON would read the same file squashed onto one line.

### Data types

JSON has exactly six kinds of values, and nothing else:

| Type    | Example            |
|---------|--------------------|
| String  | `"hello"`          |
| Number  | `42`, `3.14`       |
| Boolean | `true`, `false`    |
| Null    | `null`             |
| Object  | `{"key": "value"}` |
| Array   | `[1, 2, 3]`        |

Strings always use double quotes; single quotes aren’t valid JSON. And `true`, `false`, and `null` are always lowercase, which catches Python users who are used to typing `True`, `False`, and `None`.

### No comments

This one surprises everybody: JSON has no comments. Not `#`, not `//`, nothing. That was a deliberate choice, since JSON was meant for data passed between programs, not for files people annotate. Some tools bend the rule anyway. VS Code’s `settings.json` is really [JSON with Comments](https://code.visualstudio.com/docs/languages/json#_json-with-comments) (often called JSONC), which allows `//` and `/* */` comments. But a standard JSON parser, including Python’s, rejects any file that contains them, so a comment copied from a settings file into a data file will break it.

If you need to leave a note in real JSON, the usual workaround is an extra key that the program ignores:

``` json
{
  "_comment": "This file configures the development server",
  "port": 8080,
  "debug": true
}
```

### Common JSON mistakes

Nearly every broken JSON file you’ll meet has one of these problems:

- **A trailing comma.** JSON doesn’t allow a comma after the last item: `{"a": 1, "b": 2,}` is invalid. Python lists and dictionaries allow it, which is exactly why it’s so easy to type.
- **Single quotes.** `{'name': 'Alice'}` is a Python dictionary, not JSON. Use double quotes: `{"name": "Alice"}`.
- **Unquoted keys.** `{name: "Alice"}` works in JavaScript, not in JSON. Keys need quotes: `{"name": "Alice"}`.
- **A missing comma between items.** Easy to do when you add a line at the end. The error points at the line *after* the missing comma.
- **Comments.** Standard JSON has none. If a parser rejects your file, look for stray `//` or `#` lines.
- **Missing or extra brackets.** In deeply nested data it’s easy to lose track of a closing `}` or `]`. An editor with brace matching highlights each bracket’s partner (see [sec-text-editors](#sec-text-editors)), and a validator (next section) tells you where the count goes wrong.

## 4.4 When to use which format

You’ll rarely get to choose a format from scratch, since most tools decide for you, but knowing why each exists helps you guess what a file is for before you open it.

Use **Markdown** for documents that people read: README files, documentation, issue descriptions, notes. It’s readable as raw text and rendered nicely almost everywhere, including GitHub, GitLab, and Jupyter. Use **YAML** for configuration that people edit, such as Quarto projects, GitHub Actions workflows, and conda environments, because it’s easy on the eyes and, unlike JSON, it allows comments explaining each setting. Use **JSON** for data that programs exchange, above all API responses, because it’s strict, unambiguous, and every programming language can read it. Some tools also use JSON for their settings files (VS Code, Jupyter, npm), because the tool expects it and the strict syntax leaves nothing ambiguous. And for storing a dataset you plan to analyze, use none of these: CSV, Parquet, or a database is the right tool, as [sec-data-file-formats](#sec-data-file-formats) explains.

The rough rule of thumb: **Markdown is for documents people read, YAML is for settings people edit, and JSON is for data programs exchange.** You’ll find exceptions (plenty of tools keep settings in JSON, and some pipelines pass data around as YAML), but the rule gets you most of the way.

## 4.5 Validating files

When a YAML or JSON file breaks, the error message from the tool that tried to read it (Quarto, GitHub Actions, your script) is often vague, or buried in a longer error. Instead of staring at the file, ask a validator. It reads the file on its own and tells you the exact line and column where the rules broke.

**For JSON, you already have one.** Python’s [`json.tool`](https://docs.python.org/3/library/json.html#module-json.tool) module, part of the standard library, checks a file and pretty-prints it:

``` bash
python -m json.tool myfile.json
```

If the file is valid, you get it back, neatly indented. If it isn’t, you get one line naming the first problem and where it is, such as `Expecting ',' delimiter: line 5 column 3 (char 84)`. It stops at the first error, so fix that one and run it again until the file comes back clean.

**For YAML, install [yamllint](https://yamllint.readthedocs.io/en/stable/quickstart.html):**

``` bash
pip install yamllint
yamllint myfile.yml
```

It reports syntax errors with a line and column, and it also flags style issues. Don’t let the style warnings rattle you. The first one you’ll likely see is `missing document start "---"`, which only means the file doesn’t begin with the optional `---` line; it isn’t an error. If you only care about real problems, run `yamllint -d relaxed myfile.yml`, which uses a more forgiving set of rules. If you’d rather not install anything and PyYAML is already in your environment, this one-liner loads the file and prints a traceback only if it can’t:

``` bash
python -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" myfile.yml
```

**Online validators** work too; search for “JSON validator” or “YAML validator.” Just think before you paste: config files often hold API keys or passwords (see [sec-secrets](#sec-secrets)), and anything you paste into a website has left your computer.

> **TIP:**
>
> Many editors (VS Code, Sublime Text, JetBrains IDEs) check JSON and YAML as you type, built in or through a plugin. If you see a red squiggly underline in a config file, the editor is already telling you where the problem is.

## 4.6 Stakes and politics

Say you’re configuring a survey that runs in five countries, listed by their two-letter [country codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2): `countries: [DE, FR, GB, NO, SE]`. Load that file with PyYAML and you get back `['DE', 'FR', 'GB', False, 'SE']`. Under YAML 1.1, `NO` is one of the ways to spell false, so Norway quietly becomes a boolean. Developers call it [the Norway problem](https://hitchdev.com/strictyaml/why/implicit-typing-removed/), and it’s the same trap as `yes` and `3.10` above, landing on a country.

Nobody set out to drop Norway from anyone’s data. Years earlier, someone decided which words a parser should treat as English answers rather than as data, and the cost of that choice fell on whatever happened to collide with the list. YAML 1.2 dropped the rule in 2009, but widely used parsers still follow the older one, so the default you get depends on the library someone else picked.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: when a format guesses what your values mean, ask whose words and names its guesses were built around, and quote the values it might get wrong.

## 4.7 Worked examples

### 1. Writing a project README in Markdown

You’ve just started a class project analyzing campus dining data, and your teammates need to know how to get it running. Here’s a README that tells them:

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

Notice how much of this chapter it uses: headings to break it into sections a teammate can jump to, a numbered list for steps that happen in order, backticks around every command and path, and a fenced code block, with a language hint, for commands to run.

Notice the fences around the example, too. Because the README contains its own triple-backtick code block, the whole example is wrapped in a *four*-backtick fence. A fenced code block only ends at a fence at least as long as the one that opened it, so the inner ```` ``` ```` lines stay inside the example instead of ending it early. You’ll need the same trick whenever you write documentation *about* Markdown.

### 2. Reading a Quarto YAML config

Here’s a snippet from a `_quarto.yml`. Before reading the explanation below it, try describing its structure yourself:

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

The top-level key `book` holds three keys, `title`, `author`, and `chapters`, which you can tell belong together because they’re indented the same amount. `chapters` holds a list with two items, marked by the two dashes at the same indent. The first item is just a filename, `index.qmd`. The second item is itself a small set of keys: a `part` title and its own nested `chapters` list, holding `intro.qmd` and `methods.qmd`. If you added a third chapter to Part I, its dash would need to line up with `- intro.qmd`. Line it up with `- part:` instead and it becomes a third item in the outer list, so the chapter lands after Part I instead of inside it, with no error to warn you. (Quarto’s guide to [project files](https://quarto.org/docs/projects/quarto-projects.html) has more on what goes in `_quarto.yml`.)

### 3. Fixing a broken JSON file

A classmate sends you this file, and it won’t load. It’s broken on purpose here, with three separate mistakes, so it’s marked as plain text rather than JSON:

``` text
{
  'name': 'dining_data',
  "columns": ["date", "hall", "count",],
  "rows": 1500
  "source": "CU Dining Services"
}
```

Rather than hunting by eye, save it as `broken.json` and let the validator find the problems one at a time:

``` bash
python -m json.tool broken.json
```

``` text
Expecting property name enclosed in double quotes: line 2 column 3 (char 4)
```

Line 2, column 3 is the `'` before `name`. **Replace the single quotes** around `name` and `dining_data` with double quotes and run it again:

``` text
Illegal trailing comma before end of array: line 3 column 38 (char 64)
```

That’s the comma after `"count"`. **Delete the trailing comma** and run it again. (Python versions before 3.13 describe this one less helpfully, as `Expecting value: line 3 column 39`, but they point at the same spot.)

``` text
Expecting ',' delimiter: line 5 column 3 (char 84)
```

This one points at line 5, but nothing is wrong with line 5. The parser finished `"rows": 1500` on line 4, expected a comma, and only noticed it was missing when it reached the next key. **Add the comma at the end of line 4.** Run the validator once more, and this time it prints the whole file back, neatly indented, instead of an error. That means it’s valid. Here’s the corrected file:

``` json
{
  "name": "dining_data",
  "columns": ["date", "hall", "count"],
  "rows": 1500,
  "source": "CU Dining Services"
}
```

Three errors, three runs, and you never had to guess. That last lesson carries over to almost every parser you’ll use: when an error points at a line that looks fine, look at the end of the line *before* it.

## 4.8 Exercises

1.  Write a Markdown document with at least one heading, one ordered list, one unordered list, one code block, and one link. Render it on GitHub or in a Markdown previewer and confirm it looks the way you meant.

2.  Add a table and a task list to your document from exercise 1. Preview it in two different renderers, for example your editor’s Markdown preview and a GitHub gist. Note any differences between the two, and work out which of the features you used are GFM extensions rather than core Markdown.

3.  Open a `_quarto.yml` or `environment.yml` file from one of your class projects. Find every key-value pair, every list, and every nested structure, and draw the file’s tree structure on paper.

4.  Find a public JSON API (for example, `https://api.github.com/users/octocat`) and look at the response. Find the objects, arrays, strings, numbers, booleans, and nulls in it.

5.  Break a valid JSON file on purpose, three different ways: one trailing comma, one single-quoted string, and one missing comma. Run `python -m json.tool` after each and read the error message. Which messages pointed straight at the problem, and which pointed somewhere else?

6.  Convert this YAML to equivalent JSON by hand, then check your JSON with `python -m json.tool`:

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

7.  Find a Markdown document (a GitHub README, a Jupyter notebook, or a Quarto file) that uses at least three different formatting features. Name each feature and explain what it does.

## 4.9 One-page checklist

- **Markdown:** headings with `#`, emphasis with `*` and `**`, code with backticks, lists with `-` or `1.`, links with `[text](url)`, images with `![alt](path)`. A blank line separates paragraphs; a single newline is just a space.
- **Markdown layout:** blank lines around every heading, list, and code block; nested list markers lined up with the text of the item above (two spaces under `-`, three under `1.`).
- **Markdown flavors:** the core works everywhere; tables, task lists (`- [ ]`), strikethrough, and footnotes are extensions. Preview your document where your readers will read it.
- **YAML:** `key: value` with a space after the colon, indentation with spaces only (never tabs), siblings lined up in the same column, lists with `- item`, comments with `#`.
- **YAML types:** quote anything that should stay text but looks like a number, boolean, or date: version numbers, `yes`/`no`, ZIP codes, values containing a colon.
- **JSON:** objects with `{}`, arrays with `[]`, double quotes around every key and string, lowercase `true`/`false`/`null`, no trailing commas, no comments.
- **When in doubt, validate:** `python -m json.tool` for JSON, `yamllint` for YAML, a previewer for Markdown. If the error points at a line that looks fine, check the line before it.
- **Know which format you’re editing** before you start typing. The extension (`.md`, `.yml` or `.yaml`, `.json`) tells you.

## 4.10 Quick reference: syntax at a glance

| Feature   | Markdown            | YAML            | JSON             |
|-----------|---------------------|-----------------|------------------|
| Key-value | n/a                 | `key: value`    | `"key": "value"` |
| List      | `- item`, `1. item` | `- item`        | `["item"]`       |
| Nesting   | heading levels      | indents         | brackets         |
| Comments  | n/a                 | `# note`        | none             |
| Quoting   | n/a                 | when ambiguous  | always `"…"`     |
| Boolean   | n/a                 | `true`, `false` | `true`, `false`  |
| Extension | `.md`               | `.yml`, `.yaml` | `.json`          |

> **NOTE:**
>
> - John Gruber, [Markdown: Basics](https://daringfireball.net/projects/markdown/basics) — the creator’s own introduction; short, and the clearest statement of the readable-as-plain-text idea behind the whole format.
> - [CommonMark Spec](https://spec.commonmark.org/) — the community-maintained Markdown standard, and the place to settle what “Markdown” should mean when two renderers disagree.
> - [GitHub Flavored Markdown spec](https://github.github.com/gfm/) — the extensions GitHub adds on top of CommonMark (tables, task lists, autolinks); the dialect most readers will see your READMEs in.
> - MDN, [How to write in Markdown](https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Howto/Markdown_in_MDN) — a worked example of how a large documentation project pins down its house dialect and style rules.
> - [YAML 1.2 specification](https://yaml.org/spec/1.2.2/) — the official YAML spec; dense, but the place to settle arguments about quoting and indentation.
> - IETF, [RFC 8259: The JavaScript Object Notation (JSON) Data Interchange Format](https://datatracker.ietf.org/doc/html/rfc8259) — the official JSON spec; short and surprisingly readable.
> - Tom Preston-Werner, [TOML specification](https://toml.io/en/) — a fourth format you’ll meet in Python packaging (`pyproject.toml`) and Rust tooling; worth knowing about for when YAML feels too loose and JSON too strict.
