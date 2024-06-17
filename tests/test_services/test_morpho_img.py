"""
Unit test module for testing morphologies
"""

import pytest
from unittest.mock import patch
from api.services.morpho_img import generate_morphology_image
from tests.fixtures.utils import load_content
from api.services.nexus import fetch_file_content


@pytest.fixture
def morphology_content_url() -> str:
    return (
        "https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118",
    )


@pytest.fixture
def access_token() -> str:
    return ""


@patch("api.services.morpho_img.fetch_file_content", return_value=load_content("./tests/fixtures/data/morphology.swc"))
def test_generate_morphology_image_returns_correct_image(fetch_file_content, morphology_content_url, access_token):
    """
    Tests whether the generate morphology image() function returns correct image
    """

    response = generate_morphology_image(access_token, morphology_content_url)
    assert isinstance(response, bytes)
