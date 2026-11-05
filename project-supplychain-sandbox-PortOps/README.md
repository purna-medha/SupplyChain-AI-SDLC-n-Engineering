# PortOps — SupplyChainOps

Deterministic supply-chain digital twin for Jebel Ali container terminal operations: dwell tracking, step-tariff demurrage, automated dispute claims, and drayage dispatch.

**Codebase guide:** [CODEBASE_GUIDE.md](CODEBASE_GUIDE.md) explains the current
workflows, files, seed stories, contracts, tests, and implementation limits.

**Track B labs:** [AI container help desk](labs/ai_container_help_desk/README.md)
adds B1–B3 learner TODO starters over the existing read APIs, with a separate
AI environment and a reviewed local draft outbox.

**Monorepo siblings:** [omnicommerceops/](../omnicommerceops/) (retail) · [bfsihub/](../bfsihub/) (banking & wealth)

## Quick Start

```bash
cd supplychainops
uv sync --group dev
uv run python scripts/reset_database.py
uv run uvicorn supplychainops.main:app --reload --port 8002
uv run streamlit run ui/streamlit_dashboard.py
uv run pytest tests/ -v
```

## Architecture

```
supplychainops/
├── domain_demurrage_calculation_engine.py   # Pure dwell + step-tariff math
├── domain_dispute_claims_engine.py          # Auto-waiver state machine
├── port_read_service.py                     # SELECT queries
├── port_demurrage_service.py                # Demurrage + gate-out + KPIs
├── port_claims_service.py                   # Claim submit + manager override
└── application_api_routes.py                # Thin HTTP handlers
```

**8 tables:** vessel (includes carrier), importer, shipment, container (includes tariff rates), terminal_event, port_exception_log, claim, drayage_job.

## API

| Endpoint | Purpose |
|----------|---------|
| `GET /health` | Health check |
| `GET /importers` | List importers |
| `GET /containers` | Container overview with dwell days |
| `GET /containers/{id}/demurrage-calculation` | Fee breakdown (slim response) |
| `POST /containers/{id}/gate-out-execution` | Gate-out + terminal event |
| `POST /dispute-claims/submit` | Auto-waiver claim processing |
| `GET /dispute-claims` | Claim audit list |
| `PUT /dispute-claims/{id}/approve-override` | Manager waiver override |
| `GET /drayage-dispatch-jobs` | Truck dispatch jobs |
| `GET /analytics/operational-summary` | Port KPI metrics |
