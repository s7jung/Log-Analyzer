"""SQLAlchemy declarative base, shared types, and mixins."""

import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import DateTime, Float, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Reusable annotated types
UUIDpk = Annotated[
    uuid.UUID,
    mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
]

EmbeddingColumn = Annotated[
    list[float] | None,
    mapped_column(ARRAY(Float, dimensions=1)),
]


class TimestampMixin:
    """Adds created_at / updated_at to any model."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class Base(DeclarativeBase):
    """Declarative base for all models."""
