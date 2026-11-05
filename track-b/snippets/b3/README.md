# B3 · Workflows, specialists and approval

Complete [shared setup](../../SETUP.md), then run from `track-b`:

```bash
uv run python snippets/b3/01_workflow_patterns.py
```

Investigate a synthetic shipment delay. Run the six independent examples in order; no Ollama or MCP server is needed.

| File | Concept | Try changing |
| --- | --- | --- |
| [01_workflow_patterns.py](01_workflow_patterns.py) | Application controls sequence and routing | Change C2's status |
| [02_agent_investigation.py](02_agent_investigation.py) | Agent chooses operational tools | Set `container_id` to C2 or C9 |
| [03_agents_as_tools.py](03_agents_as_tools.py) | Coordinator calls specialists and answers | Ask only about operational facts |
| [04_handoff.py](04_handoff.py) | Specialist takes conversation ownership | Ask about departure instead of charges |
| [05_memory_and_state.py](05_memory_and_state.py) | Conversation history versus task state | Use a new session for the follow-up |
| [06_human_approval.py](06_human_approval.py) | Pause, review and resume | Try both approve and reject |

In 02, set `max_turns = 1` to observe an incomplete run at the limit.

## Review the proposed action

In 06, inspect the pending payload and type `approve` or `reject`. Approval appends to a local, in-memory demonstration outbox; it sends no external message. Invalid input stops without authorizing the action.

Core memory and approval state live in memory. Use the extensions to explore persistence.

## Continue

- [Slides](../../slides-md/b3-agentic-workflows.md) · [Lab](../../modules/b3/lab.md)
- [Exploration notebook](../../notebooks/b3_workflows_state_and_approval.ipynb) · [Notebook setup](../../notebooks/README.md)
- [Extensions: parallel work, LlamaIndex handoff and persistence](extensions/README.md)
- [Reference examples](reference/README.md) · [Verification record](VERIFICATION.md)
- [Requirements](requirements.txt) for standalone copies
