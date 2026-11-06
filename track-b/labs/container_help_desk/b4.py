"""B4 starter: inspect, scope, query and verify recorded fee data.

Learners edit five TODO functions. Fixtures and checkpoint runners are supplied.
Every process starts with fresh in-memory databases; B1–B3 TODOs are not imported.
"""

import argparse
from datetime import datetime
import json
import os

from agents import Agent, MaxTurnsExceeded, Runner, function_tool
from llama_index.core import SQLDatabase, Settings
from llama_index.core.query_engine import NLSQLTableQueryEngine
from llama_index.llms.openai import OpenAI
from pydantic import BaseModel, ConfigDict, StrictInt
from sqlalchemy import inspect, text
from sqlalchemy.exc import DatabaseError

from b4_data import AS_OF, SOURCE, TRUSTED_OWNER, make_databases, restrict_database
from support import configure_sdk, run_cli

QUESTION = "What is the total recorded USD fee for delayed containers?"
CONTEXT = "Caller A's approved snapshot. One recorded USD fee per container, not an outstanding balance."


def inspect_schema(engine) -> dict:
    """B4.1: return each table's columns, primary key and declared foreign keys."""
    # TODO: use inspect(engine) and get_table_names/get_columns/get_pk_constraint/get_foreign_keys.
    # Return {table: {"columns": [column names], "primary_key": [column names],
    #                 "foreign_keys": inspector.get_foreign_keys(table)}}.
    raise NotImplementedError("TODO B4.1: implement inspect_schema")


def read_fee(engine, container_id: str, trusted_owner: str) -> dict | None:
    """B4.2: bound ID AND owner; select only container_id, fee, currency and as_of."""
    # TODO: connection.execute(text(fixed SQL), {"id":..., "owner":...}).mappings().first().
    # Return dict(row) or None. Do not interpolate SQL or return owner/private_note.
    raise NotImplementedError("TODO B4.2: implement read_fee")


def make_query_engine(database):
    """B4.3: configure LlamaIndex over the supplied approved table."""
    # TODO: OpenAI(model="gpt-4.1-mini", temperature=0, api_key=os.environ["OPEN_AI_KEY"]).
    # Return NLSQLTableQueryEngine(sql_database=database, tables=["container_fees"],
    #     llm=..., synthesize_response=False, context_str_prefix=CONTEXT).
    raise NotImplementedError("TODO B4.3: implement make_query_engine")


def event_fee_total(engine) -> int:
    """B4.4: sum one fee per delayed USD container with at least one event."""
    # TODO: use EXISTS rather than a multiplying event join or DISTINCT amounts.
    # Execute your fixed SQL and return its scalar result. Expect 150, or 200 with equal fees.
    raise NotImplementedError("TODO B4.4: implement event_fee_total")


def make_agent(query_tool) -> Agent:
    """B4.5: give a familiar SDK agent the supplied database-query tool."""
    # TODO: Agent(model="gpt-4.1-mini", tools=[query_tool], name=...).
    # Require database evidence, exact source/as_of, units, and honest empty/failed/truncated results.
    # A failed query must not be retried or turned into a zero amount.
    raise NotImplementedError("TODO B4.5: implement make_agent")


# Supplied runners: read these to locate actual execution and its boundaries.
class FeeRecord(BaseModel):
    model_config = ConfigDict(extra="forbid")
    container_id: str
    fee: StrictInt
    currency: str
    as_of: datetime


def unpack_response(response):
    metadata = response.metadata
    print("SQL:", metadata.get("sql_query"))
    if "result" not in metadata:
        raise RuntimeError("Query rejected or failed; no successful database result.")
    rows = [list(row) for row in metadata["result"]]
    print("ROWS:", rows)
    return {"status":"ok", "columns":list(metadata["col_keys"]), "rows":rows[:5],
            "truncated":len(rows)>5, "source":SOURCE, "as_of":AS_OF, "currency":"USD"}


def query_capability(snapshot):
    database = SQLDatabase(snapshot, include_tables=["container_fees"], sample_rows_in_table_info=0)
    database.get_single_table_info("container_fees")  # Cache schema before authorizer blocks reflection.
    restrict_database(snapshot)
    Settings.embed_model = None  # Fixed-table SQL needs no vector retrieval.
    return make_query_engine(database)


def show_boundaries(snapshot, row_cap):
    restrict_database(snapshot)
    with snapshot.connect() as connection:
        for sql in ["SELECT * FROM container_fees ORDER BY container_id",
                    "SELECT * FROM private_contacts", "DELETE FROM container_fees"]:
            print("SQL:", sql)
            try:
                rows = connection.execute(text(sql)).fetchmany(row_cap + 1)
                print("VISIBLE:", rows[:row_cap], "TRUNCATED:", len(rows)>row_cap)
            except DatabaseError as error:
                print("DATABASE REJECTED/FAILED:", type(error.orig).__name__)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("checkpoint", nargs="?", choices=["schema","read","query","grain","boundaries","agent"])
    parser.add_argument("--container", default="C1")
    parser.add_argument("--question", default=QUESTION)
    parser.add_argument("--expected-json", default="[[150]]", help="Independent raw-row expectation for query")
    parser.add_argument("--equal-fees", action="store_true")
    parser.add_argument("--row-cap", type=int, default=2)
    parser.add_argument("--max-turns", type=int, default=4)
    args = parser.parse_args()
    if args.checkpoint is None:
        parser.print_help()
        return
    if args.row_cap < 1 or args.max_turns < 1:
        raise ValueError("Row cap and turn limit must be positive.")
    source, snapshot = make_databases(args.equal_fees)
    try:
        if args.checkpoint == "schema":
            print(json.dumps(inspect_schema(source), indent=2))
        elif args.checkpoint == "read":
            row = read_fee(source, args.container, TRUSTED_OWNER)
            print("RESULT:", "unavailable" if row is None else FeeRecord.model_validate(row).model_dump(mode="json"))
        elif args.checkpoint == "grain":
            with snapshot.connect() as connection:
                wrong = connection.execute(text("""SELECT SUM(f.fee) FROM container_fees f
                    JOIN events e ON e.container_id=f.container_id
                    WHERE f.status='delayed' AND f.currency='USD'""")).scalar_one()
            expected = 200 if args.equal_fees else 150  # Independent fixture arithmetic.
            print("WRONG JOIN:", wrong, "INDEPENDENT EXPECTATION:", expected)
            actual = event_fee_total(snapshot)
            print("YOUR TOTAL:", actual, "PASS" if actual==expected else "FAIL")
        elif args.checkpoint == "boundaries":
            show_boundaries(snapshot, args.row_cap)
        else:
            query_engine = query_capability(snapshot)
            if args.checkpoint == "query":
                result = unpack_response(query_engine.query(args.question))
                expected = json.loads(args.expected_json)
                print("INDEPENDENT EXPECTATION:", expected)
                print("CHECK:", "PASS" if not result["truncated"] and result["rows"]==expected else "FAIL")
            else:
                @function_tool(failure_error_function=None)
                async def query_fees(question: str) -> dict:
                    """Query caller A's approved recorded USD fee snapshot. Empty is not zero."""
                    print("TOOL QUESTION:", question)
                    response = await query_engine.aquery(question)
                    try:
                        return unpack_response(response)
                    except RuntimeError:
                        return {"status":"query_failed", "source":SOURCE, "as_of":AS_OF}

                agent = make_agent(query_fees)
                configure_sdk()
                try:
                    result = Runner.run_sync(agent, args.question+" Cite source and exact observation time.",
                                             max_turns=args.max_turns)
                except MaxTurnsExceeded:
                    raise RuntimeError("INCOMPLETE: agent turn limit reached.")
                print("ANSWER:", result.final_output)
    finally:
        source.dispose()
        snapshot.dispose()


if __name__ == "__main__":
    run_cli(main)
