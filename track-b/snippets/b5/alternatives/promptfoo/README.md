# B5 · Promptfoo alternatives

Each YAML is a counterpart to the same-numbered original B5 program. Read the [comparison map](../README.md) first. Promptfoo handles scheduling, assertions and reporting; the adjacent Python file, where present, is the application adapter or grader.

Run all commands from **track-b**. Requires Node.js **22.22.0 or newer**, npm, and the existing [shared Python setup](../../../../SETUP.md).

```bash
npm ci --prefix snippets/b5/alternatives/promptfoo
export PROMPTFOO_PYTHON="$PWD/.venv/bin/python"
export PROMPTFOO_CONFIG_DIR="$PWD/snippets/b5/alternatives/promptfoo/.promptfoo"
export PROMPTFOO_DISABLE_TELEMETRY=1
```

Run an offline example:

```bash
npm exec --prefix snippets/b5/alternatives/promptfoo -- promptfoo eval \
  --config snippets/b5/alternatives/promptfoo/02_evaluate_cases.yaml \
  --no-cache
```

Replace `02_evaluate_cases.yaml` with `01_check_one_answer.yaml`, `03_check_the_grader.yaml` or `08_repair_and_compare.yaml`. 01/02/08 deliberately include a failure; Promptfoo exits **100** when evaluation assertions fail. Inspect the failed case before treating this as an installation problem. 03 should pass all five probes.

The model-backed examples use `OPEN_AI_KEY` from the existing `snippets/.env` file. Promptfoo's Node process does not search parent directories like Python's `load_dotenv()`, so explicitly select the file. If your key is in another `.env`, pass its path instead.

```bash
npm exec --prefix snippets/b5/alternatives/promptfoo -- promptfoo eval \
  --config snippets/b5/alternatives/promptfoo/07_judge_clarity.yaml \
  --env-file snippets/.env --no-cache --max-concurrency 1

npm exec --prefix snippets/b5/alternatives/promptfoo -- promptfoo eval \
  --config snippets/b5/alternatives/promptfoo/09_repeat_agent_trials.yaml \
  --env-file snippets/.env --repeat 2 --no-cache --max-concurrency 1
```

07 evaluates three prepared drafts using real `gpt-4.1-mini` judge calls. The jargon case uses `not-llm-rubric`: it passes when the judge rejects that draft. 09 calls the SDK agent for **12 fresh trials**, not cached outputs. The baseline boundary failures are intentional. Exceptions and turn limits are retained as failed trial records with explicit status; a run with those outcomes can have zero *provider errors* while still containing failed/incomplete application attempts. Inspect the recorded status and calls.

To retain a JSON report, append `--output /tmp/b5-promptfoo-09.json` to a command. To browse saved local results:

```bash
npm exec --prefix snippets/b5/alternatives/promptfoo -- promptfoo view
```

No Promptfoo account is required for local evaluation/viewing. Repetitions and report generation do not replace custom state reset, business criteria or exact action checks. Application token usage/cost in 09 is unmeasured by this adapter, even if the report displays zero.

Try changing the fee in 01 to 200, the grader in 03 to always accept, the repaired comparison in 08, or `max_turns: 1` inside each provider's config in 09. Keep test references fixed while investigating a repair.

Verified with Promptfoo 0.125.1; its package and dependencies are pinned in `package-lock.json`. Reference: [Python providers](https://www.promptfoo.dev/docs/providers/python/), [Python assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/python/), [LLM rubrics](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/), [CLI options](https://www.promptfoo.dev/docs/usage/command-line/).
