"""Date parsing utility for natural language dates."""
from dateparser import parse
from datetime import datetime
from typing import Optional


def parse_due_date(date_str: str) -> Optional[datetime]:
    """
    Parse natural language date to datetime.

    Supports:
    - ISO 8601: "2026-01-16T15:00:00Z"
    - Relative: "tomorrow", "next week", "in 3 days"
    - Named days: "Monday", "next Friday"
    - Special: "today", "tonight", "end of month"

    Args:
        date_str: Date string in various formats

    Returns:
        Parsed datetime or None if invalid

    Raises:
        ValueError: If date format is invalid
    """
    if not date_str:
        return None

    # Try ISO 8601 first
    try:
        return datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    except ValueError:
        pass

    # Try natural language parsing
    parsed = parse(
        date_str,
        settings={
            'PREFER_DATES_FROM': 'future',
            'RETURN_AS_TIMEZONE_AWARE': False
        }
    )

    if parsed:
        return parsed

    raise ValueError(f"Invalid date format: {date_str}")
