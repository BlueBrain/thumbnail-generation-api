"""
Module: generate.py

This module defines a FastAPI router for handling requests related to morphology images.
It includes an endpoint to get a preview image of a morphology.
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import HTTPBearer
from api.util import common_params
from api.utils.morpho_img import retrieve_and_generate_morpho_image
from api.utils.trace_img import retrieve_and_generate_ephys_img
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
    try:
        image = retrieve_and_generate_morpho_image(**commons)
        return Response(image, media_type="image/png")
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
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail="Something went wrong",
        ) from exc


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
    try:
        image = retrieve_and_generate_ephys_img(**commons)
        return Response(image, media_type="image/png")
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
