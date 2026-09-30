"""
Raw event repository — CRUD operations for the raw_events table.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from integrity.hasher import sha256_hash
from storage.models import RawEvent


def insert_raw_event(
    session: Session,
    raw_data: str,
    source_format: str,
    source_file: str,
    batch_id: str | uuid.UUID,
) -> RawEvent:
    """
    Compute SHA-256 of raw_data, insert a new RawEvent row, return the ORM object.
    The object is added to the session but NOT committed — caller controls the transaction.
    """
    event = RawEvent(
        id=uuid.uuid4(),
        received_at=datetime.now(timezone.utc),
        source_format=source_format,
        source_file=source_file,
        raw_data=raw_data,
        sha256_hash=sha256_hash(raw_data),
        batch_id=uuid.UUID(str(batch_id)) if isinstance(batch_id, str) else batch_id,
    )
    session.add(event)
    return event


def get_raw_event(session: Session, event_id: str) -> RawEvent | None:
    """Fetch a single RawEvent by UUID string."""
    try:
        uid = uuid.UUID(event_id)
    except ValueError:
        return None
    return session.get(RawEvent, uid)


def get_raw_events_by_batch(session: Session, batch_id: str) -> list[RawEvent]:
    """Return all RawEvents belonging to the given batch_id."""
    try:
        bid = uuid.UUID(batch_id)
    except ValueError:
        return []
    return (
        session.query(RawEvent)
        .filter(RawEvent.batch_id == bid)
        .order_by(RawEvent.received_at)
        .all()
    )
