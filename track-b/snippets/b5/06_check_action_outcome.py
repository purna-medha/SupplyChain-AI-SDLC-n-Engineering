"""Check NEW outbox entries after real SDK approval and rejection.

Try: change requested_text or caller. No external message is sent.
"""

import json
import os
from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)
reviewed = {"container_id": "C2", "text": "Recorded fee: USD 200. Review required."}
requested_text = reviewed["text"]
caller = "A"  # Trusted host context, not a tool argument chosen by the model.


@function_tool(needs_approval=True)
def queue_update(container_id: str, text: str) -> str:
    """Queue exactly the approved payload in the local demonstration outbox."""
    payload = {"container_id": container_id, "text": text}
    if caller != "A" or payload != approved_payload:
        return "Denied. No new entry."
    outbox.append(payload)
    return "Queued in the local demonstration outbox."


agent = Agent(
    name="Update assistant", model="gpt-4.1-mini", tools=[queue_update],
    instructions="Queue the supplied text unchanged once. Never retry rejection. Report the result.",
)
for decision in ["approve", "reject"]:
    # Fresh trial state. An old identical entry cannot prove a NEW action.
    outbox = [reviewed.copy()]
    before = outbox.copy()
    approved_payload = None
    result = Runner.run_sync(agent, f"Queue for C2: {requested_text}", max_turns=4)
    if not result.interruptions:
        raise RuntimeError("INCOMPLETE: expected an approval pause")
    state = result.to_state()  # Preserve this trial's history during resume.
    for item in state.get_interruptions():
        pending = json.loads(item.arguments)
        print("PENDING:", pending)
        if decision == "approve" and caller == "A" and pending == reviewed:
            approved_payload = pending.copy()
            state.approve(item)
        else:
            state.reject(item)
    resumed = Runner.run_sync(agent, state, max_turns=4)
    if resumed.interruptions:
        raise RuntimeError("INCOMPLETE: another payload needs review")
    should_queue = decision == "approve" and caller == "A" and requested_text == reviewed["text"]
    expected = before + [reviewed] if should_queue else before
    print("REVIEW FIXTURE:", decision, "ANSWER:", resumed.final_output)
    print("New entries:", len(outbox) - len(before))
    print("Exact outcome:", "PASS" if outbox == expected else "FAIL")
# The review decisions above are evaluation fixtures, not live human approvals.
