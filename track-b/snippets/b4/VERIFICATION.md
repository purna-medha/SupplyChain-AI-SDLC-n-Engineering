# B4 query examples · verification, 6 November 2026

This record covers the [six current examples](README.md), [34-slide deck](../../slides-md/b4-enterprise-data.md) and [approved outline](../../B4-OUTLINE.md). [Captured results](verification-results.json) preserve source hashes, commands and transcripts. The API/write examples have a separate [historical record](reference/integrations/VERIFICATION.md).

## Environment and execution

`uv sync --locked` passed: 114 packages resolved, 108 installed packages audited. SQLAlchemy 2.1.8 was already installed/locked transitively; it is now also a direct dependency. No package versions were changed for this refocus.

Verified environment: Python 3.12.2, SQLite 3.51.1, SQLAlchemy 2.1.8, Pydantic 2.14.2, openai-agents 0.20.0, llama-index-core 0.14.25, llama-index-llms-openai 0.8.3 and openai 2.54.0.

All six final core files ran successfully from `track-b` using their documented `uv run python snippets/b4/...` commands. Each creates a real disposable in-memory database and imports no teaching helper. They contain 22–81 lines, including setup, comments and whitespace. 01/02/04/05 are offline. 03/06 used actual `gpt-4.1-mini` model access with `load_dotenv()` and `OPEN_AI_KEY`; no key was printed or captured. 06 made both the outer agent call and the inner SQL-generation call.

Fixed-table SQL needs no embedding operation. `Settings.embed_model=None` produces LlamaIndex's embedding-disabled/MockEmbedding setup message. That unused internal placeholder does not replace SQL generation or provide prepared successful model responses.

## Default observations

| File | Actual observation |
| --- | --- |
| 01 · Inspect schema | Tables/columns, primary keys and the declared fees-to-containers foreign key were printed from SQLAlchemy metadata |
| 02 · Scoped read | C1, fee 100, USD, snapshot time and source; no owner/private-note field in the result |
| 03 · Question to SQL | Generated SUM with delayed/USD predicates; actual rows `[(150,)]`, independent expectation `[(150,)]` |
| 04 · Business meaning | Wrong join: 250/FAIL; EXISTS repair: 150/PASS; DISTINCT amounts: 150/PASS by coincidence |
| 05 · Execution boundaries | First two approved rows visible, truncation detected; private-table read and DELETE rejected |
| 06 · Agent query | Model selected the query tool; actual SQL returned C1/100 for the highest delayed fee; final answer retained USD, exact source and timestamp |

03's observed SQL was:

```sql
SELECT SUM(container_fees.fee) FROM container_fees
WHERE container_fees.status = 'delayed' AND container_fees.currency = 'USD';
```

06's final observed answer cited `approved-fee-snapshot/A` and `2026-11-06T00:00:00Z`. A current fetch does not make that snapshot current. These are selected observations, not a reliability estimate or guaranteed future outputs.

## Changed inputs and business checks

Eight temporary source variations passed during this revision; distributed files retain the defaults. The captured results include the exact replacement values and transcripts.

| Variation | Observed result |
| --- | --- |
| 02 requests C2 | Unavailable, without a fee |
| 02 requests missing C9 | Same public unavailable result |
| 02 binds `C1' OR 1=1 --` as the ID | Unavailable; bound value did not rewrite SQL |
| 04 gives C4 fee 100 and updates independent expectation to 200 | Wrong join 300/FAIL; EXISTS 200/PASS; DISTINCT amounts 100/FAIL |
| 03 asks maximum delayed fee, independent expectation 100 | Actual SQL result `[(100,)]` |
| 03 asks C2's recorded USD fee, independent expectation empty | Actual rows `[]` |
| 06 asks C2's recorded USD fee | Actual rows `[]`; agent reported absence without inventing a fee |
| 06 uses max_turns=1 | Explicit INCOMPLETE message and actual MaxTurnsExceeded error; no final answer |

The agent limit can stop after an inner query has already executed; it does not mean no work occurred. The variation runs preceded display-only SQL-fixture formatting and added tool-question/failure print statements. The execution policy and query/agent behavior were unchanged; all six default files were rerun afterward.

04's wrong join is a prepared semantic failure, not a claimed model mistake. Its PASS/FAIL comparison uses an independently supplied classroom expectation. DISTINCT passing the first fixture is not proof of correctness.

## Controlled failure and policy probes

Temporary verification code reused the actual 05 connection policy. It rejected a private-table SELECT, DELETE, ATTACH DATABASE and `PRAGMA query_only=OFF`. The three original public rows remained. A costly read using only allowed-table cross joins was interrupted by the installed instruction callback. The actual 02 FeeRecord rejected both a text amount and a boolean amount.

A separate **supplied SQL candidate** test patched LlamaIndex's SQL-generation method to return `DELETE FROM container_fees`. It made no model call. Actual LlamaIndex parsing/execution reached the restricted database; execution failed, and 03 raised `Query rejected or failed; no database result to answer from`. This checks failure handling, not how often a model proposes an unsafe query.

The query engine can represent an SQL error in its response instead of raising it directly. 03 therefore checks for successful result metadata; 06 returns `query_failed` when it is absent. Successful empty rows are a separate outcome. The live agent's failed-query explanation branch was not separately exercised; its normal, empty and turn-limit paths were observed.

## Boundaries of this evidence

The caller-A analytics snapshot is already approved classroom input, containing C1/C4/C5 and no C2. The examples do not implement upstream authentication or tenant projection. `include_tables` selects schema context; it does not authorise access. The SQLite authorizer independently controls operations/tables, with a small function allowlist in 03/06. This mechanism must not be inferred to transfer when changing database engines.

05 detects output truncation by fetching one extra row. 06 limits rows supplied to the outer model after LlamaIndex has fetched the raw query result. These caps do not by themselves bound earlier database work or host memory. The progress callback interrupts at its first call after roughly 10,000 SQLite VM instructions; it is neither a wall-clock deadline nor a cumulative workflow budget.

No production identity provider, warehouse role/row-policy deployment, concurrency, durability or broad adversarial isolation was tested. No HTTP server is needed for the current core. Historical API/write verification does not establish current core behavior.

## Teaching and visual checks

All 34 slides rendered successfully with Marp and were visually inspected through three contact sheets. The deck explains concepts before source excerpts, links all six complete examples, and labels prepared failures and abbreviated excerpts. Local links and Python syntax were checked. Libraries have separate responsibilities; business definitions, source/time, scope and calculation remain visible independently of them.

A fresh read-only review found no critical or important issue and independently reran the four offline examples. Its minor note is that 05 labels DatabaseError as policy rejection for its three supplied statements; if that demonstration loop is extended, execution/interruption errors should be distinguished.

## Teaching refinement and Gamma copy · 6 November 2026

The Markdown deck was refined after teaching review, retaining 34 slides and the existing Marp style. Plain SQL and engine/connection/result explanations now precede bound-query code; source/analytics fixtures and the join example's event requirement are visible. Enterprise extensions are consolidated. The matching [Gamma text](../../slides-gamma/b4-enterprise-data.txt) retains the slide bodies, tables and fenced blocks, with presenter notes/configuration and local illustration navigation removed.

The refined B4/B5 decks rendered to 34/36 PNGs and were inspected through six contact sheets, with selected slides inspected at full size. A fresh read-only review checked teaching progression, source/evidence agreement and conversion parity. Its requested visible event-eligibility clarification was applied. These are teaching-material changes; executable source and recorded model runs are unchanged.

Labs, assessments, new notebooks, staging and commits remain deferred.
