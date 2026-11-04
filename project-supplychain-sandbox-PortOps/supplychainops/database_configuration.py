"""SQLite engine setup and FastAPI session dependency injection."""

from pathlib import Path
from typing import Generator

from sqlmodel import Session, create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "supplychainops.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


def get_engine(echo: bool = False):
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(
        DATABASE_URL,
        echo=echo,
        connect_args={"check_same_thread": False},
    )


def get_session_factory(engine=None):
    engine = engine or get_engine()
    return Session(engine)


def get_database_session() -> Generator[Session, None, None]:
    """FastAPI dependency — yields one request-scoped database session."""
    with get_session_factory() as session:
        yield session
