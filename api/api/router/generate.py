"""
Module: generate.py

This module defines a FastAPI router for handling requests related to morphology images.
It includes an endpoint to get a preview image of a morphology.
"""

from typing import Optional
from fastapi import APIRouter, Depends, Query, Response
from fastapi.security import HTTPBearer
from starlette.requests import Request
from api.trace_img import read_trace_img
from api.morpho_img import read_image
from api.util import get_auth, wrap_exceptions

router = APIRouter()
require_bearer = HTTPBearer()


@router.get(
    "/morphology-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
    tags=["Morphology Image"],
)
def get_morphology_image(
    request: Request,
    content_url: str,
    dpi: Optional[int] = Query(None, ge=10, le=600),
) -> Response:
    """
    Endpoint to get a preview image of a morphology.
    Sample Content URL:
    https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118
    """
    authorization = get_auth(request)
    image = wrap_exceptions(lambda: read_image(authorization, content_url, dpi=dpi))

    return Response(image, media_type="image/png")


@router.get(
    "/trace-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
    tags=["Trace Image"],
)
def get_trace_image(
    request: Request,
    content_url: str,
    dpi: Optional[int] = Query(None, ge=10, le=600),
) -> Response:
    """
    Endpoint to get a preview image of an electrophysiology trace
    Sample Content URL:
    https://bbp.epfl.ch/nexus/v1/files/public/hippocampus/https%3A%2F%2Fbbp.epfl.ch%2Fneurosciencegraph%2Fdata%2Fb67a2aa6-d132-409b-8de5-49bb306bb251
    """
    authorization = get_auth(request)
    image = wrap_exceptions(lambda: read_trace_img(authorization, content_url, dpi=dpi))

    return Response(image, media_type="image/png")
