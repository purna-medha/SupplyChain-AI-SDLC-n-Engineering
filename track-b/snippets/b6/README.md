# B6 · RAG, retrieval repairs and agentic RAG

Only the essential worked examples are in this folder. Run them in order; the same complete file is both the snippet and the instructor-led code-along. Each file adds a mechanism needed to understand this module.

| File | Why it is essential | One learner change |
| --- | --- | --- |
| [01_first_rag.py](01_first_rag.py) | Show the complete retrieval-to-answer behaviour first. | ask about crane capacity, which is absent from the synthetic notes. |
| [02_chunks_and_metadata.py](02_chunks_and_metadata.py) | Open the chunking and provenance stage of that pipeline. | change chunk_size from 40 to 14 and inspect the Sunday exception. |
| [03_inspect_retrieval.py](03_inspect_retrieval.py) | Inspect actual embeddings and scoped candidates before generation. | change top-k or trusted_terminal and inspect the actual returned evidence. |
| [04_hybrid_retrieval.py](04_hybrid_retrieval.py) | Use complementary retrieval signals through the library. | compare the three rankings for a gate question and a reefer question. |
| [05_rerank_candidates.py](05_rerank_candidates.py) | Improve ranking within an existing candidate pool. | remove gate-a from the pool and explain the limit of reranking. |
| [06_rewrite_query.py](06_rewrite_query.py) | Change search wording while inspecting preserved intent. | change the question and check that subject and intent survive rewriting. |
| [07_agentic_rag.py](07_agentic_rag.py) | Reuse the query engine as an agent-selected capability. | ask about crane capacity and inspect actual tool observations and sources. |

From `track-b`: `python codealongs/b6/01_first_rag.py`. Read [setup](../../SETUP.md) once. Each example is independent, with tiny synthetic data and direct calls to the library or Python operation being taught. Repeated setup keeps the full operation visible. There are no learner gaps or project imports.

Chat and embeddings use separate LlamaIndex adapters. Chunk/source inspection is local; the other examples need real endpoint access. Retrieval-metric arithmetic and sentence-window/parent-context variants remain slide explanations rather than extra required scripts. The hybrid example uses SimpleKeywordTableIndex and QueryFusionRetriever directly, not custom ranking machinery.

The default model examples call OpenAI through the documented libraries. They load `OPENAI_API_KEY` with dotenv. No canned output or fake successful model run replaces missing access. Labs are deferred. Earlier versions are preserved under `authoring/previous-codealongs-before-essential-selection`, outside the teaching path.
