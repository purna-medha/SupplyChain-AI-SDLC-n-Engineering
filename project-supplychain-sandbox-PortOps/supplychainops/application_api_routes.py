"""HTTP inputs and service calls. Shared error responses are registered in main.py."""

from datetime import date

from fastapi import APIRouter, Depends
from sqlmodel import Session

from supplychainops import (
    port_claims_service as claims,
    port_demurrage_service as demurrage,
    port_read_service as reads,
    validation_schemas as schemas,
)
from supplychainops.database_configuration import get_database_session

router = APIRouter()


def get_current_calculation_date() -> date:
    """Resolve the live date once per request; tests override this dependency."""
    return date.today()


@router.get("/health", response_model=schemas.HealthCheckResponse)
def health_check():
    return {"status": "ok", "application_name": "SupplyChainOps"}


@router.get("/importers", response_model=list[schemas.ImporterReadResponse])
def list_importers(session: Session = Depends(get_database_session)):
    return reads.fetch_importers(session)


@router.get("/containers", response_model=list[schemas.ContainerOverviewResponse])
def list_containers(
    importer_identifier: str,
    status_filter: str | None = None,
    session: Session = Depends(get_database_session),
    calculation_date: date = Depends(get_current_calculation_date),
):
    return reads.fetch_containers_for_importer(
        session, importer_identifier, calculation_date, status_filter
    )


@router.get(
    "/containers/{container_identifier}/demurrage-calculation",
    response_model=schemas.DemurrageCalculationBreakdownResponse,
)
def get_demurrage_calculation(
    container_identifier: str,
    session: Session = Depends(get_database_session),
    calculation_date: date = Depends(get_current_calculation_date),
):
    return demurrage.calculate_container_demurrage(session, container_identifier, calculation_date)


@router.post(
    "/containers/{container_identifier}/gate-out-execution",
    response_model=schemas.GateOutExecutionResponse,
)
def gate_out_container(
    container_identifier: str,
    session: Session = Depends(get_database_session),
    calculation_date: date = Depends(get_current_calculation_date),
):
    return demurrage.execute_gate_out(session, container_identifier, calculation_date)


@router.post(
    "/dispute-claims/submit", response_model=schemas.DisputeClaimAuditResponse, status_code=201
)
def create_dispute_claim(
    payload: schemas.DisputeClaimSubmissionRequest,
    session: Session = Depends(get_database_session),
    calculation_date: date = Depends(get_current_calculation_date),
):
    return claims.submit_dispute_claim(
        session,
        payload.container_identifier,
        payload.importer_identifier,
        payload.disputed_amount_usd,
        payload.dispute_reason_category,
        calculation_date,
    )


@router.get("/dispute-claims", response_model=list[schemas.DisputeClaimAuditResponse])
def list_dispute_claims(
    claim_decision_status_filter: str | None = None,
    session: Session = Depends(get_database_session),
):
    return reads.fetch_claims(session, claim_decision_status_filter)


@router.put(
    "/dispute-claims/{dispute_claim_identifier}/approve-override",
    response_model=schemas.DisputeClaimAuditResponse,
)
def manager_approve_override(
    dispute_claim_identifier: int,
    payload: schemas.ManualWaiverOverrideRequest,
    session: Session = Depends(get_database_session),
):
    return claims.approve_manager_override(
        session,
        dispute_claim_identifier,
        payload.approved_waiver_amount_usd,
        payload.manager_override_note,
    )


@router.get("/drayage-dispatch-jobs", response_model=list[schemas.DrayageDispatchJobResponse])
def list_drayage_dispatch_jobs(
    assigned_driver_name_filter: str | None = None,
    session: Session = Depends(get_database_session),
):
    return reads.fetch_drayage_jobs(session, assigned_driver_name_filter)


@router.get(
    "/analytics/operational-summary",
    response_model=schemas.SupplyChainOperationalSummaryMetricsResponse,
)
def operational_summary(
    session: Session = Depends(get_database_session),
    calculation_date: date = Depends(get_current_calculation_date),
):
    return demurrage.build_operational_summary(session, calculation_date)
