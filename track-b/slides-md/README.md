# Track B Markdown teaching decks

These seven Marp Markdown decks develop concepts incrementally. B0 prepares the Python subset through supply-chain examples. B1–B3 follow the revised progression: a chatbot using learned model knowledge → tools and a shared MCP server → multi-step investigation, specialist coordination and human review. Code excerpts illustrate concepts introduced by the preceding text and diagrams.

## Teaching order

| Order | Deck | Slides | Learning progression |
| --- | --- | ---: | --- |
| Prep | [B0: Python foundations](b0-python-foundations.md) | 38 | Values, collections, control flow, functions, checks, objects, dates, JSON and configuration; follow-on storage, decorators, API, async, logs and tests |
| 1 | [B1: LLM applications](b1-llm-applications.md) | 33 | Application/model roles, proprietary/open weights, hosted/local inference, instructions, conversations, tokens, generation, context limits, cost and latency |
| 2 | [B2: Tools, agents and MCP](b2-tools-and-mcp.md) | 31 | Direct function, tool contract, requests and observations, decision/feedback loop, runtime comparison, reuse, MCP ownership, shared HTTP server and an optional second client |
| 3 | [B3: Agents that manage a task](b3-agentic-workflows.md) | 36 | Prescribed and adaptive execution, plans and observations, specialists as tools, handoffs, parallel work, sessions, task state and real approval/resumption |
| 4 | [B4: Enterprise data](b4-enterprise-data.md) | 31 | Useful query, bound values, join error, grain repair, narrow capability, ownership scope, proposed SQL, effect/work limits and provenance |
| 5 | [B6: RAG and agentic RAG](b6-rag-and-agentic-rag.md) | 37 | Working RAG, pipeline objects, chunks, embeddings, retrieval, synthesis, baseline evaluation, failure-driven repairs and bounded retrieval tools |
| 6 | [B5: Safety, observability and evaluation](b5-safety-observability-evaluation.md) | 34 | Wrong fact, exact checks, expected cases, side effects, traces, resource evidence, diagnosis, same-case repair, advisory judge and integrated improvement |

**240 slides including B0 preparation; 202 across B1–B6.** Teach B0 before B1 when needed, then B1, B2, B3, B4, B6, B5. B0 has no new time allocation. B1–B3 include a 60-minute lecture pacing guide in their opening notes. Their [TODO lab packs](../labs/README.md) provide standalone and PortOps versions with incremental checkpoints. B4–B6 retain their earlier scope; their slide counts do not imply a teaching-hour allocation.

## Reading the decks

Each slide performs one step in a longer explanation. Read adjacent slides together: the earlier slide supplies the example, evidence or distinction needed by the next. Tables and summaries generally consolidate mechanisms already introduced. New requirements and visible failures motivate additional components.

Presenter notes are embedded as HTML comments. They explain what to point at, likely confusion, what learners should observe, and the bridge to the next slide. They also distinguish prepared cases from actual model output and clarify the limits of small examples.

The decks use several teaching structures deliberately:

- B0 introduces ordinary Python concepts before their small container-service illustrations; the application bridge opens mechanisms used by later libraries.
- B1 explains the language feature and access choices before the first call. Conversations motivate history; tokens and generation explain context and operating constraints. Its required chatbot has no internal records, documents or tools.
- B2 starts with the missing fact, explains the tool interaction and agent loop, then illustrates two runtimes. A reuse problem motivates MCP before server/client code appears.
- B3 expands one synthetic shipment investigation through adaptive execution, specialist coordination, retained progress and human decisions. It builds on B2's loop and MCP foundations.
- B4 begins with a useful read and introduces data correctness and governance through concrete failure cases.
- B6 shows a working whole, opens its parts, reassembles it and then pairs each failure with a matching repair.
- B5 develops an improvement loop from a wrong result and independently specified expectations.

Visible code excerpts make an already explained mechanism inspectable. They may shorten an instruction, name an inline value, or select one stage of a full script. Source links identify the complete runnable files with setup and execution. Use the current [B1 snippets](../snippets/b1/README.md), [B2 snippets](../snippets/b2/README.md) and [B3 snippets](../snippets/b3/README.md). B4–B6 still contain earlier detailed source references and need their own reconciliation before teaching.

## Examples and activities

- [Shared model configuration](../../MODEL_SETUP.md)
- [Track B setup](../SETUP.md)
- [Standalone snippets and code-alongs](../snippets/README.md)

All operational records, hours, fees and policies are synthetic classroom examples. B1 uses hosted OpenAI and local SmolLM2 through Ollama/LiteLLM. B2/B3 use the OpenAI Agents SDK and LlamaIndex with GPT-4.1-mini. B2's two MCP agent clients use one independently running local HTTP server. B3's core examples keep sessions, task data and pending approvals in memory. Its separate persistence follow-ons use temporary storage; the approval action affects a local demonstration outbox. B6 also needs an embedding route. A skip is not a successful live model, retrieval or agent run.

Run and edit the selected complete script during the code-along after its conceptual explanation. Then apply the mechanisms in the [B1–B3 labs](../labs/README.md): unfinished learner functions sit above complete scaffolding, with matching standalone and PortOps API versions. Earlier activity starters, solutions and later-module labs retain older requirements. Enterprise identity, managed credentials and durable recovery remain later topics.

## Foundation and scope

The source teaching patterns come from [the earlier AI engineering decks](../../bfsi__ai-engineering-27_July_5days/SLIDES-markdown/README.md): M1-M3 for model-backed applications; M7/M10 for tools and MCP; M8/M9 for workflow and product closure; M11/M12 for data capabilities and governance; M4/M5 for RAG; and M9/M13 for verification and testing.

This folder is the revised Markdown collection. The source BFSI files, existing `track-b/modules/b*/slides.md` and B4–B6 module labs retain their separate scope. B1–B3 module lab entrypoints link the current TODO packs. Temporary HTML/image renders used to inspect B1–B3 are not part of the Markdown teaching set.
