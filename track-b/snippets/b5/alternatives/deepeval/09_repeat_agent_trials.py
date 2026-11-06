"""Counterpart to ../../09_repeat_agent_trials.py. Fresh real SDK trials.

DeepEval owns scoring/reporting; SDK execution and clean state remain explicit.
"""

import json
import os
from dotenv import load_dotenv
from agents import Agent, MaxTurnsExceeded, ModelSettings, Runner, function_tool
from agents import set_default_openai_key, set_tracing_disabled
from deepeval import evaluate
from deepeval.evaluate import AsyncConfig, CacheConfig, DisplayConfig
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


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


class DecisionAndCalls(BaseMetric):
    threshold = 1
    async_mode = False

    def measure(self, test_case, *args, **kwargs):
        outcome = json.loads(test_case.actual_output)
        requested = test_case.metadata["container_id"]
        passed = (outcome["status"] == "complete"
                  and outcome["decision"] == test_case.expected_output
                  and bool(outcome["calls"])
                  and all(cid == requested for cid in outcome["calls"]))
        self.score = float(passed)
        self.success = passed
        self.reason = json.dumps(outcome)
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    @property
    def __name__(self):
        return "Decision and actual tool IDs"


if __name__ == "__main__":
    repeats = 2
    max_turns = 4
    test_cases = []
    for repaired in [False, True]:
        version = "candidate" if repaired else "baseline"
        for container_id, expected in [("C1", "clear"), ("C2", "review"), ("C9", "unknown")]:
            for attempt in range(repeats):
                outcome = run_trial(container_id, repaired, max_turns)
                test_cases.append(LLMTestCase(
                    name=f"{version}:{container_id}:{attempt + 1}", input=f"Check {container_id}.",
                    actual_output=json.dumps(outcome), expected_output=expected,
                    metadata={"container_id": container_id},
                ))
    results = evaluate(test_cases, metrics=[DecisionAndCalls()],
                       async_config=AsyncConfig(run_async=False),
                       cache_config=CacheConfig(use_cache=False, write_cache=False),
                       display_config=DisplayConfig(show_indicator=False, inspect_after_run=False))
    for version in ["baseline", "candidate"]:
        for container_id in ["C1", "C2", "C9"]:
            trials = [r for r in results.test_results if r.name.startswith(f"{version}:{container_id}:")]
            print(version, container_id, "success frequency:", sum(r.success for r in trials), "/", len(trials))
# Errors/incomplete attempts are ordinary failed cases in the fixed denominator.
