"""Project model."""

from __future__ import annotations

import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin, UUIDpk


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    id: Mapped[UUIDpk]
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE")
    )
    name: Mapped[str]

    user: Mapped["User"] = relationship(back_populates="projects")
    log_entries: Mapped[list["LogEntry"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
    clusters: Mapped[list["Cluster"]] = relationship(
        back_populates="project", cascade="all, delete-orphan"
    )
