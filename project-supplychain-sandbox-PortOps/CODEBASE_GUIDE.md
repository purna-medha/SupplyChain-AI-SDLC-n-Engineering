# SupplyChainOps / PortOps codebase guide

Current working-tree implementation reviewed on **2026-10-07**. Read the local
[AGENTS.md](AGENTS.md), [repository guide](../docs/REPOSITORY_GUIDE.md), and
[file inventory](../docs/FILE_INVENTORY.md) alongside this guide.

## Current product and data relationships

This is a Jebel Ali terminal sandbox. An importer inspects containers, checks
accruing demurrage, submits waiver claims, and executes gate-out. The operations
workspace shows fees, escalations, claim overrides and drayage jobs. Although
shipments are stored, the current operational case is a **container**. The
proposed shipment reliability/invoice-review product is not implemented.

```text
Importer ← Shipment → Vessel (includes carrier and terminal)
               ↑
           Container (includes locked tariff rates)
               ↑
      TerminalEvent / Claim / DrayageJob

PortExceptionLog → terminal-name and dwell-window matching for claims
```

The eight SQLModel tables and their seed files:

| Table / CSV | Rows | Important facts |
| --- | --- | --- |
| `importer` / `importers.csv` | 3 | STANDARD/GOLD/PLATINUM discounts 0/0.10/0.20 |
| `vessel` / `vessels.csv` | 2 | Vessel/carrier identities, terminal, arrival, default free days |
| `shipment` / `shipments.csv` | 3 | Bill of lading key, importer/vessel links, port codes, container count |
| `container` / `containers.csv` | 4 | Discharge, free days, optional gate-out, locked tier rates |
| `port_exception_log` / `port_exception_logs.csv` | 2 | Terminal T1 crane outage and customs outage windows |
| `terminal_event` / `terminal_events.csv` | 7 | Discharge, customs hold, inspection and gate-out observations |
| `claim` / `claims.csv` | 1 | HLCU weather claim rejected with zero waiver |
| `drayage_job` / `drayage_jobs.csv` | 3 | Assigned drivers, warehouse, SLA, transit hours and completion status |

Container tariff rates and free days are already resolved facts; calculations
do not look up a separate tariff table or use the vessel default to override
them. `tier_discount_percentage` is a fraction, e.g. `0.20`, despite its name.
Terminal events do not drive dwell calculation: container discharge/gate-out
dates do. Drayage rows are read-only in the current API; gate-out does not
advance a job or check customs clearance, fee payment, or dispatch eligibility.

The local ignored database retained old `carrier` and `tariff` tables at review
time, yielding ten physical tables versus eight current models. They are no
longer used. Reset drops only registered current tables, so those legacy tables
can remain. Use current models, CSVs and services as implementation evidence.

## Backend map

All paths below are under the inner `supplychainops/` package.

| File | Responsibility |
| --- | --- |
| `database_models.py` | Eight storage models and links |
| `database_configuration.py` | SQLite path `data/supplychainops.db`, engine and request-session dependency |
| `domain_demurrage_calculation_engine.py` | Pure dwell, overdue days, tariff split, discount/waiver math, derived status |
| `domain_dispute_claims_engine.py` | Exception overlap, automatic claim decision, override validation |
| `port_read_service.py` | Importers, joined container context, importer container views, claim/job filters |
| `port_demurrage_service.py` | Calculation orchestration, approved-waiver sums, KPIs, gate-out transaction |
| `port_claims_service.py` | Ownership/evidence checks, claim creation, manager overrides |
| `validation_schemas.py` | Typed HTTP requests/responses |
| `application_api_routes.py` | Thin route adapters and local exception-to-HTTP mapping |
| `main.py` | FastAPI lifecycle, router, permissive CORS middleware |
| `__init__.py` | Package description |

The working tree includes a frozen `ContainerContext` dataclass in
`port_read_service.py`. `load_container_context` performs one joined select
across container, shipment, vessel and importer; it raises
`ContainerContextNotFoundError` if any required link is missing. Claim and
demurrage services access its named fields. Older committed code used a tuple
and separate lookups. Preserve existing user edits when working in these files.
The overview query also joins container to shipment to restrict importer rows.

## Demurrage and status

`calculate_container_demurrage` loads context, sums positive claim waivers,
then delegates to `build_demurrage_calculation_breakdown`.

```text
end_date = gate_out_date, otherwise calculation_date
dwell = max(0, end_date - discharge_date), in days
overdue = max(0, dwell - free_days_allowed)
tier1_days = min(overdue, 5)
tier2_days = max(0, overdue - 5)
gross = round((tier1_days × rate1 + tier2_days × rate2) × (1 - discount), 2)
net = max(0, round(gross - approved_waivers, 2))
```

The field named `gross_demurrage_fee_usd` is already **after the commercial
discount**, before waivers. Gated-out containers stop accruing. Status is
derived: gate-out → `GATED_OUT`; positive overdue → `OVERDUE`; otherwise
`IN_TERMINAL`. It is not a separately persisted status column.

The pure engine returns a full breakdown (free days, tier days/rates, discount,
fees). The service deliberately returns a slimmer API shape with dwell,
overdue, gross, waiver, net and discount. Do not assume the HTTP response
exposes all of the pure engine's fields.

`build_operational_summary` totals gross fees, positive waivers, clamped net
revenue, overdue un-gated containers and escalated claims. It skips containers
with broken context links. Global net is total gross minus total waivers,
clamped once; with excessive waivers this need not equal the sum of individually
clamped container net amounts.

`execute_gate_out` rejects missing/already-gated containers, sets the current
calculation date and inserts a `GATE_OUT` event with the actual UTC timestamp
in one commit. It checks the container itself, not the full joined context.
There is no payment prerequisite or drayage mutation.

## Claim evidence and transitions

`submit_dispute_claim` checks importer existence and container ownership, then
looks for an exception at the vessel's terminal overlapping the inclusive
discharge-to-gate-out/calculation-date window. Naive exception timestamps are
interpreted as UTC; ISO strings are parsed. Any matching exception suffices.

| Evidence / amount | Stored outcome | Waiver |
| --- | --- | --- |
| No verified overlap | `REJECTED` | 0 |
| Verified, disputed amount < $500 | `AUTO_APPROVED` | Full rounded disputed amount |
| Verified, disputed amount >= $500 | `ESCALATED_TO_MANAGER` | 0 |

The submitted reason category is recorded but **not matched** to the exception
category. `excused_penalty_days_count` is stored but not used to calculate a
waiver. Claims are not capped by accrued demurrage, and duplicate claims are
not prevented. Positive waivers are summed regardless of claim status; net
payable is clamped to zero. These limits are important before adding richer
dispute or invoice logic.

`approve_manager_override` permits only an escalated claim and a waiver no
larger than the disputed amount. The HTTP schema enforces nonnegative amounts
and a nonempty note. It stores the waiver and changes status to `AUTO_APPROVED`,
including a zero waiver; it does not record a distinct manager-approved state.
The required `manager_override_note` is passed to the service but is **not
persisted**. There is no actor, timestamp, approval history, or rejection action
for an escalated claim. Direct service/engine calls do not enforce every HTTP
constraint, including nonnegative override amounts.

## HTTP boundary

| Method/path | Inputs/filter | Result |
| --- | --- | --- |
| GET `/health` | None | Status and application name |
| GET `/importers` | None | Importer cards |
| GET `/containers` | Required `importer_identifier`; optional `status_filter` | Derived container overviews |
| GET `/containers/{container_identifier}/demurrage-calculation` | Identifier | Slim fee breakdown |
| POST `/containers/{container_identifier}/gate-out-execution` | Identifier, no business body | Gate-out date and event classification |
| POST `/dispute-claims/submit` | Container, importer, positive disputed amount, reason | Claim audit response; HTTP 201 |
| GET `/dispute-claims` | Optional `claim_decision_status_filter` | Claim audit list |
| PUT `/dispute-claims/{dispute_claim_identifier}/approve-override` | Nonnegative waiver, note | Updated claim |
| GET `/drayage-dispatch-jobs` | Optional `assigned_driver_name_filter` | Dispatch job rows |
| GET `/analytics/operational-summary` | None | Operational KPI projection |

Missing context/claim maps to 404, duplicate gate-out to 409, and claim/override
validation to 400. These use FastAPI `HTTPException` bodies `{detail: ...}`,
unlike retail/BFSI structured domain-error bodies. Malformed requests use
normal 422 validation responses. An unknown importer during claim submission
is a 400 validation error, while an unknown importer in the container list
is 404. Filters are plain strings, not constrained status enums.

## UI, reset, and repeatability

`ui/api_http_client.py` provides `SupplyChainOpsApiClient` (default API 8002).
`ui/streamlit_dashboard.py` is a single top-level screen with a sidebar API URL
and health check. The importer tab lists/filters containers, inspects fees,
submits claims and gates out. The operations tab displays KPIs, claims/status
filter, escalated override form and driver-filtered jobs. It imports no backend
database or calculation module. Unlike the other dashboards, it has no explicit
outer-folder `sys.path` insertion; launch from the outer project directory.

`scripts/reset_database.py` uses `SEED_FILE_ORDER` in dependency order: importer,
vessel, shipment, container, exception, event, claim, job. `_load_csv_rows`
uses SQLModel field annotations to convert dates/datetimes, optional types,
integers/floats and empty values; naive datetimes become UTC. Tests reuse this
loader and the actual CSV files, so seed changes directly change their cases.

Live calculations use `date.today()`. In tests, an autouse fixture patches
`get_current_calculation_date` in the pure engine **and all three service
modules that imported it** to **2026-09-22**. Patch all those bindings when
maintaining the fixed-clock pattern. Gate-out event timestamps still use live
UTC time; tests do not fix them.

Fixed-date examples:

- `MSKU1234567`: September 9 discharge, five free days, eight overdue days;
  `5×150 + 3×250 = $1,500`. Terminal T1 provides verified claim evidence.
- `HLCU5566778`: September 13 discharge, four overdue days;
  `4×175×0.80 = $560`. Terminal T2 has no exception evidence; seeded claim rejected.
- `MSCU7654321`: already gated out on September 14; cannot gate out twice.
- `TCLU9876543`: open reefer container available for gate-out test.

Live values after September 22 differ for open containers; static seeds do
not mean an invariant live date.

## Tests and development

23 tests passed at review time. `tests/conftest.py` seeds a StaticPool in-memory
database and overrides `get_database_session`. `test_end_to_end_workflow.py`
covers health/importers, filters, step tariffs and discounts, gate-out, claim
decision paths, overrides, drayage/KPIs and pure overlap/math examples. Existing
tests do not demonstrate complete auditing, reason-category matching, duplicate
claim prevention, all waiver boundary cases, or shipment/invoice workflows.

From this outer directory:

```bash
uv sync --group dev
uv run uvicorn supplychainops.main:app --reload --port 8002
uv run streamlit run ui/streamlit_dashboard.py
uv run pytest tests/ -q
# Only when restoring the baseline:
uv run python scripts/reset_database.py
```

For a fee change, read the pure demurrage engine → demurrage service → schema
and fee tests. For a claim change, read exception overlap/decision/override
engine → claims service → route/schema → fixed-date tests. Keep the eight-table
current model and container-held rates for maintenance tasks. The future
shipment-centered product requires an explicitly scoped redesign rather than
renaming this existing port workflow.
