"""Counterpart to ../../08_repair_and_compare.py. No model call.

DeepEval reports both versions against the same cases, including extra fee 201.
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


def review_decision(fee, repaired):
    needs_review = fee >= 200 if repaired else fee > 200
    return "review" if needs_review else "clear"


test_cases = []
for repaired in [False, True]:
    version = "candidate" if repaired else "baseline"
    for fee, expected in [(100, "clear"), (200, "review"), (201, "review")]:
        kind = "additional" if fee == 201 else "repair case"
        test_cases.append(LLMTestCase(
            name=f"{version}: {fee} ({kind})", input=f"Check fee {fee}",
            actual_output=review_decision(fee, repaired), expected_output=expected,
        ))
evaluate(test_cases, metrics=[ExactResult()],
         async_config=AsyncConfig(run_async=False),
         cache_config=CacheConfig(use_cache=False, write_cache=False),
         display_config=DisplayConfig(show_indicator=False, inspect_after_run=False))
# Repair cases: 1/2 baseline, 2/2 candidate. Additional fee 201 passes both.
