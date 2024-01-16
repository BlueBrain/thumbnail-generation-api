import os
import unittest.mock
from fastapi import Depends
from fastapi.security import HTTPBearer
from fastapi.testclient import TestClient
from api.main import app
from api.tests.utils import get_current_user, mock_authentication

client = TestClient(app)

# Replace the actual dependency with the mocked one in your test
app.dependency_overrides[get_current_user] = mock_authentication


def test_allowed_origin():
    with unittest.mock.patch.dict("os.environ", {"WHITELISTED_CORS_URLS": "http://localhost:3000"}):
        for origin in os.environ.get("ALLOWED_ORIGINS", "").split(","):
            response = client.get(
                "/generate/morphology-image", headers={"Origin": origin, "Authorization": "Bearer mock_token"}
            )
            assert response.status_code == 422
            assert response.headers["access-control-allow-origin"] == origin


def test_not_allowed_origin():
    response = client.get("/generate/morphology-image", headers={"Origin": "http://not-allowed-origin.com"})
    assert response.status_code == 403
