"""
Thumbnail Generation API

This module defines a FastAPI application for a Thumbnail Generation API.

The application includes a single route:

- GET /: Returns a simple JSON response with the message "Hello World."

Usage:
1. Import the FastAPI class.
2. Create an instance of the FastAPI class with the desired configuration.
3. Define routes using the @app.get() decorator.

Example:
"""

from fastapi import FastAPI
from api.router import generate

tags_metadata = [
    {
        "name": "Generate",
        "description": "Generate a PNG image of a morphology",
    },
]

app = FastAPI(
    title="Thumbnail Generation API",
    debug=True,
    version="0.1.0",
)

# Include routers
app.include_router(generate.router, prefix="/generate")
