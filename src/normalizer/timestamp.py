"""
Timestamp normalization helpers — extracted from normalizer.py.

Key changes vs. original:
- get_as_utc_timestamp() now accepts `zone` as a parameter (no hardcoded Asia/Kolkata).
  Callers must pass config.LOG_TIMEZONE.
- get_utc_timestamp() unchanged.
"""
from datetime import datetime, timezone

from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def get_as_utc_timestamp(raw: str, zone: str) -> int:
    """
    Parse an RFC 3164 timestamp (e.g. 'Sep 22 14:05:31') in the given timezone
    and return Unix epoch seconds (UTC).  Returns -1 on any error.
    """
    try:
        tz = ZoneInfo(zone)
    except ZoneInfoNotFoundError:
        return -1
    year = datetime.now(tz).year
    for fmt in ("%Y %b %d %H:%M:%S", "%Y %b  %d %H:%M:%S"):
        try:
            return int(
                datetime.strptime(f"{year} {raw}", fmt)
                .replace(tzinfo=tz)
                .timestamp()
            )
        except ValueError:
            continue
    return -1


def get_utc_timestamp(raw: str) -> int:
    """
    Parse an ISO 8601 timestamp (with Z, +HH:MM offset, or no offset) and
    return Unix epoch seconds (UTC).  Returns -1 on parse error.

    Handles: '2026-09-22T14:15:31Z', '2026-09-22T14:15:31+05:30',
             '2026-09-22T14:15:31.123Z', '2026-09-22T14:15:31'
    """
    try:
        # Normalize 'Z' → '+00:00' for fromisoformat (Python < 3.11 compat)
        dt = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            # Naive datetime — assume UTC
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.astimezone(timezone.utc).timestamp())
    except ValueError:
        return -1
