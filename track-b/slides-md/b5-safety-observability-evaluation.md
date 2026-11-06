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

# B5 · Evaluating and improving AI applications

One incorrect fee decision, an execution trace and a checked repair

Requirements · Cases · Diagnosis · Re-evaluation

<!--
60-minute lecture: slides 2–10, 15 minutes; 11–19, 18 minutes; 20–25, 10 minutes; 26–36, 17 minutes. The central investigation follows C2's boundary error through checking, trace diagnosis, repair and repeated trials. Only then transfer the method to action outcomes and language judgments. Run selected demonstrations. File numbering is retained: teaching order 01,02,03,04,05,08,09,06,07. All records/policies are synthetic. B5 follows B6 in the course. ../B5-OUTLINE.md gives scope; ../snippets/b5/VERIFICATION.md records the 5 November observations. No hosted tracing account or evaluation service is needed.
-->

---

# The incorrect fee decision

The assistant answers:

> C2's recorded fee is USD 200. It is clear to proceed.

The classroom policy requires review for fees of **USD 200 or more**.

**Predict:** which part of the answer is wrong, and how would you establish the expected decision?

<!--
Opening illustration, not a verbatim promised model answer. Answer cue: the amount can be correct while clear is wrong. Derive review from the independent policy. Actual SDK/LlamaIndex observations later show this boundary error. Start with a concrete failure before introducing evaluation vocabulary.
-->

---

# The facts and policy for this investigation

| Record | Owner | Recorded fee | Expected decision |
| --- | --- | --- | --- |
| C1 | A | USD 100 | clear |
| C2 | A | USD 200 | review |
| C9 | — | No record | unknown |

A denied or unavailable read supplies no fee.

These are synthetic B5 fixtures, independent of B4's database examples.

<!--
Both known records belong to A here; B4 assigned C2 to B. Explain this fixture boundary explicitly. The defect is >200 instead of >=200, not a model's private reasoning. No production shipping policy is implied.
-->

---

# Turn the requirement into separate checks

| Requirement | What to inspect |
| --- | --- |
| Correct identity | Requested ID matches the result |
| Correct recorded fee | Amount matches the trusted fixture |
| Correct decision | Rule includes equality at 200 |
| Supported explanation | Claims follow from the supplied evidence |

A fluent answer can pass one requirement and fail another.

<!--
Later extensions add exact state-change and permission checks. For now hold the fee-decision task in focus. A successful API call or a structurally valid response does not establish every requirement.
-->

---

# Check one prepared answer

Trusted C2 fee: **200**. Prepared draft fee: **999**.

```python
checks = {
    "correct container": draft.get("container_id") == facts["container_id"],
    "correct amount": draft.get("fee") == facts["fee"],
    "source label": draft.get("source") == facts["source"],
}
```

Observed: `correct amount FAIL`; the other checks pass.

[Complete single-answer check](../snippets/b5/01_check_one_answer.py)

<!--
The first runnable illustration is offline. The full 20-line file defines facts/draft and also checks required fields and exact integer type. This excerpt selects three checks. Changing draft fee 999 to 200 makes all five pass. These checks do not evaluate the explanation text's meaning.
-->

---

# Cases cover different requirements

| Case | Input and trusted context | Expected result |
| --- | --- | --- |
| Below | A requests C1 | 100, clear |
| Boundary | A requests C2 | 200, review |
| Missing | A requests C9 | Unknown, no fee |
| Denied | B requests C2 | Denied, no fee |
| Dependency | A requests C2, source unavailable | Unavailable, no fee |

**Predict:** which case distinguishes `> 200` from `>= 200`?

<!--
Answer cue: boundary. Select representative cases from requirements before running the application. Denied and dependency cases check different conditions. The unavailable flag is a controlled fixture, not evidence of a real remote outage.
-->

---

# A case pairs an input with an expectation

```python
("boundary", "A", "C2", False, (200, "review"))
```

```text
Name | caller | requested ID | source unavailable? | expected result
```

Compare the application's actual result with this independent reference.

[Complete case loop](../snippets/b5/02_evaluate_cases.py)

<!--
The tuple comes from 02. Walk across each field before opening the loop. The reference comes from policy, not from calling the same function to generate its own expected answer. The plain loop prints expected/actual/PASS/FAIL without an evaluation framework.
-->

---

# The baseline exposes the boundary error

Observed deterministic checks:

| Case | Expected | Actual |
| --- | --- | --- |
| Below | 100, clear | 100, clear |
| Boundary | 200, review | 200, clear |
| Missing, denied, dependency | Controlled absence | Matches |

**4/5 pass.** The failing requirement is now specific.

<!--
Actual offline 02 observation. This is distinct from later repeated live agent scores of 4/6 and 6/6. Do not combine their denominators. The boundary failure is deliberate. Before trusting the result, also check that the grader itself discriminates correct/incorrect outputs.
-->

---

# Check the checker

| Supplied probe | Expected acceptance |
| --- | --- |
| Correct C2 amount and integer type | True |
| Wrong amount or container | False |
| Amount supplied as text | False |
| Missing fee | False |

**Predict:** what happens if the grader always returns `True`?

[Complete grader probes](../snippets/b5/03_check_the_grader.py)

<!--
Answer cue: the known-wrong probe exposes it. Actual 03 assertions agree with all five labels; a controlled always-true mutation fails on wrong amount. Grader probes are separate known-answer checks, not new application case scores. Wording checks arrive later.
-->

---

# Controlled tests and real model evaluations

| Controlled operation | Real model operation |
| --- | --- |
| Supply known inputs/results | Let the model choose an output or tool call |
| Check rules, parsing and state transitions | Check actual answer and execution |
| Reproduce the boundary exactly | Observe repeated trials |

Both require expectations defined before execution.

<!--
02 establishes the deterministic rule defect. 04/05 next observe how it appears inside actual agent runs; they do not replace model replies with prepared success. Mocked errors test handling of supplied failures, not what a live provider/model will do.
-->

---

# Locate where the wrong decision begins

```text
User requests C2
    Model selects read_fee with an ID
    Runtime executes the tool
    Tool returns a fee and decision
    Model explains the observation
```

Inspect the ID, observation and final answer in that order.

<!--
Reuse B2's tool loop. The model can select the wrong ID, the tool can apply a wrong rule, or generation can exceed a correct observation. Locate the earliest mismatch rather than changing prompts by default.
-->

---

# Traces, spans and events

A **trace** connects the operations belonging to a request.

A **span** records an operation, its timing and parent relationship.

An **event** records an observation during execution.

```text
Agent run → model operation → tool operation → model operation
```

<!--
This is a conceptual sequence, not a complete span tree. Frameworks can add nesting. Captured arguments/results help diagnosis; names/timing alone do not supply payloads. A trace does not reveal private model reasoning or establish correctness.
Source: https://developers.openai.com/api/docs/guides/agents/integrations-observability
-->

---

# Capture one SDK run locally

```python
set_trace_processors([processor])
result = Runner.run_sync(
    agent, request, max_turns=4,
    run_config=RunConfig(trace_include_sensitive_data=True),
)
```

The example prints native span relationships and synthetic tool arguments/results.

[Complete SDK trace example](../snippets/b5/04_trace_openai_agent.py)

<!--
The full file defines processor as BatchTraceProcessor with a small readable console exporter. request abbreviates its formatted Check message. Local printing replaces hosted export. Sensitive payload capture is deliberately enabled for synthetic fixtures; real retention needs deliberate choices. This excerpt illustrates native capture, not a custom tracing implementation or dashboard ingestion.
Source: https://developers.openai.com/api/docs/guides/agents/integrations-observability
-->

---

# The first incorrect observation

Observed C2 SDK run, condensed:

```text
Tool requested: read_fee(container_id="C2")
Tool observation: fee=200, decision="clear"
Final answer reports: fee=200, decision="clear"
Policy expects: decision="review"
```

The requested ID and amount are correct. The wrong decision already exists in the tool result.

<!--
Actual 04 observation, 5 November 2026. The final wording is condensed. The evidence implicates the business rule before generation, rather than model choice or source amount. Different future runs still need inspection.
-->

---

# Diagnose the responsible layer

| Earliest mismatch | Investigate |
| --- | --- |
| Source amount is wrong | Data or source selection |
| Tool requests the wrong ID | Arguments or task context |
| Correct fee, wrong tool decision | Business rule |
| Correct observation, unsupported final claim | Generation or evidence use |

**Predict:** which row fits the observed C2 trace?

<!--
Answer cue: business rule. Other rows are diagnostic alternatives, not claimed failures in the current run. Missing retrieved evidence belongs at retrieval/context selection, connecting B6 to this method. Also inspect the reference/checker before assuming an application defect.
-->

---

# The same investigation in LlamaIndex

| Evidence | SDK | LlamaIndex |
| --- | --- | --- |
| Requested container | C2 | C2 |
| Recorded fee | 200 | 200 |
| Tool decision | clear | clear |
| Independent expected decision | review | review |

Changing the runtime leaves the defective rule in place.

<!--
04 and 05 use the same model, instruction, records and faulty rule. Actual 5 November observations show the same first wrong result. This is a conceptual/runtime comparison, not a controlled framework performance benchmark. No second evaluation system is built.
-->

---

# LlamaIndex events expose the observation

```python
async for event in handler.stream_events():
    if isinstance(event, ToolCallResult):
        print(event.tool_name, event.tool_kwargs)
        print(event.tool_output)
result = await handler
```

Tool events supply payloads. `SimpleSpanHandler` separately supplies timing and parents.

[Complete LlamaIndex trace example](../snippets/b5/05_trace_llamaindex_agent.py)

<!--
Selected print calls from the full file; its labels add readability. Native spans in this locked environment do not themselves supply argument/result payloads. streaming=False disables token streaming while workflow events remain available. Check what the chosen recorder actually captures.
Sources: https://developers.llamaindex.ai/python/framework/understanding/agent/streaming/ and https://developers.llamaindex.ai/python/framework-api-reference/instrumentation/span_handlers/
-->

---

# Repair the rule implicated by the evidence

The requirement includes equality at USD 200.

```python
# Baseline
requires_review = fee > 200

# Candidate
requires_review = fee >= 200
```

Keep the model, instruction, source facts and expectations fixed.

<!--
08 isolates the deterministic repair before 09 tests it inside actual agent trials. No new architecture, retrieval path or prompt is needed to fix this observed defect. The condition is a direct mechanism-level illustration of the code in 08/09.
-->

---

# Recheck the failure and its neighbors

Observed isolated rule results:

| Recorded fee | Required decision | Baseline | Candidate |
| --- | --- | --- | --- |
| 100 | clear | clear | clear |
| 200 | review | clear | review |
| 201 | review | review | review |

Only the boundary decision needed to change.

[Complete deterministic repair comparison](../snippets/b5/08_repair_and_compare.py)

<!--
Actual 08 output. The original 100/200 cases and references stay fixed; 201 is an additional case separate from the repair examples. This does not infer later live model outcomes. Ask what a repair that also changed 100 to review would break.
-->

---

# Independent trials start from fresh state

Each repeated decision trial gets:

- A new agent conversation.
- The same defined source facts and policy expectation.
- An empty record of tool calls.

A previous success must not supply the next attempt's evidence.

<!--
09 creates a new Agent and calls list per attempt while holding the source fixture fixed. No outbox is part of this decision task. The later action example resets its own outbox. Isolated means starting from each case's defined fixture, not erasing legitimate history during a multi-turn task.
Source: https://www.anthropic.com/research/demystifying-evals-for-ai-agents
-->

---

# Define success for the repeated task

09 asks for exactly one decision label: `clear`, `review` or `unknown`.

A pass requires the expected label and actual tool requests for the intended ID.

```python
passed = actual == expected and bool(calls) and all(
    cid == container_id for cid in calls
)
```

[Complete real-agent repeated trials](../snippets/b5/09_repeat_agent_trials.py)

<!--
Same predicate as 09, wrapped for readability. The label-only task is explicit; this does not grade arbitrary natural-language explanations, fee fields or permission effects. Errors/incomplete runs get visible nonmatching outcomes rather than disappearing. Baseline/candidate share model, instruction, cases and checker.
-->

---

# Compare the same cases after repair

Observed real SDK trials, two attempts per case/version:

| Decision case | Baseline successes | Candidate successes |
| --- | --- | --- |
| C1: below boundary | 2/2 | 2/2 |
| C2: at boundary | 0/2 | 2/2 |
| C9: missing | 2/2 | 2/2 |

Total decision-task passes: **4/6 → 6/6**.

<!--
Actual final matched 09 comparison, 5 November 2026. No default errors/incomplete runs occurred. The isolated rule check and live agent comparison are different evidence. These scores do not cover the action/denial/clarity tasks. A prior instruction-development run remains separately recorded in verification; these matched runs use the same final instruction.
-->

---

# Stopped attempts remain in the score

A low turn limit can stop the workflow before its final answer.

```text
INCOMPLETE: turn limit
```

If one of two attempts succeeds and the other stops, report **1/2**.

Retain each error or stop reason rather than dropping that attempt.

<!--
The 1/2 illustration is hypothetical, not a captured 09 score. Actual low-limit probes retained all incomplete attempts as failures. 04 raises MaxTurnsExceeded after an explicit incomplete message; 05 surfaces its workflow limit. Different limit units are not aggregate token/tool budgets. Lowering max_turns is a suggested 09 variation.
-->

---

# A small passing sample leaves uncertainty

C2's result of 2/2 means two successful attempts from clean fixtures.

It does not establish a precise production success rate.

The current score covers the decision-label task. It does not establish that every explanation is supported or every action is permitted.

<!--
Report attempt counts and scope together. No cherry-picking the best trial or retrying entire failed trials until a pass. Provider-level retries are a separate mechanism. Judge scores and held-out tasks cannot be silently added to this denominator.
Source: https://www.anthropic.com/research/demystifying-evals-for-ai-agents
-->

---

# Inspect regressions by requirement

Prepared comparison for discussion:

| Category | Baseline | Candidate |
| --- | --- | --- |
| Boundary decision | 0/2 | 2/2 |
| Denied access | 2/2 | 1/2 |

The total rises from 2/4 to 3/4 while denied-access behavior gets worse.

**Predict:** has the permission requirement been satisfied?

<!--
Answer cue: no. Hypothetical category comparison, separate from observed runs. A better average cannot compensate for a failed authority boundary. Preserve failing cases and their category breakdown; adding easy cases is not a repair.
-->

---

# Apply the method to other requirements

The rule investigation used an exact expected decision.

| New requirement | Appropriate evidence |
| --- | --- |
| “The update was queued” | Exact new state after execution |
| “The explanation is clear” | A narrow language rubric |
| “The explanation follows the source” | Claims checked against source evidence |

Choose the check that establishes the particular requirement.

<!--
Explicit transition after completing the main investigation. Do not start a new architecture. The next action/clarity examples transfer the same expectation -> actual observation -> comparison method. A favorable clarity result does not establish source grounding or authority.
-->

---

# An action claim needs a state change

The assistant says:

> Your C2 update is queued.

Before the trial, the outbox already contains an identical old entry.

**Predict:** why would searching for the text afterward give a false pass?

<!--
Answer cue: the old entry could match even when no new action occurred. New scenario reuses B3's reviewed action; it is distinct from 09's decision-label task. The local demonstration outbox sends no external messages and is not a durable delivery service.
-->

---

# Compare the complete before and after state

For the same reviewed payload:

| Review outcome | Initial entries | Final entries | New entries |
| --- | --- | --- | --- |
| Approved, permitted payload | 1 | 2 | 1 |
| Rejected | 1 | 1 | 0 |

Count is useful; also verify the exact resulting entries.

[Complete SDK action-outcome example](../snippets/b5/06_check_action_outcome.py)

<!--
Actual default 06 observations: approval adds one exact entry; rejection adds none; full-state comparisons pass. Review decisions are supplied evaluation fixtures, not live human approvals. A count alone cannot establish that the right payload was added.
-->

---

# Check the exact action outcome

```python
expected = before + [reviewed] if should_queue else before
print("New entries:", len(outbox) - len(before))
print("Exact outcome:", "PASS" if outbox == expected else "FAIL")
```

A rejected or unapproved changed payload must leave the initial state intact.

<!--
Excerpt from 06. Host review checks caller A and exact pending payload, and the tool independently checks caller/approved payload. In the caller=B variation, host review rejects before the function executes, so that variation does not exercise the tool's separate caller check. Changed-text and denied-caller trials add no entries. No external message is sent.
-->

---

# Reset between trials; preserve history within one

```text
Start independent trial from its defined fixture
    Model proposes the action
    Review checks that pending payload
    Resume the same trial's conversation
    Compare the resulting state
Start the next trial from its defined fixture
```

Resuming an interrupted task is different from starting a fresh trial.

<!--
06 restores the seeded outbox and approved payload between approve/reject trials. It uses result.to_state() and resumes the same conversation within each trial. Resetting at resume changes the task. This complements 09's clean independent conversations; it does not contradict them.
-->

---

# A language rubric needs a narrow purpose

The clarity question is:

> Does the explanation plainly state the fee and review decision?

Accept equivalent wording. Reject unexplained codes.

Clarity alone cannot establish that the fee follows from a source or that an action was authorised.

<!--
07 uses LlamaIndex GuidelineEvaluator on prepared drafts. Its query/response input does not verify source facts. 01 separately demonstrates field correctness. Do not substitute an LLM judgment for a deterministic permission or exact state check.
Source: https://developers.llamaindex.ai/python/framework-api-reference/evaluation/guideline/
-->

---

# Check the judge against labelled examples

| Prepared draft | Reference label | Observed judge |
| --- | --- | --- |
| Clear fee and review explanation | Pass | Pass |
| Valid paraphrase | Pass | Pass |
| Unexplained codes | Fail | Fail |

Inspect disagreements and feedback before trusting a larger score.

[Complete narrow clarity judge](../snippets/b5/07_judge_clarity.py)

<!--
Actual 07 calls agreed with all three author-assigned labels on 5 November 2026. This is not independent validation of judge accuracy. The full file constructs GuidelineEvaluator and prints passing/feedback for each draft. Keep rubric/model consistent across a comparison; changes require rechecking known examples. Prepared drafts are not new agent responses.
Source: https://arxiv.org/abs/2306.05685
-->

---

# Quality, elapsed time and resource use

04 prints end-to-end elapsed run time and actual input/output tokens.

05 prints selected span durations. Nested or overlapping spans cannot simply be added into a run total.

A cost estimate needs the applicable rates; judge calls add separate evaluation usage. Missing usage remains unknown.

<!--
Reuse B1's cost-estimation concept without adding another pricing lecture. 04 stops the timer when the SDK returns, before trace flush/printing. 05/judge provider usage is not collected. These are not controlled framework performance benchmarks. A faster incorrect answer does not meet the quality requirement.
-->

---

# Keep evidence for the next regression run

Retain the failing input, initial fixture and independent expected outcome.

Record code/model/rubric configuration and detailed attempts, including errors, stop reasons and relevant state changes.

Capture the source observations needed to explain the failure.

[Run guide and verification record](../snippets/b5/README.md)

<!--
C2 remains in the case set after the repair. The earlier reference runner's unsupported not-finalized implication is retained in historical evidence, not presented as a current short-example output. Real content retention needs deliberate redaction/access choices; classroom trace payloads are synthetic. Record relevant evidence, not inferred private reasoning.
-->

---

# Re-evaluate after application changes

A model, instruction, tool, source or rubric change can alter behavior.

Rerun relevant cases and inspect remaining failures by requirement.

Reviewed operational feedback supplies new cases. A small passing classroom suite leaves untested tasks and failure modes.

<!--
Conceptual change-triggered evaluation, not CI/deployment setup. Full red-teaming, monitoring infrastructure, hosted evaluation services and lab scaffolding remain outside the hour. The current implementation uses local loops and SDK/framework calls.
Source: https://developers.openai.com/api/docs/guides/evaluation-best-practices
-->

---

# The checked improvement

C2's recorded fee was correct; the tool's boundary decision was wrong.

An independent expectation exposed the failure. The trace located it. A targeted rule change repaired the observed decision under the same checks.

**Explain:** what would you inspect if the next tool result were correct but the final answer added an unsupported claim?

<!--
Answer cue: generation/evidence use; compare final claims with the supplied observation, not only the field or clarity score. Close the central investigation without implying universal reliability or permission. Nine short examples illustrate the method; labs, assessments, new notebooks and deployment remain deferred. Matching Gamma text preserves the visible sequence.
-->
