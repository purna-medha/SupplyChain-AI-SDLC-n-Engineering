"""SQLite engine setup and FastAPI session dependency injection."""

from functools import cache
from pathlib import Path
from typing import Generator

from sqlmodel import Session, create_engine

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "data" / "supplychainops.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


@cache
def get_engine():
    """Reuse one engine; each request still gets its own session."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False},
    )


def get_database_session() -> Generator[Session, None, None]:
    """FastAPI dependency — yields one request-scoped database session."""
    with Session(get_engine()) as session:
        yield session
