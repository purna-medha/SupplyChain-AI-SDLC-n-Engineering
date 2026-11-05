# B4 standalone lab

Implement a scoped read using only SQLite and Python. This exercise has no model, server, seed file or capstone dependency.

## 1 · Worked example: inspect the owned boundary

Start with `snippets/b4/03_scoped_read_only.py`. Run it unchanged. Observe that caller A gets C1 and no C2, and that internal_note is never returned. Explain the separate roles of parameter binding, selected columns and the owner predicate. This complete card is the catch-up baseline; no previous lab is required.

## 2 · Guided practice: finish the scoped lookup

1. Save the starter below as `b4_lab.py` anywhere.
2. Replace the TODO with a fixed SELECT returning only id and fee. Bind caller and container_id separately.
3. Run `python3 b4_lab.py`; all three assertions must pass.
4. After seeding, enable query_only. Show a rejected DELETE in a try/except and verify the two original rows remain.
5. Explain why neither a successful SELECT nor query_only proves the caller scope is correct.

```python
import sqlite3

connection = sqlite3.connect(":memory:")
connection.executescript("""
CREATE TABLE containers (id TEXT, owner TEXT, fee INTEGER);
INSERT INTO containers VALUES ('C1','A',100), ('C2','B',200);
""")
caller = "A"  # Application-established scope fixture.

def read_fee(container_id):
    # TODO: parameterize both owner and id; return one row or None.
    raise NotImplementedError("Implement the scoped read")

assert read_fee("C1") == ("C1", 100)
assert read_fee("C2") is None
assert read_fee("C1' OR 1=1 --") is None
print("PASS: authorized, out-of-scope and injection-shaped inputs")
connection.close()
```

## 3 · Independent extension: preserve grain under caller scope

Start with your completed guided script. Extend the fixture setup before enabling query_only, and keep all new checks before connection.close(). Add an events table: C1 has two events and C2 has one. Set both container fees to 100; update the original C1 lookup expectation to match that explicit fixture change. Design a new operation returning the total fee for the trusted caller's containers that have at least one event. Keep identity outside the request and prevent event multiplicity from inflating the total. No implementation is supplied for this stage.

Before coding, write expected totals for caller A, caller B, an owner with no containers, and a second event added to C1. Decide and document whether an empty aggregate should return zero or None. Run `python3 b4_lab.py` and show named checks for all four scenarios. Duplicating an event must not change the corresponding total. Deliberately break the grain or scope rule, show a failing check, then restore the repair.

## Evidence to submit

Your completed script, before/after output where applicable, and two sentences explaining the mechanism. The three assertions pass. DELETE raises sqlite3.OperationalError. COUNT(*) remains 2. Assertions should fail if the taught rule is broken; do not delete failing cases.

## Optional PortOps transfer

After the independent lab, identify a corresponding read or review rule in PortOps. Describe how you would preserve its real identity, policy and tests. The classroom amounts and >=200 rule do not replace PortOps business policy. No capstone change is needed to complete this lab.
