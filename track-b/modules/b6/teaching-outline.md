# B6 teaching intentions

Module question: How do we find usable evidence before asking a model to answer, and when should retrieval become a decision?

## 1 · Make the evidence path visible
- Separate retrieval (selecting supplied material) from generation (writing an answer).
- Trace document → chunk → metadata → embedding → index → ranked nodes.
- Explain chunk size as a tradeoff between focused matching and preserved context.
- Predict how a split can separate a rule from its exception; repair and transfer to a new note.
- Explain why proximity in embedding space establishes neither truth nor permission.

## 2 · Establish a fixed RAG baseline
- Inspect top-k node IDs and scores before introducing synthesis.
- Predict whether increasing k guarantees a better answer; reveal noise and context cost.
- Connect explicit embedding/chat adapters to a compatible endpoint.
- Run a real query engine and compare individual claims with source nodes.
- Diagnose retrieval miss separately from unsupported synthesis; abstain when evidence is absent.

## 3 · Choose patterns from failure evidence
- Apply trusted terminal metadata before ranking and generation.
- Compare lexical matching with semantic matching; fuse ranks without equating raw scores.
- Predict why reranking cannot repair a candidate set that lacks the answer.
- Inspect original and rewritten self-contained queries for preserved subject, constraints and intent; explain why follow-up rewriting additionally needs explicit history.
- Use an observed failure and measurable cost to justify one pattern, rather than stacking all patterns.

## 4 · Make adaptive retrieval bounded and observable
- Contrast a fixed pipeline with model-chosen tool calls based on prior observations.
- Inspect a FunctionAgent retrieval trace and distinguish declared support from actual endpoint behavior.
- Keep tool scope fixed by the application and enforce stopping outside the model's instructions.
- Explain that multi-step fixed retrieval is not automatically agentic.

## 5 · Evaluate and transfer
- Compute precision@k, recall@k and reciprocal rank from supplied relevance labels.
- Treat retrieval quality and answer faithfulness as separate evaluation targets.
- Trace a worked evidence evaluation, complete a guided scoped evaluation, then design an unsupplied failure-driven transfer.
- Explain what a passing fixture establishes and what still needs live model validation.

## Teaching mechanisms and guided activities

Use [ten core snippets and one optional extension](../../teaching-snippets/b6/README.md) with separate predictions, reasoned reveals and experiments. The [three-activity plan](codealong-plan.md) maps these to the five existing snippets.

| Activity | Snippets | Existing checkpoints |
| --- | --- | --- |
| Baseline evidence path | s01 chunks, s02 embeddings, s03 top-k, s04 synthesis | 01–03 |
| Chosen failure-driven repair | s05 scope, s06 hybrid, s07 rerank, s08 rewrite, s10 evaluation | 04 hybrid or selected snippet |
| Bounded agent retrieval | s09 decisions, observations and stopping | 05 |

Optional context expansion extends chunk boundaries with a real sentence-window postprocessor over a supplied candidate. It is not a required eleventh topic. Evaluation starts from prepared labels/rankings and transfers to actual retrieval outputs; neither establishes answer faithfulness alone.
