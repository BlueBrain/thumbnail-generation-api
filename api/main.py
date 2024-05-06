"""
Thumbnail Generation API

This module defines a FastAPI application for a Thumbnail Generation API.
"""

from fastapi import FastAPI
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
        "description": "Endpoints related to generating the thumbnail of a resources",
    },
    {
        "name": "Soma",
        "description": "Endpoints related to generating the soma reconstruction of a morphology",
    },
]

app = FastAPI(
    title="Thumbnail Generation API",
    debug=config.DEBUG_MODE,
    version="0.4.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(config.WHITELISTED_CORS_URLS.split(",")),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(generate.router, prefix="/generate", tags=["Generate"])
app.include_router(swc.router, prefix="/soma", tags=["Soma"])
app.include_router(health.router, tags=["Health"])
