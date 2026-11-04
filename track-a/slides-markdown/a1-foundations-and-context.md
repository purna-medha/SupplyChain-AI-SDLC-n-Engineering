# A1-01 · AI development foundations and context engineering

Coding assistants can investigate, edit and execute development work. Their usefulness depends on the task, the context they receive and the evidence used to judge their results.

By the end of A1, you can prepare a small repository task, choose a suitable model and explain why the assistant's answer still needs verification.

---

# A1-02 · A1 agenda

1. AI and coding assistants
2. Features, model tiers and operating limits
3. Coding assistants across the SDLC, followed by a demonstration
4. Generated code's weaknesses and verification
5. Repository context and persistent guidance

Each section answers a practical question about using an assistant in development work.

---

# A1-03 · Generative AI produces an answer from supplied context

A language model generates a response using learned patterns and the context available in the current interaction.

A developer can ask it to explain a function, propose alternatives or draft tests. A useful response can still contain a wrong assumption about requirements or code it has not inspected.

---

# A1-04 · Training knowledge and task-time inference serve different roles

Training builds the model's learned capabilities before this task. Inference generates a response using those capabilities and the supplied context.

Reading a current file gives the assistant task evidence. It does not retrain the model or establish the owner's desired change.

A familiar-looking implementation can still belong to a different contract.

---

# A1-05 · A coding assistant connects the model to development tools

The assistant can combine a model with file search, editors, terminals and approved integrations.

The model proposes a tool action. The surrounding software executes an allowed action and returns its result. That result supplies evidence for the next decision.

An explanation of a command and an executed command are different events.

---

# A1-06 · Capabilities span the work around writing code

| Developer task | Useful assistant contribution |
| --- | --- |
| Understand code | Trace a path and cite source locations |
| Design a change | Compare approaches against constraints |
| Implement | Propose edits across relevant files |
| Verify | Draft cases and execute available checks |
| Maintain | Investigate failures and explain a diff |

The required evidence changes with the task.

---

# A1-07 · The developer owns the engineering decisions

The assistant can propose a requirement interpretation, architecture or fix. The developer decides whether it matches the intended change.

Keep consequential choices visible: what may change, which behaviour must remain, what proves completion and which actions require approval.

Understanding accepted code remains part of completing the task.

---

# A1-08 · A well-defined task produces a reviewable result

Compare two requests:

> “Improve this function.”

> “Investigate the supplied function. Explain its current behaviour, identify an ambiguous requirement and propose a small change with acceptance examples. Wait before editing.”

The second request defines the phase, expected output and stopping point.

---

# A1-09 · Assistant features address different working needs

| Feature | Working need |
| --- | --- |
| Plan mode | Investigate and agree an approach before editing |
| Repository instructions | Retain shared project guidance |
| Skills | Apply a reusable method |
| MCP integration | Access a connected capability or source |
| Hooks | Trigger checks at supported events |
| Agents or subagents | Delegate bounded work |

Names and supported behaviour vary between products.

---

# A1-10 · Planning, skills and subagents have different jobs

For the cancellation change:

- Planning proposes the affected function, caller and checks before edits.
- A skill retains the repeatable method for reviewing precedence and compatibility.
- A subagent can inspect the caller and return a bounded report to the implementation owner.

The method, the execution role and the implementation plan are separate artifacts.

---

# A1-11 · Context capacity and usage allowance are separate limits

**Context capacity** limits how much material the model can consider in an interaction.

**Usage allowance** limits how much service the account can consume over its plan's metering period.

A session can have context space remaining while the account reaches a usage limit. The two problems require different responses.

---

# A1-12 · Tokens measure pieces of the model's working material

A token is a unit used to represent text to the model. It can be a word, part of a word or punctuation, depending on the tokenizer.

Code, instructions, conversation and tool results all consume tokens when included. Lines of code and file size are only rough proxies.

The selected model's window limits the working material for an interaction.

---

# A1-13 · A large repository does not need to fit into one window

The active context includes instructions, conversation, selected source and tool results.

Even with a 1M-token window where available, loading every file can obscure the relevant contract. Search first, trace the affected path and bring in the evidence needed for the current decision.

Repository size and active context size are different quantities.

---

# A1-14 · Context grows as the investigation proceeds

Consider a session that reads the function, its caller and a long failure log. Later requests may also carry earlier messages and tool results.

The newest prompt can be short while the working context is large. Unrelated log output can compete with the one compatibility rule that matters.

Inspect the active context and retain only useful evidence.

---

# A1-15 · Compaction retains a summary, not every detail

Compaction replaces some accumulated discussion with a shorter summary so work can continue within context limits.

A summary can omit an exact rule or an unresolved question. Preserve the cancellation precedence, compatibility contract and current check state in explicit task artifacts.

After compaction, re-read a critical definition before relying on it.

---

# A1-16 · Usage information belongs in the working setup

Before substantial work, inspect:

- The selected model and available alternatives
- Account usage and any model-specific allowance
- The displayed renewal or reset information
- Whether usage is shared with other sessions

Record the actual account information rather than relying on remembered plan limits.

---

# A1-17 · Continuing a session and starting fresh require different preparation

Continue when the current task history remains useful. Start fresh when a clear handover can establish a cleaner task boundary.

A new session needs the specification, current files, check state and next action. Persistent repository guidance supplies project conventions rather than the whole previous conversation.

Inspect live files even when the handover looks complete.

---

# A1-18 · Model choice includes quality and correction effort

| Working tier | Typical starting point | Evidence to inspect |
| --- | --- | --- |
| Fast | Small, well-bounded transformations | Did it preserve the contract? |
| Default | Routine implementation and investigation | Did it find and use the relevant evidence? |
| Deep | Difficult diagnosis or cross-cutting design | Did the additional reasoning improve the decision? |

Choose against acceptance criteria, then consider latency, cost and rework.

---

# A1-19 · Requirements and design become explicit artifacts

For requirements, ask the assistant to identify ambiguity and propose acceptance examples.

For design, ask it to inspect existing mechanisms and compare alternatives against architecture, compatibility and testability.

The developer resolves important choices and records a specification and plan that can guide implementation.

---

# A1-20 · Implementation and testing form a feedback loop

The assistant implements a bounded increment and executes relevant checks. The developer compares the diff and observed behaviour with the specification.

Tests start with the first increment. A failing check becomes evidence for the next decision, rather than a reason to keep generating unrelated fixes.

---

# A1-21 · Review, delivery and maintenance depend on evidence

Review compares intended behaviour with the actual change and its checks.

Delivery adds evidence for the identified version in its target environment.

Maintenance begins with a reproducible symptom and investigates the cause.

AI can help at each stage. Passing checks, human approval and permission to release remain separate conditions.

---

# A1-22 · The shared case: a cancellation can override ETA status

**Classroom baseline:** a negative numeric ETA produces "delayed". Zero or a positive ETA produces "on_time".

**New request:** "Support cancelled shipments without changing existing calls."

The request leaves a decision open: should cancellation override the ETA result? Resolving that question precedes implementation.

These are synthetic teaching rules.

---

# A1-23 · Demonstration: the complete development loop

Follow one small change through:

1. Brief and repository investigation
2. Acceptance examples and design choice
3. Reviewed implementation plan
4. Code change and executed checks
5. Focused diff, review and readiness decision

At every step, identify what the assistant did and what the developer accepted.

---

# A1-24 · Capstone demonstration space: baseline and change

> **Capstone slot A1-E01**
>
> Select one bounded development task from the client capstone. Show the relevant source path, its caller or dependency, the requested change and a compatibility expectation.

Use only the excerpts needed to understand the decision. The complete project can be larger; there is no standalone snippet or line-count requirement.

---

# A1-25 · Capstone demonstration space: the evidence chain

> **Capstone slot A1-E02**
>
> For that same capstone task, capture the assistant request and supplied context, proposed change, actual check results and developer review decision.

Connect intent to the observed result. Label recorded evidence and unexecuted checks accurately.

---

# A1-26 · One change produces several useful records

| Record | Cancellation example |
| --- | --- |
| Intent | Represent a cancelled shipment accurately |
| Specification | Cancellation wins; omitted flag preserves ETA behaviour |
| Plan | Review function/caller, write cases, implement, check compatibility |
| Evidence | Diff and actual results, once execution is available |

Each record answers a different question about the same change.

---

# A1-27 · Plausible code can implement the wrong interpretation

A request can leave a rule unresolved. The assistant may choose a reasonable interpretation and implement it consistently.

The code can run and its generated tests can pass while both disagree with the intended behaviour.

Acceptance examples make the requirement independently inspectable.

---

# A1-28 · Local correctness can hide architectural damage

A helper can produce the right answer while bypassing an existing shared rule or changing a caller's expectations.

Before editing, identify which layer owns the decision, which interface must remain stable and which existing mechanism should be reused.

Planning depth should match the change's reach and risk.

---

# A1-29 · A generated test can preserve the same mistake

A test needs a defensible expected result and an assertion that would fail on relevant incorrect behaviour.

Ask:

- Which requirement establishes the expected result?
- Which wrong implementation would this test reject?
- Did a substitute hide the behaviour being tested?

---

# A1-30 · A completion claim needs observable support

“Implemented and tested” should lead to inspectable evidence:

- What changed in the diff
- Which check actually ran
- What result it produced
- Which requirement it establishes
- What remains untested or unresolved

An explanation helps interpret evidence but cannot replace its execution.

---

# A1-31 · Planning creates useful control points

Agree the behaviour before choosing a design. Review the plan before broad edits. Inspect an increment before delegating more work.

These control points make corrections cheaper because the developer can locate where understanding diverged.

A2 turns this principle into concrete requests, artifacts and a test-first implementation sequence.

---

# A1-32 · Repository investigation should produce a source-backed map

Ask the assistant to locate the entry point, affected function, caller and relevant tests. Have it explain the path with file locations.

Verify one claim by inspecting the cited source or running the relevant path.

Separate an observed dependency from an assumption based on a familiar project layout.

---

# A1-33 · The context package supports the current decision

Useful context includes the task, relevant source, authoritative rules, acceptance examples and constraints.

Keep stable project guidance separate from the specification for one change.

Refresh context when source or decisions change. An earlier chat summary can be useful orientation while still containing stale facts.

---

# A1-34 · Context failures have different corrections

| Failure | Example | Useful response |
| --- | --- | --- |
| Missing | The assistant never sees the caller | Inspect the caller contract |
| Distracting | Unrelated files dominate the discussion | Refocus on the affected path |
| Stale | An old interface appears in the chat | Read the current definition |
| Conflicting | Two documents state different rules | Resolve authority with the owner |

The correction should address the source of confusion.

---

# A1-35 · Persistent instructions retain verified project guidance

AGENTS.md, CLAUDE.md or the selected assistant's equivalent can record architecture, commands, conventions and recurring mistakes.

Keep the guidance concise and check commands against actual execution. Shared repository rules and personal preferences may have different scopes.

Verify which files the selected product loads and how it resolves applicable instructions.

---

# A1-36 · A small repository guidance example

**Purpose:** the classroom helper classifies shipment status.

**Architecture:** one decision function owns the rule; the caller passes inputs and uses the returned label.

**Conventions:** preserve existing caller behaviour and keep requirements separate from tool configuration.

**Verification:** check normal, precedence and compatibility cases; report what ran and what remains unverified.

---

# A1-37 · Connected evidence can change a development decision

An issue, API contract or approved schema may contain facts absent from the repository.

Use an approved read-only connection to retrieve the relevant fact. Inspect the source, version and meaning before updating a specification or plan.

MCP standardises access to supported capabilities. The returned content still needs interpretation and verification.

---

# A1-38 · A connected lookup needs an engineering consequence

**Illustrative source:** the approved classroom contract lists "delayed", "on_time" and "cancelled" as accepted status labels.

**Question:** may the assistant return a new label such as "late"?

The contract rules it out for this change. Record that constraint in the specification and identify the source. A successful lookup alone would not establish this decision.

---

# A1-39 · A1 practice: compare two context packages

Use a bounded task from the selected capstone and equivalent starting checkpoints.

Compare the assistant's interpretation with incomplete context and with the relevant requirement, source and caller context. Identify one unsupported assumption, prepare a context package and explain a model choice.

The lab should change a rule or boundary from the instructor demonstration. The written cancellation case is an optional discussion fallback.

---

# A1-40 · A1 discussion: which limit applies?

**Scenario:** the repository is larger than the model's window, the current task concerns one function and caller, and the account still has usage available.

What should the developer do next, and what evidence should the assistant inspect?

Explain why changing subscription allowance would or would not address this problem.

---

# A1-41 · A1 checkpoint

You can now explain the assistant's tool-mediated workflow, distinguish context from usage limits and prepare a source-backed context package.

Bring an initial specification, acceptance examples, repository guidance and a justified model choice into A2.

A2 develops this preparation into a reviewed plan and tested implementation.
