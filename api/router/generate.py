"""
Module: generate.py

This module defines a FastAPI router for handling requests related to morphology images.
It includes an endpoint to get a preview image of a morphology.
"""

from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer
from api.util import common_params
from api.utils.morpho_img import read_image
from api.utils.trace_img import read_trace_img

router = APIRouter()
require_bearer = HTTPBearer()


@router.get(
    "/morphology-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
)
def get_morphology_image(commons: dict = Depends(common_params)) -> Response:
    """
    Endpoint to get a preview image of a morphology.
    Sample Content URL:
    https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118
    """
    image = read_image(**commons)

    return Response(image, media_type="image/png")


@router.get(
    "/trace-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
)
def get_trace_image(commons: dict = Depends(common_params)) -> Response:
    """
    Endpoint to get a preview image of an electrophysiology trace
    Sample Content URL:
    https://bbp.epfl.ch/nexus/v1/files/public/hippocampus/https%3A%2F%2Fbbp.epfl.ch%2Fneurosciencegraph%2Fdata%2Fb67a2aa6-d132-409b-8de5-49bb306bb251
    """
    image = read_trace_img(**commons)

    return Response(image, media_type="image/png")
