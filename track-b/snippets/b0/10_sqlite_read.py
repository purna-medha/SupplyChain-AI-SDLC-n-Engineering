"""Store two synthetic records and bind a lookup value. Try: query C9."""

import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE containers (container_id TEXT PRIMARY KEY, status TEXT)")
connection.executemany(
    "INSERT INTO containers VALUES (?, ?)", [("C1", "delayed"), ("C2", "on_time")]
)
container_id = "C1"
row = connection.execute(
    "SELECT status FROM containers WHERE container_id = ?", (container_id,)
).fetchone()
print("Recorded status:", row[0] if row else "unknown")
connection.close()

