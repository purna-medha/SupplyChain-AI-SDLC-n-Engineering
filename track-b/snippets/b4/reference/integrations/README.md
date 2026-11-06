# B4 · API and controlled-write references

These are the prior API-focused B4 examples, retained as optional supporting material. They are not imported by the [current core](../../README.md). Each still runs independently; the HTTP examples need the separate service.

| File | Purpose |
| --- | --- |
| [01_read_business_api.py](01_read_business_api.py) | Plain HTTP read and controlled errors |
| [02_query_database.py](02_query_database.py) | Plain SQLite parameter binding |
| [03_scope_database_read.py](03_scope_database_read.py) | Host-owned caller and selected result fields |
| [04_agent_with_api.py](04_agent_with_api.py) | SDK tool backed by actual HTTP |
| [05_llamaindex_database_tool.py](05_llamaindex_database_tool.py) | LlamaIndex tool backed by a scoped SQLite read |
| [06_approved_database_action.py](06_approved_database_action.py) | Exact-payload review and an actual SQLite draft write |
| [07_prevent_duplicate_actions.py](07_prevent_duplicate_actions.py) | Sequential retry reuse and conflicting-payload rejection |

Use the [shared environment](../../../../SETUP.md). From `track-b`, for HTTP examples start terminal A:

```bash
uv run python snippets/b4/reference/integrations/service.py
```

In terminal B:

```bash
uv run python snippets/b4/reference/integrations/01_read_business_api.py
uv run python snippets/b4/reference/integrations/04_agent_with_api.py
```

Stop the service with Ctrl+C. It uses loopback port 8766 and public demo-token fixtures, not production authentication. To inspect a reviewed write without that server:

```bash
uv run python snippets/b4/reference/integrations/06_approved_database_action.py
```

Type approve or reject after inspecting the pending arguments. Check actual rows. The tool independently enforces owner and exact-payload scope; no external message is sent. All SQLite databases reset between script runs. 07's sequential idempotency illustration does not supply durability or a concurrent service design.

[Historical verification](VERIFICATION.md) and [captured results](verification-results.json) concern this previous seven-example version, not the current SQLAlchemy/text-to-SQL core. Model examples use `OPEN_AI_KEY`; no new packages are required.
