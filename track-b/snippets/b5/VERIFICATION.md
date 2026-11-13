# B5 generated-answer evaluation · verified 6 November 2026

This record covers the [five current examples](README.md), the aligned 36-slide [Markdown](../../slides-md/b5-safety-observability-evaluation.md)/[Gamma](../../slides-gamma/b5-safety-observability-evaluation.txt) deck and [learner lab](../../labs/container_help_desk/B5.md). [Captured evidence](verification-results.json) retains actual answers, raw feedback, source/configuration information and comparison outcomes. The [former nine-example record](reference/application_checks/VERIFICATION.md) is historical application-testing evidence.

## Actual generation and evaluation

All five core scripts ran with actual `gpt-4.1-mini` generation and/or judge calls. No prepared successful reply replaced a generation call. Files 01/02 generate one answer before judging it. 03 uses explicitly prepared calibration inputs with independent author labels and real judge calls. 04 generates four development answers and evaluates each under three criteria. 05 generates fresh baseline/candidate answers for the same four development cases and one separately labelled held-out question.

Generator/judge clients are separate but use the same model family; errors may be correlated. The generation prompt contains instruction, question and approved context, **not the reference or acceptance label**. References go only to evaluators. The thresholds are explicit teaching choices: correctness >=4 on 1–5, binary grounding=1, normalized relevance=1. Relevance's `passing` field is unset in the installed version, so the score is explicitly thresholded.

## Observed answers and judge failures

| Example | Actual observation |
| --- | --- |
| 01 · Correctness | Generated an unsupported negative release claim and an unsupported release gate; the judge incorrectly awarded 5/5 |
| 02 · Grounding | A different generated answer retained uncertainty about release; its grounding judge passed it |
| 03 · Calibration | Final five-probe run: correctness agreement 5/5, grounding 4/5; grounding falsely accepted the unsupported denial of release tomorrow |
| 04 · Dataset | Judge acceptances: correctness 4/4, grounding 3/4, relevance 4/4 |
| 05 · Prompt comparison | All-three acceptance: development baseline 3/4, candidate 4/4; held-out 1/1 under both |

01's response included: “the fee will not be released tomorrow. A review must be completed before any release can occur.” The context supplies neither assertion. The judge's feedback nevertheless called it consistent with the reference's uncertainty. This is retained as a false positive, not reported as successful answer quality.

02 is a separate generation and must not be interpreted as a grounding check of 01's answer. In 03, the shorter prepared unsupported-denial answer was rejected by correctness but accepted by grounding. A good calibration judgment on one wording does not erase the observed false pass on another wording.

04's waiver answer accepted an unsupported user premise. Grounding rejected it while correctness still accepted it at 4. The future-release answer also inferred likelihood beyond the supplied schedule information while both judges accepted it. These cases show why aggregate acceptance is not ground truth.

05 retained the same cases, model/settings, context, references, judge configuration and thresholds across prompts. The candidate corrected the waiver premise in that run. One held-out question and one attempt per case do not establish generalization/reliability. No held-out improvement is shown because both versions scored 1/1 there.

## Current score/error controls

After the first full live run, five-probe calibration was run separately after adding the unsupported-denial probe. Case formatting was expanded for readability. Review then exposed parser-scale validation gaps and one comparison error-handling gap. The final controls reject missing, invalid, nonfinite/out-of-range scores rather than counting them as passes. 05 now handles each judge error independently so remaining judgments still run. Repeats must be positive.

Five targeted controlled-boundary regressions were first observed failing and then passing. They exercise correctness 6/inf, relevance 1.5, invalid agreement, retained denominators and continued judgments after one judge error. These tests replace only model/evaluator IO and make **no model calls**. They validate reporting behavior, not judge semantics or provider reliability. Current full lab/scaffold/control suite: **24 tests passed**. The earlier full model transcripts and separate five-probe run retain their execution-version hashes where captured; final source hashes are separate. No prompt/model/threshold was changed by these control fixes.

## Current learner lab

Temporary completed copies exercised seven checkpoints/variations: offline cases, real generation, one-answer evaluation, two-judge calibration, development dataset, full prompt comparison and a two-attempt selected-case comparison. The delivered five TODO functions remain unimplemented. These actual runs are retained in [lab verification](../../labs/VERIFICATION.md).

The completed lab's separate comparison **tied** at 3/4 development for both prompts, with held-out 1/1 for both. Its candidate waiver answer passed correctness/grounding but relevance scored 0.5, criticising its refusal to accept the user's unverified premise. That judge sees question/answer, not source context. The threshold stayed at 1; the tie and feedback were preserved. Selected future-case repetition retained all four attempts. These are separate runs from snippet 05 and are not pooled with its counts.

## Environment, teaching and limits

Existing Python 3.12.2 shared environment and locked packages were reused: llama-index-core 0.14.25, llama-index-llms-openai 0.8.3 and openai 2.54.0. No dependency/model upgrade was needed. `load_dotenv()` and `OPEN_AI_KEY` supplied credentials; no key was printed or copied into code/evidence. Fixed-context judging requires no vector retrieval; the embedding-disabled/MockEmbedding setup message is not a fake answer or substitute generation.

A fresh read-only review checked code, fairness, source/evidence agreement and teaching progression. Its material score/error findings were fixed with failing-then-passing controlled tests. All 36 slides rendered and were visually inspected through contact sheets, with the final comparison clarification inspected separately. Gamma retains the same visible slide bodies, tables and fenced blocks while dropping Marp metadata, notes and local navigation.

Generated text, score and feedback all need inspection. Correctness/grounding calibration does not independently validate relevance. Missing usage/cost stays unknown; elapsed evaluation time is not generation-only latency. The examples are small classroom evidence, not statistical reliability estimates, production permissions or delivery guarantees. Earlier Promptfoo/DeepEval wrappers remain counterparts to the former rule/agent sequence, not equivalents of this five-example core. No optional framework was installed or rerun.

Formal assessments, new notebooks, staging and commits remain deferred.
