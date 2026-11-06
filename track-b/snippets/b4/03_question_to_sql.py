"""Ask LlamaIndex a business question; inspect actual SQL and database rows.

Try: ask for the maximum delayed fee and change the independent expectation to 100.
"""

import os
import sqlite3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from llama_index.core import SQLDatabase, Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI

load_dotenv()
engine = create_engine("sqlite://")
with engine.begin() as connection:
    connection.exec_driver_sql("""
        CREATE TABLE container_fees (container_id TEXT PRIMARY KEY,
            status TEXT, fee INTEGER, currency TEXT, as_of TEXT)
    """)
    connection.exec_driver_sql("""
        INSERT INTO container_fees VALUES
        ('C1','delayed',100,'USD','2026-11-06T00:00:00Z'),
        ('C4','delayed',50,'USD','2026-11-06T00:00:00Z'),
        ('C5','on_time',75,'USD','2026-11-06T00:00:00Z')
    """)
# This separate classroom snapshot contains only caller A's approved rows/fields.
database = SQLDatabase(engine, include_tables=["container_fees"], sample_rows_in_table_info=0)
database.get_single_table_info("container_fees")  # Inspect/cache schema before restricting execution.


def authorise(action, table, column, db, origin):
    allowed = (action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION)
               or action == sqlite3.SQLITE_READ and table == "container_fees"
               or action == sqlite3.SQLITE_FUNCTION and column in {"sum", "count", "max", "min", "avg", "round", "coalesce", "lower", "upper"})
    return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY


with engine.connect() as connection:
    raw = connection.connection.driver_connection
    raw.set_authorizer(authorise)  # Database rejects writes, ATTACH and other unapproved operations.
    raw.set_progress_handler(lambda: 1, 10000)  # Instruction budget, not a wall-clock deadline.
Settings.embed_model = None  # Fixed-table SQL uses schema text; no vector retrieval or embeddings.
query_engine = NLSQLTableQueryEngine(
    sql_database=database, tables=["container_fees"], synthesize_response=False,
    llm=OpenAI(model="gpt-4.1-mini", temperature=0, api_key=os.environ["OPEN_AI_KEY"]),
    context_str_prefix="Caller A's approved snapshot. One recorded USD fee per container, not an outstanding balance.",
)
question = "What is the total recorded USD fee for delayed containers?"
expected = [(150,)]  # From the business case, not computed by the generated query.
response = query_engine.query(question)
print("SQL:", response.metadata["sql_query"])
if "result" not in response.metadata:
    raise RuntimeError("Query rejected or failed; no database result to answer from")
print("ROWS:", response.metadata["result"])
print("INDEPENDENT EXPECTATION:", expected)
engine.dispose()
# include_tables selects schema context. The snapshot and connection policy supply the boundary.
