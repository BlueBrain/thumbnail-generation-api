"""
Module: util.py

This module provides utility functions.
"""

import io
from typing import Union
from typing import Optional
from urllib.parse import urlparse
from fastapi import Query
import matplotlib.pyplot as plt
import requests
from starlette.requests import Request
from api.dependencies import retrieve_user
from api.exceptions import (
    InvalidUrlParameterException,
    ResourceNotFoundException,
)


def get_file_content(authorization: str = "", content_url: str = "") -> bytes:
    """
    Gets the File content of a Nexus distribution (by requesting the resource from its content_url).

    Parameters:
        - authorization (str): Authorization header containing the access token.
        - content_url (str): URL of the distribution.

    Returns:
        str: File content as a string.

    Raises:
        str: Error message if the request to the content_url fails.
    """
    parsed_content_url = urlparse(content_url)

    if not all([parsed_content_url.scheme, parsed_content_url.netloc, parsed_content_url.path]):
        raise InvalidUrlParameterException

    response = requests.get(content_url, headers={"authorization": authorization}, timeout=15)

    if response.status_code == 200:
        return response.content
    if response.status_code == 404:
        raise ResourceNotFoundException
    raise requests.exceptions.RequestException


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


def get_buffer(fig: plt.FigureBase, dpi: Union[int, None]) -> io.BytesIO:
    """Creates a file buffer from a FigureBase object."""
    buffer = io.BytesIO()

    fig.savefig(buffer, dpi=dpi, format="png")

    buffer.seek(0)

    return buffer
