"""
Severity mapping helpers — extracted from normalizer.py (no logic changes).

Syslog severity: 0 (emergency) → 7 (debug)
CEF severity:    0 (lowest)    → 10 (highest)
ULPF scale:      1 (info)      → 5 (critical), -1 = unknown
"""


def syslog_severity_to_ulpf(sid: str) -> int:
    """Map Syslog severity code (0–7) to ULPF 1–5 scale."""
    if sid in ("0", "1"):
        return 5  # emergency / alert → critical
    elif sid in ("2", "3"):
        return 4  # critical / error  → high
    elif sid == "4":
        return 3  # warning           → medium
    elif sid == "5":
        return 2  # notice            → low
    elif sid in ("6", "7"):
        return 1  # info / debug      → informational
    return -1


def cef_severity_to_ulpf(cid: str) -> int:
    """Map CEF severity code (0–10) to ULPF 1–5 scale."""
    if cid in ("0", "1", "2", "3"):
        return 1  # low
    elif cid == "4":
        return 2
    elif cid == "5":
        return 3
    elif cid in ("6", "7"):
        return 4
    elif cid in ("8", "9", "10"):
        return 5  # critical
    return -1


def get_ulpf_severity_name(uid: int) -> str:
    """Return human-readable ULPF severity name from ULPF severity ID."""
    names = {
        1: "Informational",
        2: "Low",
        3: "Medium",
        4: "High",
        5: "Critical",
    }
    return names.get(uid, "Unknown")
