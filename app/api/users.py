"""User endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(
    body: UserCreate,
    session: AsyncSession = Depends(get_session),
) -> UserResponse:
    """Create a new user."""
    existing = await session.execute(select(User).where(User.email == body.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered.")

    user = User(
        email=body.email,
        hashed_password=body.password,  # TODO: add hashing
        full_name=body.full_name,
    )
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
