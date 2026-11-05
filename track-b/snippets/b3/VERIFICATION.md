# B3 verification · 5 November 2026

After simplification, all six core scripts and four optional comparisons/follow-ons were exercised. Sixteen execution and output checks passed. The four preserved earlier reference scripts were outside this verification.

Environment: Python 3.12.2, OpenAI Agents SDK 0.20.0, LlamaIndex core 0.14.25, and the same installed dependencies previously exercised with B2. Hosted requests used the actual GPT-4.1-mini endpoint and configured dotenv credentials.

## Simplified teaching path

- The investigator has three operational tools, a shorter task instruction and visible ID/turn-limit variables. It adds no plan-recording tool or charge calculation.
- The charges specialist retains deterministic arithmetic.
- Core memory uses one in-memory session and a plain task dictionary.
- Core approval pauses, presents exact arguments, applies an actual terminal decision and resumes in memory.
- Separate follow-ons demonstrate file-backed conversation/task storage and serialization/restoration of a pending SDK run.
- Tool execution evidence and runtime limits remain visible. Long conditional returns were expanded for readability.

## Executed cases

| Scenario | Example | Result |
| --- | --- | --- |
| workflow | [01_workflow_patterns.py](01_workflow_patterns.py) | PASS |
| investigation | [02_agent_investigation.py](02_agent_investigation.py) | PASS |
| unknown | [02_agent_investigation.py](02_agent_investigation.py) | PASS |
| on_time | [02_agent_investigation.py](02_agent_investigation.py) | PASS |
| budget | [02_agent_investigation.py](02_agent_investigation.py) | PASS |
| delegation | [03_agents_as_tools.py](03_agents_as_tools.py) | PASS |
| handoff | [04_handoff.py](04_handoff.py) | PASS |
| memory | [05_memory_and_state.py](05_memory_and_state.py) | PASS |
| approve | [06_human_approval.py](06_human_approval.py) | PASS |
| reject | [06_human_approval.py](06_human_approval.py) | PASS |
| invalid_review | [06_human_approval.py](06_human_approval.py) | PASS |
| parallel | [extensions/01_parallel_specialists.py](extensions/01_parallel_specialists.py) | PASS |
| llamaindex | [extensions/02_llamaindex_handoff.py](extensions/02_llamaindex_handoff.py) | PASS |
| persist_task | [extensions/03_persist_task_state.py](extensions/03_persist_task_state.py) | PASS |
| saved_approve | [extensions/04_saved_approval.py](extensions/04_saved_approval.py) | PASS |
| saved_reject | [extensions/04_saved_approval.py](extensions/04_saved_approval.py) | PASS |

Unknown and on-time cases avoided extra investigation reads. A one-turn budget produced an incomplete stop. Specialist tools executed and final ownership matched coordinator versus handoff semantics. Conversation history retained C1 while application task data kept the findings and pending review status.

Both core and saved-run approval paths executed the exact reviewed payload once after approval and executed no action after rejection. Invalid core review input stopped with an error before any action. The saved-run cases restored their SDK checkpoint; the core cases used in-memory state.

Variants changed the two learner-editable constants in a temporary execution string; the source files remained at their default values.

## Other checks

All active B3 Python files compiled. The 36-slide deck rendered successfully and the changed slides were visually inspected. Document links and sequential core numbering passed checks. Baseline file hashes confirm that B1/B2 examples were unchanged by this task. Lab files were not edited.

These checks establish the demonstrated mechanisms and selected behaviours, not exhaustive quality for all model outputs. Persistence follow-ons recreate objects in one process with temporary storage and retain agent definitions; they do not implement service recovery, enterprise identity or duplicate-action protection.
