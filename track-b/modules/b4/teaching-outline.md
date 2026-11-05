# B4 teaching outline · LOD 2

Module question: How can we read the right facts for the right caller within a bounded amount of work?

- Read a result deliberately
  - Slide 1: B4 · A successful query is only one piece of evidence.
  - Slide 2: A table gives each row a meaning.
  - Slide 3: A query chooses shape and membership separately.
  - Slide 4: Predict the boundary before executing.
  - Slide 5: Equality changes membership, not output shape.
  - Slide 6: Parameters keep values out of query syntax.
  - Slide 7: Predict an identifier that looks like SQL.
  - Slide 8: A bound value remains a whole value.
- Preserve grain and caller scope
  - Slide 9: A join can change the unit of a row.
  - Slide 10: Predict the total after the join.
  - Slide 11: The repeated fee explains the wrong total.
  - Slide 12: EXISTS filters without multiplying containers.
  - Slide 13: Equal amounts expose a misleading repair.
  - Slide 14: Caller scope belongs to the host.
  - Slide 15: A narrow capability owns query and fields.
  - Slide 16: Predict access for owner A.
  - Slide 17: Both predicates must hold before a fee leaves.
- Inspect generated proposals and effects
  - Slide 18: Generated SQL is a proposal to inspect.
  - Slide 19: The live experiment exposes the actual proposal.
  - Slide 20: Unexpected SQL needs diagnosis before repair.
  - Slide 21: Read-only constrains effects while enabled.
  - Slide 22: Predict permission separately from correctness.
  - Slide 23: A permitted read can still be wrong.
- Bound work and transfer guarantees
  - Slide 24: One output row can require substantial work.
  - Slide 25: A result cap should disclose truncation.
  - Slide 26: A progress callback interrupts database work.
  - Slide 27: Diagnose a slow one-row result at the work boundary.
  - Slide 28: Practice fades from a working read to a new policy.
  - Slide 29: Transfer requires all four questions again.
  - Slide 30: Explain the guarantee and its limit.

## Existing executable checkpoint map

1. `01_read_parameters.py` — Read shape, predicates and bound values.
2. `02_join_grain.py` — Grain and aggregation.
3. `03_scoped_read_only.py` — Caller scope and restricted effects.
4. `04_model_sql.py` — Live SQL proposal.
5. `05_execution_bounds.py` — Output and work budgets.

The separate [seven teaching snippets](../../teaching-snippets/b4/README.md) expose the conceptual boundaries. The [three-activity plan](codealong-plan.md) maps them to these five snippets; an activity can use several snippets.
