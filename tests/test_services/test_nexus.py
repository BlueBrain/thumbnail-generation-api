"""
Testing Nexus-related services
"""

import pytest
from unittest.mock import Mock, patch
from api.services.nexus import fetch_file_content
from api.exceptions import AuthenticationIssueException, AuthorizationIssueException, ResourceNotFoundException
from tests.utils import load_content


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
    Tests whether the proper error is raised if content_url does not exist
    """
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.json.return_value = None
    mock_get.return_value = mock_response
    with pytest.raises(ResourceNotFoundException):
        fetch_file_content(access_token, morphology_content_url)


@patch("requests.get")
def test_fetch_file_content_raises_exception_if_user_is_not_authenticated(
    mock_get, morphology_content_url, access_token
):
    """
    Tests whether the proper error is raised if the user is not authenticated
    """
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.json.return_value = None
    mock_get.return_value = mock_response
    with pytest.raises(AuthenticationIssueException):
        fetch_file_content(access_token, morphology_content_url)


@patch("requests.get")
def test_fetch_file_content_raises_exception_if_user_is_not_authorized_to_access_resource(
    mock_get, morphology_content_url, access_token
):
    """
    Tests whether the proper error is raised if the user is not authenticated
    """
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.json.return_value = None
    mock_get.return_value = mock_response
    with pytest.raises(AuthorizationIssueException):
        fetch_file_content(access_token, morphology_content_url)
