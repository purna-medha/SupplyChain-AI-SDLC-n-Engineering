# B5 reference-run verification · 5 November 2026

Historical evidence for the larger runners retained in this folder. It does not verify the current [short teaching examples](../README.md). All statements below refer to the earlier five-file version.

This record concerns the rebuilt B5 teaching examples and [Marp deck](../../../slides-md/b5-safety-observability-evaluation.md), following the [agreed outline](../../../B5-OUTLINE.md). It does not reuse legacy B5 scores as evidence for the new examples.

## Environment and configuration

`uv sync --locked` passed: 114 packages resolved, 108 installed packages audited. No dependency or lockfile change was needed. The project description and setup now include B5 in the shared environment.

- Python 3.12; `openai` 2.54.0; `openai-agents` 0.20.0.
- `llama-index-core` 0.14.25; `llama-index-llms-openai` 0.8.3.
- `pydantic` 2.14.2; `python-dotenv` 1.2.4.
- Model: `gpt-4.1-mini`, temperature 0. The provider alias was used rather than a pinned model snapshot.
- Main limits: SDK `max_turns=4`; LlamaIndex `max_iterations=4` and workflow timeout 45 seconds. These limit different runtime units.
- Synthetic classroom fixtures only. `load_dotenv()` and `OPEN_AI_KEY`; no key printed or embedded.

All five files parsed and imported. Model-backed runs used real library calls and actual responses. There was no substitution of prepared answers after an access failure. Prepared drafts are explicitly limited to the grader/calibration examples. The unavailable-source case is a controlled tool outcome, not an actual remote fee-service outage.

## Deterministic verification

[01](01_evaluate_and_repair.py) ran without model access:

- Five field-grader probes: known correct and paraphrase accepted; wrong amount, wrong type and missing field rejected.
- Six outcome probes: exact new payload and unchanged rejected state accepted; false success, old matching entry, write after rejection and changed payload rejected.
- The five policy cases produced 4/5 baseline passes and 5/5 candidate passes. Equality at USD 200 was the only baseline failure.

These are deterministic rule/host checks, not measured model accuracy.

The final `grade()` functions in [02](02_trace_actual_work.py) and [03](03_llamaindex_evaluation.py) each passed ten additional offline probes. They covered correct output, wrong amount, permitted wording variation, missing tool evidence, wrong tool ID, wrong fee type, wrong protected read, valid denial, read after denial and absent required nullable field.

All 44 captured main/additional live trials were replayed through those final graders. Outcomes were unchanged. This replay is offline grading of actual retained execution, not 44 new model runs. Later changes extracted the grader, tightened tool-argument checks, allowed repeated permitted reads, and added an SDK cost estimate; focused live integration checks then ran on the final code.

## Actual SDK and LlamaIndex comparisons

Run commands, from `track-b`:

```bash
uv run python snippets/b5/reference/02_trace_actual_work.py
uv run python snippets/b5/reference/03_llamaindex_evaluation.py
```

Each runtime evaluated the same five cases twice per version, from clean fixtures. The sole behaviour change was the tool's `> 200` to `>= 200` decision rule.

| Case | SDK baseline | SDK candidate | LlamaIndex baseline | LlamaIndex candidate |
| --- | --- | --- | --- | --- |
| Below: A, C1, USD 100 | 2/2 | 2/2 | 2/2 | 2/2 |
| Boundary: A, C2, USD 200 | 0/2 | 2/2 | 0/2 | 2/2 |
| Missing: A, C9 | 2/2 | 2/2 | 2/2 | 2/2 |
| Denied: B, C2 | 2/2 | 2/2 | 2/2 | 2/2 |
| Dependency unavailable: A, C2 | 2/2 | 2/2 | 2/2 | 2/2 |
| **Main suite** | **8/10** | **10/10** | **8/10** | **10/10** |

No infrastructure errors or incomplete outcomes occurred in these main suites. The extra C3=USD 201 case ran once per version per runtime and passed its structured contract in all four trials. It is outside the ten-trial denominators and was not used to choose the equality repair.

The native SDK tool spans and LlamaIndex tool-result events showed correct C2 arguments and an already incorrect `decision='clear'` in the baseline tool observation. Final structured fields copied that decision. After repair the tool and final fields both returned `review`. Unknown, denied and unavailable cases retained null fees/sources and no successful protected reads. Baseline and candidate graders and fixture references remained unchanged.

The score checks field identity/type/value, decision, source label, tool arguments and permitted-read history. It does not establish semantic grounding of all free text. Both output models enforce the declared format. The source-label check alone is not a faithfulness evaluation.

## Approval and actual outcomes

```bash
uv run python snippets/b5/reference/04_verify_action_outcomes.py
```

Four real SDK pause/resume trials passed their actual outcome checks:

| Evaluation fixture | Observed local state |
| --- | --- |
| Approve exact payload as A | One new exact entry, task queued |
| Reject as A | Outbox unchanged, task pending |
| Caller B, approval requested | Review rejected, outbox unchanged, task pending |
| Changed fee/text payload | Review rejected, outbox unchanged, task pending |

Each independent trial restored its outbox with an old identical entry, task phase and approval state. The paused run resumed with its own conversation history. Review decisions were predefined fixtures, not live human decisions. Final prose was retained separately from the state checks. These are four individual outcomes, not repeated reliability estimates. No external message was sent.

## Narrow judge calibration

```bash
uv run python snippets/b5/reference/05_rubric_judge.py
```

Three actual `GuidelineEvaluator` calls agreed with the author-assigned clarity references: clear explanation passed, valid paraphrase passed, unexplained codes failed. Agreement was 3/3 attempted judgments. A prepared fee of 999 failed the direct fact gate and made no judge call. This is small classroom calibration pending trainer review, not independently established judge accuracy.

The evaluator receives query/response, not source context. It cannot prove source truth, full grounding, permission or task completion. A judge error stays in its attempted denominator.

## Focused runtime and error checks

A temporary verification harness imported the final modules and used the actual SDK/framework paths:

- Final SDK normal C1 trial passed, with native function evidence and a positive text-token cost estimate.
- SDK `MAX_TURNS=1` stopped with `MaxTurnsExceeded`, `passed=false` and an incomplete status. The tool read had already occurred.
- Final LlamaIndex normal C1 trial passed with actual tool events/native spans.
- LlamaIndex `MAX_ITERATIONS=1` stopped with `WorkflowRuntimeError`, `passed=false` and an incomplete status. No successful read occurred.

Separately, scripted `RuntimeError` injections at each runtime's run boundary were retained as error trials with `passed=false` and unknown usage. Those two checks used mocked failures and made no model call. They establish host error handling, not real provider outage behaviour. The live one-step stopping checks also ran in an earlier focused pass; neither pass is included in the main suite denominators.

## Observability and resource boundaries

02 captured SDK-created trace/span IDs, parent relationships, timestamps and actual function payloads through a local processor replacing the hosted exporter. 03 captured native `SimpleSpanHandler` timing/parents and separate `ToolCallResult` arguments/observations. No claim of hosted dashboard ingestion was made or tested.

SDK main/additional trials reported 10,938 input and 1,662 output tokens in total across 22 agent trials. Each completed SDK trial reported two model requests. LlamaIndex's observed structured-formatting stage made an additional model call; its recorder leaves token usage unknown. Judge usage is likewise not collected. None of these missing counts means zero cost.

Recorded main-trial median elapsed times were:

| Runtime | Baseline | Candidate |
| --- | --- | --- |
| SDK | 3.681 s | 3.571 s |
| LlamaIndex | 3.587 s | 3.585 s |

These are small sequential observations with network variability and different framework mechanics, not a controlled latency benchmark. Per-trial timings are retained. Nested/overlapping span durations were not summed.

The final SDK script estimates standard text-token cost from input, cached input and output counts at USD 0.40, 0.10 and 1.60 per million tokens respectively, checked against the [official model page](https://developers.openai.com/api/docs/models/gpt-4.1-mini) on 5 November. The calculation was verified in a focused actual trial. Main-suite runs predated adding the cost field; their retained rows have observed token counts rather than retrospectively invented cost observations. Failed-run usage/cost is unknown. Estimates exclude other infrastructure costs and need current rates. The model page marks this model deprecated; live account access worked during this verification, but a replacement requires re-evaluation.

## A visible remaining failure

The LlamaIndex candidate's extra C3 response included:

> Since the decision is "review," it indicates the fee is under consideration and not finalized yet. No update can be made until the review decision is resolved.

The source supplies the fee and a classroom review requirement. It does not establish fee finalization or forbid preparation of an update. Structured checks passed while that prose exceeded the evidence. The deck explicitly uses this observation to explain the score's limits; the separate clarity calibration does not validate it.

A future generation/grounding repair needs its own criteria and unchanged baseline/candidate comparisons. The current evidence supports the equality-rule repair, rather than a claim that every response is correct or that the assistant is production-ready. Two repeated trials per case leave substantial uncertainty. No broad adversarial, concurrency, durable delivery, production monitoring or full multi-turn evaluation was performed.

## Retained evidence and slide review

[verification-results.json](verification-results.json) contains the main/additional trial outputs, checks, tool observations, read histories, elapsed times and available usage, plus the four outbox outcomes and judge calibration transcript. It contains synthetic records only. Final focused outcomes and source hashes are recorded separately in that file. Full temporary native trace logs and slide PNGs stay outside the teaching folders.

The Marp source renders as 36 slides using the established 16:9 theme, 27px body, 36px teal headings, 20px code and 23px tables. All slides were visually inspected through temporary PNG contact sheets; the added regression-comparison slide was checked after the final render. Prediction questions have answer cues in notes. Conceptual/shortened excerpts and prepared comparisons are labelled; actual measured results have dates and scope limits.

A separate read-only reviewer found no material snippet correctness, safety-contract or deck-evidence issue. Local Markdown links and the final source excerpts were checked. Labs, formal assessments, Gamma export and new notebooks were not created or changed for B5.
