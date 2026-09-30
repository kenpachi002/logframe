"""
Local Append-Only Hashchain Ledger for ULPF.

Design:
  - File: blockchain_ledger/chain.jsonl  (one JSON object per line)
  - Each line is a "block" containing its own hash and the previous block's hash.
  - Modifying any block changes its block_hash, breaking the prev_block_hash
    link in all subsequent blocks — making tampering detectable.
  - No external dependencies; runs fully offline (air-gap safe).

Block structure:
  {
    "block_index":    int,
    "batch_id":       str (UUID),
    "event_count":    int,
    "merkle_root":    str (64-char hex),
    "timestamp":      str (ISO 8601 UTC),
    "prev_block_hash": str (64-char hex),
    "block_hash":     str (64-char hex)  ← SHA256 of the 6 fields above joined
  }
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from integrity.hasher import sha256_hash

GENESIS_PREV_HASH = "0" * 64


def _now_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class LocalHashchain:
    """Append-only JSON-lines hashchain stored as a local file."""

    def __init__(self, ledger_path: str) -> None:
        self.path = Path(ledger_path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _last_block(self) -> dict | None:
        """Return the last block in the chain, or None if empty."""
        if not self.path.exists():
            return None
        last = None
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    last = json.loads(line)
        return last

    @staticmethod
    def _compute_block_hash(
        block_index: int,
        batch_id: str,
        event_count: int,
        merkle_root: str,
        timestamp: str,
        prev_block_hash: str,
    ) -> str:
        """
        Canonical block hash = SHA-256 of the pipe-joined canonical fields.
        Changing ANY field changes this hash.
        """
        canonical = "|".join([
            str(block_index),
            batch_id,
            str(event_count),
            merkle_root,
            timestamp,
            prev_block_hash,
        ])
        return sha256_hash(canonical)

    # ── Public API ─────────────────────────────────────────────────────────────

    def append_block(
        self,
        batch_id: str,
        event_count: int,
        merkle_root_hex: str,
    ) -> dict:
        """
        Append a new block to the chain.

        Returns the complete block dict (including block_index and block_hash).
        Thread-safety: callers should use an external lock for concurrent writers.
        """
        last = self._last_block()
        if last is None:
            block_index = 0
            prev_hash = GENESIS_PREV_HASH
        else:
            block_index = last["block_index"] + 1
            prev_hash = last["block_hash"]

        timestamp = _now_utc()
        block_hash = self._compute_block_hash(
            block_index, batch_id, event_count, merkle_root_hex, timestamp, prev_hash
        )

        block = {
            "block_index": block_index,
            "batch_id": batch_id,
            "event_count": event_count,
            "merkle_root": merkle_root_hex,
            "timestamp": timestamp,
            "prev_block_hash": prev_hash,
            "block_hash": block_hash,
        }

        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(block) + "\n")

        return block

    def verify_chain(self) -> tuple[bool, str]:
        """
        Verify the entire chain for integrity.

        Checks:
          1. Each block's stored block_hash matches the recomputed hash.
          2. Each block's prev_block_hash matches the previous block's block_hash.
          3. Genesis block has prev_block_hash == '0' * 64.

        Returns:
          (True,  "OK") if the chain is intact.
          (False, "Tampered at block N: <reason>") if any block fails.
        """
        if not self.path.exists():
            return True, "Empty chain (no blocks)"

        prev_hash = GENESIS_PREV_HASH
        prev_index = -1

        with self.path.open("r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue

                try:
                    block = json.loads(line)
                except json.JSONDecodeError as exc:
                    return False, f"Corrupt JSON at line {line_num}: {exc}"

                idx = block["block_index"]

                # Check sequential index
                if idx != prev_index + 1:
                    return False, f"Block {idx}: non-sequential index (expected {prev_index + 1})"

                # Check prev_block_hash linkage
                if block["prev_block_hash"] != prev_hash:
                    return False, (
                        f"Block {idx}: prev_block_hash mismatch "
                        f"(expected {prev_hash[:16]}..., got {block['prev_block_hash'][:16]}...)"
                    )

                # Recompute and verify block_hash
                expected_hash = self._compute_block_hash(
                    idx,
                    block["batch_id"],
                    block["event_count"],
                    block["merkle_root"],
                    block["timestamp"],
                    block["prev_block_hash"],
                )
                if block["block_hash"] != expected_hash:
                    return False, (
                        f"Block {idx}: block_hash mismatch — block has been tampered"
                    )

                prev_hash = block["block_hash"]
                prev_index = idx

        if prev_index == -1:
            return True, "Empty chain (no blocks)"

        return True, f"OK — {prev_index + 1} block(s) verified"

    def get_block(self, block_index: int) -> dict | None:
        """Return the block at the given index, or None if not found."""
        if not self.path.exists():
            return None
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                block = json.loads(line)
                if block["block_index"] == block_index:
                    return block
        return None

    def all_blocks(self) -> list[dict]:
        """Return all blocks as a list (oldest first)."""
        if not self.path.exists():
            return []
        blocks = []
        with self.path.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    blocks.append(json.loads(line))
        return blocks

    def block_count(self) -> int:
        return len(self.all_blocks())
