# B3 · Agreed lecture scope

Module question: how can an agent manage a task requiring several observations, specialist work and a human decision?

One synthetic scenario connects the lecture: investigate C1's delay, assess its implications and prepare a customer update for review. Build from B2's established agent/tool/MCP foundation.

## 1. Multi-step autonomy · 20 minutes · slides 2–13

1. Establish the larger task and the evidence it needs.
2. Explain a prescribed sequence, then motivate conditional routing.
3. Illustrate the known conditions in ordinary Python.
4. Identify which next-step decisions may be delegated to a model.
5. Explain tool responsibilities, dependent observations and a revisable task plan.
6. Illustrate a multi-tool investigator; inspect execution and its actual draft.
7. Distinguish supported completion, missing evidence and budget exhaustion.

## 2. Orchestration and delegation · 20 minutes · slides 14–24

1. Motivate a specialist through different instructions, context and tools.
2. Explain coordinator ownership and the delegation contract.
3. Illustrate specialists called as tools.
4. Explain transferred ownership, then illustrate a handoff.
5. Map the same responsibility transfer to LlamaIndex as a compact comparison.
6. Explain sequential dependencies, independent parallel work and partial aggregation.
7. Consolidate architecture choices according to task requirements.

## 3. State and human participation · 17 minutes · slides 25–34

1. Distinguish conversation context, application task data and an interrupted run.
2. Reactivate B1's follow-up problem and illustrate session-backed history.
3. Explain findings, draft and review state using a plain dictionary; introduce disk persistence as a follow-on.
4. Establish conceptually what a checkpoint retains; use the saved-run follow-on after in-memory resumption.
5. Motivate review of the exact proposed action.
6. Explain interruption, approve/reject and resumption before SDK code.
7. Inspect both actual effects in a local demonstration outbox.

## Close · 3 minutes · slides 35–36

Reassemble the investigation, specialist work, retained state and human decision. Check ownership, evidence and stopping explanations. Bridge to enterprise APIs, databases and actions in B4.

## Teaching conventions

- Match B1/B2's concept-first explanation, small illustrations, source links and connected presenter notes.
- Plans and schematic paths are labelled as proposals; real model/tool execution is inspected separately.
- Arithmetic remains deterministic, uncertainty stays visible and synthetic rules are identified.
- Examples isolate mechanisms and do not claim a complete production shipment application.
- Lab design, durable recovery machinery, extensive retry/security implementation and full evaluation remain outside this lecture.
