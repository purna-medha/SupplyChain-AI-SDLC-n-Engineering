# PortOps — SupplyChainOps

A small training application for container dwell, demurrage fees, dispute
claims and gate-out at a fictional Jebel Ali terminal. Trucking jobs are
available as a read-only list. No LLM or agent is included.

Start with [Capstone_details.md](Capstone_details.md) for the business exercise,
then use [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) to follow the code.

## Setup

Use Python 3.11+ and run these commands from this directory, where
`pyproject.toml` lives:

```bash
uv sync --group dev
uv run python scripts/reset_database.py
```

Reset replaces the database with the CSV baseline. Stop the API first. Existing
contents are saved beside it as `data/supplychainops.db.<timestamp>.bak`.
Reset also removes obsolete tables from earlier versions.

In one terminal, start the API:

```bash
uv run uvicorn supplychainops.main:app --reload --port 8002
```

In another terminal, from the same directory, start the dashboard:

```bash
uv run python -m streamlit run ui/streamlit_dashboard.py
```

Open the dashboard URL printed by Streamlit. The API documentation is at
http://localhost:8002/docs. Run the tests separately:

```bash
uv run pytest tests/ -v
```

Live requests use today's date. Tests override one date dependency to
2026-09-22; fees for open containers will therefore differ from the live demo.
The dashboard and API expose no calculation-date selector or request parameter.
Reset restores the seed data but does not change the live calculation date.

## Architecture

- `supplychainops/domain_*_engine.py`: pure calculations and claim rules.
- `supplychainops/port_*_service.py`: database reads and business workflows.
- `supplychainops/application_api_routes.py`: HTTP inputs, date dependency,
  and service calls.
- `supplychainops/main.py`: application assembly, startup, CORS and shared
  business-error handlers. Response schemas in `validation_schemas.py` handle
  serialization.
- `supplychainops/database_models.py`: eight SQLModel tables.
- `supplychainops/database_configuration.py`: one cached engine and a session
  per request.
- `ui/`: Streamlit dashboard and its HTTP client.
- `data/seed/`: eight CSV files containing 25 baseline records.

The tables are vessel (including carrier), importer, shipment, container
(including stored tariff rates), terminal event, port exception log, claim,
and drayage job.

## API

| Endpoint | Purpose |
| --- | --- |
| `GET /health` | Health check |
| `GET /importers` | List importers |
| `GET /containers` | Importer's containers, with optional status filter |
| `GET /containers/{id}/demurrage-calculation` | Fee summary |
| `POST /containers/{id}/gate-out-execution` | Gate-out and terminal event |
| `POST /dispute-claims/submit` | Create and evaluate a claim |
| `GET /dispute-claims` | Claims, stored manager notes and optional status filter |
| `PUT /dispute-claims/{id}/approve-override` | Approve an escalated claim |
| `GET /drayage-dispatch-jobs` | Read-only trucking jobs |
| `GET /analytics/operational-summary` | Fee, waiver and risk totals |

One claim is allowed per container and normalized reason. Repeats return 409.
Manager overrides require a note, store it, and set `MANAGER_APPROVED`.
The paths and existing fee-summary fields are unchanged; claim responses add
nullable `manager_override_note` and the distinct manager-approved status.

For a checkout from an earlier version, run reset before using the new claim
note field. This sandbox uses reset rather than schema migrations; the backup
retains old data for inspection.
