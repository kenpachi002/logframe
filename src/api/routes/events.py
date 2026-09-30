"""
Event routes — query normalized OCSF events.
"""
from __future__ import annotations

from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Query

from storage.db import get_session
from storage.normalized_event_repo import (
    count_normalized_events,
    get_normalized_by_raw_id,
    get_normalized_event,
    list_normalized_events,
)
from storage.raw_event_repo import get_raw_event

router = APIRouter()


@router.get("/events", summary="List normalized events")
def list_events(
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    severity_id: Optional[int] = Query(None, description="Filter by severity 1–5"),
    activity_id: Optional[int] = Query(None, description="Filter by OCSF activity_id"),
    src_ip: Optional[str] = Query(None, description="Filter by source IP"),
    source_format: Optional[str] = Query(None, description="Filter by format: syslog|cef|json"),
) -> dict[str, Any]:
    with get_session() as session:
        events = list_normalized_events(
            session,
            limit=limit,
            offset=offset,
            severity_id=severity_id,
            activity_id=activity_id,
            src_ip=src_ip,
            source_format=source_format,
        )
        total = count_normalized_events(session)
        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "events": [e.ocsf_json for e in events],
        }


@router.get("/events/{event_id}", summary="Get a single normalized event by ID")
def get_event(event_id: str) -> dict[str, Any]:
    with get_session() as session:
        event = get_normalized_event(session, event_id)
        if event is None:
            raise HTTPException(status_code=404, detail=f"Event {event_id!r} not found")
        return event.ocsf_json


@router.get(
    "/events/{event_id}/raw",
    summary="Get the raw event linked to a normalized event (traceability)",
)
def get_raw_for_event(event_id: str) -> dict[str, Any]:
    with get_session() as session:
        norm = get_normalized_event(session, event_id)
        if norm is None:
            raise HTTPException(status_code=404, detail=f"Normalized event {event_id!r} not found")
        raw = get_raw_event(session, str(norm.raw_event_id))
        if raw is None:
            raise HTTPException(status_code=404, detail="Linked raw event not found")
        return {
            "raw_event_id": str(raw.id),
            "received_at": raw.received_at.isoformat(),
            "source_format": raw.source_format,
            "source_file": raw.source_file,
            "raw_data": raw.raw_data,
            "sha256_hash": raw.sha256_hash,
            "batch_id": str(raw.batch_id) if raw.batch_id else None,
        }
