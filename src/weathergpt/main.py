"""WeatherGPT FastAPI main application entry point."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from weathergpt.api.routes import router
from weathergpt.core.config import settings
from weathergpt.core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.app_name} v{settings.app_version}...")
    logger.info(f"Supported Languages: {settings.supported_languages}")
    logger.info(f"LLM Provider: {settings.weathergpt_llm_provider}")
    yield
    logger.info(f"Shutting down {settings.app_name}...")


def create_app() -> FastAPI:
    """Factory function for FastAPI application."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=settings.app_description,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS configuration for React frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Mount API routes
    app.include_router(router)

    # Mount static frontend build if present
    frontend_dist = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")
    if os.path.exists(frontend_dist):
        app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "weathergpt.main:app",
        host=settings.weathergpt_host,
        port=settings.weathergpt_port,
        reload=settings.weathergpt_debug,
    )
