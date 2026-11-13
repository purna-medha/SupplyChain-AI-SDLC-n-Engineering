# B5 · Tracing references used by the slides

The current B5 slides link to these two standalone examples. Use the [five generated-answer examples](../README.md) for the main lesson.

| File | Supporting concept |
| --- | --- |
| [04_trace_openai_agent.py](application_checks/04_trace_openai_agent.py) | Native SDK tracing with local output |
| [05_trace_llamaindex_agent.py](application_checks/05_trace_llamaindex_agent.py) | LlamaIndex tool events and native spans |

Use [shared setup](../../../SETUP.md). From `track-b`:

```bash
uv run python snippets/b5/reference/application_checks/04_trace_openai_agent.py
uv run python snippets/b5/reference/application_checks/05_trace_llamaindex_agent.py
```

Both make actual model calls. Their intentionally incorrect fee boundary illustrates locating a tool error; execution traces do not establish generated-answer quality.
