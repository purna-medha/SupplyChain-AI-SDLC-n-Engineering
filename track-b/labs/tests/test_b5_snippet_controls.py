"""Controlled IO checks for B5 score validation/reporting. No real model calls."""

import contextlib
import io
import os
from pathlib import Path
import runpy
from types import SimpleNamespace
import unittest
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[2]


def run_controlled(filename, scores, failing_metric=None):
    class ModelBoundary:
        def __init__(self,**kwargs): pass
        def complete(self,prompt): return SimpleNamespace(text="Controlled generation boundary output")
    def evaluator(name):
        class JudgeBoundary:
            def __init__(self,**kwargs): pass
            def evaluate(self,**kwargs):
                if name==failing_metric: raise RuntimeError("controlled judge failure")
                return SimpleNamespace(score=scores[name],invalid_result=False,feedback="controlled evaluator boundary",
                                       passing=True,invalid_reason=None)
        return JudgeBoundary
    stream=io.StringIO()
    with patch.dict(os.environ,{"OPEN_AI_KEY":"controlled-no-network-key"}), \
         patch('llama_index.llms.openai.OpenAI',ModelBoundary), \
         patch('llama_index.core.evaluation.CorrectnessEvaluator',evaluator('correctness')), \
         patch('llama_index.core.evaluation.FaithfulnessEvaluator',evaluator('grounding')), \
         patch('llama_index.core.evaluation.AnswerRelevancyEvaluator',evaluator('relevance')), \
         contextlib.redirect_stdout(stream):
        runpy.run_path(str(ROOT/'snippets/b5'/filename),run_name='__main__')
    return stream.getvalue()


class SnippetControlChecks(unittest.TestCase):
    def test_single_answer_rejects_out_of_range_correctness(self):
        with self.assertRaises(RuntimeError):
            run_controlled('01_evaluate_generated_answer.py',{'correctness':6.0})

    def test_invalid_calibration_scores_do_not_count_as_agreement(self):
        output=run_controlled('03_calibrate_judges.py',{'correctness':float('inf'),'grounding':1.0})
        self.assertIn('correctness AGREEMENT: 0 / 5',output)

    def test_dataset_invalid_scores_remain_unsuccessful_attempts(self):
        output=run_controlled('04_evaluate_answer_dataset.py',{'correctness':6.0,'grounding':1.0,'relevance':1.5})
        self.assertIn('correctness PASSES: 0 / 4',output)
        self.assertIn('relevance PASSES: 0 / 4',output)

    def test_comparison_invalid_scores_cannot_make_a_prompt_pass(self):
        output=run_controlled('05_compare_prompts.py',{'correctness':6.0,'grounding':1.0,'relevance':1.5})
        self.assertIn('SUMMARY: baseline development 0 / 4',output)
        self.assertIn('SUMMARY: candidate held_out 0 / 1',output)

    def test_comparison_continues_other_judges_after_one_error(self):
        output=run_controlled('05_compare_prompts.py',{'correctness':5.0,'grounding':1.0,'relevance':1.0},'correctness')
        self.assertIn('grounding SCORE:',output)
        self.assertIn('relevance SCORE:',output)
        self.assertIn('SUMMARY: baseline development 0 / 4',output)


if __name__=='__main__': unittest.main()
