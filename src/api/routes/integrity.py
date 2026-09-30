"""
Integrity and blockchain verification routes.
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from config import Config
from integrity.blockchain import LocalHashchain
from pipeline.processor import verify_event_integrity
from storage.db import get_session
from storage.models import IntegrityBatch

router = APIRouter()


def _get_chain() -> LocalHashchain:
    return LocalHashchain(Config.BLOCKCHAIN_LEDGER_PATH)


# ── Request models ─────────────────────────────────────────────────────────────

class VerifyEventRequest(BaseModel):
    raw_event_id: str


# ── Routes ────────────────────────────────────────────────────────────────────

@router.post("/verify/event", summary="Verify integrity of a single raw event")
def verify_event(req: VerifyEventRequest) -> dict[str, Any]:
    with get_session() as session:
        result = verify_event_integrity(
            raw_event_id=req.raw_event_id,
            session=session,
            blockchain=_get_chain(),
        )
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/verify/chain", summary="Verify entire blockchain chain integrity")
def verify_chain() -> dict[str, Any]:
    chain = _get_chain()
    is_valid, detail = chain.verify_chain()
    return {
        "is_valid": is_valid,
        "block_count": chain.block_count(),
        "detail": detail,
    }


@router.get("/blockchain/blocks", summary="List all blockchain blocks")
def list_blocks() -> dict[str, Any]:
    chain = _get_chain()
    blocks = chain.all_blocks()
    return {"block_count": len(blocks), "blocks": blocks}


@router.get("/blockchain/blocks/{block_index}", summary="Get a single blockchain block")
def get_block(block_index: int) -> dict[str, Any]:
    chain = _get_chain()
    block = chain.get_block(block_index)
    if block is None:
        raise HTTPException(status_code=404, detail=f"Block {block_index} not found")
    return block


@router.get("/integrity/batches", summary="List integrity batches")
def list_batches() -> dict[str, Any]:
    with get_session() as session:
        batches = session.query(IntegrityBatch).order_by(IntegrityBatch.created_at.desc()).all()
        return {
            "count": len(batches),
            "batches": [
                {
                    "id": str(b.id),
                    "created_at": b.created_at.isoformat(),
                    "event_count": b.event_count,
                    "merkle_root": b.merkle_root,
                    "blockchain_block_index": b.blockchain_block_index,
                    "blockchain_block_hash": b.blockchain_block_hash,
                }
                for b in batches
            ],
        }
