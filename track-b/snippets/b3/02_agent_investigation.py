"""Let one agent investigate using three synthetic operational capabilities.

Try: change container_id to C2 or C9, or max_turns to 1.
"""

import os
from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)


@function_tool
def get_shipment_status(container_id: str) -> dict:
    """Read the recorded status; stop investigating an unknown identifier."""
    print("TOOL get_shipment_status:", container_id)
    records = {"C1": "delayed", "C2": "on_time"}
    return {"container_id": container_id,
            "status": records.get(container_id, "unknown")}


@function_tool
def get_tracking_events(container_id: str) -> dict:
    """Read events explaining a known shipment's current status."""
    print("TOOL get_tracking_events:", container_id)
    records = {"C1": ["Customs hold", "Planned departure missed"],
               "C2": ["Departed as planned"]}
    return {"events": records.get(container_id), "source": "classroom tracking"}


@function_tool
def get_next_departure(container_id: str) -> dict:
    """Read the scheduled onward departure; a schedule is not confirmed movement."""
    print("TOOL get_next_departure:", container_id)
    records = {"C1": "2026-11-05T18:00:00Z"}
    return {"scheduled_departure": records.get(container_id)}


agent = Agent(
    name="Shipment investigator",
    model="gpt-4.1-mini",
    instructions=(
        "Start with recorded status; choose further lookups from observations. "
        "Investigate only observed delays. Ask for a corrected ID if unknown. "
        "Use tool facts only and describe scheduled movement as scheduled. "
        "Return the requested draft or status, without inventing actions or commitments."
    ),
    tools=[get_shipment_status, get_tracking_events, get_next_departure],
)
container_id = "C1"
max_turns = 6
try:
    result = Runner.run_sync(
        agent, f"Check {container_id}. If delayed, explain its cause and next scheduled "
               "departure in a concise customer update for review.",
        max_turns=max_turns,
    )
    print("FINAL:", result.final_output)
except MaxTurnsExceeded:
    print("STOP: turn budget exhausted; investigation is incomplete.")

# A turn bound is not an aggregate tool-call or token budget.
