"""Shared pytest fixtures with in-memory SQLite seeded from CSV files."""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import supplychainops.database_models  # noqa: F401
from scripts.reset_database import SEED_FILE_ORDER, _load_csv_rows
from supplychainops.database_configuration import get_database_session
from supplychainops.domain_demurrage_calculation_engine import get_current_calculation_date
from supplychainops.main import app

FIXED_CALCULATION_DATE = date(2026, 9, 22)
SEED_DIRECTORY = (
    __import__("pathlib").Path(__file__).resolve().parent.parent / "data" / "seed"
)


@pytest.fixture(autouse=True)
def fixed_calculation_date(monkeypatch):
    for module_path in (
        "supplychainops.domain_demurrage_calculation_engine",
        "supplychainops.port_demurrage_service",
        "supplychainops.port_read_service",
        "supplychainops.port_claims_service",
    ):
        monkeypatch.setattr(
            f"{module_path}.get_current_calculation_date",
            lambda: FIXED_CALCULATION_DATE,
        )


@pytest.fixture
def engine():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        for csv_filename, model_class in SEED_FILE_ORDER:
            rows = _load_csv_rows(SEED_DIRECTORY / csv_filename, model_class)
            for row in rows:
                session.add(model_class(**row))
            session.commit()
    return test_engine


@pytest.fixture
def client(engine):
    def override_get_database_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_database_session] = override_get_database_session
    yield TestClient(app)
    app.dependency_overrides.clear()
