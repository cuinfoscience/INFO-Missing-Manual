# Paratechnical Computing Handbook

The hidden curriculum of computing for data scientists

Authors

Brian C. Keegan

Abram Handler

Published

April 2026

# 1 Introduction

## 1.1 Why this handbook?

Students’ early encounters with programming are often frustrating. Not because the computational concepts are hard to understand, but because there is so much assumed knowledge about the other involved computing technology that leaves them feeling confused and powerless. New software needs to be used, but it does not come with its own installer. New kinds of files need to be opened, but they do not open on a double click. Instructors flip between different screens and it is confusing what is happening where. It can feel like you missed a class where others learned about using all these other technical components that you are now assumed to know!

![](graphics/frustrated_computer.png)

A student and a computer in mutual frustration.

You are not alone in this feeling. Computing education has been long been criticized for relying on a hidden curriculum of skills and tools that are used but not taught in classrooms.[^1] Why are these skills not formally taught? Instructors take their own expertise for granted, believe other topics deserve a higher priority, assume that students quickly learn them on their own, and want someone else to teach these overlooked skills. The “spiral of silence”[^2] leaves students with the mistaken belief that they are alone in their confusion being expected to use tools that have not been introduced before. All these factors lead to unproductive and compounding frustrations between instructors, students, and computers.

Unfortunately, it is important to learn how to cope with and work through such frustrations. A surprisingly large fraction of your time as a developer, designer, analyst, scientist, or researcher is spent *managing* software in addition to using it. This includes installing, updating, and configuring libraries; consulting technical documentation and issue tracking to help debug problems; and integrating with external resources to connect to data and collaborate with others. These are headaches for advanced users and can be particularly demoralizing as a newcomer. But there is no way to avoid these challenges in real world workplaces, so it is important to learn to manage them yourself.

Some vendors promise their platform or service can take care of this complexity for you. Cloud platforms found on Google,[^3] Amazon Web Services,[^4] Kaggle,[^5] and others do take care of some parts of the software management. But there is no such thing as a free lunch and these platforms involve compromises like compounding financial costs, lock-in to proprietary services, and other issues of accessibility, usability, and compatibility. There can be scenarios where managed and cloud-based services are appropriate, but when those “clean” virtual machines, environments, containers, and services are no longer available (or break unexpectedly), you will not be empowered to debug or develop on your own. There is simply no escaping the need to be confident managing your own technology stack.[^6]

## 1.2 Computational thinking

Computational thinking is the disciplined way that computer scientists and data analysts approach problems. At its core it is *not* about memorizing syntax but about how to break a problem down and express a solution so that a computer can execute it. Novice students often hear instructors say “think like a computer,” but what does that mean? Four skills stand out:

- **Decomposition.** Break a large, ambiguous task into smaller pieces you can tackle one at a time. For example, downloading a dataset, cleaning it, analyzing it, and visualizing it are separate steps even if they feel like one fluid process when an instructor demonstrates them. Each step should have clear inputs and outputs.

- **Pattern recognition.** Look for similarities across examples and problems. If you have cleaned one CSV file by renaming columns and dropping missing values, you can reuse that process on another dataset. Recognizing patterns helps you avoid reinventing the wheel and informs what should be turned into a function or reusable script.

- **Abstraction.** Identify the essential details and ignore the distracting ones. A function that computes a mean does not need to know whether its input came from a spreadsheet or a database. Abstracting away unnecessary details makes your code more flexible and easier to test.

- **Algorithmic thinking.** Specify a sequence of unambiguous steps to transform your inputs into outputs. This is the heart of programming: you describe a procedure so precisely that a computer could perform it. Good algorithms include checks for error conditions and handle exceptional cases gracefully.

Computational thinking is not just for coding assignments. It is a way to reason about problems in data science, research, and daily life. Throughout this handbook you will practice applying decomposition, pattern recognition, abstraction, and algorithmic thinking to activities like organizing files, managing environments, automating workflows, and collaborating with others.

## 1.3 Defining paratechnical skills

We use the term “paratechnical skills” to refer to the tools, practices, and concepts used by computing professionals that exist *between* different technical components and therefore *beyond* traditional curricula and documentation.

## 1.4 Outline

This handbook is organized into four parts that gradually build up a novice’s paratechnical competence. Each part moves from foundational concepts to concrete skills and ends with small exercises and checklists so that you can assess your own mastery.

##### Part I–Practice of Technical Work.

We begin with the human side of computing. You will learn how to ask specific, reproducible questions when you need help, how to find and write technical documentation, how to debug systematically using decomposition, testing, and logging, and how to incorporate AI/LLM tools responsibly into your workflow. These chapters establish habits for lifelong learning and communication.

##### Part II–Your Computing Environment.

Next we explore the physical and software environment in which code runs. Chapters cover maintaining your operating system, navigating and organizing the local file system on Windows and macOS, working safely in a terminal, choosing and using text editors, adopting baseline security practices and backups, and connecting to remote machines via SSH, VPN, and cloud services. Mastery of these topics prevents many “mysterious” errors.

##### Part III–Python Working Context for Data Work.

With a stable environment in place, we turn to managing Python itself. You will learn about package managers (`conda` and `pip`), creating and using virtual environments, launching and troubleshooting Jupyter Notebook and JupyterLab, and deciding when to use notebooks versus scripts. A chapter on scripts shows how to write importable modules, add commandline interfaces, and convert between notebooks and scripts.

##### Part IV–Shipping and Sustaining Projects.

Finally we address how to make your work reproducible and collaborative. Chapters introduce lightweight project management (project briefs, reproducible structure, data hygiene, documentation, and issue tracking), version control with Git and GitHub (commits, branches, pull requests, forks, and merge conflict resolution), collaboration mechanics (writing and reviewing code, comment etiquette, and decision logging), and automation (scripts, task runners, scheduling, continuous integration, and responsible AI assistance). Together these skills enable you to deliver reliable work in teams.

##### Part V–Algorithmic Systems.

This final part goes deeper into how modern AI systems work and how to work with them as a practitioner. Where Part I covers responsible AI use in a single workflow, Part V covers the internals and infrastructure: what tokens and context windows are, how embeddings enable semantic search, how to construct effective prompts, and what changes when you call a model via API rather than a chatbot. A second chapter covers AI agent frameworks — systems where a language model reasons across multiple steps and invokes external tools — including how to define tools, manage memory, read agent traces, and guard against the failure modes unique to agentic pipelines. A third chapter addresses evaluation and auditing: how to measure AI system quality systematically, build representative test suites, use automated evaluators, and audit for bias and drift in deployed applications.

## 1.5 Acknowledgements

This guide was adapted from documentation, tutorials, and other resources listed below.

- Documentation

  - [Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html).

  - [Anaconda Individual Edition](https://docs.anaconda.com/anaconda/).

  - [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/stable/).

  - [Terminal User Guide](https://support.apple.com/guide/terminal/welcome/mac).

- Tutorials

  - Pugh, D.R. (2020). “[Getting Started with Conda](https://towardsdatascience.com/managing-project-specific-environments-with-conda-b8b50aa8be0e).”

  - Galarnyk, M. (2019). “[Installing Anaconda on Windows.](https://www.datacamp.com/community/tutorials/installing-anaconda-windows)”

  - Willems, K. (2019). “[Jupyter Notebook Tutorial](https://www.datacamp.com/community/tutorials/tutorial-jupyter-notebook).”

  - Stegner, B. (2021). “[A Beginner’s Guide to the Windows Command Prompt](https://www.makeuseof.com/tag/a-beginners-guide-to-the-windows-command-line/).”

- Courses

  - Eubank, N. (2020). *[Practical Data Science](https://www.practicaldatascience.org/html/index.html)*.

  - Athalye, A., Ortiz, J.J.G., Gjengset, J. (2020). *[Missing Semester of Your CS Education](https://missing.csail.mit.edu/)*.

[^1]: Edwards, R. (2015). [Software and the hidden curriculum in digital education](https://www.tandfonline.com/doi/abs/10.1080/14681366.2014.977809). *Pedagogy, Culture & Society*, 23(2), 265-279.

[^2]: <https://en.wikipedia.org/wiki/Spiral_of_silence>

[^3]: <https://colab.research.google.com/>

[^4]: <https://docs.aws.amazon.com/sagemaker/>

[^5]: <https://www.kaggle.com/code>

[^6]: <https://www.practicaldatascience.org/html/setting_up_your_computer.html>
