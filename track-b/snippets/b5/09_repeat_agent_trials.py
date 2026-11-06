"""Repeat real SDK trials from fresh state before and after the same rule repair.

Try: change repeats or max_turns. Errors and incomplete attempts stay visible.
"""

import os
from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, ModelSettings, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled

load_dotenv()
set_default_openai_key(os.environ["OPEN_AI_KEY"])
set_tracing_disabled(True)
repeats = 2
max_turns = 4


@function_tool
def get_review_decision(container_id: str) -> str:
    """Read the review decision for the requested synthetic record."""
    calls.append(container_id)
    fee = {"C1": 100, "C2": 200}.get(container_id)
    if fee is None:
        return "unknown"
    needs_review = fee >= 200 if repaired else fee > 200
    return "review" if needs_review else "clear"


for repaired in [False, True]:
    print("\nCANDIDATE" if repaired else "\nBASELINE")
    for container_id, expected in [("C1", "clear"), ("C2", "review"), ("C9", "unknown")]:
        successes = 0
        for attempt in range(repeats):
            calls = []  # Fresh application state and agent conversation per trial.
            agent = Agent(
                name="Fee assistant", model="gpt-4.1-mini", tools=[get_review_decision],
                model_settings=ModelSettings(temperature=0),
                instructions=("Call get_review_decision for the requested ID. Your final answer "
                              "must be exactly its one-word label: clear, review, or unknown. "
                              "Add no other words or punctuation."),
            )
            try:
                result = Runner.run_sync(agent, f"Check {container_id}.", max_turns=max_turns)
                actual = result.final_output.strip()
            except MaxTurnsExceeded:
                actual = "INCOMPLETE: turn limit"
            except Exception as error:
                actual = f"ERROR: {type(error).__name__}: {error}"
            passed = actual == expected and bool(calls) and all(cid == container_id for cid in calls)
            successes += passed
            print(container_id, "trial:", attempt + 1, "expected:", expected,
                  "actual:", actual, "PASS" if passed else "FAIL")
        print(container_id, "success frequency:", successes, "/", repeats)
# The task requires one decision label; this score does not evaluate free-text explanations.
