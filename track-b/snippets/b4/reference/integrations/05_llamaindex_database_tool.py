"""Use a narrow, scoped SQLite read as a LlamaIndex tool. No HTTP server needed.

Try: request C2 or C9. The caller identity remains host-owned.
"""

import asyncio
import os
import sqlite3
from dotenv import load_dotenv
from llama_index.core.agent.workflow import FunctionAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

load_dotenv()
connection = sqlite3.connect(":memory:")
connection.row_factory = sqlite3.Row
connection.executescript("""
CREATE TABLE containers (id TEXT PRIMARY KEY, owner TEXT, fee INTEGER, note TEXT);
INSERT INTO containers VALUES ('C1', 'A', 100, 'private investigation');
INSERT INTO containers VALUES ('C2', 'B', 200, 'private contact');
""")
connection.execute("PRAGMA query_only = ON")
trusted_owner = "A"


async def read_fee(container_id: str) -> dict:
    """Read one permitted fee. Missing and inaccessible records are unavailable."""
    row = connection.execute(
        "SELECT id AS container_id, fee FROM containers WHERE id = ? AND owner = ? LIMIT 1",
        (container_id, trusted_owner),
    ).fetchone()
    result = {"status": "unavailable"} if row is None else {
        "status": "ok", **dict(row), "currency": "USD",
        "as_of": "2026-11-06T00:00:00Z", "source": "training-db"}
    print("TOOL:", container_id, "OBSERVATION:", result)
    return result


agent = FunctionAgent(
    llm=OpenAI(model="gpt-4.1-mini", api_key=os.environ["OPEN_AI_KEY"]),
    tools=[FunctionTool.from_defaults(async_fn=read_fee)], streaming=False, timeout=30,
    system_prompt=("Use read_fee. Quote currency, source and the full as_of timestamp exactly. "
                   "Stop if unavailable; invent no fee."),
)


async def main():
    result = await agent.run(user_msg="Read C1's recorded fee and its source/time.", max_iterations=4)
    print("ANSWER:", result)


asyncio.run(main())
connection.close()
# This tiny async tool runs SQLite on its owning thread; it is not a production async DB driver.
