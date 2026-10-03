"""
LEEF (Log Event Extended Format) parser — IBM QRadar's structured log format.

LEEF 1.0 syntax:
  LEEF:1.0|<Vendor>|<Product>|<Version>|<EventID>|<Extension key=value pairs>

LEEF 2.0 syntax:
  LEEF:2.0|<Vendor>|<Product>|<Version>|<EventID>|<Delimiter>|<Extension>

Contract (same as cef.py / syslog.py):
  parse_leef(src: str) -> dict
  - Returns a flat dict with all source fields preserved.
  - Always includes raw_data = src.
  - On failure, returns {"error_message": ..., "raw_data": src}.

Reference: IBM QRadar LEEF Format Guide.
"""
import re

from parser.util import safe_int_cast


# Port-valued extension keys (cast to int)
# NOTE: "src" and "dst" are IP address fields — do NOT include them here.
_PORT_KEYS = {"srcPort", "dstPort", "spt", "dpt"}

# Canonical field aliases (LEEF extension keys → ULPF canonical)
_LEEF_ALIASES: dict[str, str] = {
    "src": "src_ip",
    "dst": "dst_ip",
    "srcPort": "src_port",
    "dstPort": "dst_port",
    "spt": "src_port",
    "dpt": "dst_port",
    "proto": "protocol",
    "devTime": "time",
    "usrName": "username",
    "identSrc": "src_ip",
    "identDst": "dst_ip",
    "srcPreNAT": "src_nat_ip",
    "dstPreNAT": "dst_nat_ip",
    "vSrc": "virtual_src",
}


def _parse_extension(extension_str: str, delimiter: str = "\t") -> dict[str, str | int]:
    """
    Parse the LEEF extension section into a key→value dict.

    LEEF 1.0 uses TAB as delimiter; LEEF 2.0 can specify a custom delimiter.
    Falls back to space-delimited key=value parsing if TAB split fails.
    """
    fields: dict[str, str | int] = {}

    # Try delimiter-based split first
    pairs = re.split(re.escape(delimiter), extension_str)
    if len(pairs) == 1 and delimiter != "\t":
        # Try TAB as fallback
        pairs = extension_str.split("\t")
    if len(pairs) == 1:
        # Fall back to regex-based key=value matching (space-separated)
        pairs_matched = re.findall(r"(\w+)=(.*?)(?=\s+\w+=|$)", extension_str.strip())
        for key, val in pairs_matched:
            val = val.strip()
            canonical = _LEEF_ALIASES.get(key, key)
            if key in _PORT_KEYS:
                fields[canonical] = safe_int_cast(val)
            else:
                fields[canonical] = val
        return fields

    for pair in pairs:
        pair = pair.strip()
        if "=" not in pair:
            continue
        key, _, val = pair.partition("=")
        key = key.strip()
        val = val.strip()
        canonical = _LEEF_ALIASES.get(key, key)
        if key in _PORT_KEYS:
            fields[canonical] = safe_int_cast(val)
        else:
            fields[canonical] = val

    return fields


def parse_leef(log: str) -> dict[str, str | int]:
    """
    Parse a LEEF 1.0 or 2.0 log line.

    Returns a dict with header fields prefixed by _leef_ and
    all extension fields at the top level.
    """
    log = log.strip()

    if not log.upper().startswith("LEEF:"):
        return {
            "error_message": "Not a LEEF line: must begin with 'LEEF:'",
            "raw_data": log,
        }

    # Split on pipe — respecting escaped pipes (\|)
    parts = re.split(r"(?<!\\)\|", log)

    # Minimum: LEEF:version | Vendor | Product | Version | EventID
    if len(parts) < 5:
        return {
            "error_message": f"Invalid LEEF format: expected ≥5 pipe-delimited fields, got {len(parts)}",
            "raw_data": log,
        }

    version_field = parts[0]          # e.g. "LEEF:2.0"
    leef_version = version_field[5:]  # strip "LEEF:"

    vendor = parts[1].replace("\\|", "|")
    product = parts[2].replace("\\|", "|")
    product_version = parts[3].replace("\\|", "|")
    raw_event_field = parts[4].replace("\\|", "|")

    # LEEF 1.0 most commonly embeds the extension in the EventID field,
    # TAB-separated: "EventID\tkey=val\tkey=val..."
    # LEEF 2.0 uses an explicit 6th pipe-field for the delimiter.
    delimiter = "\t"
    extension_str = ""

    if leef_version.startswith("2") and len(parts) >= 7:
        # LEEF 2.0: delimiter is parts[5], extension starts at parts[6]
        delimiter = parts[5] or "\t"
        event_id = raw_event_field
        extension_str = "|".join(parts[6:])
    elif "\t" in raw_event_field:
        # LEEF 1.0 TAB form: EventID and extension are both in parts[4]
        event_id, _, extension_str = raw_event_field.partition("\t")
    elif len(parts) >= 6:
        # LEEF 1.0 pipe form: extension in parts[5+]
        event_id = raw_event_field
        extension_str = "|".join(parts[5:])
    else:
        event_id = raw_event_field

    result: dict[str, str | int] = {
        "_leef_version": leef_version,
        "_leef_vendor": vendor,
        "_leef_product": product,
        "_leef_product_version": product_version,
        "_leef_event_id": event_id,
    }

    if extension_str.strip():
        result.update(_parse_extension(extension_str, delimiter))

    result["raw_data"] = log
    return result

