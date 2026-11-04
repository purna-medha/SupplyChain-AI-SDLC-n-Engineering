"""SQLModel ORM entities — 8 normalized supply-chain tables."""

from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Vessel(SQLModel, table=True):
    __tablename__ = "vessel"

    vessel_identifier: str = Field(primary_key=True, max_length=32)
    vessel_name: str = Field(max_length=128)
    carrier_identifier: str = Field(max_length=16, index=True)
    carrier_name: str = Field(max_length=128)
    default_free_days_allowed: int = 5
    contact_email_address: str = Field(max_length=128)
    berth_terminal_name: str = Field(max_length=128)
    vessel_arrival_timestamp: datetime


class Importer(SQLModel, table=True):
    __tablename__ = "importer"

    importer_identifier: str = Field(primary_key=True, max_length=32)
    importer_company_name: str = Field(max_length=128)
    commercial_tier_level: str = Field(max_length=32)
    tier_discount_percentage: float = Field(ge=0.0, le=0.20)


class Shipment(SQLModel, table=True):
    __tablename__ = "shipment"

    bill_of_lading_number: str = Field(primary_key=True, max_length=32)
    importer_identifier: str = Field(foreign_key="importer.importer_identifier", index=True)
    vessel_identifier: str = Field(foreign_key="vessel.vessel_identifier", index=True)
    origin_port_code: str = Field(max_length=16)
    destination_port_code: str = Field(max_length=16)
    total_container_count: int


class Container(SQLModel, table=True):
    __tablename__ = "container"

    container_identifier: str = Field(primary_key=True, max_length=32)
    bill_of_lading_number: str = Field(foreign_key="shipment.bill_of_lading_number", index=True)
    container_size_type: str = Field(max_length=8)
    cargo_classification_type: str = Field(max_length=16)
    vessel_discharge_date: date
    free_days_allowed: int
    gate_out_date: Optional[date] = None
    tier_1_daily_penalty_rate_usd: float
    tier_2_daily_penalty_rate_usd: float


class TerminalEvent(SQLModel, table=True):
    __tablename__ = "terminal_event"

    terminal_event_identifier: Optional[int] = Field(default=None, primary_key=True)
    container_identifier: str = Field(foreign_key="container.container_identifier", index=True)
    event_classification_type: str = Field(max_length=32)
    event_recording_timestamp: datetime


class PortExceptionLog(SQLModel, table=True):
    __tablename__ = "port_exception_log"

    exception_log_identifier: str = Field(primary_key=True, max_length=32)
    berth_terminal_name: str = Field(max_length=128)
    exception_category_type: str = Field(max_length=64)
    exception_start_timestamp: datetime
    exception_end_timestamp: datetime
    excused_penalty_days_count: int


class Claim(SQLModel, table=True):
    __tablename__ = "claim"

    dispute_claim_identifier: Optional[int] = Field(default=None, primary_key=True)
    container_identifier: str = Field(foreign_key="container.container_identifier", index=True)
    importer_identifier: str = Field(foreign_key="importer.importer_identifier", index=True)
    disputed_amount_usd: float
    dispute_reason_category: str = Field(max_length=64)
    claim_decision_status: str = Field(max_length=32)
    approved_waiver_amount_usd: float = 0.0


class DrayageJob(SQLModel, table=True):
    __tablename__ = "drayage_job"

    drayage_job_identifier: str = Field(primary_key=True, max_length=32)
    container_identifier: str = Field(foreign_key="container.container_identifier", index=True)
    assigned_truck_driver_name: str = Field(max_length=128)
    delivery_warehouse_name: str = Field(max_length=128)
    agreed_service_level_agreement_hours: int
    actual_transit_hours: Optional[float] = None
    job_completion_status: str = Field(max_length=16)
