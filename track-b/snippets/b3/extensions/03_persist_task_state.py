"""Extend 05 with file-backed conversation storage and a task-state snapshot.

Try: change the second session ID and inspect the restored task data separately.
"""

import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
from dotenv import load_dotenv
from agents import Agent, Runner, SQLiteSession, function_tool
from agents import set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)
state = {"shipment_id": "C1", "findings": [], "draft": None, "review": "pending"}


@function_tool
def get_shipment_facts(container_id: str) -> dict:
    """Read a synthetic fact and retain it in the application's task state."""
    print("TOOL get_shipment_facts:", container_id)
    if container_id != state["shipment_id"]:
        return {"error": "unknown shipment"}
    finding = {"shipment_id": "C1", "status": "delayed", "cause": "customs hold"}
    state["findings"].append(finding)
    return finding


agent = Agent(
    name="Investigator", model="gpt-4.1-mini",
    instructions=("Use the tool for shipment facts. Answer identifier-only follow-ups "
                  "from the conversation when available. Draft without claiming approval."),
    tools=[get_shipment_facts],
)
with TemporaryDirectory() as directory:
    database = Path(directory) / "conversation.db"
    session = SQLiteSession("shipment-C1", db_path=database)
    first = Runner.run_sync(agent, "Investigate C1 and draft one sentence.",
                            session=session, max_turns=4)
    state["draft"] = first.final_output
    print("DRAFT:", state["draft"])
    path = Path(directory) / "investigation.json"
    path.write_text(json.dumps(state), encoding="utf-8")

    # New objects reload the two distinct stores; the agent definition still exists.
    session = SQLiteSession("shipment-C1", db_path=database)
    state = json.loads(path.read_text(encoding="utf-8"))
    second = Runner.run_sync(
        agent, "Which shipment were we discussing? Reply with its identifier only.",
        session=session, max_turns=4,
    )
    print("FOLLOW-UP:", second.final_output)
    print("RESTORED FINDINGS:", state["findings"])
    print("RESTORED REVIEW:", state["review"])

# Saving task data is distinct from saving an interrupted SDK run.
# Temporary files are removed at the end; this is not durable production storage.
