"""
Implements async download
"""

import os
from datetime import datetime

import dateutil.parser  # type: ignore
import pytz

TIMEZONE_STR = os.getenv("TIMEZONE", "America/Los_Angeles")
TIMEZONE_INFO = pytz.timezone(TIMEZONE_STR)


def localize_datetime(dt: datetime) -> datetime:
    """Localizes a datetime."""
    if dt.tzinfo is None:
        return TIMEZONE_INFO.localize(dt)
    return dt.astimezone(TIMEZONE_INFO)


def localize_utc_datetime(dt: datetime) -> datetime:
    # set the timezone to UTC
    dt.replace(tzinfo=pytz.UTC)
    return dt.astimezone(TIMEZONE_INFO)


def parse_datetime(dt: str | datetime) -> datetime:
    """Parses a date string."""
    if isinstance(dt, datetime):
        return localize_datetime(dt)
    out: datetime | None = None
    try:
        out = datetime.fromisoformat(dt)
    except ValueError:
        out = dateutil.parser.parse(dt, fuzzy=True)
    assert out is not None
    return localize_datetime(out)
