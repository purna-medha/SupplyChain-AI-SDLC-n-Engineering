"""Pause a real tool call, review its exact payload and resume the same run.

Type approve or reject when prompted. The only action is a local demo outbox.
"""

import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)
outbox = []


@function_tool(needs_approval=True)
def queue_customer_update(container_id: str, text: str) -> str:
    """Place the reviewed message in a local demonstration outbox."""
    print("ACTION queue_customer_update:", container_id)
    outbox.append({"container_id": container_id, "text": text})
    return "Recorded in the local demo outbox."


agent = Agent(
    name="Update coordinator", model="gpt-4.1-mini",
    instructions=("Submit the supplied update unchanged through queue_customer_update. "
                  "Never retry a rejected action. Report the actual result."),
    tools=[queue_customer_update],
)
draft = "C1 is delayed by a customs hold. The next departure is scheduled for 5 November."
result = Runner.run_sync(agent, f"Queue this update for C1: {draft}", max_turns=4)
if not result.interruptions:
    raise RuntimeError("Expected an approval interruption before the action")

print("OUTBOX BEFORE:", len(outbox))
for item in result.interruptions:
    print("PENDING:", item.name, item.arguments)

decision = input("Review this payload: approve or reject? ").strip().lower()
if decision not in {"approve", "reject"}:
    raise ValueError("Expected approve or reject; no action was authorized")
state = result.to_state()
for item in state.get_interruptions():
    if decision == "approve":
        state.approve(item)
    else:
        state.reject(item)
resumed = Runner.run_sync(agent, state, max_turns=4)
if resumed.interruptions:
    raise RuntimeError("Another action needs a new review; stopped without approving it")
print("FINAL:", resumed.final_output)
print("OUTBOX AFTER:", len(outbox))
print("OUTBOX:", outbox)

# The terminal decision is a classroom review input, not enterprise authentication.
# Saving and restoring a paused run is a separate follow-on example.
