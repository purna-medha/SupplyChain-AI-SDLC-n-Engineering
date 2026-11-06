"""Database policy enforces allowed reads, separately from a model prompt.

Try: change the row cap, then explain why it is not a database-work budget.
"""

import sqlite3
from sqlalchemy import create_engine, text
from sqlalchemy.exc import DatabaseError

engine = create_engine("sqlite://")
with engine.begin() as connection:
    connection.exec_driver_sql("CREATE TABLE container_fees (container_id TEXT PRIMARY KEY, fee INTEGER)")
    connection.exec_driver_sql("INSERT INTO container_fees VALUES ('C1',100), ('C4',50), ('C5',75)")
    connection.exec_driver_sql("CREATE TABLE private_contacts (note TEXT)")
    connection.exec_driver_sql("INSERT INTO private_contacts VALUES ('synthetic-internal-only')")


def authorise(action, table, column, db, origin):
    allowed = (action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION)
               or action == sqlite3.SQLITE_READ and table == "container_fees")
    return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY


with engine.connect() as connection:
    raw = connection.connection.driver_connection
    raw.set_authorizer(authorise)
    raw.set_progress_handler(lambda: 1, 10000)
    row_cap = 2
    for sql in ["SELECT * FROM container_fees ORDER BY container_id",
                "SELECT * FROM private_contacts", "DELETE FROM container_fees"]:
        print("SQL:", sql)
        try:
            rows = connection.execute(text(sql)).fetchmany(row_cap + 1)
            print("VISIBLE:", rows[:row_cap], "TRUNCATED:", len(rows) > row_cap)
        except DatabaseError:
            print("REJECTED by database policy")
engine.dispose()
# The owner-scoped snapshot supplies row visibility; this connection policy supplies operation/table limits.
# Production systems need their own grants/views/row policies and execution limits.
