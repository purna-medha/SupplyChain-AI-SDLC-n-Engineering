"""A successful SQL query can repeat a measure at the wrong row grain.

Try: give C1 and C2 equal fees; explain why SUM(DISTINCT fee) is not a repair.
"""

import sqlite3

connection = sqlite3.connect(":memory:")
connection.executescript("""
CREATE TABLE containers (id TEXT PRIMARY KEY, fee INTEGER);
CREATE TABLE events (container_id TEXT, kind TEXT);
INSERT INTO containers VALUES ('C1', 100), ('C2', 200);
INSERT INTO events VALUES ('C1', 'scan'), ('C1', 'check'), ('C2', 'scan');
""")
rows = connection.execute(
    "SELECT id, fee FROM containers WHERE fee > ?", (100,)
).fetchall()
print("Fees above 100:", rows)

joined = connection.execute("""
SELECT c.id, c.fee, e.kind FROM containers c
JOIN events e ON c.id = e.container_id
""").fetchall()
print("One row per event:", joined)
print("Wrong total:", sum(row[1] for row in joined))

correct = connection.execute("""
SELECT SUM(c.fee) FROM containers c
WHERE EXISTS (SELECT 1 FROM events e WHERE e.container_id = c.id)
""").fetchone()[0]
print("One fee per container:", correct)
connection.close()
