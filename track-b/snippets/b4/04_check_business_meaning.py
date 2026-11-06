"""Run a prepared wrong query, diagnose its grain, and verify a repair. No model call.

Try: make C4's fee 100 and update the independent expectation to 200.
"""

from sqlalchemy import create_engine, text

engine = create_engine("sqlite://")
with engine.begin() as connection:
    connection.exec_driver_sql("CREATE TABLE container_fees (container_id TEXT PRIMARY KEY, status TEXT, fee INTEGER)")
    connection.exec_driver_sql("CREATE TABLE events (container_id TEXT REFERENCES container_fees(container_id), kind TEXT)")
    connection.exec_driver_sql("INSERT INTO container_fees VALUES ('C1','delayed',100), ('C4','delayed',50), ('C5','on_time',75)")
    connection.exec_driver_sql("INSERT INTO events VALUES ('C1','scan'), ('C1','hold'), ('C4','hold')")
# Question: total recorded fees for delayed containers that have at least one event.
expected = 150  # One fee for C1 and one for C4, regardless of their event counts.
queries = [
    ("WRONG JOIN", """
        SELECT SUM(f.fee) FROM container_fees f
        JOIN events e ON e.container_id=f.container_id
        WHERE f.status='delayed'
    """),
    ("RIGHT GRAIN", """
        SELECT SUM(f.fee) FROM container_fees f WHERE f.status='delayed'
        AND EXISTS (SELECT 1 FROM events e WHERE e.container_id=f.container_id)
    """),
    ("DISTINCT AMOUNTS", """
        SELECT SUM(DISTINCT f.fee) FROM container_fees f
        JOIN events e ON e.container_id=f.container_id
        WHERE f.status='delayed'
    """),
]
with engine.connect() as connection:
    for label, sql in queries:
        actual = connection.execute(text(sql)).scalar_one()
        print(label, "expected:", expected, "actual:", actual, "PASS" if actual == expected else "FAIL")
engine.dispose()
# DISTINCT amounts matches this fixture by coincidence; equal fees expose why it is not a repair.
