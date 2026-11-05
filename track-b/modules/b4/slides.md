---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 25px; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 20px; line-height: 1.2; }
---
# B4 · A successful query is only one piece of evidence

How can we read the right facts for the right caller within a bounded amount of work?

Use C1=100 and C2=200 throughout; all records are synthetic.

<!-- Elicit four independent concerns: execution, meaning, authority and resource use. Keep the manual total 300 visible. -->

---

# A table gives each row a meaning

One row in `containers` represents one container. `id` names it; `fee` is an integer classroom amount.

Decide this unit before choosing an aggregate.

<!-- Ask what counting rows would mean. Do not imply real billing currency or policy. -->

---

# A query chooses shape and membership separately

```sql
SELECT id, fee
FROM containers
WHERE fee > 100
```

SELECT chooses fields; WHERE decides which rows qualify.

<!-- Open card 01. Explain the mechanism before executing; changing columns does not change the predicate. -->

---

# Predict the boundary before executing

C1 has fee 100. C2 has fee 200.

Which rows pass `fee > 100`? What changes with `fee >= 100`?

Write both results and the reason.

<!-- Pause for individual answers; do not reveal the result by running early. -->

---

# Equality changes membership, not output shape

`>` returns `(C2, 200)`. `>=` also returns `(C1, 100)`.

The predicate admits equality; the selected columns remain id and fee.

<!-- Run card 01, change only the operator, and connect the extra row to the predicate. -->

---

# Parameters keep values out of query syntax

```python
query = "SELECT id, fee FROM containers WHERE id = ?"
rows = connection.execute(query, (container_id,)).fetchall()
```

The query structure is fixed before the identifier is supplied.

<!-- Open card 01. The single-item tuple supplies one value; it is not string interpolation. -->

---

# Predict an identifier that looks like SQL

The bound identifier is `C1' OR 1=1 --`.

Does the lookup match C1, every row, or no row?

Explain what the database receives as instructions.

<!-- Have learners distinguish the fixed statement from the bound string. -->

---

# A bound value remains a whole value

No row has that complete identifier, so the result is empty.

The string does not create a new OR condition. A placeholder cannot stand for a table name or an entire query.

<!-- Run card 01. Ask why a parameterized C2 lookup can still violate caller authorization. -->

---

# A join can change the unit of a row

C1 has arrived and reviewed events. C2 has one arrived event.

Joining containers to events produces one row per matching event, carrying the container fee each time.

<!-- Sketch C1 twice and C2 once; learners should see the multiplication before SQL. -->

---

# Predict the total after the join

```sql
SELECT SUM(fee)
FROM containers JOIN events
ON id = container_id
```

Will this answer “total fee across containers with events”?

<!-- Pause before card 02. Ask learners to enumerate the values being summed. -->

---

# The repeated fee explains the wrong total

The joined values are 100, 100 and 200: total **400**.

The intended container total is **300**. SQL executed correctly; the chosen row grain answered a different question.

<!-- Run card 02. Locate the error in data meaning rather than SQL syntax. -->

---

# EXISTS filters without multiplying containers

```sql
SELECT SUM(fee) FROM containers
WHERE EXISTS (
  SELECT 1 FROM events WHERE container_id = id
)
```

Each container contributes once when at least one matching event exists.

<!-- Contrast membership with joined output. The inner SELECT asks only whether a match exists. -->

---

# Equal amounts expose a misleading repair

Change both fees to 100.

`SUM(DISTINCT fee)` returns 100, although two containers owe 200 in total.

Distinct amounts are not distinct containers.

<!-- Ask learners to predict before changing card 02. Update its expected values deliberately; the original assertion encodes the original fixture. -->

---

# Caller scope belongs to the host

The host establishes owner A. The request supplies C1 or C2.

Allowing the request or model to choose the trusted owner would move authority across the wrong boundary.

<!-- Clarify the fixture is not authentication. In a deployed application identity comes from authenticated context. -->

---

# A narrow capability owns query and fields

```python
row = connection.execute(
    "SELECT id, fee FROM containers WHERE owner = ? AND id = ?",
    (authenticated_owner, container_id),
).fetchone()
```

The query binds values and enforces owner membership.

<!-- Open card 03. Note that internal_note is absent from the selected fields. -->

---

# Predict access for owner A

C1 belongs to A; C2 belongs to B.

What does `read_fee("C2")` return? What changes if the owner predicate is removed?

<!-- Keep prediction separate from the run; ask whether parameters alone would prevent the leak. -->

---

# Both predicates must hold before a fee leaves

C1 returns its fee; C2 returns no authorized row.

Removing the owner predicate leaks C2 even though the id is safely parameterized.

<!-- Run card 03, temporarily remove owner predicate and its bound value, observe the leak, then restore both. -->

---

# Generated SQL is a proposal to inspect

A schema supplies names and types. Row meaning supplies the unit of counting.

Neither makes a model proposal authoritative or factually correct.

<!-- Introduce live card 04 only after learners can manually compute 300. -->

---

# The live experiment exposes the actual proposal

```python
sql = response.choices[0].message.content
print("actual model SQL:", sql)
rows = connection.execute(sql).fetchmany(3)
```

Use only the disposable classroom database. Compare the proposal with the question.

<!-- Run configured card 04. If offline, state SKIPPED; do not replace missing inference with a claimed model output. -->

---

# Unexpected SQL needs diagnosis before repair

If the proposal fails, inspect raw SQL and the SQLite error. If it runs, inspect columns, grain and arithmetic.

Try “average fee”; the manual reference is 150.

<!-- Do not preclaim live outcomes. A fenced answer can fail syntax; a count can run but answer the wrong question. -->

---

# Read-only constrains effects while enabled

```python
connection.execute("PRAGMA query_only = ON")
```

This setting rejects writes. It does not choose the right rows or calculation.

<!-- Introduce card 03 as a limited connection behavior, not an enterprise sandbox. -->

---

# Predict permission separately from correctness

With query_only enabled, classify:

- `DELETE FROM containers`
- `SELECT SUM(fee) + 1 FROM containers`

Which executes? Which correctly answers the total-fee question?

<!-- Require two columns in the learner answer: execution allowed and semantically correct. -->

---

# A permitted read can still be wrong

DELETE raises; the two original rows remain. The SELECT executes and returns 301, which is incorrect.

Arbitrary SQL could turn query_only off; this setting alone is not a hostile-SQL boundary.

<!-- Revisit card 03, then add the prepared SELECT above before connection.close(). Reconnect to the fixed scoped capability as the safer interface. -->

---

# One output row can require substantial work

SUM over millions of inputs still returns one row.

Fetching fewer result rows controls consumption, not how much work the database already performed.

<!-- Ask learners to distinguish rows examined from rows returned before introducing the callback. -->

---

# A result cap should disclose truncation

```python
rows = cursor.fetchmany(2)
print("visible:", rows[:1], "truncated:", len(rows) > 1)
```

Fetching cap + 1 lets the host indicate that the displayed result is incomplete.

<!-- Open card 05. A truncated list must not be presented as a complete total. -->

---

# A progress callback interrupts database work

SQLite periodically invokes a callback after instruction intervals. Returning a nonzero value interrupts the query.

A callback budget and a time check bound different aspects of cooperative work.

<!-- Run card 05. The callback count is not a row count; scheduling and callback intervals prevent a hard deadline guarantee. -->

---

# Diagnose a slow one-row result at the work boundary

Symptom: an aggregate returns one row but takes too long.

Reducing fetchmany cannot repair work already performed. Inspect the query plan or apply an execution budget; preserve a clear interrupted outcome.

<!-- Ask learners to locate the boundary first. Do not silently convert interruption into a valid zero total. -->

---

# Practice fades from a working read to a new policy

Worked: inspect card 03.
Guided: finish the scoped lookup in `lab.md`.
Independent: design a scoped aggregate with repeated events and equal fees.

<!-- Explain exact lab evidence. The independent stage intentionally supplies no implementation. -->

---

# Transfer requires all four questions again

For a new data source, identify:

- What executes?
- What does each row mean?
- Who may see it?
- What work and output are allowed?

<!-- Invite a learner to apply these to a different operational table without inventing production policy. -->

---

# Explain the guarantee and its limit

Choose parameters, EXISTS, scoped capability, query_only or progress callback.

State one failure it prevents and one failure it cannot prevent.

<!-- Use assessment questions for individual retrieval; require mechanisms rather than naming features. -->

<!-- Teaching-source map: s01_read_rows.py for shape/predicates; s02_bind_values.py for data versus syntax; s03_preserve_grain.py for join membership; s04_scope_capability.py for trusted visibility; s05_generated_sql.py for actual proposals; s06_read_only_effects.py for effect permission; s07_bound_output_work.py for separate budgets. All live in ../../teaching-snippets/b4/. Guided composition: codealong-plan.md. -->
