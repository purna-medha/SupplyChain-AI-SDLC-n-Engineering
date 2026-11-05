# B6 assessment

Answer before consulting the instructor guide. Five questions, 4 points each: 2 for predicted behavior and 2 for mechanism and limits. A bare result earns at most 2/4.

1. A document says “Gate opens at 06:00. On Sunday it opens at 09:00.” Only the first sentence is retrieved for a Sunday question. The answer says 06:00 and includes that source. Locate the failure, propose a chunking repair, and explain why the citation does not establish faithfulness to the complete rule.
2. A query for Terminal A retrieves gate-b above gate-a. What does increasing top-k change? Where should trusted terminal scope be enforced, and why is a scope instruction in the answer prompt insufficient?
3. An exact rule code is absent from the vector candidate pool. Choose between hybrid retrieval and reranking, explain your choice, and identify one cost. Would your choice change if the correct candidate were already present at rank 10?
4. Compare (a) always rewrite → retrieve → rerank → answer with (b) a model that sees one tool result and chooses whether and what to retrieve next. Which is agentic, what evidence would establish that behavior, and how should it stop if evidence remains missing?
5. Relevant IDs are {gate-a, reefer-a}; retrieved IDs are [gate-b, gate-a]. Calculate precision@2, recall@2 and reciprocal rank. If the answer cites gate-a but claims that Terminal A opens at 08:00, what additional evaluation fails?
