"""Project endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectResponse

router = APIRouter()


@router.post("/projects", response_model=ProjectResponse, status_code=201)
async def create_project(
    body: ProjectCreate,
    session: AsyncSession = Depends(get_session),
) -> ProjectResponse:
    """Create a new project."""
    user = await session.get(User, body.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    project = Project(user_id=body.user_id, name=body.name)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return project
