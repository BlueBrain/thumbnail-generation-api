from pathlib import Path
from fastapi.testclient import TestClient
from api.main import app
from http import HTTPStatus

client = TestClient(app)


class TestProcessSwc:
    """
    This class defines a set of unit tests for the `/soma/process-swc` endpoint.

    The endpoint is expected to take an SWC file as input and process it. These tests
    verify the behavior of the endpoint under various cases, including:

    * No authorization header provided
    * Invalid authorization header provided
    * Empty file upload
    * Malformed SWC file upload
    * Valid SWC file upload with expected output
    """

    UNAUTHORIZED_HEADERS = {"authorization": "Bearer NOTAUTHORIZED"}
    AUTHORIZED_HEADERS = {"authorization": "Bearer AUTHORIZED"}
    TEST_FILE = Path(__file__).parent.parent / "files" / "test.swc"
    EXPECTED_OUTPUT_FILE = Path(__file__).parent.parent / "files" / "test_output.glb"

    @staticmethod
    def test_process_swc_no_headers():
        """
        Tests that the endpoint returns a 401 (Unauthorized) when no authorization header is provided.
        """
        res = client.post("/soma/process-swc")

        assert res.status_code == HTTPStatus.UNAUTHORIZED

    def test_not_authorized_bearer(self):
        """
        Tests that the endpoint returns a 401 (Unauthorized) in cases where an invalid authorization header is provided.
        """
        res = client.post(
            "/soma/process-swc",
            files=[],
            headers=self.UNAUTHORIZED_HEADERS,
        )

        assert res.status_code == HTTPStatus.UNAUTHORIZED

    def test_empty_file(self):
        """
        Tests that the endpoint returns a 422 (Unprocessable Entity) when an empty file is uploaded.
        """
        res = client.post(
            "/soma/process-swc", files={}, headers=self.AUTHORIZED_HEADERS
        )

        assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_malformed_file(self):
        """
        Tests that the endpoint returns a 422 (Unprocessable Entity) for cases when a malformed file is uploaded.
        """
        file = Path(__file__).parent.parent / "files" / "malformed.swc"

        assert file.exists()

        with open(file, "rb") as upload_file:
            res = client.post(
                "/soma/process-swc",
                headers=self.AUTHORIZED_HEADERS,
                files={"file": upload_file},
            )
        print(res.content)
        assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_working_file(self):
        """
        Tests the success case for authorized and valid file returns a 200 (OK).
        """
        file = Path(__file__).parent.parent / "files" / "test.swc"

        assert file.exists()

        with open(file, "rb") as upload_file:
            res = client.post(
                "/soma/process-swc",
                headers=self.AUTHORIZED_HEADERS,
                files={"file": upload_file},
            )

        assert res.status_code == HTTPStatus.OK

    def test_working_file_is_correct(self):
        """
        Tests the success case for authorized and valid file returns a file which is as expected for its input file.
        it compares the byte content of an expected output file, for the response of the test input file.
        """
        with open(self.TEST_FILE, "rb") as upload_file:
            res = client.post(
                "/soma/process-swc",
                headers=self.AUTHORIZED_HEADERS,
                files={"file": upload_file},
            )

            response_payload = res.read()

            with open(self.EXPECTED_OUTPUT_FILE, "rb") as expected:
                expected_data = expected.read()
                assert response_payload == expected_data

        assert res.status_code == HTTPStatus.OK


class TestProcessNexusSwc:
    """
    This class defines a set of unit tests for the `/soma/process-nexus-swc` endpoint.

    The endpoint is expected to take a URL pointing to a SWC file hosted on a Nexus server and process it.
    These tests verify the behavior of the endpoint under various conditions, including:

    - No authorization header provided
    - Invalid authorization header provided
    - Empty request body
    - Malformed content URL in request body
    - Valid URL but content not a SWC file
    - Valid content URL pointing to a SWC file
    """

    UNAUTHORIZED_HEADERS = {"authorization": "Bearer NOTAUTHORIZED"}
    AUTHORIZED_HEADERS = {"authorization": "Bearer AUTHORIZED"}

    @staticmethod
    def test_no_headers():
        """
        Tests that the endpoint returns a 401 (Unauthorized) when no authorization header is provided.
        """
        res = client.post("/soma/process-nexus-swc")

        assert res.status_code == HTTPStatus.UNAUTHORIZED

    def test_unauthorized_bearer(self):
        """
        Tests that the endpoint returns a 401 (Unauthorized) in cases where an invalid authorization header is provided.
        """
        res = client.post("/soma/process-nexus-swc", headers=self.UNAUTHORIZED_HEADERS)

        assert res.status_code == HTTPStatus.UNAUTHORIZED

    def test_empty_body(self):
        """
        Tests that the endpoint returns a 422 (Unprocessable Entity) when no body is posted.
        """
        res = client.post("/soma/process-nexus-swc", headers=self.AUTHORIZED_HEADERS)

        assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_malformed_content_url(self):
        """
        Tests that the endpoint returns a 422 (Unprocessable Entity) for cases when a malformed file is uploaded.
        """
        payload = {"content_url": "this_is_not//:www.an.url"}
        res = client.post(
            "/soma/process-nexus-swc", headers=self.AUTHORIZED_HEADERS, json=payload
        )

        assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_valid_but_wrong_url(self):
        """
        Tests that the endpoint returns a 422 (Unprocessable Entity) for cases when a valid but wrong url uploaded.
        """
        payload = {"content_url": "www.rust-lang.org"}
        res = client.post(
            "/soma/process-nexus-swc", headers=self.AUTHORIZED_HEADERS, json=payload
        )

        assert res.status_code == HTTPStatus.UNPROCESSABLE_ENTITY

    def test_valied_content_url(self):
        """
        Tests that the endpoint returns a 200 (OK) for cases when a valid url is posted.
        """
        payload = {
            "content_url": "https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118"
        }
        res = client.post(
            "/soma/process-nexus-swc", headers=self.AUTHORIZED_HEADERS, json=payload
        )

        assert res.status_code == HTTPStatus.OK
