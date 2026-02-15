"""Simple log line parser for MVP.

Supports common formats:
    [2026-02-12 10:32:11] ERROR Something failed
    2024-11-19 08:00:15 - ERROR: Database connection failed

"""

import re
from datetime import datetime

from app.schemas.log_entry import ParsedLogLine

_PATTERNS = [
    # Format 1: [YYYY-MM-DD HH:MM:SS] LEVEL message
    re.compile(
        r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]"
        r"\s+(?P<level>\w+)"
        r"\s+(?P<message>.+)$"
    ),
    # Format 2: YYYY-MM-DD HH:MM:SS - LEVEL: message
    re.compile(
        r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})"
        r"\s+-\s+(?P<level>\w+):\s*"
        r"(?P<message>.+)$"
    ),
]

_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_line(line: str) -> ParsedLogLine:
    """Parse a single log line. Returns raw_content even on failure."""
    line = line.strip()

    for pattern in _PATTERNS:
        match = pattern.match(line)
        if match:
            try:
                logged_at = datetime.strptime(match.group("timestamp"), _TIMESTAMP_FORMAT)
            except ValueError:
                logged_at = None

            return ParsedLogLine(
                raw_content=line,
                logged_at=logged_at,
                level=match.group("level").upper(),
                message=match.group("message"),
            )

    return ParsedLogLine(raw_content=line)


def parse_file_content(content: str) -> list[ParsedLogLine]:
    """Parse all non-empty lines from a log file."""
    return [parse_line(line) for line in content.splitlines() if line.strip()]
