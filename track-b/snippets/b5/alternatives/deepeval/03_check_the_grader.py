"""Counterpart to ../../03_check_the_grader.py. No model call.

A passing probe includes correctly rejecting an invalid answer.
Try: make correct_fee always return True; four probes must then fail.
"""

import json
from deepeval import evaluate
from deepeval.evaluate import AsyncConfig, CacheConfig, DisplayConfig
from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase


def correct_fee(answer):
    return (answer.get("container_id") == "C2"
            and type(answer.get("fee")) is int and answer["fee"] == 200)


class GraderProbe(BaseMetric):
    threshold = 1
    async_mode = False

    def measure(self, test_case, *args, **kwargs):
        accepted = correct_fee(json.loads(test_case.actual_output))
        expected = json.loads(test_case.expected_output)
        self.score = float(accepted == expected)
        self.success = self.score == 1
        self.reason = f"Expected acceptance: {expected}; actual acceptance: {accepted}"
        return self.score

    async def a_measure(self, test_case, *args, **kwargs):
        return self.measure(test_case)

    @property
    def __name__(self):
        return "Grader probe agreement"


probes = [
    ("known correct", {"container_id": "C2", "fee": 200}, True),
    ("wrong amount", {"container_id": "C2", "fee": 999}, False),
    ("wrong container", {"container_id": "C1", "fee": 200}, False),
    ("wrong type", {"container_id": "C2", "fee": "200"}, False),
    ("missing fee", {"container_id": "C2"}, False),
]
test_cases = [LLMTestCase(name=name, input="Check the C2 fee grader",
                          actual_output=json.dumps(answer), expected_output=json.dumps(expected))
              for name, answer, expected in probes]
evaluate(test_cases, metrics=[GraderProbe()],
         async_config=AsyncConfig(run_async=False),
         cache_config=CacheConfig(use_cache=False, write_cache=False),
         display_config=DisplayConfig(show_indicator=False, inspect_after_run=False))
