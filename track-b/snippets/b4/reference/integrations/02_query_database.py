"""Read selected fields using a bound SQL value. No model or service needed.

Try: request C9, then C1' OR 1=1 --. The latter is still one identifier value.
"""

import sqlite3

connection = sqlite3.connect(":memory:")
connection.row_factory = sqlite3.Row
connection.executescript("""
CREATE TABLE containers (id TEXT PRIMARY KEY, fee INTEGER, currency TEXT, note TEXT);
INSERT INTO containers VALUES ('C1', 100, 'USD', 'private investigation');
INSERT INTO containers VALUES ('C2', 200, 'USD', 'private contact');
""")
connection.execute("PRAGMA query_only = ON")
container_id = "C1"
row = connection.execute(
    "SELECT id, fee, currency FROM containers WHERE id = ? LIMIT 1", (container_id,)
).fetchone()
print("RESULT:", dict(row) if row else "unavailable")
connection.close()
# The private note is omitted. Owner scope is introduced separately in example 03.
