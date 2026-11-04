"""Read-path queries — SELECT only, returns ORM rows or overview dicts."""

from dataclasses import dataclass
from typing import List, Optional

from sqlmodel import Session, select

from supplychainops.database_models import (
    Claim,
    Container,
    DrayageJob,
    Importer,
    Shipment,
    Vessel,
)
from supplychainops.domain_demurrage_calculation_engine import (
    calculate_container_dwell_days,
    calculate_overdue_days_count,
    derive_container_status_label,
    get_current_calculation_date,
)


class ContainerContextNotFoundError(LookupError):
    """Raised when container, shipment, vessel, or importer cannot be resolved."""


@dataclass(frozen=True)
class ContainerContext:
    """Everything needed to reason about one container at the port."""

    container: Container
    shipment: Shipment
    vessel: Vessel
    importer: Importer


def fetch_importers(session: Session) -> List[Importer]:
    return list(session.exec(select(Importer)).all())


def load_container_context(session: Session, container_identifier: str) -> ContainerContext:
    """Load container and its shipment, vessel, and importer in one query.

    container → shipment → vessel + importer
    """
    statement = (
        select(Container, Shipment, Vessel, Importer)
        .join(Shipment, Container.bill_of_lading_number == Shipment.bill_of_lading_number)
        .join(Vessel, Shipment.vessel_identifier == Vessel.vessel_identifier)
        .join(Importer, Shipment.importer_identifier == Importer.importer_identifier)
        .where(Container.container_identifier == container_identifier)
    )
    row = session.exec(statement).first()
    if row is None:
        raise ContainerContextNotFoundError("Container context not found")

    container, shipment, vessel, importer = row
    container_context = ContainerContext(
        container=container,
        shipment=shipment,
        vessel=vessel,
        importer=importer,
    )
    return container_context


def fetch_containers_for_importer(
    session: Session,
    importer_identifier: str,
    status_filter: Optional[str] = None,
) -> List[dict]:
    if session.get(Importer, importer_identifier) is None:
        raise ContainerContextNotFoundError("Importer not found")

    calculation_date = get_current_calculation_date()
    statement = (
        select(Container)
        .join(Shipment, Container.bill_of_lading_number == Shipment.bill_of_lading_number)
        .where(Shipment.importer_identifier == importer_identifier)
    )
    containers = session.exec(statement).all()

    overview_rows: List[dict] = []
    for container in containers:
        # How long has this container been at the terminal?
        dwell_days = calculate_container_dwell_days(
            container.vessel_discharge_date,
            container.gate_out_date,
            calculation_date,
        )

        # Is it past the free-day allowance?
        overdue_days = calculate_overdue_days_count(
            dwell_days,
            container.free_days_allowed,
        )

        # What status should the portal show?
        status_label = derive_container_status_label(
            container.gate_out_date,
            overdue_days,
        )

        if status_filter is not None and status_label != status_filter:
            continue

        overview_rows.append(
            {
                "container_identifier": container.container_identifier,
                "bill_of_lading_number": container.bill_of_lading_number,
                "importer_identifier": importer_identifier,
                "container_size_type": container.container_size_type,
                "cargo_classification_type": container.cargo_classification_type,
                "vessel_discharge_date": container.vessel_discharge_date,
                "gate_out_date": container.gate_out_date,
                "free_days_allowed": container.free_days_allowed,
                "container_dwell_days": dwell_days,
                "container_status_label": status_label,
            }
        )

    return overview_rows


def fetch_drayage_jobs(
    session: Session,
    assigned_driver_name_filter: Optional[str] = None,
) -> List[DrayageJob]:
    statement = select(DrayageJob)
    if assigned_driver_name_filter:
        statement = statement.where(
            DrayageJob.assigned_truck_driver_name == assigned_driver_name_filter
        )
    return list(session.exec(statement).all())


def fetch_claims(
    session: Session,
    claim_decision_status_filter: Optional[str] = None,
) -> List[Claim]:
    statement = select(Claim)
    if claim_decision_status_filter:
        statement = statement.where(
            Claim.claim_decision_status == claim_decision_status_filter
        )
    return list(session.exec(statement).all())
