"""Supplied B4 fixture/projection and SQLite policy. No model or network calls."""

import sqlite3
from sqlalchemy import create_engine, text

TRUSTED_OWNER = "A"  # Host identity fixture; not a model argument or real authentication.
AS_OF = "2026-11-06T00:00:00Z"
SOURCE = "approved-fee-snapshot/A"


def make_databases(equal_fees=False):
    """Build source records, then project A's approved rows/fields into another DB."""
    source = create_engine("sqlite://")
    snapshot = create_engine("sqlite://")
    records = [
        {"id":"C1", "owner":"A", "status":"delayed", "fee":100},
        {"id":"C2", "owner":"B", "status":"delayed", "fee":200},
        {"id":"C4", "owner":"A", "status":"delayed", "fee":100 if equal_fees else 50},
        {"id":"C5", "owner":"A", "status":"on_time", "fee":75},
    ]
    with source.begin() as connection:
        connection.exec_driver_sql("""CREATE TABLE container_fees (
            container_id TEXT PRIMARY KEY, owner TEXT, status TEXT, fee INTEGER,
            currency TEXT, as_of TEXT, private_note TEXT)""")
        connection.exec_driver_sql("""CREATE TABLE events (
            container_id TEXT REFERENCES container_fees(container_id), kind TEXT)""")
        connection.execute(text("""INSERT INTO container_fees VALUES
            (:id, :owner, :status, :fee, 'USD', :as_of, 'synthetic-internal-only')"""),
            [dict(record, as_of=AS_OF) for record in records])
        connection.exec_driver_sql("""INSERT INTO events VALUES
            ('C1','scan'), ('C1','hold'), ('C2','hold'), ('C4','hold')""")
        rows = connection.execute(text("""SELECT container_id, status, fee, currency, as_of
            FROM container_fees WHERE owner=:owner"""), {"owner":TRUSTED_OWNER}).mappings().all()
        events = connection.execute(text("""SELECT e.container_id, e.kind FROM events e
            JOIN container_fees f ON f.container_id=e.container_id WHERE f.owner=:owner"""),
            {"owner":TRUSTED_OWNER}).mappings().all()
    with snapshot.begin() as connection:
        connection.exec_driver_sql("""CREATE TABLE container_fees (
            container_id TEXT PRIMARY KEY, status TEXT, fee INTEGER, currency TEXT, as_of TEXT)""")
        connection.exec_driver_sql("""CREATE TABLE events (
            container_id TEXT REFERENCES container_fees(container_id), kind TEXT)""")
        connection.execute(text("INSERT INTO container_fees VALUES (:container_id,:status,:fee,:currency,:as_of)"),
                           [dict(row) for row in rows])
        connection.execute(text("INSERT INTO events VALUES (:container_id,:kind)"),
                           [dict(row) for row in events])
        # A non-public control table makes the policy probe a real denied read.
        connection.exec_driver_sql("CREATE TABLE private_contacts (note TEXT)")
        connection.exec_driver_sql("INSERT INTO private_contacts VALUES ('synthetic-private-control')")
    return source, snapshot


def authorise(action, table, column, database, origin):
    functions = {"sum", "count", "max", "min", "avg", "round", "coalesce", "lower", "upper"}
    allowed = (action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION)
               or action == sqlite3.SQLITE_READ and table == "container_fees"
               or action == sqlite3.SQLITE_FUNCTION and column in functions)
    return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY


def restrict_database(engine):
    """Restrict the toy SQLite connection after schema inspection/caching."""
    with engine.connect() as connection:
        raw = connection.connection.driver_connection
        raw.set_authorizer(authorise)
        raw.set_progress_handler(lambda: 1, 10000)
