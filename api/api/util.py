"""
Module: util.py

This module provides utility functions.
"""

import io
from typing import Union
from typing import Callable, Optional
from urllib.parse import urlparse

from fastapi import HTTPException, Query
import matplotlib.pyplot as plt
import requests
from starlette.requests import Request

from api.dependencies import retrieve_user
from api.exceptions import (
    InvalidUrlParameterException,
    NoCellFound,
    NoConversionFound,
    NoIcDataFound,
    NoProtocolFound,
    NoRateFound,
    NoRepetitionFound,
    NoSweepFound,
    NoUnitFound,
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


def wrap_exceptions(callback: Callable):
    """
    Decorator function for handling exceptions in /generate requests
    """

    def wrap(*args, **kwargs):
        try:
            return callback(*args, **kwargs)
        except InvalidUrlParameterException as exc:
            raise HTTPException(
                status_code=422,
                detail="Invalid content_url parameter in request.",
            ) from exc
        except ResourceNotFoundException as exc:
            raise HTTPException(
                status_code=404,
                detail="There was no distribution for that content url.",
            ) from exc
        except NoCellFound as exc:
            # https://stackoverflow.com/questions/5604816/whats-the-most-appropriate-http-status-code-for-an-item-not-found-error-page
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain a 'cell'.",
            ) from exc
        except NoRepetitionFound as exc:
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain a 'repetition'.",
            ) from exc
        except NoSweepFound as exc:
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain a 'sweep'.",
            ) from exc
        except NoProtocolFound as exc:
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain a 'protocol'.",
            ) from exc
        except NoIcDataFound as exc:
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain any Ic data.",
            ) from exc
        except NoUnitFound as exc:
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain a 'unit'.",
            ) from exc
        except NoRateFound as exc:
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain a 'rate'.",
            ) from exc
        except NoConversionFound as exc:
            raise HTTPException(
                status_code=404,
                detail="There the NWB file didn't contain a 'conversion'.",
            ) from exc
        except Exception as exc:
            raise HTTPException(
                status_code=400,
                detail="Something went wrong.",
            ) from exc

    return wrap


def get_buffer(fig: plt.FigureBase, dpi: Union[int, None]) -> io.BytesIO:
    """Creates a file buffer from a FigureBase object."""
    buffer = io.BytesIO()

    fig.savefig(buffer, dpi=dpi, format="png")

    buffer.seek(0)

    return buffer
