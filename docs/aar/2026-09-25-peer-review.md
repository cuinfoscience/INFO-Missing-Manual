# Peer review of the whole book, September 2026

**What this is.** Ten reviews of *The Missing Manual for Information Scientists*, written on 2026-09-25, right after the voice rewrite (#61–#68). **They are simulated.** Each was written by an AI agent playing a fictional persona, at the maintainer's request, to stress-test the book from the perspectives of the fields it serves before a revision. The personas are not real people, and the reviews are not endorsements or real peer review. The plan built from them is [`plans/2026-09-25-peer-review-revisions.md`](../plans/2026-09-25-peer-review-revisions.md).

**How they were made.** Every agent got the same brief: read `AGENTS.md`'s overview and style guide, the introduction, and its persona's primary chapters in full; skim the "Why read this chapter" bullets and headings of every other chapter; then write 300–600 words, in the book's own conversational voice, that are mostly generative critique (what to add, cut, restructure, or rethink, tied to named chapters and sections), with at most a sentence or two of praise. Each agent checked its claims about the book by grepping the chapters, and edited nothing.

**Who reviewed what.** Three reviewers from computer science education, three from library and information science, two from the quantitative social sciences, and two from project management. Between them, every chapter, both appendices, the introduction, and the conclusion were read in full by at least one reviewer, and every reviewer also commented on the book as a whole.

| # | Persona | Field | Primary chapters |
|---|---|---|---|
| 1 | Dana Okafor, community-college CS1 instructor | CS education | operating-system, file-system, terminal, text-editors, debugging, tracebacks |
| 2 | Priya Raman, computing-education researcher | CS education | introduction, questions, documentation, reading-docs, regex, conclusion; exercises and checklists book-wide |
| 3 | Marco Delgado, coding-workshop instructor for researchers | CS education | package-management, virtual-environments, jupyter, scripting, linting, remote |
| 4 | Helen Park, research data management librarian | Library and information science | data-file-formats, tabular-data, project-management, secrets, glossary |
| 5 | Tomás Rivera, teaching and learning librarian | Library and information science | reading-scholarship, writing-manuscripts, writing-thesis, ai-llm, AI disclosure |
| 6 | Aisha Bello, digital humanities librarian and archivist | Library and information science | common-formats, latex, presenting, artifacts-have-politics; every Stakes section |
| 7 | Jordan Whitfield, computational social scientist | Quantitative social sciences | pandas-basics, sql-basics, http-apis, evaluating-ai |
| 8 | Ruth Lindqvist, quantitative methods professor (sociology) | Quantitative social sciences | llm-internals, ai-agents, evaluating-ai; tabular-data's validation |
| 9 | Sam Nakamura, research-lab project manager | Project management | project-management, version-control, collaboration, automation |
| 10 | Grace Mensah, technical program manager, nonprofit data team | Project management | version-control, collaboration, automation, secrets, remote |

**Editor's notes.** The reviews are reproduced as written. Before using them, the maintainer's agent re-checked their claims against the book; one needs a correction. Review 9 says IRB "comes up exactly once in the whole book"; it appears in four chapters (`ai-llm`, `jupyter`, `remote`, and `writing-thesis`), though none of them explains what an IRB review involves or how long it takes, which is the reviewer's real point. Other book-wide claims were confirmed: no chapter mentions plagiarism, installs Python from python.org, shows PowerShell's "is not recognized" error, or names the FAIR principles.

---

## Review 1: Dana Okafor, community-college CS1 instructor

*Primary chapters: operating-system, file-system, terminal, text-editors, debugging, tracebacks*

I'd hand Part II to my students tomorrow, so read this as notes from someone who wants to use it.

Start with the order. My students' first three weeks are: get Python running, open a terminal, find their file, read their first red text. The sidebar spans everything from `terminal` to `writing-thesis`, and puts Markdown and YAML (`common-formats`) ahead of all of that. It also puts `debugging` in Part I with `@sec-terminal`, a Part II chapter, as its prerequisite, while `tracebacks` lists `debugging` as *its* prerequisite. Flip those two: tracebacks is the half-hour skill ("It's short on purpose"), and debugging is the discipline built on it. Then add a "first programming course" path to the Outline in `index.qmd`: file-system, terminal, text-editors, virtual-environments, tracebacks.

The biggest gap: the book never installs Python. `package-management` opens with conda versus pip, and the only install help is a Real Python link in its Further reading. Nobody meets the python.org installer's "Add python.exe to PATH" checkbox, which is behind a lot of the week-one `python` failures I see. A short "Getting a Python" section, one route per operating system plus a check that it worked, would save me a lecture.

Next, Windows readers are treated as translators. The terminal chapter's "Common errors and what they mean" shows `zsh: command not found`, but my students get PowerShell's "is not recognized as the name of a cmdlet," which appears nowhere in the book. Show both. Chromebooks come up once, in "Stakes and politics," as people the defaults leave out. That's honest, but it doesn't help them: point them to ChromeOS's Linux environment, or bless the Codespaces route `jupyter` already covers.

Two of the most common novice terminal moments are missing. `terminal` never says Ctrl+C stops a runaway command, and nothing separates the shell prompt from Python's `>>>`. Every semester someone types `pip install pandas` at `>>>`, gets a `SyntaxError`, and can't find the way out. A "which prompt am I at?" box would fix that, and the SyntaxError entry in `tracebacks` could name the case.

`debugging` reads like a data-science chapter. It opens on a pandas `KeyError`, its MRE technique depends on `StringIO` and `read_csv`, and its error-families table leaves out `SyntaxError` and `IndentationError`, which are most of what a week-two student sees. Put a pure-Python bug (a loop, a list) before the pandas ones. Then think about splitting the chapter: the loop, labeled prints, and `breakpoint()` early; logging, pytest, and `git bisect` later.

The same `FileNotFoundError` on `data/input.csv` gets a full walkthrough three times: file-system's "Diagnosing 'file not found'", terminal's "Diagnosing a 'file not found' error", and debugging's "'File not found' that is really 'wrong folder'". Keep the one in `file-system` and link to it from the other two. In `text-editors`, I'd trade the Emacs survival set and the IDE refactoring section for the week-one VS Code trap: the Run button uses whichever interpreter VS Code picked, which may not be the one your terminal runs. Link to "VS Code and venvs" in `virtual-environments` from the write-run-read loop.

Last, the exercises. Debugging's "Take a recent error you ran into" assumes a new student has a stock of errors, and the backup worked example begins "Suppose you've just bought a 1 TB external drive," which many of my students can't afford. Ship a starter project with broken files built in (the chapters already share `~/Courses/INFO-3010/Project`), and give the backup section a free route. And present the "At CU Boulder" callouts as a template other schools fill in, so instructors elsewhere know to swap them out.


---

## Review 2: Priya Raman, computing-education researcher

*Primary chapters: index, questions, documentation, reading-docs, regex, conclusion*

The "Why read this chapter" bullets are good motivation because they start from a real situation, so keep them. My worry is the other end of each chapter. The book teaches well through worked examples, but it gives readers almost nothing to check what they learned.

Start with the exercises. There are roughly 240 of them, and I found only about three that ask the reader to predict before running anything (sql-basics: "write down how many rows it should return"). Many assume material a novice doesn't have yet: "a bug you ran into this week" (questions), "a confusing error you've run into" (documentation), "a regex you find confusing" (regex). A dozen need a classmate, and none come with answers. In a course, every instructor has to write their own. Give each chapter two or three predict-then-run items, with answers in a collapsed callout. Regex is the obvious place to start. Hand readers the `notes` Series from "Extracting order IDs" and ask what `.str.extract(r"Order #(\d+)")` returns for row 3 before they run it. Then ship one small practice repository that the whole book uses, so every "your own" exercise has a fallback.

Next, fade the scaffolding. Questions walks through three fully rewritten questions, then jumps straight to "rewrite three vague questions." Put a half-finished one in between, say a draft with Goal and Actual filled in and Expected and Context left blank for the reader. Documentation's "Weak"/"Better" troubleshooting pair could use the same middle step.

Then turn repetition into retrieval. Diátaxis is taught in full twice: once in documentation's "Documentation genres and the questions they answer" and again in reading-docs' "The four genres of documentation." Documentation also covers finding, reading, and version-matching docs, which reading-docs does better; let reading-docs own reading, and make documentation a writing chapter. Along the same lines, `sys.executable` shows up in nine chapters. "Which Python is actually running?" is the book's threshold concept, so name it once in the introduction. Wherever it comes back, have the chapter ask the reader to recall it instead of explaining it again.

The prerequisite callouts also disagree with the sidebar order. Debugging, in Part I, lists terminal, in Part II, as a prerequisite. Regex lists only scripting, yet its "Regex in pandas" section and first worked example run on pandas `.str` methods, and pandas-basics doesn't come until Part IV. Tabular-data uses `pd.to_numeric` and `.dt` throughout, while pandas-basics, which comes *after* it, lists tabular-data as its own prerequisite. An instructor assigning chapters in sidebar order hits all of these. I'd put pandas-basics before tabular-data, move regex into Part IV after pandas-basics (and add pandas-basics to its prerequisites), and add two or three suggested reading paths for instructors to the introduction's Outline, such as a first-two-weeks path for a data course.

Transfer needs explicit threads that link the chapters. The introduction spends a whole section on computational thinking's four skills, and they never appear again. The conclusion's takeaways ("See before you act," "Check before you trust") are exactly the threads that would help readers see what the chapters have in common, but only terminal's running theme uses one of those phrases. Tie each running theme to one takeaway, so the conclusion collects threads readers already know, or cut the computational-thinking section.

Finally, the checklists. About a dozen chapters (questions, documentation, terminal) write their one-page checklists as first-person statements ("I can tell whether I need reference docs…"). Reading-docs and regex use commands instead. Put every checklist in the "I can…" form; that brings back assessable outcomes at the end of each chapter without restoring the learning objectives you dropped from the front.


---

## Review 3: Marco Delgado, workshop instructor and trainer for hands-on coding workshops for researchers

*Primary chapters: package-management, virtual-environments, jupyter, scripting, linting, remote*

Keep the `sys.executable` check, repeated everywhere; it's the single move that rescues most workshop setups. But Part III never commits to one setup path. `package-management` says use conda if your course hands you an environment file, and its Template C calls conda "(preferred)"; `virtual-environments` says "For most projects, **start with `venv`**"; `uv` appears only in a meme and Further reading. And nowhere does the book show how to install Python itself: there's a Real Python link at the bottom of `package-management`, and that's it. That's where I lose a third of the room on day one. Pick one default (I'd say python.org or uv plus `.venv`, with conda as a labeled detour for GDAL- and CUDA-type needs), put it in a short "Day zero" setup appendix every chapter can point to, and if you reject uv, say why in a paragraph.

Next, cut the repetition. Creating and activating a venv, `python -m pip`, the `where.exe` warning, and registering a Jupyter kernel are each taught in full in two or three chapters, and the prerequisites form a loop: `virtual-environments` requires `@sec-pkg-mgmt`, which defers to `virtual-environments` for "what a venv actually is on disk." Put `virtual-environments` first as the what-and-why, and shrink `package-management`'s "Working with venv and pip" to a pointer so that chapter can own conflicts, pins, and conda. The same goes for `jupyter` and `scripting`: both tell the Pimentel 2019 story in Stakes, both walk through `nbconvert`'s `get_ipython()` output, and "When to move from notebooks to scripts (and back)" duplicates "Notebook or script? Choosing on purpose." Keep one copy, in `scripting`. `jupyter` runs 859 lines, and "Finding what's slow: measure, then profile" is excellent but misplaced; its `cProfile` example is already a script, `clean.py`, so it belongs in `scripting` or `debugging`.

`jupyter` is JupyterLab-only. VS Code appears once, inside the Codespaces discussion, yet many of my learners run notebooks in VS Code, where the kernel picker has its own traps; `virtual-environments` gives it one paragraph, and `jupyter` needs its own. In `linting`, teach `ruff` alone: the checklist already says "Prefer `ruff format` over `black`," so the `black` section and `jupyter-black` can shrink to a sidebar.

`remote` has a sequencing problem. It sits in Part II with only `@sec-terminal` as a prerequisite, but its worked examples activate a `.venv` and tunnel to JupyterLab. Its Slurm script runs `module load python/3.11` and then `source ~/projects/sales/.venv/bin/activate` without saying that venv must be built on the cluster, from that module's Python. That's the first cluster failure I'd bet on. Move it to the end of Part III, or add the prerequisites and a "build your environment on the server" step.

For live coding, the examples hop between `housing-audit`, `term-project`, `~/Courses/INFO-3010/Project`, and `sales-project`. Instructors want one project that carries from chapter to chapter, and `scripting`'s `sales-project` (with `src/sales/` and `paths.py`, which `jupyter` already imports) is the obvious one. Small inconsistencies bite copy-pasters too: `scripting` uses bare `pip install -e .` and `pip install -r requirements.txt` right after other chapters insist on `python -m pip`, and the Python version drifts between 3.12 (conda examples) and 3.11 (Dockerfile, ruff `target-version`, the cluster module).

Across the whole book, the "Why read this chapter" bullets in all seven parts read like real learner complaints, which is exactly right for a reference. A Day zero appendix would serve the data chapters in Part IV and the automation work in Part VI as much as Part III.


---

## Review 4: Helen Park, research data management librarian at a university library

*Primary chapters: data-file-formats, tabular-data, project-management, secrets, appendix-glossary*

Keep "Data dictionary and codebook" in `project-management` as it is. A dictionary that `check_data.py` tests against is better than what I hand most grad students. My main critique is that the book's data lifecycle stops too early. `project-management` has four phases (plan, build, verify, deliver), and "deliver" ends when the memo is handed in. The book never covers licensing your outputs, writing a README for someone who will reuse the data, depositing it somewhere that assigns a DOI, or deciding what to keep and what to destroy.

The pieces for this are already in the book, just not connected. `file-system` warns that CU deletes your files "approximately 90 days" after graduation. `version-control` says in one sentence that Zenodo can give a release a DOI. `writing-thesis` puts "IRB submission if needed" in week 5 and "deposit" in week 12, but it never mentions a data management plan. I'd close `project-management` with a section like "Share, archive, and let go" to pull them together. It would cover LICENSE files (CC0 or CC BY for data, MIT for code), CITATION.cff, a dataset README, and how institutional repositories, Zenodo, OSF, and ICPSR compare. FAIR would work as a one-paragraph frame; that acronym isn't in the book yet.

The provenance note asks for "four things," but not the dataset's version, its persistent identifier, or how to cite it. The example records `license: CC-BY 4.0` without saying what a license lets you do, and that decides whether `data/raw/` can go in a public repository. "Data files over a few megabytes, which belong in external storage" should name *which* storage.

"Sensitive data" is a single paragraph and needs more. Students need to know that IRB protocols, consent forms, and data use agreements limit where data can live. They need de-identification in practice: direct versus indirect identifiers, and a linking key stored apart from the data. They also need FERPA, which the book mentions only in `ai-llm` and `questions`. `secrets` names "a lab's human-subjects survey" in its Stakes section, but "What if I already leaked a secret?" only covers keys. You can rotate a key, but you can't rotate a participant's identity. Add a parallel section on leaked personal data that says who to tell (the PI, the IRB, campus security).

In `data-file-formats`, the checklist line "Use Parquet for intermediate files and anything over ~100 MB" is right for working files and wrong for archiving. "When not to use Parquet" should add sharing and preservation, where open formats like UTF-8 CSV plus a data dictionary are the safer choice. The chapter also skips Stata, SPSS, and SAS files, which are what social-science students download from ICPSR. `pd.read_stata` keeps value labels, so the file carries part of its own codebook.

`tabular-data` says "Write down which rows you removed and *why*," but no template shows where that record goes. Have the pipeline write a row-count log, and document the *processed* data's derived variables, since that's the file a reuser actually gets.

The glossary's 39 terms leave out the stewardship vocabulary the chapters use: provenance, metadata, license, DOI, checksum, personal data, de-identification. Git, API, and environment variable are missing too. Add a "repository" entry that separates a Git repository, a data repository, and the "university's repository" from the Open access entry. Also, 12 terms (CLI, terminal, pip, YAML, version, and others) are never linked from any chapter. Either link them on first use or cut them.


---

## Review 5: Tomás Rivera, teaching and learning librarian

*Primary chapters: reading-scholarship, writing-manuscripts, writing-thesis, ai-llm, appendix-ai-disclosure*

Keep "Getting a copy without paying for it" and the retraction check in "Is this paper any good?" exactly as they are. Those are the pages I'd hand my own workshop students. Most of what follows is about what's missing around them.

**Reading-scholarship never teaches searching.** The chapter goes straight from triage to getting a copy, and then to citation chaining in "Synthesis." It never shows how to find the first paper. Add a section on searching on purpose: which database fits which field (ACM Digital Library, Scopus, JSTOR, LISTA), keywords versus subject terms, one Boolean example, and a search log. The title also promises "Books," but books only come up in passing, through interlibrary loan. Either add a short section on reading a monograph or drop the word. And librarians appear only twice in the book, both times as people to ask about predatory venues. We also do research consultations, and the literature-map and thesis-proposal sections should say so.

**Nothing in the book covers quoting, paraphrasing, or plagiarism.** A search for "plagiar" returns nothing in any chapter. Most student plagiarism I see isn't intentional: the student's notes don't show which lines were copied from the source. The reading-note template has "Quotes worth keeping" but no place for a page number. Add a locator field, and a rule to keep quotation marks on anything copied. Give writing-manuscripts a section on quoting, paraphrasing, and citation style, including text recycling, since its reader is often turning a class paper or thesis chapter into a paper. The Zotero worked example is all Better BibTeX. Most social-science and humanities students write in Word or Google Docs, so add the word-processor plugin and how to choose APA or Chicago.

**Ai-llm is a coding chapter with an integrity section attached.** Its one sample disclosure is about a README and unit tests, and the "Why read" bullet about an invented source gets just one exercise. Students need a research-and-writing path through the chapter: AI search and summary tools and what they get wrong, how APA, MLA, and Chicago say to cite AI output, and AI detectors, whose false positives fall hardest on second-language writers. Keeping drafts and version history (@sec-git-github) is the best defense against a false positive. Writing-thesis never mentions AI at all, though graduate schools increasingly have thesis policies.

**The disclosure appendix contradicts itself.** "What the AI was *not* asked to do" says claims about authors and papers stayed out of AI hands. The section just before it reports finding "invented references, including a Further reading item whose authors didn't exist." Readers will notice, so reconcile the two. The appendix also claims the human authors' voice while listing itself among the parts Claude drafted. Its "Checklist for your own work" should ask for tool versions, dates, and whether prompts were kept. Replace "use your library" in its reading list with real sources, such as COPE's position statement on AI and authorship.

**Across the book,** evaluating sources is scattered. Questions covers Stack Overflow, reading-docs has "When a blog post is wrong," reading-scholarship covers peer review, and evaluating-ai covers AI output, but none of them link to the others. Cross-link them with a shared "who says so, and how do they know?" prompt. Also close one loop. Writing-manuscripts promises "a replication-ready code and data release" but never says how to make one. Point to version-control's Zenodo DOIs, and add a data-availability statement to the submission checklist.


---

## Review 6: Aisha Bello, digital humanities librarian and archivist

*Primary chapters: common-formats, latex, presenting, artifacts-have-politics*

The book says it's for humanities students, but I looked for mine (encoding letters in TEI, cleaning OCR, citing a box and folder) and mostly didn't find them. Every running example is empirical social computing: Reddit civility, difference-in-differences, campus dining traffic. Pick one humanities thread, say a small collection of digitized letters, and carry it through `common-formats`, `regex`, and `data-file-formats`.

**common-formats.** For my students, the format they meet constantly outside of code is XML: TEI, EAD finding aids, MODS and Dublin Core records, EPUB, OAI-PMH harvests. The book mentions XML only in asides (what's inside a `.docx`, a launchd plist). A short XML section (elements versus attributes, well-formed versus valid, `xmllint --noout` in "Validating files") would fit the chapter's shape. Then there's non-Latin text: `json.dumps({"name": "José 李"})` writes `"Jos\u00e9 \u674e"` unless you pass `ensure_ascii=False`, and PyYAML's `safe_dump` escapes the same string unless you pass `allow_unicode=True`. That belongs beside the Norway problem, the best Stakes opening of these four. And "When to use which format" could ask how long a file needs to last, pointing to the Library of Congress's Sustainability of Digital Formats site.

**latex.** Put `José 李 مرحبا` into this chapter's first document and pdfLaTeX, Overleaf's default compiler, stops with `! LaTeX Error: Unicode character 李 (U+674E) not set up for use with LaTeX.` That error isn't in "Reading LaTeX errors without panicking," and the book never mentions `fontspec`, `babel`, or `polyglossia`. XeLaTeX and LuaLaTeX come up only as fixes for a stubborn journal template or for `metropolis`'s Fira fonts. A student writing about Arabic poetry needs a paragraph on switching compilers and loading a font that has the script. The bibliography section is written for ACM and IEEE. Add `biblatex-chicago` for notes-bibliography style, and a sample entry for an archival source. The tagged-PDF Stakes section is excellent; put its `\DocumentMetadata` line in the Templates too, so the good default is the one people copy.

**presenting.** "Why a talk isn't a paper read aloud" holds for a CHI slot, but in history, literature, and much of the humanities, reading a paper aloud *is* the genre. Say so, then teach writing for the ear: shorter sentences, signposts spoken aloud, a large-type reading copy, and the usual rule of thumb of about two minutes per double-spaced page. Then cover images: getting permission to show an archival photo on a slide and crediting it, alt text inside the slide file, and depositing the deck afterward (`version-control` already introduces Zenodo).

**artifacts-have-politics, and the thread as a whole.** Across the book the Stakes openings are specific and varied: the Norway problem, `Tagged: no`, the Amharic token count, the 90-day account deletion in `file-system`. But they lean on three themes the cornerstone barely develops. Accessibility drives `latex`, `presenting`, `documentation`, and `debugging`, yet the cornerstone never mentions disability, and its "Key laws" section names no accessibility law (the ADA, Section 508). Its only copyright law is the DMCA: nothing on fair use, text-and-data mining, or Creative Commons, and no chapter helps a student license their own code or data. Memory and loss (`file-system`, `http-apis`, the notebook study in `scripting`) have no home either, and neither does classification, though `sql-basics` tells the OMB race-categories story; Bowker and Star's *Sorting Things Out* is the obvious anchor. Add sections on access and on archives, add "Access" and "Durability" to the checklist, and bring in Indigenous data sovereignty (the CARE principles). Finally, the cornerstone links to only six chapters, and `regex` isn't one of them, even though both chapters open on the same rejected-name form. Link the cornerstone to the chapters that point back to it.


---

## Review 7: Jordan Whitfield, assistant professor of computational social science

*Primary chapters: pandas-basics, sql-basics, http-apis, evaluating-ai*

I'd assign these four chapters tomorrow, and the MENA "Stakes and politics" section in `sql-basics` is the best framing of measurement politics I've seen in a tools book. Here's what I'd change for students who work with surveys, administrative records, and platform data.

**Meet the R students where they are.** Half my class learned `dplyr` first, and the only nod to R in `pandas-basics` is one sentence saying data frames came from R. Put an "If you learned R first" callout next to the existing "If you're following a pandas 2 tutorial" callout. It should cover the index, which has no tidyverse counterpart; `mutate` ≈ `assign`; `group_by() |> summarise()` ≈ `groupby().agg()`; and the default that will actually burn them: R's `sum()` returns `NA` unless you pass `na.rm = TRUE`, while pandas skips `NaN` without a word. A `dplyr` column in the "SQL ↔ pandas translation table" in `sql-basics` would save me a lecture.

**Give `pandas-basics` a survey example.** Its examples are grocery prices, office supplies, and iris. `to_datetime` never appears in the chapter, and `value_counts` and `crosstab` don't show up until `evaluating-ai`. Weighted means don't appear anywhere in the book. A short "Summarizing responses" section would cover what my students do in week two: `value_counts(normalize=True, dropna=False)`, `crosstab`, an ordered `Categorical` for a Likert scale so "Agree" doesn't sort before "Disagree", and `np.average(..., weights=...)` for survey weights.

**In `http-apis`, treat the people as well as the server.** "Respect `robots.txt`, and read the terms" handles courtesy and legality well, but collecting posts from people is human-subjects data. The chapter never mentions an IRB, even though `jupyter` and `remote` both do. One paragraph would do it: ask whether your project needs review, store only the fields you need, and decide what to do about content the author later deletes. The roadmap already has an open "Data ethics and licensing" item, and this is where it would land. Second, the chapter parses responses straight into DataFrames. The chapter's own stakes section makes the case against that: the API won't give you the same answer next year. Save every raw response to `data/raw/` with a timestamp before parsing, and cross-reference `project-management`. Third, swap the weather example for a public-data API social scientists use, such as the Census Bureau's, which teaches the same lessons about keys and parameters.

**`evaluating-ai` is a methods chapter wearing an AI label.** Kappa, gold labels, and audit studies à la Bertrand and Mullainathan are content analysis. Yet its only prerequisite is `llm-internals`, and nothing in Part IV links to it. Add `pandas-basics` as a prerequisite and link to it from `tabular-data`. Two additions would make it a chapter I'd assign on its own. First, Krippendorff's alpha, the standard in my field when you have more than two coders or some missing codes. Second, the step the chapter stops just short of: "the false alarms inflate your number." Show it. Estimate the share of negative comments from the model labels and from gold, then show how far apart they are and what that does to a group comparison. That gap is where students' findings go wrong.

**Across the book, add a capstone thread and a chart.** Part IV ends at APIs, and Part V starts with reading scholarship. Nothing in between takes a cleaned table to a chart or a stated finding. I'd add a short capstone thread through Part IV: pull records from an API, store them in SQLite, clean, summarize, label open text with an LLM, and validate. A small visualization section would close the loop to a result you can defend.


---

## Review 8: Ruth Lindqvist, professor of quantitative methods in a sociology department

*Primary chapters: llm-internals, ai-agents, evaluating-ai (plus tabular-data's validation sections)*

I'll say the kind thing once: "Score the model, with honest uncertainty" is better than most of what my graduate students get, and the bootstrap table is exactly what they need to see. Keep it. Now the harder part. The word "validity" doesn't appear anywhere in this book. My students are going to use it to justify LLM-coded survey responses in theses, so that gap matters.

**Evaluating-ai mixes up two different jobs for one evaluation set.** "Build a small evaluation set" tells students to oversample the edges and "add every failure you find." Then "How sure can you be?" asks what the model would get "on the other 1,984." A set built on purpose to be hard is a test suite, not a probability sample, and its accuracy tells you nothing about the rest of the comments. Split the two jobs explicitly: a *random* sample for estimating accuracy, and a separate hard-case suite for regression checks. There's a related problem. The chapter reruns the same set after every prompt change, and the summarization worked example rewords the rubric "until they don't" disagree and then validates the judge on those same 10 items. That's tuning on your test data. Add a held-out split, and explain why.

**Treat an LLM's labels as measurement with error, all the way into the analysis.** The chapter gets close ("the false alarms inflate your number") and then stops. Show a simple misclassification correction for a prevalence estimate, and point to social-science work on using imperfect LLM labels in downstream inference, such as Egami and colleagues' design-based supervised learning. Also treat the model as a rater of its own: run it three times and compute kappa across the runs. That's the natural payoff of llm-internals' point that temperature 0 isn't reproducible.

**Some statistical fixes.** When you compare two prompts on the same items, "intervals overlap a lot" is the wrong test. Use a paired bootstrap of the difference, or McNemar's test. For a proportion at n = 16, mention the Wilson interval (roughly 0.50 to 0.90 here). Put Krippendorff's alpha next to kappa. And say plainly that kappa measures *reliability*, since two raters can agree perfectly on a bad construct. The group audit explains the model's miss on comment 14 after seeing the data, which is a good place to warn about after-the-fact stories and about testing many subgroups.

**Llm-internals Exercise 5 asks for a `confidence` field** with no warning that a model's self-reported confidence usually isn't calibrated. Students will put that number in a table. Two sentences would fix it.

**Ai-agents' "Turning a notebook workflow into an agent"** says choosing "which analysis fits, and whether to retry after a failure" is "where an agent helps." For research, that's where it hurts: an agent that retries until something works is automated p-hacking. Say that analyses get pre-specified, and keep agents to the fixed transformations.

**Across the book:** tabular-data's dropna example in "Stakes and politics" is the best writing on measurement here. Name MCAR, MAR, and MNAR there. Then add a short section on levels of measurement and survey weights, which the book never covers, and link to project-management's "Data dictionary and codebook." Reading-scholarship's "Is this paper any good?" checks peer review, venue, retractions, and citations, but never asks how the paper measured anything. Finally, evaluating-ai lists only llm-internals as a prerequisite, when what it really builds on is pandas-basics and tabular-data. Social scientists will arrive at this chapter first, so fix that callout.


---

## Review 9: Sam Nakamura, research project manager for a university research lab

*Primary chapters: project-management, version-control, collaboration, automation*

Part VI is where I'd send a new RA, and it mostly gets the practices right. Keep the fresh-clone reproducibility check in `project-management` (the missing `pyarrow` and `data/processed/` folder are exactly what I see every fall) and the invisible-labor "Stakes and politics" section. My critique is about *scale*: every scenario in Part VI is a semester group project, and research work isn't shaped like that.

Look at the openings. `project-management` starts "It's the night before your group's final project is due," `automation` starts "It's the night before your group project is due," and `collaboration` starts "It's the Thursday before your group project is due." The "Why read" list in `project-management` promises issues on "a project with three people and six weeks." A lab project lasts three years, has people coming and going the whole time, mixes a PI, grad students, and sophomores, and lives in a GitHub organization that outlives all of them. Vary the openings, and give Part VI one lab-shaped thread.

**Handoffs are too small.** The "Handoff notes" section in `collaboration` is about the end of a work session. The handoff that sinks labs is a student graduating. Add a departure checklist: move repositories from personal accounts into the lab org, rotate every credential the student created, find cron jobs and CI secrets tied to their account (`automation`'s closing prompt about "an author, an operator, and someone who reads the logs" sets this up nicely), record where the data lives and under what agreement, and tag and archive the state that produced the paper. At that point, "Tags and releases (optional)" in `version-control` isn't optional.

**Onboarding is missing.** Every `version-control` example starts from your own `git init` or a fork. None shows joining an existing repository in an organization: accepting the invite, turning on two-factor authentication, following someone else's README, running the smoke test, picking up a `good first issue`, and opening a first PR. Protected branches get one sentence in `collaboration` ("Who owns this?"), yet a new member's first rejected push is often a branch-protection rule, and the "If `git push` is rejected" callout only covers the fetch-first case. A "first week on someone else's project" worked example would do more for week-one productivity than anything else here.

**Planning is too optimistic.** "Planning, without the bureaucracy" has a brief and milestones but says nothing about estimating time, padding for overruns, or waiting on other people. In research the blockers are IRB approval, a data use agreement, or an advisor's review cycle, and each takes weeks. IRB comes up exactly once in the whole book, in the `writing-thesis` timeline table. "Sensitive data" should name IRB protocols and data use agreements, and link to that timeline.

**Consolidate Part VI.** Issue anatomy appears twice ("What a good issue looks like," four parts, in `project-management`; "What a good issue contains," five ingredients, in `collaboration`), and the Blocker/Suggestion/Question/Nit taxonomy appears in both `version-control` and `collaboration`. Give each one home. `project-management` says "Prerequisites: none" while its examples run `git init` and "Fixes #42", so list `@sec-git-github` or put version control first. And pick one running project: `coffee-sales` covers two chapters and the survey project covers the other two.

Two smaller points. `collaboration`'s "Why read" promises to explain what open-source maintainers expect, and no section delivers it, so write one or cut the bullet. Book-wide, the Introduction calls the book "a reference, not a novel" but offers no reading paths. A few role-based routes ("first week in a research lab: terminal, version control, virtual environments, project management, secrets, remote computing") would let an RA read it as a curriculum.


---

## Review 10: Grace Mensah, technical program manager for a nonprofit data team

*Primary chapters: version-control, collaboration, automation, secrets, remote*

I hire the people this book is written for, so I read Part VI asking one thing: would a graduate who'd absorbed it be ready for week one on my team? On mechanics, mostly yes; keep the reflog walkthrough, the Blocker/Suggestion/Question/Nit labels, and the empty-environment cron test. The gaps are about joining an organization.

**Every scenario starts a project; jobs start by inheriting one.** "Start a new repository," "A new project from scratch" in secrets, and the group-project framing in collaboration all assume you're there at the beginning. My interns clone a three-year-old repository with CI, CODEOWNERS, protected branches, and a half-wrong README. Add a worked example spanning version-control and collaboration: an intern gets access, runs the README on a clean machine, opens a first small PR into someone else's review hierarchy, and files issues for everything that broke.

**Add offboarding next to "Handoff notes."** The Alice → Bob note covers the work in progress, not what the person owned. When an intern leaves, what breaks is the cron job on their laptop, the pipeline authenticating with their personal access token, and the cloud VM billed to a project nobody watches. Secrets recommends a token that "expires next month," which is right, and at work is how a pipeline dies on a Saturday. A "your last week" checklist would close the loop across automation, secrets, and remote: transfer scheduled jobs, swap personal tokens for team-owned ones, hand over or delete cloud resources. Automation's own closing prompt about "an author, an operator, and someone who reads the logs" is the frame for it.

**Secrets needs an organizational layer.** @tbl-secret-homes stops at a password manager and GitHub Actions secrets. Add: two-factor on the accounts themselves (the chapter never mentions it); cloud CLI credentials such as `~/.aws/credentials`, which is odd to leave out when the chapter's own Uber case was an access key; and, in "What if I already leaked a secret?", tell your security contact *first*. Right now "telling your team, instructor, or IT staff" comes last, after rotating and rewriting history. A new hire who quietly fixes things scares me more than one who reports a leak in five minutes.

**Remote's cloud section assumes your own card.** "Whose card pays the bill" is the right question, but at work it's the organization's account, and the habits change: ask before you create anything, tag every resource with an owner and an end date, and know who gets the budget alert. Automation says Actions is "free for public repositories"; add a line saying private repos have a monthly minute quota, which is exactly where a three-version matrix hurts.

**Missing entirely: reporting up.** Collaboration's "Short written updates" (yesterday, today, blocked) is written for teammates. Nothing teaches a status note for a non-technical manager or funder: where things stand, the risks, the decisions needed, and new dates, including how to say "this will be late" a week early instead of the night before. That's the skill I most wish new hires had.

**On balance, the book prepares students for graduate school better than for a job.** Part V is built around academic genres (reading scholarship, manuscripts, the thesis, LaTeX), and Presenting's "job talk" is a faculty job talk. Add a "Writing at work" chapter (status update, one-page decision memo, incident write-up, brief for a non-technical partner), or give each Part V chapter a workplace section. Most of your readers will write far more status updates than dissertations.
