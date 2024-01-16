"""
This module contains unit tests for the behavior of the FastAPI application related to CORS.
"""

import os
import unittest.mock
from fastapi.testclient import TestClient
from api.main import app
from api.tests.utils import get_current_user, mock_authentication

client = TestClient(app)

app.dependency_overrides[get_current_user] = mock_authentication


def test_allowed_origin():
    """
    Test the behavior of the app when making requests from allowed origins.

    This test uses unittest.mock.patch.dict to temporarily set the WHITELISTED_CORS_URLS
    environment variable and iterates over the ALLOWED_ORIGINS, making requests to
    "/generate/morphology-image" with different origins. It checks that the response
    status code is 422 and the "access-control-allow-origin" header is set correctly.

    Note: The test uses "mock_token" as the authorization token in the request headers.
    """
    with unittest.mock.patch.dict("os.environ", {"WHITELISTED_CORS_URLS": "http://localhost:3000"}):
        for origin in os.environ.get("ALLOWED_ORIGINS", "").split(","):
            response = client.get(
                "/generate/morphology-image", headers={"Origin": origin, "Authorization": "Bearer mock_token"}
            )
            assert response.status_code == 422
            assert response.headers["access-control-allow-origin"] == origin


def test_not_allowed_origin():
    """
    Test the behavior of the app when making requests from not allowed origins.

    This test makes a request to "/generate/morphology-image" with an origin that is not
    allowed in the CORS configuration. It checks that the response status code is 403.
    """
    response = client.get("/generate/morphology-image", headers={"Origin": "http://not-allowed-origin.com"})
    assert response.status_code == 403
