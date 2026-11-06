# B5 · Evaluation, tracing and improvement

**Start with [01 · Check one answer](#01-check-one-answer).** Finish one example before moving to the next.

By the end, you can define a check, find where a wrong result begins, verify an action's effect, and compare a repair against unchanged expectations.

Run commands from **track-b** after completing [shared setup](../../SETUP.md). Each file is complete and imports no teaching helpers. No server or observability account is needed. Allow about **60 minutes** for the lessons, excluding setup; model response times vary.

## Part 1 · Decide what correct means

### 01 Check one answer

1. **Understand.** A well-formed answer can contain a wrong fact. Check requirements separately: required fields, types, identity, amount and source. This prepared example compares a draft against a trusted record for C2, whose recorded fee is USD 200.
2. **Predict.** The draft has all the required fields but gives a fee of 999. Which check should fail?
3. **Run** [01_check_one_answer.py](01_check_one_answer.py). This lesson is offline.

   ```bash
   uv run python snippets/b5/01_check_one_answer.py
   ```

4. **Observe.** `correct amount FAIL` appears while the other checks pass. This is an intentional lesson result, not a setup error. The checks inspect fields; they do not evaluate the explanation text's meaning.
5. **Try.** Change the draft fee from 999 to 200 and rerun. All five checks should pass. You have corrected one fact without changing the requirements.

### 02 Test more than the happy path

1. **Understand.** A case pairs an input with an independently chosen expected outcome. Test boundaries, missing records, denied access and unavailable dependencies. Here, caller A owns C1/USD 100 and C2/USD 200; fees **at least USD 200** require review.
2. **Predict.** Does `fee > 200` implement that policy at exactly 200?
3. **Run** [02_evaluate_cases.py](02_evaluate_cases.py). This lesson is offline.

   ```bash
   uv run python snippets/b5/02_evaluate_cases.py
   ```

4. **Observe.** Four of five cases pass. The boundary case expects `(200, "review")` but receives `(200, "clear")`. Missing, denied and unavailable outcomes preserve the absence of a fee. `unavailable=True` is a supplied test condition, not a real service outage.
5. **Try.** Replace only `fee > 200` with `fee >= 200` and rerun the same cases. Expect 5/5. Keep the expected outcomes fixed so the comparison still tests the policy.

### 03 Check the checker

1. **Understand.** A grader can be defective too. Give it known correct and incorrect answers, with expected accept/reject decisions. A checker that accepts everything cannot tell you whether a repair worked.
2. **Predict.** Should C2 with the text value `"200"` pass a checker requiring an integer amount?
3. **Run** [03_check_the_grader.py](03_check_the_grader.py). This lesson is offline.

   ```bash
   uv run python snippets/b5/03_check_the_grader.py
   ```

4. **Observe.** The known correct answer is accepted. Wrong amount, container, type and missing fee are rejected. The assertions confirm that the checker agrees with each supplied reference decision.
5. **Try.** Temporarily replace the body of `correct_fee` with `return True` and rerun. Expect an assertion failure on `wrong amount`. That failure exposes the defective checker; restore the function afterward.

## Part 2 · Find the cause and check the effect

The next three lessons make actual model calls using `OPEN_AI_KEY`. Their records and policies are synthetic; they do not depend on edits made in Part 1.

### 04 Trace an SDK request

1. **Understand.** An incorrect final answer may originate in the tool's observation. A trace links the model request, tool arguments, returned observation and final answer. Find the first point where the evidence conflicts with the policy before changing a prompt.
2. **Predict.** For C2/USD 200, should the tool report `clear` or `review` under the policy from lesson 02?
3. **Run** [04_trace_openai_agent.py](04_trace_openai_agent.py).

   ```bash
   uv run python snippets/b5/04_trace_openai_agent.py
   ```

4. **Observe.** Find the function span's arguments and observation. The deliberately defective tool returns fee 200 with decision `clear`; `POLICY EXPECTS: review` supplies the independent reference. In the verified run, the final answer copied the wrong decision. Native SDK spans are printed locally; this does not test a hosted dashboard.
5. **Try.** Change `container_id` from `"C2"` to `"C1"` and rerun. Its fee 100 should produce `clear`. Compare the tool observation with the final answer, rather than judging only the wording.

### 05 Investigate the same request with LlamaIndex

1. **Understand.** The evidence you need stays the same across runtimes: requested input, actual tool result and final explanation. LlamaIndex tool events expose arguments/observations; its native spans provide parent relationships and timing.
2. **Predict.** Can changing the orchestration library repair the same defective fee rule?
3. **Run** [05_trace_llamaindex_agent.py](05_trace_llamaindex_agent.py).

   ```bash
   uv run python snippets/b5/05_trace_llamaindex_agent.py
   ```

4. **Observe.** For C2, look for fee 200 and decision `clear` in the observation. The policy still expects review. In the verified run, the final answer also reported clear. Different instrumentation exposes the same underlying rule error.
5. **Try.** Set `container_id = "C9"` and rerun. Look for an absent fee and `unknown`; check that the answer does not invent an amount.

### 06 Check what an approved action actually changed

1. **Understand.** “Queued” in an answer does not prove a new action occurred. Compare complete state before and after execution. This example starts with an old identical outbox entry, so merely finding the payload afterward is insufficient. It reuses B3's pause/review/resume mechanism.
2. **Predict.** How many **new** entries should approval add? How many should rejection add?
3. **Run** [06_check_action_outcome.py](06_check_action_outcome.py). It supplies review decisions automatically as evaluation inputs; no interactive approval is needed.

   ```bash
   uv run python snippets/b5/06_check_action_outcome.py
   ```

4. **Observe.** The approval trial should add one exact new entry; the rejection trial should add none. Inspect `PENDING`, `New entries` and `Exact outcome: PASS`. Each trial restores its initial outbox, while a paused/resumed trial preserves its conversation. This local outbox sends no external messages.
5. **Try.** Set `caller = "B"` and rerun. Both trials should add zero entries and pass their unchanged-state checks. Here, host review rejects caller B before tool execution. The tool also contains a separate caller check; this variation does not exercise it.

## Part 3 · Judge narrowly and compare a repair

### 07 Judge clarity with an explicit rubric

1. **Understand.** Some requirements concern language rather than exact fields. A narrow rubric can ask whether an explanation is understandable and accept equivalent wording. That judgment does not establish factual truth or permission to act.
2. **Predict.** Which is clearer: “A reviewer must check it” or `R1 XFLAG-A7`?
3. **Run** [07_judge_clarity.py](07_judge_clarity.py). This makes evaluator model calls.

   ```bash
   uv run python snippets/b5/07_judge_clarity.py
   ```

4. **Observe.** Compare each `REFERENCE LABEL` with `JUDGE` and read the feedback. The verified run accepted the plain explanation and paraphrase, then rejected the unexplained codes. These three author-labelled examples do not establish judge accuracy.
5. **Try.** Rephrase the second draft using different plain language, preserving its amount and review meaning. Keep its reference label `True`. Rerun and inspect the judgment: equivalent wording should be acceptable under this rubric, while the model's verdict still needs review.

### 08 Verify the repair against unchanged cases

1. **Understand.** A repair comparison is meaningful when its cases and expectations stay fixed. Change the suspected cause, then check both the failure and neighboring inputs. This example compares `> 200` with `>= 200` without involving a model.
2. **Predict.** Which fee should change decision: 100, 200 or 201?
3. **Run** [08_repair_and_compare.py](08_repair_and_compare.py). This lesson is offline.

   ```bash
   uv run python snippets/b5/08_repair_and_compare.py
   ```

4. **Observe.** At 200, BASELINE fails and CANDIDATE passes. Fee 100 remains clear in both. The additional 201 case returns review in both. Only the boundary decision needed to change.
5. **Try.** Replace only `fee >= 200` with `fee > 201` and rerun. The unchanged checks expose the regression at 200, and the additional 201 result is also wrong. Restore `fee >= 200` afterward.

### 09 Repeat real agent trials from fresh state

1. **Understand.** One successful agent run is limited evidence. Repeat the same task from fresh state and count outcomes against the same expectations. Keep failed and incomplete attempts in the denominator. This task requires an exact decision word and actual tool calls for the requested ID; it does not score arbitrary prose.
2. **Predict.** Which case should improve when the rule changes: C1/100, C2/200 or missing C9?
3. **Run** [09_repeat_agent_trials.py](09_repeat_agent_trials.py). This makes multiple model calls: two attempts per case for both versions.

   ```bash
   uv run python snippets/b5/09_repeat_agent_trials.py
   ```

4. **Observe.** Inspect each trial and its `success frequency`. The verified comparison improved from 4/6 baseline successes to 6/6 candidate successes; C2 supplied the difference. Your runs may differ. Two attempts per case cannot establish a dependable production success rate.
5. **Try.** Set `max_turns = 1` and rerun. Inspect incomplete attempts and confirm that they remain in the denominator. A stopped run must not disappear from the score.

## Keep these boundaries clear

<details>
<summary>Scores, traces and resource measurements</summary>

- **Scope of a check:** 01/03 inspect fields; 07 judges clarity on prepared drafts. A clarity pass establishes neither source grounding nor authority. 09 scores its label-and-tool task, not the broader application contract.
- **Trace measurements:** 04 prints actual token counts and elapsed time. 05 prints selected span timing/parents; missing provider/judge usage remains unknown. Nested or overlapping span durations cannot simply be added into end-to-end time. B1 introduces cost estimation.
- **Model comparisons:** the examples retain B1–B3's `gpt-4.1-mini`. Recheck access/rates before class. Evaluate a replacement against the same cases and expectations. Current observations are recorded in [verification](VERIFICATION.md).

</details>

## Teaching and optional tools

- [36-slide deck](../../slides-md/b5-safety-observability-evaluation.md) and [Gamma text](../../slides-gamma/b5-safety-observability-evaluation.txt): the lecture follows the rule investigation through repair/repetition, then extends to actions and clarity. File numbering stays unchanged.
- [Promptfoo and DeepEval alternatives](alternatives/README.md): optional implementations of selected lessons, with separate setup/locks and [verification](alternatives/VERIFICATION.md). Choose one implementation per teaching step.
- [Larger reference runners](reference/README.md): earlier case matrices, reporting and historical evidence. The nine core files do not import them.

Labs, assessments and new notebooks remain deferred.
