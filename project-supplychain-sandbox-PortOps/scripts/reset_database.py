"""Dynamically seed SQLite from normalized CSV files in data/seed/."""

import csv
from datetime import date, datetime, timezone
from pathlib import Path
import types
from typing import Any, Annotated, Union, get_args, get_origin

from sqlmodel import Session, SQLModel

import supplychainops.database_models  # noqa: F401
from supplychainops.database_configuration import get_engine
from supplychainops.database_models import (
    Claim,
    Container,
    DrayageJob,
    Importer,
    PortExceptionLog,
    Shipment,
    TerminalEvent,
    Vessel,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SEED_DIRECTORY = PROJECT_ROOT / "data" / "seed"

SEED_FILE_ORDER = [
    ("importers.csv", Importer),
    ("vessels.csv", Vessel),
    ("shipments.csv", Shipment),
    ("containers.csv", Container),
    ("port_exception_logs.csv", PortExceptionLog),
    ("terminal_events.csv", TerminalEvent),
    ("claims.csv", Claim),
    ("drayage_jobs.csv", DrayageJob),
]


def _unwrap_annotation(annotation):
    origin = get_origin(annotation)
    if origin is Annotated:
        return _unwrap_annotation(get_args(annotation)[0])
    if origin in (Union, types.UnionType):
        non_none = [arg for arg in get_args(annotation) if arg is not type(None)]
        return _unwrap_annotation(non_none[0]) if non_none else annotation
    return annotation


def _coerce_field_value(field_name: str, raw_value: str, model_class) -> Any:
    if raw_value == "" or raw_value is None:
        return None
    annotation = _unwrap_annotation(model_class.model_fields[field_name].annotation)
    if annotation is date:
        return date.fromisoformat(raw_value)
    if annotation is datetime:
        parsed = datetime.fromisoformat(raw_value)
        return parsed if parsed.tzinfo else parsed.replace(tzinfo=timezone.utc)
    if annotation is int:
        return int(raw_value)
    if annotation is float:
        return float(raw_value)
    return raw_value


def _load_csv_rows(csv_path: Path, model_class) -> list[dict]:
    rows: list[dict] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        for raw_row in csv.DictReader(handle):
            coerced = {
                key: _coerce_field_value(key, value, model_class)
                for key, value in raw_row.items()
            }
            rows.append(coerced)
    return rows


def seed_database() -> None:
    engine = get_engine()
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    for csv_filename, model_class in SEED_FILE_ORDER:
        csv_path = SEED_DIRECTORY / csv_filename
        rows = _load_csv_rows(csv_path, model_class)
        with Session(engine) as session:
            for row in rows:
                session.add(model_class(**row))
            session.commit()
        print(f"Seeded {len(rows)} rows from {csv_filename}")


if __name__ == "__main__":
    seed_database()
