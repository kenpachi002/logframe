"""
XML log parser — supports flat and one-level-nested XML event payloads.

Contract (same as cef.py / syslog.py):
  parse_xml(src: str) -> dict
  - Returns a flat dict with all source fields preserved.
  - Always includes raw_data = src.
  - On failure, returns {"error_message": ..., "raw_data": src}.

Handles common formats:
  - <Event>…</Event>   (Windows Event Log style)
  - <syslog>…</syslog> (vendor syslog-over-XML)
  - Any generic flat XML object
"""
import xml.etree.ElementTree as ET

from parser.util import safe_int_cast


# Network-field synonyms to flatten from XML attributes
_NET_FIELD_MAP = {
    "src_ip": ["src_ip", "srcip", "src", "SourceAddress", "src_addr", "SrcIP"],
    "dst_ip": ["dst_ip", "dstip", "dst", "DestAddress", "dst_addr", "DstIP"],
    "src_port": ["src_port", "srcport", "spt", "SourcePort", "SrcPort"],
    "dst_port": ["dst_port", "dstport", "dpt", "DestinationPort", "DstPort"],
    "protocol": ["protocol", "proto", "Protocol"],
}


def _flatten_element(element: ET.Element, prefix: str = "") -> dict[str, str]:
    """Recursively flatten an XML element into a dot-separated key dict."""
    result: dict[str, str] = {}

    # Own text
    if element.text and element.text.strip():
        key = prefix if prefix else element.tag
        result[key] = element.text.strip()

    # Own attributes
    for attr_key, attr_val in element.attrib.items():
        result_key = f"{prefix}.{attr_key}" if prefix else attr_key
        result[result_key] = attr_val

    # Child elements (one level deep flattened)
    for child in element:
        child_prefix = f"{prefix}.{child.tag}" if prefix else child.tag
        result.update(_flatten_element(child, child_prefix))

    return result


def parse_xml(log: str) -> dict[str, str | int]:
    """
    Parse an XML-formatted log/event string.

    Returns a flat dict with all attributes and text nodes extracted.
    Network fields (src_ip, dst_ip, ports, protocol) are normalised by alias.
    """
    result: dict[str, str | int] = {}

    try:
        root = ET.fromstring(log.strip())
    except ET.ParseError as e:
        return {
            "format": "xml",
            "error_message": str(e),
            "raw_data": log,
        }

    # Flatten root text + attributes + children
    result.update(_flatten_element(root))

    # Also do a simple flat top-level child extraction (friend's original logic)
    for child in root:
        if child.text and child.text.strip():
            result.setdefault(child.tag, child.text.strip())

    # Resolve network-field aliases → canonical names
    for canonical, aliases in _NET_FIELD_MAP.items():
        for alias in aliases:
            if alias in result and canonical not in result:
                val = result.pop(alias)
                if "port" in canonical:
                    result[canonical] = safe_int_cast(val)
                else:
                    result[canonical] = val
                break

    # Tag the format
    result.setdefault("_xml_root_tag", root.tag)

    # Preserve complete original event (ULPF requirement)
    result["raw_data"] = log

    return result
