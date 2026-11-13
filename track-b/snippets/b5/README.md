# B5 · Evaluate generated LLM answers

This folder contains the five examples used by the current B5 slides and the two linked tracing references. Future-delivery experiments are outside this client snapshot.

**Start with [01 · Evaluate one generated answer](#01-evaluate-one-generated-answer).** Follow one answer from generation to judgment before running a dataset.

By the end, you can evaluate actual generated text for correctness, grounding and relevance, inspect judge mistakes, and compare prompts on unchanged cases.

Complete [shared setup](../../SETUP.md) and run commands from **track-b**. All five files use `load_dotenv()` and `OPEN_AI_KEY`. They use the existing LlamaIndex packages and `gpt-4.1-mini`; each is complete and imports no teaching helper. **Every core example makes model calls.** Generator and judge are configured separately, but currently use the same model family; their errors need not be independent.

Allow about **60 minutes** for teaching and selected demonstrations, excluding setup. Dataset/comparison scripts make multiple generation and judge calls; run one implementation per teaching step.

## 01 Evaluate one generated answer

1. **Understand.** Correctness asks whether an actual answer meets the question and an independently written reference. The generator receives instruction, question and approved context. Only the evaluator receives the reference.
2. **Predict.** The context supplies C2's recorded USD 200 fee and review rule, but no release schedule. Can it establish that C2 will—or will not—be released tomorrow?
3. **Run** [01_evaluate_generated_answer.py](01_evaluate_generated_answer.py).

   ```bash
   uv run python snippets/b5/01_evaluate_generated_answer.py
   ```

4. **Observe.** Read `GENERATED ANSWER`, then the reference, score and feedback. In one actual run the answer asserted C2 would not be released tomorrow, yet the judge awarded 5/5. Absence of a schedule supports uncertainty, not a positive or negative release guarantee. A judge pass is not proof.
5. **Try.** Ask only about the fee/review requirement and update the independent reference to that narrower question. Inspect the newly generated answer and judgment; do not reuse a prepared answer as model output.

## 02 Check support from the supplied context

1. **Understand.** Grounding asks whether the answer's claims follow from its supplied evidence. It differs from reference correctness: an answer can stay within the evidence while omitting part of the question. LlamaIndex's FaithfulnessEvaluator receives the actual response and context.
2. **Predict.** Would a fluent, relevant sentence announcing a release date be supported here?
3. **Run** [02_check_grounding.py](02_check_grounding.py).

   ```bash
   uv run python snippets/b5/02_check_grounding.py
   ```

4. **Observe.** Compare the context with every factual claim before inspecting `GROUNDED` and feedback. The observed answer said the release date was unknown and received a grounding pass. This file generates a **new answer**; its score does not grade the different answer produced by 01.
5. **Try.** Change the question to ask whether release tomorrow is guaranteed. Inspect how uncertainty is expressed and how the judge grades it. Either generator or judge can make a mistake.

## 03 Check the judges against labelled examples

1. **Understand.** A judge needs its own checks. These explicitly prepared answers calibrate the correctness and grounding judges. They are not claimed generation-model outputs. Known wrong amounts, unsupported positive/negative release claims and valid paraphrases test different weaknesses. Relevance calibration is a further exercise using clearly off-topic answers.
2. **Predict.** Should “will not be released tomorrow” pass merely because no release schedule is available?
3. **Run** [03_calibrate_judges.py](03_calibrate_judges.py).

   ```bash
   uv run python snippets/b5/03_calibrate_judges.py
   ```

4. **Observe.** Compare author labels with each judge's acceptance and feedback. The five-probe run observed correctness agreement 5/5 and grounding agreement 4/5: grounding incorrectly accepted the unsupported negative release claim. The earlier generated-answer false pass also remains evidence. Neither small calibration nor one good judgment establishes accuracy.
5. **Try.** Add an answer containing one supported fee fact and one unsupported operational claim, with a label you establish first. Inspect disagreements. If you change a judge/rubric, rerun both baseline and candidate under that same revised judge.

## 04 Evaluate a small generated-answer dataset

1. **Understand.** Cases define questions, context and independent references before execution. This file generates fresh answers for four development cases: a known fee, missing record, future release and misleading waiver premise. It reports three separate model judgments.
2. **Predict.** Can an answer address the question and still repeat its unsupported premise?
3. **Run** [04_evaluate_answer_dataset.py](04_evaluate_answer_dataset.py).

   ```bash
   uv run python snippets/b5/04_evaluate_answer_dataset.py
   ```

4. **Observe.** Inspect each answer and feedback before totals. One run reported correctness 4/4, grounding 3/4 and relevance 4/4. The waiver answer was relevant but ungrounded. Its correctness judge also accepted it, illustrating why the counts must not be treated as truth. Generation/judge errors remain visible and stay in the attempted-case denominator.
5. **Try.** Add a case asking for an outstanding balance when no payment data is supplied. Write its expected response independently, then inspect actual generation and all three judgments. Keep “recorded fee” distinct from “outstanding balance”.

## 05 Compare prompts under unchanged evaluation

1. **Understand.** Compare a plain baseline with an explicit evidence-use/uncertainty instruction. Model, context, questions, references, evaluator configuration and thresholds stay fixed. Each attempt generates fresh text. A separate held-out comparison question is not used to develop the candidate prompt.
2. **Predict.** Which answers should the candidate affect? Could a longer answer introduce a new unsupported claim?
3. **Run** [05_compare_prompts.py](05_compare_prompts.py).

   ```bash
   uv run python snippets/b5/05_compare_prompts.py
   ```

4. **Observe.** The observed snippet summary was baseline development 3/4, candidate 4/4; both accepted the held-out answer, 1/1. A separate completed-lab run tied at 3/4 development for both prompts because one candidate answer lost relevance credit while its fact judges passed. These are judge acceptances, not proven quality rates. Inspect individual answers and feedback; do not adjust thresholds afterward to force an improvement.
5. **Try.** Increase `repeats` to 2. Keep every attempt and compare the same case/split counts. Do not tune the prompt using held-out feedback and then describe that same case as still unseen; reserve another case for the next comparison.

## What each score means

| Criterion | Inputs used by the judge | Scale | Declared teaching pass |
| --- | --- | --- | --- |
| Correctness | Question, generated answer, independent reference | 1–5 | At least 4 |
| Grounding/faithfulness | Generated answer and supplied context | 0 or 1 | 1 |
| Answer relevance | Question and generated answer | Normalized 0–1 | 1 |

These thresholds are explicit teaching choices. Do not average unlike scales or assume that a relevant answer is factual. In the installed LlamaIndex version, answer relevance supplies a normalized score without a `passing` verdict, so the code applies its threshold explicitly.

<details>
<summary>Execution and evidence limits</summary>

Each file is standalone and contains its own small fixture. Records and policy are synthetic. The context has C1/USD 100, C2/USD 200, review at 200 or more, an explicit missing C9 record and no waiver/payment/release information. Observation time is a fixed snapshot, not a current guarantee.

The same model family generates and judges; separate calls do not establish independent errors. Generated answers, raw scores and feedback require inspection. Unknown/invalid judgments are not successful scores. A failed generation supplies no answer to judge. Small repeated counts and classroom labels do not establish production reliability. The five files do not measure an aggregate dollar cost; missing usage stays unknown.

Fixed-context evaluation needs no vector retrieval. LlamaIndex's embedding-disabled/MockEmbedding message is an unused setup placeholder, not a substitute for real generation or judgment. No observability account, database server or hosted evaluation service is required.

</details>

## Continue

- [36-slide deck](../../slides-md/b5-safety-observability-evaluation.md), [Gamma text](../../slides-gamma/b5-safety-observability-evaluation.txt) and [teaching outline](../../B5-OUTLINE.md).
- [B5 learner lab](../../labs/container_help_desk/B5.md): case design, real generation, evaluation, calibration and prompt comparison.
- [Current verification](VERIFICATION.md): actual answers, judge disagreements and comparison records.
- [Tracing references](reference/README.md): the two SDK/LlamaIndex examples linked from the slides.

Formal assessments and new notebooks remain deferred.
