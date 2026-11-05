# TODO later · B4, B5 and B6

Saved: 4 November 2026. Intended next working session: 5 November 2026.

Status: deferred curriculum proposal. Work on B3 first. This checklist records the discussion; individual teaching choices still need refinement before implementation.

## Starting point and proposed sequence

B1 covers hosted/local model access and a general-knowledge chatbot. B2 introduces tools, agent runtimes and shared MCP capabilities. B3 is being discussed as multi-step agentic work, orchestration, delegation, state and human review.

Proposed continuation:

| Module | Central question | Resulting capability |
| --- | --- | --- |
| B4 · Enterprise systems and actions | How does the agent work with business systems? | API/database-backed tools and controlled actions |
| B5 · RAG and agentic RAG | How does it use internal document knowledge? | Retrieval, source-grounded answers and retrieval as an agent tool |
| B6 · Evaluation, observability and reliability | How do we verify behaviour and improve it? | Evaluation cases, execution traces, safeguards and measured repair |

**Numbering is provisional.** The existing B5 files cover evaluation and the existing B6 files cover RAG. The proposal swaps their teaching positions and identifiers. No renaming has been performed. Confirm the final arrangement before moving files or updating links.

## Shared authoring requirements

- [ ] Retain the working assumption of one hour of lecture and one hour of lab per module; confirm scope against this budget.
- [ ] Teach each concept through text and explanation before using a simplified snippet to illustrate it.
- [ ] Progress from a concrete problem to a small working example, then expose the mechanism and its limits.
- [ ] Use short, standalone documentation-style examples customized for synthetic Maersk shipping scenarios.
- [ ] Execute actual library/model/service calls. Clearly label synthetic records; do not replace execution with canned successful output.
- [ ] Reuse the preceding modules' concepts and domain vocabulary without making every example depend on a large shared project.
- [ ] Keep required examples few enough to teach properly; use edits and extensions for variations.
- [ ] Use `load_dotenv()` and `OPEN_AI_KEY` consistently with the revised B1/B2 examples when configuring hosted model calls.
- [ ] Introduce permissions, limits and basic execution evidence when first needed. B6 consolidates and tests them.
- [ ] Keep slide decks, snippet guides, setup instructions and labs aligned with the final teaching order.

## B4 · Enterprise systems and actions

Example task: check shipment facts and create a draft exception case in a local training service.

### Teaching progression

- [ ] Bridge from B2/B3: a tool's contract can stay familiar while its implementation changes from a dictionary to an enterprise service.
- [ ] Wrap one HTTP API with a narrow business tool; explain inputs, response mapping, timeout and controlled errors.
- [ ] Add one database-backed read using parameterized queries and bounded results.
- [ ] Explain useful data contracts: identifiers, units, source, freshness and explicit missing/error outcomes.
- [ ] Enforce caller scope and permissions in the application/service boundary using trusted caller identity.
- [ ] Distinguish read operations from actions that change records.
- [ ] Demonstrate action preview, human approval and execution. Relate this to B3's approval lifecycle.
- [ ] Explain duplicate-action prevention and what happens after rejection or failure without expanding into a full distributed-systems lesson.

### Scope decisions

- [ ] Reuse MCP knowledge from B2; avoid another protocol introduction.
- [ ] Make API/database integration the main lesson. Reduce the existing emphasis on SQL syntax and join mechanics.
- [ ] Keep text-to-SQL as a comparison or optional extension; distinguish generated proposals from independently enforced permissions and execution restrictions.
- [ ] Choose a small local service or reuse a suitable existing training service; keep records synthetic and setup manageable.

### Lab and artifacts

- [ ] Define a lab outcome: an agent using a real local API/database, showing an allowed request, a denied request and a controlled action.
- [ ] Select a small core snippet sequence, then author/refine slides and lab instructions around the conceptual progression.
- [ ] Verify successful calls, unknown IDs, forbidden scope, service failure and the approve/reject paths.

## B5 · RAG and agentic RAG — proposed numbering

Example task: explain which supplied exception-handling SOP applies to a shipment's observed circumstances.

### Teaching progression

- [ ] Begin with a question that business tools cannot answer because the answer lives in documents.
- [ ] Supply one short document directly, then motivate retrieval for a larger collection.
- [ ] Explain document loading, chunks, metadata, embeddings, indexing and query-time retrieval.
- [ ] Build a working retrieval-to-answer baseline with inspectable source evidence.
- [ ] Distinguish a retrieval miss from an answer unsupported by the retrieved material.
- [ ] Include an unsupported-question case and explain the expected abstention behaviour.
- [ ] Demonstrate one observed failure and one chosen repair, such as hybrid retrieval for exact identifiers.
- [ ] Expose retrieval as an agent tool alongside shipment/business tools from the preceding modules.
- [ ] Contrast a fixed RAG pipeline with model-selected retrieval based on observations.

### Scope decisions

- [ ] Use LlamaIndex for the concrete RAG examples, building on the framework exposure in B2/B3.
- [ ] Configure the embedding and generation models explicitly as separate capabilities.
- [ ] Prioritize understanding the baseline over teaching a catalogue of retrieval techniques.
- [ ] Keep additional reranking, query rewriting and context-expansion techniques as extensions unless the final timing supports one of them.
- [ ] Preserve source identity and apply trusted document scope before evidence reaches the model.

### Lab and artifacts

- [ ] Define a lab outcome: an assistant combining shipment facts with cited SOP evidence.
- [ ] Prepare a tiny document collection, supported questions, an unsupported question and one deliberate retrieval failure.
- [ ] Select the core snippets and align slides, lab and setup instructions.
- [ ] Verify actual embeddings, returned chunks, source evidence and agent tool execution; inspect quality separately from successful API execution.

## B6 · Evaluation, observability and reliability — proposed numbering

Example task: diagnose and improve the assembled shipment assistant using evidence from the same evaluation cases before and after a change.

### Teaching progression

- [ ] Define expected behaviour before running the application; prepare a small representative case set.
- [ ] Evaluate factual correctness, tool/action behaviour and document support as separate targets.
- [ ] Inspect traces containing actual model/tool calls, observations, errors, latency and reported usage.
- [ ] Test missing evidence, wrong tool choices, denied access and misleading instructions embedded in tool/document content.
- [ ] Revisit the enforcement boundaries introduced earlier: caller permissions, allowed operations, budgets and human approval.
- [ ] Connect an observed failure to its responsible layer, make one targeted repair and rerun the same cases.
- [ ] Add a regression case for the learned failure.
- [ ] Introduce rubric-based model judging for subjective qualities such as clarity, after deterministic checks of known facts.
- [ ] Explain what the small evaluation establishes and what remains uncertain.

### Scope decisions

- [ ] Make the main outcome measured improvement, supported by traces and cases.
- [ ] Reuse earlier safeguards rather than teaching every safety mechanism from scratch here.
- [ ] Start with visible local execution evidence; choose an external tracing/evaluation integration only if it adds enough teaching value for the time and setup.
- [ ] Keep model judging advisory; it does not supply action authorization or replace known-answer checks.

### Lab and artifacts

- [ ] Define a lab outcome: a documented failure, its trace, a targeted repair and a before/after comparison.
- [ ] Prepare representative cases covering normal behaviour, missing information, forbidden actions and resource limits.
- [ ] Select the core snippets and align slides, lab and setup instructions.
- [ ] Run relevant checks against actual execution and retain enough evidence to reproduce the comparison.

## Source material and resumption checklist

- [Day 3 curriculum](</Users/ajinkyak/Desktop/10_October/2-Training-Portflio/workshops-porfolio/ai-engineering-5-days-program-building/a_curriculum/a_final/lod2/ai-for-engineers-building-ai-applications-lod2-day-03-curriculum.md>): M8 orchestration and M9 memory/state/human review primarily inform B3. B4 can build on its review boundary.
- [Day 4 curriculum](</Users/ajinkyak/Desktop/10_October/2-Training-Portflio/workshops-porfolio/ai-engineering-5-days-program-building/a_curriculum/a_final/lod2/ai-for-engineers-building-ai-applications-lod2-day-04-curriculum.md>): M10's MCP introduction is largely covered by B2; M11 informs B4, while M12's controls inform B4 and B6.
- Existing decks: [enterprise data](slides-md/b4-enterprise-data.md), [RAG](slides-md/b6-rag-and-agentic-rag.md), [evaluation](slides-md/b5-safety-observability-evaluation.md).
- Existing snippets: [B4](snippets/b4/README.md), [current B6 RAG](snippets/b6/README.md), [current B5 evaluation](snippets/b5/README.md).

When resuming:

- [ ] Read the finalized B3 scope and establish exactly what learners already know.
- [ ] Resolve the proposed B5/B6 numbering swap.
- [ ] Refine B4's scope and teaching progression first; then B5, then B6.
- [ ] Review existing artifacts for reusable material and stale links before authoring replacements.
- [ ] Finalize the small core examples, slides and labs for each module, then verify them together.
