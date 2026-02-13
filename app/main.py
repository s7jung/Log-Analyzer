"""FastAPI application entrypoint."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import health, logs, projects, users
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown hooks."""
    from app.database import create_tables, dispose_engine
    await create_tables()
    yield
    await dispose_engine()


def create_application() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()
    from app import __version__

    app = FastAPI(
        title=settings.app_name,
        version=__version__,
        lifespan=lifespan,
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
    )
    app.include_router(health.router, prefix=settings.api_v1_prefix, tags=["health"])
    app.include_router(users.router, prefix=settings.api_v1_prefix, tags=["users"])
    app.include_router(projects.router, prefix=settings.api_v1_prefix, tags=["projects"])
    app.include_router(logs.router, prefix=settings.api_v1_prefix, tags=["logs"])
    return app


app = create_application()
