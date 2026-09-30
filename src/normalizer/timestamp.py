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
    Parse an ISO 8601 UTC timestamp (e.g. '2026-09-22T14:15:31Z') and return
    Unix epoch seconds.  Returns -1 on parse error.
    """
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ"):
        try:
            return int(
                datetime.strptime(raw, fmt).replace(tzinfo=timezone.utc).timestamp()
            )
        except ValueError:
            continue
    return -1
