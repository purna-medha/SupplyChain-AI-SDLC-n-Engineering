# A3-01 · Team development with coding agents

An AI-assisted change becomes team work when another developer can understand its intent, inspect its evidence and continue it safely.

A3 develops isolation, reusable skills, focused PRs, review and current-revision evidence.

---

# A3-02 · A3 agenda

1. Isolated work and execution scope
2. Reusable skills and their evaluation
3. Focused changes and PR context
4. AI-assisted review and validated findings
5. CI evidence and transferable handover

The team needs reliable artifacts even when it uses different assistant sessions.

---

# A3-03 · Isolation gives each task a clear working state

A branch identifies a line of development. A worktree supplies another checkout where a separate session can work.

Use isolation appropriate to the task and preserve unrelated changes already present.

Separate checkouts reduce file collisions, while shared interfaces and integration decisions still need coordination.

---

# A3-04 · Execution scope follows the task's dependencies

| Scope | Useful when |
| --- | --- |
| Current session | Existing context remains relevant |
| Fresh session | A handover can establish a cleaner task boundary |
| Scoped subagent | A bounded investigation has a clear returned artifact |
| Independent worktree session | Work can proceed with isolated files and agreed interfaces |

The choice includes review and coordination effort.

---

# A3-05 · A delegated task needs an input and output contract

**Assistant request**

> “Inspect the supplied change for compatibility issues. Use the specification and caller context. Report source-backed findings and missing evidence. Do not edit files. Return a concise result for the implementation owner.”

State tool limits and who reviews the result.

---

# A3-06 · Shared changes need sequential decisions

When two tasks change the same file or contract, establish the order and ownership before both proceed.

If work conflicts, inspect both intents and the actual diff before choosing a resolution. Preserve accepted unrelated work.

**Capstone slot A3-E01:** a small overlapping change and the decision needed to resolve it.

---

# A3-07 · Parallel output has a review cost

Two sessions can produce more changes than one developer can meaningfully inspect.

Before parallel work, ask whether tasks are independent, interfaces are agreed and each result has a focused check.

Keep tightly coupled work sequential when coordination would cost more than the waiting it avoids.

---

# A3-08 · Reusable knowledge belongs in different artifacts

| Artifact | What it retains |
| --- | --- |
| Repository instructions | Stable project guidance |
| Specification | One change's intended behaviour |
| Skill | A repeatable working method |
| Agent definition | A bounded execution role |
| Hook or CI check | An executable rule or check |

A plugin can package capabilities for distribution.

---

# A3-09 · A useful skill captures a method already understood

Choose a method from A2, such as evidence-led debugging or test-first implementation.

State when it applies, which inputs it needs, what decisions it preserves, its steps, expected outputs and exceptions.

**Capstone slot A3-E02:** a small skill artifact for the selected assistant, with trigger and method visible.

---

# A3-10 · Worked skill method: review a bounded change

**Trigger:** a request to review a small behavioural change.

**Inputs:** specification, proposed plan/diff and available check evidence.

**Method:** identify requirements; compare behaviour and caller compatibility; distinguish demonstrated defects from questions; request missing evidence; return findings with impact and requirement references.

**Exception:** stop and ask for the missing specification. No approval, deployment or unrelated edits.

This is the method text; product packaging remains a separate artifact.

---

# A3-11 · Invocation must result in applied work

A saved skill file establishes availability only when the assistant can discover or explicitly invoke it as supported.

Inspect whether the resulting work follows the method and supplies its required evidence.

Separate failure to load the skill from failure of the loaded procedure to guide the task.

---

# A3-12 · Three small cases can reveal useful differences

Use a normal task, a relevant boundary case and an exception or out-of-scope request.

Record expected outcomes before the run. Evaluate the initial skill, revise it and repeat the same cases from equivalent starting states.

Compare discovery, substantive results, evidence and scope handling, including regressions.

---

# A3-13 · Worked evaluation cases for the review method

| Input case | Expected method behaviour |
| --- | --- |
| Proposed plan gives ETA priority over cancellation | Cite conflict with R2 and explain the consequence |
| Plan preserves precedence but omits caller verification | Request R3 evidence, without claiming a demonstrated defect |
| Request asks the reviewer to deploy the change | Stay within review scope and state the missing authorisation |

These are expected outcomes. Baseline and revised observations are recorded only after actual use.

---

# A3-14 · Peer transfer exposes hidden assumptions

Give a peer the artifact, required inputs and one case without narrating the previous chat.

Inspect whether they can invoke the method and interpret its evidence. Correct missing context revealed by the transfer.

Retain an owner, version, review rules and reevaluation triggers alongside the results.

---

# A3-15 · A focused PR explains one coherent change

A reviewer needs the problem, intended behaviour, changed boundary and evidence.

Keep unrelated cleanup or dependency changes separate when they do not support the task.

The PR should remain understandable to a teammate who never saw the assistant conversation.

---

# A3-16 · An assistant can draft the PR, but claims need checking

**Assistant request**

> “Draft a PR description from the specification, final diff and actual check results. Explain behaviour, validation, risks, limitations and rollback. Label checks not run. Do not claim approval or deployment.”

Verify the draft against the current files and recorded execution.

---

# A3-17 · Worked PR draft with an honest validation state

**Intent:** add cancellation precedence while preserving existing callers.

**Scope:** R1–R4 and the optional-flag change. No new status labels or unrelated cleanup.

**Validation:** acceptance cases are defined; execution evidence is not yet attached.

**Risk/recovery:** verify caller compatibility; retain the previous version for code recovery.

**Decision:** hold for implementation evidence and human review. This illustrative draft does not claim a completed PR.

---

# A3-18 · Requirement-to-evidence links support review

| Requirement | Where the change implements it | Evidence needed |
| --- | --- | --- |
| New behaviour | Affected function or decision | Focused behavioural check |
| Compatibility | Caller boundary | Existing-call or integration check |
| Failure handling | Validation or error boundary | Negative-case check |

Use actual references once the capstone excerpt is supplied.

---

# A3-19 · The diff is part of the explanation

Inspect changed source, tests and configuration together.

Ask whether each change supports the specification, whether expectations weakened and whether generated noise hides the important edit.

**Capstone slot A3-E03:** a focused capstone diff and an unrelated edit that should remain outside the PR.

---

# A3-20 · Rollback describes a recovery decision

Identify a known-good checkpoint and the condition that would make the change unacceptable.

Explain how code recovery differs from recovery of data or external effects when those exist.

For the capstone excerpt, a prior code version and repeatable checks are sufficient to discuss the principle.

---

# A3-21 · Review asks whether the change deserves acceptance

Compare the specification and plan with the actual implementation, caller behaviour, tests and configuration.

AI can propose issues across correctness, compatibility and unintended changes. A finding becomes useful when it states impact and evidence that a reviewer can inspect.

Human judgment establishes acceptable intent and risk.

---

# A3-22 · A review request should demand evidence

**Assistant request**

> “Review this diff against the specification and caller contract. For each substantive finding, give the location, violated expectation, impact and evidence. Separate confirmed defects from questions. Do not edit or approve the PR.”

Check the assistant's highest-impact claim before acting on it.

---

# A3-23 · Two written findings, two different decisions

**Finding A:** “The proposed plan gives the ETA result priority over cancellation, so negative ETA can override the new status.” This conflicts with R2 and needs correction.

**Finding B:** “Every existing caller must pass the new flag.” R3 explicitly permits omission. The claim needs source evidence before acceptance.

These are findings about a proposed plan and contract, not observations of executed code.

---

# A3-24 · A convincing finding can still be wrong

Inspect the cited code, requirement and execution path.

Reproduce a claimed behavioural issue when practical. Accept a justified finding, reject an unsupported claim or record the evidence still needed.

**Capstone slot A3-E04:** one valid finding and one plausible finding contradicted by the actual contract.

---

# A3-25 · Corrections need a new check and a reviewed diff

A justified finding changes the working state.

Ask the assistant for a focused correction, inspect what changed and rerun affected checks. Revisit nearby assumptions when the correction crosses an interface.

Resolve the finding using the corrected version's evidence rather than the earlier pipeline result.

---

# A3-26 · A peer should challenge a consequential assumption

Have the reviewer choose one assumption that affects behaviour or compatibility.

Ask what source establishes it and which check would expose its violation.

The exercise succeeds when the team either supports the assumption with evidence or corrects the missing decision.

---

# A3-27 · Current-revision evidence matters

An earlier passing pipeline does not describe a later edit automatically.

Before acceptance, match the diff, test results and review record to the same current revision.

**Capstone slot A3-E05:** a simple revision/evidence timeline with one stale success and one pending check.

---

# A3-28 · CI failures need interpretation before correction

Give the assistant the failing step, relevant log, revision and local comparison.

Ask whether the evidence points to application behaviour, test setup, dependency/environment differences or policy failure.

Make a correction justified by that diagnosis and repeat the relevant check.

---

# A3-29 · Passing checks, approval and merge permission differ

Checks report properties of a tested revision.

A reviewer decides whether the change and remaining risk are acceptable.

Repository rules determine which conditions permit integration.

A workflow that runs checks needs appropriate required-check or merge-rule configuration to enforce them.

---

# A3-30 · Handover supports the next person, not only the next model

Record the accepted decisions, current files, actual check outcomes, unresolved conditions and next action.

The receiver should inspect live state before continuing. Mark unexecuted checks and distinguish planned work from completed work.

Use the same discipline for a teammate, a fresh assistant session or a delegated investigation.

---

# A3-31 · Repeated findings can improve shared practice

A recurring project-specific mistake may belong in repository guidance. A repeatable investigation method may belong in a skill.

A rule that needs dependable execution may need a hook or CI check.

Choose the artifact according to the problem and maintain it through review.

---

# A3-32 · A3 practice: a reviewable team handoff

Use an isolated capstone change, its requirement, current diff and check evidence.

Apply the review method, prepare a focused PR and exchange a substantive finding with a peer. Validate the finding, correct justified issues and transfer the handover or reusable method into a fresh session.

Keep the lab change different from the instructor's reviewed example; provide an independent checkpoint if earlier work is unfinished.

---

# A3-33 · A3 discussion: the review sounds authoritative

**Scenario:** the assistant labels a change a compatibility defect, but the cited caller uses a different contract version.

What should the developer inspect before editing? How should the finding be recorded if it remains unverified?

Explain why confident wording does not establish impact.

---

# A3-34 · A3 checkpoint

You can isolate work, apply and evaluate a reusable skill, prepare a focused PR and validate review findings.

The next step is to make relevant quality feedback repeatable through an automated harness.

A4 develops the checks and triggering mechanisms while preserving human review of requirements and architecture.
