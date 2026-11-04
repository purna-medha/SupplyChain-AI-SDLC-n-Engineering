# PortOps (SupplyChainOps) — Project Prompt

Enterprise training sandbox for container terminal demurrage, dispute claims, and inland drayage.

## Stack

Python 3.10+, FastAPI, SQLModel, SQLite, Streamlit, pytest. No LLM dependencies.

## Layered Architecture

| Layer | Files |
|-------|-------|
| Pure engines | `domain_demurrage_calculation_engine.py`, `domain_dispute_claims_engine.py` |
| Services | `port_read_service.py`, `port_demurrage_service.py`, `port_claims_service.py` |
| API | `application_api_routes.py`, `main.py` |

## Data Model (8 tables)

Vessel merges carrier fields. Container stores locked-in tier penalty rates at discharge. Tariff and carrier tables removed.

## Run Commands

```bash
uv sync --group dev
uv run python scripts/reset_database.py
uv run uvicorn supplychainops.main:app --reload --port 8002
uv run streamlit run ui/streamlit_dashboard.py
uv run pytest tests/ -v
```
