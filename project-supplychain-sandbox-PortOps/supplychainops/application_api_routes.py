"""Thin FastAPI route handlers — delegate to service layer."""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session

from supplychainops.database_configuration import get_database_session
from supplychainops.port_claims_service import (
    ClaimNotFoundError,
    ClaimValidationError,
    approve_manager_override,
    submit_dispute_claim,
)
from supplychainops.port_demurrage_service import (
    GateOutConflictError,
    build_operational_summary,
    calculate_container_demurrage,
    execute_gate_out,
)
from supplychainops.port_read_service import (
    ContainerContextNotFoundError,
    fetch_claims,
    fetch_containers_for_importer,
    fetch_drayage_jobs,
    fetch_importers,
)
from supplychainops.validation_schemas import (
    ContainerOverviewResponse,
    DemurrageCalculationBreakdownResponse,
    DisputeClaimAuditResponse,
    DisputeClaimSubmissionRequest,
    DrayageDispatchJobResponse,
    GateOutExecutionResponse,
    HealthCheckResponse,
    ImporterReadResponse,
    ManualWaiverOverrideRequest,
    SupplyChainOperationalSummaryMetricsResponse,
)

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse)
def health_check():
    return HealthCheckResponse(status="ok", application_name="SupplyChainOps")


@router.get("/importers", response_model=List[ImporterReadResponse])
def list_importers(session: Session = Depends(get_database_session)):
    return [ImporterReadResponse.model_validate(row) for row in fetch_importers(session)]


@router.get("/containers", response_model=List[ContainerOverviewResponse])
def list_containers(
    importer_identifier: str = Query(...),
    status_filter: Optional[str] = Query(None),
    session: Session = Depends(get_database_session),
):
    try:
        rows = fetch_containers_for_importer(session, importer_identifier, status_filter)
    except ContainerContextNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return [ContainerOverviewResponse(**row) for row in rows]


@router.get(
    "/containers/{container_identifier}/demurrage-calculation",
    response_model=DemurrageCalculationBreakdownResponse,
)
def get_demurrage_calculation(
    container_identifier: str,
    session: Session = Depends(get_database_session),
):
    try:
        breakdown = calculate_container_demurrage(session, container_identifier)
    except ContainerContextNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return DemurrageCalculationBreakdownResponse(**breakdown)


@router.post(
    "/containers/{container_identifier}/gate-out-execution",
    response_model=GateOutExecutionResponse,
)
def gate_out_container(
    container_identifier: str,
    session: Session = Depends(get_database_session),
):
    try:
        result = execute_gate_out(session, container_identifier)
    except ContainerContextNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except GateOutConflictError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return GateOutExecutionResponse(**result)


@router.post(
    "/dispute-claims/submit",
    response_model=DisputeClaimAuditResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_dispute_claim(
    payload: DisputeClaimSubmissionRequest,
    session: Session = Depends(get_database_session),
):
    try:
        claim = submit_dispute_claim(
            session,
            payload.container_identifier,
            payload.importer_identifier,
            payload.disputed_amount_usd,
            payload.dispute_reason_category,
        )
    except ContainerContextNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ClaimValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return DisputeClaimAuditResponse.model_validate(claim)


@router.get("/dispute-claims", response_model=List[DisputeClaimAuditResponse])
def list_dispute_claims(
    claim_decision_status_filter: Optional[str] = Query(None),
    session: Session = Depends(get_database_session),
):
    claims = fetch_claims(session, claim_decision_status_filter)
    return [DisputeClaimAuditResponse.model_validate(claim) for claim in claims]


@router.put(
    "/dispute-claims/{dispute_claim_identifier}/approve-override",
    response_model=DisputeClaimAuditResponse,
)
def manager_approve_override(
    dispute_claim_identifier: int,
    payload: ManualWaiverOverrideRequest,
    session: Session = Depends(get_database_session),
):
    try:
        claim = approve_manager_override(
            session,
            dispute_claim_identifier,
            payload.approved_waiver_amount_usd,
            payload.manager_override_note,
        )
    except ClaimNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except ClaimValidationError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return DisputeClaimAuditResponse.model_validate(claim)


@router.get("/drayage-dispatch-jobs", response_model=List[DrayageDispatchJobResponse])
def list_drayage_dispatch_jobs(
    assigned_driver_name_filter: Optional[str] = Query(None),
    session: Session = Depends(get_database_session),
):
    jobs = fetch_drayage_jobs(session, assigned_driver_name_filter)
    return [DrayageDispatchJobResponse.model_validate(job) for job in jobs]


@router.get(
    "/analytics/operational-summary",
    response_model=SupplyChainOperationalSummaryMetricsResponse,
)
def operational_summary(session: Session = Depends(get_database_session)):
    return SupplyChainOperationalSummaryMetricsResponse(**build_operational_summary(session))
