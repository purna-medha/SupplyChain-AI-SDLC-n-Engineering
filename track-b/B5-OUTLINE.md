# B5 · Evaluating and improving generated LLM answers

Approved revision, 6 November 2026. One teaching hour plus a separate [learner lab draft](labs/container_help_desk/B5.md). The core now evaluates actual generated text; the two SDK/LlamaIndex tracing examples linked by the slides remain [supporting examples](snippets/b5/reference/README.md). Course order remains B1 → B2 → B3 → B4 → B6 → B5.

**Outcome:** define answer-quality requirements, generate actual answers, evaluate correctness/support/relevance, inspect judge failures, and compare one prompt change under unchanged evaluation.

## 1 · Generate and evaluate an actual answer · 20 minutes

Use a synthetic approved context with C1/USD 100, C2/USD 200 and review at 200 or more. C9 has no matching record. No payment, waiver or release schedule information is supplied. Its source/time is a fixed observation, not a current guarantee.

Ask about C2's recorded fee, review and release. The generator receives question/context/instruction, while only the correctness evaluator receives an independent reference. Inspect the actual text before its score. Correctness checks question/answer/reference; faithfulness checks answer/context; answer relevance checks question/answer. A relevant answer can still be false, and a grounded answer can omit requested information.

The first real run asserted a release outcome unsupported by the context while receiving a correctness 5/5. Keep this observed judge failure visible rather than treating an evaluator as ground truth. A separate grounding example generates its own answer; its score must not be attributed to the earlier answer.

## 2 · Calibrate judges and evaluate a small dataset · 20 minutes

Use explicitly prepared, independently labelled probes: correct facts, wrong amount, unsupported positive/negative release guarantees and a valid paraphrase. Do not describe these calibration inputs as application-model outputs. Compare feedback and acceptance with the labels. One observed grounding judge accepted the unsupported negative guarantee; finite calibration does not establish accuracy.

Generate fresh answers for four development cases: known fee, missing C9, unanswerable future release and a misleading waiver premise. Print each answer, separate scores and feedback. Thresholds are declared teaching choices: correctness >=4 on 1–5; faithfulness=1 on 0/1; normalized answer relevance=1. Unlike scales are not averaged. The installed AnswerRelevancyEvaluator does not set passing, so apply its threshold explicitly.

Preserve generation failures, missing/invalid scores and judge errors. Missing measurements are unknown. Attempts remain in declared denominators; distinguish measurement failure from a valid adverse judgment. Inspect false positives rather than interpreting aggregate acceptance as true quality.

## 3 · Compare prompts, then use supporting evidence · 20 minutes

Compare a baseline instruction with an evidence-use/uncertainty candidate while keeping model, questions, context, references, judges/rubrics and thresholds fixed. Generate fresh text for each version/attempt. Reserve a separate comparison question from prompt development and report development/held-out results separately. If a judge or reference changes, rerun both versions under the changed configuration.

Inspect which case changed and whether any other requirement regressed. Repeat selected cases with every error/invalid attempt retained. Ties and regressions are legitimate outcomes; do not manufacture improvement or substitute prepared answers. Once held-out feedback informs tuning, reserve a fresh case for the next comparison.

Native SDK/LlamaIndex traces can explain agent execution and source use. Exact action-state checks, deterministic tests and prior decision-label trials are outside this client snapshot. They do not replace generation-quality evaluation. Do not add a second agent architecture, retrieval pipeline or evaluation-platform setup.

## Five standalone core examples

1. `01_evaluate_generated_answer.py`: real generation plus reference-based correctness.
2. `02_check_grounding.py`: real generation plus context-support judgment.
3. `03_calibrate_judges.py`: prepared labelled probes for model judges.
4. `04_evaluate_answer_dataset.py`: actual answers across development cases, with separate judgments.
5. `05_compare_prompts.py`: fresh matched prompt comparison and held-out case.

Each file imports no teaching helper, uses the existing locked LlamaIndex environment and load_dotenv()/OPEN_AI_KEY, and separately configures generation/judging. The current generator/judge use the same model family; their errors may be correlated. No canned successful model replies, hosted observability account or database service is required.

The [36-slide Markdown deck](slides-md/b5-safety-observability-evaluation.md) and [Gamma text](slides-gamma/b5-safety-observability-evaluation.txt) follow this progression. The [lab](labs/container_help_desk/B5.md) leaves five small functions unfinished: cases, generation, evaluator configuration, evaluation and candidate instruction. Its proposed 60-minute timing awaits an instructor dry run. Formal assessments and new notebooks remain deferred.

## Sources and implementation boundaries

[OpenAI evaluation guidance](https://developers.openai.com/api/docs/guides/evaluation-best-practices) informs task-specific datasets, independent criteria, judge calibration and matched comparisons. [LlamaIndex evaluation reference](https://developers.llamaindex.ai/python/framework-api-reference/evaluation/) documents correctness/faithfulness and their distinct inputs; [answer-relevance examples](https://developers.llamaindex.ai/python/examples/evaluation/answer_and_context_relevancy/) document normalized relevance scores.

The [current verification](snippets/b5/VERIFICATION.md) retains actual answers, judge false positives, configuration and comparison results. Older rule-repair scores remain historical, not evidence for the new LLM evaluation. Earlier Promptfoo/DeepEval wrappers are in the planning folder; they remain counterparts to the former sequence, not equivalents of these five examples. Dependencies/models are unchanged; no hosted OpenAI Evals API is introduced.
