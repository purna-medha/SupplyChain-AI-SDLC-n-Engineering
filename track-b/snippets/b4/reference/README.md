# B4 · Supporting examples

Start with the [six core examples](../README.md): SQLAlchemy schema inspection/scoped reads, LlamaIndex text-to-SQL, semantic validation, execution policy and an agent query capability.

The earlier examples below remain optional:

| File or group | Purpose |
| --- | --- |
| [01_query_and_check_grain.py](01_query_and_check_grain.py) | Earlier SQLite join/grain illustration |
| [02_generate_and_validate_sql.py](02_generate_and_validate_sql.py) | Earlier direct model SQL experiment with an independent expected total |
| [03_governed_read_capability.py](03_governed_read_capability.py) | Earlier fixed SQLite scope/row-bound example |
| [API and write integrations](integrations/README.md) | Actual HTTP source, API/DB agent tools, exact-payload review and operation-ID reuse |

Use the [shared environment](../../../SETUP.md). For example:

```bash
uv run python snippets/b4/reference/01_query_and_check_grain.py
```

The old generated-SQL comparison reads `OPEN_AI_KEY` and uses a disposable in-memory dataset without a caller-scope contract. Its query-only/progress settings are limited teaching controls, not a hostile-query production sandbox. The core's explicit execution policy is the current teaching path.
