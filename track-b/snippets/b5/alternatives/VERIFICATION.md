# B5 alternatives · verification

Verified 6 November 2026. These observations apply to the optional Promptfoo/DeepEval counterparts, not to every behaviour of the wider application.

## Environment and isolation

Promptfoo 0.125.1 was installed and executed with Node.js 25.3.0 and npm 11.7.0. Its declared Node floor is 22.22.0. Python adapters used the existing Track B Python 3.12 environment, including OpenAI Agents SDK 0.20.0 and OpenAI 2.54.0.

DeepEval 4.3.3 ran in its separate locked Python 3.13.6 environment with OpenAI Agents SDK 0.20.0, OpenAI 2.54.0, Pydantic 2.14.3 and python-dotenv 1.2.4. The shared environment and root lockfile were not changed. Dependency locks are included for both optional paths. Actual model calls used `gpt-4.1-mini` and existing credentials; no key is included in the artifacts.

## Native runner results

| Example | Promptfoo | DeepEval |
| --- | --- | --- |
| 01 · Prepared answer | Four of five component assertions pass; one failed answer case | Four of five requirement cases pass |
| 02 · Five cases | 4/5; boundary fails | 4/5; boundary fails |
| 03 · Grader probes | 5/5, including correct rejection | 5/5, including correct rejection |
| 07 · Real clarity judge | 3/3 calibration probes agree: accept, accept, reject | Actual labels true, true, false agree with references |
| 08 · Rule comparison | Baseline 1/2 repair cases; candidate 2/2; extra 201 passes both | Same results; combined report 5/6 |
| 09 · Real SDK trials | Baseline 4/6; candidate 6/6 | Baseline 4/6; candidate 6/6 |

Each 09 run executed three cases twice per version: 12 trials per tool, **24 actual agent trials total**. Both tools recorded C1 clear 2/2, baseline C2 review 0/2, candidate C2 review 2/2, and C9 unknown 2/2. Every completed trial recorded the correct requested tool ID. The candidate changes only `> 200` to `>= 200`; the model, instruction, cases and criteria remain fixed within each comparison. Promptfoo used `--repeat 2 --no-cache --max-concurrency 1`. DeepEval generated each trial afresh before evaluating, with grading caching disabled.

07's drafts are prepared inputs, not freshly generated answers. Promptfoo uses a negated rubric on the known-negative draft, so its 3/3 refers to agreement with labels. DeepEval prints its three actual judgments. These are different algorithms with the same narrow criteria; three probes do not establish judge accuracy. No new live LlamaIndex evaluation was needed.

## Scripted checks and limitations

Seven focused offline contract checks passed. They exercised: all source/access outcomes; boundary and extra fee; rejection of missing/incorrect fee types, including bool/float; detection of an always-accepting grader; actual tool-ID scoring; fresh agents and isolated tool-call lists while invoking actual decorated SDK tools with a controlled runner; and retention of scripted turn-limit/runtime-error records as failed trials. Scripted checks verify handling, not live model choices. The temporary verification harness and full run logs are under `/tmp/b5-eval-alternatives`; [compact results](verification-results.json) retain the relevant outcomes.

An initial Promptfoo clarity run had three configuration errors because the Node process did not discover the parent `.env` file. No judge calls ran in that attempt. Selecting the existing `.env` explicitly resolved the issue; the run guide documents this requirement. A first scripted SDK-tool check used the wrong context wrapper; correcting the verification harness to use `ToolContext` produced seven passing checks. No application change was required.

Promptfoo exits 100 for expected assertion failures; DeepEval's `evaluate()` reports failures and returns normally. A clean process exit therefore has different meanings. No hosted dashboard ingestion, CI integration, external observability service, live outage or broader approval/outbox evaluation was added. Keep original example 06 for exact action-state verification.

Usage and dollar cost for the SDK adapters were not exported to either runner. Default zero usage fields in Promptfoo are **unmeasured**, not evidence of zero consumption. DeepEval's reported evaluation time for 09 excludes prior agent generation. Promptfoo separately recorded token usage for its judge assertions; judge calls are additional model usage. Scores and latencies are not a tool-performance benchmark.

Fresh syntax checks, 69 local-link checks and the native offline runs were performed. A separate read-only code review found no Critical or Important issues. No core slide sequence, labs or assessments were added. Two repetitions per case are a classroom illustration, not evidence of production reliability.
