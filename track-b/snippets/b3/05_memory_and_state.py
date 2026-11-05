"""Retain a conversation separately from application-owned investigation state.

Try: give the second call a new SQLiteSession("other") and compare its context.
"""

import os
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
session = SQLiteSession("shipment-C1")  # Default storage is in memory.
first = Runner.run_sync(agent, "Investigate C1 and draft one sentence.",
                        session=session, max_turns=4)
state["draft"] = first.final_output
print("DRAFT:", state["draft"])

second = Runner.run_sync(
    agent, "Which shipment were we discussing? Reply with its identifier only.",
    session=session, max_turns=4,
)
print("FOLLOW-UP:", second.final_output)
print("FINDINGS:", state["findings"])
print("REVIEW:", state["review"])

# The session supplies model context. The dictionary holds application task data.
