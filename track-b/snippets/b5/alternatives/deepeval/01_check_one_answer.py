"""Counterpart to ../../01_check_one_answer.py. Prepared data; no model call.

DeepEval reports the same five requirements; the wrong amount still fails.
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


facts = {"container_id": "C2", "fee": 200, "source": "fees-v1"}
draft = {"container_id": "C2", "fee": 999, "source": "fees-v1",
         "text": "Your recorded fee is ready."}
checks = {
    "required fields": all(field in draft for field in facts),
    "fee type": type(draft.get("fee")) is int,
    "correct container": draft.get("container_id") == facts["container_id"],
    "correct amount": draft.get("fee") == facts["fee"],
    "source label": draft.get("source") == facts["source"],
}
test_cases = [LLMTestCase(name=name, input=name, actual_output=json.dumps(passed),
                          expected_output="true") for name, passed in checks.items()]
evaluate(test_cases, metrics=[ExactResult()],
         async_config=AsyncConfig(run_async=False),
         cache_config=CacheConfig(use_cache=False, write_cache=False),
         display_config=DisplayConfig(show_indicator=False, inspect_after_run=False))
# Field checks do not assess the meaning or clarity of draft["text"].
