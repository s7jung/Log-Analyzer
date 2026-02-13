"""Cluster model."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, EmbeddingColumn, TimestampMixin, UUIDpk


class Cluster(Base, TimestampMixin):
    __tablename__ = "clusters"

    id: Mapped[UUIDpk]
    project_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("projects.id", ondelete="CASCADE")
    )
    label: Mapped[str | None] = mapped_column(index=True)
    embedding: Mapped[EmbeddingColumn]

    project: Mapped["Project"] = relationship(back_populates="clusters")
    log_entries: Mapped[list["LogEntry"]] = relationship(back_populates="cluster")
