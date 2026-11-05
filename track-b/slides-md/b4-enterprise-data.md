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

# B4 · From a useful query to a governed capability

Our workflow can request a fact.

Now we need to understand what a returned row means, who may receive it and how much work the read may perform.

<!--
Start from the B2/B3 tool rather than a SQL catalogue. The running data is synthetic container fees. Classroom queries use disposable SQLite; enterprise access choices will follow once the local read is understood.
-->

---

# A business question comes first

> Which containers have a fee above 100?

Prepared records:

| Container | Fee |
| --- | ---: |
| C1 | 100 |
| C2 | 200 |

What should the result contain?

<!--
Establish an independent expected answer before showing SQL. C2 qualifies and C1 does not under the strict 'above' requirement. The amounts are simplified teaching values. This small question lets shape and membership become visible separately.
-->

---

# Read the required rows

```sql
SELECT id, fee FROM containers
WHERE fee > ? ORDER BY id
```

Bind the threshold value 100.

Source: [row-reading example](../authoring/previous-codealongs-before-essential-selection/b4/01_read_rows.py)

<!--
Point to selected fields, predicate and ordering as separate choices. Run the source and inspect both cursor columns and actual rows. We have a useful query before adding generated SQL or enterprise controls.
-->

---

# Change the boundary, inspect the membership

Change `>` to `>=`.

Which row is newly included? Do the column names change?

A query has both an output shape and a rule for which records belong in it.

<!--
Have learners predict C1's inclusion. This exercise prepares them to inspect a generated query later. The ability to execute SQL is separate from correctly expressing the business question.
-->

---

# A requested ID is data

Now the user asks for C1's fee.

The request supplies a value to match, rather than permission to rewrite the SQL statement.

Keep the query structure owned by the application.

<!--
Move from a fixed threshold to external request input. Learners know API arguments from B2, so parameter binding is a familiar boundary applied to SQL. The next example contrasts an ordinary ID with SQL-looking text.
-->

---

# Bind values into fixed SQL

```python
for requested_id in ["C1", "C1' OR 1=1 --"]:
    rows = connection.execute(
        "SELECT id, fee FROM containers WHERE id = ?",
        (requested_id,),
    ).fetchall()
    print(repr(requested_id), rows)
```

Source: [02_bind_values.py](../authoring/previous-codealongs-before-essential-selection/b4/02_bind_values.py#L13)

<!--
Read the fixed query and the separate argument tuple. Run both requested IDs. The SQL-looking string remains one complete value and matches no supplied record. Binding does not by itself add caller scope or choose the right business calculation.
-->

---

# A new question needs an event table

> What are the total fees for containers that have an event?

| Container | Fee | Number of events |
| --- | ---: | ---: |
| C1 | 100 | 2 |
| C2 | 200 | 1 |

The intended total is 300.

<!--
Add one piece of data to create a concrete join problem. Establish that the measure belongs to a container, while events have their own rows. Ask learners to predict the joined rows before calculating anything.
-->

---

# A join changes the row meaning

```text
C1, 100, check
C1, 100, scan
C2, 200, scan
```

Summing the fee over these event rows gives 400.

The query ran successfully, but C1's fee was counted twice.

<!--
These rows follow the supplied grain example. The problem is not invalid SQL or arithmetic; it is summing at the wrong grain. This makes the repair necessary and provides vocabulary for later generated-query review.
-->

---

# Filter by membership without multiplying rows

```sql
SELECT SUM(c.fee) FROM containers c
WHERE EXISTS (
    SELECT 1 FROM events e
    WHERE e.container_id = c.id
)
```

Source: [grain example](../authoring/previous-codealongs-before-essential-selection/b4/03_preserve_grain.py)

<!--
EXISTS answers whether a matching event exists while retaining one row per container. Run the card and compare 400 with 300. Ask why SUM(DISTINCT fee) would fail when two different containers happen to have the same fee.
-->

---

# Describe the grain before generating a query

“One row per container” explains how to interpret the fee.

The schema also needs field meanings, units and relevant dates.

A model given only table names may produce plausible SQL with the wrong business meaning.

<!--
Use the join failure as motivation for richer schema context. The same documentation helps human reviewers. Approved examples and sample rows can help, but production-sensitive data should not be copied into a classroom prompt.
-->

---

# The application needs a useful capability

A status assistant should not need every table and internal field just to answer:

> What is this container's recorded fee?

Wrap the understood read in a narrow business contract.

<!--
Transition from query mechanics to the M11 capability-design story. SQL remains inside the owning service. Ask which inputs and result fields the caller actually needs, using B2's function-contract lesson.
-->

---

# State the capability contract

Illustrative enterprise contract:

```text
input: container_id
result: permitted fee, currency, as_of, source
absence: controlled unavailable result
```

The interface describes the business fact rather than storage internals.

<!--
This is a proposed richer contract, not a claim that every field is implemented by the tiny source. The existing scope card supplies ID and fee. Explain why source and freshness would matter when the same fact is later used in an answer.
-->

---

# The requested record may belong to someone else

The scope example adds ownership:

| Container | Owner | Fee |
| --- | --- | ---: |
| C1 | A | 100 |
| C2 | B | 200 |

The caller is A. Which record may the capability return?

<!--
Make the permission problem concrete before a security table. The caller identity is trusted classroom context, not a model-generated argument. C2 exists and has a well-formed ID, but neither establishes the caller's permission.
-->

---

# Apply both record and owner predicates

```python
result = connection.execute(
    "SELECT id, fee FROM containers WHERE id = ? AND owner = ?",
    (requested_id, trusted_owner),
).fetchone()
```

Source: [04_scope_capability.py](../authoring/previous-codealongs-before-essential-selection/b4/04_scope_capability.py#L16)

<!--
Explain the two placeholders and why the owner comes from host context. Run the complete card for C1, C2 and a missing ID. Only id and fee are selected; the internal note is not part of the permitted output.
-->

---

# Check identity before interpreting permission

Authentication establishes who the caller is.

Authorisation determines whether that caller may read this record.

The classroom owner string demonstrates the second decision; production identity must come from a trusted system.

<!--
The distinction now resolves an actual question about trusted_owner. Avoid introducing an entire authentication implementation. Ask why accepting owner='A' from the model's tool arguments would break the intended boundary.
-->

---

# Return controlled absence

An inaccessible record does not become available because the model asks more confidently.

The scope example returns “not available” for the missing and outside-owner records.

The result avoids exposing fields that the caller should not receive.

<!--
Explain what the actual source does rather than promise an enterprise error taxonomy. Different products may deliberately distinguish some absence cases. In this lesson the important property is that the forbidden fee and internal note do not leave the read path.
-->

---

# Publish the business capability through MCP

```text
host admits the tool
  → server checks trusted caller scope
  → service reads permitted fields
  → bounded result returns to the host
```

B2's protocol can carry this contract.

<!--
Reuse the familiar MCP boundary without teaching it again. This is the architectural mapping; the core SQL card is not a new governed MCP server. The server must enforce its own policy even when a calling host makes a mistake.
-->

---

# A model can help propose a query

The schema and business question can be supplied to a model.

The returned SQL is a candidate implementation of the question.

Use the same independent expected facts we used to review our hand-written query.

<!--
Introduce natural-language-to-SQL after learners can inspect SQL meaning and scope. The current live experiment runs on a separate synthetic all-container dataset. It does not inherit the owner fixture from the previous card or establish production-grade SQL isolation.
-->

---

# Supply the schema and question

```python
    messages=[
        {
            "role": "system",
            "content": "Return one plain SQLite SELECT, no fences. "
            "containers(id TEXT PRIMARY KEY, fee INTEGER); one row per container.",
        },
        {"role": "user", "content": "What is the total fee across all containers?"},
    ],
)
```

Source: [05_generated_sql.py](../authoring/previous-codealongs-before-essential-selection/b4/05_generated_sql.py#L24)

<!--
Read the one-row-per-container description and the requested total. Run the complete card and retain the actual proposed statement. It may be correct, wrong or malformed. Do not manufacture a particular failure to match a lecture script.
-->

---

# Inspect before trusting the result

For the two-row dataset, the independently known total is 300.

Check the proposed query's table, aggregation, joins and filters.

Then compare its actual result with the reference.

<!--
The complete card prints both actual rows and a known reference, or a controlled execution error. The tiny database is disposable and has a read-only setting and progress limit. Those are limited teaching controls, not permission to run arbitrary model SQL against production data.
-->

---

# Read-only stops a different failure

What if the proposed operation tries to delete records?

A read-only access path should reject the write.

That effect restriction still cannot decide whether a permitted total is the right total.

<!--
Separate two guarantees using the next card: a blocked DELETE and a permitted MAX that is wrong for SUM. The sequence matters because learners already understand the correct reference result.
-->

---

# Observe a blocked write and a wrong read

```python
connection.execute("PRAGMA query_only = ON")
try:
    connection.execute("DELETE FROM containers")
except sqlite3.OperationalError as error:
    print("write blocked:", error)
wrong_total = connection.execute("SELECT MAX(fee) FROM containers").fetchone()[0]
print("permitted read:", wrong_total, "known total:", 300)
```

Source: [06_read_only_effects.py](../authoring/previous-codealongs-before-essential-selection/b4/06_read_only_effects.py#L13)

<!--
Run the full source. query_only blocks the demonstrated DELETE while enabled, but MAX returns 200 instead of the known total 300. It is a mutable connection setting, not a hostile-SQL sandbox or an authorisation system.
-->

---

# A small result can require large work

A single aggregate row can scan or generate many intermediate rows.

Limiting returned rows bounds disclosure size.

Execution time and database work need their own limits.

<!--
Introduce resource controls through the one-row counterexample instead of a general checklist. Ask learners whether a row cap of two would stop a costly recursive aggregate. The next source makes that failure visible.
-->

---

# Detect result truncation

```python
row_cap = 2
rows = connection.execute("SELECT id FROM containers ORDER BY id").fetchmany(
    row_cap + 1
)
print("visible:", rows[:row_cap], "truncated:", len(rows) > row_cap)
```

Source: [07_bound_output_work.py](../authoring/previous-codealongs-before-essential-selection/b4/07_bound_output_work.py#L13)

Fetch one extra row to detect whether the visible result is incomplete.

<!--
Run the first part of the source. The result exposes truncation explicitly rather than silently pretending two rows are the full dataset. This bounds visible output, while the next part addresses work before any row returns.
-->

---

# Interrupt excessive database work

```python
def stop_work():
    global callbacks
    callbacks += 1
    return callbacks >= 5


connection.set_progress_handler(stop_work, 100)
```

Source: [07_bound_output_work.py](../authoring/previous-codealongs-before-essential-selection/b4/07_bound_output_work.py#L21)

The source's recursive aggregate is interrupted by a progress budget.

<!--
The progress handler is SQLite-specific classroom evidence. Run the complete query and inspect the actual interrupted outcome. Enterprise services may use timeouts, warehouse limits and connection controls; choose mechanisms appropriate to the real engine.
-->

---

# Carry the source and freshness forward

A fee has a record identity, currency and point in time.

The capability should preserve the information needed to interpret it.

An explanation must not silently turn a dated observation into a current guarantee.

<!--
Return to the richer contract introduced earlier. The toy cards isolate mechanisms and do not return every provenance field. Ask learners to name the additional fields a useful enterprise result would require, without claiming that code has already implemented them.
-->

---

# Record the access decision

An audit event should connect the caller, capability, permitted request and outcome.

For a denial, record that protected downstream work did not occur.

Keep unnecessary private result data out of the log.

<!--
Adapt M12's audit lesson after scope and limits have meaning. A polite denial is not proof if data already reached a log. Protected, durable audit storage is an enterprise implementation concern beyond the print-based teaching examples.
-->

---

# Choose an approved enterprise read path

Use a curated service, warehouse view or read replica with least privilege.

Scope credentials and define result, execution and connection limits.

Treat high-impact writes as a separate capability with an explicit approval boundary.

<!--
This operational summary lands after learners have experienced correctness, scope and cost failures. Briefly discuss managed short-lived credentials and avoiding broad shared service accounts. No production database access is required for the classroom builds.
-->

---

# The governed capability, assembled

```text
business question
  → narrow contract
  → trusted caller and permitted record
  → correct query at the right grain
  → bounded work and selected fields
  → interpretable result and audit outcome
```

<!--
Have learners explain which earlier example justifies each stage. This is the culmination of the module, rather than its opening taxonomy. A successfully executed query establishes only one part of the complete data-access claim.
-->

---

# Practice · Build and inspect the read

Complete the [B4 worked examples](../codealongs/b4/README.md).

Preserve correct totals, enforce caller scope and inspect an actual generated query.

Change a boundary or policy and compare with your predicted result. Labs will follow separately.

<!--
Ask learners to predict the wrong-owner and duplicated-fee outcomes before running. Keep the reference result independent of the implementation. A changed case with equal fees is useful for exposing an accidental DISTINCT-based repair.
-->

---

# B4 · A result with an explanation

We can explain what a row means, why it is correct, why the caller may receive it and how the read is bounded.

Next: B6 supplies evidence from documents when the required fact is a policy passage rather than a table row.

<!--
Use one final container question and ask for evidence for each claim. Avoid accepting a successful SQL execution as a substitute for all four. The distinction between structured facts and document evidence prepares the retrieval module.
-->
