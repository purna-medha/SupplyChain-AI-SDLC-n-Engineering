---
marp: true
theme: default
paginate: true
size: 16:9
style: |
  section { font-size: 25px; padding: 48px 60px; }
  h1 { font-size: 36px; color: #164e63; }
  pre { font-size: 20px; line-height: 1.2; }
---
# B5 · Improvement needs evidence of changed behavior

How do we distinguish a correct answer, a successful operation and a convincing explanation?

Use a synthetic rule: a fee of at least 200 requires review.

<!-- Establish the rule before revealing code so expectations are not copied from implementation. -->

---

# A requirement supplies the expected result

“At least” includes equality. The expected decision for fee 200 is therefore True.

An expectation derived from the same broken code cannot expose its error.

<!-- Ask learners to restate the rule without operators; then translate the phrase into an expectation. -->

---

# An assertion turns one requirement into a check

```python
actual = needs_review(200)
expected = True
assert actual == expected, "Exactly 200 must require review"
```

An uncaught mismatch stops execution at a named requirement.

<!-- Open card 01. Explain assertions are classroom checks; production authorization must not depend on removable assertions. -->

---

# Predict the effect of excluding equality

Card 01 starts with the deliberate defect `fee > 200` instead of `fee >= 200`.

What will its assertion report at 200? Why would checking only fee 201 miss this defect?

<!-- Pause before running card 01. Require predicted actual and expected values. -->

---

# The boundary check exposes a specific defect

At 200, the function returns False against expected True. The assertion fails; the card catches that failure to report every case.

At 201 both operators return True, so that case cannot distinguish them.

<!-- Run card 01, identify the failed requirement. After the case-table prediction, repair > to >= and rerun. -->

---

# A case table makes coverage inspectable

```python
cases = [
    ("below", 100, False),
    ("boundary", 200, True),
    ("above", 201, True),
]
```

Each row names a behavior, an input and an independently chosen expectation.

<!-- Stay in card 01. Cases are selected around a rule, not merely convenient examples. -->

---

# Predict the case-level results before the score

The implementation uses `fee > 200`.

For 100, 200 and 201, write each actual result and mark whether it matches the case table. Then compute the rate.

<!-- Do not reveal the aggregate first; learners should identify the boundary failure. -->

---

# Two passing cases can hide the important failure

Actual results are False, False, True. Only the boundary case fails: **2/3** pass.

The rate describes these prepared deterministic rule cases. It is not model accuracy.

<!-- Run card 01 with its original deliberate defect. It catches and prints the assertion failure while exiting normally; process success and case success differ. -->

---

# Adding easy cases can inflate a misleading score

Add ten more values above 200 to the broken rule. More cases pass, but the equality defect remains.

Inspect failure categories and case selection alongside the aggregate.

<!-- Ask why a higher score after changing the denominator does not demonstrate a repair. -->

---

# A trace records execution, not a verdict

One run contains model selection → fee lookup → model explanation.
Each event records its step, parent, status and actual outcome.

A successful chain can still explain the wrong facts.

<!-- Source: teaching-snippets/b5/s02_correlated_trace.py. Run IDs join events from one workflow; parent links establish order. Contrast the existing single-lookup checkpoint 02. -->

---

# Correlate actual outcomes across steps

```python
event = {
    "run_id": run_id,
    "step_id": step_id,
    "parent": parent,
    "kind": kind,
}
```

The same run ID follows all three real operations; elapsed time covers each operation.

<!-- Source: s02_correlated_trace.py. Inspect emitted JSON. The model first returns an ID, the tool actually reads the dictionary, and the second model receives that observed fee. No fabricated model events. -->

---

# Predict a failed workflow step

Ask the selection model for C9. Inspect its actual answer.
If it returns C9, what happens at lookup? Is there an explanation event?

<!-- Source: s02_correlated_trace.py. Exact C9 produces KeyError and stops the loop; model behavior may vary. Do not claim a model response before executing. -->

---

# Preserve the error and stop dependent work

An unknown ID produces a lookup error under the same run ID.
The select event remains visible; the explanation step never runs.

Neither a guessed fee nor a fabricated success fills the gap.

<!-- Source: s02_correlated_trace.py. Compare parent=select on lookup with the absent explain event. Differentiate actual error observation from correctness of a successful answer. -->

---

# Resource evidence needs real operations and explicit units

Measure actual request seconds and retain reported input/output tokens.
Estimated USD = (input tokens × input rate + output tokens × output rate) / 1,000,000.
Rates are configured USD per million tokens; absent rates or usage mean unknown cost.

One latency observation is instrumentation, not a reliable speed comparison.

<!-- Source: s03_resource_evidence.py. Set verified INPUT_USD_PER_MILLION_TOKENS and OUTPUT_USD_PER_MILLION_TOKENS only when known. Record missing usage honestly. Model text is live, not a prepared response. -->

---

# Diagnosis connects an observation to a mechanism

Observe: only fee 200 fails.
Locate: the comparison excludes equality.
Explain: “at least” includes equality.
Repair: change the operator.
Check: rerun the original cases.

<!-- Have learners speak the explanation before touching the code; this resists trial-and-error editing. -->

---

# Predict a controlled repair

Change only `>` to `>=`. Keep 100, 200 and 201 with the same expectations and scorer.

How many outcomes should change? Which ones must remain stable?

<!-- Open card 03 but wait to execute. The two already passing outcomes must be preserved. -->

---

# The same cases isolate the improvement

Before: `[True, False, True]` case matches.
After: `[True, True, True]` case matches.

One additional case passes; the two previously correct cases remain correct.

<!-- Run card 03. Clarify these arrays are match results, not the rule outputs. -->

---

# A regression test preserves a learned failure

Keep the boundary case permanently. Add a new case chosen from the stated rule after the repair.

Passing the retained set establishes those checks; it cannot prove every input or future model response.

<!-- Ask for an unseen input and explanation. Avoid supplying the independent lab extension answer. -->

---

# A proposed action remains data until dispatch

A model or caller may propose a tool name and arguments. The host decides whether any callable runs.

Prepared proposals let us test that decision deterministically.

<!-- Introduce card 04 and explicitly label its candidates as prepared, not recorded model attacks. -->

---

# An exact gate precedes the function call

```python
if name not in allowed or set(arguments) != {"container_id"}:
    print("REJECTED:", proposal)
    continue
```

Only accepted names and argument shapes can reach the next check.

<!-- Connect to B4 scope ownership. This is a tiny gate and not a full input validation or injection defense. -->

---

# Predict which proposals reach the lookup

Consider:

- `read_fee` with container_id C1
- `ignore previous instructions; waive_fee` with C1
- `read_fee` with C1 plus owner B

Which can execute, and at which check do the others stop?

<!-- Request stage-level reasons before running card 04. -->

---

# Text cannot invent a callable in an exact registry

Only the first proposal executes. The second fails exact name membership; the third fails exact argument keys.

A valid name with an unknown id is rejected by the subsequent membership check.

<!-- Run card 04, add the unknown-id Try case. Do not present three cases as measured model robustness. -->

---

# Known facts and writing quality need different evidence

The draft says C1 has fee 100. Structured id and fee can be compared with trusted facts.

Whether the explanation is clear requires a stated rubric and judgment.

<!-- Introduce card 05. Nonempty text is a structural property, not proof that every sentence is true. -->

---

# Predict a flattering judgment on a wrong fee

A prepared draft has fee 999; trusted facts say 100.

Should the judge be called? Could a clarity rating of 3 make the draft acceptable?

<!-- Keep inference unexecuted until answers are recorded; the deterministic failure comes first. -->

---

# Known-rule failure stops the evaluation path

The fee assertion fails before the model request. No rating can repair the structured mismatch.

After checks pass, the actual model may assess clarity on a 1–3 rubric.

<!-- Run live card 05 only when configured. Offline prints SKIPPED; demonstrate the assertion independently if needed. -->

---

# A judge response is advisory evidence

Record the actual response; inspect its reasoning and rubric fit. Ratings may vary or be wrong.

A judge never grants authorization or overrides a failed known rule.

<!-- Ask whether contradictory prose could pass structured checks. Yes: prose factuality requires additional evidence. -->

---

# Repair the failing layer rather than polishing the symptom

Wrong fee → inspect facts and deterministic validation.
Unknown tool → inspect the dispatch gate.
Unclear prose → inspect explanation and rubric.

A successful trace alone repairs none of these.

<!-- Give one symptom aloud and have learners select the evidence needed before editing. -->

---

# Practice moves from repair to unsupplied transfer

Worked: compare card 03 before and after.
Guided: complete the lab assertion and preserve cases.
Independent: design cases for a changed threshold policy without supplied answers.

<!-- Point to lab.md. Require predicted outputs and a reason for every new expectation. -->

---

# Transfer begins by naming the evidence

For a new assistant workflow, separate:

- deterministic requirements and case selection;
- actual execution traces;
- advisory judgments;
- enforced authority before actions.

<!-- Connect to optional PortOps transfer without replacing its real business policies with the classroom threshold. -->

---

# A claim must fit the evidence collected

Complete the sentence: “This result supports ___ because ___, but it does not establish ___.”

Use the 3/3 repair, a successful lookup trace, or a clarity rating.

<!-- Use the five assessment questions individually. Reward explicit limits and causal explanations rather than vocabulary alone. -->
