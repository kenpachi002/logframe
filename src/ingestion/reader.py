"""
Ingestion layer — reads raw log lines from files, stdin, or in-memory lists.
"""
from __future__ import annotations

import sys
from typing import Generator


def read_file(filepath: str) -> Generator[str, None, None]:
    """Yield non-empty, stripped lines from a log file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if line:
                yield line


def read_stdin() -> Generator[str, None, None]:
    """Yield non-empty, stripped lines from stdin."""
    for line in sys.stdin:
        line = line.strip()
        if line:
            yield line


def read_lines(lines: list[str]) -> Generator[str, None, None]:
    """Yield non-empty, stripped lines from an in-memory list (for demo/test)."""
    for line in lines:
        line = line.strip()
        if line:
            yield line


def chunk(
    lines: Generator[str, None, None], size: int
) -> Generator[list[str], None, None]:
    """
    Group a generator of lines into chunks of `size`.
    The last chunk may be smaller than `size`.
    """
    batch: list[str] = []
    for line in lines:
        batch.append(line)
        if len(batch) >= size:
            yield batch
            batch = []
    if batch:
        yield batch
