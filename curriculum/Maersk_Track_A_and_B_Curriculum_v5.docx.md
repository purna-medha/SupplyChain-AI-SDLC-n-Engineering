# The Modern AI Developer · delivered technical curriculum

Maersk November 2026 teaching snapshot, frozen on **13 November 2026**. Delivered by Ajinkya Kolhe in collaboration with Imarticus Learning. The [repository guide](../README.md) defines the included assets; [RELEASE.md](../RELEASE.md) records verification and limits.

This document describes the supplied technical courseware. The historical v4 curriculum and Train the Trainer proposal describe a broader programme; they are background, not evidence that all proposed assessments, solutions or enablement stages are included here.

## Audience and format

Software developers and infrastructure engineers, including trainer nominees. Teach concepts, demonstrate selected complete examples, then use exploration notebooks or intentional learner TODOs for practice. Timing estimates in module guides exclude setup and are not a validated delivery schedule for all 408 slides.

Track A covers AI as a software-engineering collaborator. Track B covers AI models and agents as application components. The package has five Track A modules, six core Track B modules and optional B0 Python preparation.

## Teaching sequence and materials

| Order | Module | Materials |
| --- | --- | --- |
| A1 | Foundations and context engineering | [Slides](../track-a/slides-markdown/a1-foundations-and-context.md) |
| A2 | Coding, testing, debugging and refactoring | [Slides](../track-a/slides-markdown/a2-coding-testing-debugging-refactoring.md) |
| A3 | Team development with coding agents | [Slides](../track-a/slides-markdown/a3-team-development.md) |
| A4 | Automated quality harness | [Slides](../track-a/slides-markdown/a4-automated-quality-harness.md) |
| A5 | Brief to a validated PR | [Slides](../track-a/slides-markdown/a5-validated-pr-capstone.md) |
| Optional prep | B0 · Python foundations | [Slides](../track-b/slides-md/b0-python-foundations.md) · [Snippets](../track-b/snippets/b0/README.md) |
| B1 | Models, messages, tokens and cost | [Slides](../track-b/slides-md/b1-llm-applications.md) · [Snippets](../track-b/snippets/b1/README.md) |
| B2 | Tools, agents and MCP | [Slides](../track-b/slides-md/b2-tools-and-mcp.md) · [Snippets](../track-b/snippets/b2/README.md) |
| B3 | Workflows, specialists, state and approval | [Slides](../track-b/slides-md/b3-agentic-workflows.md) · [Snippets](../track-b/snippets/b3/README.md) |
| B4 | Querying enterprise data with AI agents | [Slides](../track-b/slides-md/b4-enterprise-data.md) · [Snippets](../track-b/snippets/b4/README.md) |
| B6 | RAG and agentic RAG | [Slides](../track-b/slides-md/b6-rag-and-agentic-rag.md) · [Snippets](../track-b/snippets/b6/README.md) |
| B5 | Generated-answer evaluation and prompt improvement | [Slides](../track-b/slides-md/b5-safety-observability-evaluation.md) · [Snippets](../track-b/snippets/b5/README.md) |

Keep module identifiers unchanged: **B1 → B2 → B3 → B4 → B6 → B5**. [Setup](../track-b/SETUP.md) and [model configuration](../MODEL_SETUP.md) describe the actual delivered environments and key names.

## Track A outcomes

**A1:** prepare repository context and acceptance criteria, understand model/context limitations, and retain responsibility for engineering decisions.

**A2:** investigate code, implement a focused change, reproduce a defect, review tests and validate a refactor rather than trusting generated output.

**A3:** use shared context, isolated work, review evidence and human merge decisions when collaborating with coding agents.

**A4:** explain and demonstrate automated quality feedback and execution controls in the workflow illustrated by the deck.

**A5:** connect brief, acceptance criteria, implementation, checks, review and rollback into a justified delivery decision.

The five decks include demonstrations and discussion prompts. A separate runnable Track A checkpoint repository, completed module solutions and formal assessments are not included. The supplied deterministic [PortOps baseline](../project-supplychain-sandbox-PortOps/README.md) is available for repository exploration and change exercises.

## Track B outcomes and practice

### B1 · Model calls, messages and tokens

Run hosted and local model examples; distinguish instructions, context and conversation history; inspect token IDs, usage, latency and estimated cost. Six standalone examples support a conversation lab and an exploration notebook.

### B2 · Tools, agents and MCP

Start with an ordinary status-read function, advertise its contract, observe the model/runtime/tool round trip, then share capabilities through MCP. The slide-linked SDK example has one completed read tool and a four-turn bound. Five core files support the independent tools/MCP lab and notebook.

### B3 · Bounded workflows, specialists, state and review

Compare application-controlled sequences with agent-selected investigation. Inspect specialist coordination and handoff, conversation memory versus task state, and explicit approval before a local outbox action. Six core examples support the workflow lab and notebook. Persistent-state variations are optional extensions.

### B4 · Permitted structured data and query evidence

Inspect schemas, read a caller-scoped record with bound parameters, generate SQL over an approved projection, check row grain and totals, enforce database restrictions, and use query results inside a bounded agent. Six core examples and a five-TODO learner lab use synthetic, disposable databases. The query/agent steps make real model calls; a successful query does not establish business correctness.

### B6 · RAG and agentic RAG

Build and inspect a document-grounded answer pipeline. Examine chunks, metadata, actual embedding retrieval, hybrid ranking, reranking, query rewriting and a bounded agent using retrieval as a tool. The seven worked examples use synthetic port notes independently of PortOps.

A B6 learner lab, formal assessment and Gamma copy are not included. Chat and embedding adapters are explicitly configured in the source; B6 uses a separate environment and `OPENAI_API_KEY` as documented in setup.

### B5 · Evaluate generated answers and compare prompts

Define independent expectations; generate actual answers; evaluate correctness, grounding and relevance separately; calibrate judges with labelled probes; and compare a prompt change under unchanged evaluation. Preserve failures, judge disagreements and matched case counts. A tie is a legitimate result.

The delivered path is five small LlamaIndex examples using the approved fee snapshot, aligned slides and a five-TODO Container Help Desk lab. Two SDK/LlamaIndex tracing references support execution diagnosis. No hosted observability/evaluation platform, DeepEval/Promptfoo curriculum or production guardrail system is required by this sequence. Those alternative designs are outside this client snapshot.

## Supplied practice assets

- [B1–B3 notebooks](../track-b/notebooks/README.md): three complete exploration notebooks, distributed without outputs. Live branches require explicit opt-in.
- [B1–B5 learner starters](../track-b/labs/README.md): independent Container Help Desk exercises with intentionally unfinished functions; earlier modules need not be completed first.
- [PortOps capstone baseline](../project-supplychain-sandbox-PortOps/Capstone_details.md): deterministic dwell/demurrage, claims, gate-out and read-only trucking visibility. No AI behavior is implemented.
- [Supplied PowerPoints](../track-b/slides-powerpoint/README.md): five B1–B5 presentation files preserved unchanged.
- [Gamma-ready copies](../track-b/slides-gamma/README.md): B0–B5 presentation-import text derived from the authoritative Markdown decks.

## Exclusions and verification boundaries

Formal module assessments, completed learner solutions, a B6 lab, a separate Track A checkpoint pack, a production AI capstone, observed trainer teachbacks and SME readiness certification are not delivered in this source snapshot. The broader Train the Trainer proposal remains a separate programme description.

Lab time budgets are estimates awaiting an instructor dry run. The package uses synthetic records and does not supply enterprise identity, production policies or approved access to external services. Earlier model runs are dated observations; offline freeze checks do not verify present provider availability, model quality or a fresh dependency installation. See [RELEASE.md](../RELEASE.md).
