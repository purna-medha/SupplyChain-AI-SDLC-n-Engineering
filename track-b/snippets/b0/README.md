# B0 · Python for the supply-chain workshop

Use Python 3.11 or later. From `track-b`:

```bash
python3 snippets/b0/01_values_and_arithmetic.py
```

The 14 numbered examples use only Python's standard library: **no package install or API key required**. Each runs independently. Change one input and explain the result.

All records are synthetic. The transport quote is a flat pickup quote, separate from PortOps demurrage. Examples use no live shipment or capstone database.

## Core language path · 01–09

| File | Concept | Try changing |
| --- | --- | --- |
| [01_values_and_arithmetic.py](01_values_and_arithmetic.py) | Values, arithmetic and printing | Quote four containers |
| [02_lists_and_dictionaries.py](02_lists_and_dictionaries.py) | Records, collections and missing fields | Append C3; inspect the length |
| [03_conditions_and_loops.py](03_conditions_and_loops.py) | Loops and conditional branches | Change C2 to delayed |
| [04_functions_and_hints.py](04_functions_and_hints.py) | Parameters, returns and type hints | Use named arguments; try count 1.5 |
| [05_handling_errors.py](05_handling_errors.py) | Handle an expected exception | Try a negative count |
| [06_classes_and_methods.py](06_classes_and_methods.py) | Dataclass attributes and methods | Create another quote |
| [07_imports_and_dates.py](07_imports_and_dates.py) | Imports, dates and durations | Change the as-of date |
| [08_json_messages.py](08_json_messages.py) | Python values versus JSON text | Append an assistant message |
| [09_environment_variables.py](09_environment_variables.py) | Configuration and interpreter identity | Set `PORTOPS_URL` and rerun |

Type hints do not enforce runtime types. Example 09 reads process variables; loading a `.env` file requires an explicit loader, introduced in B1. It prints only whether a key exists.

## Application bridge · 10–14

Use these when the later application syntax is new; they are optional before B1.

| File | Concept | Try changing |
| --- | --- | --- |
| [10_sqlite_read.py](10_sqlite_read.py) | In-memory SQLite and bound query values | Query unknown C9 |
| [11_decorators.py](11_decorators.py) | Wrap a function | Use C2 |
| [12_async_calls.py](12_async_calls.py) | `async def`, `await` and event loops | Read C9 |
| [13_logging.py](13_logging.py) | Context in logs | Change IDs; inspect warnings |
| [14_testing_and_debugging.py](14_testing_and_debugging.py) | Tests and debugging | Remove the input check, observe failure, restore it |

## Optional local API

With [uv installed](../../SETUP.md), run from `track-b`:

```bash
uv run --with fastapi --with uvicorn uvicorn server:app --app-dir snippets/b0/extensions --port 8003
```

[server.py](extensions/server.py) exposes `/health` and `/containers/{container_id}`. Open [API docs](http://127.0.0.1:8003/docs); try C1, C2 and unknown C9. Stop with **Ctrl+C**. If occupied, change the port in both command and URL.

The first run may download packages. `--with` supplies FastAPI/Uvicorn without changing project dependencies.

## Continue

Before B1, explain a message dictionary, named arguments and attribute access.

- [Slides](../../slides-md/b0-python-foundations.md) · [Gamma copy](../../slides-gamma/b0-python-foundations.txt)
- [B1 snippet guide](../b1/README.md) · [Shared setup](../../SETUP.md)
- [Verification and example limits](VERIFICATION.md)
