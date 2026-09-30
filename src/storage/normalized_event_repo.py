"""
Normalized event repository — CRUD for the normalized_events table.
"""
from __future__ import annotations

import uuid
from datetime import datetime, timezone

from sqlalchemy import desc
from sqlalchemy.orm import Session

from storage.models import NormalizedEvent


def _parse_ip(ip_str: str | None) -> str | None:
    """Return IP string if valid-looking, else None (avoids INET cast errors)."""
    if not ip_str or ip_str in ("unknown", "None"):
        return None
    return ip_str


def _epoch_to_dt(epoch: int | None) -> datetime | None:
    """Convert Unix epoch int to UTC datetime, or None if -1 / missing."""
    if epoch is None or epoch == -1:
        return None
    try:
        return datetime.fromtimestamp(int(epoch), tz=timezone.utc)
    except (OSError, OverflowError, ValueError):
        return None


def insert_normalized_event(
    session: Session,
    raw_event_id: str | uuid.UUID,
    ocsf_event: dict,
    source_format: str,
) -> NormalizedEvent:
    """
    Insert a normalized OCSF event linked to its raw event.
    Denormalizes key fields for fast indexed queries.
    """
    src_ip = _parse_ip(
        (ocsf_event.get("src_endpoint") or {}).get("ip")
    )
    dst_ip = _parse_ip(
        (ocsf_event.get("dst_endpoint") or {}).get("ip")
    )

    event = NormalizedEvent(
        id=uuid.UUID(str(ocsf_event["ulpf_event_id"])),
        raw_event_id=uuid.UUID(str(raw_event_id)),
        normalized_at=datetime.now(timezone.utc),
        source_format=source_format,
        ocsf_json=ocsf_event,
        severity_id=ocsf_event.get("severity_id"),
        activity_id=ocsf_event.get("activity_id"),
        src_ip=src_ip,
        dst_ip=dst_ip,
        event_time=_epoch_to_dt(ocsf_event.get("time")),
    )
    session.add(event)
    return event


def get_normalized_event(session: Session, event_id: str) -> NormalizedEvent | None:
    """Fetch a single NormalizedEvent by UUID string."""
    try:
        uid = uuid.UUID(event_id)
    except ValueError:
        return None
    return session.get(NormalizedEvent, uid)


def get_normalized_by_raw_id(
    session: Session, raw_event_id: str
) -> NormalizedEvent | None:
    """Return the NormalizedEvent linked to a given raw_event_id."""
    try:
        uid = uuid.UUID(raw_event_id)
    except ValueError:
        return None
    return (
        session.query(NormalizedEvent)
        .filter(NormalizedEvent.raw_event_id == uid)
        .first()
    )


def list_normalized_events(
    session: Session,
    limit: int = 100,
    offset: int = 0,
    severity_id: int | None = None,
    activity_id: int | None = None,
    src_ip: str | None = None,
    source_format: str | None = None,
) -> list[NormalizedEvent]:
    """
    Return a filtered, paginated list of NormalizedEvents (newest first).
    All filter params are optional.
    """
    q = session.query(NormalizedEvent)
    if severity_id is not None:
        q = q.filter(NormalizedEvent.severity_id == severity_id)
    if activity_id is not None:
        q = q.filter(NormalizedEvent.activity_id == activity_id)
    if src_ip:
        q = q.filter(NormalizedEvent.src_ip == src_ip)
    if source_format:
        q = q.filter(NormalizedEvent.source_format == source_format)
    return (
        q.order_by(desc(NormalizedEvent.normalized_at))
        .offset(offset)
        .limit(limit)
        .all()
    )


def count_normalized_events(session: Session) -> int:
    return session.query(NormalizedEvent).count()
