"""Enforce trusted owner scope before returning selected fields.

Try: remove only the owner predicate. Does binding still prevent cross-owner access?
"""

import sqlite3

connection = sqlite3.connect(":memory:")
connection.row_factory = sqlite3.Row
connection.executescript("""
CREATE TABLE containers (id TEXT PRIMARY KEY, owner TEXT, fee INTEGER, note TEXT);
INSERT INTO containers VALUES ('C1', 'A', 100, 'private investigation');
INSERT INTO containers VALUES ('C2', 'B', 200, 'private contact');
""")
connection.execute("PRAGMA query_only = ON")
trusted_owner = "A"  # Trusted host identity fixture, never a model argument.


def read_fee(container_id):
    row = connection.execute(
        "SELECT id AS container_id, fee FROM containers WHERE id = ? AND owner = ? LIMIT 1",
        (container_id, trusted_owner),
    ).fetchone()
    if row is None:
        return {"status": "unavailable"}
    return {"status": "ok", **dict(row), "currency": "USD",
            "as_of": "2026-11-06T00:00:00Z", "source": "training-db"}


for container_id in ["C1", "C2", "C9"]:
    result = read_fee(container_id)
    print("AUDIT:", trusted_owner, "read_fee", container_id, result["status"])
    print("RESULT:", result)
connection.close()
# Missing and outside-owner records return the same public absence result.
