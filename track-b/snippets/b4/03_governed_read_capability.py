"""Expose a narrow read with trusted owner scope, selected fields and a row bound.

Try: request C2 as owner A, then request more than the allowed row count.
"""

import sqlite3

connection = sqlite3.connect(":memory:")
connection.executescript("""
CREATE TABLE containers (id TEXT, owner TEXT, fee INTEGER, note TEXT);
INSERT INTO containers VALUES ('C1', 'A', 100, 'private investigation');
INSERT INTO containers VALUES ('C2', 'B', 200, 'private contact');
""")
connection.execute("PRAGMA query_only = ON")
trusted_owner = "A"  # Supplied trusted identity fixture; never a model argument.


def read_fee(container_id, max_rows=1):
    if type(max_rows) is not int or not 1 <= max_rows <= 2:
        raise ValueError("Row budget must be 1 or 2")
    return connection.execute(
        "SELECT id, fee FROM containers WHERE id = ? AND owner = ? LIMIT ?",
        (container_id, trusted_owner, max_rows),
    ).fetchall()


for container_id, limit in [("C1", 1), ("C2", 1), ("C1", 100)]:
    try:
        print(container_id, read_fee(container_id, limit))
    except ValueError as error:
        print("Denied:", error)
connection.close()
