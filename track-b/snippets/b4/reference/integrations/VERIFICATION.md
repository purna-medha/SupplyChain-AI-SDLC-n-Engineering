# B4 integration-reference verification · 6 November 2026

Historical record for the prior API-focused examples retained in this folder. It does not verify the [current core](../../README.md). Statements below describe that earlier version.

This record covers the revised [seven short examples](README.md), their [small HTTP source](service.py), the [34-slide deck](../../../../slides-md/b4-enterprise-data.md) and [module outline](../../../../B4-OUTLINE.md). They teach the mechanisms independently; they do not claim a single integrated production workflow.

## Environment

`uv sync --locked` passed: 114 packages resolved and 108 installed packages audited. Dependencies and lockfile were unchanged. B4 now uses the same shared environment as B1–B3/B5 rather than a separate later-module environment.

Verified installed versions: Python 3.12, SQLite 3.51.1, openai-agents 0.20.0, openai 2.54.0, llama-index-core 0.14.25 and llama-index-llms-openai 0.8.3. Model examples used actual `gpt-4.1-mini` access, `load_dotenv()` and `OPEN_AI_KEY`. No key was printed or embedded. Model defaults were retained; these observations are not reliability estimates or guaranteed future outputs.

All eight core/support files parsed. The seven numbered examples contain 22–66 lines; service.py has 50 lines. No teaching helper is imported. The HTTP examples use a real separate process on `127.0.0.1:8766`. SQLite databases are real, disposable and in memory. The async database tools keep each toy SQLite connection on its owning thread; they are not production async database drivers.

## Offline and direct-source operations

| Example/check | Observed result |
| --- | --- |
| 02 · Parameterized read | C1 returned ID, fee 100 and USD, without its private note |
| 02 · SQL-looking requested ID | Returned unavailable, not all records |
| 03 · Caller A scope | C1 returned fee/source/snapshot; C2/C9 returned only unavailable |
| Temporary removal of only owner scope | C2 became readable by A despite parameter binding |
| 03 · Attempted DELETE under query-only | Write rejected; both original records remained |
| 07 · First insert, same-payload retry, changed-payload retry | created, reused, conflict, with one final row |

The mutation and blocked-write probes ran in temporary verification code, not in the distributed teaching files. They establish the contrast shown in the slides. Row limits do not establish query-work limits. The source-unavailable/timeout mappings do not turn absence into a zero fee.

## Real HTTP service checks

The service started successfully as a loopback-only process. Seven direct requests verified status and body:

| Request fixture | Observed status/result |
| --- | --- |
| A requests C1 | 200, fee 100, USD, training-api, supplied snapshot |
| A requests C2 | 404, unavailable, no fee |
| A requests C9 | 404, same public unavailable result |
| B requests C2 | 200, fee 200 |
| B requests C1 | 404, unavailable |
| Invalid token | 401, unauthenticated |
| Malformed ID | 400, invalid_request |

No response exposed the owner/private-note fields. 01 also ran directly against the actual source; its denied and missing variations both printed unavailable/404. Server console audit entries recorded caller fixture, ID and HTTP status without printing the demo token or fee. These logs are not protected durable audit storage, and a denial can still require an internal ownership lookup.

The verification service was stopped after its successful/denied checks, and loopback port 8766 was confirmed closed. The tokens are intentionally public classroom fixtures, not production authentication. Python's HTTP server is used only as a small synthetic source, not as production hosting.

## Actual agent and review operations

| Example | Default observation |
| --- | --- |
| 04 · SDK API tool | Actual C1 HTTP tool observation contained fee 100, currency, source and snapshot |
| 05 · LlamaIndex DB tool | Actual scoped SQL tool observation contained the same fee and metadata from training-db |
| 06 · Approved database action | Real SDK pause/review/resume created exactly `('request-001', 'C1', 'Customs hold')` |

Initial normal answers in 04/05 preserved the date but omitted midnight UTC precision. The instruction was clarified to quote the full `as_of` timestamp exactly, then both normal examples were rerun. Their final observed answers retained `2026-11-06T00:00:00Z`, USD and the appropriate source. Initial and final transcripts are separate. This does not establish that every future model explanation will preserve every field.

Thirteen focused live input/review/limit variations passed:

- Plain HTTP denied C2 and missing C9 produced unavailable/404.
- SDK denied/missing requests produced actual unavailable tool observations with no fee.
- LlamaIndex denied/missing requests likewise produced no fee.
- Rejected review, invalid review input, denied C2, missing C9 and a changed unapproved payload each left the draft table empty.
- SDK max_turns=1 and LlamaIndex max_iterations=1 stopped with their actual runtime-limit errors. The SDK also printed an explicit incomplete message.

The denied/missing/limit variations preceded the final timestamp-only instruction clarification; HTTP/SQL and approval enforcement code was unchanged. Normal tool calls were rerun after that clarification. Fixed turn/iteration limits are different runtime units, not aggregate tool/token budgets.

A later focused test exercised the final SDK tool implementation directly through its native ToolContext, without a model call: first invocation returned created; the same operation/payload returned reused; an unapproved changed payload returned denied; a newly approved different payload under the old operation ID returned conflict. The database retained the one original row. This test used the final schema with its NOT NULL operation key. It is separate from the real model-selected approval run.

06 uses actual terminal review; verification supplied approve/reject text as controlled test input. Approval cannot override the database-owner or exact-payload checks. Further interruptions stop for new review. The supplied reason Customs hold is a synthetic draft payload, not inferred from the API response. No external message was sent.

## Failure and timeout evidence

A scripted TimeoutError at 01's HTTP boundary printed `SERVICE UNAVAILABLE: TimeoutError`; it used a mock and made no HTTP/model call. A separate stopped-service check verified real connection-failure mapping in 01 and the SDK tool. These are distinct from an actually observed network timeout.

The normal examples use blocking HTTP-operation timeout=2 seconds, SDK max_turns=4, and LlamaIndex max_iterations=4 with workflow timeout=30. The toy examples do not establish production deadlines, retry/reconciliation semantics, or a complete outage test suite. They surface errors rather than substituting successful fixture replies.

## Retained SQL comparisons

The former SQL-focused examples moved to [reference](../README.md); they are not imported by core files. The SQL-generation reference was updated to `OPEN_AI_KEY` and made an actual model call. Observed proposal: `SELECT SUM(fee) AS total_fee FROM containers;`, actual result `[(300,)]`, matching the independent reference. The grain example's deliberate join total is 400 versus the intended 300. Giving the second call in 07 a new operation ID was also checked: it created a second row rather than reusing the first. Neither aggregate reference dataset claims caller-scope enforcement.

These are disposable SQL comparisons. Query-only mode and a progress callback are not a production hostile-query sandbox. The core agents receive narrow business tools, not an arbitrary SQL execution interface.

## Limits and handoff

[verification-results.json](verification-results.json) retains current source hashes, readable default/variation transcripts, direct HTTP observations and final focused-tool outcomes. The comparison concerns actual operations and selected examples; it is not a measured production-readiness or statistical-reliability claim. No broad adversarial, concurrent retry, durable idempotency, real identity-provider, cloud database or external delivery system was tested. Databases reset between processes.

A separate read-only review found no material code, teaching-alignment or evidence issue. All 34 slides were rendered to temporary PNGs and visually inspected through contact sheets. Excerpts are complete where practical, with shortened bodies/illustrations labelled and full source links provided. Concept explanations precede code; prediction questions have answer cues in notes. Local links, source syntax, setup and course-map status were checked.

Labs, assessments, notebooks, Gamma export, staging and commits remain outside this revision.
