"""Dispute claim write operations — auto-waiver engine and manager overrides."""

from sqlmodel import Session, select

from supplychainops.database_models import Claim, Importer, PortExceptionLog
from supplychainops.domain_dispute_claims_engine import (
    evaluate_dispute_claim_decision,
    validate_manual_waiver_override,
    verify_port_exception_overlap,
)
from supplychainops.domain_demurrage_calculation_engine import get_current_calculation_date
from supplychainops.port_read_service import ContainerContextNotFoundError, load_container_context


class ClaimValidationError(ValueError):
    """Raised when claim submission or override rules are violated."""


class ClaimNotFoundError(LookupError):
    """Raised when dispute claim identifier does not exist."""


def submit_dispute_claim(
    session: Session,
    container_identifier: str,
    importer_identifier: str,
    disputed_amount_usd: float,
    dispute_reason_category: str,
) -> Claim:
    if session.get(Importer, importer_identifier) is None:
        raise ClaimValidationError("Importer not found")

    container_context = load_container_context(session, container_identifier)
    if container_context.shipment.importer_identifier != importer_identifier:
        raise ClaimValidationError("Container does not belong to importer")

    calculation_date = get_current_calculation_date()
    dwell_end = container_context.container.gate_out_date or calculation_date
    exception_logs = session.exec(select(PortExceptionLog)).all()
    verified = verify_port_exception_overlap(
        container_context.vessel.berth_terminal_name,
        container_context.container.vessel_discharge_date,
        dwell_end,
        [log.model_dump() for log in exception_logs],
    )
    decision_status, approved_waiver = evaluate_dispute_claim_decision(
        disputed_amount_usd,
        verified,
    )

    claim = Claim(
        container_identifier=container_identifier,
        importer_identifier=importer_identifier,
        disputed_amount_usd=disputed_amount_usd,
        dispute_reason_category=dispute_reason_category,
        claim_decision_status=decision_status,
        approved_waiver_amount_usd=approved_waiver,
    )
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim


def approve_manager_override(
    session: Session,
    dispute_claim_identifier: int,
    approved_waiver_amount_usd: float,
    manager_override_note: str,
) -> Claim:
    claim = session.get(Claim, dispute_claim_identifier)
    if claim is None:
        raise ClaimNotFoundError("Dispute claim not found")

    validation_error = validate_manual_waiver_override(
        approved_waiver_amount_usd,
        claim.disputed_amount_usd,
        claim.claim_decision_status,
    )
    if validation_error:
        raise ClaimValidationError(validation_error)

    claim.approved_waiver_amount_usd = approved_waiver_amount_usd
    claim.claim_decision_status = "AUTO_APPROVED"
    session.add(claim)
    session.commit()
    session.refresh(claim)
    return claim
