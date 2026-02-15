"""Service layer for log querying and processing."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.log_entry import LogEntry

ERROR_LEVELS = {"ERROR", "FATAL"}


class LogProcessingService:
    """Encapsulates log query and processing logic."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def filter_error_logs(self, project_id: UUID) -> list[LogEntry]:
        """Return only ERROR and FATAL level logs for a project."""
        stmt = (
            select(LogEntry)
            .where(LogEntry.project_id == project_id)
            .where(LogEntry.level.in_(ERROR_LEVELS))
            .order_by(LogEntry.logged_at.asc())
        )
        result = await self._session.execute(stmt)
        return list(result.scalars().all())
