"""
Unit test module for testing electrophysiology services
"""

from io import BytesIO
from PIL import Image
from unittest.mock import patch
from api.services.trace_img import generate_electrophysiology_image
from tests.fixtures.utils import load_nwb_content
from tests.fixtures.nexus import trace_content_url, access_token


@patch(
    "api.services.trace_img.fetch_file_content",
    return_value=load_nwb_content("./tests/fixtures/data/correct_trace.nwb"),
)
def test_generate_electrophysiology_image_returns_correct_image(fetch_file_content, trace_content_url, access_token):
    """
    Tests whether the generate electrophysiology image() function returns correct image
    """

    response = generate_electrophysiology_image(access_token, trace_content_url)
    assert isinstance(response, bytes)
    image = Image.open(BytesIO(response))
    dpi = image.info.get("dpi")
    assert round(dpi[0]) == 72
