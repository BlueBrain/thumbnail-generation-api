"""
Thumbnail Generation API

This module defines a FastAPI application for a Thumbnail Generation API.
"""

from contextlib import asynccontextmanager
import sentry_sdk
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import generate, swc, health
from api.settings import settings

tags_metadata = [
    {
        "name": "Health",
        "description": "Endpoints related to checking the health of the application",
    },
    {
        "name": "Generate",
        "description": "Endpoints related to generating the thumbnail of a resource",
    },
    {
        "name": "Soma",
        "description": "Endpoints related to generating the soma reconstruction of a morphology",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan events set the events that will be executed at the startup (before yield)
    and the shutdown (after yield) of the application
    """
    # pylint: disable=unused-argument
    # pylint: disable=redefined-outer-name
    # Startup code
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn, traces_sample_rate=0.2, profiles_sample_rate=0.05, environment=settings.environment
        )
    yield


app = FastAPI(
    title="Thumbnail Generation API",
    debug=settings.debug_mode,
    lifespan=lifespan,
    version="0.5.0",
    openapi_tags=tags_metadata,
    docs_url=f"{settings.base_path}/docs",
    openapi_url=f"{settings.base_path}/openapi.json",
)


base_router = APIRouter(prefix=settings.base_path)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.whitelisted_cors_urls.split(",")),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
base_router.include_router(generate.router, prefix="/generate", tags=["Generate"])
base_router.include_router(swc.router, prefix="/soma", tags=["Soma"])
base_router.include_router(health.router, tags=["Health"])

app.include_router(base_router)
