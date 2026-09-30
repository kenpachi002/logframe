"""
Pipeline Processor — orchestrates the full per-event and per-batch pipeline.

Per-event flow:
  raw line → dispatch (detect + parse) → insert raw_event → normalize → validate → insert normalized_event

Per-batch flow:
  list of lines → process each event → collect sha256 hashes → merkle root → blockchain block → integrity_batch record
"""
from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy.orm import Session

from config import Config
from integrity.blockchain import LocalHashchain
from integrity.hasher import merkle_root
from normalizer.normalizer import normalize
from parser import UnknownFormatError, dispatch
from schema.universal_event import UniversalEvent
from storage.models import IntegrityBatch, TamperCheck
from storage.normalized_event_repo import insert_normalized_event
from storage.raw_event_repo import get_raw_event, insert_raw_event


# ── Per-event processing ──────────────────────────────────────────────────────

def process_log_line(
    raw_line: str,
    source_file: str,
    batch_id: uuid.UUID,
    session: Session,
) -> dict[str, Any]:
    """
    Full pipeline for a single log line.

    Steps:
      1. Detect format + parse → parsed dict
      2. Insert raw_event (with sha256 hash)
      3. Generate UUIDs for both raw and normalized events
      4. Normalize → OCSF event dict
      5. Validate against Pydantic schema
      6. Insert normalized_event
      7. Return the OCSF event dict

    Returns the OCSF event dict on success.
    On parse error, still stores the raw event and returns an error-flagged dict.
    """
    raw_line = raw_line.strip()
    if not raw_line:
        return {}

    # ── Step 1: detect + parse ────────────────────────────────────────────────
    try:
        format_id, parsed = dispatch(raw_line)
    except UnknownFormatError as exc:
        format_id = "unknown"
        parsed = {"error_message": str(exc), "raw_data": raw_line}

    # ── Step 2: store raw event ───────────────────────────────────────────────
    raw_event = insert_raw_event(
        session=session,
        raw_data=raw_line,
        source_format=format_id,
        source_file=source_file,
        batch_id=batch_id,
    )
    session.flush()  # populate raw_event.id without full commit

    # ── Steps 3–4: assign IDs + normalize ────────────────────────────────────
    norm_event_id = str(uuid.uuid4())
    raw_event_id = str(raw_event.id)

    ocsf = normalize(
        format_id=format_id,
        parsed=parsed,
        ulpf_event_id=norm_event_id,
        ulpf_raw_event_id=raw_event_id,
        log_timezone=Config.LOG_TIMEZONE,
    )

    # ── Step 5: validate (log warnings but don't fail the pipeline) ───────────
    try:
        UniversalEvent.model_validate(ocsf)
    except Exception as exc:
        ocsf["_validation_warning"] = str(exc)

    # ── Step 6: store normalized event ───────────────────────────────────────
    insert_normalized_event(
        session=session,
        raw_event_id=raw_event_id,
        ocsf_event=ocsf,
        source_format=format_id,
    )

    return ocsf


# ── Per-batch processing ──────────────────────────────────────────────────────

def process_batch(
    raw_lines: list[str],
    source_file: str,
    session: Session,
    blockchain: LocalHashchain,
) -> dict[str, Any]:
    """
    Process a batch of raw log lines through the full pipeline.

    Steps:
      1. Generate a batch UUID
      2. Process each line (parse → normalize → store)
      3. Fetch sha256 hashes of all raw events in the batch
      4. Compute Merkle root of those hashes
      5. Append a blockchain block anchoring the Merkle root
      6. Record the IntegrityBatch in the DB
      7. Return a summary dict

    All DB writes in this batch share a single transaction (managed by caller's session context).
    """
    batch_id = uuid.uuid4()
    ocsf_events: list[dict] = []
    errors: list[str] = []

    # Process every line
    for line in raw_lines:
        if not line.strip():
            continue
        try:
            evt = process_log_line(
                raw_line=line,
                source_file=source_file,
                batch_id=batch_id,
                session=session,
            )
            if evt:
                ocsf_events.append(evt)
        except Exception as exc:
            errors.append(f"Line error: {exc} | line={line[:60]!r}")

    # Collect hashes from the raw events we just inserted (still in session)
    from storage.raw_event_repo import get_raw_events_by_batch  # local import avoids cycle
    session.flush()

    raw_events = get_raw_events_by_batch(session, str(batch_id))
    hashes = [re.sha256_hash for re in raw_events]

    # Compute Merkle root and anchor on blockchain
    root = merkle_root(hashes)
    block = blockchain.append_block(
        batch_id=str(batch_id),
        event_count=len(raw_events),
        merkle_root_hex=root,
    )

    # Record IntegrityBatch in DB
    ib = IntegrityBatch(
        id=batch_id,
        event_count=len(raw_events),
        merkle_root=root,
        blockchain_block_index=block["block_index"],
        blockchain_block_hash=block["block_hash"],
    )
    session.add(ib)

    return {
        "batch_id": str(batch_id),
        "event_count": len(raw_events),
        "events_normalized": len(ocsf_events),
        "errors": errors,
        "merkle_root": root,
        "blockchain_block_index": block["block_index"],
        "blockchain_block_hash": block["block_hash"],
    }


# ── Tamper detection ──────────────────────────────────────────────────────────

def verify_event_integrity(
    raw_event_id: str,
    session: Session,
    blockchain: LocalHashchain,
) -> dict[str, Any]:
    """
    Re-hash the stored raw_data and compare to stored sha256_hash.
    Also records the check in tamper_checks table.

    Returns a result dict with is_tampered bool and detail string.
    """
    from integrity.hasher import sha256_hash  # local import

    raw_event = get_raw_event(session, raw_event_id)
    if raw_event is None:
        return {"error": f"raw_event_id {raw_event_id!r} not found"}

    recomputed = sha256_hash(raw_event.raw_data)
    is_tampered = recomputed != raw_event.sha256_hash

    # Lookup the blockchain block for this batch
    block_index = None
    if raw_event.batch_id:
        # Find the IntegrityBatch to get the block index
        ib = session.query(IntegrityBatch).filter(
            IntegrityBatch.id == raw_event.batch_id
        ).first()
        if ib:
            block_index = ib.blockchain_block_index

    detail = "VERIFIED — raw_data hash matches stored hash" if not is_tampered else (
        "TAMPERED — raw_data has been modified since ingestion"
    )

    check = TamperCheck(
        raw_event_id=raw_event.id,
        stored_hash=raw_event.sha256_hash,
        recomputed_hash=recomputed,
        batch_id=raw_event.batch_id,
        blockchain_block_index=block_index,
        is_tampered=is_tampered,
        detail=detail,
    )
    session.add(check)

    return {
        "raw_event_id": raw_event_id,
        "stored_hash": raw_event.sha256_hash,
        "recomputed_hash": recomputed,
        "is_tampered": is_tampered,
        "blockchain_block_index": block_index,
        "detail": detail,
    }
