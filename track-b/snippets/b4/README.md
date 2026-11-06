# B4 · Querying enterprise data with AI agents

**Start with [01 · Inspect the schema](#01-inspect-the-schema).** Work through one example at a time.

By the end, you can turn a permitted business question into an inspectable database result, check its meaning, and give that capability to an agent.

Run commands from **track-b** after completing [shared setup](../../SETUP.md). Each file is complete and creates its own disposable database. No server is needed. Allow about **60 minutes** for the lessons, excluding setup; model response times vary.

## Part 1 · Understand the data

### 01 Inspect the schema

1. **Understand.** A schema describes tables, columns, keys and relationships. SQLAlchemy's Inspector reads this metadata from the actual database. Before querying, identify what one row represents: here, one container or one fee for that container. Column names alone cannot define an “outstanding balance”.
2. **Predict.** Which column connects a fee to its container?
3. **Run** [01_inspect_schema.py](01_inspect_schema.py). This lesson is offline.

   ```bash
   uv run python snippets/b4/01_inspect_schema.py
   ```

4. **Observe.** The output lists `containers` and `fees`. The declared foreign key connects `fees.container_id` to `containers.id`; `fees.container_id` is also its primary key. That structure describes at most one fee row per container.
5. **Try.** Open the file and identify the SQL declaration that produced the foreign-key output. You can now connect observed metadata to its declaration.

### 02 Read only the caller's permitted record

1. **Understand.** Bound values keep an input inside the query's fixed structure. A separate owner condition restricts whose record is returned. The host supplies caller A; C1 belongs to A, while C2 belongs to B. Pydantic then checks the returned fields and types. These are three separate jobs.
2. **Predict.** Should A receive C2's fee even when C2 is a valid ID?
3. **Run** [02_scoped_read.py](02_scoped_read.py). This lesson is offline.

   ```bash
   uv run python snippets/b4/02_scoped_read.py
   ```

4. **Observe.** C1 returns fee `100`, currency `USD`, source `training-db` and an `as_of` timestamp. Owner and private notes are omitted. The typed result describes its shape; it does not prove that the fee is correct or current.
5. **Try.** Change `container_id = "C1"` to `container_id = "C2"` and rerun. Expect `RESULT: unavailable`. Parameter binding alone would not supply this owner restriction.

### 03 Turn a question into SQL

1. **Understand.** LlamaIndex supplies the approved schema and business context to a model, then executes its SQL proposal. SQLAlchemy provides the database connection. The result still needs checking against a separately established expectation.

   This example starts with an **already approved caller-A snapshot**:

   | Container | Recorded status | Recorded USD fee |
   | --- | --- | --- |
   | C1 | delayed | 100 |
   | C4 | delayed | 50 |
   | C5 | on_time | 75 |

   C2 is absent before model access. “Recorded fee” does not establish an outstanding balance.

2. **Predict.** What should the total be for delayed containers? Which row must be excluded?
3. **Run** [03_question_to_sql.py](03_question_to_sql.py). **This makes a model call** using `OPEN_AI_KEY` from shared setup.

   ```bash
   uv run python snippets/b4/03_question_to_sql.py
   ```

4. **Observe.** Inspect the generated SQL for the delayed/USD conditions. The verified run returned:

   ```text
   ROWS: [(150,)]
   INDEPENDENT EXPECTATION: [(150,)]
   ```

   C1 and C4 contribute 100 + 50. C5 is on time. Generated SQL can vary; inspect your actual proposal and result. A rejected or failed query must remain a failure.

5. **Try.** Ask for the **maximum** recorded USD fee for delayed containers and change `expected` to `[(100,)]`. State that expectation before rerunning; do not copy it from the generated query's result.

## Part 2 · Check and use the result

### 04 Check what the calculation means

1. **Understand.** A query can execute successfully and count the wrong thing. A fee belongs to one container, but that container can have several tracking events. Joining those events can repeat the fee. This is a problem of **grain**: what each result row represents.
2. **Predict.** C1 has fee 100 and two events; C4 has fee 50 and one event. What happens if the joined rows are summed?
3. **Run** [04_check_business_meaning.py](04_check_business_meaning.py). This lesson is offline; the wrong query is deliberately prepared.

   ```bash
   uv run python snippets/b4/04_check_business_meaning.py
   ```

4. **Observe.** The wrong join returns `250 FAIL`. The `EXISTS` query checks event membership without repeating each fee and returns `150 PASS`. `SUM(DISTINCT fee)` also returns 150 on this fixture, but it removes repeated amounts rather than repeated containers.
5. **Try.** Change C4's fee from 50 to 100 and update `expected` to 200. Rerun: the join returns 300, `EXISTS` returns 200, and DISTINCT amounts returns 100. Equal fees expose the false repair.

### 05 Enforce access and detect partial output

1. **Understand.** A database must enforce permitted operations independently of model instructions. This example's SQLite authorizer permits reads of the approved fee table and rejects private reads and writes. A separate row cap controls how much output is displayed.
2. **Predict.** There are three approved rows and `row_cap = 2`. Can the displayed two rows represent the complete result?
3. **Run** [05_enforce_query_boundaries.py](05_enforce_query_boundaries.py). This lesson is offline.

   ```bash
   uv run python snippets/b4/05_enforce_query_boundaries.py
   ```

4. **Observe.** The approved read shows:

   ```text
   VISIBLE: [('C1', 100), ('C4', 50)] TRUNCATED: True
   ```

   The private-table read and DELETE print `REJECTED by database policy`. Fetching one extra row detects truncation. It does not limit how much work the database did; the progress callback supplies a separate instruction budget.

5. **Try.** Set `row_cap = 3` and rerun. All three approved rows should be visible with `TRUNCATED: False`; the forbidden operations should still be rejected. Output size and access policy are independent.

### 06 Give the agent the query capability

1. **Understand.** The familiar Agents SDK loop chooses a tool; LlamaIndex handles the tool's inner database question. The tool returns actual rows, column names, a truncation flag and source/time metadata. The agent must explain that evidence faithfully, including absence or failure.
2. **Predict.** Which delayed container has the highest recorded USD fee in A's snapshot?
3. **Run** [06_agent_queries_database.py](06_agent_queries_database.py). **Both the agent and SQL generation make model calls.**

   ```bash
   uv run python snippets/b4/06_agent_queries_database.py
   ```

4. **Observe.** Follow `TOOL QUESTION` → `SQL` → `ROWS` → `ANSWER`. The verified run returned C1/100 and cited `approved-fee-snapshot/A` with `2026-11-06T00:00:00Z`. Check that your answer preserves USD and the supplied timestamp. Fetching an old snapshot now does not make its observations current.
5. **Try.** Replace the user question with `What is the recorded USD fee for container C2? Cite source/time.` Expect no matching rows and an explanation of absence. An empty result does not establish a zero fee.

## Keep these boundaries clear

<details>
<summary>Access, execution limits and framework messages</summary>

- **Approved data:** these snapshots are synthetic trusted inputs. The examples do not implement upstream authentication or tenant projection. Production visibility needs enforcement through the owning service/database, such as grants, governed views or row policies. `include_tables` selects schema context; it does not authorise access.
- **Execution limits:** the SQLite authorizer restricts operations/tables; 03/06 also allow selected functions. The progress callback interrupts at its first callback after roughly 10,000 SQLite VM instructions. That is neither a wall-clock deadline nor a cumulative workflow budget. Changing the database URL does not transfer this SQLite policy to another engine.
- **Output limits:** 06 caps rows sent to the outer model after LlamaIndex fetches the raw result. That cap alone does not bound earlier database work or host memory. The agent's turn limit is another separate constraint.
- **Framework message:** fixed-table SQL needs no embedding service. LlamaIndex's embedding-disabled/MockEmbedding message refers to an unused internal placeholder. SQL generation still uses a real model call.

These small demonstrations do not establish production isolation or reliability. See [verification](VERIFICATION.md) for actual runs, changed inputs and supplied failure probes.

</details>

## Teaching and further reading

- [34-slide deck](../../slides-md/b4-enterprise-data.md), [Gamma text](../../slides-gamma/b4-enterprise-data.txt) and [module outline](../../B4-OUTLINE.md).
- [Optional SQL/API/write references](reference/README.md). B3's approval ideas carry into separately controlled writes; the longer demonstrations remain here.
- [Next module: B6 · RAG](../b6/README.md), before B5 evaluation.

The examples retain B1–B3's `gpt-4.1-mini`; recheck model access before class. Labs, assessments, new notebooks and deployment remain deferred.
