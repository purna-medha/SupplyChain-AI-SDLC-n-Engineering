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

# B4 · Querying enterprise data with AI agents

A business question, an approved database path and a checked answer

Schema · SQLAlchemy Core · LlamaIndex · Agent tools

<!--
60-minute lecture: slides 2–17, 28 minutes; 18–26, 19 minutes; 27–34, 13 minutes. Explain concepts before opening their complete examples. Slides 31/32 are brief optional enterprise extensions. Run selected examples; variations support further exploration. All records/callers/fees are synthetic. Course order: B1 → B2 → B3 → B4 → B6 → B5. Source: ../B4-OUTLINE.md. Execution observations: ../snippets/b4/VERIFICATION.md. No HTTP service is needed for the six core files.
-->

---

# The business question

> What is the total recorded USD fee for my delayed containers?

We need to identify the caller's permitted records, select delayed containers and add each recorded fee once.

**Predict:** what information must the application obtain before it can answer?

<!--
Answer cue: trusted caller context, approved records, status/fee definitions and currency. The model's general shipping knowledge cannot establish private recorded fees. A recorded fee is not automatically an outstanding balance; the fixture has no payments data.
-->

---

# The next capability after B1–B3

| Earlier capability | What B4 adds |
| --- | --- |
| B1: use a model | Supply authoritative structured facts |
| B2: obtain facts through tools | Back a capability with a database |
| B3: coordinate a task | Query and interpret permitted business data |

The agent loop stays familiar. The data capability becomes richer.

<!--
Keep the focus on what the application can now do. A database connection is not a new agent architecture. Approved APIs and semantic services may also be the organisation's access path.
-->

---

# Known lookups and analytical questions

| Request | Suitable starting point |
| --- | --- |
| “What is C1's recorded fee?” | Fixed query with a container-ID parameter |
| “What is the total for delayed containers?” | Analytical query over approved data |

Use an existing approved business API or semantic interface when it provides the needed capability.

<!--
We first understand a fixed operational read, then add flexible question-to-SQL generation. This is not a recommendation to expose arbitrary production SQL. The capability owner chooses the access path.
-->

---

# The synthetic business records

| Container | Owner | Recorded status | Fee |
| --- | --- | --- | --- |
| C1 | A | delayed | USD 100 |
| C2 | B | delayed | USD 200 |
| C4 | A | delayed | USD 50 |
| C5 | A | on_time | USD 75 |

Lookup examples use C1/C2. Analytics uses A's C1/C4/C5 snapshot.

<!--
Establish the business facts before SQL. The files create separate disposable fixtures; they do not form a shared database pipeline. C2 belongs to B in B4. The later B5 evaluation fixture is separate and gives both known records to A. Preserve this distinction when teaching across modules.
-->

---

# Tables describe rows and relationships

The first example separates containers from their fees:

```text
containers: id, owner, status       one row per container
fees: container_id, fee, currency   one fee row per container

fees.container_id → containers.id
```

A **primary key** identifies a row. A **foreign key** declares a relationship to another table.

<!--
01 uses only C1/C2. fees.container_id is both its primary key and a declared foreign key. We inspect the declaration; the demonstration does not establish that every database constraint was exercised. Later events can have several rows per container, which makes row meaning important.
-->

---

# Inspect the actual schema

SQLAlchemy's Inspector reads database metadata.

```python
inspector = inspect(engine)
print(inspector.get_table_names())
print(inspector.get_columns("fees"))
print(inspector.get_foreign_keys("fees"))
```

[Complete schema-inspection example](../snippets/b4/01_inspect_schema.py)

<!--
The complete file creates its fixture and iterates actual tables, columns, primary keys and declared foreign keys. This excerpt selects a few calls. The engine's connection responsibility is explained before executing a business query. No ORM classes are needed.
Sources: https://docs.sqlalchemy.org/en/21/core/reflection.html and https://docs.sqlalchemy.org/en/21/tutorial/engine.html
-->

---

# Schema and business meaning

Metadata can tell us that a column is called `fee`.

It cannot establish whether that amount is recorded, invoiced or outstanding, or which date/status defines “delayed this week”.

Agree on the calculation, units and time window before querying.

<!--
An ambiguous question requires clarification. Our contract uses recorded status='delayed', one recorded fee per container and USD. No payments table exists, so the snapshot cannot establish an outstanding balance. A current status and any historical delay event are different conditions.
-->

---

# The fixed lookup's contract

```text
User input:      requested container ID
Trusted context: caller A
Read:            matching ID AND matching owner
Return:          ID, fee, currency and observation time
```

The lookup fixture keeps these fields in one `container_fees` table.

The host supplies the caller identity; the model does not choose it.

<!--
02 is independent of 01 and combines lookup fields to isolate a small business read. It contains C1/A/100 and C2/B/200, plus a private note omitted from the output. This host identity is a classroom fixture, not an authentication implementation.
-->

---

# SQL selects fields and matching rows

For A's request about C1, the intended read is:

```sql
SELECT container_id, fee, currency, as_of
FROM container_fees
WHERE container_id = 'C1' AND owner = 'A'
LIMIT 1
```

`SELECT` chooses fields. `WHERE` filters rows. `LIMIT` caps output.

**Predict:** what should this read return if the requested ID is C2?

<!--
This literal SQL is a conceptual illustration of 02's fixed query, not the Python input-binding implementation. Answer cue: no row, because C2 belongs to B. A valid ID alone does not establish access. The amount is not returned for denied or missing records.
-->

---

# SQLAlchemy executes the database operation

```text
Engine       manages connectivity to a database
    ↓
Connection   executes a SQL statement with supplied values
    ↓
Result       exposes the returned rows
```

Creating an engine does not perform the business read. Executing the statement does.

<!--
The complete scripts use create_engine('sqlite://') for disposable in-memory SQLite. SQLAlchemy Core gives connections, SQL execution and result handling without requiring ORM model classes. Creation/fixture setup is ordinary application code; it is independent of model decisions.
Source: https://docs.sqlalchemy.org/en/21/tutorial/engine.html
-->

---

# Bound values inside a fixed query

```python
row = connection.execute(text(
    "SELECT container_id, fee, currency, as_of FROM container_fees "
    "WHERE container_id = :id AND owner = :owner LIMIT 1"
), {"id": container_id, "owner": trusted_owner}).mappings().first()
```

`:id` and `:owner` receive values without rewriting the statement.

`mappings()` exposes named fields; `first()` obtains the first row, if any.

[Complete scoped read](../snippets/b4/02_scoped_read.py)

<!--
The preceding slides establish the query and connection before this excerpt. The full file opens the connection and supplies container_id/trusted_owner. Values bind separately from SQL structure; the owner condition separately supplies this tool's scope. A selected result omits owner/private_note.
Source: https://docs.sqlalchemy.org/en/21/tutorial/dbapi_transactions.html
-->

---

# Scope and bound values have separate jobs

Observed lookup variations for caller A:

| Requested ID | Public result |
| --- | --- |
| C1 | Recorded fee 100 USD |
| C2 | Unavailable |
| C9 | Unavailable |
| `C1' OR 1=1 --` | Unavailable |

The owner condition restricts membership. Binding keeps an input a value.

<!--
Default and changed-input observations are captured in the B4 verification record. Unknown and inaccessible records have the same public result. SQL-looking text is still one bound ID value, not a change to the query's syntax.
-->

---

# A typed business result

Pydantic checks the declared result fields and types:

```python
class FeeRecord(BaseModel):
    container_id: str
    fee: StrictInt
    currency: str
    as_of: datetime
```

Correct shape still needs factual, permission and freshness checks.

<!--
Excerpt from 02; its full model also supplies the source label training-db. model_validate checks the selected row. StrictInt rejects text/bool amounts. Structure cannot establish that a recorded amount is current or correctly calculated.
Source: https://pydantic.dev/docs/validation/latest/concepts/models/
-->

---

# The approved analytics snapshot

For analytics, the later examples start with this separate approved input:

| Container | Recorded status | Recorded USD fee |
| --- | --- | --- |
| C1 | delayed | 100 |
| C4 | delayed | 50 |
| C5 | on_time | 75 |

C2, owner fields and private notes are absent before model access.

<!--
This is a new fixture/projection, not a model-generated tenant filter or a pipeline implemented by earlier scripts. 03/06 include currency and as_of; 04/05 retain only fields needed for their lessons. Production visibility must come from an enforced trusted data/policy path, such as grants, views, row policies or the owning service. include_tables alone does not authorise access.
-->

---

# Establish the answer before generating SQL

For the delayed-container question:

```text
C1: delayed → contributes 100
C4: delayed → contributes  50
C5: on_time → excluded

Independent expected total: 150 USD
```

**Predict:** what would the total become if the status condition were omitted?

<!--
Answer cue: 225 USD. Derive expectations from the business facts and definition, not from the same query being checked or a model's approval of itself. The full 03 file supplies expected=[(150,)] independently.
-->

---

# SQL expresses the intended calculation

```sql
SELECT SUM(fee)
FROM container_fees
WHERE status = 'delayed' AND currency = 'USD'
```

`WHERE` selects eligible rows. `SUM` adds their fee values.

This hand-understood query describes what a generated proposal must achieve.

<!--
A conceptual query over the approved A snapshot. It establishes the calculation before introducing text-to-SQL. Status and currency filters matter; the snapshot already establishes caller visibility. No payments/balance calculation is implied.
-->

---

# The model proposes the query

```text
Question + approved schema + business definitions
                         ↓
                  Model proposes SQL
                         ↓
             Restricted database executes
                         ↓
                    Actual rows
```

The application still checks permission and business meaning.

<!--
SQL generation does not grant access or establish correctness. The connection policy rejects unapproved operations independently of the proposal. Fixed-table schema context needs no vector retrieval. Schema/metadata also require approval for disclosure.
Source: https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/
-->

---

# LlamaIndex supplies the query capability

```python
database = SQLDatabase(
    engine, include_tables=["container_fees"], sample_rows_in_table_info=0
)
query_engine = NLSQLTableQueryEngine(
    sql_database=database, tables=["container_fees"],
    llm=llm, synthesize_response=False,
)
```

The selected table supplies schema context. Database policy separately enforces access.

[Complete question-to-SQL example](../snippets/b4/03_question_to_sql.py)

<!--
The complete file supplies llm, business definitions, approved fixture and SQLite authorizer/progress policy. The excerpt shortens model construction and omits context_str_prefix. sample_rows=0 omits automatic sample-row prompting; it does not prevent returning rows. synthesize_response=False exposes raw results before a second generated explanation. Embeddings are disabled for this fixed-table path; the unused MockEmbedding setup message does not replace an actual SQL-generation call.
-->

---

# Inspect the proposal and actual result

Observed model proposal, formatted:

```sql
SELECT SUM(container_fees.fee) FROM container_fees
WHERE container_fees.status = 'delayed'
  AND container_fees.currency = 'USD';
```

```text
ROWS: [(150,)]
INDEPENDENT EXPECTATION: [(150,)]
```

<!--
Actual 03 observation, 6 November 2026. SQL spelling/format may vary. The changed maximum-fee question returned [(100,)]. A matching result on one fixture is evidence, not proof of all query semantics. 03 rejects a response lacking successful result metadata rather than treating an SQL error as an empty or zero result.
-->

---

# A valid join can repeat a fee

New question: total fees for delayed containers **with at least one event**.

Joining tracking events introduces several rows per container:

```text
C1, fee 100, scan
C1, fee 100, hold
C4, fee  50, hold
```

**Predict:** sum these joined rows. Does the result still represent one fee per eligible container?

<!--
Answer cue: 250, while the intended total is 150. 04 executes a deliberately prepared wrong join, not a claimed model mistake. Its question is recorded fees for delayed containers that have at least one event. Each fee must contribute once; the join changes result grain to event rows.
-->

---

# Preserve one contribution per container

`EXISTS` checks event membership without multiplying fee rows:

```sql
SELECT SUM(f.fee)
FROM container_fees f
WHERE f.status='delayed'
AND EXISTS (
    SELECT 1 FROM events e WHERE e.container_id=f.container_id
)
```

Wrong join: **250**. Intended grain: **150**.

[Complete semantic failure and repair](../snippets/b4/04_check_business_meaning.py)

<!--
Explain grain as what one row represents. The fixed calculation contributes one fee per eligible container. The expected total is supplied independently. Schema permission and syntax validity cannot establish that this measure was calculated at the correct grain.
-->

---

# Equal amounts expose a false repair

Give C1 and C4 a recorded fee of USD 100 each.

| Approach | Result |
| --- | --- |
| Intended one fee per eligible container | 200 |
| Join over all event rows | 300 |
| SUM of DISTINCT fee amounts | 100 |

Distinct amounts do not identify distinct containers.

<!--
Verified 04 variation with independent expectation updated to 200. DISTINCT happened to return 150 on the original fixture. Equal values expose why it is not a general repair. Keep the expectation independent when changing data.
-->

---

# The database enforces execution boundaries

| Attempt | Observed outcome |
| --- | --- |
| Read the approved fee table | Permitted |
| Read private_contacts | Rejected |
| Delete fee records | Rejected |

A model instruction alone cannot supply this enforcement.

[Complete database-policy example](../snippets/b4/05_enforce_query_boundaries.py)

<!--
05 installs a SQLite connection authorizer. 03/06 additionally permit selected aggregate/string functions. Actual controlled probes also rejected ATTACH and policy-changing PRAGMA operations. Schema is inspected/cached before restriction in model examples. The approved snapshot supplies row visibility; the callback supplies table/operation restrictions. Production systems need their own tested identities/policies; these callbacks are not a portable production sandbox certification.
Source: https://www.sqlite.org/c3ref/set_authorizer.html
-->

---

# Partial output and database work

With three approved rows and a display cap of two:

```text
VISIBLE: [('C1', 100), ('C4', 50)]
TRUNCATED: True
```

Fetching one extra row detects incomplete output.

A separate progress callback limits query instructions. A row cap does not bound earlier database work.

<!--
05 uses fetchmany(row_cap+1). Changing row_cap to 3 shows all rows with False. The SQLite progress handler interrupts at its first callback after roughly 10,000 VM instructions: not a wall-clock deadline or cumulative workflow budget. In 06 the outer-model row cap applies after LlamaIndex fetches raw results, so it alone does not bound memory/prior work.
-->

---

# Empty, zero and failed results

| Observation | Meaning depends on the contract |
| --- | --- |
| Empty rows | No matching visible records |
| NULL SUM over no matches | No non-NULL amount contributed |
| Recorded fee of 0 | A supplied zero amount |
| Query rejected or failed | No successful result to answer from |

A failed read must not become a fabricated zero fee.

<!--
03 checks for result metadata because LlamaIndex can represent SQL errors in a response. 06 returns query_failed for missing result metadata. A COUNT of no rows may legitimately be zero; specify the measure. The verified C2 lookup returned [] and no fee.
-->

---

# A query capability inside the familiar agent loop

```text
User asks a fee question
    SDK agent selects query_fees(question)
    LlamaIndex proposes SQL; restricted database executes
    Tool returns rows, columns, source/time and truncation
    SDK agent explains that evidence
```

B2's tool interaction now contains a governed database query.

<!--
The outer SDK runtime and inner query engine have separate roles. Both make actual model calls. Reuse B2's request/execution/observation model; do not introduce another orchestration architecture. The supplied snapshot's upstream approval is a classroom precondition.
-->

---

# The query tool returns database evidence

```python
@function_tool
async def query_fees(question: str) -> dict:
    response = await query_engine.aquery(question)
    # Check failure; return actual rows and source/snapshot metadata.
```

An empty result, a failed query and truncated output need explicit reporting.

[Complete SDK agent with a LlamaIndex query tool](../snippets/b4/06_agent_queries_database.py)

<!--
Abbreviated body. The complete file prints tool question, actual SQL and rows, checks result metadata, and returns columns/rows/status/source/as_of/truncated. It caps rows sent to the outer model after raw fetching. The tool executes async on the SQLite connection's owning thread. Model instructions request faithful explanations but are not independent factual enforcement.
-->

---

# Inspect the complete evidence path

Observed highest-delayed-fee request:

```text
Question: highest recorded USD fee among delayed containers
SQL: ... WHERE status='delayed' AND currency='USD'
     ORDER BY fee DESC LIMIT 1
ROWS: [('C1', 100)]
Answer: C1, USD 100, with source and snapshot time
```

**Predict:** what should the agent report when asked for absent C2?

<!--
Condensed actual 06 observation, 6 November 2026. Source approved-fee-snapshot/A; as_of 2026-11-06T00:00:00Z. C2 variation returned [] and reported absence without a fee. A max_turns=1 variation stopped incomplete. These observations are not reliability estimates or guaranteed future answers.
-->

---

# Preserve the observation's scope and time

A useful answer retains the record identity, currency, source and observation time.

A partial result must remain visibly partial.

**Predict:** does querying a midnight snapshot at noon make its observations current at noon?

<!--
Answer cue: no. Snapshot time differs from fetch time. Preserve 2026-11-06T00:00:00Z rather than silently substituting now. In production, preserve per-record currency/time and coverage rather than assuming every result uses this classroom's fixed metadata.
-->

---

# Extension · Larger schemas and accepted metrics

Retrieve only relevant, approved table descriptions and relationships when a schema becomes large.

A governed view or semantic interface can define an accepted measure instead of asking the agent to invent its calculation.

The organisation still owns definitions, data quality and access policy.

<!--
Optional enterprise extension. LlamaIndex SQLTableRetrieverQueryEngine retrieves schema context; B6 later teaches embeddings/retrieval. dbt MetricFlow is an example of business-owned semantic metrics and relationship-driven query generation. No new installation is required here. Retrieved metadata must be approved for disclosure. A semantic layer does not guarantee every result.
Sources: https://developers.llamaindex.ai/python/examples/index_structs/struct_indices/sqlindexdemo/ and https://docs.getdbt.com/docs/build/about-metricflow
-->

---

# Extension · Separate controlled writes

An analytical query does not authorise changing a business record.

Reuse B3's exact-payload review and recheck permission within a transaction.

A retry after a lost reply needs the same operation identity and compatible payload.

[Optional reviewed write](../snippets/b4/reference/integrations/06_approved_database_action.py) · [Optional sequential retry](../snippets/b4/reference/integrations/07_prevent_duplicate_actions.py)

<!--
Supporting references, not a new core workflow. The reviewed-write example uses actual SDK pause/resume and a disposable SQLite insert; host review and the tool enforce owner/exact payload. The sequential retry example shows created/reused/conflict, not durable concurrent idempotency or actual network-loss reconciliation. No external message is sent. Commit/rollback determine persistence inside the transaction.
-->

---

# The libraries implement distinct responsibilities

| Library | Responsibility |
| --- | --- |
| SQLAlchemy Core | Metadata, connections and SQL execution |
| LlamaIndex | Schema-grounded question-to-SQL capability |
| Pydantic | Declared fields/types for a business result |
| Agents SDK | Model decisions and tool feedback |

Business meaning and permitted access remain explicit application requirements.

<!--
Return to mechanisms only after learners have seen their purpose. SQLDatabase wraps SQLAlchemy; include_tables supplies schema context. The database/service policy is separate from generation/orchestration. The six complete examples implement one learning step each, without teaching helpers.
-->

---

# An inspectable answer to the business question

Select the caller's permitted delayed records, add each fee once and compare the actual result with the intended calculation.

Retain the source, observation time and any failure or output limit.

Next, B6 supplies document evidence when rows cannot answer the question.

<!--
Return to the opening question: A's C1 and C4 contribute USD 150. Ask learners to identify source, scope, calculation and evidence in their own words. Labs, assessments and new notebooks remain deferred. Markdown is the authoritative source; its matching Gamma text carries the same visible teaching sequence.
-->
