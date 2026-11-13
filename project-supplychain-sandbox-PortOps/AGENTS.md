# SupplyChainOps Contributor Guide

For a detailed source-derived map of workflows, files, seeds, API contracts,
tests, and known implementation limits, read [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md).
The [capstone description](Capstone_details.md) defines the learner workflow
and distinguishes implemented behavior from optional extensions.

## For non-technical readers

SupplyChainOps is a practice environment for managing shipping containers at a
busy port. It tracks how long containers remain at the terminal, calculates
storage charges when they stay too long, handles requests to review those
charges, records containers leaving the terminal, and displays existing onward
trucking jobs. Trucking jobs can be viewed and filtered by driver. It is
designed to make port operations and the reasons behind each decision easier
to understand.

## Purpose and stack

SupplyChainOps (PortOps) is a deterministic FastAPI, SQLModel/SQLite, and
Streamlit training sandbox for Jebel Ali container-terminal dwell, step-tariff
demurrage, dispute claims, gate-out, and read-only drayage job visibility.
Read `PROJECT_PROMPT.md` and `README.md` before changing its calculations or
workflow.

## Layered architecture

- `domain_demurrage_calculation_engine.py` and
  `domain_dispute_claims_engine.py` are pure engines. Keep them free from
  database, HTTP, FastAPI, and UI imports.
- `port_read_service.py` owns SELECT-oriented reads. `port_demurrage_service.py`
  owns demurrage, gate-out, and KPI workflows; `port_claims_service.py` owns
  claim submission and manager-override workflows.
- `application_api_routes.py` remains a thin HTTP adapter. Keep validation
  models in `validation_schemas.py` and storage models in `database_models.py`.
- `main.py` is the application assembly point; database lifecycle access stays
  in `database_configuration.py`.
- The Streamlit dashboard in `ui/` must use `ui/api_http_client.py`, not
  database or service imports.

## Domain invariants

- Demurrage must use the supplied pure dwell and step-tariff calculation
  functions. Use the tariff rates stored on each container. Seed data supplies
  these as the rates agreed at discharge; the application has no discharge-time
  rate-selection or locking workflow. Do not recreate separate tariff or
  carrier tables.
- Claims must follow the auto-waiver state machine and verified exception-log
  rules. A manager override is valid only for an escalated claim; persist its
  note and use `MANAGER_APPROVED`. Reject a second claim for the same container
  and normalized reason with HTTP 409.
- Preserve deterministic calculation-date handling so dwell, fees, and tests
  stay reproducible. Resolve the date once through the API dependency and pass
  it explicitly to services and pure calculations; tests override that dependency.
- Keep the eight-table model intact: vessel (including carrier), importer,
  shipment, container, terminal event, port exception log, claim, and drayage
  job.

## Data, tests, and local development

- CSV seed inputs live in `data/seed/`; `data/supplychainops.db` is generated.
  Regenerate it with `python scripts/reset_database.py`, rather than editing
  the database by hand. Reset validates seeds, saves a timestamped `.bak` copy,
  and recreates only the eight current tables, removing legacy tables.
- Add focused coverage to `tests/test_end_to_end_workflow.py` when changing
  workflows, pure math, validation, or HTTP behavior. Retain the fixed-date
  fixture pattern for date-sensitive tests.
- From this directory:

  ```bash
  uv sync --group dev
  uv run python scripts/reset_database.py
  uv run pytest tests/ -v
  uv run uvicorn supplychainops.main:app --reload --port 8002
  uv run python -m streamlit run ui/streamlit_dashboard.py
  ```
