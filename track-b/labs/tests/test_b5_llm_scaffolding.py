"""Checks for the supplied generated-answer evaluation runner, not learner TODOs."""

import contextlib
import importlib
import io
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from unittest.mock import patch

LAB = Path(__file__).resolve().parents[1] / "container_help_desk"
sys.path.insert(0,str(LAB))


def result(score, invalid=False):
    return SimpleNamespace(score=score, invalid_result=invalid, invalid_reason="bad parse" if invalid else None,
                           feedback="controlled evaluator result", passing=None)


class LLMEvaluationScaffoldChecks(unittest.TestCase):
    def test_normalized_relevance_is_graded_without_a_passing_field(self):
        lab=importlib.import_module("b5")
        recorded=lab.metric_record("relevance",result(1.0))
        self.assertEqual(recorded["status"],"valid")
        self.assertTrue(recorded["passed"])

    def test_missing_invalid_and_out_of_range_scores_cannot_pass(self):
        lab=importlib.import_module("b5")
        for value in [result(None),result(1.0,True),result(3.0),result(float('nan'))]:
            with self.subTest(value=value):
                recorded=lab.metric_record("relevance",value)
                self.assertEqual(recorded["status"],"invalid")
                self.assertFalse(recorded["passed"])

    def test_reference_is_not_forwarded_to_generation(self):
        lab=importlib.import_module("b5")
        case={"id":"one","question":"question","context":"approved facts","reference":"REFERENCE_ONLY_CANARY"}
        def generation(generator,instruction,question,context):
            return "leaked" if "REFERENCE_ONLY_CANARY" in question+context+instruction else "actual boundary answer"
        judges={name:name for name in lab.THRESHOLDS}
        def evaluate(evaluator,case,answer):
            return result(5.0 if evaluator=="correctness" else 1.0)
        with patch.object(lab,"generate_answer",side_effect=generation), patch.object(lab,"evaluate_answer",side_effect=evaluate):
            with contextlib.redirect_stdout(io.StringIO()):
                trial=lab.run_case(object(),judges,case,"baseline")
        self.assertEqual(trial["answer"],"actual boundary answer")
        self.assertTrue(trial["passed"])

    def test_one_judge_error_does_not_erase_other_metric_results(self):
        lab=importlib.import_module("b5")
        case={"id":"one","question":"question","context":"facts","reference":"reference"}
        judges={name:name for name in lab.THRESHOLDS}
        def evaluate(evaluator,case,answer):
            if evaluator=="grounding": raise RuntimeError("controlled evaluator failure")
            return result(5.0 if evaluator=="correctness" else 1.0)
        with patch.object(lab,"generate_answer",return_value="controlled answer"), patch.object(lab,"evaluate_answer",side_effect=evaluate):
            with contextlib.redirect_stdout(io.StringIO()):
                trial=lab.run_case(object(),judges,case,"baseline")
        self.assertFalse(trial["passed"])
        self.assertEqual(trial["metrics"]["grounding"]["status"],"error")
        self.assertIsNone(trial["metrics"]["grounding"]["score"])
        self.assertTrue(trial["metrics"]["relevance"]["passed"])

    def test_every_generation_error_remains_in_both_comparison_versions(self):
        lab=importlib.import_module("b5")
        cases=[{"id":"one","question":"q","context":"facts","reference":"r","split":"development"}]
        with patch.object(lab,"generate_answer",side_effect=RuntimeError("controlled generation failure")):
            with contextlib.redirect_stdout(io.StringIO()):
                trials=lab.compare_prompts(object(),{},cases,"candidate",2)
        self.assertEqual(len(trials),4)
        self.assertEqual([trial["version"] for trial in trials],["baseline","baseline","candidate","candidate"])
        self.assertTrue(all(not trial["passed"] and trial["generation_error"] for trial in trials))
        self.assertTrue(all(trial["answer"] is None for trial in trials))

    def test_unfinished_generation_stops_as_a_todo(self):
        lab=importlib.import_module("b5")
        case={"id":"one","question":"q","context":"facts","reference":"r"}
        with self.assertRaises(NotImplementedError):
            lab.run_case(object(),{},case,"baseline")


if __name__ == "__main__":
    unittest.main()
