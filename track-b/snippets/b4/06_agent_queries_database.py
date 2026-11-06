"""Give a familiar SDK agent a LlamaIndex database-query capability.

Try: ask for unavailable C2, or lower max_turns to 1 and observe the incomplete run.
"""

import os
import sqlite3
from dotenv import load_dotenv
from sqlalchemy import create_engine
from agents import Agent, MaxTurnsExceeded, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled
from llama_index.core import SQLDatabase, Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)
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
database = SQLDatabase(engine, include_tables=["container_fees"], sample_rows_in_table_info=0)
database.get_single_table_info("container_fees")


def authorise(action, table, column, db, origin):
    allowed = (action in (sqlite3.SQLITE_SELECT, sqlite3.SQLITE_TRANSACTION)
               or action == sqlite3.SQLITE_READ and table == "container_fees"
               or action == sqlite3.SQLITE_FUNCTION and column in {"sum", "count", "max", "min", "avg", "round", "coalesce", "lower", "upper"})
    return sqlite3.SQLITE_OK if allowed else sqlite3.SQLITE_DENY


with engine.connect() as connection:
    raw = connection.connection.driver_connection
    raw.set_authorizer(authorise)
    raw.set_progress_handler(lambda: 1, 10000)
Settings.embed_model = None  # Fixed approved schema, no vector retrieval.
query_engine = NLSQLTableQueryEngine(
    sql_database=database, tables=["container_fees"], synthesize_response=False,
    llm=OpenAI(model="gpt-4.1-mini", temperature=0, api_key=os.environ["OPEN_AI_KEY"]),
    context_str_prefix="Caller A snapshot. One recorded USD fee per container, not an outstanding balance.",
)


@function_tool
async def query_fees(question: str) -> dict:
    """Query only caller A's approved recorded-fee snapshot. Empty is not a zero fee."""
    print("TOOL QUESTION:", question)
    response = await query_engine.aquery(question)
    print("SQL:", response.metadata["sql_query"])
    if "result" not in response.metadata:
        print("QUERY FAILED: no database result")
        return {"status": "query_failed"}
    rows = response.metadata["result"]
    print("ROWS:", rows)
    return {"status": "ok", "columns": response.metadata["col_keys"], "rows": rows[:5],
            "truncated": len(rows) > 5, "source": "approved-fee-snapshot/A",
            "as_of": "2026-11-06T00:00:00Z"}


agent = Agent(
    name="Fee analyst", model="gpt-4.1-mini", tools=[query_fees],
    instructions=("Use query_fees for database facts. Preserve units and exact source/as_of. "
                  "Report empty/truncated/failed results honestly. Do not retry a failed query."),
)
try:
    result = Runner.run_sync(agent, "Which delayed container has the highest recorded USD fee? Cite source/time.", max_turns=4)
    print("ANSWER:", result.final_output)
except MaxTurnsExceeded:
    print("INCOMPLETE: turn limit reached.")
    raise
engine.dispose()
