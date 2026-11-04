# Maersk AI Engineering — Consolidated Content Summary

**As of:** 1 November 2026  
**Program:** The Modern AI Developer / Maersk AI Train the Trainer Enablement  
**Purpose:** A single overview of the curriculum, teaching approach, current materials, reference projects and remaining work.

## 1. Program overview

The program develops two complementary engineering capabilities:

- **Track A — AI-Augmented Software Development:** use coding assistants and agents to understand, implement, test, review and deliver software changes.
- **Track B — Agentic AI Application Building:** build application features that use models, tools, enterprise data and retrieval within explicit execution, evaluation and human-review boundaries.

The audience is software developers and infrastructure engineers, including Maersk trainer nominees. The wider Train the Trainer engagement aims to prepare internal SMEs to deliver the material independently.

The current content comprises **11 technical modules: five in Track A and six in Track B**. B6 was added after the original ten-module planning baseline. The curriculum retains historical three-day/hour allocations, but explicitly states that these have not been recalculated for the expanded content. Delivery timing remains to be agreed.

Primary planning sources:

- [Current Track A/B curriculum](curriculum/Maersk_Track_A_and_B_Curriculum_v5.docx.md)
- [Train the Trainer proposal](curriculum/Maersk_Proposal_1_Train_the_Trainer_Revised.docx.md)
- [Original v4 curriculum](curriculum/THE%20MODERN%20AI%20DEVELOPER%20%E2%80%94%20v4%20-%20Maersk.md), retained as historical scope reference

## 2. Current content at a glance

| Material | Current inventory | Status / boundary |
| --- | ---: | --- |
| Track A Markdown slides | 5 decks, 118 slides | Authored with presenter notes; repository code is illustrative |
| Track B Markdown slides | 6 decks, 193 slides | Authored with presenter notes; some detailed excerpts still reference archived examples |
| Total Markdown teaching slides | **11 decks, 311 slides** | Content-review inventory, not an agreed duration |
| Track B essential code-alongs | **28 Python files** | Selected standalone worked examples; final verification/consolidation remains |
| Track B PowerPoint slides | 6 decks, 193 slides | Pandoc exports with native text, code, tables and presenter notes |
| Track A demonstration repository | Not delivered as a separate runnable pack | Slide illustrations define its intended progression |
| Labs | Deferred | Earlier documents and starter/solution packs remain reference material |
| Capstone | Existing PortOps reference and AI extension | Final Maersk use case and integration scope remain to be selected |
| Trainer-enablement package | Defined in the proposal | Do not infer completion from technical slide availability |

Start with the current indexes:

- [Track A slide index](track-a/slides-md/README.md)
- [Track B slide index](track-b/slides-md/README.md)
- [Track B essential snippet/code-along index](track-b/codealongs/README.md)
- [Track B PowerPoint index](track-b/slides-pptx/README.md)
- [All six Track B PowerPoint decks — ZIP](track-b/slides-pptx/Track_B_PowerPoint_Decks.zip)

## 3. Track A — AI-Augmented Software Development

### Modules and learning progression

| Module | Core content | Teaching progression | Slides |
| --- | --- | --- | ---: |
| **A1 — Foundations and Context Engineering** | Model/agent foundations, prompts, acceptance criteria, repository instructions, context failures and model choice | Understand a function; expose ambiguity in a change request; agree criteria; supply relevant code, instructions and design decisions | 25 |
| **A2 — Coding, Testing, Debugging and Refactoring** | Feature changes, reviewed tests, defect reproduction, regression checks, caller integration and behaviour-preserving refactoring | Turn criteria into tests; inspect an implementation; reproduce a precedence bug; repair it; verify the caller and reject unsuitable suggestions | 25 |
| **A3 — Team Development with Coding Agents** | Branches, worktrees, focused PRs, AI-assisted review, human review, CI and reusable task instructions | Make the local change understandable to a teammate; isolate work; prepare a PR; inspect findings and current-revision checks | 23 |
| **A4 — Harness, Security and Quality** | Deterministic checks, hooks, permissions, hostile context, isolation, schema validation and execution evidence | Observe a failure or missing check; introduce the relevant mechanism; repeat the attempt; inspect what was enforced | 23 |
| **A5 — Brief to a Validated PR** | Requirements, context, tests, implementation, review, CI, remaining risk and rollback | Integrate A1–A4 into one evidence-backed merge-or-hold decision | 22 |

### Shared teaching example

Track A grows a small **synthetic shipment-status service**:

1. The baseline returns `delayed` for negative `hours_to_eta` and `on_time` otherwise, including zero.
2. The change adds an optional `cancelled=False` argument.
3. Cancellation takes precedence over ETA classification and returns `cancelled`.
4. Existing calls that omit the flag preserve their earlier behaviour.
5. Tests, caller handling, review and delivery evidence develop around this same change.

The same example culminates in a focused PR with reviewed tests, check results, known limitations and a human decision. These are classroom rules, not Maersk operating policies.

### Teaching unit

Track A uses **a small repository task, an exact assistant request and observable engineering evidence**. Evidence can be a diff, test result, review finding or denied action. A5 consolidates the previously taught practices rather than introducing another tool survey.

The slide code, file tree and commands are illustrations for a future prepared repository. The slides do not establish that a runnable repository, CI workflow, hook configuration or sandbox exercise has already been delivered.

## 4. Track B — Agentic AI Application Building

### Teaching order and essential examples

Teach **B1 → B2 → B3 → B4 → B6 → B5**. B6 retains its identifier while appearing before the closing evaluation module.

| Module | Essential learning | Selected examples | Files | Slides |
| --- | --- | --- | ---: | ---: |
| **B1 — From LLMs to AI Applications** | Model calls, instructions, context, history, structured output, validation and model selection | First call; system instruction; supplied context; conversation history; JSON output; Pydantic schema; model comparison | 7 | 29 |
| **B2 — Tools, Function Calling and MCP** | Function contracts, model proposals, host execution, correlated observations and external capabilities | Function/schema; complete tool round trip; MCP server; MCP client | 4 | 30 |
| **B3 — Agentic Workflow Design** | Fixed versus routed execution, state, observation-driven decisions, bounded autonomy, framework mapping and human review | Chain/router; bounded manual agent loop; LlamaIndex agent; review/save/reload state | 4 | 32 |
| **B4 — Enterprise Data, Knowledge and Actions** | SQL meaning, schema-grounded query generation, independent validation and scoped access | Query/grain repair; generated SQL with a known reference; narrow governed read | 3 | 31 |
| **B6 — RAG and Agentic RAG** | Document grounding, chunks, metadata, embeddings, retrieval, repairs and query engines as tools | First RAG; chunks/metadata; retrieval inspection/scope; hybrid search; reranking; query rewriting; agentic RAG | 7 | 37 |
| **B5 — Safety, Observability and Evaluation** | Expected cases, actual traces, diagnosis, measured repair and advisory judgment | Evaluate/repair; trace actual work; rubric-based judge after factual checks | 3 | 34 |
| **Total** | | | **28** | **193** |

Each module's [code-along index](track-b/codealongs/README.md) links the actual filenames and explains why each example is essential.

### The first LLM call establishes the foundation

The first example explicitly teaches:

1. Import `dotenv` and LiteLLM.
2. Load `OPENAI_API_KEY` from `.env`.
3. Select an OpenAI model through LiteLLM.
4. Supply OpenAI-format messages.
5. Extract and print the returned text.

[First LLM call source](track-b/codealongs/b1/01_first_llm_call.py):

```python
import os
from dotenv import load_dotenv
from litellm import completion

load_dotenv()

response = completion(
    model="openai/gpt-4.1-mini",
    api_key=os.environ["OPENAI_API_KEY"],
    messages=[{"role": "user", "content": "What is container dwell time?"}],
)
print(response.choices[0].message.content)
```

Subsequent examples repeat the understood foundation and introduce a meaningful addition. Instructions change behaviour; context supplies facts; history supports follow-ups; parsing and schemas establish accepted application data.

### Scope of the selected set

A curriculum bullet does not automatically require another script. Pattern comparisons, policy catalogues, metric arithmetic and conceptual extensions can be taught in slides where another runnable file adds little understanding.

The current examples use synthetic container records, terminal notes and classroom policies. SQLite supports the small SQL demonstrations; DuckDB, approved warehouse views and enterprise services remain applicable deployment choices. Local JSON events introduce tracing; a hosted Langfuse integration is not implemented by those trace examples.

## 5. Agreed teaching and code-authoring principles

### Slides teach through a sequence

The earlier [BFSI slide collection](bfsi__ai-engineering-27_July_5days/SLIDES-markdown/README.md) supplies the instructional foundation.

- Start from something the learner already understands.
- Establish a concrete need before introducing the mechanism that addresses it.
- Give each slide one teaching step within a longer explanation.
- Keep the example and terminology stable while introducing the next concept.
- Show the important code, request, result or trace on the slide.
- Introduce complexity after the simpler version exposes a limitation.
- Use failures to explain the need for a particular repair or control.
- Place comparison tables after enough concrete experience to interpret them.
- Reassemble the complete workflow after explaining its parts.
- Use presenter notes for the spoken explanation, likely confusion and bridge to the next slide.

The sequence can differ by topic. RAG uses a working whole, its parts and a reconstructed whole. Tool use builds the pieces of a round trip. Advanced retrieval pairs a diagnosed failure with a matching repair.

### Snippets and code-alongs share one file

A **snippet** is a complete worked example. A **code-along** is running and editing that same file with the instructor. **Labs are separate work and remain deferred.**

The selected scripts follow library-quickstart style:

- One essential purpose, small inputs and a visible result.
- Direct calls to the relevant library or Python operation.
- Self-contained data and explicit necessary setup.
- No capstone dependency, hidden teaching helper or generic factory.
- Repetition where it makes a file independently understandable.
- No arbitrary line cap that encourages compressed or fragmented code.
- A small learner change that reveals the mechanism's effect.
- Real model operations when configured; prepared inputs identified honestly.

MCP is the intentional two-file exception because its server/client process boundary is part of the lesson.

## 6. Tooling and environment

| Area | Current material |
| --- | --- |
| Coding assistance | Claude Code and GitHub Copilot workflows, subject to approved access |
| Team delivery | Git, worktrees, PRs, CI and CodeQL or an approved equivalent |
| Model calls | LiteLLM with explicit OpenAI models in the introductory examples |
| Key loading | `python-dotenv`, with the real key supplied locally |
| Structured validation | Python JSON handling and Pydantic |
| Tool connectivity | MCP server/client |
| Framework agents and RAG | LlamaIndex, with OpenAI-compatible chat and embedding adapters |
| Teaching data | Inline synthetic records/documents and disposable SQLite databases |
| Observability/evaluation | Actual local trace events, deterministic checks and advisory model judgment |
| Slide sources | Marp Markdown with presenter notes |
| PowerPoint conversion | Pandoc with a widescreen reference theme and native editable objects |

Use [Track B setup](track-b/SETUP.md) for the selected examples. Base dependencies are in [requirements-teaching.txt](track-b/requirements-teaching.txt); the B3 framework example and B6 also require [requirements-rag.txt](track-b/requirements-rag.txt).

The first-call teaching path deliberately uses direct hosted OpenAI access. [MODEL_SETUP.md](MODEL_SETUP.md) retains the broader OpenAI-compatible gateway/local-service reference. Adapting the selected scripts to another deployment is a later variation, not a prerequisite for understanding the first call.

The model IDs in examples are explicit teaching settings, not a recommendation that they are the latest or best choice. Check account availability before delivery. Never commit actual API keys.

## 7. Reference projects and capstone

### Original PortOps sandbox

[PortOps / SupplyChainOps](project-supplychain-sandbox-PortOps/README.md) is an existing deterministic logistics reference covering container dwell, demurrage calculations, claims, terminal events and dispatch. It provides a possible integration base rather than a prerequisite for the standalone lessons.

### Preserved Track B AI extension

[PortOps Exception Assistant](track-b/CAPSTONE.md) describes an educational extension that gathers scoped operational facts, drafts a recommendation, records execution evidence and preserves a human review boundary.

Its documented distinction is important: an approved recommendation does not itself execute an operational waiver, gate-out action or message delivery. The reference uses synthetic data and classroom identities.

Standalone B6 retrieval is available as teaching content, but the preserved capstone documentation explicitly says document-RAG integration is not yet implemented in that runtime.

### Final Maersk capstone

The final business problem remains to be selected with Maersk SMEs. A Logistics Exception Resolution Agent is illustrative, not a confirmed production design.

The planning intention is two milestones:

1. **Track A:** a validated software change and review evidence.
2. **Track B:** a bounded application workflow with approved tools/data, review boundaries, traces and evaluation.

Current teaching follows small standalone mechanisms first, with larger integration afterward. Do not treat older statements that every lesson already extends one common application as an accurate description of the current example set.

## 8. Train the Trainer scope

The proposal adds a trainer-development journey to the technical content:

| Component | Intended coverage |
| --- | --- |
| Teach, demo and prepare | Explanation, demonstrations, preparation and demo-failure handling |
| Lab handling and troubleshooting | Supporting mixed speeds and diagnosing setup/code issues |
| Questions and classroom management | Handling unknowns, participation and pacing |
| Full-class preparation and reflection | Readiness checks, feedback and delivery improvement |

Two observed teaching-practice rounds are proposed, with feedback and improvement between them. Readiness outcomes are:

- Ready to Deliver Independently.
- Ready with Initial Support.
- Requires Additional Practice.

The proposed module teaching pack contains slides, a standard lab, an assessment and a capstone checkpoint. Technical decks alone do not establish that this full trainer-enablement package is complete.

## 9. Current versus historical material

| Location | How to use it |
| --- | --- |
| `curriculum/` | Current planning documents plus historical v4 scope |
| `track-a/slides-md/` | Current Track A Markdown decks |
| `track-b/slides-md/` | Current Track B Markdown decks |
| `track-b/slides-pptx/` | Pandoc PowerPoint exports and the six-deck ZIP |
| `track-b/codealongs/b1` through `b6` | Current selected 28-file teaching path |
| `track-b/modules/` | Module indexes plus older outlines, slides, assessments and lab documents; check current indexes first |
| `track-b/teaching-snippets/` and `track-b/snippets/` | Earlier collections retained as reference |
| `track-b/authoring/previous-codealongs-before-essential-selection/` | Previous larger code-along collection and starter/solution packs |
| Other `track-b/authoring/previous-*` folders | Earlier teaching designs and expanded examples |
| `track-b/slides-html/` | Earlier HTML previews; do not assume they reflect current Markdown |
| `bfsi__ai-engineering-27_July_5days/` | Source-client teaching material and runnable reference patterns |

## 10. Readiness and remaining work

The following are remaining tasks, not claims of completed delivery:

1. **Review the Markdown content.** Confirm technical accuracy, pacing and the example sequence with the trainer and stakeholders.
2. **Finish slide/example alignment.** Some detailed Track B excerpts still link to archived mechanisms. The required practice set is the 28-file selection; align classroom instructions and relevant excerpts with it.
3. **Update verification tooling.** The existing `verify_quickstart_codealongs.py` still expects the previous 47-file set and offline-skip behaviour. It must be revised before it can validate the current 28-file selection reliably.
4. **Verify the selected examples in the delivery environment.** Compile/local checks are distinct from actual model, embedding, tool-selection and retrieval runs. Earlier verification results for superseded collections do not validate the new set.
5. **Build Track A demonstration checkpoints.** Prepare the small repository, tests, approved tool setup, CI and isolated control demonstrations represented in the slides.
6. **Develop labs later.** Existing lab starters and documents are retained reference material, not evidence that the revised lab path is complete.
7. **Finalise the capstone.** Agree the Maersk scenario and decide which current reference components to reuse.
8. **Prepare and assess the TTT stages.** Complete the trainer-facing packs, observed practice and readiness process.
9. **Recalculate delivery time.** The expanded eleven-module scope needs a new agenda rather than the original ten-module allocation.
10. **Refresh exports after content changes.** Regenerate the PowerPoint decks when the Markdown changes; Track A PowerPoint decks have not been created in the current inventory.

### Verification boundary for this summary

The inventory was checked against the local files on 1 November 2026: 118 Track A slides, 193 Track B slides, 28 selected Track B Python files and six PowerPoint decks containing 193 slides and 193 notes pages. This confirms artifact presence and structure, not successful live delivery or complete application behaviour.
