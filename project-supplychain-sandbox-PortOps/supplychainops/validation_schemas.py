"""Pydantic v2 request and response wire contracts."""

from datetime import date, datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class ImporterReadResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    importer_identifier: str
    importer_company_name: str
    commercial_tier_level: str
    tier_discount_percentage: float


class ContainerOverviewResponse(BaseModel):
    container_identifier: str
    bill_of_lading_number: str
    importer_identifier: str
    container_size_type: str
    cargo_classification_type: str
    vessel_discharge_date: date
    gate_out_date: Optional[date]
    free_days_allowed: int
    container_dwell_days: int
    container_status_label: str


class DemurrageCalculationBreakdownResponse(BaseModel):
    container_identifier: str
    container_dwell_days: int
    overdue_days_count: int
    gross_demurrage_fee_usd: float
    approved_waiver_amount_usd: float
    net_payable_demurrage_fee_usd: float
    tier_discount_percentage: float


class DisputeClaimSubmissionRequest(BaseModel):
    container_identifier: str
    importer_identifier: str
    disputed_amount_usd: float = Field(gt=0)
    dispute_reason_category: str


class DisputeClaimAuditResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    dispute_claim_identifier: int
    container_identifier: str
    importer_identifier: str
    disputed_amount_usd: float
    dispute_reason_category: str
    claim_decision_status: str
    approved_waiver_amount_usd: float


class ManualWaiverOverrideRequest(BaseModel):
    approved_waiver_amount_usd: float = Field(ge=0)
    manager_override_note: str = Field(min_length=1, max_length=256)


class DrayageDispatchJobResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    drayage_job_identifier: str
    container_identifier: str
    assigned_truck_driver_name: str
    delivery_warehouse_name: str
    agreed_service_level_agreement_hours: int
    actual_transit_hours: Optional[float]
    job_completion_status: str


class SupplyChainOperationalSummaryMetricsResponse(BaseModel):
    gross_accrued_demurrage_fees_usd: float
    approved_credit_waivers_usd: float
    net_demurrage_revenue_usd: float
    at_risk_container_count: int
    pending_escalated_claim_count: int


class GateOutExecutionResponse(BaseModel):
    container_identifier: str
    gate_out_date: date
    event_classification_type: str = "GATE_OUT"


class HealthCheckResponse(BaseModel):
    status: str
    application_name: str


class ApiErrorResponse(BaseModel):
    detail: str
