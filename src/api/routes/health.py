"""
Health and utility routes.

GET /api/health         — Backend status, DB type, blockchain stats
GET /api/formats        — Supported log formats
GET /api/samples/{fmt}  — Sample log lines for the given format (for the UI "Load Sample" button)
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from config import Config
from integrity.blockchain import LocalHashchain

router = APIRouter()


@router.get("/health", summary="Backend health check and system info")
def health() -> dict[str, Any]:
    """Returns backend liveness plus key system state for the UI status bar."""
    chain = LocalHashchain(Config.BLOCKCHAIN_LEDGER_PATH)
    is_valid, chain_detail = chain.verify_chain()

    # Check DB connectivity
    db_ok = True
    db_error = None
    try:
        from storage.db import get_session
        with get_session() as session:
            session.execute(__import__("sqlalchemy").text("SELECT 1"))
    except Exception as exc:
        db_ok = False
        db_error = str(exc)

    return {
        "status": "ok",
        "service": "ULPF",
        "version": Config.ULPF_VERSION,
        "ocsf_version": Config.OCSF_VERSION,
        "db_type": Config.db_type_label(),
        "db_ok": db_ok,
        "db_error": db_error,
        "blockchain_blocks": chain.block_count(),
        "blockchain_valid": is_valid,
        "blockchain_detail": chain_detail,
        "supported_formats": ["syslog", "cef", "json"],
    }


@router.get("/formats", summary="List supported log formats")
def list_formats() -> dict[str, Any]:
    """Returns the list of supported log formats and their detection rules."""
    return {
        "formats": [
            {
                "id": "syslog",
                "name": "Syslog",
                "description": "RFC 3164 and RFC 5424 syslog messages",
                "detection": "Starts with <NNN> priority prefix",
                "example": "<134>Jan  1 12:00:00 fw01 kernel: DROP SRC=1.2.3.4",
            },
            {
                "id": "cef",
                "name": "CEF (Common Event Format)",
                "description": "ArcSight Common Event Format — used by Cisco, Palo Alto, Fortinet, Check Point",
                "detection": "Starts with CEF:",
                "example": "CEF:0|Cisco|ASA|9.1|106001|Inbound TCP connection denied|5|src=10.0.0.1 dst=192.168.1.100",
            },
            {
                "id": "json",
                "name": "JSON",
                "description": "Structured JSON log objects",
                "detection": "Starts with {",
                "example": '{"time":"2024-01-01T12:00:00Z","severity":3,"src_ip":"10.0.0.1","message":"Connection attempt"}',
            },
        ]
    }


@router.get("/samples/{fmt}", summary="Get sample log lines for a given format")
def get_samples(fmt: str) -> dict[str, Any]:
    """Returns real sample log lines from the built-in sample library."""
    fmt = fmt.lower().strip()
    try:
        if fmt == "syslog":
            from sample.syslog import SAMPLE_SYSLOGS
            lines = SAMPLE_SYSLOGS
        elif fmt == "cef":
            from sample.cef import SAMPLE_CEF_LOGS
            lines = SAMPLE_CEF_LOGS
        elif fmt == "json":
            from sample.json_log import SAMPLE_JSON_LOGS
            lines = SAMPLE_JSON_LOGS
        elif fmt == "all":
            from sample.syslog import SAMPLE_SYSLOGS
            from sample.cef import SAMPLE_CEF_LOGS
            from sample.json_log import SAMPLE_JSON_LOGS
            lines = SAMPLE_SYSLOGS[:4] + SAMPLE_CEF_LOGS[:3] + SAMPLE_JSON_LOGS[:2]
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown format '{fmt}'. Supported: syslog, cef, json, all"
            )
    except ImportError as exc:
        raise HTTPException(status_code=500, detail=f"Sample module error: {exc}") from exc

    return {
        "format": fmt,
        "count": len(lines),
        "lines": lines,
        "joined": "\n".join(lines),
    }
