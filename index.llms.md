# Missing Manual for Information Scientists

The hidden curriculum of computing technologies

Author

Brian C. Keegan

Published

April 2026

# 1 Introduction

## 1.1 Why this handbook?

Students’ early encounters with programming are often frustrating. Not because the computational concepts are hard to understand, but because there is so much assumed knowledge about the other involved computing technology that leaves them feeling confused and powerless. New software needs to be used, but it does not come with its own installer. New kinds of files need to be opened, but they do not open on a double click. Instructors flip between different screens and it is confusing what is happening where. It can feel like you missed a class where others learned about using all these other technical components that you are now assumed to know!

![](graphics/frustrated_computer.png)

A student and a computer in mutual frustration.

You are not alone in this feeling. Computing education has been long been criticized for relying on a hidden curriculum of skills and tools that are used but not taught in classrooms.([Edwards 2015](#ref-edwardsSoftwareHiddenCurriculum2015)) Why are these skills not formally taught? Instructors take their own expertise for granted, believe other topics deserve a higher priority, assume that students quickly learn them on their own, and want someone else to teach these overlooked skills. The “[spiral of silence](https://en.wikipedia.org/wiki/Spiral_of_silence)” leaves students with the mistaken belief that they are alone in their confusion being expected to use tools that have not been introduced before. All these factors lead to unproductive and compounding frustrations between instructors, students, and computers.

Unfortunately, it is important to learn how to cope with and work through such frustrations. A surprisingly large fraction of your time as a developer, designer, analyst, scientist, or researcher is spent *managing* software in addition to using it. This includes installing, updating, and configuring libraries; consulting technical documentation and issue tracking to help debug problems; and integrating with external resources to connect to data and collaborate with others. These are headaches for advanced users and can be particularly demoralizing as a newcomer. But there is no way to avoid these challenges in real world workplaces, so it is important to learn to manage them yourself.

Some vendors promise their platform or service can take care of this complexity for you. Cloud platforms like [Google colab](https://colab.research.google.com/), Amazon Web Services [SageMaker](https://docs.aws.amazon.com/sagemaker/), [Kaggle](https://www.kaggle.com/code), and others do take care of some parts of the software management. But there is no such thing as a free lunch and these platforms involve compromises like compounding financial costs, lock-in to proprietary services, and other issues of accessibility, usability, and compatibility. There can be scenarios where managed and cloud-based services are appropriate, but when those “clean” virtual machines, environments, containers, and services are no longer available (or break unexpectedly), you will not be empowered to debug or develop on your own. There is simply no escaping the need to be confident managing your own technology stack.

## 1.2 Computational thinking

Computational thinking is the disciplined way that computer scientists and data analysts approach problems ([Wing 2006](#ref-wingComputationalThinking2006)). At its core it is *not* about memorizing syntax but about how to break a problem down and express a solution so that a computer can execute it. Novice students often hear instructors say “think like a computer,” but what does that mean? Four skills stand out:

- **Decomposition.** Break a large, ambiguous task into smaller pieces you can tackle one at a time. For example, downloading a dataset, cleaning it, analyzing it, and visualizing it are separate steps even if they feel like one fluid process when an instructor demonstrates them. Each step should have clear inputs and outputs.

- **Pattern recognition.** Look for similarities across examples and problems. If you have cleaned one CSV file by renaming columns and dropping missing values, you can reuse that process on another dataset. Recognizing patterns helps you avoid reinventing the wheel and informs what should be turned into a function or reusable script.

- **Abstraction.** Identify the essential details and ignore the distracting ones. A function that computes a mean does not need to know whether its input came from a spreadsheet or a database. Abstracting away unnecessary details makes your code more flexible and easier to test.

- **Algorithmic thinking.** Specify a sequence of unambiguous steps to transform your inputs into outputs. This is the heart of programming: you describe a procedure so precisely that a computer could perform it. Good algorithms include checks for error conditions and handle exceptional cases gracefully.

Computational thinking is not just for coding assignments. It is a way to reason about problems in data science, research, and daily life. Throughout this handbook you will practice applying decomposition, pattern recognition, abstraction, and algorithmic thinking to activities like organizing files, managing environments, automating workflows, and collaborating with others.

## 1.3 Outline

This handbook is organized into seven parts that gradually build up a novice’s paratechnical competence. Each part moves from foundational concepts to concrete skills and ends with small exercises and checklists so that you can assess your own mastery.

##### Part I–Practice of Technical Work.

We begin with the human side of computing. You will learn how to ask specific, reproducible questions when you need help, how to find and write technical documentation, how to read and write the common text formats your tools rely on, how to read official documentation efficiently, how to debug systematically using decomposition, testing, and logging, how to read Python tracebacks, and how to think about the politics of the artifacts you build. These chapters establish habits for lifelong learning and communication.

##### Part II–Your Computing Environment.

Next we explore the physical and software environment in which code runs. Chapters cover maintaining your operating system, navigating and organizing the local file system on Windows and macOS, working safely in a terminal, choosing and using text editors, and connecting to remote machines via SSH, VPN, and cloud services. Mastery of these topics prevents many “mysterious” errors.

##### Part III–Python Working Context for Data Work.

With a stable environment in place, we turn to managing Python itself. You will learn about package managers (`conda` and `pip`), creating and using virtual environments, launching and troubleshooting Jupyter Notebook and JupyterLab, deciding when to use notebooks versus scripts, working with regular expressions, and adopting consistent code style with linting and formatting tools. A chapter on scripts shows how to write importable modules, add commandline interfaces, and convert between notebooks and scripts.

##### Part IV–Working with Data.

The next part is about the day-to-day craft of working with data. Chapters cover the common data file formats you will encounter, the principles of tabular data (wide vs. tidy, cleaning, and validation), the pandas idioms you will reach for most often, the SQL basics that translate between dataframes and databases, and how to talk to the web through HTTP and APIs.

##### Part V–Communication.

Computing is most of what an information scientist does, but communication is what makes the work count. This part covers the genres you will be asked to produce: how to read scholarly articles and books efficiently, how to write scholarly manuscripts for conferences and journals, how to write a thesis (MS, monograph, or three-paper), how to present your work in talks of every length, and how to use LaTeX and BibTeX to produce the documents themselves. The chapters can be read independently, and they cross-reference each other and the rest of the book.

##### Part VI–Shipping and Sustaining Projects.

We then address how to make your work reproducible and collaborative. Chapters introduce lightweight project management (project briefs, reproducible structure, data hygiene, documentation, and issue tracking), version control with Git and GitHub (commits, branches, pull requests, forks, and merge conflict resolution), collaboration mechanics (writing and reviewing code, comment etiquette, and decision logging), automation (scripts, task runners, scheduling, continuous integration, and responsible AI assistance), and how to manage environment variables and secrets. Together these skills enable you to deliver reliable work in teams.

##### Part VII–Algorithmic Systems.

This final part goes deeper into how modern AI systems work and how to work with them as a practitioner. Where earlier chapters cover responsible AI use in everyday workflows, Part VII covers the internals and infrastructure: what tokens and context windows are, how embeddings enable semantic search, how to construct effective prompts, and what changes when you call a model via API rather than a chatbot. A second chapter covers AI agent frameworks where a language model reasons across multiple steps and invokes external tools including how to define tools, manage memory, read agent traces, and guard against the failure modes unique to agentic pipelines. A third chapter addresses evaluation and auditing: how to measure AI system quality systematically, build representative test suites, use automated evaluators, and audit for bias and drift in deployed applications.

## 1.4 Acknowledgements

This guide was adapted from conversations and materials developed by [Brian C. Keegan](https://www.brianckeegan.com/) and [Abram Handler](https://www.abehandler.com/) at the University of Colorado Boulder’s [Department of Information Science](https://www.colorado.edu/cmdi/infoscience). The material was also developed with the use of LLM tools, please read the [AI disclosure statement](parts/appendix/appendix-ai-disclosure.llms.md). It draws on the collective wisdom of many students, colleagues, and practitioners who have shared their experiences and insights about the hidden curriculum of computing. The authors are grateful to all those who have contributed to this project through feedback, suggestions, and encouragement.

Edwards, Richard. 2015. “Software and the Hidden Curriculum in Digital Education.” *Pedagogy, Culture & Society* 23 (2): 265–79.

Wing, Jeannette M. 2006. “Computational Thinking.” *Communications of the ACM* 49 (3): 33–35.
