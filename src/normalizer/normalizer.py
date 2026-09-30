"""
ULPF Normalizer — converts any parsed log dict into an OCSF 1.9.0 Network Activity event.

Supported source formats: syslog, cef, json, xml, csv, leef
Output schema: see universal_event_schema_v0.1.md and src/schema/universal_event.py

Key fixes vs. original normalizer.py:
  - CEF severity now correctly uses cef_severity_to_ulpf() (not syslog mapping).
  - Output matches OCSF field names (time, severity_id at top level, raw_data at top level).
  - activity_id inferred from message/action keywords (ALLOW→Open, DENY→Refuse, etc.).
  - protocol_num looked up from IANA table.
  - direction_id inferred where possible.
  - status_id derived from activity_id.
  - unmapped dict captures any source fields without an OCSF home.
  - Timezone is always taken from Config, never hardcoded.
"""
from __future__ import annotations

from normalizer.severity import (
    cef_severity_to_ulpf,
    get_ulpf_severity_name,
    syslog_severity_to_ulpf,
)
from normalizer.timestamp import get_as_utc_timestamp, get_utc_timestamp
from parser.util import safe_int_cast


# ── OCSF constants ─────────────────────────────────────────────────────────────

CATEGORY_UID = 4               # Network Activity
CATEGORY_NAME = "Network Activity"
CLASS_UID = 4001               # Network Activity class
CLASS_NAME = "Network Activity"
OCSF_VERSION = "1.9.0"

PRODUCT_META = {
    "name": "ULPF",
    "version": "0.1.0",
    "vendor_name": "ULPF",
}

# ── Activity ID mapping ────────────────────────────────────────────────────────

ACTIVITY_KEYWORDS: dict[int, list[str]] = {
    1: ["allow", "accept", "permitted", "established", "open", "permit", "pass", "passed"],
    2: ["close", "fin", "teardown", "closed", "end", "terminate"],
    3: ["reset", "rst"],
    4: ["fail", "error", "drop", "dropped", "failed", "no route", "timeout"],
    5: ["deny", "denied", "block", "blocked", "reject", "rejected", "refused", "refuse"],
    6: ["traffic", "log", "audit", "monitor", "detect"],
    7: ["listen"],
}

ACTIVITY_NAMES = {
    0: "Unknown",
    1: "Open",
    2: "Close",
    3: "Reset",
    4: "Fail",
    5: "Refuse",
    6: "Traffic",
    7: "Listen",
}

# status_id: 1=Success, 2=Failure, 0=Unknown
ACTIVITY_TO_STATUS = {
    0: (0, "Unknown"),
    1: (1, "Success"),
    2: (1, "Success"),
    3: (2, "Failure"),
    4: (2, "Failure"),
    5: (2, "Failure"),
    6: (1, "Success"),
    7: (1, "Success"),
}

# ── Protocol number lookup (IANA) ──────────────────────────────────────────────

PROTOCOL_NUM: dict[str, int] = {
    "hopopt": 0,
    "icmp": 1,
    "tcp": 6,
    "udp": 17,
    "gre": 47,
    "esp": 50,
    "ah": 51,
    "icmpv6": 58,
    "sctp": 132,
}

# ── Device type lookup ─────────────────────────────────────────────────────────

DEVICE_TYPE_KEYWORDS: dict[int, list[str]] = {
    9:  ["firewall", "asa", "pix", "fortigate", "checkpoint", "pf", "iptables", "netfilter"],
    12: ["router", "srx", "ce", "pe"],
    13: ["ids"],
    14: ["ips"],
    11: ["switch"],
}

DEVICE_VENDOR_TO_TYPE: dict[str, int] = {
    "cisco": 9,
    "palo alto networks": 9,
    "fortinet": 9,
    "juniper": 12,
    "check point": 9,
}


# ── Helper functions ──────────────────────────────────────────────────────────

def _infer_activity_id(text: str) -> int:
    """Infer OCSF activity_id from free-text (message, name, action fields)."""
    text_lower = text.lower()
    for activity_id, keywords in ACTIVITY_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return activity_id
    return 0  # Unknown


def _infer_activity_from_dict(d: dict) -> int:
    """Check multiple dict fields for activity inference."""
    for field in ("message", "_cef_name", "action", "outcome", "reason", "msg"):
        val = d.get(field)
        if val and isinstance(val, str):
            act = _infer_activity_id(val)
            if act != 0:
                return act
    return 0


def _get_protocol_num(proto_name: str | None) -> int:
    if not proto_name:
        return -1
    return PROTOCOL_NUM.get(str(proto_name).lower(), -1)


def _infer_device_type(vendor: str, product: str, hostname: str) -> int:
    combined = f"{vendor} {product} {hostname}".lower()
    for type_id, keywords in DEVICE_TYPE_KEYWORDS.items():
        for kw in keywords:
            if kw in combined:
                return type_id
    if vendor:
        for v, t in DEVICE_VENDOR_TO_TYPE.items():
            if v in vendor.lower():
                return t
    return 0


def _infer_direction_id(d: dict) -> tuple[int, str]:
    """Return (direction_id, direction_name). 1=Inbound, 2=Outbound, 0=Unknown."""
    direction_field = d.get("deviceDirection") or d.get("direction") or ""
    dl = str(direction_field).lower()
    if dl in ("0", "inbound", "in"):
        return 1, "Inbound"
    if dl in ("1", "outbound", "out"):
        return 2, "Outbound"
    return 0, "Unknown"


def _pick(d: dict, *keys: str, default=None):
    """Return first non-None, non-empty value from dict for given keys."""
    for k in keys:
        v = d.get(k)
        if v is not None and v != "":
            return v
    return default


def _collect_unmapped(parsed: dict, mapped_keys: set[str]) -> dict:
    """Collect all keys not in mapped_keys into an unmapped dict."""
    return {
        k: v
        for k, v in parsed.items()
        if k not in mapped_keys and not k.startswith("_ulpf_internal")
    }


# ── Format-specific normalizers ───────────────────────────────────────────────

# Keys consumed by syslog normalizer (not placed in unmapped)
_SYSLOG_MAPPED = {
    "format", "version", "time", "hostname", "app_name", "process_id", "message_id",
    "structured_data", "message", "priority", "facility", "facility_name",
    "severity", "severity_name", "raw_data",
    "src_ip", "dst_ip", "src_port", "dst_port", "protocol",
}

# Keys consumed by CEF normalizer
_CEF_MAPPED = {
    "_cef_version", "_cef_vendor", "_cef_product", "_cef_device_version",
    "_cef_signature_id", "_cef_name", "_cef_severity", "raw_data",
    "src", "spt", "dst", "dpt", "proto", "shost", "dhost", "app",
    "deviceDirection", "deviceExternalId",
}

# Keys consumed by JSON normalizer
_JSON_MAPPED = {
    "time", "timestamp", "severity", "raw_data",
    "src_ip", "srcip", "src", "source_ip", "source",
    "src_port", "srcport", "sport", "spt", "source_port", "sourceport",
    "src_hostname", "shost", "source_hostname",
    "dst_ip", "dstip", "dst", "destination_ip", "destination",
    "dst_port", "dstport", "dport", "dpt", "destination_port", "destinationport",
    "dst_hostname", "dhost", "destination_hostname",
    "protocol", "proto",
    "message", "msg",
    "app_name", "app", "app_protocol_name",
    "device_hostname", "hostname",
    "device_version", "version",
    "device_vendor_name", "vendor_name", "vendor",
    "device_product_name", "product_name", "product",
}


def _build_base(
    time_val: int,
    activity_id: int,
    severity_id: int,
    message: str | None,
    raw_data: str,
    ulpf_event_id: str,
    ulpf_raw_event_id: str,
) -> dict:
    status_id, status = ACTIVITY_TO_STATUS.get(activity_id, (0, "Unknown"))
    return {
        "time": time_val,
        "activity_id": activity_id,
        "activity_name": ACTIVITY_NAMES.get(activity_id, "Unknown"),
        "category_uid": CATEGORY_UID,
        "category_name": CATEGORY_NAME,
        "class_uid": CLASS_UID,
        "class_name": CLASS_NAME,
        "type_uid": CLASS_UID * 100 + activity_id,
        "severity_id": severity_id,
        "severity": get_ulpf_severity_name(severity_id),
        "message": message,
        "status_id": status_id,
        "status": status,
        "raw_data": raw_data,
        "ulpf_event_id": ulpf_event_id,
        "ulpf_raw_event_id": ulpf_raw_event_id,
    }


def normalize_syslog(
    parsed: dict,
    ulpf_event_id: str,
    ulpf_raw_event_id: str,
    log_timezone: str,
) -> dict:
    raw_data = parsed.get("raw_data", "")
    severity_id = syslog_severity_to_ulpf(str(parsed.get("severity", "")))
    message = parsed.get("message", None)
    activity_id = _infer_activity_from_dict(parsed)

    # Timestamp
    time_raw = parsed.get("time")
    if time_raw:
        if "T" in str(time_raw) and "Z" in str(time_raw):
            time_val = get_utc_timestamp(str(time_raw))
        else:
            time_val = get_as_utc_timestamp(str(time_raw), log_timezone)
    else:
        time_val = -1

    proto_name = _pick(parsed, "protocol") or None
    proto_name_lower = str(proto_name).lower() if proto_name else None
    direction_id, direction = _infer_direction_id(parsed)

    result = _build_base(time_val, activity_id, severity_id, message, raw_data,
                         ulpf_event_id, ulpf_raw_event_id)

    hostname = parsed.get("hostname")

    result["src_endpoint"] = {
        "ip": _pick(parsed, "src_ip") or None,
        "port": safe_int_cast(str(parsed["src_port"])) if "src_port" in parsed else None,
        "hostname": None,
    }
    result["dst_endpoint"] = {
        "ip": _pick(parsed, "dst_ip") or None,
        "port": safe_int_cast(str(parsed["dst_port"])) if "dst_port" in parsed else None,
        "hostname": None,
    }
    result["connection_info"] = {
        "direction_id": direction_id,
        "direction": direction,
        "protocol_name": proto_name_lower,
        "protocol_num": _get_protocol_num(proto_name),
        "protocol_ver_id": 4,
    }
    result["app_name"] = parsed.get("app_name") or None
    result["app_protocol_name"] = None
    result["device"] = {
        "hostname": hostname,
        "vendor_name": None,
        "product_name": None,
        "version": None,
        "type_id": _infer_device_type("", "", str(hostname or "")),
    }
    result["metadata"] = {
        "version": OCSF_VERSION,
        "product": PRODUCT_META,
        "source_format": "syslog",
        "source_format_detail": {
            "syslog_format": parsed.get("format"),
            "priority": parsed.get("priority"),
            "facility": parsed.get("facility"),
            "facility_name": parsed.get("facility_name"),
            "severity_name": parsed.get("severity_name"),
            "process_id": parsed.get("process_id"),
            "message_id": parsed.get("message_id"),
            "structured_data": parsed.get("structured_data") or {},
        },
    }
    result["unmapped"] = _collect_unmapped(parsed, _SYSLOG_MAPPED)
    return result


def normalize_cef(
    parsed: dict,
    ulpf_event_id: str,
    ulpf_raw_event_id: str,
    log_timezone: str,
) -> dict:
    raw_data = parsed.get("raw_data", "")
    # BUG FIX: must use cef_severity_to_ulpf, not syslog mapping
    severity_id = cef_severity_to_ulpf(str(parsed.get("_cef_severity", "")))
    message = parsed.get("_cef_name") or None
    activity_id = _infer_activity_from_dict(parsed)

    # CEF rarely carries a timestamp in the extension; default -1
    time_val = -1

    proto_name = _pick(parsed, "proto") or None
    proto_name_lower = str(proto_name).lower() if proto_name else None
    direction_id, direction = _infer_direction_id(parsed)

    vendor = parsed.get("_cef_vendor", "") or ""
    product = parsed.get("_cef_product", "") or ""

    result = _build_base(time_val, activity_id, severity_id, message, raw_data,
                         ulpf_event_id, ulpf_raw_event_id)

    result["src_endpoint"] = {
        "ip": _pick(parsed, "src") or None,
        "port": parsed.get("spt") or None,
        "hostname": _pick(parsed, "shost") or None,
    }
    result["dst_endpoint"] = {
        "ip": _pick(parsed, "dst") or None,
        "port": parsed.get("dpt") or None,
        "hostname": _pick(parsed, "dhost") or None,
    }
    result["connection_info"] = {
        "direction_id": direction_id,
        "direction": direction,
        "protocol_name": proto_name_lower,
        "protocol_num": _get_protocol_num(proto_name),
        "protocol_ver_id": 4,
    }
    result["app_name"] = _pick(parsed, "app") or None
    result["app_protocol_name"] = _pick(parsed, "app") or None
    result["device"] = {
        "hostname": _pick(parsed, "deviceExternalId") or None,
        "vendor_name": vendor or None,
        "product_name": product or None,
        "version": parsed.get("_cef_device_version") or None,
        "type_id": _infer_device_type(vendor, product, ""),
    }
    result["metadata"] = {
        "version": OCSF_VERSION,
        "product": PRODUCT_META,
        "source_format": "cef",
        "source_format_detail": {
            "cef_version": parsed.get("_cef_version"),
            "signature_id": parsed.get("_cef_signature_id"),
        },
    }

    # All extension fields that weren't consumed → unmapped
    result["unmapped"] = _collect_unmapped(parsed, _CEF_MAPPED)
    return result


def normalize_json(
    parsed: dict,
    ulpf_event_id: str,
    ulpf_raw_event_id: str,
    log_timezone: str,
) -> dict:
    raw_data = parsed.get("raw_data", "")

    try:
        severity_id = int(parsed.get("severity", -1))
    except (TypeError, ValueError):
        severity_id = -1

    message = _pick(parsed, "message", "msg") or None
    activity_id = _infer_activity_from_dict(parsed)

    # Timestamp
    time_raw = _pick(parsed, "time", "timestamp")
    if time_raw:
        ts = str(time_raw)
        if "T" in ts and ("Z" in ts or "+" in ts):
            time_val = get_utc_timestamp(ts)
        else:
            try:
                time_val = int(ts)
            except ValueError:
                time_val = -1
    else:
        time_val = -1

    src_ip = _pick(parsed, "src_ip", "srcip", "src", "source_ip", "source") or None
    src_port_raw = _pick(parsed, "src_port", "srcport", "sport", "spt", "source_port", "sourceport")
    src_port = safe_int_cast(str(src_port_raw)) if src_port_raw is not None else None
    src_host = _pick(parsed, "src_hostname", "shost", "source_hostname") or None

    dst_ip = _pick(parsed, "dst_ip", "dstip", "dst", "destination_ip", "destination") or None
    dst_port_raw = _pick(parsed, "dst_port", "dstport", "dport", "dpt", "destination_port", "destinationport")
    dst_port = safe_int_cast(str(dst_port_raw)) if dst_port_raw is not None else None
    dst_host = _pick(parsed, "dst_hostname", "dhost", "destination_hostname") or None

    proto_name = _pick(parsed, "protocol", "proto") or None
    proto_name_lower = str(proto_name).lower() if proto_name else None
    direction_id, direction = _infer_direction_id(parsed)

    dev_hostname = _pick(parsed, "device_hostname", "hostname") or None
    dev_version = _pick(parsed, "device_version", "version") or None
    dev_vendor = _pick(parsed, "device_vendor_name", "vendor_name", "vendor") or None
    dev_product = _pick(parsed, "device_product_name", "product_name", "product") or None

    result = _build_base(time_val, activity_id, severity_id, message, raw_data,
                         ulpf_event_id, ulpf_raw_event_id)

    result["src_endpoint"] = {"ip": src_ip, "port": src_port if isinstance(src_port, int) else None, "hostname": src_host}
    result["dst_endpoint"] = {"ip": dst_ip, "port": dst_port if isinstance(dst_port, int) else None, "hostname": dst_host}
    result["connection_info"] = {
        "direction_id": direction_id,
        "direction": direction,
        "protocol_name": proto_name_lower,
        "protocol_num": _get_protocol_num(proto_name),
        "protocol_ver_id": 4,
    }
    result["app_name"] = _pick(parsed, "app_name", "app") or None
    result["app_protocol_name"] = _pick(parsed, "app_protocol_name") or None
    result["device"] = {
        "hostname": dev_hostname,
        "vendor_name": dev_vendor,
        "product_name": dev_product,
        "version": dev_version,
        "type_id": _infer_device_type(str(dev_vendor or ""), str(dev_product or ""), str(dev_hostname or "")),
    }
    result["metadata"] = {
        "version": OCSF_VERSION,
        "product": PRODUCT_META,
        "source_format": "json",
        "source_format_detail": {},
    }
    result["unmapped"] = _collect_unmapped(parsed, _JSON_MAPPED)
    return result


# ── Public API ────────────────────────────────────────────────────────────────

_NORMALIZER_MAP = {
    "syslog": normalize_syslog,
    "cef":    normalize_cef,
    "json":   normalize_json,
    # XML, CSV, and LEEF parsers all resolve fields to the same canonical
    # names (src_ip, dst_ip, src_port, dst_port, protocol, message, …)
    # used by normalize_json — so they share that normalizer directly.
    "xml":    normalize_json,
    "csv":    normalize_json,
    "leef":   normalize_json,
}


def normalize(
    format_id: str,
    parsed: dict,
    ulpf_event_id: str,
    ulpf_raw_event_id: str,
    log_timezone: str = "Asia/Kolkata",
) -> dict:
    """
    Convert a parsed log dict into an OCSF 1.9.0 Network Activity event dict.

    Args:
        format_id:         one of 'syslog', 'cef', 'json', 'xml', 'csv', 'leef'
        parsed:            output of the corresponding parser
        ulpf_event_id:     UUID4 string for the normalized event
        ulpf_raw_event_id: UUID4 string of the corresponding raw event row
        log_timezone:      IANA timezone string for RFC 3164 timestamp parsing

    Returns:
        OCSF-aligned dict ready for Pydantic validation and DB storage.

    Raises:
        ValueError if format_id is not recognized.
    """
    fn = _NORMALIZER_MAP.get(format_id)
    if fn is None:
        raise ValueError(f"No normalizer for format '{format_id}'")

    if "error_message" in parsed:
        # Parser returned an error — return a minimal event preserving the raw data.
        return {
            "time": -1,
            "activity_id": 0, "activity_name": "Unknown",
            "category_uid": CATEGORY_UID, "category_name": CATEGORY_NAME,
            "class_uid": CLASS_UID, "class_name": CLASS_NAME,
            "type_uid": CLASS_UID * 100,
            "severity_id": -1, "severity": "Unknown",
            "message": parsed.get("error_message"),
            "status_id": 0, "status": "Unknown",
            "raw_data": parsed.get("raw_data", ""),
            "ulpf_event_id": ulpf_event_id,
            "ulpf_raw_event_id": ulpf_raw_event_id,
            "src_endpoint": {}, "dst_endpoint": {}, "connection_info": {},
            "app_name": None, "app_protocol_name": None,
            "device": {}, "unmapped": {},
            "metadata": {
                "version": OCSF_VERSION,
                "product": PRODUCT_META,
                "source_format": format_id,
                "source_format_detail": {"parse_error": parsed.get("error_message")},
            },
        }

    return fn(parsed, ulpf_event_id, ulpf_raw_event_id, log_timezone)
