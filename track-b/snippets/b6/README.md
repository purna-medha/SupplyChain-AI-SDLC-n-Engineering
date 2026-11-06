# B6 · RAG and agentic RAG

Use the [later-module setup](../../SETUP.md#later-modules), including RAG requirements. With that environment active, run from `track-b`:

```bash
python snippets/b6/01_first_rag.py
```

| File | Concept | Try changing |
| --- | --- | --- |
| [01_first_rag.py](01_first_rag.py) | Retrieve evidence, answer and inspect sources | Ask about absent crane capacity |
| [02_chunks_and_metadata.py](02_chunks_and_metadata.py) | Chunk boundaries and source metadata | Change chunk size from 40 to 14 |
| [03_inspect_retrieval.py](03_inspect_retrieval.py) | Actual embeddings, ranking and trusted scope | Change top-k or terminal |
| [04_hybrid_retrieval.py](04_hybrid_retrieval.py) | Combine dense and keyword rankings | Compare gate and reefer queries |
| [05_rerank_candidates.py](05_rerank_candidates.py) | Rerank an existing candidate pool | Remove gate-a before reranking |
| [06_rewrite_query.py](06_rewrite_query.py) | Rewrite while preserving the information need | Change the question |
| [07_agentic_rag.py](07_agentic_rag.py) | Query engine as a bounded agent tool | Inspect observations and missing evidence |

Example 02 is local. The others need `OPENAI_API_KEY`; chat uses GPT-4.1-mini and embeddings use text-embedding-3-small. Classroom chunk budgets count words, not provider tokens.

The [slides](../../slides-md/b6-rag-and-agentic-rag.md) explain retrieval metrics and surrounding-context repairs conceptually. These are not extra runnable examples. Source links identify the seven files above.

See the [course map](../../README.md) for scope status. No B6 lab pack or formal assessment is currently available.
