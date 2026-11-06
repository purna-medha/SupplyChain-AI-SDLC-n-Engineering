# B5 · Simplified teaching examples verified 5 November 2026

The current [nine examples](README.md) replace the earlier five larger runners as the teaching sequence. They contain 20–63 lines each and import no teaching helpers. The [reference folder](reference/README.md) retains the older runners and their separate historical evidence.

## Environment

The existing locked shared environment was reused without dependency changes: Python 3.12, openai-agents 0.20.0, openai 2.54.0, llama-index-core 0.14.25, llama-index-llms-openai 0.8.3, Pydantic 2.14.2 and python-dotenv 1.2.4. Model-backed examples used actual `gpt-4.1-mini` access and `OPEN_AI_KEY` loaded by `load_dotenv()`. No key was printed. Temperature 0 is set in the trace, judge and repeated-trial examples; the approval example retains the SDK default. These are dated observations, not promised future outputs.

## Offline examples

| Example | Observed result |
| --- | --- |
| 01 · One answer | Shape/type/identity/source checks pass; deliberately wrong amount fails |
| 02 · Five cases | 4/5 pass; equality at USD 200 exposes the deliberate defect |
| 03 · Grader probes | All five expected accept/reject judgments match |
| 08 · Repair | Below-boundary case passes both versions; boundary fails before and passes after; additional USD 201 case returns review in both |

A corrected draft fee of 200 made all 01 checks pass. A deliberately mutated always-true grader in 03 failed its assertion on the wrong-amount probe. These checks used controlled values and no model calls. 01/03 do not evaluate prose meaning. Actual clarity/paraphrase judgment is demonstrated separately in 07.

## Actual model-backed examples

| Example | Observed result |
| --- | --- |
| 04 · SDK trace | Native C2 function arguments were correct; observation already said `fee=200, decision=clear`; final answer copied that incorrect decision |
| 05 · LlamaIndex trace | Same C2 request and observation; final answer also reported clear |
| 06 · Action outcome | Approval added one exact new entry; rejection added none; both complete outbox comparisons passed |
| 07 · Clarity judge | Clear explanation and paraphrase passed; unexplained codes failed, matching all three classroom labels |
| 09 · Repeated trials | Boundary-only rule repair improved the observed decision-task result from 4/6 to 6/6 |

The 04/05 comparison uses the same source fixtures, question, model, instruction and policy expectation. Neither rebuilds an evaluation framework. SDK spans include IDs/parents and actual function payloads through a small readable console exporter. LlamaIndex tool events supply arguments/observations; its native span handler supplies IDs/parents/timing. No hosted trace-export ingestion was tested or claimed.

09 ran each unchanged case twice per version, creating a new agent/conversation and tool-call list for every trial:

| Decision case | Baseline successes | Candidate successes |
| --- | --- | --- |
| C1, below boundary | 2/2 | 2/2 |
| C2, at boundary | 0/2 | 2/2 |
| C9, unknown | 2/2 | 2/2 |
| Total | 4/6 | 6/6 |

The sole difference within this final comparison is `fee > 200` versus `fee >= 200`. Its task explicitly requires one final decision word. Passing requires that word and actual tool requests for the requested ID. It does not grade arbitrary natural-language answers or the broader application contract. Two attempts per case leave substantial uncertainty.

An initial development run of 09 returned sentences for C9 despite the intended label-only task. Those attempts failed the unchanged strict checker. The instruction was clarified to explicitly enumerate the allowed single words and prohibit added words/punctuation. Both baseline and candidate were then rerun under that same clarified instruction. The initial transcript is retained separately; the table above uses only the final matched comparison. No answers were silently normalized to turn failures into passes.

## Input, approval and stopping variations

Focused runs changed only documented input/limit values, without editing the distributed sources:

- SDK C1 and C9 variations exposed clear and unknown tool observations respectively, with absent fees left null.
- LlamaIndex C1 and C9 variations exposed the same observations under the same policy expectations.
- SDK `max_turns=1` stopped with an explicit incomplete message and `MaxTurnsExceeded`.
- LlamaIndex `max_iterations=1` surfaced its workflow-limit error.
- Changed text in 06 was rejected. Both review fixtures created zero new entries and passed their unchanged-state checks.
- Caller B in 06 likewise created zero new entries under both review fixtures.
- Repeated trials with `max_turns=1` and one attempt per case retained all six incomplete attempts as failures, with 0/1 per case/version.

A separate scripted `RuntimeError` at the SDK run boundary in 09 retained twelve error attempts and six 0/2 success-frequency results. That check used a mock and made no model calls; it verifies error handling, not actual provider outage behavior. The source-unavailable case in 02 is also controlled, not a live remote outage.

06 restores the seeded old outbox entry and approval payload between independent trials, then preserves the current trial's state while resuming after review. Its review decisions are evaluation fixtures, not live human approvals. A new payload requires its own exact approval. No external message is sent.

## Resource and score limits

04 prints actual token counts and elapsed SDK run time, ending its timer before trace flush/printing. 05 prints selected native span durations; its provider usage is not collected. 07 has additional evaluator model calls. Missing usage/cost remains unknown. Current short examples do not calculate an aggregate dollar cost; B1 introduces that calculation and the longer reference runner retains a fuller example. Nested/overlapping span durations cannot be added as end-to-end time.

The three 07 reference labels are author-assigned classroom examples, not independently validated judge accuracy. GuidelineEvaluator sees query/response, not source context; a clarity pass proves neither source truth nor permission. The older unsupported C3 fee-finalization claim remains an explicitly historical reference observation in the slides, not output attributed to a current short example.

## Files and slide alignment

[verification-results.json](verification-results.json) retains the current source hashes, readable default/variation transcripts, final repeated-run summary and the separately labelled initial instruction result. Earlier runner results remain exclusively in [reference evidence](reference/verification-results.json).

The deck still has 36 slides and the established Marp style. Code excerpts, filenames, current counts and presenter notes were synchronized with the short examples; full-run historical scores are no longer presented as current-core evidence. Current decision-task results are distinguished from the broader deterministic/source/approval cases. Changed slides were rendered and visually inspected. Local links and source syntax were checked.

## Teaching refinement and Gamma copy · 6 November 2026

The 36-slide Markdown deck now follows C2's boundary error through requirements, cases/checker probes, traces, diagnosis, repair and repeated trials. Action outcomes and clarity judgments then extend the method. The existing snippet numbering is retained; the lecture order is 01, 02, 03, 04, 05, 08, 09, 06, 07. A matching [Gamma text copy](../../slides-gamma/b5-safety-observability-evaluation.txt) preserves slide bodies, tables and fenced blocks while removing notes/configuration and local navigation.

The refined B4/B5 decks rendered to 34/36 PNGs and were visually inspected. Fresh read-only review confirmed source/evidence alignment and Gamma parity. Executable sources and the recorded model runs/scores are unchanged; no new model comparison is claimed by this teaching revision.

Labs, assessments and new notebooks remain deferred. No dependency, commit or staging operation was part of this revision.
