# Missing Manual for Information Scientists

The hidden curriculum of computing technologies

Author

Brian C. Keegan

Published

September 2026

# 1 Introduction

## 1.1 Why this handbook?

Your first weeks of programming can be frustrating, and usually not because the ideas are hard. The ideas are often the easy part. What trips you up is everything *around* them. A tutorial says to install a package, and nobody says where to type the command. A file arrives that won’t open on a double click. Your instructor flips between a terminal, an editor, a browser, and a notebook, and you lose track of which window is doing what. It can feel like there was a class everyone else took, the one where they learned all this, and you missed it.

![A cartoon of a stick figure with a round head, frowning and resting its chin on its hand while it glares at a desktop computer monitor.](graphics/frustrated_computer.png)

A student and a computer in mutual frustration.

If that’s how you feel, you’re in good company, and you haven’t missed anything. Education researchers have a name for the things a course expects you to know without ever teaching them: the [hidden curriculum](https://en.wikipedia.org/wiki/Hidden_curriculum). Software is part of it. Richard Edwards has argued that the code, algorithms, and standards in the software used in education quietly shape what teachers and students can see and do, in ways that aren’t always apparent to the people using it.([Edwards 2015](#ref-edwardsSoftwareHiddenCurriculum2015)) Instructors at MIT noticed the same gap in computer science and built a whole course to fill it, [The Missing Semester of Your CS Education](https://missing.csail.mit.edu/), because classes rarely teach proficiency with the tools students spend hundreds of hours using.

Why doesn’t anyone teach this stuff? Some of it is the [curse of knowledge](https://en.wikipedia.org/wiki/Curse_of_knowledge): instructors have used these tools for so long that they’ve forgotten they ever had to learn them. Some of it is priorities, since there’s only so much time in a semester, and some of it is hope, that students will pick it up on their own or that another course will cover it. Meanwhile, each student stays quiet because they assume everyone else already knows. Psychologists call that [pluralistic ignorance](https://en.wikipedia.org/wiki/Pluralistic_ignorance), and it feeds a classroom version of the “[spiral of silence](https://en.wikipedia.org/wiki/Spiral_of_silence)”: the fewer people ask, the more alone each confused person feels, and the less anyone asks. The frustration compounds, between instructors, students, and computers alike.

Here’s the part nobody likes to hear: you can’t skip this. A surprisingly large share of the time a developer, designer, analyst, scientist, or researcher spends at a computer goes to *managing* software rather than using it: installing, updating, and configuring libraries; reading documentation and issue trackers to work out why something broke; and connecting to data and to other people’s work. Those chores give experienced people headaches too. They’re just more demoralizing when you’re new and can’t tell whether the problem is the tool or you. (It’s usually the tool, or the missing explanation of it.)

Some platforms promise to make the whole mess go away. Hosted notebooks like [Google Colab](https://colab.research.google.com/) and [Kaggle](https://www.kaggle.com/code), and cloud services like Amazon’s [SageMaker](https://docs.aws.amazon.com/sagemaker/), really do take some of the setup off your hands, and for a quick class exercise they can be the right call ([sec-jupyter](#sec-jupyter) compares the hosted notebooks). But there’s no free lunch. You trade the setup for costs that grow over time, limits you don’t control, and [lock-in](https://en.wikipedia.org/wiki/Vendor_lock-in) to one company’s way of doing things. And when that tidy managed environment changes, breaks, or goes away, you’re left debugging a system you never learned. Being comfortable managing your own computer, your own Python, and your own project is what lets you choose those services on purpose instead of depending on them.

That’s what this handbook is for. It’s the missing class: the practical, rarely taught skills that sit between knowing what to type and knowing how to work.

## 1.2 Computational thinking

You’ve probably heard an instructor say “think like a computer” and wondered what that actually means. The usual name for it is [computational thinking](https://en.wikipedia.org/wiki/Computational_thinking), a phrase Jeannette Wing popularized in a 2006 essay arguing that it’s a way of approaching problems that everyone can use, not just computer scientists ([Wing 2006](#ref-wingComputationalThinking2006)). It isn’t about memorizing syntax. It’s about breaking a problem down and describing a solution precisely enough that a computer can carry it out. Teachers often split it into four skills:

- **Decomposition.** Break a large, fuzzy task into smaller pieces you can tackle one at a time. Downloading a dataset, cleaning it, analyzing it, and charting it are separate steps, even when an instructor’s demo makes them look like one smooth motion. Each step should have clear inputs and outputs. You’ll practice this when you split a project into milestones you can finish in a week or two ([sec-project-management](#sec-project-management)), and when you hunt a bug by checking a pipeline one stage at a time to find where it first goes wrong ([sec-debugging](#sec-debugging)).

- **Pattern recognition.** Notice when a new problem looks like one you’ve already solved. If you’ve cleaned one CSV file by renaming columns and dropping missing values, you can reuse that process on the next one. Spotting the pattern saves you from reinventing the wheel, and it tells you what’s worth turning into a function or a script. You’ll practice it when a block you’ve pasted into three notebook cells becomes one function ([sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks)), and when you learn to recognize the ten exceptions you’ll see most often, each with its usual first suspect ([sec-tracebacks](#sec-tracebacks)).

- **Abstraction.** Keep the details that matter and set aside the ones that don’t. A function that computes a mean doesn’t need to know whether its numbers came from a spreadsheet or a database. Leaving out what doesn’t matter makes your code more flexible and easier to test. A regular expression is abstraction in miniature: it keeps the shape of an order number, a `#` followed by digits, and ignores which digits they are ([sec-regex](#sec-regex)).

- **Algorithmic thinking.** Write down a sequence of unambiguous steps that turns your inputs into outputs. This is the heart of programming: describing a procedure so precisely that a computer could follow it, including what to do when something goes wrong. You’ll do it for real when you turn a README’s how-to-run checklist into a script or a `make` target that runs every step in the same order every time, and stops at the first failure instead of carrying on ([sec-automation](#sec-automation)).

None of this is only for coding assignments. You’ll use the same four moves throughout this book on problems that don’t look like programming at all: organizing a project’s files, untangling a broken environment, automating a chore you’re tired of doing by hand, and splitting up work with teammates.

## 1.3 Outline

This handbook is a reference, not a novel. You don’t have to read it front to back, and you probably shouldn’t: when something is in your way, find the chapter about it and start there. Every chapter is written to stand on its own. Each one opens with a short callout naming the chapters worth reading first, a “Why read this chapter” list of the snags that usually bring people to it, and a one-line running theme. Most end the same way, too: a “Stakes and politics” section about who a tool serves and who pays when it fails, worked examples, exercises, a one-page checklist, and a short list of further reading.

The chapters are grouped into seven parts.

##### Part I — Practice of Technical Work

The book starts with the human side of computing, because these habits make everything else easier. You’ll learn how to ask a technical question someone can actually answer ([sec-asking-questions](#sec-asking-questions)), how to find and write the documentation that keeps a project usable ([sec-documentation](#sec-documentation)), and how to read and write Markdown, YAML, and JSON, the text formats your tools quietly depend on ([sec-common-formats](#sec-common-formats)). Then come the skills for getting yourself unstuck: reading official documentation instead of guessing from search results ([sec-reading-docs](#sec-reading-docs)), debugging as a calm investigation rather than a string of hopeful reruns ([sec-debugging](#sec-debugging)), and reading a Python traceback so it tells you what went wrong and where ([sec-tracebacks](#sec-tracebacks)). The part ends with an essay on the politics built into the tools you use and the tools you’ll make ([sec-artifacts-politics](#sec-artifacts-politics)), which every other chapter’s “Stakes and politics” section points back to.

##### Part II — Computing Environment

Next comes the machine your code runs on. You’ll learn how to keep your operating system updated, backed up, and healthy ([sec-os-management](#sec-os-management)); how files, folders, paths, and cloud-synced drives really work on Windows and macOS ([sec-filesystem](#sec-filesystem)); how to work in a terminal without fear of breaking something ([sec-terminal](#sec-terminal)); how to choose and set up a text editor ([sec-text-editors](#sec-text-editors)); and how to reach remote machines with SSH, move files to them, tunnel back to a remote Jupyter, and work through a VPN or on a cloud server ([sec-remote-computing](#sec-remote-computing)). Getting these right prevents a lot of errors that otherwise look like mysteries.

##### Part III — Python Management

With your computer in order, the book turns to Python itself. You’ll learn to install packages with `pip` and `conda` and untangle version conflicts ([sec-pkg-mgmt](#sec-pkg-mgmt)), keep each project’s packages separate in its own virtual environment ([sec-virtual-environments](#sec-virtual-environments)), launch and troubleshoot Jupyter notebooks ([sec-jupyter](#sec-jupyter)), and move work out of a notebook into scripts and modules you can import and run from the command line ([sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks)). Two shorter chapters cover regular expressions for finding and extracting patterns in text ([sec-regex](#sec-regex)) and the formatters and linters that keep your code consistent and catch mistakes before you run it ([sec-linting](#sec-linting)).

##### Part IV — Working with Data

This part is the day-to-day craft of working with data. It covers the file formats you’ll meet, from CSV and JSON to Excel and Parquet, and what to do when a file is too big for memory ([sec-data-file-formats](#sec-data-file-formats)); the shape, cleaning, and validation of tables, so bad data stops you at the start instead of at the end ([sec-tabular-data](#sec-tabular-data)); the pandas moves you’ll reach for most often and the traps that catch newcomers ([sec-pandas-basics](#sec-pandas-basics)); enough SQL to query a database and translate between SQL and pandas ([sec-sql-basics](#sec-sql-basics)); and how to fetch data from the web through HTTP and APIs ([sec-http-apis](#sec-http-apis)).

##### Part V — Communication

Computing may be most of what you do, but communication is what makes the work count. This part covers the genres you’ll be asked to produce: how to read scholarly articles and books without drowning in them ([sec-reading-scholarship](#sec-reading-scholarship)), how to write manuscripts for conferences and journals ([sec-writing-manuscripts](#sec-writing-manuscripts)), how to write a thesis, whether it’s an honors thesis, a master’s thesis, or a monograph or three-paper dissertation ([sec-writing-thesis](#sec-writing-thesis)), how to give a talk of any length ([sec-presenting](#sec-presenting)), and how to use LaTeX and BibTeX to produce the documents themselves ([sec-latex](#sec-latex)).

##### Part VI — Project Management

Then the book zooms out from a single file to a whole project, and from you to a team. You’ll learn lightweight project management: a plan, a folder layout that gives every file a home, care for your data, a decision log, and issues that track the work ([sec-project-management](#sec-project-management)). You’ll learn version control with Git and GitHub, from your first commit through branches, pull requests, forks, and merge conflicts ([sec-git-github](#sec-git-github)); the mechanics of working with other people, like reviewing code, writing comments that help, and handing work off ([sec-collaboration](#sec-collaboration)); automation with scripts, `make`, scheduled jobs, continuous integration, and pre-commit hooks ([sec-automation](#sec-automation)); and how to keep API keys and passwords out of your code with environment variables ([sec-secrets](#sec-secrets)).

##### Part VII — Algorithmic Systems

The last part is about the AI tools that are now part of almost every workflow. It starts with using AI assistants well: deciding how much to check an answer, prompting for help you can act on, and protecting your privacy and academic integrity ([sec-ai-llm](#sec-ai-llm)). Then it looks under the hood at how language models work: tokens and context windows, sampling and temperature, embeddings, the difference between a chatbot and an API, tool calling, and why models make things up ([sec-llm-internals](#sec-llm-internals)). It goes on to AI agents, where a model works through many steps and calls tools on its own, and the ways those systems fail ([sec-ai-agents](#sec-ai-agents)). It closes with evaluating and auditing AI outputs: building a test set, measuring quality, and checking for bias ([sec-evaluating-ai](#sec-evaluating-ai)).

After a short conclusion, two appendices close the book: a glossary of the terms the chapters use ([sec-glossary](#sec-glossary)) and a disclosure of how AI tools were used to write this handbook ([sec-ai-disclosure](#sec-ai-disclosure)).

## 1.4 Acknowledgements

This guide grew out of conversations and materials developed by [Brian C. Keegan](https://www.brianckeegan.com/) and [Abram Handler](https://www.abehandler.com/) at the University of Colorado Boulder’s [Department of Information Science](https://www.colorado.edu/cmdi/infoscience). It was also developed with the help of AI tools; [sec-ai-disclosure](#sec-ai-disclosure) says exactly how. It draws on the collective wisdom of many students, colleagues, and practitioners who have shared their experiences of the hidden curriculum of computing, and the authors are grateful to everyone who has contributed feedback, suggestions, and encouragement along the way.

Edwards, Richard. 2015. “Software and the Hidden Curriculum in Digital Education.” *Pedagogy, Culture & Society* 23 (2): 265–79.

Wing, Jeannette M. 2006. “Computational Thinking.” *Communications of the ACM* 49 (3): 33–35.
