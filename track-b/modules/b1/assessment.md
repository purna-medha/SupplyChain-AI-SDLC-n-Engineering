# B1 concept checks

1. The question stays fixed but the answer changes from a paragraph to three steps. Which request component probably changed? Does that component enforce a Python output contract?
2. Why can a model answer “What is dwell time?” but cannot reliably know the fee for a private container identifier without supplied facts? What changes when context is added?
3. A follow-up says “Which container does it apply to?” What must this stateless application's second request contain, and why does that affect token usage?
4. Explain the separate failures in broken JSON, `{"container_id":"C1"}`, an unsupported status value, and a well-formed note for another importer's container.
5. One model answers faster but changes the supplied fee. Another is slower and preserves it. What should you inspect before choosing, and what additional information is needed to turn token usage into currency cost?
