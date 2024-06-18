from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from api.main import app
from api.dependencies import retrieve_user
from tests.fixtures.utils import load_content
from api.user import User


class TestMorphologyImage:
    @classmethod
    def setup_class(cls):
        cls.client = TestClient(app)
        app.dependency_overrides[retrieve_user] = cls.override_retrieve_user

    @staticmethod
    def override_retrieve_user():
        return User(access_token="test-access-token", username="test")

    @patch(
        "api.services.morpho_img.fetch_file_content", return_value=load_content("./tests/fixtures/data/morphology.swc")
    )
    def test_morphology_thumbnail_generation_returns_200_and_image(self, fetch_file_content):
        headers = {"Authorization": "Bearer fake-super-secret-token"}
        response = self.client.get(
            "/generate/morphology-image",
            headers=headers,
            params={"content_url": "http://example.com/image", "dpi": 300},
        )
        assert response.status_code == 200
        assert response.headers["content-type"] == "image/png"

    @patch("requests.get")
    def test_morphology_thumbnail_generation_returns_404_if_resource_not_exists(self, mock_get):
        headers = {"Authorization": "Bearer fake-super-secret-token"}
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response
        response = self.client.get(
            "/generate/morphology-image",
            headers=headers,
            params={"content_url": "http://example.com/image", "dpi": 300},
        )
        assert response.status_code == 404
        assert response.json()["detail"] == "The resource is not found"

    @patch("requests.get")
    def test_morphology_thumbnail_generation_returns_422_if_content_url_is_wrong(self, mock_get):
        headers = {"Authorization": "Bearer fake-super-secret-token"}
        mock_response = Mock()
        mock_response.status_code = 404
        mock_response.json.return_value = None
        mock_get.return_value = mock_response
        response = self.client.get(
            "/generate/morphology-image",
            headers=headers,
            params={"content_url": "notAurl/image", "dpi": 300},
        )
        assert response.status_code == 422
        assert response.json()["detail"] == "Invalid content_url parameter in request"
