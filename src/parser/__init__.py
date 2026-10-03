"""
Parser Registry — plug-and-play format dispatcher.

Adding a new format:
  1. Create src/parser/my_format.py with parse_my_format(src: str) -> dict
  2. Add a detect_my_format(src: str) -> bool function below
  3. Add an entry to PARSER_REGISTRY

The registry is evaluated in order: cef → leef → syslog → xml → json → csv.
"""
import re

from parser.cef      import parse_cef
from parser.syslog   import parse_syslog
from parser.json_log import parse_json_log
from parser.xml_log  import parse_xml
from parser.csv_log  import parse_csv_log
from parser.leef     import parse_leef


# ── Detection functions ────────────────────────────────────────────────────────

def detect_cef(src: str) -> bool:
    return src.lstrip().upper().startswith("CEF:")


def detect_leef(src: str) -> bool:
    return src.lstrip().upper().startswith("LEEF:")


def detect_syslog(src: str) -> bool:
    return bool(re.match(r"^<\d+>", src.lstrip()))


def detect_xml(src: str) -> bool:
    s = src.lstrip()
    return s.startswith("<") and not s.startswith("<<")


def detect_json(src: str) -> bool:
    """
    Match JSON objects ({}) and arrays ([]).
    Arrays are detected so that parse_json_log can reject them with a clear
    error message, rather than silently falling to the CSV catch-all.
    """
    s = src.lstrip()
    return s.startswith("{") or s.startswith("[")


def detect_csv(src: str) -> bool:
    """
    CSV is the catch-all: accept if the line has at least one comma
    and does not match any structured format above.
    """
    return "," in src and not detect_cef(src) and not detect_leef(src)


# ── Registry ───────────────────────────────────────────────────────────────────

PARSER_REGISTRY: dict[str, dict] = {
    "cef":    {"detect": detect_cef,    "parse": parse_cef},
    "leef":   {"detect": detect_leef,   "parse": parse_leef},
    "syslog": {"detect": detect_syslog, "parse": parse_syslog},
    "xml":    {"detect": detect_xml,    "parse": parse_xml},
    "json":   {"detect": detect_json,   "parse": parse_json_log},
    "csv":    {"detect": detect_csv,    "parse": parse_csv_log},
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
