"""Pydantic schemas for project endpoints."""

from uuid import UUID

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    user_id: UUID


class ProjectResponse(BaseModel):
    id: UUID
    name: str
    user_id: UUID

    model_config = {"from_attributes": True}
