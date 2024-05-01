"""
Module: health.py

This module provides a simple health check endpoint for the web server.
"""

from fastapi import APIRouter


router = APIRouter()


@router.get("/health")
async def health():
    """Simple health check endpoint"""
    return {"status": "OK"}
