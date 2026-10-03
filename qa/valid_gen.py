from __future__ import annotations

import json

from case import Case


def generate_valid_cases() -> list[Case]:
    """Generate a reproducible set of well-formed logs for all six parsers."""
    cases: list[Case] = []
    ports = (0, 1, 443, 65535)

    for index in range(36):
        src_ip = f"10.0.0.{index + 1}"
        dst_ip = f"198.51.100.{index + 1}"
        line = (
            f"CEF:0|Acme|Edge|1.0|{1000 + index}|Network connection|{index % 11}|"
            f"src={src_ip} dst={dst_ip} spt={ports[index % len(ports)]} "
            f"dpt={ports[(index + 1) % len(ports)]} proto=tcp"
        )
        cases.append(Case(
            id=f"CEF-{index + 1:03}", line=line, expect="accept", want_format="cef",
            want={"class_uid": 4001, "src_endpoint.ip": src_ip},
        ))

    for index in range(30):
        src_ip = f"10.1.0.{index + 1}"
        port = ports[index % len(ports)]
        if index % 2:
            delimiter = ("\t", ",", "~")[index % 3]
            extension = delimiter.join((f"src={src_ip}", f"srcPort={port}", "proto=tcp"))
            line = f"LEEF:2.0|Acme|Gateway|1.0|evt-{index}|{delimiter}|{extension}"
        else:
            line = f"LEEF:1.0|Acme|Gateway|1.0|evt-{index}\tsrc={src_ip}\tsrcPort={port}\tproto=tcp"
        cases.append(Case(
            id=f"LEEF-{index + 1:03}", line=line, expect="accept", want_format="leef",
            want={"src_endpoint.ip": src_ip},
            forbid=["unmapped._leef_version"],
            xfail="LEEF_UNMAPPED_LEAK",
        ))

    for index in range(36):
        src_ip = f"192.0.2.{index + 1}"
        dst_ip = f"198.51.100.{index + 1}"
        message = (
            f"SRC={src_ip} DST={dst_ip} SPT={ports[index % 4]} "
            f"DPT={ports[(index + 1) % 4]} PROTO=TCP connection established"
        )
        line = f"<{index % 192}>1 2025-01-02T03:04:05Z fw-{index} filter 123 ID47 - {message}"
        cases.append(Case(
            id=f"SYSLOG-{index + 1:03}", line=line, expect="accept", want_format="syslog",
            want={"src_endpoint.ip": src_ip, "class_uid": 4001},
        ))

    for index in range(36):
        src_ip = f"203.0.113.{index + 1}"
        line = json.dumps({
            "time": 1735787045,
            "src_ip": src_ip,
            "dst_ip": f"198.51.100.{index + 1}",
            "src_port": ports[index % 4],
            "dst_port": ports[(index + 1) % 4],
            "protocol": "tcp",
            "message": "connection permitted",
            "vendor": "Acme",
            "sequence": index,
        })
        cases.append(Case(
            id=f"JSON-{index + 1:03}", line=line, expect="accept", want_format="json",
            want={"src_endpoint.ip": src_ip, "class_uid": 4001},
        ))

    for index in range(30):
        src_ip = f"10.2.0.{index + 1}"
        line = (
            f"<Event><SrcIP>{src_ip}</SrcIP><DstIP>198.51.100.{index + 1}</DstIP>"
            f"<SrcPort>{ports[index % 4]}</SrcPort><DstPort>443</DstPort>"
            "<Protocol>tcp</Protocol><Message>connection established</Message></Event>"
        )
        cases.append(Case(
            id=f"XML-{index + 1:03}", line=line, expect="accept", want_format="xml",
            want={"src_endpoint.ip": src_ip, "class_uid": 4001},
        ))

    for index in range(30):
        src_ip = f"172.16.0.{index + 1}"
        line = (
            "srcip,dstip,srcport,dstport,proto,msg\n"
            f"{src_ip},198.51.100.{index + 1},{ports[index % 4]},443,tcp,connection permitted"
        )
        cases.append(Case(
            id=f"CSV-{index + 1:03}", line=line, expect="accept", want_format="csv",
            want={"src_endpoint.ip": src_ip, "class_uid": 4001},
        ))

    extras = [
        Case("EDGE-LEADING-SPACE", "  {\"message\":\"connection established\"}  ", "accept", "json"),
        Case("EDGE-UNICODE", json.dumps({"message": "connection permitted ☀", "src_ip": "192.0.2.1"}), "accept", "json"),
        Case("EDGE-EMPTY-OBJECT", "{}", "accept", "json", want={"class_uid": 4001}),
        Case("EDGE-NESTED-JSON", '{"src":{"ip":"192.0.2.10"},"message":"connection established"}', "accept", "json", want={"src_endpoint.ip": "192.0.2.10"}, xfail="NESTED_JSON"),
        Case("EDGE-CEF-NO-EXT", "CEF:0|Acme|Edge|1.0|7|Network event|5|", "accept", "cef"),
        Case("EDGE-CSV-QUOTED-COMMA", 'srcip,msg\n192.0.2.7,"connection, permitted"', "accept", "csv", want={"src_endpoint.ip": "192.0.2.7"}),
        Case("EDGE-CRLF", '{"message":"connection established","src_ip":"192.0.2.8"}\r\n', "accept", "json", want={"src_endpoint.ip": "192.0.2.8"}),
        Case("EDGE-LONG-MESSAGE", json.dumps({"message": "x" * 100_000}), "accept", "json", want={"class_uid": 4001}, note="100 KB parser throughput case"),
        Case("EDGE-ISO-OFFSET", '{"time":"2024-01-01T12:00:00+05:30","message":"network event"}', "accept", "json", want={"time": 1704090600}, xfail="ISO_OFFSET_TIME"),
        Case("EDGE-ACTIVITY-PRECEDENCE", '{"message":"timeout after deny"}', "accept", "json", want={"activity_id": 5}, xfail="ACTIVITY_PRECEDENCE"),
        Case("EDGE-ACTIVITY-SUBSTRING", '{"message":"login attempt"}', "accept", "json", want={"activity_id": 0}, xfail="ACTIVITY_SUBSTRING"),
        Case("EDGE-SYSLOG-IPV6", "<34>1 2025-01-02T03:04:05Z fw filter 123 ID47 - SRC=2001:db8::1 DST=2001:db8::2 connection established", "accept", "syslog", want={"src_endpoint.ip": "2001:db8::1"}, xfail="IPV6_SYSLOG"),
        Case("EDGE-JSON-IPV6-VERSION", '{"src_ip":"2001:db8::1","message":"network traffic"}', "accept", "json", want={"connection_info.protocol_ver_id": 6}, xfail="PROTOCOL_VER_HARDCODED"),
        Case("EDGE-XML-NAMESPACE", '<Event xmlns="urn:test"><SrcIP>192.0.2.9</SrcIP></Event>', "accept", "xml", want={"src_endpoint.ip": "192.0.2.9"}, xfail="XML_NAMESPACE"),
    ]
    cases.extend(extras)
    return cases