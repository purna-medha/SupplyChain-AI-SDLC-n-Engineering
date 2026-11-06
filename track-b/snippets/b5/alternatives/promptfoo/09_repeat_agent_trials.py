"""One fresh SDK trial per provider call. Promptfoo supplies repetition/scoring.

Use --repeat 2 --no-cache. Errors are recorded outputs, never omitted trials.
"""

import json
import os
from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, ModelSettings, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled


def run_trial(container_id, repaired, max_turns=4):
    load_dotenv()
    set_default_openai_key(os.environ["OPEN_AI_KEY"])
    set_tracing_disabled(True)
    calls = []  # Local to this invocation, including failed invocations.

    @function_tool
    def get_review_decision(container_id: str) -> str:
        """Read the review decision for the requested synthetic record."""
        calls.append(container_id)
        fee = {"C1": 100, "C2": 200}.get(container_id)
        if fee is None:
            return "unknown"
        needs_review = fee >= 200 if repaired else fee > 200
        return "review" if needs_review else "clear"

    agent = Agent(
        name="Fee assistant", model="gpt-4.1-mini", tools=[get_review_decision],
        model_settings=ModelSettings(temperature=0),
        instructions=("Call get_review_decision for the requested ID. Your final answer "
                      "must be exactly its one-word label: clear, review, or unknown. "
                      "Add no other words or punctuation."),
    )
    try:
        result = Runner.run_sync(agent, f"Check {container_id}.", max_turns=max_turns)
        return {"status": "complete", "decision": result.final_output.strip(), "calls": calls}
    except MaxTurnsExceeded:
        return {"status": "incomplete", "decision": "INCOMPLETE: turn limit", "calls": calls}
    except Exception as error:
        return {"status": "error", "decision": f"ERROR: {type(error).__name__}: {error}",
                "calls": calls}


def call_api(prompt, options, context):
    config = options["config"]
    outcome = run_trial(context["vars"]["container_id"], config["repaired"],
                        max_turns=config.get("max_turns", 4))
    return {"output": json.dumps(outcome)}


def get_assert(output, context):
    outcome = json.loads(output)
    requested = context["vars"]["container_id"]
    passed = (outcome["status"] == "complete"
              and outcome["decision"] == context["vars"]["expected"]
              and bool(outcome["calls"]) and all(cid == requested for cid in outcome["calls"]))
    return {"pass": passed, "score": int(passed), "reason": json.dumps(outcome)}
