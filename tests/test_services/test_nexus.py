"""
Testing Nexus-related services
"""

import pytest
from unittest.mock import Mock, patch
from api.services.nexus import fetch_file_content
from api.exceptions import ResourceNotFoundException
from tests.fixtures.utils import load_content
from tests.fixtures.nexus import morphology_content_url, access_token


@patch("requests.get")
def test_fetch_file_content_returns_data_if_request_is_200(mock_get, morphology_content_url, access_token):
    """
    Tests whether the content is correctly returned if the request is 200
    """
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = load_content("./tests/fixtures/data/morphology.swc", encoded=False)
    mock_get.return_value = mock_response

    fetch_file_content(access_token, morphology_content_url)


@patch("requests.get")
def test_fetch_file_content_raises_exception_if_content_url_does_not_exist(
    mock_get, morphology_content_url, access_token
):
    """
    Tests whether the content is correctly returned if the content does not exist
    """
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = None
    mock_get.return_value = mock_response
    with pytest.raises(ResourceNotFoundException):
        fetch_file_content(access_token, morphology_content_url)
