"""Pydantic schemas for user endpoints."""

from uuid import UUID

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str | None = None


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: str | None

    model_config = {"from_attributes": True}
