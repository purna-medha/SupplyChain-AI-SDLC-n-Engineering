# PortOps (SupplyChainOps) — Project Prompt

Training sandbox for container dwell, demurrage fees, dispute claims, gate-out,
and read-only inland drayage job visibility. See `Capstone_details.md` for scope.

## Stack

Python 3.11+, FastAPI, SQLModel, SQLite, Streamlit, pytest. No LLM dependencies.

## Layered Architecture

| Layer | Files |
|-------|-------|
| Pure engines | `domain_demurrage_calculation_engine.py`, `domain_dispute_claims_engine.py` |
| Services | `port_read_service.py`, `port_demurrage_service.py`, `port_claims_service.py` |
| API | `application_api_routes.py`, `main.py` |

## Data Model (8 tables)

Vessel includes carrier fields. Each container stores its free-day allowance
and two daily tariff rates, loaded from the CSV seeds. These rates represent
the rates agreed at discharge; the application has no discharge-time
rate-selection or locking workflow. There are no separate tariff or carrier
tables.

Fee calculations use the importer's stored discount fraction. The seeded
Standard, Gold and Platinum importers have discounts of 0.00, 0.10 and 0.20;
the application does not derive discounts from tier names.

Manager overrides store a note on the existing claim table and use
`MANAGER_APPROVED`. A container/reason pair may have only one claim.

The API resolves the calculation date once and passes it explicitly to services.
Live requests use today's date; tests override the dependency to 2026-09-22.
There is no calculation-date selector in the dashboard or API request contract,
and resetting the database does not change the live calculation date.

Drayage job updates, SLA penalties and gate-out/dispatch synchronization are
optional extensions, not implemented workflows.

## Run Commands

```bash
uv sync --group dev
uv run python scripts/reset_database.py
uv run uvicorn supplychainops.main:app --reload --port 8002
uv run python -m streamlit run ui/streamlit_dashboard.py
uv run pytest tests/ -v
```
