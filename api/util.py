"""
Module: util.py

This module provides utility functions.
"""

from typing import Optional
from fastapi import Query
from starlette.requests import Request
from api.dependencies import retrieve_user


async def common_params(
    request: Request,
    content_url: str,
    dpi: Optional[int] = Query(None, ge=10, le=600),
):
    """
    Get Bearer token from request
    """
    user = retrieve_user(request)
    authorization = f"Bearer {user.access_token}"

    return {"authorization": authorization, "content_url": content_url, "dpi": dpi}
