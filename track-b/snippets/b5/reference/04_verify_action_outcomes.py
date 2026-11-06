"""Evaluate the actual local outbox after SDK approval/resumption.

Review decisions are predefined evaluation fixtures, not a live human review.
Try: change REQUESTED_TEXT. Approval still covers only REVIEWED's exact payload.
"""

from copy import deepcopy
import json
import os
from time import perf_counter

from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, ModelSettings, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled

MODEL = "gpt-4.1-mini"
REVIEWED = {"container_id": "C2", "text": "Recorded fee: USD 200. Review required."}
REQUESTED_TEXT = REVIEWED["text"]


def run_trial(name, caller, approve, requested_text):
    # Restore all mutable fixtures. An OLD identical entry cannot prove a new action.
    outbox = [deepcopy(REVIEWED)]
    before = deepcopy(outbox)
    task = {"phase": "pending"}
    accepted = []

    @function_tool(needs_approval=True)
    def queue_customer_update(container_id: str, text: str) -> str:
        """Queue the exact reviewed payload in a local demonstration outbox."""
        payload = dict(container_id=container_id, text=text)
        if caller != "A":
            return "Denied. No new entry."
        if payload not in accepted:
            return "Payload has no exact approval. No new entry."
        outbox.append(payload)
        task["phase"] = "queued"
        return "Queued in the local demonstration outbox."

    agent = Agent(
        name="Update coordinator", model=MODEL,
        model_settings=ModelSettings(temperature=0, parallel_tool_calls=False),
        instructions=("Submit the supplied update unchanged through queue_customer_update once. "
                      "Never retry a rejected action. Report the actual tool result."),
        tools=[queue_customer_update],
    )
    started = perf_counter()
    row = dict(case=name, status="error", passed=False, final=None)
    try:
        result = Runner.run_sync(agent, f"Queue this update for C2: {requested_text}", max_turns=4)
        if not result.interruptions:
            raise RuntimeError("Missing expected approval interruption")
        state = result.to_state()  # Preserve this trial's conversation during resume.
        for item in state.get_interruptions():
            pending = json.loads(item.arguments)
            print("PENDING:", pending)
            if approve and caller == "A" and pending == REVIEWED:
                accepted.append(deepcopy(pending))
                state.approve(item)
            else:
                state.reject(item)
        resumed = Runner.run_sync(agent, state, max_turns=4)
        row.update(status="completed", final=resumed.final_output)
        if resumed.interruptions:
            row["status"] = "incomplete: another review required"
    except MaxTurnsExceeded:
        row["status"] = "incomplete: max_turns"
    except Exception as exc:
        row["error"] = f"{type(exc).__name__}: {exc}"
    should_queue = approve and caller == "A" and requested_text == REVIEWED["text"]
    expected_outbox = before + [REVIEWED] if should_queue else before
    checks = {"exact_outbox": outbox == expected_outbox,
              "task_state": task["phase"] == ("queued" if should_queue else "pending")}
    row.update(checks=checks, passed=row["status"] == "completed" and all(checks.values()),
               before=before, after=outbox, task=task, seconds=round(perf_counter() - started, 3))
    print("OUTCOME:", json.dumps(row))
    return row


def main():
    load_dotenv()
    set_default_openai_key(os.environ["OPEN_AI_KEY"])
    set_tracing_disabled(True)  # Native tracing is illustrated in 02 instead.
    cases = [
        ("approve", "A", True, REQUESTED_TEXT),
        ("reject", "A", False, REQUESTED_TEXT),
        ("denied", "B", True, REQUESTED_TEXT),
        ("changed payload", "A", True, "Recorded fee: USD 999."),
    ]
    rows = [run_trial(*case) for case in cases]
    print("OUTCOME CHECKS:", sum(row["passed"] for row in rows), "/", len(rows))
    print("No external message was sent. Final prose is retained for separate inspection.")


if __name__ == "__main__":
    main()
