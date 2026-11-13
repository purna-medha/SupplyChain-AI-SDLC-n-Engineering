# PortOps capstone: explain and resolve a container charge

## The scenario

An importer has a container waiting at a terminal. Its free storage allowance
has expired and daily demurrage charges are accruing. The importer needs to
understand the bill, request a waiver when a verified port exception exists,
and record the container leaving the terminal.

The supplied application uses deterministic Python rules, SQLite storage,
FastAPI endpoints and a Streamlit dashboard. Its importer and operations tabs
are two views of the same data; they are not authenticated user roles.

## What the application implements

1. List an importer's containers and show dwell days and derived status.
2. Calculate step-tariff fees, commercial discounts, approved waivers and net
   payable charges.
3. Submit a claim, check container ownership, verify terminal/date exception
   evidence, and approve, reject or escalate the claim.
4. Let a manager approve an escalated claim, storing the approval note.
5. Record gate-out and a terminal event; stop further fee accrual.
6. Show fee/risk totals, claim history and read-only trucking jobs.

The eight tables are vessel, importer, shipment, container, terminal event,
port exception log, claim and drayage job. Carrier details belong to vessels;
daily tariff rates and free-day allowances belong to containers. The seeds
supply rates representing those agreed at discharge; the application has no
discharge-time rate-selection or locking workflow.

## Business rules

Dwell days are the nonnegative number of days from discharge to gate-out, or
the calculation date for a container still at the terminal. Overdue days are
dwell days minus the container's free allowance, clamped to zero.

The first five overdue days use tier 1; subsequent days use tier 2. Multiply
the resulting charge by `1 - tier_discount_percentage`, then subtract approved
waivers and clamp net payable to zero. The field named `gross_demurrage_fee_usd`
is the amount after the commercial discount and before waivers.

The discount is stored as a fraction on the importer. In the seed data,
Standard has 0.00, Gold 0.10 and Platinum 0.20. Calculations read that stored
fraction directly; they do not derive a discount from the tier name.
Rates and free days come from each container, not a runtime carrier/tariff lookup.

| Claim evidence and amount | Outcome | Waiver |
| --- | --- | --- |
| No exception at the same terminal overlapping the dwell window | `REJECTED` | Zero |
| Verified exception and amount below $500 | `AUTO_APPROVED` | Disputed amount |
| Verified exception and amount of $500 or more | `ESCALATED_TO_MANAGER` | Zero pending review |
| Manager approves an escalated claim | `MANAGER_APPROVED` | Approved amount, from zero through disputed amount |

A manager note is trimmed, must contain 1–256 characters, and is stored.
Only an escalated claim can be overridden, and it cannot be approved twice.
A container may have one claim per reason, including rejected claims. Reasons
are trimmed and uppercased; a repeat returns HTTP 409 without another waiver.

For this exercise, evidence matches terminal and inclusive dates only. The
submitted reason is recorded but does not have to match the exception category.
`excused_penalty_days_count` is stored but does not determine the waiver.

## A walkthrough with fixed-date expectations

Tests use **2026-09-22**. Live requests use today's date, so open-container
fees vary. The dashboard and API expose no calculation-date selector or request
parameter. Resetting the database restores the seed data but does not change
the live calculation date. To reproduce these amounts, use tests that override
`get_current_calculation_date`, as shown in `tests/conftest.py`.

At the fixed date, starting from the seed baseline:

1. Inspect `MSKU1234567` for `IMP-GULF-001`: 13 dwell days, five free days,
   eight overdue days. Its charge is `5 × $150 + 3 × $250 = $1,500`.
2. Submit a $350 crane-breakdown claim. The terminal has overlapping exception
   evidence, so the claim is auto-approved and net payable becomes $1,150.
3. Submit the same container/reason again: expect 409 and no additional waiver.
4. Reset the baseline, submit a $750 claim, then approve a $600 manager waiver
   with a note. Expect `MANAGER_APPROVED`, the stored note, and $900 net payable.
5. Record gate-out. Advancing the calculation date must no longer increase
   dwell days or gross fees. Later approved waivers can still change net payable.
   A second gate-out returns 409.

Use `HLCU5566778` to investigate missing terminal evidence. Its baseline weather
claim is already rejected, so use a different reason for a new submission.

## Boundaries and optional extensions

Trucking jobs can be listed and filtered by driver. Truck assignments, delivery
updates, SLA penalties and automatic dispatch after gate-out are not implemented.
Gate-out does not check payment, customs clearance or dispatch eligibility.

Claims for different reasons can accumulate waivers, with no cap against the
accrued charge. Net payable is clamped to zero. Duplicate checking is intended
for sequential classroom use, not concurrent submissions. The sandbox has no
authentication, approval actor/timestamp history, claim reopening or production
schema migrations.

Possible extensions include reason/category evidence matching, financial waiver
caps, authenticated approvals, drayage updates and SLA calculations. An
AI-engineering capstone can add tools, grounded explanations and evaluations
over the supplied API; no AI behavior is included in the baseline.
