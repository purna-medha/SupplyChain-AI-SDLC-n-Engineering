# B5 · Larger reference runners

These are the earlier, more extensive examples. The [short teaching sequence](../README.md) is the starting point. None of the teaching files imports these runners.

| File | Optional detail |
| --- | --- |
| [01_evaluate_and_repair.py](01_evaluate_and_repair.py) | Field/outbox grader probes and a deterministic five-case comparison |
| [02_trace_actual_work.py](02_trace_actual_work.py) | SDK repeated comparisons, native processor, usage and cost reporting |
| [03_llamaindex_evaluation.py](03_llamaindex_evaluation.py) | LlamaIndex repeated comparisons, events and native spans |
| [04_verify_action_outcomes.py](04_verify_action_outcomes.py) | Four approval/outbox outcome fixtures |
| [05_rubric_judge.py](05_rubric_judge.py) | Fact gate, clarity calibration and aggregate agreement |

Use the same [shared environment](../../../SETUP.md). From `track-b`, for example:

```bash
uv run python snippets/b5/reference/02_trace_actual_work.py
```

[Historical verification](VERIFICATION.md) and [captured results](verification-results.json) describe these larger versions, not the simplified core. In particular, their 8/10 to 10/10 scores do not verify the new short examples. The unsupported C3 explanation retained in the slides came from this earlier LlamaIndex run.
