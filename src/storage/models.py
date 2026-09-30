"""
SQLAlchemy ORM models — dialect-agnostic for both PostgreSQL and SQLite.

Type strategy:
  UUID:  stored as CHAR(36) string in both dialects (TypeDecorator handles conversion)
  JSONB: SQLAlchemy JSON type (uses JSONB on Postgres, TEXT on SQLite)
  INET:  String(45) — stores IPv4 and IPv6 addresses in both dialects
"""
from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    SmallInteger,
    String,
    Text,
    TypeDecorator,
    CHAR,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


# ── Dialect-agnostic UUID type ─────────────────────────────────────────────────

class UUIDType(TypeDecorator):
    """
    Stores UUIDs as CHAR(36) strings in both SQLite and PostgreSQL.
    Returns uuid.UUID objects to Python.
    """
    impl = CHAR(36)
    cache_ok = True

    def process_bind_param(self, value: Any, dialect: Any) -> str | None:
        if value is None:
            return None
        if isinstance(value, uuid.UUID):
            return str(value)
        return str(uuid.UUID(str(value)))

    def process_result_value(self, value: Any, dialect: Any) -> uuid.UUID | None:
        if value is None:
            return None
        return uuid.UUID(str(value))


# ── Base ───────────────────────────────────────────────────────────────────────

class Base(DeclarativeBase):
    pass


# ── Models ─────────────────────────────────────────────────────────────────────

class RawEvent(Base):
    """
    Stores the complete original log line exactly as received — before any processing.
    This is the immutable source of truth for tamper detection.
    """
    __tablename__ = "raw_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType, primary_key=True, default=uuid.uuid4
    )
    received_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    source_format: Mapped[str] = mapped_column(String(32), nullable=False)
    source_file: Mapped[str | None] = mapped_column(Text, nullable=True)
    raw_data: Mapped[str] = mapped_column(Text, nullable=False)
    sha256_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    batch_id: Mapped[uuid.UUID | None] = mapped_column(
        UUIDType, nullable=True, index=True
    )

    # Relationships
    normalized_event: Mapped[NormalizedEvent | None] = relationship(
        "NormalizedEvent", back_populates="raw_event", uselist=False, lazy="select"
    )
    tamper_checks: Mapped[list[TamperCheck]] = relationship(
        "TamperCheck", back_populates="raw_event", lazy="select"
    )


class NormalizedEvent(Base):
    """
    Stores the OCSF-normalized event linked back to its raw source via raw_event_id.
    """
    __tablename__ = "normalized_events"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType, primary_key=True, default=uuid.uuid4
    )
    raw_event_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType,
        ForeignKey("raw_events.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    normalized_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    source_format: Mapped[str] = mapped_column(String(32), nullable=False)
    ocsf_json: Mapped[dict] = mapped_column(JSON, nullable=False)

    # Denormalized columns for fast filtering
    severity_id: Mapped[int | None] = mapped_column(SmallInteger, nullable=True, index=True)
    activity_id: Mapped[int | None] = mapped_column(SmallInteger, nullable=True, index=True)
    src_ip: Mapped[str | None] = mapped_column(String(45), nullable=True, index=True)
    dst_ip: Mapped[str | None] = mapped_column(String(45), nullable=True, index=True)
    event_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, index=True
    )

    # Relationships
    raw_event: Mapped[RawEvent] = relationship(
        "RawEvent", back_populates="normalized_event"
    )


class IntegrityBatch(Base):
    """
    Tracks a batch of raw events that were Merkle-hashed and anchored on the blockchain.
    """
    __tablename__ = "integrity_batches"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType, primary_key=True, default=uuid.uuid4
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    event_count: Mapped[int] = mapped_column(Integer, nullable=False)
    merkle_root: Mapped[str] = mapped_column(String(64), nullable=False)
    blockchain_block_index: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    blockchain_block_hash: Mapped[str | None] = mapped_column(String(64), nullable=True)


class TamperCheck(Base):
    """
    Records every tamper-detection check for auditability.
    """
    __tablename__ = "tamper_checks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType, primary_key=True, default=uuid.uuid4
    )
    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    raw_event_id: Mapped[uuid.UUID] = mapped_column(
        UUIDType,
        ForeignKey("raw_events.id"),
        nullable=False,
        index=True,
    )
    stored_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    recomputed_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    batch_id: Mapped[uuid.UUID | None] = mapped_column(UUIDType, nullable=True)
    blockchain_block_index: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    is_tampered: Mapped[bool] = mapped_column(Boolean, nullable=False)
    detail: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Relationships
    raw_event: Mapped[RawEvent] = relationship("RawEvent", back_populates="tamper_checks")
