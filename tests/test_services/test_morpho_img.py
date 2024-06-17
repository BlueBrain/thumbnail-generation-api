"""
Unit test module for testing morphologies
"""

from io import BytesIO
from PIL import Image
from unittest.mock import patch
from api.services.morpho_img import generate_morphology_image
from tests.fixtures.utils import load_content
from tests.fixtures.nexus import morphology_content_url, access_token


@patch("api.services.morpho_img.fetch_file_content", return_value=load_content("./tests/fixtures/data/morphology.swc"))
def test_generate_morphology_image_returns_correct_image(fetch_file_content, morphology_content_url, access_token):
    """
    Tests whether the generate morphology image() function returns correct image
    """

    response = generate_morphology_image(access_token, morphology_content_url)
    assert isinstance(response, bytes)
    image = Image.open(BytesIO(response))
    dpi = image.info.get("dpi")
    assert round(dpi[0]) == 72


@patch("api.services.morpho_img.fetch_file_content", return_value=load_content("./tests/fixtures/data/morphology.swc"))
def test_generate_morphology_image_returns_correct_dpi(fetch_file_content, morphology_content_url, access_token):
    """
    Tests whether the generate morphology image() function returns correct image
    """

    response = generate_morphology_image(access_token, morphology_content_url, dpi=300)
    assert isinstance(response, bytes)
    image = Image.open(BytesIO(response))
    dpi = image.info.get("dpi")
    assert round(dpi[0]) == 300
