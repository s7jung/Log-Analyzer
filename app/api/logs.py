"""Log upload endpoint."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.log_entry import LogEntry
from app.models.project import Project
from app.schemas.log_entry import UploadLogResponse
from app.services.log_parser import parse_file_content

router = APIRouter()

MAX_UPLOAD_BYTES = 10 * 1024 * 1024  # 10 MB


@router.post("/upload-log", response_model=UploadLogResponse)
async def upload_log(
    file: UploadFile,
    project_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> UploadLogResponse:
    """Upload a text log file, parse it, and store entries in the database."""
    # Validate project exists
    project = await session.get(Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")

    # Read and validate file
    raw_bytes = await file.read()
    if len(raw_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds 10 MB limit.")

    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 encoded text.")

    parsed_lines = parse_file_content(content)
    if not parsed_lines:
        raise HTTPException(status_code=400, detail="File is empty or has no valid lines.")

    # Store entries
    parsed_count = 0
    failed_count = 0

    for line in parsed_lines:
        if line.logged_at is not None:
            parsed_count += 1
        else:
            failed_count += 1

        session.add(LogEntry(
            project_id=project_id,
            raw_content=line.raw_content,
            logged_at=line.logged_at,
            level=line.level,
            message=line.message,
        ))

    await session.commit()

    return UploadLogResponse(
        project_id=project_id,
        total_lines=len(parsed_lines),
        parsed=parsed_count,
        failed=failed_count,
    )
