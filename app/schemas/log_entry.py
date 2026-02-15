"""Pydantic schemas for log entry endpoints."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class ParsedLogLine(BaseModel):
    """A single parsed log line."""

    raw_content: str
    logged_at: datetime | None = None
    level: str | None = None
    message: str | None = None


class LogEntryResponse(BaseModel):
    """A stored log entry returned from the API."""

    id: UUID
    project_id: UUID
    raw_content: str
    logged_at: datetime | None = None
    level: str | None = None
    message: str | None = None

    model_config = {"from_attributes": True}


class UploadLogResponse(BaseModel):
    """Response after uploading and parsing a log file."""

    project_id: UUID
    total_lines: int
    parsed: int
    failed: int
