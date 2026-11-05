"""A coordinator calls two specialists while retaining the final answer.

Try: ask only for operational facts and inspect which specialist is called.
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)


@function_tool
def read_operational_facts(container_id: str) -> dict:
    """Read synthetic status, events and scheduled onward movement."""
    print("OPERATIONS TOOL:", container_id)
    records = {"C1": {"status": "delayed", "cause": "customs hold",
                      "next_departure": "2026-11-05T18:00:00Z"}}
    return records.get(container_id, {"error": "unknown shipment"})


@function_tool
def calculate_charge_exposure(container_id: str) -> dict:
    """Calculate illustrative exposure using a synthetic two-day record."""
    print("CHARGES TOOL:", container_id)
    if container_id != "C1":
        return {"error": "unknown shipment"}
    days, free_days, usd_per_day = 2, 1, 100
    return {"usd": max(days - free_days, 0) * usd_per_day,
            "policy": "synthetic teaching rule"}


operations = Agent(
    name="Operations specialist", model="gpt-4.1-mini",
    instructions="Use your tool. Return operational facts and missing information.",
    tools=[read_operational_facts],
)
charges = Agent(
    name="Charges specialist", model="gpt-4.1-mini",
    instructions="Use your calculator. Report illustrative USD exposure and its limits.",
    tools=[calculate_charge_exposure],
)
coordinator = Agent(
    name="Coordinator", model="gpt-4.1-mini",
    instructions=("Obtain operations and charges evidence from the relevant specialists "
                  "before preparing a concise update. Preserve missing facts and "
                  "label synthetic calculations. You own the final answer."),
    tools=[
        operations.as_tool("investigate_operations", "Obtain shipment operational evidence.",
                           max_turns=4),
        charges.as_tool("assess_charges", "Assess illustrative shipment charge exposure.",
                        max_turns=4),
    ],
)
result = Runner.run_sync(
    coordinator, "Investigate C1's delay and charge exposure. Draft an update for review.",
    max_turns=6,
)
print("FINAL OWNER:", result.last_agent.name)
print("FINAL:", result.final_output)

# Each nested specialist has its own turn bound; the outer limit is not global.
