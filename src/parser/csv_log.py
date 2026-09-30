"""
CSV log parser — handles comma-delimited log exports from firewalls, IDS/IPS,
and network devices (e.g. Fortinet traffic logs, Cisco Meraki, pfSense CSV).

Contract (same as cef.py / syslog.py):
  parse_csv_log(src: str) -> dict
  - Returns a flat dict with all source fields preserved.
  - Always includes raw_data = src.
  - On failure, returns {"error_message": ..., "raw_data": src}.

Handles two forms:
  1. Header row + data row (two-line input): header,row\n values,row
  2. Single data row — fields are named col_0, col_1, … automatically.

Network-field aliases are normalized to canonical names.
"""
import csv
import io

from parser.util import safe_int_cast


# Field alias → canonical name mapping
_NET_FIELD_ALIASES: dict[str, str] = {
    # src ip
    "srcip": "src_ip", "src": "src_ip", "source_ip": "src_ip",
    "sourceip": "src_ip", "SrcAddr": "src_ip", "srcaddr": "src_ip",
    "SourceAddress": "src_ip", "src_address": "src_ip",
    # dst ip
    "dstip": "dst_ip", "dst": "dst_ip", "destination_ip": "dst_ip",
    "destip": "dst_ip", "DstAddr": "dst_ip", "dstaddr": "dst_ip",
    "DestAddress": "dst_ip", "dst_address": "dst_ip",
    # ports
    "srcport": "src_port", "sport": "src_port", "spt": "src_port",
    "source_port": "src_port", "SourcePort": "src_port",
    "dstport": "dst_port", "dport": "dst_port", "dpt": "dst_port",
    "destination_port": "dst_port", "DestPort": "dst_port",
    # protocol
    "proto": "protocol", "Protocol": "protocol",
    # hostname / device
    "hostname": "device_hostname", "host": "device_hostname",
    "DeviceName": "device_hostname",
    # action / outcome
    "Action": "action", "outcome": "action", "disposition": "action",
    # message / description
    "msg": "message", "description": "message", "desc": "message",
    "event_description": "message",
}

_PORT_FIELDS = {"src_port", "dst_port"}


def _resolve_aliases(row: dict[str, str]) -> dict[str, str | int]:
    """Rename aliased keys to canonical names and cast port values."""
    result: dict[str, str | int] = {}
    for k, v in row.items():
        canonical = _NET_FIELD_ALIASES.get(k, k)
        val: str | int = v.strip() if isinstance(v, str) else v
        if canonical in _PORT_FIELDS and val != "":
            val = safe_int_cast(str(val))
        result[canonical] = val
    return result


def parse_csv_log(src: str) -> dict[str, str | int]:
    """
    Parse a CSV log line (or header+data pair) into a field dict.

    Supports:
      - Single line: auto-generated column names (col_0, col_1, …)
      - Two lines: first line = header, second = values
    """
    src_stripped = src.strip()

    if not src_stripped:
        return {"error_message": "Empty CSV input", "raw_data": src}

    lines = [ln for ln in src_stripped.splitlines() if ln.strip()]

    try:
        if len(lines) >= 2:
            # header + data
            reader = csv.DictReader(io.StringIO("\n".join(lines)))
            rows = list(reader)
            if not rows:
                return {"error_message": "CSV parsed to zero rows", "raw_data": src}
            row = dict(rows[0])
        else:
            # Single data row — auto-name columns
            reader_single = csv.reader(io.StringIO(lines[0]))
            values = next(reader_single)
            row = {f"col_{i}": v for i, v in enumerate(values)}
    except csv.Error as e:
        return {"error_message": f"CSV parse error: {e}", "raw_data": src}

    if not row:
        return {"error_message": "CSV row is empty", "raw_data": src}

    result = _resolve_aliases(row)
    result["raw_data"] = src
    return result
