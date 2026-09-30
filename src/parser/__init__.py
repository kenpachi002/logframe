"""
Parser Registry — plug-and-play format dispatcher.

Adding a new format:
  1. Create src/parser/my_format.py with parse_my_format(src: str) -> dict
  2. Add a detect_my_format(src: str) -> bool function below
  3. Add an entry to PARSER_REGISTRY

The registry is evaluated in order: cef → syslog → json.
"""
import re

from parser.cef import parse_cef
from parser.syslog import parse_syslog
from parser.json_log import parse_json_log


# ── Detection functions ────────────────────────────────────────────────────────

def detect_cef(src: str) -> bool:
    return src.lstrip().upper().startswith("CEF:")


def detect_syslog(src: str) -> bool:
    return bool(re.match(r"^<\d+>", src.lstrip()))


def detect_json(src: str) -> bool:
    s = src.lstrip()
    return s.startswith("{")


# ── Registry ───────────────────────────────────────────────────────────────────

PARSER_REGISTRY: dict[str, dict] = {
    "cef":    {"detect": detect_cef,    "parse": parse_cef},
    "syslog": {"detect": detect_syslog, "parse": parse_syslog},
    "json":   {"detect": detect_json,   "parse": parse_json_log},
}


# ── Dispatcher ─────────────────────────────────────────────────────────────────

class UnknownFormatError(ValueError):
    """Raised when no registered parser can handle the input."""


def dispatch(src: str) -> tuple[str, dict]:
    """
    Detect the format of `src` and parse it.

    Returns:
        (format_id, parsed_dict)
            format_id: one of the PARSER_REGISTRY keys
            parsed_dict: flat dict from the parser (always contains 'raw_data')

    Raises:
        UnknownFormatError: if no registered parser recognises the input.
    """
    src = src.strip()
    if not src:
        raise UnknownFormatError("Empty log line")

    for format_id, entry in PARSER_REGISTRY.items():
        if entry["detect"](src):
            parsed = entry["parse"](src)
            return format_id, parsed

    raise UnknownFormatError(f"No parser matched log: {src[:80]!r}")
