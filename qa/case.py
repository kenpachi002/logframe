from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Literal


Expectation = Literal["accept", "reject", "fuzz"]


class Verdict(StrEnum):
    PASS_YES = "PASS_YES"
    PASS_NO = "PASS_NO"
    WARN = "WARN"
    FAIL = "FAIL"
    CRASH = "CRASH"
    XFAIL = "XFAIL"
    XPASS = "XPASS"


@dataclass(slots=True)
class Case:
    id: str
    line: str
    expect: Expectation
    want_format: str | None = None
    want: dict[str, Any] = field(default_factory=dict)
    forbid: list[str] = field(default_factory=list)
    xfail: str | None = None
    note: str = ""


KNOWN_XFAILS: dict[str, str] = {
    "PORT_RANGE": "Normalized port values are not constrained to 0-65535.",
    "INVALID_PORT_TYPE": "A nonnumeric JSON port can be discarded while the event is accepted.",
    "NESTED_JSON": "Nested JSON endpoint objects are not flattened.",
    "JSON_ARRAY_AS_CSV": "JSON arrays can be misdetected as CSV.",
    "CSV_GREEDY": "CSV detection accepts arbitrary comma-containing text.",
    "ACTIVITY_PRECEDENCE": "Activity keyword precedence can select the wrong activity.",
    "ACTIVITY_SUBSTRING": "Activity inference currently matches substrings.",
    "ISO_OFFSET_TIME": "ISO timestamps with offsets are not normalized correctly.",
    "IPV6_SYSLOG": "Syslog network-field extraction currently handles IPv4 only.",
    "XML_NAMESPACE": "XML namespace-qualified tags are not mapped to network fields.",
    "LEEF_UNMAPPED_LEAK": "LEEF header fields can leak into the unmapped object.",
    "WARN_ONLY_VALIDATION": "The ingest pipeline records schema failures as warnings.",
    "PROTOCOL_VER_HARDCODED": "The normalized protocol version is hard-coded to IPv4.",
    "YEAR_BOUNDARY": "RFC3164 timestamps infer the year from the current date.",
}


def dotted_get(value: Any, path: str) -> tuple[bool, Any]:
    """Resolve a dotted dict/list path, distinguishing missing from null."""
    current = value
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        elif isinstance(current, list) and part.isdigit() and int(part) < len(current):
            current = current[int(part)]
        else:
            return False, None
    return True, current