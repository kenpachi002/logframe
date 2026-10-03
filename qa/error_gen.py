from __future__ import annotations

from case import Case


def generate_error_cases() -> list[Case]:
    """Generate malformed and ambiguous inputs that should be refused."""
    cases: list[Case] = []

    for index in range(30):
        cases.append(Case(
            id=f"UNKNOWN-{index + 1:03}",
            line=f"unstructured payload with no known syntax {index}",
            expect="reject",
            note="No registered format marker or CSV delimiter.",
        ))

    for index in range(30):
        fields = ["CEF:0", "Acme", "Edge", "1.0", str(index), "Truncated", "5"]
        fields = fields[: 1 + index % 7]
        cases.append(Case(
            id=f"BAD-CEF-{index + 1:03}", line="|".join(fields), expect="reject",
            want_format="cef", note="Truncated CEF header.",
        ))

    for index in range(30):
        fields = ["LEEF:2.0", "Acme", "Gateway", "1.0"][: 1 + index % 4]
        cases.append(Case(
            id=f"BAD-LEEF-{index + 1:03}", line="|".join(fields), expect="reject",
            want_format="leef", note="Truncated LEEF header.",
        ))

    for index in range(30):
        cases.append(Case(
            id=f"BAD-JSON-{index + 1:03}",
            line=f'{{"sequence": {index}, "message": "unterminated", }}',
            expect="reject", want_format="json", note="Invalid JSON object syntax.",
        ))

    for index in range(30):
        cases.append(Case(
            id=f"BAD-XML-{index + 1:03}",
            line=f"<Event><Value>{index}</Event>",
            expect="reject", want_format="xml", note="Mismatched XML tags.",
        ))

    whitespace = ("", " ", "\t", "\r\n", " \t  ")
    for index in range(10):
        cases.append(Case(
            id=f"EMPTY-{index + 1:03}", line=whitespace[index % len(whitespace)],
            expect="reject", note="Empty or whitespace-only log.",
        ))

    for index in range(20):
        cases.append(Case(
            id=f"AMBIGUOUS-CSV-{index + 1:03}",
            line=f"arbitrary phrase {index},still not a structured log",
            expect="reject", want_format="csv", xfail="CSV_GREEDY",
            note="Comma catch-all may accept arbitrary prose as CSV.",
        ))

    for index in range(20):
        cases.append(Case(
            id=f"JSON-ARRAY-{index + 1:03}",
            line=f"[1, 2, {{\"sequence\": {index}}}]",
            expect="reject", want_format="json", xfail="JSON_ARRAY_AS_CSV",
            note="JSON arrays are not accepted log objects.",
        ))

    cases.extend([
        Case("BAD-PORT-RANGE", "CEF:0|Acme|Edge|1.0|1|Network event|5|spt=70000", "reject", "cef", xfail="PORT_RANGE"),
        Case("BAD-NESTED-ENDPOINT", '{"src":{"ip":"192.0.2.1"}}', "reject", "json"),
        Case("BAD-JSON-PORT-TYPE", '{"src_port":[],"message":"network event"}', "reject", "json", xfail="INVALID_PORT_TYPE"),
        Case("BAD-SYSLOG-PRI-SYNTAX", "<abc>1 invalid syslog", "reject"),
    ])
    return cases