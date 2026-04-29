# 37  Working with AI Agent Frameworks

> **TIP:**
>
> **Prerequisites (read first if unfamiliar):** [sec-llm-internals](#sec-llm-internals), [sec-scripts-vs-notebooks](#sec-scripts-vs-notebooks).
>
> **See also:** [sec-ai-llm](#sec-ai-llm), [sec-evaluating-ai](#sec-evaluating-ai).

## Purpose

![Confession Bear Meme: I let my agent run overnight, it deleted all my files.](../../graphics/memes/ai-agents.png)

A chatbot answers one question at a time. An AI agent is different: it uses a language model as a reasoning engine, equips it with tools, and lets it take a sequence of actions — calling APIs, reading files, searching the web, running code — to complete a goal that may take many steps.

Agent frameworks have become a major pattern in applied AI work. You will encounter them in research pipelines, data processing workflows, software development assistants, and automated systems. Understanding how they work — what the agentic loop is, how tools are defined and invoked, how memory is managed, and where these systems reliably fail — puts you in a position to use them deliberately rather than being surprised when something goes wrong.

This chapter builds on the model internals from [sec-llm-internals](#sec-llm-internals) and the responsible-use practices from [sec-ai-llm](#sec-ai-llm). Where those chapters focus on individual prompts and outputs, this one focuses on *systems*: sequences of model calls, tool invocations, and decision points that can touch real data, real services, and real consequences.

## Learning objectives

By the end of this chapter, you should be able to:

1.  Describe the four core components of an AI agent

2.  Trace the steps of an agentic loop and identify where failures typically occur

3.  Compare two or three major agent frameworks and articulate when each is appropriate

4.  Define a tool with a well-written description and input schema

5.  Explain the difference between in-context memory and external memory

6.  Read an agent trace and identify what the model decided and why

7.  Describe at least three failure modes specific to agentic systems

8.  Apply human-in-the-loop checkpoints to limit the blast radius of agent errors

## Running theme: trust but verify at every step

An agent that works in a demo can fail catastrophically in production. The autonomy that makes agents useful — they keep going without you — is also what makes their failures hard to catch. Build in checkpoints, keep tools narrowly scoped, and treat agent actions as irreversible until proven otherwise.

## 37.1 From chatbot to agent

A chatbot is a single-turn or multi-turn conversation: you send a message, the model responds. An agent extends this with four components working together.

**Model.** A language model is the agent’s reasoning engine. It receives context, decides what to do next, and either produces a final answer or decides to invoke a tool.

**Tools.** Functions the model can call to take actions or retrieve information. Tools might query a database, read a file, call an external API, run a shell command, or search the web. The model does not execute these directly — it generates a structured request, and your code runs the function.

**Memory.** The information available to the model across steps. This includes in-context history (what has happened so far in this run), external memory (documents or records retrieved from a store), and sometimes longer-term memory persisted across runs.

**Planning loop.** The control structure that decides when to keep going and when to stop. Some agents are simple loops: call the model, execute tool, repeat. Others have more complex planning structures with explicit goal decomposition and reflection steps.

The key difference between a chatbot and an agent is *action*: an agent can change things in the world, not just describe them. That distinction matters because it changes the stakes of errors. A chatbot that hallucinates gives you bad text; an agent that hallucinates may delete a file, send a message, or make an API call you did not intend.

## 37.2 The agentic loop

The core of every agent is a loop that alternates between model reasoning and action execution. The pattern is sometimes called **observe–think–act**:

1.  **Observe**: The agent receives the current state — the user goal, any prior tool results, conversation history, and retrieved context.

2.  **Think**: The model reasons about the current state and decides what to do next: invoke a tool, ask a clarifying question, or produce a final answer.

3.  **Act**: If the model decides to use a tool, your code executes the tool and returns the result to the model. The result becomes part of the next observation.

4.  **Repeat**: Steps 1–3 repeat until the model produces a final answer or a stop condition is reached.

A minimal agentic loop looks like:

    while not done:
        response = model.call(context)
        if response.has_tool_call():
            result = execute_tool(response.tool_call)
            context.append(result)
        else:
            final_answer = response.text
            done = True

Several things can go wrong in this loop:

- The model loops indefinitely, calling tools repeatedly without converging.

- A tool call fails and the error message is not informative enough for the model to recover.

- The context grows with each iteration until it hits the context window limit.

- The model decides it is done but the task is actually incomplete.

Building a robust agent means designing for these failure paths, not just the happy path.

## 37.3 Overview of agent frameworks

Several frameworks exist to help you build agents without implementing the loop, tool management, and memory yourself. Each makes different trade-offs.

### LangChain

[LangChain](https://python.langchain.com/docs/introduction/) is a comprehensive Python and JavaScript library for building LLM-powered applications. It provides abstractions for chains (sequential model calls), agents (loop-based reasoning), tools, memory, and retrieval. LangChain has a large ecosystem of integrations with databases, APIs, and model providers.

*Best for:* Teams that want a batteries-included framework with many pre-built components. Its abstraction layer is useful for rapid prototyping but can obscure what is happening underneath.

### LlamaIndex

[LlamaIndex](https://docs.llamaindex.ai/en/stable/) (formerly GPT Index) focuses on retrieval-augmented generation: connecting language models to structured and unstructured data. It provides data loaders, index types, and query engines that make it easier to build knowledge-retrieval pipelines.

*Best for:* Applications that center on querying documents, PDFs, databases, or APIs — where the primary challenge is getting the right information into context.

### Claude Agent SDK / Anthropic API

Anthropic’s Claude models support tool use natively through the Messages API. The [Anthropic documentation](https://docs.anthropic.com/en/docs/agents-and-tools/) describes patterns for building agents directly using the API without a framework, giving you full control over the loop.

*Best for:* Teams who want to minimize abstraction and understand exactly what is being sent to the model. Also appropriate when you need to integrate tightly with existing code.

### CrewAI

[CrewAI](https://docs.crewai.com/) provides a higher-level abstraction: you define *agents* (with roles and goals) and *tasks* (with descriptions and expected outputs), and CrewAI orchestrates the agents working together.

*Best for:* Multi-agent workflows where different agents play different roles (researcher, writer, reviewer) and need to hand off work to each other.

### When to skip a framework

Frameworks add complexity, dependencies, and a layer of abstraction between you and the model. For a simple two-step agent (retrieve data, summarize it), implementing the loop directly with the model’s API is often clearer and easier to debug. Start simple and add framework complexity only when you genuinely need what the framework provides.

## 37.4 Defining and registering tools

The quality of your tool definitions directly determines whether the model uses tools correctly. A poorly described tool will be called with wrong arguments, called at the wrong time, or ignored entirely.

A good tool definition has three parts:

**Name.** Short, descriptive, underscore-separated. The model will refer to this in its reasoning. `search_documentation` is better than `tool1` or `doTheSearch`.

**Description.** A clear natural-language explanation of what the tool does, when to use it, and what it returns. The model reads this description to decide whether to call the tool. Vague descriptions produce unpredictable calls.

**Input schema.** A JSON schema defining the parameters the tool accepts, with types and descriptions for each parameter. Mark required parameters explicitly.

Example of a well-defined tool:

    {
      "name": "query_database",
      "description": "Run a read-only SQL SELECT query against the
        project database. Use this when you need to look up records,
        counts, or aggregates. Do not use for INSERT, UPDATE, or DELETE.
        Returns a list of rows as JSON objects.",
      "input_schema": {
        "type": "object",
        "properties": {
          "sql": {
            "type": "string",
            "description": "A valid SQL SELECT statement."
          }
        },
        "required": ["sql"]
      }
    }

Principles for writing tool descriptions:

- Say what the tool does *and* when to use it.

- Describe what the tool *does not* do (e.g., “read-only, no writes”).

- Describe the return format so the model knows how to interpret the result.

- Keep descriptions focused; one tool, one purpose.

- Expose only tools the agent actually needs for the current task.

Restricting tool access is a safety practice, not just housekeeping. An agent that has access to a “send email” tool might use it unexpectedly. Only expose tools the agent needs for the specific workflow you are running.

## 37.5 Memory types

Memory determines what information is available to the model as it works. Different memory types serve different purposes.

### In-context memory

Everything currently in the context window: the user’s original request, tool call results, prior responses, system prompt. This is the only memory that directly influences the model’s next decision.

*Limitation:* Bounded by the context window. Long-running agents will eventually fill the context, at which point older information must be summarized or dropped.

### External memory: vector stores

A vector database stores document embeddings and retrieves semantically similar documents at query time. When the agent needs background information, it embeds the query, retrieves relevant documents, and injects them into context.

*Use case:* Knowledge retrieval, documentation search, “chat with your documents” applications. Allows the agent to work with document collections far larger than any context window.

### External memory: structured databases

Relational or key-value databases that the agent queries via a tool (like the `query_database` example above). Structured memory is better than vector search when you need exact lookups, counts, or joins rather than similarity matching.

### Episodic and long-term memory

Some agent frameworks support persisting a summary of past sessions to a store, then loading relevant summaries at the start of new sessions. This gives the appearance of memory across conversations. It is more complex to implement and comes with privacy considerations: be deliberate about what you store and how long you keep it.

## 37.6 Multi-step reasoning patterns

How the model reasons through a multi-step problem — not just that it uses tools, but how it structures its thinking — significantly affects reliability.

### Chain-of-thought

Prompting the model to “explain your reasoning step by step” before producing an answer. This does not change the model’s architecture, but it primes the model to generate intermediate reasoning steps that are more likely to be correct than jumping directly to an answer.

Use chain-of-thought for: multi-step calculations, logical deductions, ambiguous categorizations, debugging.

### ReAct (Reason + Act)

A prompting pattern where the model alternates between **reasoning** (“I need to find the latest version of this library”) and **action** (calling a tool to do so). The reasoning step is made explicit in the output, which makes traces easier to read and debug.

A ReAct trace looks like:

    Thought: I need to check the current pandas version.
    Action: run_shell_command({"command": "pip show pandas"})
    Observation: Name: pandas, Version: 2.2.1
    Thought: The user has pandas 2.2.1. I can now answer the question.
    Answer: You are running pandas 2.2.1.

### Reflection

After the agent produces an initial answer or plan, it reviews its own output and identifies potential errors or improvements. Reflection adds one or two additional model calls but catches mistakes that would otherwise be missed.

*When to use:* High-stakes decisions, structured outputs that must be valid (JSON schema, SQL), or any step where an error would be costly to detect later.

### Reading agent traces

Agent frameworks typically log traces: the sequence of model calls, tool invocations, and results. Reading traces is a critical debugging skill. When an agent fails, the trace tells you:

- What context the model had when it made a bad decision

- Which tool call was wrong, and what arguments it used

- Whether the error was in the model’s reasoning or in the tool execution

- Where in the loop the failure propagated

## 37.7 Orchestrating multi-agent systems

Some tasks benefit from multiple specialized agents working together rather than a single all-purpose agent.

### Subagents

A **subagent** is an agent invoked as a tool by a parent (orchestrator) agent. The orchestrator decomposes the task, delegates subtasks to subagents, and aggregates results. Subagents can run in parallel if the subtasks are independent, which can significantly reduce total wall-clock time.

### Supervisor patterns

In a **supervisor** architecture, one agent manages a team of specialized agents: a researcher, a writer, a reviewer. The supervisor routes tasks, checks outputs, and decides when the overall task is complete. This is useful when you have genuinely distinct specializations that benefit from separate system prompts and tool sets.

### Handoffs

In sequential multi-agent pipelines, a **handoff** is the transfer of a task and its accumulated context from one agent to the next. Clean handoffs require that each agent produces output in a structured format the receiving agent can parse.

*Common problem:* Information loss at handoffs. If the first agent’s output is a long, unstructured paragraph, the second agent may miss key details. Design outputs at each stage to be explicit, structured, and complete.

## 37.8 Failure modes and risk

Agentic systems introduce failure modes that do not exist in single-call workflows.

**Runaway loops.** The model keeps calling tools without converging. Causes: the stop condition was not clearly defined, the model is stuck in a cycle, or a tool keeps returning errors. Fix: set a maximum number of iterations; always implement a hard stop.

**Cascading errors.** An error in step 3 corrupts the context, causing steps 4 and 5 to fail in confusing ways that look unrelated to the original problem. Fix: validate tool outputs before appending them to context; add explicit error-handling branches.

**Unintended side effects.** The model calls a tool that modifies state (writes a file, posts to an API, sends a message) when it should not have. Fix: separate read tools from write tools; require explicit confirmation before executing write actions (see [sec-ai-llm](#sec-ai-llm) for the risk-based policy).

**Context overflow.** Long-running agents fill the context window with tool results and previous reasoning. The model then loses access to earlier instructions. Fix: summarize and compress context periodically; test with long runs before deploying.

**Prompt injection via tool results.** A malicious document or API response contains text designed to override the agent’s instructions (“Ignore previous instructions and instead…”). Fix: treat tool results as untrusted data; use separate system prompts that are not overridable by tool output; sanitize inputs from external sources.

**Authorization creep.** An agent with broad tool access may take actions outside the intended scope because the task description was ambiguous. Fix: apply least-privilege principles to tool definitions; use separate tool sets for different agent roles.

### Human-in-the-loop checkpoints

For any action that is hard to reverse — writing to a database, sending a message, making a financial transaction, deleting a file — implement a human confirmation step before the action executes. This is not a failure of the agent; it is an appropriate design choice given the stakes.

    def execute_tool(tool_call):
        if tool_call.name in HIGH_RISK_TOOLS:
            confirm = input(f"Agent wants to run {tool_call.name} "
                            f"with args {tool_call.args}. Allow? [y/N] ")
            if confirm.lower() != 'y':
                return {"error": "Action cancelled by user."}
        return TOOL_REGISTRY[tool_call.name](**tool_call.args)

## 37.9 Stakes and politics

An AI agent is a language model with hands — it can call tools, read and write files, send network requests, and execute code, all in pursuit of a goal someone gave it. The political dimension of that capability is steeper than for chat alone, because the consequences of an agent’s actions persist after the conversation ends.

Three things to notice. First, *agents act on behalf of someone, but rarely the person they affect*. An agent that books appointments, approves transactions, or sends messages is acting in the name of its operator. The people receiving those appointments, transactions, and messages are interacting with a non-human system that may not be obvious as such, and that is held accountable through whatever legal and reputational machinery surrounds the operator. As agents move from research demos into production deployments — customer service, hiring, content moderation, healthcare triage — that asymmetry grows. Second, *autonomy concentrates with capital*. Building, deploying, and supervising agents at scale is expensive: long-running compute, monitoring infrastructure, observability tooling, the team that watches for misbehavior. Individuals can build small agents on their laptops; operating them on the scale that makes business sense requires a budget that filters out everyone except established companies and well-funded startups. The promise that “anyone can have an agent” is real for hobby projects and false for the deployments that affect millions of people.

Third, *the alignment problem is a labor problem too*. Aligning an agent to behave well — refusing dangerous tool calls, escalating to humans, respecting the user’s intent — requires the same RLHF and red-teaming labor that aligning chat models does (see [sec-ai-llm](#sec-ai-llm)). The “human in the loop” the framework documentation cheerfully assumes is, at scale, a contracted reviewer with a quota and a queue.

See [sec-artifacts-politics](#sec-artifacts-politics) for the broader framework, [sec-ai-llm](#sec-ai-llm) for the user-side workflow, [sec-llm-internals](#sec-llm-internals) for the model under the hood, and [sec-evaluating-ai](#sec-evaluating-ai) for how we test whether an agent is actually doing what we asked. The concrete prompt to carry forward: when you build or deploy an agent, ask whose goals it is optimizing for and whose interests it might harm without telling them.

## 37.10 Worked examples

### Building a research agent with document retrieval

You want an agent that can answer research questions by first searching a document corpus, then synthesizing an answer with citations. The minimum design has two tools: a `search_documents` tool that does vector search over your corpus and returns the top-k document IDs and snippets, and a `read_document` tool that fetches the full text of a document by ID. You then write a system prompt that explicitly tells the agent to *search first*, cite the sources it used, and acknowledge uncertainty when the retrieved documents do not contain the answer. Test the loop with three to five real research questions and read the trace carefully — you are watching for the agent to use retrieval in the cases where it should and to *not* invent answers when nothing is found. Once that core loop works, add a reflection step: after producing an initial answer, the agent re-reads its own answer and identifies any gaps, optionally searching again to fill them. As the conversation grows, monitor how much context each turn consumes and set a threshold at which older results get summarized rather than passed forward verbatim, so the agent does not run out of context window in the middle of a long session.

### Converting a multi-step notebook workflow into an agent

You have a notebook with five distinct stages — load data, clean it, run analysis, generate figures, write a report — and you want to wrap it in an agent that can run any subset on demand. Walk through the notebook and identify which steps involve *decisions* (which file to load, which analysis to run, whether to retry on failure) versus pure transformations. The decision points are where an agent helps; the pure transformations should stay as plain functions. Wrap each stage in a tool with a clear input schema (`load_data(path)`, `run_analysis(table)`, `generate_report(results)`) and write a system prompt that describes the overall goal and explains when each tool should be called. Test the agent end-to-end on a known sample dataset, and compare its outputs to the manual notebook outputs to confirm they match. Critically, add a **human-in-the-loop checkpoint** before any tool that touches shared output — the report generation step is the natural place — so a person reviews the analysis before it gets distributed.

### Diagnosing a misbehaving agent from its trace

An agent ran in production and produced the wrong result. The first move is to **reproduce the failure** and capture the *full* trace: every model call, every tool call, every result, every token in context at every step. Then walk the trace from the beginning until you find the **first place where the output diverged** from the expected behavior. That step is your suspect. From there, ask two questions. Was the failure in the **model’s reasoning** (the model had the right context but drew a wrong conclusion), or was it in the **tool’s execution** (the tool returned a confusing or incorrect result that fed bad data into the model)? And did the model have the **context it needed** at the moment of the bad decision, or had something earlier been pushed out of the window or never included? Once you have a hypothesis, isolate the failing prompt — copy the exact context the model saw at that step into a standalone API call — and verify that you can reproduce the bad output deterministically. Then fix the cause: tighten the tool’s return format, expand the system prompt, add a validation step that catches the bad output before it propagates, or shrink the context. Add a regression test that exercises the same scenario, and your future self will thank you.

## 37.11 Exercises

1.  Find documentation or a blog post for one of the frameworks mentioned in this chapter (LangChain, LlamaIndex, CrewAI, or a direct API approach). Summarize in one paragraph: what problem it is designed for, what its main abstractions are, and one trade-off compared to building an agent directly with the API.

2.  Write a tool definition (name, description, input schema) for a function that retrieves all rows from a CSV file where a specified column matches a given value. Pay attention to the description: include what the tool does, when to use it, and what it returns.

3.  Sketch (in pseudocode or plain English) a two-agent system where one agent collects information and a second agent writes a summary. What does the handoff look like? What structured format should the first agent produce so the second agent can use it reliably?

4.  Consider an agent that can read files, write files, and send emails. Classify each tool as low-risk, medium-risk, or high-risk according to the framework from [sec-ai-llm](#sec-ai-llm). For the high-risk tools, describe what a human-in-the-loop checkpoint would look like.

5.  Read an example agent trace from any framework’s documentation. Identify: (a) where the model decides to call a tool, (b) what information the tool returned, (c) whether the model’s decision was correct given what it knew. Describe one thing you would change about the tool definition or system prompt to improve the agent’s behavior.

## 37.12 One-page checklist

- Confirm the task genuinely requires multiple steps before building an agent; use a direct API call for single-step tasks

- Set a maximum iteration count to prevent runaway loops

- Write tool descriptions that explain what the tool does, when to use it, and what it returns

- Expose only the tools an agent needs for its specific role; remove tools that are not needed

- Classify tools by risk (read-only vs. write vs. irreversible); add confirmation prompts before high-risk actions

- Log full traces (model calls, tool calls, results) so failures can be diagnosed

- Test the agentic loop with adversarial inputs and edge cases, not just the happy path

- Monitor context size across long runs; implement context summarization before the window fills

- Treat tool results from external sources as untrusted; sanitize inputs that could contain prompt injection

- Add human-in-the-loop checkpoints for any action that cannot be easily undone

> **NOTE:**
>
> - Anthropic, [Building agents with the Claude API](https://docs.anthropic.com/en/docs/agents-and-tools/overview) — patterns and examples for tool use and agentic loops; includes the “human in the loop” pattern this chapter recommends.
> - Anthropic, [Building effective agents](https://www.anthropic.com/research/building-effective-agents) — a research-blog post on minimal, robust agent designs; a useful counterweight to over-engineered framework abstractions.
> - LangChain, [Agents documentation](https://python.langchain.com/docs/tutorials/agents/) — a framework-level walk-through of agent construction.
> - OpenAI, [Function calling guide](https://platform.openai.com/docs/guides/function-calling) — the canonical reference for defining tools the model can invoke.
> - Shunyu Yao et al., [ReAct: Synergizing Reasoning and Acting in Language Models](https://arxiv.org/abs/2210.03629) (ICLR 2023) — the paper that named the “reason then act” loop most agent frameworks now implement.
> - Sayash Kapoor and Arvind Narayanan, [AI Agents That Matter](https://www.aisnakeoil.com/p/ai-agents-that-matter) — practitioner critique of agent benchmarks; useful counterweight to demo-driven hype.
> - LangSmith, [Tracing and observability documentation](https://docs.smith.langchain.com/) — the most widely used commercial observability layer for agent runs; the “log full traces” advice in this chapter is best operationalized with a tool like this.
