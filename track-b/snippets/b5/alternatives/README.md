# B5 · Specialist evaluation alternatives

These are optional counterparts to the existing B5 examples. Choose plain Python, Promptfoo or DeepEval for the same teaching step; do not run all three paths in the one-hour session. The original nine programs remain the core sequence.

| Original example | Promptfoo version | DeepEval version |
| --- | --- | --- |
| [01 · Check one answer](../01_check_one_answer.py) | [YAML assertions](promptfoo/01_check_one_answer.yaml) | [Five reported requirements](deepeval/01_check_one_answer.py) |
| [02 · Evaluate cases](../02_evaluate_cases.py) | [Case configuration](promptfoo/02_evaluate_cases.yaml) + [application adapter](promptfoo/02_evaluate_cases.py) | [Cases and deterministic metric](deepeval/02_evaluate_cases.py) |
| [03 · Check the grader](../03_check_the_grader.py) | [Probe configuration](promptfoo/03_check_the_grader.yaml) + [grader](promptfoo/03_check_the_grader.py) | [Grader probes](deepeval/03_check_the_grader.py) |
| [07 · Judge clarity](../07_judge_clarity.py) | [`llm-rubric`](promptfoo/07_judge_clarity.yaml) | [`GEval`](deepeval/07_judge_clarity.py) |
| [08 · Repair and compare](../08_repair_and_compare.py) | [Comparison configuration](promptfoo/08_repair_and_compare.yaml) + [rule adapter](promptfoo/08_repair_and_compare.py) | [Both versions and unchanged references](deepeval/08_repair_and_compare.py) |
| [09 · Repeat agent trials](../09_repeat_agent_trials.py) | [Repeated evaluation](promptfoo/09_repeat_agent_trials.yaml) + [SDK adapter and assertion](promptfoo/09_repeat_agent_trials.py) | [Fresh SDK trials and evaluation](deepeval/09_repeat_agent_trials.py) |

Start with the [Promptfoo run guide](promptfoo/README.md) or [DeepEval run guide](deepeval/README.md). Each numbered example stands alone; it imports no other teaching example or shared teaching helper. The tooling has separate manifests and lockfiles. The shared Track B `pyproject.toml` and `uv.lock` do not gain dependencies.

## What the libraries replace

**Promptfoo** supplies case scheduling, repeated execution, assertion evaluation, comparison tables and result export. Small Python adapters still implement the application. 01/03/07 use its built-in echo provider to evaluate prepared drafts without generating another answer. Its Python assertions keep exact business checks visible.

**DeepEval** supplies the test-case format, metric execution, per-case feedback and aggregate reporting. The deterministic examples use short `BaseMetric` implementations: the library cannot infer the correct fee or policy. Example 07 uses its built-in `GEval` judge. In 09, Python still generates fresh SDK trials; DeepEval grades and reports their recorded outcomes. Some alternatives are longer than plain Python because they expose the framework contract.

04/05 retain the existing native tracing examples. 06 retains the SDK approval and exact new-outbox-entry checks; a library score cannot replace that application-state verification. No additional trace service is introduced.

## Keep the comparison honest

All records and policies are synthetic: C1=100, C2=200, C9 absent, owner A, review at **USD 200 or more**. The deliberately defective baseline uses `> 200`; the candidate uses `>= 200`.

| Example | Expected interpretation |
| --- | --- |
| 01 | Four of five requirements pass. Promptfoo reports one failed answer with five component assertions; DeepEval reports five requirement cases. These are different reporting units. |
| 02 | Four of five cases pass; only the boundary case fails. |
| 03 | All five grader probes pass, including correct rejection of four invalid answers. |
| 07 | Expected judge labels are true, true, false. Promptfoo negates the assertion on the jargon draft so three passing probes means agreement with the three labels. DeepEval prints each actual judgment beside its reference label. |
| 08 | On the two repair cases: baseline 1/2, candidate 2/2. The additional USD 201 case passes both versions. The combined library report is 5/6. |
| 09 | Three cases × two repetitions × two versions = 12 trials. Score the exact decision and actual requested tool IDs; retain errors and incomplete outcomes. |

01/02/03/08 are offline after installation. 07 makes real judge calls; 09 makes real SDK agent calls. Each 09 trial has its own agent, conversation and tool-call list. Promptfoo must run with `--no-cache`; DeepEval explicitly disables grading-cache reads/writes and generates each trial anew. Neither judge sees an author-supplied acceptance label as an input.

Judge algorithms and score scales differ. Matching criteria do not make their numerical scores interchangeable. Three calibration drafts and two trials per case are teaching evidence, not established accuracy or production reliability.

These alternatives focus on evaluation, not resource accounting. The SDK adapters do not export token usage or dollar cost to their evaluation runners. Promptfoo may display default zero usage for these custom providers; that means **unmeasured**, not free. DeepEval's evaluation duration in 09 excludes the earlier SDK generation loop. Judge calls also consume resources.

See the dated [verification record](VERIFICATION.md) and [compact results](verification-results.json).
