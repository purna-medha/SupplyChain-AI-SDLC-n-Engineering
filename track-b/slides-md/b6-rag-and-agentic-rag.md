---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 27px; padding: 44px 55px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 20px; }
  table { font-size: 23px; }
---
<!-- _class: lead -->

# B6 · From supplied context to retrieved evidence

B1 placed facts in a request by hand.

Now a document collection supplies the evidence. We will build a small RAG answer, open its parts, then improve it when a named failure appears.

<!--
Teach after B4 and before B5. Follow the BFSI M4 whole-parts-whole sequence, then M5 failure-to-repair pairs. The final section reuses B3's agent loop for retrieval. All terminal notes and hours are synthetic.
-->

---

# The answer lives in a document

> When does Terminal A open?

The supplied note says:

```text
Terminal A gate opens at 06:00.
```

The application needs that passage before generating an answer.

<!--
Connect to B1's missing factual context. General model knowledge cannot establish the contents of this private classroom corpus. We need to find the relevant passage and place it in the request, rather than train new weights for this one fact.
-->

---

# First understand the useful behaviour

```text
question → find relevant text → supply context → answer
```

Retrieval-augmented generation connects search to generation.

The retrieved text supplies evidence for the answer.

<!--
Name RAG after its job is understandable. Ask learners what the model would lose if the passage were missing. This is the minimal mental model; the next small example lets them see a complete result before learning every component.
-->

---

# A small working RAG pipeline

```python
index = VectorStoreIndex(nodes, embed_model=embed)
engine = index.as_query_engine(llm=llm, similarity_top_k=2)
```

Source: [04_basic_rag.py](../authoring/previous-codealongs-before-essential-selection/b6/04_basic_rag.py#L34)

`nodes` contains the supplied notes. `embed` and `llm` are the configured embedding and chat adapters.

<!--
Open the complete file and run its question loop. Model setup is already supplied; keep attention on index and query engine. This is a first working shape, just as M4 uses a tiny framework example before unpacking the objects.
-->

---

# Inspect the answer and its sources

```python
response = engine.query(
    question + " Use only supplied notes; report missing evidence."
)
print("question:", question, "answer:", response)
for hit in response.source_nodes:
    print("source:", hit.node.node_id, hit.score, hit.node.text)
```

Source: [04_basic_rag.py](../authoring/previous-codealongs-before-essential-selection/b6/04_basic_rag.py#L40)

Compare the opening-time answer with the actual source text.

<!--
Read actual returned nodes rather than assume a citation is sufficient. The file also asks about crane capacity, which is absent from the corpus. Keep that result for a later failure discussion; first explain the pieces that produced the supported answer.
-->

---

# What the short example packaged

```text
document text → chunks → embeddings → index
question → retrieval → supplied context → generated answer
```

We will inspect these objects one at a time.

<!--
Return from the successful whole to its parts. Ask learners to locate the text and the index in the source before advancing. The two lines were convenient because a framework performed several stages, not because those stages disappeared.
-->

---

# Documents need retrieval units

A document can contain several topics.

A chunk is a smaller piece the search system can return.

For our notes, opening hours and the reefer desk are separate information needs.

<!--
Introduce chunking as the unit of search. Learners already understand that context is supplied; now they choose how much text travels together. Avoid starting with a catalogue of splitter libraries.
-->

---

# Split a supplied document

```python
splitter = SentenceSplitter(
    chunk_size=size,
    chunk_overlap=0,
    tokenizer=str.split,
    chunking_tokenizer_fn=lambda text: text.split(". "),
)
```

Source: [01_documents_chunks.py](../authoring/previous-codealongs-before-essential-selection/b6/01_documents_chunks.py#L20)

The full example compares small and larger chunk budgets.

<!--
Explain size, overlap and sentence-aware splitting using the supplied document. The source deliberately counts words to avoid tokenizer downloads; its budget is not the chat model's token count. Run it and inspect each actual node's text.
-->

---

# Keep source identity with each chunk

The document carries `terminal: A` metadata and a stable source ID.

Each node should retain the connection to its source.

That connection lets us inspect an answer and later enforce eligible evidence scope.

<!--
Show the printed source and metadata from s01. Explain the source-to-chunk relationship before treating metadata as a filter configuration. A text fragment without its provenance is much harder to cite or diagnose.
-->

---

# Meaning needs a searchable representation

A user asks “When can I enter?” while a document says “gate opens.”

An embedding maps each text to a numeric vector.

Compatible query and document vectors let us compare meaning-related passages.

<!--
This creates the need for embeddings through a wording mismatch. Keep exact-term search for a later failure. Similarity is a relevance signal; it does not establish truth or permission, which learners will see in the ranking and scope examples.
-->

---

# Compare actual embeddings

```python
query = embed.get_query_embedding("When can I enter Terminal A?")
for text, vector in zip(texts, embed.get_text_embedding_batch(texts)):
    dot = sum(a * b for a, b in zip(query, vector))
    norm = sqrt(sum(a * a for a in query) * sum(b * b for b in vector))
    print(text, "dimensions:", len(vector), "cosine:", round(dot / norm, 3))
```

Source: [02_embeddings.py](../authoring/previous-codealongs-before-essential-selection/b6/02_embeddings.py#L21)

<!--
The complete file supplies the embedding adapter and two source texts. Run it and inspect vector dimensions and actual cosine scores. The same configured embedding model represents query and documents. A text-generation-only endpoint cannot perform this operation.
-->

---

# Store searchable nodes in an index

```text
stable ID + chunk text + metadata + embedding
                    ↓
               searchable index
```

An index makes the prepared collection reusable for queries.

<!--
Tie the representation back to the objects already printed. A persistent vector store is useful when the collection is reused at scale; the tiny examples can remain in memory. Changing documents, chunk boundaries or embedding models requires an index-maintenance decision.
-->

---

# Retrieve before generating an answer

```python
index = VectorStoreIndex(nodes, embed_model=embed)
retriever = index.as_retriever(similarity_top_k=2)
for hit in retriever.retrieve("When does Terminal A gate open?"):
    print(hit.node.node_id, hit.score, hit.node.text)
```

Source: [03_vector_retrieval.py](../authoring/previous-codealongs-before-essential-selection/b6/03_vector_retrieval.py#L27)

Inspect IDs, scores and text. No answer has been generated by this retrieval call.

<!--
The code now exposes the stage the query engine hid. Ask whether the required opening-time passage appears. top_k controls how many candidates are selected; score values rank those candidates and are not universal confidence probabilities.
-->

---

# Top-k changes what reaches the model

A small k can miss a needed passage.

A larger k can recover it, while adding competing text and context cost.

Change k and inspect the evidence before judging the answer.

<!--
Use the same question and corpus to isolate this one choice. Do not promise that increasing k improves quality. The next step reconnects the candidate passages to the model request learners understood in B1.
-->

---

# Retrieval supplies the context for generation

The selected passages become context for a chat model.

The question and an instruction to use that evidence accompany them.

The query engine packages this retrieval-and-synthesis path.

<!--
Return to s04 after showing the retriever directly. Ask learners to explain what engine.query adds beyond retriever.retrieve. A source node identifies evidence on the response path, while claim support still needs inspection.
-->

---

# The baseline, understood end to end

```text
source → chunk → vector → index
question → ranked passages → context → answer + sources
```

We can now inspect what the first short example did.

<!--
This closes the whole-parts-whole baseline section. Have learners point to each object in the linked snippets. Only after they own the baseline should we add more techniques. Next use its unresolved crane-capacity result to introduce diagnosis.
-->

---

# An answer can be missing for different reasons

For “What is Terminal A crane capacity?”:

- The corpus may contain no such fact.
- Retrieval may miss a fact that exists.
- Generation may ignore the supplied evidence.

These need different responses.

<!--
Revisit the actual second question from s04. Do not attribute its failure to retrieval until checking the source collection. If the answer is absent everywhere, report missing evidence instead of inventing a more elaborate pipeline.
-->

---

# Establish an evaluation case first

Prepared two-part question:

> When does Terminal A open, and where is its reefer desk?

Required evidence: `gate-a` and `reefer-a`.

Now inspect which of those IDs were actually retrieved.

<!--
Adapt M5's golden-set start. Relevance labels come from the question and corpus, not from the ranker being evaluated. A tiny diagnostic set helps decide what to repair; it is not a production benchmark.
-->

---

# A ranking gives measurable evidence

Prepared top two: `gate-b`, `gate-a`.

```text
precision@2 = 1 relevant result / 2 returned = 1/2
recall@2    = 1 recovered / 2 required      = 1/2
```

The generated answer still needs its own support check.

<!--
Use ../authoring/previous-codealongs-before-essential-selection/b6/10_retrieval_evaluation.py for the complete metric arithmetic, including reciprocal rank. This ranking is a fixture, not a live retrieval result. Keep those evidence types separate when comparing an actual pipeline change.
-->

---

# Failure · The chunk lost the exception

Source:

> Gate opens at 06:00. On Sunday it opens at 09:00.

A Sunday query retrieves only the first sentence.

The precise match contains incomplete evidence.

<!--
Start the advanced section with the same chunking limitation seen in s01. Ask why a correct-looking citation would still fail the Sunday question. The next slide adds exactly the surrounding information missing from the search unit.
-->

---

# Repair · Expand the answer context

Search a focused unit, then include its surrounding evidence.

```text
matched sentence → neighbouring window or parent section
```

A structured chunk can also keep a rule and its exception together.

<!--
Explain sentence windows and parent-context expansion conceptually; they are extensions beyond the core path. The idea is separate search granularity from answer context. Re-run the same Sunday case and inspect the exception before claiming improvement.
-->

---

# Failure · An exact identifier is missed

A query contains an exact time, rule code or reference.

Dense search may find a similar passage while missing the exact term.

A lexical signal can recover evidence that similarity alone ranked poorly.

<!--
Use the supplied hybrid card's '08:00' query. Establish the search failure before introducing fusion. Dense retrieval may already do well on this tiny case; inspect actual rankings rather than force a failure. The additional signal is still understandable.
-->

---

# Repair · Combine rankings

```python
hybrid = QueryFusionRetriever(
    retrievers=[dense, keyword],
    llm=llm,
    mode="reciprocal_rerank",
    num_queries=1,
    similarity_top_k=2,
    use_async=False,
)
```

Source: [06_hybrid_fusion.py](../authoring/previous-codealongs-before-essential-selection/b6/06_hybrid_fusion.py#L36)

Rank fusion combines positions without treating raw lexical and vector scores as the same unit.

<!--
The file directly creates a dense retriever and a SimpleKeywordTableIndex retriever, then combines them with QueryFusionRetriever. num_queries=1 keeps the original query without adding generated rewrites. Inspect all three actual rankings; this core keyword example does not claim BM25 scoring.
-->

---

# Failure · The right passage is buried

Retrieval returns the needed passage along with several plausible distractors.

Keeping every candidate increases noise.

A second scoring stage can examine the question and candidates more closely.

<!--
This is a ranking problem only if the needed passage is already in the candidate pool. Ask learners to distinguish it from the earlier recall failure. That distinction explains both the value and the limit of the next technique.
-->

---

# Repair · Rerank the candidate pool

```python
reranker = LLMRerank(llm=llm, top_n=1)
for pool in (candidates, [hit for hit in candidates if hit.node.node_id != "gate-a"]):
    print("pool:", [hit.node.node_id for hit in pool])
    reranked = reranker.postprocess_nodes(
        pool, query_str="When does Terminal A gate open?"
    )
    for hit in reranked:
        print("after:", hit.node.node_id, hit.score, hit.node.text)
```

Source: [07_rerank.py](../authoring/previous-codealongs-before-essential-selection/b6/07_rerank.py#L33)

<!--
The card uses prepared candidate order and actual model reranking. Run both pools: one includes gate-a and one omits it. A reranker can reorder supplied candidates but cannot return a missing source. Explain the added model-call cost after showing its role.
-->

---

# Failure · The wording is a poor search query

“For Terminal A, when can I get in through the gate?”

A more direct query can make the subject and information need explicit.

The rewrite must preserve Terminal A and the opening-time task.

<!--
Use the same corpus to avoid changing the evidence problem. Rewriting can help colloquial wording, but it can also drift. Query decomposition and hypothetical-answer expansion are additional options when a measured query-shape problem justifies them.
-->

---

# Repair · Rewrite and compare

```python
question = "For Terminal A, when can I get in through the gate?"
rewrite = llm.complete(
    "Return only a search query. Preserve subject, task and constraints: " + question
).text
print("original:", question, "rewrite to review:", rewrite)
for query in (question, rewrite):
    print(query, [(hit.node.node_id, hit.score) for hit in retriever.retrieve(query)])
```

Source: [08_query_rewrite.py](../authoring/previous-codealongs-before-essential-selection/b6/08_query_rewrite.py#L35)

<!--
Run the actual rewrite, inspect its meaning and compare both retrieved rankings. A fluent rewrite does not guarantee better retrieval. Preserve independently enforced scope; a rewrite must not choose which private terminal records the caller is permitted to see.
-->

---

# Failure · Similar evidence is outside scope

A request scoped to Terminal A retrieves Terminal B's note.

An instruction to ignore B does not undo disclosure if B's text already entered the model request.

Eligibility must be decided before synthesis.

<!--
Connect directly to B4's trusted-owner predicate. The new application is document eligibility rather than row eligibility. This example earns a metadata filter without introducing another authentication system.
-->

---

# Repair · Apply trusted metadata scope

```python
trusted_terminal = "A"  # Application context, not a model-generated argument.
filters = MetadataFilters(
    filters=[MetadataFilter(key="terminal", value=trusted_terminal)]
)
retriever = index.as_retriever(similarity_top_k=2, filters=filters)
for hit in retriever.retrieve("When does the gate open?"):
    print(hit.node.node_id, hit.node.metadata, hit.node.text)
```

Source: [05_metadata_scope.py](../authoring/previous-codealongs-before-essential-selection/b6/05_metadata_scope.py#L32)

<!--
The trusted terminal value is application context in the card. Run it and inspect returned metadata. Carry this scope through hybrid search, reranking and retrieval tools. The filter demonstrates eligibility mechanics, not complete production identity.
-->

---

# A fixed RAG pipeline may be sufficient

Our configured pipeline retrieves and synthesises for each question.

It can include filtering, rewriting or reranking without a model choosing the next operation.

Use this simpler shape when the information path is known.

<!--
Summarise the understood repairs before introducing agency. Multiple stages do not themselves make retrieval agentic. B3's defining mechanism was observations influencing a new model-selected action; now apply that mechanism to evidence gathering.
-->

---

# An agent can request retrieval

A model may choose a search tool, observe its result and decide whether another lookup is needed.

The search pipeline becomes one capability within a bounded workflow.

The host retains evidence scope and execution limits.

<!--
Reuse B2's tool contract and B3's observation loop. Do not re-explain basic function calling. The new idea is exposing a query engine as the capability. A fixed retrieval chain remains a valid choice when adaptation adds no value.
-->

---

# Wrap the query engine as a tool

```python
tool = QueryEngineTool.from_defaults(
    query_engine=engine,
    name="terminal_notes",
    description="Search synthetic Terminal A notes.",
)
```

Source: [09_agentic_rag.py](../authoring/previous-codealongs-before-essential-selection/b6/09_agentic_rag.py#L37)

The description tells the model what evidence this capability can search.

<!--
The full source builds the scoped classroom corpus and engine first. QueryEngineTool makes the familiar query engine available to an agent. Ask what additional tool would be needed for a genuinely different evidence collection.
-->

---

# Place the tool inside a bounded agent

```python
agent = FunctionAgent(
    tools=[tool],
    llm=llm,
    timeout=90,
    streaming=False,
    system_prompt="Use notes for facts. Report missing evidence.",
)
```

Source: [09_agentic_rag.py](../authoring/previous-codealongs-before-essential-selection/b6/09_agentic_rag.py#L42)

```python
handler = agent.run(user_msg="When does Terminal A open?", max_iterations=4)
```

Source: [09_agentic_rag.py](../authoring/previous-codealongs-before-essential-selection/b6/09_agentic_rag.py#L52)

<!--
Show handler=agent.run in the full source. Iterations and timeout bound different resources, and neither is a separate exact tool-call count budget. The model must support native tool proposals. No tool events means the run has not demonstrated retrieval.
-->

---

# Inspect the actual retrieval observation

```python
if isinstance(event, ToolCallResult):
    print("request:", event.tool_name, event.tool_kwargs)
    print("observation:", event.tool_output.content)
    for hit in getattr(event.tool_output.raw_output, "source_nodes", []):
        print("source:", hit.node.node_id, hit.node.text)
```

Source: [09_agentic_rag.py](../authoring/previous-codealongs-before-essential-selection/b6/09_agentic_rag.py#L54)

<!--
Run the complete card and inspect tool arguments, returned evidence and sources. Compare them with the final answer. The card may use one tool call; do not claim it demonstrated an additional adaptive lookup unless the observed trace actually shows one.
-->

---

# Reassemble the evidence path

```text
question
  → fixed retrieval or a model-selected search
  → eligible candidates
  → inspected evidence
  → generated answer
  → claim-support and task checks
```

Every added stage should address an observed need.

<!--
Ask learners to justify the chosen path for the opening-time question versus a two-part investigation. Use the earlier failure-to-repair pairs to explain each optional stage. This is the closing synthesis, not a requirement to add every technique.
-->

---

# Practice · Baseline, repair, then adaptation

Use the [B6 worked examples](../codealongs/b6/README.md).

Build baseline RAG, diagnose scope and inspect bounded agent retrieval.

Introduce a new corpus failure and justify one measured repair. Labs will follow separately.

<!--
Separate real chat/embedding/tool runs from prepared metric and structural checks. A missing endpoint remains an unvalidated live boundary. Learners should preserve the same question and expected evidence when comparing before and after.
-->

---

# B6 · An answer with an evidence path

We can explain what was searched, what was retrieved and which claims it supports.

We can also choose a repair from the observed failure.

Next: B5 turns these observations into repeatable evaluation and improvement.

<!--
Ask for one actual retrieval result and its remaining limitation. A correct source ID does not automatically establish answer faithfulness. B5 now brings together known contracts, traces and appropriate judgments across the complete workflow.
-->
