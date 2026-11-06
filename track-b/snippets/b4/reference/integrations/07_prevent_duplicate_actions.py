"""Use a stable operation ID to prevent duplicate drafts. No model needed.

Try: give the second call a new request_id. Predict the number of rows.
"""

import sqlite3

connection = sqlite3.connect(":memory:")
connection.execute("CREATE TABLE drafts (request_id TEXT PRIMARY KEY NOT NULL, container_id TEXT, reason TEXT)")


def create_draft(request_id, container_id, reason):
    existing = connection.execute("SELECT container_id, reason FROM drafts WHERE request_id = ?",
                                  (request_id,)).fetchone()
    if existing and existing != (container_id, reason):
        return "conflict: same operation ID with a different payload"
    connection.execute("INSERT INTO drafts VALUES (?, ?, ?) ON CONFLICT(request_id) DO NOTHING",
                       (request_id, container_id, reason))
    connection.commit()
    return "reused" if existing else "created"


print(create_draft("request-001", "C1", "Customs hold"))
print(create_draft("request-001", "C1", "Customs hold"))  # Retry after a lost response.
print(create_draft("request-001", "C1", "Different reason"))
print("ACTUAL ROWS:", connection.execute("SELECT * FROM drafts").fetchall())
connection.close()
# This is a sequential example. Concurrent retries and durable storage need a service design.
