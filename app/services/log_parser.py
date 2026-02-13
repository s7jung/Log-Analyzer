"""Simple log line parser for MVP.

Expected format:
    [2026-02-12 10:32:11] ERROR Something failed

Falls back gracefully. unparseable lines are stored with raw_content only.
"""

import re
from datetime import datetime

from app.schemas.log_entry import ParsedLogLine

# [YYYY-MM-DD HH:MM:SS] LEVEL message
_LOG_PATTERN = re.compile(
    r"^\[(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\]"
    r"\s+(?P<level>\w+)"
    r"\s+(?P<message>.+)$"
)

_TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"


def parse_line(line: str) -> ParsedLogLine:
    """Parse a single log line. Returns raw_content even on failure."""
    line = line.strip()
    match = _LOG_PATTERN.match(line)
    if not match:
        return ParsedLogLine(raw_content=line)

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


def parse_file_content(content: str) -> list[ParsedLogLine]:
    """Parse all non-empty lines from a log file."""
    return [parse_line(line) for line in content.splitlines() if line.strip()]
