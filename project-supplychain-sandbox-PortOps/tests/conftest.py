"""Shared pytest fixtures with in-memory SQLite seeded from CSV files."""

from datetime import date
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import supplychainops.database_models  # noqa: F401
from scripts.reset_database import SEED_FILE_ORDER, _load_csv_rows
from supplychainops.database_configuration import get_database_session
from supplychainops.application_api_routes import get_current_calculation_date
from supplychainops.main import app

FIXED_CALCULATION_DATE = date(2026, 9, 22)
SEED_DIRECTORY = Path(__file__).resolve().parent.parent / "data" / "seed"


@pytest.fixture(autouse=True)
def fixed_calculation_date():
    app.dependency_overrides[get_current_calculation_date] = lambda: FIXED_CALCULATION_DATE
    yield
    app.dependency_overrides.pop(get_current_calculation_date, None)


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
def client(engine, monkeypatch):
    from supplychainops import main
    monkeypatch.setattr(main, "get_engine", lambda: engine)

    def override_get_database_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_database_session] = override_get_database_session
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_database_session, None)
