# 25  How to Read Scholarly Articles and Books

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-asking-questions](#sec-asking-questions), [sec-documentation](#sec-documentation).
>
> **See also:** [sec-writing-manuscripts](#sec-writing-manuscripts), [sec-latex](#sec-latex), [sec-ai-llm](#sec-ai-llm), [sec-git-github](#sec-git-github).

## Purpose

The first time you open a research paper, it does not feel like reading. It feels like staring at a wall of jargon, equations, citation soup, and unfamiliar conventions. You read the abstract, blink, read it again, and have no idea what the paper actually claims. You scroll to the introduction, and the authors begin a polite argument with people you have never heard of about a problem you didn’t know existed. Twenty minutes later you are exhausted, and you still cannot tell a friend in one sentence what the paper is about.

This chapter teaches you a small set of techniques that turn that experience into something tractable. It covers how to triage a paper before committing to read it, how to read at three different depths depending on your goal, how reading conventions differ between HCI papers, machine-learning papers, social-science papers, and humanities scholarship, and how to keep what you read in a system you can actually use months later. None of this is mysterious. It is just craft, and like all craft it improves rapidly once someone tells you what professionals actually do.

Read this chapter before your first literature-heavy assignment. It will save you from a common failure mode where students “do the readings” by highlighting every other sentence and remembering nothing.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Apply Keshav’s three-pass method to triage and read a research paper at the depth your goal actually requires.

2.  Recognize the rhetorical conventions of HCI/CSCW papers, machine-learning and data-science papers, social-science empirical work, and humanities scholarship, and adjust your reading accordingly.

3.  Maintain a personal literature library in Zotero with the Better BibTeX add-on, so that your reading integrates seamlessly with your writing tools.

4.  Take structured notes (Cornell, Zettelkasten, or annotation-based) that you can synthesize across many sources without re-reading every paper.

5.  Build a small literature map for a research question and identify the recurring “key papers” and “key authors” in a field.

## Running theme: you are not reading to finish; you are reading to decide what to read more carefully

Reading scholarship is fundamentally a triage problem. You will encounter far more papers than you can ever read deeply. The skill is not “reading faster” — it is reading at the right depth, for the right purpose, on the right paper, and knowing how to decide.

## 25.1 Why reading is hard (and why nobody taught you)

Most undergraduates arrive at their first research paper with the reading habits they built in high school: read every sentence in order, highlight things that seem important, take notes if forced. That strategy works for a textbook, where every sentence is intended for you and the author has tried to maximize clarity. It fails for a research paper, where the audience is a small community of specialists, the structure is rhetorical rather than pedagogical, and the author’s primary goal is to defend a contribution against skeptical reviewers — not to teach you.

This is not your fault, and it is not the authors’ fault either. Research papers are *condensed correspondence between specialists*. They assume context you don’t have. They use jargon as shorthand because the audience already knows it. They cite earlier work in passing because the audience has already read it. When you read a CHI paper as a sophomore and feel like the words are doing something different than in a textbook, you are correct: they are. The trick is not to read harder. The trick is to read with a different protocol.

Two ideas underpin everything else in this chapter. First, **most papers do not deserve a full read.** A paper you cite once in a literature review may need only ten minutes of your attention. A paper you build directly on may need six hours. You decide. Second, **you read in passes, not in a single sweep.** Each pass adds depth, and you only commit the next pass if the previous pass justified it.

## 25.2 The three-pass method

Srinivasan Keshav’s three-page note “How to Read a Paper” ([^1]) is the canonical reference. It is short — read it before your next assigned paper. The method:

**Pass 1: the five-to-ten-minute skim.** You are deciding whether to read this paper at all. Read the title, abstract, introduction’s first paragraph and last paragraph, and the conclusion. Look at every figure and read every figure caption. Glance at the section headings to get the structure. Skim the references for names you recognize. At the end of pass 1, you should be able to answer five questions: what is the paper’s category (empirical, theoretical, system-building, survey)? What is the broad context? Are the assumptions reasonable? What are the main contributions, in your own words? Is the paper well-written? If your one-line summary doesn’t fit, the paper either isn’t ready for you or isn’t what you thought.

**Pass 2: the one-hour structured read.** You have decided this paper is worth reading. Read it linearly, but ignore the proofs, the deepest math, and the appendices. Pay close attention to the figures, tables, and the sentences immediately surrounding them — those are usually the spine of the argument. Mark unfamiliar terms and citations to chase later. At the end of pass 2, you should be able to summarize the main thrust of the paper to someone else, with evidence — a paragraph, not a sentence. If you cannot, the paper may be poorly written, or you may be missing background. That’s a signal to read a related survey paper before coming back.

**Pass 3: the deep read.** You are going to build on this paper. Plan four to six hours, sometimes more. Read every section. Reproduce the argument from the paper’s premises. Try to re-derive the equations or re-implement the method from memory; check what you got wrong. Note the assumptions you would challenge in your own work. At the end of pass 3, you should be able to reconstruct the paper from scratch and identify its weaknesses.

The cost of pass 1 is small. The cost of pass 3 is enormous. Most students invert this — they jump straight into linear reading and burn two hours on a paper that pass 1 would have told them to set aside. Don’t do that.

## 25.3 Reading across disciplines

Information-science research draws from so many fields that you will read papers from at least four different rhetorical traditions in the same semester. Each genre signals “the contribution” in a different place.

**HCI venues (CHI, CSCW, ICWSM, FAccT).** These papers are usually IMRaD-shaped — Introduction, Related Work, Methods, Findings, Discussion — but with rhetorical flexibility. Qualitative and mixed-methods papers are common. The introduction earns its keep by stating the *gap* and the *contribution* clearly; if you cannot find the “in this paper, we…” sentence in the first two pages, you are probably reading a poor paper or you are reading too fast. The discussion section often contains “implications for design,” which is where the paper translates findings into something practitioners can use. In CSCW especially, the framing in the introduction does most of the rhetorical work; read it twice.

**Data-science and machine-learning papers.** These are denser, with the argument carried by figures, tables, and benchmarks. Related work is often a thicket of citations to keep up with a fast-moving field. The contribution is usually a method, an empirical result on a benchmark, or a dataset. Read the abstract, the figure showing the main result (almost always Figure 1 or Figure 2), and the experimental setup section. Skip the related work on a first pass; you can come back. If the paper claims state-of-the-art, look at how they define the baseline and what the error bars (if any) say.

**Social-science empirical papers (JASIST, JCMC, *New Media & Society*, *Information, Communication & Society*).** These follow theory–method–results–discussion fairly strictly. The theory section matters: it tells you what the authors think they are measuring and why. Operationalization — how an abstract construct gets turned into a measurable variable — is where most of the action is. Pay attention to the identification strategy (causal inference, descriptive, exploratory) and the limitations section, which is more substantive in social science than in many CS venues.

**Humanities scholarship.** Argument-driven. The abstract may not summarize the argument; sometimes it merely sets up the question. The structure is rhetorical, not formulaic. There is usually a thesis sentence — a single sentence that states what the author is claiming — somewhere in the first few pages, and the rest of the article is a move-by-move defense of that claim. When you read a humanities paper, hunt for the thesis sentence first, then read the article as a series of moves *on* that thesis: what is the author conceding, what are they arguing against, where are they introducing evidence?

If you read across these traditions without adjusting, you will find yourself either lost (in humanities) or bored (in CS). The same paper, read with the wrong protocol, will feel either pretentious or trivial.

## 25.4 Skimming vs. deep reading: deciding what a paper is for

Before you open a paper, name your purpose. Three common ones:

**Reading for citation.** You need to know what this paper says so you can refer to it accurately in your own writing. Pass 1 is usually enough. The dangerous failure mode is citing a paper for a claim it doesn’t actually make — make sure your one-line summary actually fits the sentence you plan to write.

**Reading for replication.** You are going to build on the paper, reuse its method, or reproduce its results. Pass 3 is required. Plan accordingly.

**Reading to teach yourself a concept.** You are using the paper as a textbook substitute. Often a survey paper or a textbook chapter is a better choice; if you must read primary literature, prefer the most recent paper that cites the older work and read its related-work section as a curated tour of the field.

Different purposes, different passes. Refusing to triage is the most common reason students burn out reading.

## 25.5 Note-taking systems

A note-taking system is what turns reading into knowledge that survives. Without one, you will re-read the same paper six months later and not remember why you cared. Three approaches dominate; pick one and stick with it for a semester before judging.

**Cornell notes.** A page is divided into a narrow left column (cues), a wide right column (notes), and a strip at the bottom (summary). You take notes in the right column while reading, generate cue questions in the left column afterwards, and write a 2–3 sentence summary at the bottom. Excellent for a single dense source you need to study. Less helpful for synthesizing across sources.

**Zettelkasten (“slip-box”) and atomic notes.** A method developed by the German sociologist Niklas Luhmann, modernized in tools like Obsidian ([^2]) and Logseq ([^3]). Each note is small — one idea per note — and notes link to other notes. You write in your own words; you tag and link as you go. Over time the system becomes a graph of ideas you can navigate. The strength of Zettelkasten is synthesis: when you sit down to write a literature review, you already have the connective tissue. The weakness is overhead — if you build the system but never write, you have built a very pretty filing cabinet.

**Annotation-first.** You highlight and comment directly on the PDF. Tools like Hypothes.is ([^4]) annotate publicly on the web; Zotero’s built-in PDF reader annotates inside your library. Combine highlighting with tags and short comments, then extract the tagged passages into your notes when you write. Low overhead, good for fast triage. The risk is that highlights are not knowledge — re-read your annotations periodically to extract the ideas, or they will rot.

You don’t need to choose forever. Most working researchers blend annotation-first with a Zettelkasten layer for the ideas that matter.

## 25.6 Reference management with Zotero

You will accumulate hundreds of papers over four years. If you do not manage them, you will lose them — to a dead Dropbox link, to a stale Mendeley export, to a bibliography that doesn’t match your `.tex` file. **Use Zotero.** It is free, open-source, actively maintained, and integrates with every writing tool you will use.

Install Zotero ([^5]) and the Zotero Connector browser extension. Create a top-level collection for each course or project — for example, “INFO 4XXX – Term Paper” — and save papers into it as you find them. The browser connector is the magic part: a single click on a Google Scholar result, a publisher’s PDF page, or an arXiv abstract saves the metadata, attaches the PDF, and files everything automatically.

The single most useful add-on is **Better BibTeX** ([^6]). It generates stable, readable citation keys (e.g., `keshav2007paper`) that don’t change when Zotero updates. Configure it once with a citation-key pattern like `[auth:lower][year]`, and your `.bib` exports will be consistent across years and machines. Better BibTeX also auto-exports your library to a `.bib` file on disk; point your LaTeX project at that file and your bibliography is always current. See [sec-latex](#sec-latex) for the writing-side workflow.

Tag aggressively. Tags in Zotero are flat and free-form, which makes them excellent for the kind of “I’ll know it when I see it” filtering that comes up when you are writing. Tag by method, population, theory, or just `to-read` and `read`.

Mendeley and Paperpile are alternatives. Mendeley’s parent company has a checkered history of changing terms in ways that hurt users; Paperpile is fine but proprietary and Google-Scholar-centric. For a portable, durable workflow, Zotero is the safe default.

## 25.7 Synthesis: building a literature map

A literature map is the artifact you build when you are about to write a literature review or a paper’s related-work section. It is not the literature review itself — it is the organized set of notes you write *from*.

The simplest format is a **concept matrix** (Webster & Watson 2002 ([^7])). Rows are papers; columns are concepts, methods, populations, or theoretical frames. A cell holds a one-word, one-phrase, or short note about how that paper treats that concept. After you populate the matrix for ten or fifteen papers, the columns become the natural sections of your literature review, and the empty cells reveal gaps in the literature — possibly your contribution.

To find the right papers in the first place, do **forward and backward citation tracing.** Backward: read the references of a key paper to find the work it builds on. Forward: paste the paper’s title into Google Scholar and click “Cited by N” to find the work that builds on it. Connected Papers ([^8]) and Litmaps ([^9]) both visualize these networks, and either is worth ten minutes when you start a new project. Look for **key authors** — names that appear in multiple bibliographies — and read their most recent paper to catch up on their current direction.

A good literature map is small. Fifteen well-organized papers beat fifty disorganized ones. Resist the urge to expand the matrix until every cell is filled — your time is better spent reading the next paper deeply than reading the next paper at all.

## 25.8 Reading with AI: legitimate uses and traps

Large language models change the economics of reading, in both helpful and harmful ways. See [sec-ai-llm](#sec-ai-llm) for the full discussion of what AI tools can and cannot do; the rules in this chapter are specific to scholarly reading.

**Legitimate uses.** Asking an LLM to summarize a paper for triage (pass 1, with caveats). Asking it to define a piece of unfamiliar notation or terminology. Asking it to critique your own one-paragraph summary of a paper, to surface what you missed. Generating a list of related papers you should look up — *which you then verify in Zotero or Scholar*, because LLMs hallucinate citations confidently.

**Traps.** Using an LLM summary as a substitute for reading the paper at all. This will catch up with you the first time you cite the paper for a claim it doesn’t actually make. LLMs are confident; they do not flag what they are unsure of; and they cannot distinguish a paper’s findings from a paper’s framing of others’ findings.

A useful protocol: ask the LLM for a summary, then read the paper at pass 1, then compare. Where they disagree, the paper wins. Where the LLM mentioned something the paper didn’t, treat it as suspect and check.

## 25.9 Stakes and politics

The skill of reading scholarship efficiently is genuinely useful. It is also entangled with a system that decides who gets to read at all. Three things to notice. First, *paywalls and access*. The major academic publishers (Elsevier, Springer Nature, Wiley, Taylor & Francis) charge institutional subscription fees that are routinely in the millions of dollars per year, with predictable consequences: faculty at well-funded universities have frictionless access, faculty at smaller institutions and the entire Global South do not, and members of the public — including the taxpayers who funded most of the research — get a paywall by default. Sci-Hub and the broader open-access movement exist precisely because this gradient is so steep.

Second, *citation networks encode status*. Whose papers get read, cited, and assigned in courses depends partly on the work’s quality and partly on the social and institutional networks the authors are inside. Citation patterns systematically under-cite women, scholars of color, scholars from non-English-speaking institutions, and scholars from the Global South, even when the underlying work is comparable. Whose ideas you read becomes whose ideas you cite, and whose ideas you cite becomes whose work the next reader sees.

Third, *what publication shape counts*. The journals and proceedings most rewarded by hiring and tenure committees are overwhelmingly Anglophone, run by editorial boards from a small number of countries, and require fluency in genre conventions (IMRaD, theory-method-results) that have a specific provenance. Work that does not fit these conventions — community-engaged research, indigenous knowledge traditions, applied/practitioner work — is harder to publish and harder to find when you are reading.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework. The concrete prompt to carry forward: when you build a literature map, ask whose work was easy to find and whose work the system you searched in routinely buries.

## 25.10 Worked examples

### First-pass a CHI paper in eight minutes

Pick a recent CHI paper on a topic you care about — say, an empirical study of how data-science students use AI assistants. Set a timer for eight minutes.

*Minutes 0–1.* Read the title and abstract. Write one sentence in your notes: what is the paper claiming? If you cannot, re-read the abstract once.

*Minutes 1–3.* Read the first paragraph of the introduction (sets up the problem) and the last paragraph (states the contribution). The middle of the introduction is usually the literature gap and the framing — skim it for the names of competing approaches.

*Minutes 3–5.* Look at every figure. Read every caption. The figure that shows the main result is usually obvious — it is the one with the prominent comparison or the most callouts. If the paper is qualitative, the “figure” might be a participant quote in a callout box; treat it the same way.

*Minutes 5–7.* Read the section headings. Skim the discussion section for “implications” or “design considerations” — those are the takeaways. Glance at the related work for names you recognize.

*Minute 7–8.* Write three things: a one-sentence summary, the contribution in your own words, and one question you would want to ask the authors.

You now have enough to decide whether to read pass 2. If you cannot fill in the three things, the paper is either poorly written or beyond your current background — either way, that is information.

### Setting up a Zotero library for a semester project

You are starting a term paper for a class. Here is the setup, end to end.

1.  Install Zotero from <https://www.zotero.org/> and the Zotero Connector for your browser. Create a free Zotero account so your library syncs across devices.
2.  In Zotero, right-click “My Library” → New Collection → name it “INFO 4XXX – Term Paper”.
3.  Install Better BibTeX: from inside Zotero, Tools → Add-ons → install from `.xpi` (download the latest from <https://retorque.re/zotero-better-bibtex/>). Restart Zotero.
4.  In Edit → Preferences → Better BibTeX, set the citation-key formula to `[auth:lower][year]`. This produces keys like `keshav2007`.
5.  Open Better BibTeX preferences → Automatic Export → set up an auto-export of your collection to `~/code/term-paper/references.bib`. Now any time you save a paper into the collection, the `.bib` file updates automatically.
6.  Find five papers via Google Scholar. On each result page, click the Zotero Connector icon. Zotero pulls the metadata, fetches the PDF where it can, and files the entry in your collection. Add tags as you go.
7.  Open `references.bib` in your text editor; you should see five BibTeX entries with stable keys.

Total time: about twenty minutes the first time, two minutes per paper after that.

### Synthesizing five papers into a one-page literature map

You have read five papers about how moderation policies on online platforms affect user behavior. You need a literature review section.

Build a concept matrix. Rows are the five papers. Columns are: *platform studied*, *moderation intervention*, *outcome measure*, *method*, *primary finding*, *limitation*. Fill each cell with one phrase.

After you populate the matrix, look at the columns. *Outcome measure* might split into “behavioral” (post counts, user departures) and “linguistic” (toxicity, civility). That split is now a section of your literature review. *Method* might split into “natural experiment” and “interview study” — another section. The empty cells — say, no one has measured behavioral outcomes after a policy change on a small platform — is a candidate gap for your own contribution.

Your three-paragraph synthesis writes itself. Paragraph one: scope of the literature. Paragraph two: what is converged on (the columns most papers fill the same way). Paragraph three: where the literature disagrees or is silent (the columns with disagreement or empty cells). You have not done magic; you have just made the structure visible.

## 25.11 Templates

A reading-note template you can paste at the top of every new note:

``` markdown
# {Paper title}

**Citation:** {full citation in your preferred style}
**Zotero key:** {citation key from Better BibTeX}
**Pass:** {1, 2, or 3}
**Date read:** {YYYY-MM-DD}

## One-sentence summary

(In your own words.)

## Claim

(What does the paper argue?)

## Evidence

(How is the claim supported? Methods, data, key results.)

## Critique / gap

(What did they not address? What would you challenge?)

## Connections

- See also: {[[other-note]] or @sec-... or paper key}
- Cites: {key works the paper builds on}
- Cited by: {if known, key works that build on it}

## Quotes worth keeping

> ...
```

A literature-map concept-matrix template (paste into a new markdown file and edit):

``` markdown
| Paper | Population | Method | Outcome | Theoretical frame | Finding |
|---|---|---|---|---|---|
| @key1 | ... | ... | ... | ... | ... |
| @key2 | ... | ... | ... | ... | ... |
```

## 25.12 Exercises

1.  Apply Keshav’s pass 1 and pass 2 to an assigned paper. Submit a one-page summary that includes the contribution in your own words, the method, the main finding, and one limitation.
2.  Set up a Zotero library with the Better BibTeX add-on and export a `.bib` file containing at least five papers on a topic you care about.
3.  Pick an HCI paper and a data-science paper on similar topics. Write a 300-word note explaining how each genre privileges different kinds of evidence and contribution.
4.  Use Connected Papers (<https://www.connectedpapers.com/>) to find five neighbors of a paper you have read. Identify the “key author” who appears most often in the cluster, and read their most recent paper.
5.  Annotate a publicly available paper using Hypothes.is (<https://web.hypothes.is/>). Share the link with a classmate and discuss what you each highlighted.

## 25.13 One-page checklist

- Did you decide *before* reading what depth this paper deserves?
- Did you read the abstract and conclusion before the body?
- Did you look at every figure and read every caption?
- Did you write a one-sentence summary in your own words?
- Did you save the paper to Zotero with the right tags and collection?
- Did you record the citation key before you started writing?
- For pass 2 papers, did you write a structured note (claim / evidence / critique / connections)?
- For pass 3 papers, did you re-derive or re-implement the core method?
- When you used an LLM, did you verify its summary against the paper?
- Did you tag at least one connection to another paper or note?

## 25.14 Quick reference: matching reading depth to your goal

| Goal | Pass | Time | Output |
|----|----|----|----|
| Decide whether to cite | 1 | 5–10 min | One-line yes/no |
| Summarize for a literature review | 1 + 2 | 1 hour | Three-sentence note |
| Replicate or build on the work | 1 + 2 + 3 | 4–6 hours | Reproduction notes |
| Teach a concept to yourself | 1 + 2 (often a survey instead) | varies | Notes you can teach from |

> **NOTE:**
>
> - S. Keshav, [How to Read a Paper](https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf) (*ACM SIGCOMM CCR*, 2007) — the canonical 4-page essay on the three-pass method; worth re-reading before every literature search.
> - Jane Webster and Richard T. Watson, [Analyzing the Past to Prepare for the Future: Writing a Literature Review](https://www.jstor.org/stable/4132319) (*MIS Quarterly*, 2002) — the standard reference for concept-driven literature reviews in IS-adjacent fields.
> - Sönke Ahrens, [*How to Take Smart Notes*](https://www.soenkeahrens.de/en/takesmartnotes) (2017) — the modern Zettelkasten manifesto; a useful pairing with Zotero for serious reading habits.
> - Zotero, [Documentation](https://www.zotero.org/support/) — the free, open-source reference manager most academics now use; the entry point for Better BibTeX, browser connectors, and group libraries.
> - Jenny Bryan, [Naming things](https://speakerdeck.com/jennybc/how-to-name-files) — the slides on file-naming conventions; applies directly to PDF and notes files in a reading workflow.
> - DOAJ, [Directory of Open Access Journals](https://doaj.org/) — the canonical index for venue-level open access; useful when you want to filter your searches to OA-by-default journals.
> - ACM, [Open Access Initiatives](https://www.acm.org/publications/openaccess) and arXiv, [About arXiv](https://info.arxiv.org/about/index.html) — two of the largest discipline-relevant open-access channels for IS-adjacent work; pairs with the “Stakes and politics” framing above.

[^1]: <https://web.stanford.edu/class/ee384m/Handouts/HowtoReadPaper.pdf>

[^2]: <https://obsidian.md/>

[^3]: <https://logseq.com/>

[^4]: <https://web.hypothes.is/>

[^5]: <https://www.zotero.org/>

[^6]: <https://retorque.re/zotero-better-bibtex/>

[^7]: <https://www.jstor.org/stable/4132319>

[^8]: <https://www.connectedpapers.com/>

[^9]: <https://www.litmaps.com/>
