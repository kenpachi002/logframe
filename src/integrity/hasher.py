"""
SHA-256 hashing and Merkle root computation for ULPF integrity layer.
"""
from __future__ import annotations

import hashlib


def sha256_hash(data: str) -> str:
    """Return the SHA-256 hex digest of a UTF-8 encoded string."""
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def merkle_root(hashes: list[str]) -> str:
    """
    Compute a Merkle root from a list of SHA-256 hex strings.

    Edge cases:
      - Empty list  → hash of the literal string "EMPTY_BATCH"
      - Single hash → returned as-is (it is its own root)
      - Odd count   → last hash is duplicated before pairing

    Algorithm:
      Pairs are hashed as SHA256(left_hex_string + right_hex_string),
      i.e. the two hex strings are concatenated (not their raw bytes).
    """
    if not hashes:
        return sha256_hash("EMPTY_BATCH")

    level = list(hashes)

    while len(level) > 1:
        if len(level) % 2 == 1:
            level.append(level[-1])  # duplicate last if odd

        next_level: list[str] = []
        for i in range(0, len(level), 2):
            combined = level[i] + level[i + 1]
            next_level.append(sha256_hash(combined))
        level = next_level

    return level[0]
