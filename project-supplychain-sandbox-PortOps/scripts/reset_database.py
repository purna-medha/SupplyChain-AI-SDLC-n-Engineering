"""Dynamically seed SQLite from normalized CSV files in data/seed/."""

import csv
import sqlite3
from datetime import date, datetime, timezone
from pathlib import Path
import types
from typing import Any, Annotated, Union, get_args, get_origin

from sqlmodel import Session, SQLModel
from sqlalchemy import MetaData

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


def seed_database() -> Path | None:
    """Validate seeds, back up current data, and rebuild only the eight current tables."""
    seed_batches = []
    for filename, model in SEED_FILE_ORDER:
        rows = _load_csv_rows(SEED_DIRECTORY / filename, model)
        seed_batches.append((filename, [model.model_validate(row) for row in rows]))
    engine = get_engine()
    database_path = Path(engine.url.database)
    backup_path = None
    if database_path.exists():
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        backup_path = database_path.with_name(f"{database_path.name}.{timestamp}.bak")
        with sqlite3.connect(database_path) as source, sqlite3.connect(backup_path) as backup:
            source.backup(backup)
        print(f"Backed up existing database to {backup_path}")

    # Reflect the physical schema so obsolete carrier/tariff tables are removed too.
    existing_tables = MetaData()
    existing_tables.reflect(bind=engine)
    existing_tables.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        for filename, models in seed_batches:
            session.add_all(models)
            session.flush()
            print(f"Seeded {len(models)} rows from {filename}")
        session.commit()
    return backup_path


if __name__ == "__main__":
    seed_database()
