# Maersk AI Engineering · delivered content summary

Snapshot: **13 November 2026**. This inventory describes the materials in the client release. Start with the [repository guide](README.md); verification is recorded in [RELEASE.md](RELEASE.md).

## Teaching inventory

| Material | Delivered inventory |
| --- | --- |
| Track A | Five Markdown decks, 163 slides; [index](track-a/README.md) |
| Track B | Six core decks, 207 slides; optional B0 adds one deck and 38 slides; [course map](track-b/README.md) |
| Total | 12 decks, 408 slides including B0; 11 core decks, 370 slides excluding B0 |
| Supplied PowerPoints | Five unchanged B1–B5 presentations, 170 slides; [index](track-b/slides-powerpoint/README.md) |
| Core Python snippets | 35 numbered examples across B1–B6; [run guides](track-b/snippets/README.md) |
| Python preparation | 14 B0 snippets plus optional API extension |
| Exploration notebooks | Three notebooks, 39 code cells, distributed with empty outputs; [guide](track-b/notebooks/README.md) |
| Learner labs | Five independent Container Help Desk starters for B1–B5; [guide](track-b/labs/README.md) |
| Reference application | Deterministic PortOps FastAPI/SQLite/Streamlit application, eight seed tables and tests; [setup](project-supplychain-sandbox-PortOps/README.md) |

There is no all-deck PowerPoint ZIP, `codealongs/` folder or separate PortOps AI extension in this release. Five supplied B1–B5 PowerPoints are preserved as-is. Markdown decks are authoritative; local Gamma authoring copies are excluded from the client snapshot. The supplied PowerPoints were checked structurally, not certified as text-identical or visually revalidated.

## Learning progression

Track A covers foundations and context; coding, testing and debugging; team development; quality harnesses; and delivery from brief to a validated PR. Its decks contain demonstrations and discussion cues; a separate runnable checkpoint repository is not included.

Track B is taught in the order **B1 → B2 → B3 → B4 → B6 → B5**. Optional B0 provides Python foundations. B1 introduces model calls and conversations; B2 tools and MCP; B3 bounded workflows, state and review; B4 permitted database access and query evidence; B6 retrieval and agentic RAG; B5 generated-answer evaluation and prompt comparison.

B5's five standalone LlamaIndex examples match its slides and learner lab. Two short SDK/LlamaIndex tracing references remain because the slides link to them. Other evaluation experiments are outside the client snapshot.

## Setup and evidence

[Track B setup](track-b/SETUP.md) specifies the locked B1–B5 environment and separate B6 requirements. [Model configuration](MODEL_SETUP.md) explains the actual key names used by these files. Labs and notebooks document their own environments. PortOps needs no model key.

The release checks cover offline execution, the PortOps and lab suites, source/notebook parsing, local links. Dated verification records retain earlier live model observations and judge disagreements. A passing API call is not evidence of answer quality; no live model or fresh dependency-installation claim is implied by the offline freeze checks.

## Explicit boundaries

B1–B5 labs retain unfinished learner functions; these are not completed solutions or formal assessments. B6 has no learner lab. Trainer teachbacks, SME readiness assessment, production integration, a common AI capstone implementation and the broader Train the Trainer proposal are outside this source release. Existing 30–60-minute lab budgets remain estimates.

Earlier curricula and the Train the Trainer proposal are background documents. This snapshot does not claim that every proposed asset, duration or enablement stage was delivered. Future refinements do not block preservation of this completed teaching assignment.
