"""LogEntry model."""

from __future__ import annotations

import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, EmbeddingColumn, TimestampMixin, UUIDpk


class LogEntry(Base, TimestampMixin):
    __tablename__ = "log_entries"

    id: Mapped[UUIDpk]
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE")
    )
    cluster_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clusters.id", ondelete="SET NULL")
    )
    raw_content: Mapped[str] = mapped_column(Text)
    logged_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    level: Mapped[str | None] = mapped_column(index=True)
    message: Mapped[str | None] = mapped_column(Text)
    source: Mapped[str | None] = mapped_column(index=True)
    embedding: Mapped[EmbeddingColumn]

    project: Mapped["Project"] = relationship(back_populates="log_entries")
    cluster: Mapped["Cluster | None"] = relationship(back_populates="log_entries")
