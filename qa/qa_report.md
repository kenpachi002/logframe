# ULPF QA Report

Cases: **716**

| Verdict | Count |
|---|---:|
| PASS_YES | 383 |
| PASS_NO | 254 |
| WARN | 0 |
| FAIL | 0 |
| CRASH | 0 |
| XFAIL | 27 |
| XPASS | 52 |

## By Format

| Format | PASS_YES | PASS_NO | WARN | FAIL | CRASH | XFAIL | XPASS |
|---|---:|---:|---:|---:|---:|---:|---:|
| cef | 90 | 46 | 0 | 0 | 0 | 1 | 0 |
| csv | 59 | 5 | 0 | 0 | 0 | 20 | 0 |
| json | 50 | 64 | 0 | 0 | 0 | 5 | 21 |
| leef | 54 | 31 | 0 | 0 | 0 | 0 | 30 |
| syslog | 94 | 0 | 0 | 0 | 0 | 1 | 0 |
| unknown | 0 | 52 | 0 | 0 | 0 | 0 | 0 |
| xml | 36 | 56 | 0 | 0 | 0 | 0 | 1 |

## Cases

| ID | Format | Expected | Verdict | Time (ms) | Reason |
|---|---|---|---|---:|---|
| CEF-001 | cef | accept | PASS_YES | 0.368 | Parsed, normalized, and strictly validated. |
| CEF-002 | cef | accept | PASS_YES | 0.104 | Parsed, normalized, and strictly validated. |
| CEF-003 | cef | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| CEF-004 | cef | accept | PASS_YES | 0.123 | Parsed, normalized, and strictly validated. |
| CEF-005 | cef | accept | PASS_YES | 0.080 | Parsed, normalized, and strictly validated. |
| CEF-006 | cef | accept | PASS_YES | 0.051 | Parsed, normalized, and strictly validated. |
| CEF-007 | cef | accept | PASS_YES | 0.047 | Parsed, normalized, and strictly validated. |
| CEF-008 | cef | accept | PASS_YES | 0.044 | Parsed, normalized, and strictly validated. |
| CEF-009 | cef | accept | PASS_YES | 0.115 | Parsed, normalized, and strictly validated. |
| CEF-010 | cef | accept | PASS_YES | 0.050 | Parsed, normalized, and strictly validated. |
| CEF-011 | cef | accept | PASS_YES | 0.069 | Parsed, normalized, and strictly validated. |
| CEF-012 | cef | accept | PASS_YES | 0.045 | Parsed, normalized, and strictly validated. |
| CEF-013 | cef | accept | PASS_YES | 0.143 | Parsed, normalized, and strictly validated. |
| CEF-014 | cef | accept | PASS_YES | 0.100 | Parsed, normalized, and strictly validated. |
| CEF-015 | cef | accept | PASS_YES | 0.084 | Parsed, normalized, and strictly validated. |
| CEF-016 | cef | accept | PASS_YES | 0.065 | Parsed, normalized, and strictly validated. |
| CEF-017 | cef | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| CEF-018 | cef | accept | PASS_YES | 0.205 | Parsed, normalized, and strictly validated. |
| CEF-019 | cef | accept | PASS_YES | 0.090 | Parsed, normalized, and strictly validated. |
| CEF-020 | cef | accept | PASS_YES | 0.066 | Parsed, normalized, and strictly validated. |
| CEF-021 | cef | accept | PASS_YES | 0.067 | Parsed, normalized, and strictly validated. |
| CEF-022 | cef | accept | PASS_YES | 0.062 | Parsed, normalized, and strictly validated. |
| CEF-023 | cef | accept | PASS_YES | 0.058 | Parsed, normalized, and strictly validated. |
| CEF-024 | cef | accept | PASS_YES | 0.058 | Parsed, normalized, and strictly validated. |
| CEF-025 | cef | accept | PASS_YES | 0.056 | Parsed, normalized, and strictly validated. |
| CEF-026 | cef | accept | PASS_YES | 0.057 | Parsed, normalized, and strictly validated. |
| CEF-027 | cef | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| CEF-028 | cef | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| CEF-029 | cef | accept | PASS_YES | 0.048 | Parsed, normalized, and strictly validated. |
| CEF-030 | cef | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CEF-031 | cef | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CEF-032 | cef | accept | PASS_YES | 0.038 | Parsed, normalized, and strictly validated. |
| CEF-033 | cef | accept | PASS_YES | 0.041 | Parsed, normalized, and strictly validated. |
| CEF-034 | cef | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CEF-035 | cef | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CEF-036 | cef | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| LEEF-001 | leef | accept | XPASS | 0.117 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-002 | leef | accept | XPASS | 0.081 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-003 | leef | accept | XPASS | 0.048 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-004 | leef | accept | XPASS | 0.043 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-005 | leef | accept | XPASS | 0.040 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-006 | leef | accept | XPASS | 0.063 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-007 | leef | accept | XPASS | 0.040 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-008 | leef | accept | XPASS | 0.040 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-009 | leef | accept | XPASS | 0.039 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-010 | leef | accept | XPASS | 0.099 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-011 | leef | accept | XPASS | 0.087 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-012 | leef | accept | XPASS | 0.056 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-013 | leef | accept | XPASS | 0.042 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-014 | leef | accept | XPASS | 0.038 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-015 | leef | accept | XPASS | 0.038 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-016 | leef | accept | XPASS | 0.038 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-017 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-018 | leef | accept | XPASS | 0.036 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-019 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-020 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-021 | leef | accept | XPASS | 0.036 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-022 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-023 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-024 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-025 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-026 | leef | accept | XPASS | 0.036 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-027 | leef | accept | XPASS | 0.035 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-028 | leef | accept | XPASS | 0.037 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-029 | leef | accept | XPASS | 0.036 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| LEEF-030 | leef | accept | XPASS | 0.038 | Known defect not reproduced (LEEF_UNMAPPED_LEAK). Parsed, normalized, and strictly validated. |
| SYSLOG-001 | syslog | accept | PASS_YES | 1.563 | Parsed, normalized, and strictly validated. |
| SYSLOG-002 | syslog | accept | PASS_YES | 0.102 | Parsed, normalized, and strictly validated. |
| SYSLOG-003 | syslog | accept | PASS_YES | 0.071 | Parsed, normalized, and strictly validated. |
| SYSLOG-004 | syslog | accept | PASS_YES | 0.062 | Parsed, normalized, and strictly validated. |
| SYSLOG-005 | syslog | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| SYSLOG-006 | syslog | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| SYSLOG-007 | syslog | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| SYSLOG-008 | syslog | accept | PASS_YES | 0.057 | Parsed, normalized, and strictly validated. |
| SYSLOG-009 | syslog | accept | PASS_YES | 0.056 | Parsed, normalized, and strictly validated. |
| SYSLOG-010 | syslog | accept | PASS_YES | 0.057 | Parsed, normalized, and strictly validated. |
| SYSLOG-011 | syslog | accept | PASS_YES | 0.060 | Parsed, normalized, and strictly validated. |
| SYSLOG-012 | syslog | accept | PASS_YES | 0.058 | Parsed, normalized, and strictly validated. |
| SYSLOG-013 | syslog | accept | PASS_YES | 0.056 | Parsed, normalized, and strictly validated. |
| SYSLOG-014 | syslog | accept | PASS_YES | 0.057 | Parsed, normalized, and strictly validated. |
| SYSLOG-015 | syslog | accept | PASS_YES | 0.056 | Parsed, normalized, and strictly validated. |
| SYSLOG-016 | syslog | accept | PASS_YES | 0.055 | Parsed, normalized, and strictly validated. |
| SYSLOG-017 | syslog | accept | PASS_YES | 0.053 | Parsed, normalized, and strictly validated. |
| SYSLOG-018 | syslog | accept | PASS_YES | 0.054 | Parsed, normalized, and strictly validated. |
| SYSLOG-019 | syslog | accept | PASS_YES | 0.057 | Parsed, normalized, and strictly validated. |
| SYSLOG-020 | syslog | accept | PASS_YES | 0.056 | Parsed, normalized, and strictly validated. |
| SYSLOG-021 | syslog | accept | PASS_YES | 0.054 | Parsed, normalized, and strictly validated. |
| SYSLOG-022 | syslog | accept | PASS_YES | 0.055 | Parsed, normalized, and strictly validated. |
| SYSLOG-023 | syslog | accept | PASS_YES | 0.056 | Parsed, normalized, and strictly validated. |
| SYSLOG-024 | syslog | accept | PASS_YES | 0.056 | Parsed, normalized, and strictly validated. |
| SYSLOG-025 | syslog | accept | PASS_YES | 0.055 | Parsed, normalized, and strictly validated. |
| SYSLOG-026 | syslog | accept | PASS_YES | 0.087 | Parsed, normalized, and strictly validated. |
| SYSLOG-027 | syslog | accept | PASS_YES | 0.124 | Parsed, normalized, and strictly validated. |
| SYSLOG-028 | syslog | accept | PASS_YES | 0.081 | Parsed, normalized, and strictly validated. |
| SYSLOG-029 | syslog | accept | PASS_YES | 0.071 | Parsed, normalized, and strictly validated. |
| SYSLOG-030 | syslog | accept | PASS_YES | 0.063 | Parsed, normalized, and strictly validated. |
| SYSLOG-031 | syslog | accept | PASS_YES | 0.219 | Parsed, normalized, and strictly validated. |
| SYSLOG-032 | syslog | accept | PASS_YES | 0.114 | Parsed, normalized, and strictly validated. |
| SYSLOG-033 | syslog | accept | PASS_YES | 0.147 | Parsed, normalized, and strictly validated. |
| SYSLOG-034 | syslog | accept | PASS_YES | 0.099 | Parsed, normalized, and strictly validated. |
| SYSLOG-035 | syslog | accept | PASS_YES | 0.080 | Parsed, normalized, and strictly validated. |
| SYSLOG-036 | syslog | accept | PASS_YES | 0.085 | Parsed, normalized, and strictly validated. |
| JSON-001 | json | accept | PASS_YES | 0.085 | Parsed, normalized, and strictly validated. |
| JSON-002 | json | accept | PASS_YES | 0.064 | Parsed, normalized, and strictly validated. |
| JSON-003 | json | accept | PASS_YES | 0.051 | Parsed, normalized, and strictly validated. |
| JSON-004 | json | accept | PASS_YES | 0.047 | Parsed, normalized, and strictly validated. |
| JSON-005 | json | accept | PASS_YES | 0.046 | Parsed, normalized, and strictly validated. |
| JSON-006 | json | accept | PASS_YES | 0.044 | Parsed, normalized, and strictly validated. |
| JSON-007 | json | accept | PASS_YES | 0.042 | Parsed, normalized, and strictly validated. |
| JSON-008 | json | accept | PASS_YES | 0.045 | Parsed, normalized, and strictly validated. |
| JSON-009 | json | accept | PASS_YES | 0.044 | Parsed, normalized, and strictly validated. |
| JSON-010 | json | accept | PASS_YES | 0.044 | Parsed, normalized, and strictly validated. |
| JSON-011 | json | accept | PASS_YES | 0.060 | Parsed, normalized, and strictly validated. |
| JSON-012 | json | accept | PASS_YES | 0.049 | Parsed, normalized, and strictly validated. |
| JSON-013 | json | accept | PASS_YES | 0.073 | Parsed, normalized, and strictly validated. |
| JSON-014 | json | accept | PASS_YES | 0.046 | Parsed, normalized, and strictly validated. |
| JSON-015 | json | accept | PASS_YES | 0.036 | Parsed, normalized, and strictly validated. |
| JSON-016 | json | accept | PASS_YES | 0.035 | Parsed, normalized, and strictly validated. |
| JSON-017 | json | accept | PASS_YES | 0.036 | Parsed, normalized, and strictly validated. |
| JSON-018 | json | accept | PASS_YES | 0.034 | Parsed, normalized, and strictly validated. |
| JSON-019 | json | accept | PASS_YES | 0.034 | Parsed, normalized, and strictly validated. |
| JSON-020 | json | accept | PASS_YES | 0.034 | Parsed, normalized, and strictly validated. |
| JSON-021 | json | accept | PASS_YES | 0.035 | Parsed, normalized, and strictly validated. |
| JSON-022 | json | accept | PASS_YES | 0.037 | Parsed, normalized, and strictly validated. |
| JSON-023 | json | accept | PASS_YES | 0.034 | Parsed, normalized, and strictly validated. |
| JSON-024 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-025 | json | accept | PASS_YES | 0.034 | Parsed, normalized, and strictly validated. |
| JSON-026 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-027 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-028 | json | accept | PASS_YES | 0.034 | Parsed, normalized, and strictly validated. |
| JSON-029 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-030 | json | accept | PASS_YES | 0.032 | Parsed, normalized, and strictly validated. |
| JSON-031 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-032 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-033 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-034 | json | accept | PASS_YES | 0.032 | Parsed, normalized, and strictly validated. |
| JSON-035 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| JSON-036 | json | accept | PASS_YES | 0.033 | Parsed, normalized, and strictly validated. |
| XML-001 | xml | accept | PASS_YES | 0.447 | Parsed, normalized, and strictly validated. |
| XML-002 | xml | accept | PASS_YES | 0.095 | Parsed, normalized, and strictly validated. |
| XML-003 | xml | accept | PASS_YES | 0.073 | Parsed, normalized, and strictly validated. |
| XML-004 | xml | accept | PASS_YES | 0.064 | Parsed, normalized, and strictly validated. |
| XML-005 | xml | accept | PASS_YES | 0.066 | Parsed, normalized, and strictly validated. |
| XML-006 | xml | accept | PASS_YES | 0.062 | Parsed, normalized, and strictly validated. |
| XML-007 | xml | accept | PASS_YES | 0.062 | Parsed, normalized, and strictly validated. |
| XML-008 | xml | accept | PASS_YES | 0.060 | Parsed, normalized, and strictly validated. |
| XML-009 | xml | accept | PASS_YES | 0.061 | Parsed, normalized, and strictly validated. |
| XML-010 | xml | accept | PASS_YES | 0.062 | Parsed, normalized, and strictly validated. |
| XML-011 | xml | accept | PASS_YES | 0.061 | Parsed, normalized, and strictly validated. |
| XML-012 | xml | accept | PASS_YES | 0.064 | Parsed, normalized, and strictly validated. |
| XML-013 | xml | accept | PASS_YES | 0.062 | Parsed, normalized, and strictly validated. |
| XML-014 | xml | accept | PASS_YES | 0.063 | Parsed, normalized, and strictly validated. |
| XML-015 | xml | accept | PASS_YES | 0.060 | Parsed, normalized, and strictly validated. |
| XML-016 | xml | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| XML-017 | xml | accept | PASS_YES | 0.061 | Parsed, normalized, and strictly validated. |
| XML-018 | xml | accept | PASS_YES | 0.062 | Parsed, normalized, and strictly validated. |
| XML-019 | xml | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| XML-020 | xml | accept | PASS_YES | 0.060 | Parsed, normalized, and strictly validated. |
| XML-021 | xml | accept | PASS_YES | 0.058 | Parsed, normalized, and strictly validated. |
| XML-022 | xml | accept | PASS_YES | 0.058 | Parsed, normalized, and strictly validated. |
| XML-023 | xml | accept | PASS_YES | 0.057 | Parsed, normalized, and strictly validated. |
| XML-024 | xml | accept | PASS_YES | 0.057 | Parsed, normalized, and strictly validated. |
| XML-025 | xml | accept | PASS_YES | 0.076 | Parsed, normalized, and strictly validated. |
| XML-026 | xml | accept | PASS_YES | 0.063 | Parsed, normalized, and strictly validated. |
| XML-027 | xml | accept | PASS_YES | 0.061 | Parsed, normalized, and strictly validated. |
| XML-028 | xml | accept | PASS_YES | 0.058 | Parsed, normalized, and strictly validated. |
| XML-029 | xml | accept | PASS_YES | 0.058 | Parsed, normalized, and strictly validated. |
| XML-030 | xml | accept | PASS_YES | 0.059 | Parsed, normalized, and strictly validated. |
| CSV-001 | csv | accept | PASS_YES | 0.097 | Parsed, normalized, and strictly validated. |
| CSV-002 | csv | accept | PASS_YES | 0.071 | Parsed, normalized, and strictly validated. |
| CSV-003 | csv | accept | PASS_YES | 0.047 | Parsed, normalized, and strictly validated. |
| CSV-004 | csv | accept | PASS_YES | 0.043 | Parsed, normalized, and strictly validated. |
| CSV-005 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-006 | csv | accept | PASS_YES | 0.041 | Parsed, normalized, and strictly validated. |
| CSV-007 | csv | accept | PASS_YES | 0.042 | Parsed, normalized, and strictly validated. |
| CSV-008 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-009 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-010 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-011 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-012 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-013 | csv | accept | PASS_YES | 0.041 | Parsed, normalized, and strictly validated. |
| CSV-014 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-015 | csv | accept | PASS_YES | 0.044 | Parsed, normalized, and strictly validated. |
| CSV-016 | csv | accept | PASS_YES | 0.038 | Parsed, normalized, and strictly validated. |
| CSV-017 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-018 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-019 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-020 | csv | accept | PASS_YES | 0.041 | Parsed, normalized, and strictly validated. |
| CSV-021 | csv | accept | PASS_YES | 0.041 | Parsed, normalized, and strictly validated. |
| CSV-022 | csv | accept | PASS_YES | 0.041 | Parsed, normalized, and strictly validated. |
| CSV-023 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-024 | csv | accept | PASS_YES | 0.041 | Parsed, normalized, and strictly validated. |
| CSV-025 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-026 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-027 | csv | accept | PASS_YES | 0.040 | Parsed, normalized, and strictly validated. |
| CSV-028 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-029 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| CSV-030 | csv | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| EDGE-LEADING-SPACE | json | accept | PASS_YES | 0.039 | Parsed, normalized, and strictly validated. |
| EDGE-UNICODE | json | accept | PASS_YES | 0.322 | Parsed, normalized, and strictly validated. |
| EDGE-EMPTY-OBJECT | json | accept | PASS_YES | 0.042 | Parsed, normalized, and strictly validated. |
| EDGE-NESTED-JSON | json | accept | XFAIL | 0.432 | NESTED_JSON: Strict event validation failed: 1 validation error for UniversalEvent src_endpoint.ip   Input should be a valid string [type=string_type, input_value={'ip': '192.0.2.10'}, input_type=dict]     For further information visit https://errors.pydantic.dev/2.13/v/string_type |
| EDGE-CEF-NO-EXT | cef | accept | PASS_YES | 0.083 | Parsed, normalized, and strictly validated. |
| EDGE-CSV-QUOTED-COMMA | csv | accept | PASS_YES | 0.156 | Parsed, normalized, and strictly validated. |
| EDGE-CRLF | json | accept | PASS_YES | 0.076 | Parsed, normalized, and strictly validated. |
| EDGE-LONG-MESSAGE | json | accept | PASS_YES | 2.102 | Parsed, normalized, and strictly validated. |
| EDGE-ISO-OFFSET | json | accept | XPASS | 0.078 | Known defect not reproduced (ISO_OFFSET_TIME). Parsed, normalized, and strictly validated. |
| EDGE-ACTIVITY-PRECEDENCE | json | accept | XFAIL | 0.042 | ACTIVITY_PRECEDENCE: Field 'activity_id': expected 5, got 4. |
| EDGE-ACTIVITY-SUBSTRING | json | accept | XFAIL | 0.036 | ACTIVITY_SUBSTRING: Field 'activity_id': expected 0, got 6. |
| EDGE-SYSLOG-IPV6 | syslog | accept | XFAIL | 0.461 | IPV6_SYSLOG: Field 'src_endpoint.ip': expected '2001:db8::1', got None. |
| EDGE-JSON-IPV6-VERSION | json | accept | XFAIL | 0.051 | PROTOCOL_VER_HARDCODED: Field 'connection_info.protocol_ver_id': expected 6, got 4. |
| EDGE-XML-NAMESPACE | xml | accept | XPASS | 0.090 | Known defect not reproduced (XML_NAMESPACE). Parsed, normalized, and strictly validated. |
| UNKNOWN-001 | - | reject | PASS_NO | 0.008 | No parser matched log: 'unstructured payload with no known syntax 0' |
| UNKNOWN-002 | - | reject | PASS_NO | 0.005 | No parser matched log: 'unstructured payload with no known syntax 1' |
| UNKNOWN-003 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 2' |
| UNKNOWN-004 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 3' |
| UNKNOWN-005 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 4' |
| UNKNOWN-006 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 5' |
| UNKNOWN-007 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 6' |
| UNKNOWN-008 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 7' |
| UNKNOWN-009 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 8' |
| UNKNOWN-010 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 9' |
| UNKNOWN-011 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 10' |
| UNKNOWN-012 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 11' |
| UNKNOWN-013 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 12' |
| UNKNOWN-014 | - | reject | PASS_NO | 0.004 | No parser matched log: 'unstructured payload with no known syntax 13' |
| UNKNOWN-015 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 14' |
| UNKNOWN-016 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 15' |
| UNKNOWN-017 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 16' |
| UNKNOWN-018 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 17' |
| UNKNOWN-019 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 18' |
| UNKNOWN-020 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 19' |
| UNKNOWN-021 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 20' |
| UNKNOWN-022 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 21' |
| UNKNOWN-023 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 22' |
| UNKNOWN-024 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 23' |
| UNKNOWN-025 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 24' |
| UNKNOWN-026 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 25' |
| UNKNOWN-027 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 26' |
| UNKNOWN-028 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 27' |
| UNKNOWN-029 | - | reject | PASS_NO | 0.002 | No parser matched log: 'unstructured payload with no known syntax 28' |
| UNKNOWN-030 | - | reject | PASS_NO | 0.003 | No parser matched log: 'unstructured payload with no known syntax 29' |
| BAD-CEF-001 | cef | reject | PASS_NO | 0.006 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 1 |
| BAD-CEF-002 | cef | reject | PASS_NO | 0.004 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 2 |
| BAD-CEF-003 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 3 |
| BAD-CEF-004 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 4 |
| BAD-CEF-005 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 5 |
| BAD-CEF-006 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 6 |
| BAD-CEF-007 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 7 |
| BAD-CEF-008 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 1 |
| BAD-CEF-009 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 2 |
| BAD-CEF-010 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 3 |
| BAD-CEF-011 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 4 |
| BAD-CEF-012 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 5 |
| BAD-CEF-013 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 6 |
| BAD-CEF-014 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 7 |
| BAD-CEF-015 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 1 |
| BAD-CEF-016 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 2 |
| BAD-CEF-017 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 3 |
| BAD-CEF-018 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 4 |
| BAD-CEF-019 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 5 |
| BAD-CEF-020 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 6 |
| BAD-CEF-021 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 7 |
| BAD-CEF-022 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 1 |
| BAD-CEF-023 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 2 |
| BAD-CEF-024 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 3 |
| BAD-CEF-025 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 4 |
| BAD-CEF-026 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 5 |
| BAD-CEF-027 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 6 |
| BAD-CEF-028 | cef | reject | PASS_NO | 0.003 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 7 |
| BAD-CEF-029 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 1 |
| BAD-CEF-030 | cef | reject | PASS_NO | 0.002 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 2 |
| BAD-LEEF-001 | leef | reject | PASS_NO | 0.004 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-002 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-LEEF-003 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 3 |
| BAD-LEEF-004 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| BAD-LEEF-005 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-006 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-LEEF-007 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 3 |
| BAD-LEEF-008 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| BAD-LEEF-009 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-010 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-LEEF-011 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 3 |
| BAD-LEEF-012 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| BAD-LEEF-013 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-014 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-LEEF-015 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 3 |
| BAD-LEEF-016 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| BAD-LEEF-017 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-018 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-LEEF-019 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 3 |
| BAD-LEEF-020 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| BAD-LEEF-021 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-022 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-LEEF-023 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 3 |
| BAD-LEEF-024 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| BAD-LEEF-025 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-026 | leef | reject | PASS_NO | 0.004 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-LEEF-027 | leef | reject | PASS_NO | 0.004 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 3 |
| BAD-LEEF-028 | leef | reject | PASS_NO | 0.003 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| BAD-LEEF-029 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 1 |
| BAD-LEEF-030 | leef | reject | PASS_NO | 0.002 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 2 |
| BAD-JSON-001 | json | reject | PASS_NO | 0.024 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-002 | json | reject | PASS_NO | 0.012 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-003 | json | reject | PASS_NO | 0.007 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-004 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-005 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-006 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-007 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-008 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-009 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-010 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 41 |
| BAD-JSON-011 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-012 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-013 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-014 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-015 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-016 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-017 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-018 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-019 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-020 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-021 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-022 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-023 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-024 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-025 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-026 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-027 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-028 | json | reject | PASS_NO | 0.006 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-029 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-JSON-030 | json | reject | PASS_NO | 0.005 | JSON decode error: Illegal trailing comma before end of object at position 42 |
| BAD-XML-001 | xml | reject | PASS_NO | 0.040 | mismatched tag: line 1, column 17 |
| BAD-XML-002 | xml | reject | PASS_NO | 0.019 | mismatched tag: line 1, column 17 |
| BAD-XML-003 | xml | reject | PASS_NO | 0.017 | mismatched tag: line 1, column 17 |
| BAD-XML-004 | xml | reject | PASS_NO | 0.016 | mismatched tag: line 1, column 17 |
| BAD-XML-005 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 17 |
| BAD-XML-006 | xml | reject | PASS_NO | 0.016 | mismatched tag: line 1, column 17 |
| BAD-XML-007 | xml | reject | PASS_NO | 0.016 | mismatched tag: line 1, column 17 |
| BAD-XML-008 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 17 |
| BAD-XML-009 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 17 |
| BAD-XML-010 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 17 |
| BAD-XML-011 | xml | reject | PASS_NO | 0.018 | mismatched tag: line 1, column 18 |
| BAD-XML-012 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-013 | xml | reject | PASS_NO | 0.017 | mismatched tag: line 1, column 18 |
| BAD-XML-014 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-015 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-016 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-017 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-018 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-019 | xml | reject | PASS_NO | 0.014 | mismatched tag: line 1, column 18 |
| BAD-XML-020 | xml | reject | PASS_NO | 0.014 | mismatched tag: line 1, column 18 |
| BAD-XML-021 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-022 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-023 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-024 | xml | reject | PASS_NO | 0.014 | mismatched tag: line 1, column 18 |
| BAD-XML-025 | xml | reject | PASS_NO | 0.014 | mismatched tag: line 1, column 18 |
| BAD-XML-026 | xml | reject | PASS_NO | 0.014 | mismatched tag: line 1, column 18 |
| BAD-XML-027 | xml | reject | PASS_NO | 0.014 | mismatched tag: line 1, column 18 |
| BAD-XML-028 | xml | reject | PASS_NO | 0.016 | mismatched tag: line 1, column 18 |
| BAD-XML-029 | xml | reject | PASS_NO | 0.015 | mismatched tag: line 1, column 18 |
| BAD-XML-030 | xml | reject | PASS_NO | 0.014 | mismatched tag: line 1, column 18 |
| EMPTY-001 | - | reject | PASS_NO | 0.002 | Empty log line |
| EMPTY-002 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-003 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-004 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-005 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-006 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-007 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-008 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-009 | - | reject | PASS_NO | 0.001 | Empty log line |
| EMPTY-010 | - | reject | PASS_NO | 0.001 | Empty log line |
| AMBIGUOUS-CSV-001 | csv | reject | XFAIL | 0.060 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-002 | csv | reject | XFAIL | 0.041 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-003 | csv | reject | XFAIL | 0.033 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-004 | csv | reject | XFAIL | 0.031 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-005 | csv | reject | XFAIL | 0.031 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-006 | csv | reject | XFAIL | 0.032 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-007 | csv | reject | XFAIL | 0.031 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-008 | csv | reject | XFAIL | 0.030 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-009 | csv | reject | XFAIL | 0.029 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-010 | csv | reject | XFAIL | 0.030 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-011 | csv | reject | XFAIL | 0.045 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-012 | csv | reject | XFAIL | 0.032 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-013 | csv | reject | XFAIL | 0.030 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-014 | csv | reject | XFAIL | 0.030 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-015 | csv | reject | XFAIL | 0.030 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-016 | csv | reject | XFAIL | 0.029 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-017 | csv | reject | XFAIL | 0.029 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-018 | csv | reject | XFAIL | 0.029 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-019 | csv | reject | XFAIL | 0.029 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| AMBIGUOUS-CSV-020 | csv | reject | XFAIL | 0.029 | CSV_GREEDY: Input was parsed and produced a schema-valid event. |
| JSON-ARRAY-001 | json | reject | XPASS | 0.010 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-002 | json | reject | XPASS | 0.005 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-003 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-004 | json | reject | XPASS | 0.005 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-005 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-006 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-007 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-008 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-009 | json | reject | XPASS | 0.003 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-010 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-011 | json | reject | XPASS | 0.003 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-012 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-013 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-014 | json | reject | XPASS | 0.003 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-015 | json | reject | XPASS | 0.003 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-016 | json | reject | XPASS | 0.003 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-017 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-018 | json | reject | XPASS | 0.004 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-019 | json | reject | XPASS | 0.003 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| JSON-ARRAY-020 | json | reject | XPASS | 0.003 | Known defect not reproduced (JSON_ARRAY_AS_CSV). Expected JSON object, got list |
| BAD-PORT-RANGE | cef | reject | XFAIL | 0.052 | PORT_RANGE: Input was parsed and produced a schema-valid event. |
| BAD-NESTED-ENDPOINT | json | reject | PASS_NO | 0.053 | Strict event validation rejected input: 1 validation error for UniversalEvent src_endpoint.ip   Input should be a valid string [type=string_type, input_value={'ip': '192.0.2.1'}, input_type=dict]     For further information visit https://errors.pydantic.dev/2.13/v/string_type |
| BAD-JSON-PORT-TYPE | json | reject | XFAIL | 0.037 | INVALID_PORT_TYPE: Input was parsed and produced a schema-valid event. |
| BAD-SYSLOG-PRI-SYNTAX | xml | reject | PASS_NO | 0.027 | no element found: line 1, column 21 |
| FUZZ-001 | cef | fuzz | PASS_YES | 0.053 | Mutation parsed and normalized without an exception. |
| FUZZ-002 | cef | fuzz | PASS_YES | 0.043 | Mutation parsed and normalized without an exception. |
| FUZZ-003 | cef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-004 | cef | fuzz | PASS_NO | 0.068 | Strict event validation failed: 1 validation error for UniversalEvent src_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='6553t=0', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-005 | cef | fuzz | PASS_YES | 0.041 | Mutation parsed and normalized without an exception. |
| FUZZ-006 | cef | fuzz | PASS_NO | 0.045 | Strict event validation failed: 1 validation error for UniversalEvent src_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='1 \x00dpt=443', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-007 | cef | fuzz | PASS_NO | 0.006 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 7 |
| FUZZ-008 | cef | fuzz | PASS_NO | 0.005 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 7 |
| FUZZ-009 | cef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-010 | cef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-011 | cef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-012 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-013 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-014 | cef | fuzz | PASS_NO | 0.044 | Strict event validation failed: 1 validation error for UniversalEvent src_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='1=443', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-015 | - | fuzz | PASS_NO | 0.007 | No parser matched log: 'CE:F0\|Acme\|Edge\|1.0\|1014\|Network coconnection\|3\|src=10.0.0.15 dst=198.51.100.\x0015' |
| FUZZ-016 | cef | fuzz | PASS_YES | 0.041 | Mutation parsed and normalized without an exception. |
| FUZZ-017 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-018 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-019 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-020 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-021 | cef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-022 | cef | fuzz | PASS_NO | 0.054 | Strict event validation failed: 2 validation errors for UniversalEvent src_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='1\x00', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='443 prot\x00o=tcp', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-023 | cef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-024 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-025 | cef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-026 | cef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-027 | cef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-028 | cef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-029 | cef | fuzz | PASS_NO | 0.045 | Strict event validation failed: 1 validation error for UniversalEvent dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='1to=tcp', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-030 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-031 | cef | fuzz | PASS_NO | 0.051 | Strict event validation failed: 1 validation error for UniversalEvent dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='65535 pro5535 pro\x00to=tcp', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-032 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-033 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-034 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-035 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-036 | cef | fuzz | PASS_NO | 0.053 | Strict event validation failed: 1 validation error for UniversalEvent dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='0\x00', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-037 | - | fuzz | PASS_NO | 0.006 | No parser matched log: 'LEEF1:.0\|Acme\|Gay\|1.0\|evt-0\trsc=10.1.0.1\tsrcPort=0\tproto=tcp' |
| FUZZ-038 | leef | fuzz | PASS_YES | 0.052 | Mutation parsed and normalized without an exception. |
| FUZZ-039 | leef | fuzz | PASS_YES | 0.050 | Mutation parsed and normalized without an exception. |
| FUZZ-040 | leef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-041 | leef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-042 | leef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-043 | leef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-044 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-045 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-046 | leef | fuzz | PASS_YES | 0.077 | Mutation parsed and normalized without an exception. |
| FUZZ-047 | leef | fuzz | PASS_YES | 0.077 | Mutation parsed and normalized without an exception. |
| FUZZ-048 | leef | fuzz | PASS_YES | 0.233 | Mutation parsed and normalized without an exception. |
| FUZZ-049 | leef | fuzz | PASS_YES | 0.047 | Mutation parsed and normalized without an exception. |
| FUZZ-050 | csv | fuzz | PASS_YES | 0.051 | Mutation parsed and normalized without an exception. |
| FUZZ-051 | leef | fuzz | PASS_YES | 0.041 | Mutation parsed and normalized without an exception. |
| FUZZ-052 | leef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-053 | leef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-054 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-055 | leef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-056 | leef | fuzz | PASS_YES | 0.074 | Mutation parsed and normalized without an exception. |
| FUZZ-057 | leef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-058 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-059 | leef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-060 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-061 | - | fuzz | PASS_NO | 0.007 | No parser matched log: 'LEEFEF:1.0\|Acme\|Gateway\|1.0\|evt-24\tsrc=10.1.0.25\tsrcPort=0\tproto=tcp' |
| FUZZ-062 | leef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-063 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-064 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-065 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-066 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-067 | syslog | fuzz | PASS_YES | 0.090 | Mutation parsed and normalized without an exception. |
| FUZZ-068 | syslog | fuzz | PASS_YES | 0.066 | Mutation parsed and normalized without an exception. |
| FUZZ-069 | syslog | fuzz | PASS_YES | 0.061 | Mutation parsed and normalized without an exception. |
| FUZZ-070 | syslog | fuzz | PASS_YES | 0.060 | Mutation parsed and normalized without an exception. |
| FUZZ-071 | syslog | fuzz | PASS_YES | 0.055 | Mutation parsed and normalized without an exception. |
| FUZZ-072 | syslog | fuzz | PASS_YES | 0.058 | Mutation parsed and normalized without an exception. |
| FUZZ-073 | syslog | fuzz | PASS_YES | 0.058 | Mutation parsed and normalized without an exception. |
| FUZZ-074 | syslog | fuzz | PASS_YES | 0.055 | Mutation parsed and normalized without an exception. |
| FUZZ-075 | syslog | fuzz | PASS_YES | 0.052 | Mutation parsed and normalized without an exception. |
| FUZZ-076 | syslog | fuzz | PASS_YES | 0.058 | Mutation parsed and normalized without an exception. |
| FUZZ-077 | syslog | fuzz | PASS_YES | 0.058 | Mutation parsed and normalized without an exception. |
| FUZZ-078 | syslog | fuzz | PASS_YES | 0.061 | Mutation parsed and normalized without an exception. |
| FUZZ-079 | syslog | fuzz | PASS_YES | 0.070 | Mutation parsed and normalized without an exception. |
| FUZZ-080 | syslog | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-081 | syslog | fuzz | PASS_YES | 0.062 | Mutation parsed and normalized without an exception. |
| FUZZ-082 | syslog | fuzz | PASS_YES | 0.059 | Mutation parsed and normalized without an exception. |
| FUZZ-083 | syslog | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-084 | syslog | fuzz | PASS_YES | 0.053 | Mutation parsed and normalized without an exception. |
| FUZZ-085 | syslog | fuzz | PASS_YES | 0.055 | Mutation parsed and normalized without an exception. |
| FUZZ-086 | syslog | fuzz | PASS_YES | 0.058 | Mutation parsed and normalized without an exception. |
| FUZZ-087 | syslog | fuzz | PASS_YES | 0.059 | Mutation parsed and normalized without an exception. |
| FUZZ-088 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-089 | syslog | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-090 | syslog | fuzz | PASS_YES | 0.062 | Mutation parsed and normalized without an exception. |
| FUZZ-091 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-092 | syslog | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-093 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-094 | syslog | fuzz | PASS_YES | 0.053 | Mutation parsed and normalized without an exception. |
| FUZZ-095 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-096 | syslog | fuzz | PASS_YES | 0.055 | Mutation parsed and normalized without an exception. |
| FUZZ-097 | syslog | fuzz | PASS_YES | 0.052 | Mutation parsed and normalized without an exception. |
| FUZZ-098 | syslog | fuzz | PASS_YES | 64.732 | Mutation parsed and normalized without an exception. |
| FUZZ-099 | syslog | fuzz | PASS_YES | 0.109 | Mutation parsed and normalized without an exception. |
| FUZZ-100 | syslog | fuzz | PASS_YES | 0.071 | Mutation parsed and normalized without an exception. |
| FUZZ-101 | syslog | fuzz | PASS_YES | 0.062 | Mutation parsed and normalized without an exception. |
| FUZZ-102 | syslog | fuzz | PASS_YES | 0.059 | Mutation parsed and normalized without an exception. |
| FUZZ-103 | json | fuzz | PASS_YES | 0.058 | Mutation parsed and normalized without an exception. |
| FUZZ-104 | json | fuzz | PASS_NO | 0.022 | JSON decode error: Expecting value at position 8 |
| FUZZ-105 | json | fuzz | PASS_NO | 0.011 | JSON decode error: Expecting property name enclosed in double quotes at position 21 |
| FUZZ-106 | json | fuzz | PASS_NO | 0.009 | JSON decode error: Invalid control character at at position 50 |
| FUZZ-107 | json | fuzz | PASS_NO | 0.008 | JSON decode error: Expecting ',' delimiter at position 153 |
| FUZZ-108 | json | fuzz | PASS_NO | 0.009 | JSON decode error: Expecting ':' delimiter at position 107 |
| FUZZ-109 | json | fuzz | PASS_YES | 0.049 | Mutation parsed and normalized without an exception. |
| FUZZ-110 | json | fuzz | PASS_NO | 0.010 | JSON decode error: Expecting ',' delimiter at position 14 |
| FUZZ-111 | json | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-112 | json | fuzz | PASS_NO | 0.010 | JSON decode error: Expecting ',' delimiter at position 196 |
| FUZZ-113 | json | fuzz | PASS_NO | 0.008 | JSON decode error: Expecting ',' delimiter at position 128 |
| FUZZ-114 | json | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-115 | json | fuzz | PASS_NO | 0.008 | JSON decode error: Expecting property name enclosed in double quotes at position 74 |
| FUZZ-116 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Expecting ':' delimiter at position 84 |
| FUZZ-117 | json | fuzz | PASS_NO | 0.006 | JSON decode error: Invalid control character at at position 51 |
| FUZZ-118 | json | fuzz | PASS_NO | 0.006 | JSON decode error: Invalid control character at at position 33 |
| FUZZ-119 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Invalid control character at at position 111 |
| FUZZ-120 | json | fuzz | PASS_NO | 0.006 | JSON decode error: Invalid control character at at position 108 |
| FUZZ-121 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Unterminated string starting at at position 182 |
| FUZZ-122 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Expecting ',' delimiter at position 142 |
| FUZZ-123 | json | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-124 | json | fuzz | PASS_NO | 0.008 | JSON decode error: Invalid control character at at position 32 |
| FUZZ-125 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Invalid control character at at position 101 |
| FUZZ-126 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Expecting ',' delimiter at position 106 |
| FUZZ-127 | json | fuzz | PASS_NO | 0.006 | JSON decode error: Expecting ',' delimiter at position 11 |
| FUZZ-128 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Invalid control character at at position 144 |
| FUZZ-129 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Invalid control character at at position 136 |
| FUZZ-130 | json | fuzz | PASS_NO | 0.006 | JSON decode error: Expecting ',' delimiter at position 31 |
| FUZZ-131 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Expecting property name enclosed in double quotes at position 47 |
| FUZZ-132 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Expecting ',' delimiter at position 172 |
| FUZZ-133 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Invalid control character at at position 191 |
| FUZZ-134 | json | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-135 | json | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-136 | json | fuzz | PASS_NO | 0.009 | JSON decode error: Invalid control character at at position 96 |
| FUZZ-137 | json | fuzz | PASS_NO | 0.007 | JSON decode error: Expecting ':' delimiter at position 7 |
| FUZZ-138 | json | fuzz | PASS_NO | 0.006 | JSON decode error: Expecting ',' delimiter at position 14 |
| FUZZ-139 | xml | fuzz | PASS_NO | 0.047 | not well-formed (invalid token): line 1, column 11 |
| FUZZ-140 | xml | fuzz | PASS_NO | 0.026 | mismatched tag: line 1, column 114 |
| FUZZ-141 | xml | fuzz | PASS_YES | 0.079 | Mutation parsed and normalized without an exception. |
| FUZZ-142 | xml | fuzz | PASS_NO | 0.023 | mismatched tag: line 1, column 73 |
| FUZZ-143 | xml | fuzz | PASS_NO | 0.018 | mismatched tag: line 1, column 24 |
| FUZZ-144 | xml | fuzz | PASS_NO | 0.016 | mismatched tag: line 1, column 24 |
| FUZZ-145 | xml | fuzz | PASS_NO | 0.018 | not well-formed (invalid token): line 1, column 74 |
| FUZZ-146 | xml | fuzz | PASS_NO | 0.015 | not well-formed (invalid token): line 1, column 9 |
| FUZZ-147 | xml | fuzz | PASS_NO | 0.017 | mismatched tag: line 1, column 91 |
| FUZZ-148 | xml | fuzz | PASS_NO | 0.019 | not well-formed (invalid token): line 1, column 150 |
| FUZZ-149 | xml | fuzz | PASS_YES | 0.063 | Mutation parsed and normalized without an exception. |
| FUZZ-150 | xml | fuzz | PASS_NO | 0.024 | no element found: line 1, column 180 |
| FUZZ-151 | xml | fuzz | PASS_NO | 0.020 | mismatched tag: line 1, column 172 |
| FUZZ-152 | xml | fuzz | PASS_NO | 0.017 | not well-formed (invalid token): line 1, column 90 |
| FUZZ-153 | xml | fuzz | PASS_NO | 0.018 | not well-formed (invalid token): line 1, column 107 |
| FUZZ-154 | xml | fuzz | PASS_NO | 0.019 | mismatched tag: line 1, column 168 |
| FUZZ-155 | xml | fuzz | PASS_NO | 0.019 | mismatched tag: line 1, column 168 |
| FUZZ-156 | xml | fuzz | PASS_NO | 0.018 | mismatched tag: line 1, column 157 |
| FUZZ-157 | xml | fuzz | PASS_YES | 0.062 | Mutation parsed and normalized without an exception. |
| FUZZ-158 | xml | fuzz | PASS_YES | 0.060 | Mutation parsed and normalized without an exception. |
| FUZZ-159 | xml | fuzz | PASS_NO | 0.021 | mismatched tag: line 1, column 116 |
| FUZZ-160 | xml | fuzz | PASS_NO | 0.018 | not well-formed (invalid token): line 1, column 71 |
| FUZZ-161 | xml | fuzz | PASS_NO | 0.016 | not well-formed (invalid token): line 1, column 81 |
| FUZZ-162 | xml | fuzz | PASS_YES | 0.059 | Mutation parsed and normalized without an exception. |
| FUZZ-163 | xml | fuzz | PASS_NO | 0.022 | mismatched tag: line 1, column 181 |
| FUZZ-164 | xml | fuzz | PASS_NO | 0.032 | mismatched tag: line 1, column 122 |
| FUZZ-165 | xml | fuzz | PASS_NO | 0.021 | mismatched tag: line 1, column 169 |
| FUZZ-166 | xml | fuzz | PASS_NO | 0.018 | mismatched tag: line 1, column 158 |
| FUZZ-167 | xml | fuzz | PASS_NO | 0.057 | mismatched tag: line 1, column 67 |
| FUZZ-168 | xml | fuzz | PASS_NO | 0.040 | not well-formed (invalid token): line 1, column 72 |
| FUZZ-169 | csv | fuzz | PASS_YES | 0.121 | Mutation parsed and normalized without an exception. |
| FUZZ-170 | csv | fuzz | PASS_NO | 0.098 | Strict event validation failed: 'NoneType' object has no attribute 'startswith' |
| FUZZ-171 | csv | fuzz | PASS_YES | 0.080 | Mutation parsed and normalized without an exception. |
| FUZZ-172 | csv | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-173 | csv | fuzz | PASS_YES | 0.048 | Mutation parsed and normalized without an exception. |
| FUZZ-174 | csv | fuzz | PASS_YES | 0.044 | Mutation parsed and normalized without an exception. |
| FUZZ-175 | csv | fuzz | PASS_YES | 0.043 | Mutation parsed and normalized without an exception. |
| FUZZ-176 | csv | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-177 | csv | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-178 | csv | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-179 | csv | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-180 | csv | fuzz | PASS_NO | 0.042 | Strict event validation failed: 'NoneType' object has no attribute 'startswith' |
| FUZZ-181 | csv | fuzz | PASS_NO | 0.040 | Strict event validation failed: 'NoneType' object has no attribute 'startswith' |
| FUZZ-182 | csv | fuzz | PASS_YES | 0.042 | Mutation parsed and normalized without an exception. |
| FUZZ-183 | csv | fuzz | PASS_YES | 0.041 | Mutation parsed and normalized without an exception. |
| FUZZ-184 | csv | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-185 | csv | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-186 | csv | fuzz | PASS_YES | 0.049 | Mutation parsed and normalized without an exception. |
| FUZZ-187 | csv | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-188 | csv | fuzz | PASS_NO | 0.039 | Strict event validation failed: 'NoneType' object has no attribute 'startswith' |
| FUZZ-189 | csv | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-190 | csv | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-191 | csv | fuzz | PASS_YES | 0.043 | Mutation parsed and normalized without an exception. |
| FUZZ-192 | csv | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-193 | csv | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-194 | csv | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-195 | csv | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-196 | csv | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-197 | csv | fuzz | PASS_NO | 0.038 | Strict event validation failed: 'NoneType' object has no attribute 'startswith' |
| FUZZ-198 | csv | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-199 | json | fuzz | PASS_YES | 0.041 | Mutation parsed and normalized without an exception. |
| FUZZ-200 | csv | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-201 | - | fuzz | PASS_NO | 0.006 | No parser matched log: '}{' |
| FUZZ-202 | json | fuzz | PASS_NO | 0.053 | Strict event validation failed: 1 validation error for UniversalEvent src_endpoint.ip   Input should be a valid string [type=string_type, input_value={'ip': '192.0.2.10'}, input_type=dict]     For further information visit https://errors.pydantic.dev/2.13/v/string_type |
| FUZZ-203 | cef | fuzz | PASS_YES | 0.043 | Mutation parsed and normalized without an exception. |
| FUZZ-204 | csv | fuzz | PASS_YES | 0.045 | Mutation parsed and normalized without an exception. |
| FUZZ-205 | json | fuzz | PASS_NO | 0.022 | JSON decode error: Expecting ':' delimiter at position 3 |
| FUZZ-206 | json | fuzz | PASS_NO | 0.166 | JSON decode error: Invalid control character at at position 27303 |
| FUZZ-207 | json | fuzz | PASS_NO | 0.009 | JSON decode error: Expecting property name enclosed in double quotes at position 36 |
| FUZZ-208 | - | fuzz | PASS_NO | 0.005 | No parser matched log: '\x00{"messa\x00ge":"timeout after deny"}' |
| FUZZ-209 | - | fuzz | PASS_NO | 0.003 | No parser matched log: '\x00{"message":\x00"login attempt"}' |
| FUZZ-210 | syslog | fuzz | PASS_YES | 0.090 | Mutation parsed and normalized without an exception. |
| FUZZ-211 | json | fuzz | PASS_YES | 0.043 | Mutation parsed and normalized without an exception. |
| FUZZ-212 | xml | fuzz | PASS_YES | 0.078 | Mutation parsed and normalized without an exception. |
| FUZZ-213 | cef | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-214 | - | fuzz | PASS_NO | 0.006 | No parser matched log: 'ECF:0\|Acme\|Edge\|1.0\|1001\|Network connection\|1\|src=10.0.0.2 dst=198.51.100.2 spt=' |
| FUZZ-215 | cef | fuzz | PASS_YES | 0.041 | Mutation parsed and normalized without an exception. |
| FUZZ-216 | cef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-217 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-218 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-219 | cef | fuzz | PASS_NO | 0.052 | Strict event validation failed: 1 validation error for UniversalEvent dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='655proto=tcp', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-220 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-221 | cef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-222 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-223 | cef | fuzz | PASS_NO | 0.044 | Strict event validation failed: 1 validation error for UniversalEvent dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='65535 prot\x00o=tcp', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-224 | cef | fuzz | PASS_NO | 0.049 | Strict event validation failed: 1 validation error for UniversalEvent dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='0p', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-225 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-226 | cef | fuzz | PASS_NO | 0.043 | Strict event validation failed: 1 validation error for UniversalEvent dst_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='443 pro', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-227 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-228 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-229 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-230 | cef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-231 | cef | fuzz | PASS_YES | 0.034 | Mutation parsed and normalized without an exception. |
| FUZZ-232 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-233 | cef | fuzz | PASS_NO | 0.005 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 7 |
| FUZZ-234 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-235 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-236 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-237 | cef | fuzz | PASS_NO | 0.005 | Invalid CEF format: expected at least 8 pipe-delimited header fields, got 6 |
| FUZZ-238 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-239 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-240 | cef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-241 | cef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-242 | - | fuzz | PASS_NO | 0.006 | No parser matched log: 'C\x00EF:0\|Acme\|Edge\|1.0\|1029\|Network connection\|7\|src=10.0.0.30 dst=198.51.1000 spt' |
| FUZZ-243 | cef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-244 | cef | fuzz | PASS_NO | 0.043 | Strict event validation failed: 1 validation error for UniversalEvent src_endpoint.port   Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='65535 dp\x00t=0 prot\x00o=tcp', input_type=str]     For further information visit https://errors.pydantic.dev/2.13/v/int_parsing |
| FUZZ-245 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-246 | - | fuzz | PASS_NO | 0.005 | No parser matched log: 'CEF\x00:0\|Acme\|Edge\|1.0\|1033\|Network connection\|0\|src=10.0.0.34 dst=198.51.100.34 s' |
| FUZZ-247 | cef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-248 | cef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-249 | leef | fuzz | PASS_YES | 0.050 | Mutation parsed and normalized without an exception. |
| FUZZ-250 | leef | fuzz | PASS_YES | 0.041 | Mutation parsed and normalized without an exception. |
| FUZZ-251 | leef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-252 | leef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-253 | leef | fuzz | PASS_NO | 0.005 | Invalid LEEF format: expected ≥5 pipe-delimited fields, got 4 |
| FUZZ-254 | leef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-255 | leef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-256 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-257 | leef | fuzz | PASS_YES | 0.034 | Mutation parsed and normalized without an exception. |
| FUZZ-258 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-259 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-260 | leef | fuzz | PASS_YES | 0.049 | Mutation parsed and normalized without an exception. |
| FUZZ-261 | leef | fuzz | PASS_YES | 0.039 | Mutation parsed and normalized without an exception. |
| FUZZ-262 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-263 | - | fuzz | PASS_NO | 0.006 | No parser matched log: 'LEF:1.0\|Acme\|Gateway\|1.0\|ev\x00t-14\tsrc=10.1.0.15\tsrcPort=443\tproto=tcp' |
| FUZZ-264 | leef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-265 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-266 | leef | fuzz | PASS_YES | 0.089 | Mutation parsed and normalized without an exception. |
| FUZZ-267 | leef | fuzz | PASS_YES | 0.040 | Mutation parsed and normalized without an exception. |
| FUZZ-268 | leef | fuzz | PASS_YES | 0.038 | Mutation parsed and normalized without an exception. |
| FUZZ-269 | leef | fuzz | PASS_YES | 0.036 | Mutation parsed and normalized without an exception. |
| FUZZ-270 | - | fuzz | PASS_NO | 0.006 | No parser matched log: 'LE\x00EF:2.0\|Acme\|Gateway\|\x001.0\|evt-21\|\t\|src=10.1.0.22\tsrcPort=1\tproto=tcp' |
| FUZZ-271 | leef | fuzz | PASS_YES | 0.037 | Mutation parsed and normalized without an exception. |
| FUZZ-272 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-273 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-274 | leef | fuzz | PASS_YES | 0.035 | Mutation parsed and normalized without an exception. |
| FUZZ-275 | leef | fuzz | PASS_YES | 0.033 | Mutation parsed and normalized without an exception. |
| FUZZ-276 | leef | fuzz | PASS_YES | 0.031 | Mutation parsed and normalized without an exception. |
| FUZZ-277 | leef | fuzz | PASS_YES | 0.034 | Mutation parsed and normalized without an exception. |
| FUZZ-278 | leef | fuzz | PASS_YES | 0.065 | Mutation parsed and normalized without an exception. |
| FUZZ-279 | syslog | fuzz | PASS_YES | 0.074 | Mutation parsed and normalized without an exception. |
| FUZZ-280 | syslog | fuzz | PASS_YES | 0.222 | Mutation parsed and normalized without an exception. |
| FUZZ-281 | syslog | fuzz | PASS_YES | 0.073 | Mutation parsed and normalized without an exception. |
| FUZZ-282 | syslog | fuzz | PASS_YES | 0.061 | Mutation parsed and normalized without an exception. |
| FUZZ-283 | syslog | fuzz | PASS_YES | 0.063 | Mutation parsed and normalized without an exception. |
| FUZZ-284 | syslog | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-285 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-286 | syslog | fuzz | PASS_YES | 0.062 | Mutation parsed and normalized without an exception. |
| FUZZ-287 | syslog | fuzz | PASS_YES | 0.053 | Mutation parsed and normalized without an exception. |
| FUZZ-288 | syslog | fuzz | PASS_YES | 0.062 | Mutation parsed and normalized without an exception. |
| FUZZ-289 | syslog | fuzz | PASS_YES | 0.067 | Mutation parsed and normalized without an exception. |
| FUZZ-290 | syslog | fuzz | PASS_YES | 0.059 | Mutation parsed and normalized without an exception. |
| FUZZ-291 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-292 | syslog | fuzz | PASS_YES | 0.064 | Mutation parsed and normalized without an exception. |
| FUZZ-293 | syslog | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-294 | syslog | fuzz | PASS_YES | 0.059 | Mutation parsed and normalized without an exception. |
| FUZZ-295 | syslog | fuzz | PASS_YES | 0.057 | Mutation parsed and normalized without an exception. |
| FUZZ-296 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-297 | syslog | fuzz | PASS_YES | 0.054 | Mutation parsed and normalized without an exception. |
| FUZZ-298 | syslog | fuzz | PASS_YES | 0.058 | Mutation parsed and normalized without an exception. |
| FUZZ-299 | syslog | fuzz | PASS_YES | 0.097 | Mutation parsed and normalized without an exception. |
| FUZZ-300 | - | fuzz | PASS_NO | 0.006 | No parser matched log: '>1 2025-01-02T03:04:05Z fw-21 filter 123 ID47 - SRC=192.0.2.22 DST=198.51.100.22' |
