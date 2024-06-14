"""
Module: generate.py

This module defines a FastAPI router for handling requests related to morphology images.
It includes an endpoint to get a preview image of a morphology.
"""

from fastapi import APIRouter, Depends, Response
from fastapi.security import HTTPBearer
from api.services.trace_img import generate_electrophysiology_image
from api.services.morpho_img import generate_morphology_image
from api.dependencies import retrieve_user
from api.models.common import ImageGenerationInput
from api.user import User


router = APIRouter()
require_bearer = HTTPBearer()


@router.get(
    "/morphology-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
)
def get_morphology_image(
    image_input: ImageGenerationInput = Depends(), user: User = Depends(retrieve_user)
) -> Response:
    """
    Endpoint to get a preview image of a morphology.
    Sample Content URL:
    https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118
    """
    image = generate_morphology_image(
        access_token=user.access_token, content_url=image_input.content_url, dpi=image_input.dpi
    )

    return Response(image, media_type="image/png")


@router.get(
    "/trace-image",
    dependencies=[Depends(require_bearer)],
    response_model=None,
)
def get_trace_image(image_input: ImageGenerationInput = Depends(), user: User = Depends(retrieve_user)) -> Response:
    """
    Endpoint to get a preview image of an electrophysiology trace
    Sample Content URL:
    https://bbp.epfl.ch/nexus/v1/files/public/hippocampus/https%3A%2F%2Fbbp.epfl.ch%2Fneurosciencegraph%2Fdata%2Fb67a2aa6-d132-409b-8de5-49bb306bb251
    """
    image = generate_electrophysiology_image(
        access_token=user.access_token, content_url=image_input.content_url, dpi=image_input.dpi
    )

    return Response(image, media_type="image/png")
