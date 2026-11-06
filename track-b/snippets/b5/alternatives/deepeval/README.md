# B5 · DeepEval alternatives

These are complete, independently runnable counterparts to the same-numbered original B5 programs. Read the [comparison map](../README.md) first. Each file includes the metric it uses; no shared teaching helpers hide the checks.

Run from **track-b**. This folder has its own `pyproject.toml`, `uv.lock` and ignored `.venv`, so installing DeepEval does not alter the shared B1–B5 environment.

```bash
uv sync --project snippets/b5/alternatives/deepeval --locked
export DEEPEVAL_TELEMETRY_OPT_OUT=YES
export DEEPEVAL_CACHE_FOLDER="$PWD/snippets/b5/alternatives/deepeval/.deepeval"

uv run --project snippets/b5/alternatives/deepeval --locked python \
  snippets/b5/alternatives/deepeval/02_evaluate_cases.py
```

Replace the filename with `01_check_one_answer.py`, `03_check_the_grader.py` or `08_repair_and_compare.py` for the other offline examples. All four require no model key after installation. The deliberately wrong amount and rule must still fail. A short deterministic `BaseMetric` provides exact checks; DeepEval executes the metric and formats results.

The live examples use `load_dotenv()` and `OPEN_AI_KEY`, following [shared setup](../../../../SETUP.md):

```bash
uv run --project snippets/b5/alternatives/deepeval --locked python \
  snippets/b5/alternatives/deepeval/07_judge_clarity.py

uv run --project snippets/b5/alternatives/deepeval --locked python \
  snippets/b5/alternatives/deepeval/09_repeat_agent_trials.py
```

07 uses `GEval` with an explicit `gpt-4.1-mini` judge, temperature 0 and a binary clarity decision. Compare actual judgments with the labels printed beside them. No source-grounding or authorization claim follows from a clarity pass.

09 generates 12 real SDK trials, creating fresh tool state and an agent for each one. DeepEval then scores all recorded outcomes and prints per-case feedback plus success frequencies. Failed and incomplete attempts remain in the denominator. `repeats` and `max_turns` are visible near the bottom of the program. Grading-cache reads/writes are disabled; SDK generation always executes anew.

`evaluate()` reports failed cases without raising an assertion, so these demonstration programs can exit **0 even when their report contains deliberate failures**. They are teaching reports, not CI gates. DeepEval's `assert_test()` is available when assertion-style failure is required. Application token usage/cost is unmeasured here; the displayed evaluation duration for 09 excludes agent generation that happened before `evaluate()`.

No Confident AI account or login is required for these local examples. DeepEval writes local run artifacts to the configured ignored cache folder.

Verified with DeepEval 4.3.3 and OpenAI Agents SDK 0.20.0. Reference: [local evaluations](https://deepeval.com/docs/getting-started), [custom metrics](https://deepeval.com/docs/metrics-custom), [G-Eval](https://deepeval.com/docs/metrics-llm-evals), [evaluation configuration](https://deepeval.com/docs/evaluation-flags-and-configs).
