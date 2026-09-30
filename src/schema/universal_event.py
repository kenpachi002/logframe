"""
ULPF Universal Event Schema — Pydantic v2 model.

This is the single source of truth for:
  - Validating normalizer output.
  - FastAPI response serialization.
  - NDJSON export typing.

Matches universal_event_schema_v0.1.md and OCSF 1.9.0 Network Activity class (4001).
"""
from __future__ import annotations

from typing import Any, Optional

from pydantic import BaseModel, Field


class EndpointModel(BaseModel):
    ip: Optional[str] = None
    port: Optional[int] = None
    hostname: Optional[str] = None


class ConnectionInfoModel(BaseModel):
    direction_id: int = 0
    direction: str = "Unknown"
    protocol_name: Optional[str] = None
    protocol_num: int = -1
    protocol_ver_id: int = 4


class DeviceModel(BaseModel):
    hostname: Optional[str] = None
    vendor_name: Optional[str] = None
    product_name: Optional[str] = None
    version: Optional[str] = None
    type_id: int = 0


class ProductMeta(BaseModel):
    name: str
    version: str
    vendor_name: str


class MetadataModel(BaseModel):
    version: str = "1.9.0"
    product: ProductMeta
    source_format: str
    source_format_detail: dict[str, Any] = Field(default_factory=dict)


class UniversalEvent(BaseModel):
    # ── OCSF Base Event ───────────────────────────────────────────────────────
    time: int                               # Unix epoch seconds; -1 if unknown
    activity_id: int
    activity_name: str
    category_uid: int = 4
    category_name: str = "Network Activity"
    class_uid: int = 4001
    class_name: str = "Network Activity"
    type_uid: int
    severity_id: int                        # ULPF 1–5; -1 = unknown
    severity: str
    message: Optional[str] = None
    status_id: int
    status: str
    raw_data: str                           # COMPLETE original log line

    # ── Traceability ──────────────────────────────────────────────────────────
    ulpf_event_id: str                      # UUID of the normalized event
    ulpf_raw_event_id: str                  # UUID FK to raw_events table

    # ── Network Activity ──────────────────────────────────────────────────────
    src_endpoint: EndpointModel = Field(default_factory=EndpointModel)
    dst_endpoint: EndpointModel = Field(default_factory=EndpointModel)
    connection_info: ConnectionInfoModel = Field(default_factory=ConnectionInfoModel)
    app_name: Optional[str] = None
    app_protocol_name: Optional[str] = None

    # ── Device ────────────────────────────────────────────────────────────────
    device: DeviceModel = Field(default_factory=DeviceModel)

    # ── Metadata ──────────────────────────────────────────────────────────────
    metadata: MetadataModel

    # ── Unmapped source fields ────────────────────────────────────────────────
    unmapped: dict[str, Any] = Field(default_factory=dict)
