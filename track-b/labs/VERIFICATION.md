# B1–B3 lab verification · 5 November 2026

Both lab paths were checked with learner implementations applied only to
disposable copies. The delivered starters retain all 14 empty TODO functions
per version: 12 core functions and two optional B3 extensions.

## Executed checks

| Check | Result |
| --- | --- |
| Supplied scaffold suite | 7 tests passed, including both copies and repeat-review regressions |
| Existing PortOps suite, run from its project directory | 23 tests passed; one existing Starlette/httpx deprecation warning |
| Initial B1–B3 help from another working directory | Passed for both copies |
| Unfinished first model call | Reports TODO B1.1, exit 2, no invented reply |
| PortOps adapter | Actual HTTP GETs against existing routes, with CSV seeds in an in-memory DB |
| PortOps fixture date | Fixed at 2026-09-22: MSKU1234567 is OVERDUE with USD 1500 net; MSCU7654321 is GATED_OUT |
| Scripted model with real SDK execution | Tool observations, task JSON and actual RunState save/restore passed |
| Human review with scripted model output | Approve, reject and invalid input exercised for both copies; exact payload retained |
| Real MCP transport | Both completed copies discovered and invoked read tools over local HTTP |
| Unfinished MCP read | Actual is_error result detected; runner raised instead of printing a completed answer |
| Live GPT-4.1-mini smoke checks | B1 instruction call, B2 status/fee tool answer, B3 investigation and rejection passed for both copies |
| Local lab document links | 37 links resolved |
| Python syntax and empty TODO bodies | All starter/scaffold files parsed; 14 learner functions per version remain unimplemented |

The temporary PortOps server used the existing route/service/engine code with
an in-memory seeded database. It did not reset or modify the capstone's working
database. Live review rejected the local outbox proposal; no customer message
was sent. Scripted output was used explicitly to verify scaffold behavior,
separately from the live model smoke checks.

Two review findings were fixed: a rejected new draft cannot inherit an older
identical outbox entry's queued outcome, and MCP tool-error results cannot
silently count as a completed checkpoint. The former has a persisted
regression test; the latter was exercised through an actual MCP connection.

## Commands

From the repository root, with the lab dependencies available:

```bash
python -m unittest discover -s track-b/labs/tests -v
```

From `project-supplychain-sandbox-PortOps`, with its environment active:

```bash
python -m pytest
```

The disposable integration/live scripts and logs are local review artifacts at
`/private/tmp/maersk-b1-b3-lab-verification-20261105/`; they are not learner
solutions in the teaching pack.

## Limits and unrelated collection failures

This verifies runnable scaffolding and representative completed paths. It is
not a guarantee that a participant's implementation or every model response
meets the lesson requirements. Follow-ups with a new session, optional local
inference, coordinator and handoff extensions were not live-tested as part
of this lab check; their source mechanisms remain in the existing snippets.

An initial pytest invocation from the wider repository root also discovered
unrelated archived BFSI material and stopped on five collection errors:

- `CODEALONGS/tests/test_m0_section_1_materials.py`: missing `nbformat`.
- `CODEALONGS/tests/test_m0_section_2_materials.py`: missing `nbformat`.
- `CODEALONGS/tests/test_m0_section_3_materials.py`: missing `nbformat`.
- `CODEALONGS/tests/test_m1_model_access_materials.py`: missing `nbformat`.
- `M13-M15-OFFLINE-HARDENING-DRAFT/m15_observability_deployment/04_api_smoke_test.py`:
  its local server could not become healthy in the restricted execution environment.

These were outside the lab change. Running the actual PortOps project suite
from its documented directory passed all 23 tests.
