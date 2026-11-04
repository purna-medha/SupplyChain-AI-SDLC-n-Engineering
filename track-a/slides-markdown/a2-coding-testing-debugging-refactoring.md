# A2-01 · AI-powered coding, testing, debugging and refactoring

A prepared context package becomes useful when it guides an implementation the developer can inspect and verify.

A2 develops the working sequence: complete the specification, challenge the plan, implement through tests, investigate a defect and preserve behaviour during refactoring.

---

# A2-02 · A2 agenda

1. Complete the specification and compare designs
2. Challenge the plan and direct implementation
3. Lead implementation with TDD
4. Diagnose defects through experiments
5. Refactor and preserve continuity

The specification remains the authority for expected behaviour throughout these activities.

---

# A2-03 · An incomplete request delegates hidden decisions

“Add support for missing input” leaves important questions unanswered.

Does missing input mean an omitted argument, an empty value or an unavailable source? Should the function reject it, return a new result or preserve an existing default?

An assistant can choose a coherent interpretation that the owner never intended.

---

# A2-04 · Requirements exploration is a useful assistant task

**Assistant request**

> “Read the request and supplied function/caller. Identify ambiguous behaviour, propose acceptance examples and distinguish facts from assumptions. Do not edit code. Flag decisions that require the requirement owner's answer.”

Review the proposed questions before accepting the assistant's interpretation.

---

# A2-05 · Worked intent record: cancellation support

**Problem:** a cancelled shipment currently receives an ETA-based label.

**Outcome:** represent cancellation while preserving existing callers.

**Affected boundary:** the decision function and its caller.

**Constraint:** retain the existing string-label interface.

**Owner decision:** cancellation overrides ETA status. Missing or invalid ETA support is outside this change.

---

# A2-06 · The specification describes observable behaviour

| Specification element | What it establishes |
| --- | --- |
| Outcome and scope | The change and its non-goals |
| Input/output contract | Accepted values, results and errors |
| Compatibility | Existing behaviour that must remain |
| Constraints | Relevant architectural or access boundaries |
| Acceptance examples | Observable evidence of success |

Open questions need owners and a blocking/non-blocking status.

---

# A2-07 · Worked specification: numbered behaviour

- **R1:** With the cancellation flag false or omitted, negative numeric ETA yields "delayed"; zero/positive ETA yields "on_time".
- **R2:** With the flag true, every supported numeric ETA yields "cancelled".
- **R3:** The caller still receives one string label. Existing calls need no new argument.
- **R4:** Keep one owner for status decisions; preserve existing input/error handling. No new labels or unrelated refactor.

These requirements define what implementation must establish.

---

# A2-08 · Acceptance examples reveal boundary decisions

**Expected outcomes from the worked specification, not execution results:**

| ETA | Cancellation | Expected label | Requirement |
| --- | --- | --- | --- |
| -2 | omitted | delayed | R1, R3 |
| 0 | false | on_time | R1 |
| 4 | false | on_time | R1 |
| -2 | true | cancelled | R2 |
| 4 | true | cancelled | R2 |

The negative-ETA cancellation case distinguishes competing precedence rules.

---

# A2-09 · Design alternatives need repository evidence

Ask the assistant to compare a small extension with a broader redesign.

Inspect where the rule currently lives, which callers depend on it and what tests can establish compatibility. Compare change surface, clarity and maintenance cost.

Choose an approach that meets the requirement and preserves the relevant architectural boundaries.

---

# A2-10 · Two designs, one explicit compatibility decision

**Option A:** extend the existing decision function with an optional flag and preserve its string result.

**Option B:** return a new object and duplicate status logic in the caller.

Option A fits R3–R4 with a smaller change surface. Option B could serve a different requirement but needs justification and a revised interface contract.

Preference becomes a decision when checked against requirements.

---

# A2-11 · Specification completeness has a practical test

Give the specification and relevant context to a fresh reader.

Can they explain what must change, what must remain, how errors behave and what evidence establishes completion?

If they must invent a consequential requirement, resolve the gap before implementation. The specification need not prescribe every internal statement.

---

# A2-12 · A plan connects requirements to changes and checks

The assistant's plan should identify affected files, dependencies, ordered increments and acceptance evidence.

Each increment should have an observable payoff and a check. Risky assumptions deserve early investigation.

A plan that says only “implement, test, review” leaves the important engineering decisions unexplained.

---

# A2-13 · Worked plan: requirement, increment and proof

| Increment | Requirement | Planned evidence |
| --- | --- | --- |
| Inspect function and caller | R3–R4 | Confirm one rule owner and current interface |
| Add precedence case first | R2 | Intended failing check for negative ETA plus cancellation |
| Extend the existing function | R1–R2 | New case and baseline cases pass |
| Exercise omitted flag through caller | R3 | Old call form retains its result |

These are planned checks; none is reported as executed.

---

# A2-14 · Plan review challenges the assistant's assumptions

**Assistant request**

> “Propose the smallest approach consistent with the specification. Name affected files, existing mechanisms to reuse, risks and checks. Explain rejected alternatives and identify unverified assumptions. Wait for review before implementation.”

Check the cited mechanisms and the proposed order against the source.

---

# A2-15 · An implementation assignment establishes boundaries

Give the assistant:

- The increment and authoritative specification
- Relevant code, caller and test context
- Constraints and permitted implementation choices
- Expected deliverables and checks
- Conditions for stopping or asking a question

Reference stable artifacts rather than restating conflicting versions in several prompts.

---

# A2-16 · A complete bounded assignment for this change

**Assistant request**

> “Use R1–R4 and the acceptance table. Inspect the existing function and caller, then propose the smallest implementation plan. Preserve the string result and old call form. Write the negative-ETA cancellation case before implementation. Explain its failure, make the focused correction and rerun relevant cases. Stop for any requirement conflict. Report the diff, actual checks and limitations.”

---

# A2-17 · Small increments make course correction specific

After an increment, inspect the diff and run its focused checks before authorising more work.

If the result deviates, identify whether the issue concerns a requirement, missing context, a flawed plan or incorrect code.

Resolve the source of the mismatch, then repeat the relevant check.

---

# A2-18 · The correction depends on where understanding diverged

| Mismatch | Appropriate next action |
| --- | --- |
| Cancellation precedence is undecided | Obtain the owner decision |
| The caller was never inspected | Supply or investigate its contract |
| Plan duplicates the rule | Revise ownership and implementation approach |
| Code disagrees with R2 | Correct implementation, preserving R2's check |

“Try again” does not identify which problem needs repair.

---

# A2-19 · Rejection and recovery preserve useful work

A proposed change can fail the specification even when it is well written.

Explain the violated constraint, isolate the unsuitable increment and preserve unrelated accepted work. Inspect the actual working state before continuing.

**Capstone slot A2-E02:** one small rejected diff and the evidence-based correction request.

---

# A2-20 · TDD puts the behavioural target before implementation

The developer agrees expected behaviour, directs the assistant to write a meaningful test and observes the intended failure.

Only then does implementation attempt to satisfy that expectation.

The sequence creates a check that can challenge the generated code rather than simply describe what it already does.

---

# A2-21 · Test selection follows the boundary being checked

| Boundary | Suitable check |
| --- | --- |
| Local decision rule | Focused unit test |
| Function and caller contract | Small integration check |
| User-observable result | Acceptance observation |

Use controlled inputs. Substitute unrelated dependencies without replacing the behaviour the test is supposed to exercise.

---

# A2-22 · Red means an intended behavioural failure

**Assistant request**

> “Write a test for the agreed boundary case before implementation. Run it and show why it fails. Stop if setup fails or the failure is unrelated to the expected behaviour.”

**Capstone slot A2-E03:** requirement-linked test and the actual intended failing result.

---

# A2-23 · Green and refactor preserve the agreed expectation

Authorise the smallest implementation that satisfies the failing case. Run it, inspect the diff and repeat relevant existing checks.

Refactoring can then improve internal structure while preserving the established contract.

**Capstone slot A2-E04:** the minimal implementation diff and actual passing result for A2-E03.

---

# A2-24 · A passing test can still be weak evidence

Ask which wrong implementation would pass the test.

Warning signs include checking only successful execution, accepting any non-empty result, copying the faulty algorithm and mocking the function under test.

**Capstone slot A2-E05:** a weak assertion and a stronger requirement-based assertion.

---

# A2-25 · Verification extends beyond the new assertion

Run nearby regression checks and observe the relevant caller behaviour.

Report which requirement each result supports, which version was checked and what remains untested.

A fresh reviewer can challenge omitted cases, but independence still depends on checking assumptions against requirements and evidence.

---

# A2-26 · A defect report supplies a symptom before a cause

Record expected behaviour, actual behaviour, input, environment and current revision.

Ask the assistant to establish the smallest reproducible case before proposing a fix.

A message saying “this fails intermittently” does not yet identify which path, condition or component causes the problem.

---

# A2-27 · Competing hypotheses make the investigation testable

| Hypothesis | Evidence that could discriminate |
| --- | --- |
| A decision rule is wrong | Failure persists with a direct local call |
| A caller supplies the wrong value | Local call passes but caller path fails |
| Old state remains in use | Behaviour changes after controlled state refresh |

Select experiments by what they can rule out.

---

# A2-28 · Predictions turn a tool run into an experiment

**Assistant request**

> “List plausible causes and the evidence for each. Propose one small experiment that distinguishes them. State the expected result under each hypothesis. Do not change application behaviour yet.”

Compare the actual observation with the predictions before choosing the next step.

---

# A2-29 · A debugging experiment separates rule and caller defects

**Reported symptom:** a cancelled shipment with negative ETA appears as "delayed."

| Hypothesis | Discriminating observation |
| --- | --- |
| Core precedence is wrong | A direct call with cancellation true also disagrees with R2 |
| Caller loses the flag | Direct call agrees with R2; caller path disagrees |

Run the smallest comparison before deciding where to edit. These are predictions, not observed results.

---

# A2-30 · The demonstrated cause supports a narrow fix

Explain how the input reaches the faulty decision and produces the symptom.

Turn the reproducer into a regression test, inspect its intended failure and compare plausible fixes for side effects.

**Capstone slot A2-E06:** minimal reproducer, discriminating result and the narrow corrective diff.

---

# A2-31 · A successful fix leaves reusable evidence

Repeat the reproducer and neighbouring checks. Retain the failure, experiment, correction and observed result.

Explain which earlier hypothesis the evidence contradicted and why the accepted fix addresses the cause.

The maintenance record should allow a peer to distinguish a demonstrated diagnosis from the assistant's initial guess.

---

# A2-32 · A refactor needs an explicit behaviour boundary

Name the observable outputs, error behaviour, interfaces and compatibility expectations that must remain unchanged.

Ask the assistant to improve one maintainability issue within that boundary.

If existing behaviour is unclear, add characterization checks before changing its structure.

---

# A2-33 · Refactoring requests should constrain scope

**Assistant request**

> “Propose a small refactor of the supplied function and caller. Preserve the listed outputs, interface and compatibility cases. Explain the benefit before editing. Keep unrelated cleanup separate and run the preservation checks afterward.”

Review the proposed transformation as well as the resulting code.

---

# A2-34 · A diff separates a fix from a refactor

For a fix, ask which expected behaviour changes from incorrect to correct.

For a refactor, ask which behaviour remains invariant and what structural improvement results.

**Capstone slot A2-E07:** separate small fix and refactor diffs with their corresponding checks.

---

# A2-35 · A handover preserves the task state

A useful handover records:

- Current checkpoint and relevant files
- Agreed decisions and completed work
- Checks actually executed and their outcomes
- Unresolved questions or limitations
- The next bounded action

It distinguishes verified state from planned work.

---

# A2-36 · Worked handover after planning

**State:** cancellation intent, R1–R4 and the acceptance table are agreed. Implementation is not yet authorised.

**Decision:** extend the current rule owner; preserve string output and omitted-flag calls.

**Checks:** precedence and caller cases are planned, not run.

**Next action:** inspect the supplied source, validate the plan and write R2's failing case. Stop if the actual caller contract contradicts R3.

---

# A2-37 · A fresh session verifies before continuing

**Assistant request**

> “Read the handover and inspect the current files. Confirm the completed work and remaining check. Identify any mismatch before implementing the next bounded action.”

Use a separate session or peer to test whether the recorded state is understandable and current.

---

# A2-38 · A2 practice: one meaningful change

Start from the capstone's lab checkpoint and a request with a meaningful input, rule or compatibility difference from the demonstration.

Produce the specification, reviewed plan and bounded assistant assignment. Use test-first implementation, investigate one unsuccessful attempt and prepare a handover.

The external cancellation-code scenario is a written preparation exercise; the actual lab uses the selected capstone and its source, checks and recovery checkpoint.

---

# A2-39 · A2 discussion: the assistant changed the test

**Scenario:** a new test fails. The assistant changes its expected result and reports that all checks now pass.

What evidence would justify accepting that change? What would make it an attempt to redefine success?

Explain which artifact should resolve the disagreement.

---

# A2-40 · A2 checkpoint

You can prepare an implementation-ready specification, challenge a plan, direct a red–green cycle and investigate a defect through evidence.

Carry the understood diff, checks and handover into A3.

A3 makes the work reusable and reviewable by teammates who did not participate in the original assistant session.
