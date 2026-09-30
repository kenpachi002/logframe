"""
POST /api/ingest  — The main entry point for the frontend.

Accepts raw log text (one or more lines), runs the full ULPF pipeline
(parse → normalize → store raw + normalized → hash → blockchain block),
and returns the batch summary plus all normalized OCSF events.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from config import Config
from integrity.blockchain import LocalHashchain
from pipeline.processor import process_batch
from storage.db import get_session
from storage.normalized_event_repo import list_normalized_events
from storage.raw_event_repo import get_raw_events_by_batch

router = APIRouter()


class IngestRequest(BaseModel):
    logs: str = Field(
        ...,
        description="Raw log text — one log entry per line. Mixed formats supported.",
        min_length=1,
    )
    source_hint: str = Field(
        "auto",
        description="Format hint: 'auto' (default), 'syslog', 'cef', or 'json'. "
                    "Auto-detection is always used; this field is informational.",
    )


@router.post("/ingest", summary="Ingest raw log lines through the full ULPF pipeline")
def ingest_logs(req: IngestRequest) -> dict[str, Any]:
    """
    Full pipeline for a batch of raw log lines submitted from the UI.

    Steps (all real — no mock data):
      1. Split submitted text into individual log lines
      2. Auto-detect format + parse each line (CEF / Syslog / JSON)
      3. Store each raw event with its SHA-256 hash
      4. Normalize each to an OCSF 1.9.0 Network Activity event
      5. Validate against the Pydantic UniversalEvent schema
      6. Store each normalized event (FK-linked to its raw event)
      7. Compute Merkle root of all raw SHA-256 hashes in the batch
      8. Append a new blockchain block anchoring the Merkle root
      9. Return batch summary + all normalized events
    """
    lines = [ln for ln in req.logs.splitlines() if ln.strip()]
    if not lines:
        raise HTTPException(status_code=422, detail="No non-empty log lines found in input.")

    blockchain = LocalHashchain(Config.BLOCKCHAIN_LEDGER_PATH)

    try:
        with get_session() as session:
            result = process_batch(
                raw_lines=lines,
                source_file="ui-ingest",
                session=session,
                blockchain=blockchain,
            )
            batch_id = result["batch_id"]

            # Fetch the normalized events that belong to this batch
            raw_events = get_raw_events_by_batch(session, batch_id)
            raw_ids = {str(r.id) for r in raw_events}

            # Get all recent normalized events and filter to this batch
            recent = list_normalized_events(session, limit=max(500, len(lines) * 2))
            events = [
                e.ocsf_json
                for e in recent
                if str(e.raw_event_id) in raw_ids
            ]

    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Pipeline error: {str(exc)}"
        ) from exc

    return {
        "batch_id": result["batch_id"],
        "event_count": result["event_count"],
        "events_normalized": result["events_normalized"],
        "errors": result.get("errors", []),
        "merkle_root": result["merkle_root"],
        "blockchain_block_index": result["blockchain_block_index"],
        "blockchain_block_hash": result["blockchain_block_hash"],
        "events": events,
    }
