"""Health check endpoints."""

from fastapi import APIRouter
from sqlalchemy import text

from app.config import get_settings
from app.database import engine

router = APIRouter()


@router.get("/health", status_code=200)
async def health_check() -> dict:
    """Liveness/readiness check with DB connectivity."""
    db_status = "not_configured"
    db_error: str | None = None

    if get_settings().database_url:
        try:
            async with engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
            db_status = "connected"
        except Exception as e:
            db_status = "error"
            db_error = str(e)

    return {
        "status": "healthy",
        "database": db_status,
        "database_error": db_error,
    }
