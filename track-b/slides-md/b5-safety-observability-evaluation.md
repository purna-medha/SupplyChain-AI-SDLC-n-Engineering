---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 27px; padding: 44px 55px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 20px; }
  table { font-size: 23px; }
---
<!-- _class: lead -->

# B5 · Evaluate and improve generated LLM answers

Actual answers, independent expectations and inspected judgments

Correctness · Grounding · Relevance · Prompt comparison

<!--
60 minutes: slides 2–15, 20 minutes; 16–25, 20 minutes; 26–36, 20 minutes. Core order: five standalone snippets 01–05. Generate actual answers, inspect judgments and judge mistakes, then compare prompts under fixed criteria. Run selected demonstrations; full comparisons make multiple generation/judge calls. All records/policies are synthetic. Actual 6 November observations: ../snippets/b5/VERIFICATION.md. B5 follows B6. Agent tracing, deterministic rules and action checks are supporting references, not the core LLM-quality task.
-->

---

# The answer we need to evaluate

> Explain C2's recorded fee, review requirement and whether it will be released tomorrow.

The application should use its approved facts and acknowledge missing information.

**Predict:** what would make an answer useful—and what claim would require more evidence?

<!--
A useful answer preserves amount/currency, applies the supplied review policy and does not invent a release schedule. User premises are not automatically verified operational facts. Begin with the language-generation requirement, not a Python rule defect or a grader library.
-->

---

# The supplied synthetic context

| Record | Recorded fee | Status |
| --- | --- | --- |
| C1 | USD 100 | on_time |
| C2 | USD 200 | delayed |
| C9 | No matching record | Unavailable |

Recorded fees of USD 200 or more require review.

No waiver, payment or release schedule is supplied.

<!--
Fixed source fees-v1, observed 2026-11-06T00:00:00Z. This independent B5 fixture is not the B4 database or the B1–B3 lab record set. The task requires claims supported by this approved context. Recorded fee does not establish outstanding balance; missing schedule establishes neither a positive nor a negative release guarantee.
-->

---

# An independent reference answer

C2's recorded fee is **USD 200**, so review is required under the supplied policy.

Its release date cannot be determined from the supplied information.

Write the expected meaning before generation. Valid paraphrases may express it differently.

<!--
This is an author-written reference, not a model reply or exact string every answer must reproduce. The reference goes only to the correctness evaluator. It is separate from the approved facts supplied to generation. Human agreement on expectations is part of evaluation design.
Source: https://developers.openai.com/api/docs/guides/evaluation-best-practices
-->

---

# Generation and evaluation have different inputs

```text
Instruction + question + approved context → Generator → Actual answer

Question + actual answer + reference      → Correctness judge
Actual answer + approved context         → Grounding judge
Question + actual answer                 → Relevance judge
```

The generator does not receive the reference answer or calibration labels.

<!--
The model producing an answer and the model judging it have separate responsibilities. Current examples configure separate clients using the same gpt-4.1-mini model family; separate calls do not establish independent errors. Do not feed the expected answer to generation and then call that a meaningful task test.
-->

---

# Generate the answer before grading it

```python
answer = generator.complete(
    f"Answer the shipping enquiry.\n"
    f"CONTEXT:\n{context}\nQUESTION: {question}"
).text
print("GENERATED ANSWER:", answer)
```

Inspect the actual text before reading any score.

[Complete generation and correctness example](../snippets/b5/01_evaluate_generated_answer.py)

<!--
Formatting-only equivalent of 01's generation call; the full file defines generator, context and question. It makes an actual model call, not an echo of a prepared answer. The independent reference is not interpolated into this request. Credentials use load_dotenv and OPEN_AI_KEY.
-->

---

# An actual answer exceeded the evidence

Excerpt from the observed generated answer:

> “the fee will not be released tomorrow. A review must be completed before any release can occur.”

The context supplies neither a release schedule nor that release gate.

**Predict:** should a correctness judge accept these claims?

<!--
Actual 01 output, 6 November 2026. Preserve the original fee wording, which also confuses a fee with container release. The model additionally referred to delayed as fee status. These are generated-answer problems, not prepared failures or a promised response on every future run. The next slides inspect the actual judge's decision.
-->

---

# Separate the quality requirements

| Criterion | Question it asks |
| --- | --- |
| Correctness | Does the answer meet the question and independent reference? |
| Grounding | Are its claims supported by the supplied context? |
| Relevance | Does it address the user's question? |

A relevant answer can contain a wrong fact. A supported answer can leave part of the request unanswered.

<!--
These criteria overlap but are not interchangeable. In this task approved evidence, not an unverified waiver premise, establishes operational facts. Human inspection still matters. We evaluate generation with fixed supplied context; no retrieval pipeline is rebuilt here.
Sources: https://developers.llamaindex.ai/python/framework-api-reference/evaluation/ and https://developers.llamaindex.ai/python/examples/evaluation/answer_and_context_relevancy/
-->

---

# Reference-based correctness judgment

LlamaIndex's `CorrectnessEvaluator` considers the question, actual response and reference.

Its score uses a **1–5** scale. The example declares **at least 4** as passing.

The score expresses the judge's assessment; it does not establish ground truth.

<!--
Threshold 4 is the library default and an explicit teaching choice. Do not average this scale with normalized relevance or binary faithfulness. CorrectnessEvaluator does not use contexts in its implementation; support has its own evaluator.
Source: https://developers.llamaindex.ai/python/framework-api-reference/evaluation/
-->

---

# Evaluate the generated text

```python
evaluator = CorrectnessEvaluator(llm=judge, score_threshold=4.0)
result = evaluator.evaluate(
    query=question, response=answer, reference=reference
)
print(result.score, result.passing)
print(result.feedback)
```

Read feedback alongside the answer and reference.

[Complete correctness example](../snippets/b5/01_evaluate_generated_answer.py)

<!--
The code follows actual generation. The complete script checks for missing/invalid judgments rather than declaring them passes. Generator and judge configuration remain visible. No hosted evaluator platform is introduced.
-->

---

# The judge also made a mistake

For the unsupported release answer, the observed result was:

```text
CORRECTNESS: 5.0
PASS: True
```

Its feedback treated the negative release prediction as consistent with uncertainty.

A high score can coexist with a factual/evidence-use failure.

<!--
Actual 01 judge output for the answer shown on slide 7. The supplied reference says the release date cannot be determined; it does not say tomorrow's release will not occur. Do not present the score as a successful answer. This false positive motivates judge calibration and separate grounding checks.
-->

---

# Missing evidence supports uncertainty

| Statement | Established by this context? |
| --- | --- |
| C2 has a recorded fee of USD 200 | Yes |
| Review is required under the supplied policy | Yes |
| A release date cannot be determined here | Yes |
| C2 will—or will not—be released tomorrow | No |

Check the meaning of claims, including their certainty.

<!--
Human interpretation of the supplied classroom facts. Delay status alone does not determine tomorrow's release. A review requirement for a fee does not supply an operational release gate. Distinguish absence of evidence from evidence of absence.
-->

---

# Grounding checks the answer against context

Supply the actual response and the evidence available to generation.

Inspect every factual claim, including extra explanations the question did not require.

An unsupported detail can make a fluent answer unsuitable.

<!--
FaithfulnessEvaluator checks support from response/context; it does not use an independent reference answer to establish completeness or answer relevance. The default judge can itself miss unsupported claims, as the later calibration shows.
Source: https://developers.llamaindex.ai/python/framework-api-reference/evaluation/
-->

---

# Evaluate context support

```python
result = FaithfulnessEvaluator(llm=judge).evaluate(
    response=answer, contexts=[context]
)
print(result.passing, result.score)
print(result.feedback)
```

This example generates a new answer before evaluating it.

[Complete grounding example](../snippets/b5/02_check_grounding.py)

<!--
02 has its own generation call and question about what is known of release. Its judgment must not be attributed to 01's different answer. Fixed-context evaluation uses no vector retrieval. The unused MockEmbedding setup message follows disabling embedding setup, not a prepared model reply.
-->

---

# A supported answer in a separate run

The observed 02 answer stated that the release date was unknown from the available information.

```text
GROUNDED: True
SCORE: 1.0
FEEDBACK: YES
```

Inspect the answer itself; the judgment does not evaluate all possible replies.

<!--
Actual 02 observation, 6 November 2026. It correctly retained uncertainty in this run. A grounding pass does not establish that every requested part was answered or that the source is current. The score is binary model judgment, not a confidence probability.
-->

---

# Judges need their own evaluation

Use prepared answers whose expected acceptance is established independently.

Include clear successes, wrong facts, unsupported claims and valid paraphrases.

Keep these calibration labels out of the evaluator request.

<!--
Prepared text is appropriate for testing a judge, while application-quality evaluation requires actual application outputs. We label that difference explicitly. Both baseline and candidate must use the same calibrated judge/rubric; if it changes, rerun both.
Source: https://developers.openai.com/api/docs/guides/evaluation-best-practices
-->

---

# Calibration probes

| Prepared answer | Expected acceptance |
| --- | --- |
| Correct fee, review and uncertainty | Accept |
| Wrong fee of USD 999 | Reject |
| Unsupported release tomorrow | Reject |
| Unsupported denial of release tomorrow | Reject |
| Same correct meaning in different wording | Accept |

**Predict:** can passing four easy probes establish judge accuracy?

<!--
Answer cue: no. These five labels are classroom author judgments, not independently validated large-scale annotations. The unsupported-denial probe was added after the real generation/judging failure, showing how observed failures grow a case set.
-->

---

# Compare actual judgments with the labels

```python
result = evaluator.evaluate(
    query=question, response=answer,
    reference=reference, contexts=[context]
)
accepted = result.score >= thresholds[name]
print("EXPECTED:", expected, "ACCEPTED:", accepted)
```

[Complete judge-calibration example](../snippets/b5/03_calibrate_judges.py)

<!--
Shortened excerpt from 03: full code handles invalid/missing results and evaluator exceptions before deciding accepted, retains every attempted probe in the denominator and prints feedback. Each evaluator uses its relevant inputs. expected is printed/compared by Python, not sent as a judge input.
-->

---

# Calibration exposed another false pass

Observed five-probe agreement:

| Judge | Agreement with author labels |
| --- | --- |
| Correctness | 5/5 |
| Grounding | 4/5 |

The grounding judge accepted the unsupported negative release claim.

<!--
Actual updated 03 run, 6 November 2026. The correctness judge rejected the shorter negative claim here, while it accepted the longer actual 01 answer. Small wording/context differences can affect judgments. The grounding feedback was YES for the unsupported denial. Preserve these inconsistencies instead of hiding them behind a single favorable score.
-->

---

# Use judgments as inspected evidence

The current generator and judges use the same model family. Their errors need not be independent.

Inspect disagreements and known false positives before trusting a larger report.

If the judge or rubric changes, rerun every compared prompt under that revised evaluation.

<!--
Do not call separate clients independent ground truth. Human checks and task-specific calibration remain needed. Clarity/formality preferences can leak into correctness feedback, as one paraphrase judgment illustrated. Judge calls consume their own resources; missing usage remains unknown.
-->

---

# A case contains more than a question

```text
Case ID
Question
Approved context
Independent reference answer
```

The generator gets question/context. The evaluator receives the actual answer and its relevant evidence/reference.

<!--
All case data is explicit and small. Write references before generation; do not use the generated answer as its own reference. Case IDs preserve which requirement failed. No general dataset framework is needed for this teaching step.
-->

---

# The development dataset

| Case | Requirement to inspect |
| --- | --- |
| Known C2 fee | Correct amount, units and review |
| Missing C9 | Unavailable information, not zero |
| Tomorrow's release | Preserve uncertainty |
| Claimed waiver | Do not adopt an unsupported premise |

**Predict:** could the waiver answer be relevant while unsupported?

<!--
Answer cue: yes. The task requires facts supported by the approved snapshot, not treating a user's operational premise as verified evidence. These four questions/references are the development cases shared by 04 and 05.
-->

---

# Generate and evaluate each actual answer

```python
answer = generator.complete(
    f"Answer the shipping enquiry.\nCONTEXT:\n{context}\nQUESTION: {question}"
).text
result = evaluator.evaluate(
    query=question, response=answer,
    reference=reference, contexts=[context]
)
```

[Complete generated-answer dataset](../snippets/b5/04_evaluate_answer_dataset.py)

<!--
Excerpt illustrates generation followed by one evaluator invocation. Full code loops through the three evaluators, records separate scores/feedback and catches generation/judge errors with attempted cases retained. Relevance's normalized score is explicitly thresholded because its passing field is unset in this installed version.
-->

---

# Separate judgments reveal different failures

Observed development-case acceptance:

| Criterion | Accepted cases |
| --- | --- |
| Correctness | 4/4 |
| Grounding | 3/4 |
| Relevance | 4/4 |

These are model judgments, not verified quality rates.

<!--
Actual 04 run, 6 November 2026. Grounding rejected the waiver-premise response; correctness still accepted it at 4. Both judges also missed an unsupported likelihood inference in the future-release case. Preserve raw answers/feedback so the report can be audited. Do not average these unlike scales or equate aggregate acceptance with truth.
-->

---

# Inspect the waiver answer's actual failure

Condensed observed behavior:

```text
User premise: C2's fee has been waived
Answer: accepts the premise and permits skipping review
Approved context: no waiver information supplied
```

The answer addresses the question, but the operational premise is unverified.

<!--
Condensed actual 04 observation, not a verbatim quote. Its relevance judge passed; grounding failed. Correctness also passed at 4, a false positive relative to the agreed reference. This directs attention to source authority/uncertainty instructions and evaluator limitations rather than a Python threshold repair.
-->

---

# A targeted instruction change

Baseline: answer the shipping enquiry helpfully.

Candidate:

- Use only supplied facts and policy.
- Correct unsupported premises and state unavailable information.
- Do not infer waivers, balances or release dates.
- Answer each requested part while preserving units.

<!--
05 defines this candidate before evaluation using development-task requirements; it does not change the source facts, policy, questions or references. A prompt can help but does not enforce truth or guarantee a higher score. Do not supply the reference to the generator.
-->

---

# Keep the comparison matched

Change the generation instruction.

Keep model/settings, cases, context, references, evaluator models/rubrics and thresholds fixed.

Generate fresh answers for both versions. A tie or regression is a valid outcome.

<!--
Comparing prompts is the initial teaching experiment; model comparison is a later use of the same principles. Don't change generator and grader simultaneously then attribute all score movement to the prompt. No prepared successful candidate replies replace actual outputs.
Source: https://developers.openai.com/api/docs/guides/evaluation-best-practices
-->

---

# Reserve a held-out question

| Split | Role in this comparison |
| --- | --- |
| Four development cases | Inspect failures and formulate the candidate |
| One held-out comparison question | Check a task not used to develop it |

Once its feedback informs tuning, reserve another independent case for the next comparison.

<!--
Held-out question compares C1/C2 amounts and review requirements. It appears in 05, not 04's development set. One held-out example is deliberately small and cannot establish generalization. The candidate is fixed before inspecting that comparison's output. Classroom learners can see source data, so treat this as a process demonstration, not a blind benchmark.
-->

---

# Fresh generation for each prompt and attempt

```text
For each prompt version
    For each unchanged case
        Generate a fresh answer
        Run the same three judges
        Retain text, feedback, status and outcome
```

[Complete matched prompt comparison](../snippets/b5/05_compare_prompts.py)

<!--
05 defaults to repeats=1, so five cases and two versions mean ten generated answers plus judge calls. Increase repeats for more evidence; each .complete request starts from the supplied prompt without retained conversation history. Provider caching/retries are separate behavior. All errors/invalid judgments remain attempted cases.
-->

---

# The observed prompt comparison

All-three-judgments acceptance, one attempt per case:

| Split | Baseline | Candidate |
| --- | --- | --- |
| Development | 3/4 | 4/4 |
| Held out | 1/1 | 1/1 |

Inspect actual answers before interpreting the higher development count.

<!--
Actual 05 run, 6 November 2026. Baseline waiver response failed correctness/grounding; candidate corrected that premise in this run. Held-out answers were accepted under both prompts, so no held-out improvement is shown. Known evaluator false positives remain; acceptance is not proven quality. Different runs may tie, regress or produce errors.
-->

---

# Compare the changed answer, not just totals

In a separate lab run, the candidate correctly challenged the unverified waiver premise.

The relevance judge gave it **0.5**, criticising its refusal to accept that premise. Development acceptance tied at **3/4** for both prompts.

Inspect whether the criterion captures the intended task before interpreting the score.

<!--
Actual separate completed-lab comparison, 6 November 2026. Both prompts accepted the held-out answer. Candidate waiver answer passed correctness/grounding but AnswerRelevancy scored 0.5, penalising refusal to accept the user's waiver claim. That evaluator sees question/answer, not the approved source context. The report retained the threshold of 1 and the tie; it was not changed to manufacture improvement. These are different generated runs from snippet 05's preceding table, not pooled scores.
-->

---

# Preserve unsuccessful and ungraded attempts

| Outcome | Record it as |
| --- | --- |
| Generation failure | Attempt with no generated answer |
| Judge error or invalid result | Unknown judgment with error/status |
| Valid adverse judgment | Scored failure of that criterion |

Keep attempted cases in the declared denominator. Unknown is not a measured zero score.

<!--
04/05 print errors and retain attempted-case denominators. The learner lab additionally saves per-metric status, including range/finite-score validation, and continues other judges after one error. A compound pass is a declared reporting choice; inspect individual metrics. A zero faithfulness score is different from an unavailable judgment.
-->

---

# Repetition and measurement scope

More attempts give additional evidence, not a guarantee.

Report case/split counts and keep errors visible. Separate generation latency from evaluation work when measuring resources.

Small calibration sets, one held-out case and a shared model family leave substantial uncertainty.

<!--
05 can repeat cases; the lab can restrict to a selected case with --repeats 2. Selected-case output is not a full-dataset or held-out score. Current short examples do not collect an aggregate dollar cost; judge calls add usage. Missing token usage remains unknown. Nested span times cannot simply be added as end-to-end generation time.
-->

---

# Traces support agent diagnosis

When an agent answer fails, inspect actual tool requests, returned observations and the final explanation.

A trace can locate where the failure began. It does not replace answer-quality evaluation.

[SDK tracing reference](../snippets/b5/reference/application_checks/04_trace_openai_agent.py) · [LlamaIndex events reference](../snippets/b5/reference/application_checks/05_trace_llamaindex_agent.py)

<!--
Supporting examples preserve the prior tool/rule investigation. Exact outbox effects and deterministic checks remain useful application/agent tests, but are not the core generated-answer evaluation. No new runtime or hosted observability setup is introduced here.
-->

---

# Lab · Evaluate actual generated answers

| Checkpoint | Learner work |
| --- | --- |
| Cases and generation | Independent references; real model answers |
| Evaluation | Configure and call the three evaluators |
| Calibration | Inspect prepared-label agreement and mistakes |
| Dataset | Read per-case answers, scores and feedback |
| Prompt comparison | One candidate; matched cases and held-out task |

[Independent B5 learner lab](../labs/container_help_desk/B5.md)

<!--
Five learner TODO functions, supplied actual-model/evaluation/reporting runners, no dependency on unfinished B4. Target 60 minutes including exploration, with setup completed beforehand; instructor timing unvalidated. Formal assessments and new notebooks remain deferred.
-->

---

# A checked claim of improvement

Generate actual answers. Compare them with independent expectations and supplied evidence.

Inspect the judges as well as the model. Retain changed-case answers, regressions and remaining uncertainty.

**Explain:** what would you do when a judge passes an answer whose release claim exceeds the context?

<!--
Answer cue: identify the unsupported claim, inspect reference/context and judge feedback, add a labelled probe, and revise/recheck the evaluator if needed. Rerun both prompt versions if evaluation criteria change. The five core snippets, Markdown deck and lab follow this generated-answer evaluation sequence.
-->
