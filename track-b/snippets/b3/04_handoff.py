"""Transfer the conversation to the specialist who should answer it.

Try: change the question to C1's next departure. Inspect FINAL OWNER.
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)


@function_tool
def read_departure(container_id: str) -> dict:
    """Read a synthetic scheduled departure."""
    print("OPERATIONS TOOL:", container_id)
    if container_id != "C1":
        return {"error": "unknown shipment"}
    return {"scheduled_departure": "2026-11-05T18:00:00Z"}


@function_tool
def read_charge_exposure(container_id: str) -> dict:
    """Read an illustrative calculation, not a real invoice."""
    print("CHARGES TOOL:", container_id)
    if container_id != "C1":
        return {"error": "unknown shipment"}
    return {"usd": 100, "policy": "synthetic teaching rule"}


operations = Agent(
    name="Operations specialist", model="gpt-4.1-mini",
    handoff_description="Answers questions about shipment movements and departures.",
    instructions="Use your tool and answer the user with the observed facts.",
    tools=[read_departure],
)
charges = Agent(
    name="Charges specialist", model="gpt-4.1-mini",
    handoff_description="Answers questions about illustrative shipment charges.",
    instructions="Use your tool; answer in USD and label the calculation illustrative.",
    tools=[read_charge_exposure],
)
triage = Agent(
    name="Triage", model="gpt-4.1-mini",
    instructions="Hand the request to the appropriate specialist; let it answer.",
    handoffs=[operations, charges],
)
result = Runner.run_sync(triage, "What is C1's charge exposure?", max_turns=6)
print("FINAL OWNER:", result.last_agent.name)
print("FINAL:", result.final_output)
