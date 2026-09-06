from fastapi import FastAPI

from app.api.routes import campaigns, health, runs, targets
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title="Agent-on-Agent Red Teaming Platform API",
        version=settings.app_version,
        summary="Backend API for authorized local/lab LLM red-team campaigns.",
    )
    app.include_router(health.router)
    app.include_router(campaigns.router)
    app.include_router(targets.router)
    app.include_router(runs.router)
    return app


app = create_app()
