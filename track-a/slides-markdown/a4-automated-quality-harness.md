# A4-01 · Verifying AI-generated code with a quality harness

A quality harness executes defined checks around generated changes and returns evidence the assistant and developer can act on.

A4 connects tests, quality tools, hooks and CI into a repeatable check–repair–recheck loop.

---

# A4-02 · A4 agenda

1. Properties checked by the harness
2. Reliable executable checks
3. Hooks and timely feedback
4. The check–repair–recheck loop
5. Shared CI gates and human review

The harness supplies evidence within its defined coverage.

---

# A4-03 · A harness connects a change to an observed result

The assistant proposes an edit. A check executes against the resulting state. Its output identifies a satisfied property or a failure requiring attention.

The developer interprets that result against the specification and directs the next action.

Reliable feedback requires both a meaningful check and a dependable execution path.

---

# A4-04 · Different checks establish different properties

| Check | Property it can help establish |
| --- | --- |
| Formatter check | Source follows the configured layout |
| Lint | Selected suspicious patterns or conventions |
| Type check | Selected interface/type consistency |
| Behavioural test | A specified result for controlled inputs |
| Contract check | Data conforms at a defined boundary |

The exact coverage depends on configuration and cases.

---

# A4-05 · A running example can violate its contract

A function can execute without an exception while returning a result the caller cannot use correctly.

The harness needs a check at the boundary where that expectation matters.

**Capstone slot A4-E01:** one tiny generated change with a behavioural or caller-contract violation and the property a check should detect.

---

# A4-06 · Evidence has a coverage boundary

A passing formatter check says nothing about the intended business result. A passing normal-case test may omit a failure path.

Ask which incorrect behaviours the harness can reject and which still need additional checks or review.

Architectural consistency and requirement interpretation remain explicit developer judgments.

---

# A4-07 · The harness should follow the change's risk

Choose checks for the affected behaviour and boundary.

A local transformation may need focused tests and lint. An interface change may need caller compatibility or contract checks as well.

Reuse the repository's established tools before introducing additional setup that does not improve the evidence.

---

# A4-08 · A useful check is reproducible

A developer or assistant should be able to run the check from a known working location with the necessary inputs and configuration.

It should produce a useful diagnostic and signal failure through its process result.

**Capstone slot A4-E02:** the selected capstone check command, its configuration and one genuine failure message.

---

# A4-09 · Formatting and checking have different effects

A formatter can modify a file. A formatting check reports whether it already conforms.

Automatic changes still belong in the reviewed diff. A check used by CI should communicate failure clearly when the required formatting is absent.

The assistant needs to know whether the command only observes state or also changes it.

---

# A4-10 · Lint and behavioural tests complement one another

A lint rule can detect a selected code pattern. A behavioural test checks an expected result for a specified case.

A code change can pass one and fail the other.

**Capstone slot A4-E03:** one lint issue and one behavioural issue in the shared capstone excerpt, with separate diagnostic signals.

---

# A4-11 · Contract checks belong at the relevant boundary

For a function and caller, inspect accepted inputs, return shape and error expectations.

An isolated internal check may miss a caller's incompatible assumption. Add evidence where values cross the boundary.

Use substitutes only for unrelated dependencies, preserving the behaviour the check needs to observe.

---

# A4-12 · A deliberately faulty variant tests the check itself

Before relying on a check, show that it rejects a relevant incorrect variant for the intended reason.

Then restore the correct state and show that the check accepts it.

This distinguishes a functioning verification path from a command that merely runs successfully.

---

# A4-13 · A hook schedules a check at a supported event

The assistant's lifecycle exposes events such as a tool action before execution or after completion.

A hook can run a configured command at one of those events. The command still needs a meaningful property to check.

The event, matcher and command determine what the hook observes.

---

# A4-14 · Before-action and after-action checks have different power

A before-action check can prevent a matching action when its decision mechanism blocks it.

An after-action check sees the state after the action and can report a problem. Its failure does not automatically undo the edit.

Match the event to whether the requirement is prevention or feedback.

---

# A4-15 · The event position changes what the hook can do

**Before-action scenario:** a matching edit targets a protected fixture. The hook checks the proposed target and can reject that action through the product's supported decision mechanism.

**After-action scenario:** the source edit completes. Lint examines the changed state and reports a problem. The edit remains until explicitly corrected or reverted.

These mechanism scenarios describe ordering, not actual tool output.

---

# A4-16 · A lightweight hook keeps feedback close to the edit

Use a fast relevant check during editing. Save heavier regression or scanning work for appropriate checkpoints and CI.

Show the triggering edit, command execution, diagnostic and assistant response together.

**Capstone slot A4-E04:** a small hook configuration and feedback wrapper for the capstone demonstration's existing check.

---

# A4-17 · Protected fixtures illustrate a narrow preventive rule

A supplied pre-action hook can refuse a matching edit to a verification fixture and explain the restriction.

**Capstone slot A4-E05:** one protected-fixture attempt and the actual decision message.

Inspect the event and tool coverage before concluding which actions the rule prevents.

---

# A4-18 · A hook needs an observable verification path

Check that the configured hook loads, its event occurs, the matcher selects the action and the command executes.

If the expected feedback is absent, investigate that chain before changing application code.

An installed configuration file alone does not demonstrate a working hook.

---

# A4-19 · The assistant needs the failure and its meaning

**Assistant request**

> “Run the agreed check after this increment. If it fails, explain the failing property using the diagnostic and relevant code. Propose a focused correction. Preserve the specification and existing acceptance expectations.”

Inspect the proposed diagnosis before accepting another edit.

---

# A4-20 · Two repair proposals preserve different things

**Repair scenario:** a proposed implementation would fail the agreed R2 precedence check.

**Proposal A:** change the expected result to "delayed" for cancelled shipments with negative ETA.

**Proposal B:** correct the precedence logic and retain the agreed expected result.

Under the worked specification, B is the justified direction. A needs a new owner decision changing R2; a desire for green checks is insufficient.

---

# A4-21 · Rechecking the same expectation tests the repair

Retain the original failing case. After the correction, rerun that case and the relevant neighbouring checks.

Inspect the diff for unrelated changes and altered expectations.

**Capstone slot A4-E06:** original failure, focused repair and subsequent result for the unchanged acceptance check.

---

# A4-22 · Changing checks can hide the defect

Disabling a rule, skipping a failing test or broadening an assertion can turn the signal green without correcting behaviour.

Review application code, tests and harness configuration together.

A legitimate check correction needs evidence that the previous expectation or configuration was wrong.

---

# A4-23 · Tooling failures and application failures need different repairs

If the runner cannot import dependencies or find its configuration, establish a working check environment first.

If the check executes and rejects an observed result, inspect the application and its expected contract.

Avoid changing business logic to compensate for an unrelated setup failure.

---

# A4-24 · Repeated unresolved failures call for a new investigation

When several edits fail the same check, pause the generation loop.

Revisit the requirement, current context, plan and test setup. Ask which assumption has not been verified.

Useful progress is a better explanation supported by evidence, not simply another larger diff.

---

# A4-25 · CI provides another route to the same checks

Reuse the underlying check commands in local work and the supplied pipeline.

A change made outside the assistant's hook coverage should still encounter the relevant CI check.

**Capstone slot A4-E07:** the shared check entry point and a seeded violation detected by the pipeline.

---

# A4-26 · Check execution and merge enforcement are separate settings

A pipeline can report a failure while repository policy still permits integration.

Required checks and review rules establish which conditions must hold before merge, subject to the configured access and bypass rules.

Inspect the actual policy rather than assuming that a workflow's presence makes it mandatory.

---

# A4-27 · Current evidence supports a bounded readiness decision

Match the final diff, check results and review record to the same revision.

List unresolved risks or unexecuted checks. Explain which conditions remain before acceptance.

A green harness supports the decision within its coverage. Requirements, architectural fit and acceptable risk still need review.

---

# A4-28 · The harness can improve through observed failures

When a relevant defect escapes, ask whether an economical deterministic check could detect that class of mistake.

Add or refine the check, verify it against a faulty variant and review its effect on legitimate work.

Keep its purpose, configuration and owner understandable to the next developer.

---

# A4-29 · A4 practice: an observable feedback loop

Use the capstone's existing quality tools and a supplied change with one quality issue and one behavioural or contract issue.

Select the relevant checks, observe their failure, direct a focused repair and rerun. Configure or inspect a lightweight supported hook and compare its coverage with the supplied CI check.

Use independent faulty/recovery checkpoints. Configuration and actual outputs will populate the capstone evidence slots.

---

# A4-30 · A4 discussion: the edit already happened

**Scenario:** an after-edit hook reports a failure. The assistant says the failed hook prevented the source change.

What should the developer inspect? Which event would be appropriate for a rule that must prevent a matching edit?

Explain the difference between reporting and undoing a change.

---

# A4-31 · A4 checkpoint

You can explain what the harness checks, verify its execution path and use its feedback to direct a repair.

You can distinguish a hook's coverage, a CI result and the policy that governs integration.

A5 combines these capabilities into an independently justified PR.
