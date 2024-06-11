"""
Thumbnail Generation API

This module defines a FastAPI application for a Thumbnail Generation API.
"""

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import config
from api.router import generate, swc, health

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

app = FastAPI(
    title="Thumbnail Generation API",
    debug=config.DEBUG_MODE,
    version="0.4.4",
    openapi_tags=tags_metadata,
    docs_url=f"{config.BASE_PATH}/docs",
    openapi_url=f"{config.BASE_PATH}/openapi.json",
)

base_router = APIRouter(prefix=config.BASE_PATH)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.WHITELISTED_CORS_URLS.split(",")),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
base_router.include_router(generate.router, prefix="/generate", tags=["Generate"])
base_router.include_router(swc.router, prefix="/soma", tags=["Soma"])
base_router.include_router(health.router, tags=["Health"])

app.include_router(base_router)
