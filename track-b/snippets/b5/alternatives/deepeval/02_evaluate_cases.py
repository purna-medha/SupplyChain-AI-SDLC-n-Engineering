"""Counterpart to ../../02_evaluate_cases.py. No model call.

DeepEval runs the five cases and reports the deliberate boundary failure.
"""

import json
from deepeval import evaluate
from deepeval.evaluate import AsyncConfig, CacheConfig, DisplayConfig
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


class ExactResult(BaseMetric):
    """Deterministic equality; DeepEval handles evaluation and reporting."""
    threshold = 1
    async_mode = False

    def measure(self, test_case, *args, **kwargs):
        self.score = float(test_case.actual_output == test_case.expected_output)
        self.success = self.score == 1
        self.reason = f"Expected {test_case.expected_output}; actual {test_case.actual_output}"
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    @property
    def __name__(self):
        return "Exact result"


def get_fee_decision(caller, container_id, unavailable=False):
    record = {"C1": ("A", 100), "C2": ("A", 200)}.get(container_id)
    if record is None:
        return None, "unknown"
    owner, fee = record
    if caller != owner:
        return None, "denied"
    if unavailable:
        return None, "unavailable"
    return fee, "review" if fee > 200 else "clear"  # Deliberate defect.


cases = [
    ("below", "A", "C1", False, (100, "clear")),
    ("boundary", "A", "C2", False, (200, "review")),
    ("missing", "A", "C9", False, (None, "unknown")),
    ("denied", "B", "C2", False, (None, "denied")),
    ("dependency", "A", "C2", True, (None, "unavailable")),
]
test_cases = [
    LLMTestCase(name=name, input=f"Check {container_id} for {caller}; unavailable={unavailable}",
                actual_output=json.dumps(get_fee_decision(caller, container_id, unavailable)),
                expected_output=json.dumps(expected))
    for name, caller, container_id, unavailable, expected in cases
]
evaluate(test_cases, metrics=[ExactResult()],
         async_config=AsyncConfig(run_async=False),
         cache_config=CacheConfig(use_cache=False, write_cache=False),
         display_config=DisplayConfig(show_indicator=False, inspect_after_run=False))
