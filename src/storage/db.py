"""
Database connection and session management.
Supports both PostgreSQL (production/Supabase) and SQLite (zero-config default).
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from config import Config
from storage.models import Base


def get_engine() -> Engine:
    """Create and return the SQLAlchemy engine using Config.

    SQLite: single-file DB, StaticPool so the same connection is reused
            (needed in tests and for FastAPI's threading model).
    PostgreSQL/Supabase: standard pool with pre-ping.
    """
    url = Config.db_url()

    if Config.is_sqlite():
        from sqlalchemy.pool import StaticPool
        return create_engine(
            url,
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
            echo=False,
        )

    return create_engine(
        url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        echo=False,
    )


_engine: Engine | None = None
_SessionFactory: sessionmaker | None = None


def _ensure_engine() -> Engine:
    global _engine, _SessionFactory
    if _engine is None:
        _engine = get_engine()
        _SessionFactory = sessionmaker(bind=_engine, expire_on_commit=False)
    return _engine


@contextmanager
def get_session() -> Generator[Session, None, None]:
    """Context manager that yields a database session and commits/rolls back automatically."""
    _ensure_engine()
    session: Session = _SessionFactory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def init_db() -> None:
    """
    Initialize the database schema.

    For PostgreSQL: runs the raw SQL migration first (uuid-ossp extension, indexes),
                    then creates any remaining tables via ORM.
    For SQLite:     skips the raw SQL migration (no extension needed),
                    creates all tables via ORM directly.
    """
    engine = _ensure_engine()

    if not Config.is_sqlite():
        # Run the raw SQL migration (PostgreSQL-specific: uuid extension + indexes)
        migration_file = Path(__file__).parent.parent.parent / "migrations" / "001_initial_schema.sql"
        if migration_file.exists():
            with engine.connect() as conn:
                sql = migration_file.read_text(encoding="utf-8")
                for stmt in sql.split(";"):
                    stmt = stmt.strip()
                    if stmt:
                        try:
                            conn.execute(text(stmt))
                        except Exception:
                            pass  # Ignore "already exists" errors (idempotent)
                conn.commit()

    # Create any tables not yet present (idempotent for both dialects)
    Base.metadata.create_all(engine)
    print(f"[DB] Schema initialized ({Config.db_type_label()}).")
