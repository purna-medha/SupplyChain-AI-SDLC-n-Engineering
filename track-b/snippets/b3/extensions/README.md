# B3 · Comparisons and persistence follow-ons

These examples illustrate concepts already explained in the [B3 lecture](../../../slides-md/b3-agentic-workflows.md). They are outside the six-file core sequence.

| File | Purpose |
| --- | --- |
| [01_parallel_specialists.py](01_parallel_specialists.py) | Run two real model tasks concurrently, retain branch identity and mark partial outcomes |
| [02_llamaindex_handoff.py](02_llamaindex_handoff.py) | Express the SDK charges handoff using LlamaIndex's AgentWorkflow |
| [03_persist_task_state.py](03_persist_task_state.py) | Extend core 05 with a file-backed conversation and task JSON snapshot |
| [04_saved_approval.py](04_saved_approval.py) | Extend core 06 with serialization/restoration of the pending SDK run |

Use the [B3 dependency setup](../README.md). From track-b:

~~~bash
uv run python snippets/b3/extensions/01_parallel_specialists.py
uv run python snippets/b3/extensions/02_llamaindex_handoff.py
uv run python snippets/b3/extensions/03_persist_task_state.py
uv run python snippets/b3/extensions/04_saved_approval.py
~~~

The parallel example supplies synthetic facts directly to two model calls. It does not perform shipment reads or establish a latency benchmark. The LlamaIndex example executes a real synthetic charge-reading tool after handing off from Triage to Charges. All four examples require OPEN_AI_KEY. The saved-approval example prompts for approve or reject. Both persistence follow-ons use temporary files, recreate objects in the same process and retain the original agent definitions; they do not demonstrate full service recovery.
