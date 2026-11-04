"""Demurrage orchestration — tariff lookup, breakdown, gate-out, KPI aggregation."""

from datetime import date, datetime, timezone
from typing import Optional

from sqlmodel import Session, select

from supplychainops.database_models import Claim, Container, TerminalEvent
from supplychainops.domain_demurrage_calculation_engine import (
    build_demurrage_calculation_breakdown,
    get_current_calculation_date,
)
from supplychainops.port_read_service import ContainerContextNotFoundError, load_container_context


class GateOutConflictError(Exception):
    """Container has already been gated out."""


def sum_approved_waivers(session: Session, container_identifier: str) -> float:
    claims = session.exec(
        select(Claim).where(Claim.container_identifier == container_identifier)
    ).all()
    return round(
        sum(
            claim.approved_waiver_amount_usd
            for claim in claims
            if claim.approved_waiver_amount_usd > 0
        ),
        2,
    )


def calculate_container_demurrage(
    session: Session,
    container_identifier: str,
    current_calculation_date: Optional[date] = None,
) -> dict:
    """Single source of truth for per-container demurrage breakdown."""
    container_context = load_container_context(session, container_identifier)
    container = container_context.container
    importer = container_context.importer

    calculation_date = current_calculation_date or get_current_calculation_date()
    approved_waiver = sum_approved_waivers(session, container_identifier)
    breakdown = build_demurrage_calculation_breakdown(
        container_identifier=container.container_identifier,
        vessel_discharge_date=container.vessel_discharge_date,
        gate_out_date=container.gate_out_date,
        free_days_allowed=container.free_days_allowed,
        tier_1_daily_penalty_rate_usd=container.tier_1_daily_penalty_rate_usd,
        tier_2_daily_penalty_rate_usd=container.tier_2_daily_penalty_rate_usd,
        tier_discount_percentage=importer.tier_discount_percentage,
        approved_waiver_amount_usd=approved_waiver,
        current_calculation_date=calculation_date,
    )

    # API wire fields only — tier breakdown details stay in the pure engine.
    return {
        "container_identifier": breakdown["container_identifier"],
        "container_dwell_days": breakdown["container_dwell_days"],
        "overdue_days_count": breakdown["overdue_days_count"],
        "gross_demurrage_fee_usd": breakdown["gross_demurrage_fee_usd"],
        "approved_waiver_amount_usd": breakdown["approved_waiver_amount_usd"],
        "net_payable_demurrage_fee_usd": breakdown["net_payable_demurrage_fee_usd"],
        "tier_discount_percentage": importer.tier_discount_percentage,
    }


def build_operational_summary(session: Session) -> dict:
    calculation_date = get_current_calculation_date()

    # --- Per-container demurrage rollup ---
    gross_accrued = 0.0
    at_risk_count = 0
    for container in session.exec(select(Container)).all():
        try:
            breakdown = calculate_container_demurrage(
                session, container.container_identifier, calculation_date
            )
        except ContainerContextNotFoundError:
            # Skip rows with broken shipment, vessel, or importer links.
            continue
        gross_accrued += breakdown["gross_demurrage_fee_usd"]
        if container.gate_out_date is None and breakdown["overdue_days_count"] > 0:
            at_risk_count += 1

    # --- Claim-level KPIs ---
    claims = session.exec(select(Claim)).all()
    approved_waivers = round(
        sum(claim.approved_waiver_amount_usd for claim in claims if claim.approved_waiver_amount_usd > 0),
        2,
    )
    pending_escalated = sum(
        1 for claim in claims if claim.claim_decision_status == "ESCALATED_TO_MANAGER"
    )

    return {
        "gross_accrued_demurrage_fees_usd": round(gross_accrued, 2),
        "approved_credit_waivers_usd": approved_waivers,
        "net_demurrage_revenue_usd": round(max(0.0, gross_accrued - approved_waivers), 2),
        "at_risk_container_count": at_risk_count,
        "pending_escalated_claim_count": pending_escalated,
    }


def execute_gate_out(session: Session, container_identifier: str) -> dict:
    # Validate container exists and has not already left the terminal.
    container = session.get(Container, container_identifier)
    if container is None:
        raise ContainerContextNotFoundError("Container not found")
    if container.gate_out_date is not None:
        raise GateOutConflictError("Container already gated out")

    # Record gate-out date and terminal audit event.
    gate_out_date = get_current_calculation_date()
    container.gate_out_date = gate_out_date
    session.add(container)
    session.add(
        TerminalEvent(
            container_identifier=container_identifier,
            event_classification_type="GATE_OUT",
            event_recording_timestamp=datetime.now(timezone.utc),
        )
    )
    session.commit()
    return {"container_identifier": container_identifier, "gate_out_date": gate_out_date}
