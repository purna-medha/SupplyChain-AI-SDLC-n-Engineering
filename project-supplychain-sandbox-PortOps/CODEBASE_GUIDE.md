# SupplyChainOps / PortOps codebase guide

Read [AGENTS.md](AGENTS.md) for contributor rules,
[README.md](README.md) for setup and
[Capstone_details.md](Capstone_details.md) for the exercise and scope.

## Follow one workflow

For a fee calculation, read these files in order:

1. `domain_demurrage_calculation_engine.py`: the pure calculation.
2. `port_demurrage_service.py`: load container context and approved waivers,
   then call the calculation.
3. `application_api_routes.py`: accept the identifier, resolve the calculation
   date through a dependency, then call the service. `main.py` maps missing
   context to HTTP 404.
4. `validation_schemas.py`: select the fee fields exposed over HTTP.
5. `ui/api_http_client.py` and `ui/streamlit_dashboard.py`: call and display it.

All backend paths above are inside `supplychainops/`. The UI imports no backend
service or database code. HTTP response models serialize service dictionaries
and ORM rows; routes do not manually rebuild those response models.

## Files and responsibilities

| File | Responsibility |
| --- | --- |
| `database_models.py` | Eight storage models; manager note lives on Claim |
| `database_configuration.py` | Cached SQLite engine; request-scoped Session |
| `domain_demurrage_calculation_engine.py` | Pure dwell, overdue, tariff, discount, waiver and status functions |
| `domain_dispute_claims_engine.py` | Exception overlap, automatic decision and override validation |
| `port_read_service.py` | Importers, joined container context, container overviews, claims and jobs |
| `port_demurrage_service.py` | Calculation orchestration, waivers, KPIs and gate-out |
| `port_claims_service.py` | Ownership, duplicate checks, claim submission and override persistence |
| `validation_schemas.py` | Request validation and HTTP response contracts |
| `application_api_routes.py` | HTTP inputs, calculation-date dependency and service calls |
| `main.py` | Application lifecycle, router, CORS and shared 400/404/409 error responses |
| `scripts/reset_database.py` | CSV parsing, seed validation, backup and schema reset |

`ContainerContext` is a frozen dataclass holding container, shipment, vessel
and importer. `load_container_context` resolves them in one joined query and
raises `ContainerContextNotFoundError` if any link is absent.

## Data and baseline

```text
Importer ← Shipment → Vessel (includes carrier and terminal)
               ↑
           Container (includes stored tariff rates)
               ↑
      TerminalEvent / Claim / DrayageJob

PortExceptionLog → terminal/date evidence for claims
```

| CSV in `data/seed/` | Rows |
| --- | ---: |
| `importers.csv` | 3 |
| `vessels.csv` | 2 |
| `shipments.csv` | 3 |
| `containers.csv` | 4 |
| `port_exception_logs.csv` | 2 |
| `terminal_events.csv` | 7 |
| `claims.csv` | 1 |
| `drayage_jobs.csv` | 3 |

Container discharge/gate-out dates drive dwell; terminal events do not.
Container tariff rates and free days are already resolved facts loaded from
the CSV seeds. The rates represent those agreed at discharge; no discharge-time
rate-selection or locking workflow is implemented. The vessel's default free
days do not override the container's allowance. Discount percentages are
fractions stored on importers. The seeded Standard/Gold/Platinum values are
0.00/0.10/0.20; calculations use the stored fraction rather than the tier name.

## Calculation date and database lifecycle

`application_api_routes.get_current_calculation_date` resolves `date.today()`
through FastAPI dependency injection once per request. Read, fee, claim,
summary and gate-out workflows receive that date explicitly. The pure engine
requires a date and never consults the clock.

The dashboard and API request contract provide no calculation-date override.
Resetting the database restores seed data but does not change the live date.

`tests/conftest.py` overrides that one dependency to **2026-09-22**, seeds an
in-memory database from the real CSVs, and overrides the session dependency.
Direct service/engine tests pass dates as ordinary arguments. Gate-out audit
timestamps still record actual UTC time, independently of the calculation date.

`get_engine()` caches one engine. Each API request opens and closes its own
Session. Startup creates missing current tables but does not migrate existing
ones or load seeds. Run reset for a fresh baseline or after a schema change.

Reset validates every seed row before changing the database. If an existing
file is present, SQLite's backup API saves a consistent timestamped `.bak`
copy beside it. Reset reflects and drops the physical tables, including legacy
carrier/tariff tables, creates the eight current models, then inserts seeds
in dependency order in one transaction. Stop the running API before reset.
Backups contain the old schema and data; they are for inspection or restoration
with the matching code version, not automatic migration to the new schema.

## Fee and status rules

```text
end = gate_out_date, otherwise calculation_date
dwell = max(0, end - discharge_date), in days
overdue = max(0, dwell - free_days_allowed)
tier1_days = min(overdue, 5)
tier2_days = max(0, overdue - 5)
gross = round((tier1_days × rate1 + tier2_days × rate2) × (1 - discount), 2)
net = max(0, round(gross - approved_waivers, 2))
```

Gross is after the commercial discount, before waivers. Status is derived:
gate-out → `GATED_OUT`; otherwise positive overdue → `OVERDUE`; otherwise
`IN_TERMINAL`. Gate-out sets the supplied calculation date and inserts one
`GATE_OUT` event in the same commit. An already gated-out container returns 409.

The fee service returns the full pure breakdown. The HTTP response model
exposes only identifier, dwell, overdue, gross, waiver, net and discount fields.

The KPI summary skips containers with broken context links, counts un-gated
containers already overdue as at-risk, and counts escalated claims. Global net
is total gross minus total positive waivers, clamped once. Excess waivers mean
this can differ from the sum of individually clamped net amounts.

## Claim decisions and audit

Submission verifies importer existence and container ownership, normalizes the
reason with strip/uppercase, and rejects an existing container/reason pair
with 409. This also applies to a prior rejected claim. Different reasons may
produce separate claims. This is a sequential classroom check, not a
concurrency/idempotency guarantee.

Evidence requires the same vessel terminal and an exception overlapping the
inclusive discharge-to-gate-out/calculation-date window. Naive timestamps are
interpreted as UTC. Reason/category matching and excused penalty days are not
used. No evidence → rejected; evidence with amount below $500 → full automatic
waiver; evidence with amount at least $500 → escalation with zero waiver.

Only `ESCALATED_TO_MANAGER` may transition through an override. A finite,
nonnegative waiver no larger than the disputed amount and a trimmed note of
1–256 characters are required. The service stores both waiver and note, sets
`MANAGER_APPROVED`, and commits. A zero waiver is allowed. Claim list and
submission/override responses include nullable `manager_override_note`.

The baseline has no separate approval history, actor, timestamp or manager
rejection/reopening action. Waivers are not capped against accrued fees.
Positive waiver amounts are summed irrespective of status; valid application
writes issue positive waivers only for approved claims.

## HTTP and UI boundaries

See the endpoint table in [README.md](README.md). Shared exception handlers in
`main.py` translate service errors into HTTP responses. Missing containers/context
and claims return 404; repeated gate-out or container/reason claims return
409; claim/override business validation returns 400. Invalid request shapes
return FastAPI's 422. Errors use `{detail: ...}`. Status filters are strings.
Unknown importer is 400 during submission and 404 during container listing.

The dashboard offers importer and operations views, displays stored notes in
the claims table, includes `MANAGER_APPROVED` in its filter and shows write
errors without a traceback. Its personas are not authentication boundaries.
Drayage jobs are read-only. Gate-out has no payment/customs prerequisites and
does not advance trucking jobs; no SLA penalty engine is implemented.

## Verification

```bash
uv run pytest tests/ -v
```

The suite covers pure math, discount and evidence examples, fixed-date HTTP
journeys, error statuses, manager note persistence/filtering, duplicate waiver
prevention, explicit service dates, slim fee responses, backup recovery,
legacy-table removal and invalid-seed safety. Add focused workflow coverage in
`tests/test_end_to_end_workflow.py` when changing these behaviors.
