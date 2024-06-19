"""
Thumbnail Generation API

This module defines a FastAPI application for a Thumbnail Generation API.
"""

import sentry_sdk
from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.router import generate, swc, health
from settings import settings

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

sentry_sdk.init(
    dsn=settings.SENTRY_DSN, traces_sample_rate=1.0, profiles_sample_rate=1.0, environment=settings.ENVIRONMENT
)

app = FastAPI(
    title="Thumbnail Generation API",
    debug=settings.DEBUG_MODE,
    version="0.5.0",
    openapi_tags=tags_metadata,
    docs_url=f"{settings.BASE_PATH}/docs",
    openapi_url=f"{settings.BASE_PATH}/openapi.json",
)

base_router = APIRouter(prefix=settings.BASE_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.WHITELISTED_CORS_URLS.split(",")),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
base_router.include_router(generate.router, prefix="/generate", tags=["Generate"])
base_router.include_router(swc.router, prefix="/soma", tags=["Soma"])
base_router.include_router(health.router, tags=["Health"])

app.include_router(base_router)
