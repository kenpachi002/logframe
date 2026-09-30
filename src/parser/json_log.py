"""
JSON log parser — extracted from normalizer.py into its own module.

Follows the same contract as parser/cef.py and parser/syslog.py:
  parse_json_log(src: str) -> dict
  - Returns a flat dict with all source fields preserved.
  - Always includes raw_data = src.
  - On failure, returns {"error_message": ..., "raw_data": src}.
"""
import json


def parse_json_log(src: str) -> dict:
    """
    Parse a JSON-formatted log line.
    The JSON object is returned as-is with raw_data appended.
    Raises nothing — errors are returned in the dict.
    """
    try:
        parsed = json.loads(src)
    except json.JSONDecodeError as exc:
        return {
            "error_message": f"JSON decode error: {exc.msg} at position {exc.pos}",
            "raw_data": src,
        }

    if not isinstance(parsed, dict):
        return {
            "error_message": f"Expected JSON object, got {type(parsed).__name__}",
            "raw_data": src,
        }

    parsed["raw_data"] = src
    return parsed
