from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


class TestMorphologyImage:
    @staticmethod
    def test_no_auth():
        response = client.get("/generate/morphology-image")
        assert response.status_code == 403

    @staticmethod
    def test_missing_headers():
        response = client.get(
            "/generate/morphology-image", headers={"authorization": "Bearer test"}
        )

        assert response.status_code == 403

    @staticmethod
    def test_complete_headers():

        headers = {
            "authorization": "Bearer test",
            "content_url": "https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118",
            "dpi": "100"
        }

        ...


class TestTraceImage:
    @staticmethod
    def test_no_auth():
        response = client.get("/generate/trace-image")
        assert response.status_code == 403

    @staticmethod
    def test_missing_headers():
        response = client.get(
            "/generate/trace-image", headers={"authorization": "Bearer test"}
        )

        assert response.status_code == 403

    @staticmethod
    def test_success():

        ...
