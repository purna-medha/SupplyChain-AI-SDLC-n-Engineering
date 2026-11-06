"""Review an exact payload, then create a real SQLite draft. No external message.

Try: approve, reject, or request C2. Example 07 demonstrates a retry in one process.
"""

import json
import os
import sqlite3
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)
connection = sqlite3.connect(":memory:")
connection.executescript("""
CREATE TABLE containers (id TEXT PRIMARY KEY, owner TEXT);
INSERT INTO containers VALUES ('C1', 'A'), ('C2', 'B');
CREATE TABLE drafts (request_id TEXT PRIMARY KEY NOT NULL, container_id TEXT, reason TEXT);
""")
trusted_owner = "A"
request_id = "request-001"  # Host-owned operation identity, stable for a retry.
approved_payload = None


@function_tool(needs_approval=True)
async def create_draft(container_id: str, reason: str) -> dict:
    """Create only the approved, permitted draft. Reuse the request identity on retries."""
    payload = {"container_id": container_id, "reason": reason}
    owner = connection.execute("SELECT owner FROM containers WHERE id = ?", (container_id,)).fetchone()
    if owner != (trusted_owner,) or payload != approved_payload:
        return {"status": "denied"}
    existing = connection.execute("SELECT container_id, reason FROM drafts WHERE request_id = ?",
                                  (request_id,)).fetchone()
    if existing and existing != (container_id, reason):
        return {"status": "conflict"}
    connection.execute("INSERT INTO drafts VALUES (?, ?, ?) ON CONFLICT(request_id) DO NOTHING",
                       (request_id, container_id, reason))
    connection.commit()
    return {"status": "reused" if existing else "created", "request_id": request_id}


agent = Agent(
    name="Draft assistant", model="gpt-4.1-mini", tools=[create_draft],
    instructions="Create the supplied draft unchanged once. Never retry rejection. Report the result.",
)
reviewed = {"container_id": "C1", "reason": "Customs hold"}
result = Runner.run_sync(agent, f"Create this draft: {json.dumps(reviewed)}", max_turns=4)
if not result.interruptions:
    raise RuntimeError("INCOMPLETE: expected review before a write")
state = result.to_state()
for item in state.get_interruptions():
    pending = json.loads(item.arguments)
    print("REVIEW:", pending)
    decision = input("approve or reject? ").strip().lower()
    if decision == "approve" and pending == reviewed:
        approved_payload = pending.copy()
        state.approve(item)
    else:
        state.reject(item)
resumed = Runner.run_sync(agent, state, max_turns=4)
if resumed.interruptions:
    raise RuntimeError("INCOMPLETE: another payload needs review")
print("ANSWER:", resumed.final_output)
print("ACTUAL DRAFT ROWS:", connection.execute("SELECT * FROM drafts").fetchall())
connection.close()
