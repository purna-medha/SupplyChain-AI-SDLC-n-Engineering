# B4 · Querying enterprise data with AI agents

Revised direction approved in conversation, 6 November 2026. Working budget: one teaching hour, with a separate [B4 learner lab draft](labs/container_help_desk/B4.md). Formal assessments and new notebooks remain deferred. Course order remains B1 → B2 → B3 → B4 → B6 → B5.

The refined [34-slide deck](slides-md/b4-enterprise-data.md) explains the intended SQL and SQLAlchemy engine/connection/result roles before the bound-query illustration. It distinguishes the source and approved analytics fixtures, then develops question-to-SQL, semantic correctness and agent use. Larger-schema/metric and write/retry topics are brief extensions. A matching [Gamma text copy](slides-gamma/b4-enterprise-data.txt) is available.

**Objective:** answer a permitted business question using structured enterprise-style data, inspect actual SQL/results, verify the business meaning, and expose the governed query capability to an existing agent.

## Progression from B1–B3

B1 puts a model in an application. B2 gives it tools and shared capabilities. B3 coordinates a larger task using workflows, specialists, state and review. B4 adds schema-grounded database querying. Concepts come before compact, complete examples; libraries implement the illustrated capability rather than becoming the curriculum.

The prior B4 revision overemphasised HTTP plumbing and write controls. Those examples remain optional [integration references](snippets/b4/reference/integrations/README.md). The core now centres on SQLAlchemy Core and LlamaIndex structured-data querying, with business meaning and access restrictions visible. B3's approval lifecycle is reused briefly rather than retaught.

## 1 · Understand the business question and approved schema

Use a narrow operational request, such as C1's recorded fee, and a new analytical request, such as the total recorded USD fee for delayed containers. Distinguish a fixed parameterized tool from flexible natural-language querying. Prefer an existing approved API/semantic interface where that is the enterprise's access path.

Inspect actual tables, columns, keys and foreign keys with SQLAlchemy. Explain what one row represents, which relationships are valid, and what metadata cannot tell us: definitions of delayed/outstanding, currencies, time windows and source freshness. An ambiguous question needs clarification before execution. Do not silently rename a recorded fee an outstanding balance.

## 2 · Obtain a correct, scoped database result

Start with a hand-understood parameterized read. Host-owned caller context supplies owner scope, selected fields omit private notes, and a Pydantic result declares amount/unit/time fields. Explain shape validation separately from facts and permissions. Unknown and inaccessible IDs return controlled absence.

Then supply an approved, small schema and business definitions to LlamaIndex `SQLDatabase`/`NLSQLTableQueryEngine`. Observe the generated SQL and actual rows before answering. The classroom analytics connection has a separate approved caller-A snapshot and a SQLite authorizer that permits only selected reads/functions/transactions. Writes, attachments, private tables and policy-changing statements are not authorised. A progress handler supplies a limited instruction-based budget. No embedding service is needed for this fixed-schema path.

Framework `include_tables` config supplies schema context, not database permissions. In production, the approved snapshot must come from a trusted policy/data pipeline, or equivalent visibility must be enforced by grants, views, row policies and service controls. A SQLite callback is a classroom policy mechanism, not a substitute for that production design.

## 3 · Check business meaning and use the capability in an agent

Use one prepared join failure: a fee belongs to a container while events can have multiple rows. Execute the valid-but-wrong join, inspect its inflated total, and compare an EXISTS-based repair against an independent expected result. Equal-fee variation exposes why deduplicating amounts is not a general repair.

Demonstrate actual rejection of a private-table read and a write. Distinguish returned-row limits, detected truncation and query-work limits. Empty rows, NULL aggregate results and zero amounts need explicit interpretation. Keep failed queries visibly failed.

Give the existing SDK agent the LlamaIndex query capability. Inspect the model-selected question, generated SQL, returned rows, final answer and source/snapshot. Handle missing, failed and truncated observations honestly. This composes familiar tools/runtimes; it does not introduce a new agent architecture.

Discuss relevant-schema retrieval for larger approved schemas and business-owned metric definitions/semantic layers as enterprise extensions. Reuse B3's exact-payload review for separately controlled writes; transactions, uncertain outcomes and stable operation identities remain important but the larger demonstrations live in references.

## Core teaching files

1. `01_inspect_schema.py`: SQLAlchemy inspection and declared relationships.
2. `02_scoped_read.py`: bound values, trusted owner and typed result.
3. `03_question_to_sql.py`: actual schema-grounded SQL generation/execution.
4. `04_check_business_meaning.py`: incorrect join, correct grain and DISTINCT variation.
5. `05_enforce_query_boundaries.py`: database policy, forbidden operations and output truncation.
6. `06_agent_queries_database.py`: the query capability used by a familiar SDK agent.

Every file builds its own disposable in-memory fixture and imports no teaching helper. SQLAlchemy is declared directly at its already locked version; no server or production credentials are required. Model examples use `load_dotenv()` and `OPEN_AI_KEY`.

## Synthetic data and expectations

- Basic source inspection/lookup: C1 belongs to A with USD 100; C2 belongs to B with USD 200.
- Approved A analytics snapshot: C1 delayed/USD 100, C4 delayed/USD 50, C5 on_time/USD 75. C2 is not in this snapshot.
- Snapshot time: `2026-11-06T00:00:00Z`. It is recorded context, not the current request time.
- Delayed total: USD 150. All-row total would be USD 225, so omitting the status filter changes the result.
- Highest delayed fee: C1/USD 100.
- Event example: C1 has two events, C4 one. The incorrect joined total is 250; the intended total is 150.

The approved snapshot is supplied as a trusted classroom input; these files do not implement its upstream authentication/tenant-projection pipeline. Do not imply that every source table was loaded and filtered by the model.

## Verification and sources

Separate offline checks, actual model calls, changed questions and scripted failure probes. Verify actual SQL/rows, owner denial/absence, injection-shaped values, type checking, equal-fee semantics, table/write/ATTACH/PRAGMA restrictions, query interruption and agent stopping. Preserve uncertainty and don't promise fixed stochastic outputs.

Primary references: [SQLAlchemy engine](https://docs.sqlalchemy.org/en/21/tutorial/engine.html), [schema reflection](https://docs.sqlalchemy.org/en/21/core/reflection.html), [LlamaIndex text-to-SQL](https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/), [SQLite authorizer](https://www.sqlite.org/c3ref/set_authorizer.html), [PostgreSQL row policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html). These inform implementation choices; they do not establish one universal enterprise stack.
