"""
Raw event routes.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from storage.db import get_session
from storage.models import RawBatchPayload
from storage.raw_event_repo import get_raw_event, get_raw_events_by_batch

router = APIRouter()


@router.get("/raw/{raw_event_id}", summary="Get a raw event by ID")
def get_raw(raw_event_id: str) -> dict[str, Any]:
    with get_session() as session:
        raw = get_raw_event(session, raw_event_id)
        if raw is None:
            raise HTTPException(status_code=404, detail=f"Raw event {raw_event_id!r} not found")
        return {
            "raw_event_id": str(raw.id),
            "received_at": raw.received_at.isoformat(),
            "source_format": raw.source_format,
            "source_file": raw.source_file,
            "raw_data": raw.raw_data,
            "sha256_hash": raw.sha256_hash,
            "batch_id": str(raw.batch_id) if raw.batch_id else None,
        }


@router.get("/raw/batch/{batch_id}", summary="Get all raw events in a batch")
def get_batch_raw(batch_id: str) -> dict[str, Any]:
    with get_session() as session:
        try:
            payload = session.get(RawBatchPayload, batch_id)
        except ValueError:
            payload = None
        raws = get_raw_events_by_batch(session, batch_id)
        return {
            "batch_id": batch_id,
            "count": len(raws),
            "raw_payload": payload.raw_payload if payload else None,
            "raw_payload_sha256": payload.sha256_hash if payload else None,
            "events": [
                {
                    "raw_event_id": str(r.id),
                    "source_format": r.source_format,
                    "sha256_hash": r.sha256_hash,
                    "raw_data": r.raw_data,
                }
                for r in raws
            ],
        }
