---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 25px; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 19px; line-height: 1.2; }
---
# B6 · An answer needs an evidence path

How do we find usable evidence before asking a model to answer?

Synthetic terminal notes throughout. Teach after B4 and before B5.

<!-- Source map: ../../teaching-snippets/b6/README.md; guided activity map: codealong-plan.md. Ask what a model can know from a terminal identifier alone. Establish the module question; none of these notes is operational policy. -->

---

# Retrieval and generation answer different questions

Retrieval: which supplied passages might help?

Generation: what answer can be written from those passages?

A failure in either stage can produce a wrong answer.

<!-- Draw two boxes with evidence crossing the boundary. Ask which box to inspect first when a correct-looking answer is unsupported. -->

---

# A tiny corpus makes evidence inspectable

`gate-a`: Terminal A gate opens at 06:00.

`gate-b`: Terminal B gate opens at 08:00.

`reefer-a`: Terminal A reefer desk is beside gate 2.

<!-- Keep these IDs visible. Ask for the correct evidence ID for each question before running retrieval. -->

---

# Chunks are the units retrieved into context

A document is a source. A chunk is a smaller retrievable piece.

Chunk boundaries determine which facts travel together.

Small chunks focus matching; larger chunks preserve more context.

<!-- Open teaching snippet s01_documents_chunks.py. Avoid claiming a universal best chunk size; show the actual node text. -->

---

# Metadata keeps a chunk connected to its source

```python
from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter

doc = Document(text="Terminal A gate opens at 06:00.",
               metadata={"terminal": "A", "source": "gate-a"})
splitter = SentenceSplitter(chunk_size=64, chunk_overlap=0)
nodes = splitter.get_nodes_from_documents([doc])
```

Inspect text and metadata together.

<!-- This is a focused API excerpt; teaching snippet s01 has its complete configuration. Explain inherited provenance before discussing vectors. -->

---

# Predict what a boundary can remove

Prepared changed case:

“Gate opens at 06:00. On Sunday it opens at 09:00.”

A Sunday question retrieves only the first sentence.

What information is missing? What change would you try?

<!-- Pause for predictions. Do not reveal the Sunday answer until learners name the exception and boundary. -->

---

# A rule without its exception is incomplete evidence

The retrieved sentence cannot support the Sunday opening time.

Keep the rule and exception together, or retrieve adjoining context.

Then re-run the Sunday question and inspect the selected text.

<!-- Optional extension: teaching-snippets/b6/optional/01_context_expansion.py expands a supplied match using actual sentence-window APIs, without embedding search. Reveal 09:00 from the complete prepared document. Overlap may help but does not guarantee semantic completeness; test the changed case. -->

---

# Embeddings make similarity computable

An embedding maps text to a numeric vector.

The same embedding model maps corpus chunks and queries into a comparable space.

Closeness is a relevance signal; it does not establish truth or permission.

<!-- Open teaching snippet s02_embeddings.py. Ask why changing only the query embedding model makes old index vectors unsuitable even if dimensions happen to match. -->

---

# The endpoint needs two distinct capabilities

```python
embedding = OpenAILikeEmbedding(
    model_name=os.environ["COURSE_EMBED_MODEL"],
    api_base=os.environ["OPENAI_API_BASE"],
    api_key=os.environ["OPENAI_API_KEY"],
)
```

Chat writes language. Embeddings create vectors.
`COURSE_MODEL=openai/<alias>` names the chat route.

<!-- Imports and full setup are in the teaching snippets and SETUP. Explain that the adapter receives the chat alias without the LiteLLM openai/ prefix; an embedding route must exist separately. -->

---

# Top-k returns candidates before an answer exists

```python
index = VectorStoreIndex(nodes, embed_model=embedding)
retriever = index.as_retriever(similarity_top_k=2)
hits = retriever.retrieve("When does Terminal A open?")
for hit in hits:
    print(hit.node.node_id, hit.score, hit.node.text)
```

Inspect IDs, scores and text before synthesis.

<!-- Run teaching snippet s03_vector_retrieval.py. Scores depend on model and backend and are not calibrated probabilities of correctness. -->

---

# Predict whether more context guarantees improvement

With k=1, the relevant rule is missing.

With k=3, both terminal rules enter context.

Is the answer now guaranteed to improve? What should we inspect?

<!-- Collect both the possible benefit and possible harm. Do not present a specific live ranking as predetermined. -->

---

# A larger k trades recall for more competing material

More candidates can recover a missing rule.

They can also add irrelevant or contradictory context and token cost.

Measure relevant evidence recovered and inspect the resulting answer.

<!-- Reveal the tradeoff. Have learners change k in teaching snippet s03 and record the real ranking rather than copying an expected list. -->

---

# Fixed RAG connects retrieval to synthesis

```python
engine = index.as_query_engine(llm=llm, similarity_top_k=2)
response = engine.query("When does Terminal A open?")
print(response)
for source in response.source_nodes:
    print(source.node.node_id, source.node.text)
```

The pipeline runs its configured stages for each question.

<!-- Run teaching snippet s04_basic_rag.py with OpenAILike explicitly configured. Offline mode skips real calls; do not substitute prepared wording for model output. -->

---

# Returned sources support inspection, not automatic trust

A source node tells us what evidence entered the response path.

Check each answer claim against the relevant passage.

A cited Terminal A rule does not support an 08:00 claim.

<!-- Compare actual response text with source_nodes. Distinguish evidence availability from claim support; citation formatting alone cannot verify faithfulness. -->

---

# Diagnose the first broken boundary

Required evidence absent → inspect ingestion and retrieval.

Evidence present, claim unsupported → inspect synthesis.

Evidence unavailable anywhere → say it is unavailable.

<!-- Ask learners to classify a Sunday exception omitted during ingestion versus an answer ignoring a retrieved exception. Both yield wrong answers but need different repairs. -->

---

# Scope determines eligibility before similarity

Terminal B may be semantically similar and still be outside the requested scope.

Trusted application context supplies the allowed terminal.

Filter before evidence reaches synthesis.

<!-- Connect to B4 caller scope. Terminal metadata is a teaching fixture, not a complete production authorization system. -->

---

# A metadata filter expresses an eligibility rule

```python
filters = MetadataFilters(filters=[
    MetadataFilter(key="terminal", value="A"),
])
retriever = index.as_retriever(
    filters=filters, similarity_top_k=2,
)
```

The application owns the filter value.

<!-- Run teaching snippet s05_metadata_scope.py before the guided lab. Check that the chosen vector store supports the filter; unsupported filtering must not silently become unscoped retrieval. -->

---

# Predict whether prompt instructions enforce scope

A retriever sends Terminal B text to the model.

The prompt says: “Use only Terminal A information.”

Has the application prevented Terminal B evidence from crossing the boundary?

<!-- Pause. Ask learners to distinguish prevention of disclosure from a request about answer behavior. -->

---

# A prompt cannot undo evidence already disclosed

The text has already reached the model.

Apply trusted scope in retrieval and preserve it through hybrid, reranking and tools.

Verify returned metadata before synthesis.

<!-- Reveal and connect to the metadata lab. Do not let a model-generated query supply unrestricted authorization filters. -->

---

# Lexical retrieval preserves exact-term signals

A rule identifier can matter even when its surrounding meaning resembles many other notes.

Lexical matching rewards matching terms; vector matching rewards learned similarity.

Their mistakes can differ.

<!-- Open teaching snippet s06_hybrid_fusion.py. Its tiny lexical ranker makes the mechanism visible; it is not a production BM25 implementation. -->

---

# Rank fusion combines ordering without equating scores

Reciprocal-rank contribution: `1 / (constant + rank)`

Add contributions for the same node across rankings.

A vector similarity and a lexical score need not share a scale.

<!-- Trace one candidate in teaching snippet s06. This snippet explicitly fuses ranks; do not describe it as a hidden framework hybrid service. Explain extra retrieval cost. -->

---

# Reranking spends more effort on a smaller pool

Retrieve a broader candidate set.

Compare each candidate more closely with the question.

Keep fewer passages for synthesis.

```python
from llama_index.core.postprocessor import LLMRerank
reranker = LLMRerank(llm=llm, top_n=1)
reranked = reranker.postprocess_nodes(hits, query_str=question)
```

`hits` comes from retrieval; `llm` uses the explicit chat adapter.

<!-- Run teaching snippet s07_rerank.py with its prepared candidate pools; LLMRerank performs real model work. Contrast candidates entering the reranker with survivors leaving it. -->

---

# Predict whether reranking can recover an absent rule

The candidate pool contains only `gate-b` and `reefer-a`.

The question asks when Terminal A opens.

Can a perfect reranker return `gate-a`?

<!-- Require a reason tied to the input set, not model intelligence. Keep the answer on the next slide. -->

---

# Reranking cannot select a candidate it never received

The missing rule must first enter the candidate pool.

Repair retrieval or ingestion before tuning the reranker.

When the right node is already present, reranking may improve its position.

<!-- Reveal the candidate-set limit. Measure retrieval coverage separately from ranking quality; an LLM guess is not recovered source evidence. -->

---

# Query rewriting can make conversational wording searchable

“For Terminal A, when can I get in through the gate?”

A rewrite can express the opening-time intent more directly.

Keep the original question and inspect the rewrite.

```python
rewrite = llm.complete(
    "Return only a search query; preserve terminal and intent: " + question
).text
print(question, rewrite)
hits = retriever.retrieve(rewrite)
```

This excerpt uses the configured `llm` and `retriever`.

<!-- Run teaching snippet s08_query_rewrite.py with a self-contained question. A rewrite is actual generation and may lose constraints or invent them. Conversational follow-up rewriting is an extension that requires explicitly supplied history; this excerpt does not supply history. -->

---

# A rewrite must preserve the intended question

Compare original intent and rewritten subject, task and constraints.

“Terminal A opening time” preserves the subject.
“Terminal B opening time” changes the task.

Evaluate retrieval on the rewritten query, not its fluency.

<!-- Use these as prepared comparison examples, not expected endpoint outputs. Ask for a new follow-up that should cause clarification rather than guessed context. -->

---

# Choose the repair that matches the observed failure

| Failure | Repair | Added cost |
| --- | --- | --- |
| Wrong terminal | Metadata scope | Metadata validation |
| Exact term missed | Hybrid retrieval | Extra ranking/fusion |
| Good candidate buried | Rerank | Extra inference |
| Missing subject | Rewrite | Call and intent-drift risk |

<!-- Ask learners to select one repair for a concrete trace. More components create more failure points; keep the baseline for comparison. -->

---

# Agentic RAG makes retrieval a model decision

Fixed: always run the configured retrieval stages.

Agentic: observe a result, then choose whether and what to retrieve next.

Multiple fixed stages alone do not establish agency.

<!-- Connect to B2/B3 tool-request and host-execution ownership. The distinction is adaptive control, not framework branding or the number of calls. -->

---

# A retrieval tool makes the decision observable

A FunctionAgent receives described retrieval capabilities.

The model proposes a tool call. The host executes its bounded query engine.

The resulting observation can influence the next action.

<!-- Open teaching snippet s09_agentic_rag.py. Inspect actual ToolCallResult events. A prompt asking for both terminal facts is not proof that both tool calls happened. -->

---

# A retrieval budget belongs to the host

Bound agent iterations and execution time.

Preserve tool scope independently of model arguments.

On exhaustion or missing evidence, report the gap instead of inventing a completed lookup.

<!-- Use the exact budget configuration in teaching snippet s09. Explain iteration caps are not identical to tool-call caps; inspect endpoint timeout and agent timeout separately. -->

---

# Predict which trace demonstrates adaptation

Trace A: rewrite → retrieve → rerank → answer, every time.

Trace B: retrieve gate rule → observe missing desk detail → choose desk lookup → answer.

Which trace provides evidence of an agentic retrieval decision?

<!-- These are prepared traces. Ask which intermediate observation changed the next action and how learners would verify that in the real event stream. -->

---

# The observation-to-action link establishes adaptation

Trace B changes its next lookup in response to missing evidence.

Review tool names, arguments, observations and stop reason.

A run with no tool calls has not demonstrated retrieval.

<!-- Reveal B, then inspect the actual s09 trace. Model variation or tool incompatibility is diagnostic evidence, not a reason to fabricate a successful transcript. -->

---

# Relevance labels make retrieval evaluation concrete

Relevant: `{gate-a, reefer-a}`
Retrieved: `[gate-b, gate-a]`

Predict precision@2, recall@2 and reciprocal rank.

What part of answer quality remains unmeasured?

<!-- Run teaching snippet s10_retrieval_evaluation.py only after predictions; its k=2 fixture matches this slide. Define relevant labels as human-supplied fixture judgments; they are not generated truth. -->

---

# Retrieval metrics cannot establish answer faithfulness

Precision@2 = 1/2. Recall@2 = 1/2.
Reciprocal rank = 1/2: the first relevant node is second.

An answer can still contradict the retrieved passage.
Evaluate claim support separately.

<!-- Reveal with numerator and denominator. Reciprocal rank only cares about the first relevant hit; recall reveals the missing second required fact. -->

---

# Practice fades support while preserving evidence

Worked: trace the lab’s worked ranking calculation and explain its labels.

Guided: enforce terminal scope and compute metrics in the standalone lab.

Independent: design a changed corpus failure, choose a repair and compare before/after evidence.

<!-- Open lab.md. Separate the offline contract exercise from live semantic retrieval; passing the first is not proof of the second. -->

---

# Transfer requires an explanation of the boundary

For your result, name:

1. The evidence needed and evidence actually retrieved.
2. The failure that justified the chosen pattern.
3. The added cost and remaining uncertainty.
4. The condition for answering, abstaining or stopping.

<!-- Close with an unsupplied scenario: a current rule and obsolete rule share terms. Ask how provenance and eligibility affect the design; do not introduce real policy. -->
