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
        # Sanitize error to avoid leaking credentials/passwords or server host details
        db_error = "Database connectivity check failed (verify database status and credentials)"

    overall_status = "ok" if (db_ok and is_valid) else "degraded"

    return {
        "status": overall_status,
        "service": "ULPF",
        "version": Config.ULPF_VERSION,
        "ocsf_version": Config.OCSF_VERSION,
        "db_type": Config.db_type_label(),
        "db_ok": db_ok,
        "db_error": db_error,
        "blockchain_blocks": chain.block_count(),
        "blockchain_valid": is_valid,
        "blockchain_detail": chain_detail,
        "supported_formats": ["syslog", "cef", "json", "xml", "csv", "leef"],
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
                "description": "ArcSight Common Event Format — Cisco, Palo Alto, Fortinet, Check Point",
                "detection": "Starts with CEF:",
                "example": "CEF:0|Cisco|ASA|9.1|106001|Inbound TCP connection denied|5|src=10.0.0.1 dst=192.168.1.100",
            },
            {
                "id": "leef",
                "name": "LEEF (Log Event Extended Format)",
                "description": "IBM QRadar format — LEEF 1.0 and 2.0",
                "detection": "Starts with LEEF:",
                "example": "LEEF:1.0|IBM|QRadar|7.4.0|NetworkAllow\tsrc=10.0.0.5\tdst=203.0.113.20\tsrcPort=52000\tdstPort=443",
            },
            {
                "id": "xml",
                "name": "XML",
                "description": "Windows Event Log, vendor syslog-over-XML, generic event XML",
                "detection": "Starts with <",
                "example": "<Event><EventID>5156</EventID><SrcIP>192.168.1.5</SrcIP><DstIP>10.0.0.1</DstIP><Action>Permit</Action></Event>",
            },
            {
                "id": "json",
                "name": "JSON",
                "description": "Structured JSON log objects — cloud, EDR, application events",
                "detection": "Starts with {",
                "example": '{"time":"2024-01-01T12:00:00Z","severity":3,"src_ip":"10.0.0.1","message":"Connection attempt"}',
            },
            {
                "id": "csv",
                "name": "CSV",
                "description": "Comma-separated log exports — Fortinet, pfSense, Cisco Meraki, SIEM exports",
                "detection": "Contains commas, does not match CEF/LEEF",
                "example": "timestamp,src_ip,dst_ip,protocol,action\n2024-01-15T12:00:00Z,10.0.0.5,8.8.8.8,TCP,allow",
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
        elif fmt == "xml":
            from sample.xml_log import SAMPLE_XML_LOGS
            lines = SAMPLE_XML_LOGS
        elif fmt == "csv":
            from sample.csv_log import SAMPLE_CSV_LOGS
            lines = SAMPLE_CSV_LOGS
        elif fmt == "leef":
            from sample.leef import SAMPLE_LEEF_LOGS
            lines = SAMPLE_LEEF_LOGS
        elif fmt == "all":
            from sample.syslog import SAMPLE_SYSLOGS
            from sample.cef import SAMPLE_CEF_LOGS
            from sample.json_log import SAMPLE_JSON_LOGS
            from sample.xml_log import SAMPLE_XML_LOGS
            from sample.csv_log import SAMPLE_CSV_LOGS
            from sample.leef import SAMPLE_LEEF_LOGS
            lines = (
                SAMPLE_SYSLOGS[:3] + SAMPLE_CEF_LOGS[:3]
                + SAMPLE_JSON_LOGS[:2] + SAMPLE_XML_LOGS[:2]
                + SAMPLE_CSV_LOGS[:2] + SAMPLE_LEEF_LOGS[:2]
            )
        else:
            raise HTTPException(
                status_code=404,
                detail=f"Unknown format '{fmt}'. Supported: syslog, cef, json, xml, csv, leef, all"
            )
    except ImportError as exc:
        raise HTTPException(status_code=500, detail=f"Sample module error: {exc}") from exc

    return {
        "format": fmt,
        "count": len(lines),
        "lines": lines,
        "joined": "\n".join(lines),
    }
