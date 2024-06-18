"""
Unit test module related to the router of /generate
"""

from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
import pytest
from api.main import app
from api.dependencies import retrieve_user
from tests.fixtures.utils import load_content, load_nwb_content
from api.user import User


def override_retrieve_user():
    """
    Overrides the retrieve_user() function
    """
    return User(access_token="test-access-token", username="test")


@pytest.fixture
def mock_headers():
    """
    Mock headers fixture for dummy requests
    """
    return {"Authorization": "Bearer fake-super-secret-token"}


class TestMorphologyThumbnailGenerationRouter:
    """
    Unit test class for testing the router of morphology thumbnail generation
    """

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)
        app.dependency_overrides[retrieve_user] = override_retrieve_user

    @patch(
        "api.services.morpho_img.fetch_file_content", return_value=load_content("./tests/fixtures/data/morphology.swc")
    )
    def test_morphology_thumbnail_generation_returns_200_and_image(self, fetch_file_content, mock_headers):
        """
        Tests whether the router returns a 200 and an image if the request is correct
        """
        response = self.client.get(
            "/generate/morphology-image",
            headers=mock_headers,
            params={"content_url": "http://example.com/image", "dpi": 300},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    @patch("requests.get")
    def test_morphology_thumbnail_generation_returns_404_if_resource_not_exists(self, mock_get, mock_headers):
        """
        Tests whether the router returns a 404 and correct error message if resource does not exist
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response
        response = self.client.get(
            "/generate/morphology-image",
            headers=mock_headers,
            params={"content_url": "http://example.com/image", "dpi": 300},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "The resource is not found"

    @patch("requests.get")
    def test_morphology_thumbnail_generation_returns_422_if_content_url_is_wrong(self, mock_get, mock_headers):
        """
        Tests whether the router returns a 422 and correct error message if content url is wrong
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response
        response = self.client.get(
            "/generate/morphology-image",
            headers=mock_headers,
            params={"content_url": "notAurl/image", "dpi": 300},
        )
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid content_url parameter in request"


class TestElectrophusiologyThumbnailGenerationRouter:
    """
    Unit test class for testing the router of morphology thumbnail generation
    """

    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)
        app.dependency_overrides[retrieve_user] = override_retrieve_user

    @patch(
        "api.services.trace_img.fetch_file_content",
        return_value=load_nwb_content("./tests/fixtures/data/correct_trace.nwb"),
    )
    def test_electrophysiology_thumbnail_generation_returns_200_and_image(self, fetch_file_content, mock_headers):
        """
        Tests whether the router returns a 200 and an image if the request is correct
        """
        response = self.client.get(
            "/generate/trace-image",
            headers=mock_headers,
            params={"content_url": "http://example.com/image", "dpi": 300},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    @patch("requests.get")
    def test_electrophysiology_thumbnail_generation_returns_404_if_resource_not_exists(self, mock_get, mock_headers):
        """
        Tests whether the router returns a 404 and correct error message if resource does not exist
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response
        response = self.client.get(
            "/generate/trace-image",
            headers=mock_headers,
            params={"content_url": "http://example.com/image", "dpi": 300},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "The resource is not found"

    @patch("requests.get")
    def test_electrophysiology_thumbnail_generation_returns_422_if_content_url_is_wrong(self, mock_get, mock_headers):
        """
        Tests whether the router returns a 422 and correct error message if content url is wrong
        """
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response
        response = self.client.get(
            "/generate/trace-image",
            headers=mock_headers,
            params={"content_url": "notAurl/image", "dpi": 300},
        )
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid content_url parameter in request"
