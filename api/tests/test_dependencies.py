"""
Testing the dependencies module
"""

from pathlib import Path
import subprocess
import jwt
import pytest
from fastapi import HTTPException
from starlette.requests import Request
from api.dependencies import retrieve_user
from api.user import User


class TestRetrieveUser:
    """
    Test class for the retrieve_user function in the dependencies module.

    Uses the starlette Request with custom parameters to simulate the request input to the retrieve_user function

        request = Request(scope={
            "type": "http",
            "headers": [
                ("authorization".encode(), f"Bearer {valid_token}".encode())
            ]
        })

    NOTE: headers must be in bytes, therefore strings must be encoded to bytes

    Methods:
        - test_valid_token: Simulates a request with a valid token and validates the returned User object.
        - test_invalid_token: Simulates a request with an invalid token and checks for a raised HTTPException with a 401 status code.
        - test_no_token: Simulates a request with an empty authorization header and checks for a raised HTTPException with a 401 status code.
        - test_no_authorization_header: Simulates a request without an authorization header and checks for a raised HTTPException with a 401 status code.

    Dependencies:
    - This class relies on the retrieve_user function from the dependencies module.
    - It uses the MockRequest class for creating mock Request objects for testing.
    """

    @staticmethod
    def test_valid_token(monkeypatch):
        """
        Tests the retrieve_user function with a valid token.

        This test case mocks a valid token using monkeypatch and ensures that the retrieve_user
        function returns the expected User object with correct attributes.
        """
        valid_token = "valid_token"
        monkeypatch.setattr(
            jwt, "decode", lambda token, options: {"preferred_username": "user123"}
        )

        request = Request(
            scope={
                "type": "http",
                "headers": [
                    ("authorization".encode(), f"Bearer {valid_token}".encode())
                ],
            }
        )

        user = retrieve_user(request)

        assert isinstance(user, User)
        assert user.username == "user123"
        assert user.access_token == valid_token

    @staticmethod
    def test_invalid_token():
        """
        Tests the retrieve_user function with an invalid token.

        This test case mocks an invalid token using monkeypatch and ensures that the retrieve_user
        function raises an HTTPException with a 401 status code and the correct detail message.
        """
        invalid_token = "invalid_token"

        request = Request(
            scope={
                "type": "http",
                "headers": [
                    ("authorization".encode(), f"Bearer {invalid_token}".encode())
                ],
            }
        )

        with pytest.raises(HTTPException) as exc_info:
            retrieve_user(request)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Access token is invalid"

    @staticmethod
    def test_no_token():
        """
        Tests HTTPException raised for missing access token in Authorization header.

        This test creates a request object with an empty Authorization header.
        It verifies that the `retrieve_user` function raises an HTTPException with a 401
        status code and an error message indicating that a valid access token is missing.
        """

        request = Request(
            scope={"type": "http", "headers": [("authorization".encode(), "".encode())]}
        )

        with pytest.raises(HTTPException) as exc_info:
            retrieve_user(request)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Access token is invalid"

    @staticmethod
    def test_no_authorization_header():
        """
        Tests HTTPException raised for missing Authorization header.

        This test creates a request object that completely lacks an Authorization header.
        It asserts that the `retrieve_user` function raises an HTTPException with a 401
        status code, signifying the absence of required authorization credentials.
        """

        request = Request(
            scope={"type": "http", "headers": [("anyheader".encode(), "".encode())]}
        )

        with pytest.raises(HTTPException) as exc_info:
            retrieve_user(request)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Access token is invalid"


class TestBlender:
    """
    Integration Tests for blender.

    Methods:
    - test_blender_exists: Verifies that the Blender executable exists was built at the expected path.
    - test_blender_version: Tests Blender executable is callable and returns the exepected blender version.
    """

    BLENDER_VERSION = b"Blender 3.5.0"
    BLENDER_PATH = (
        Path().resolve() / "blender" / "bbp-blender-3.5" / "blender-bbp" / "blender"
    )

    def test_blender_exists(self):
        """
        Verifies that the Blender executable exists at the expected path.
        """

        assert self.BLENDER_PATH.exists()

    def test_blender_version(self):
        """
        Checks if the Blender executable runs and has the expected version (3.5.0)
        """

        command = [self.BLENDER_PATH.as_posix(), "--version"]

        result = subprocess.run(command, check=True, capture_output=True)

        first_line = result.stdout.splitlines()[0]

        assert first_line == self.BLENDER_VERSION


class TestNMV:
    """
    Integration Tests related to the NeuromorphoVis (NMV) tool.

    Tests that NMV script is callable and runs succesfully with a test swc file
        Success is measured by:
            - Blender stdout printing GTLF file was exported
            - NMV script prints "NMV Done" to stdout
            - GTLF file is found in output directory
            - GLTF file is the same as an expected output.glb

    Methods:
    - test_nmv_soma_path_exists: Verifies that the Soma python file exists and was built at the expected path.
    - test_neuromorphovis_path_exists: Verifies that the neuromorphovis.py python file exists and was built at the expected path.
    - test_nmv_call_with_empty_path: Tests that NMV script is callable and is expected to fail with a specific message when called with an empty file
    - test_nmv_call_with_working_file: Tests that NMV script is callable and runs succesfully with a test swc file and stdout output is as exepected
    - test_nmv_call_produces_correct_output: Tests that NMV script is callable and runs succesfully with a test swc file and fileoutput is present and as expected
    """

    NEUROMORPHOVIS_PATH = Path().resolve() / "neuromorphovis.py"

    SOMA_PATH = (
        Path().resolve() / "nmv" / "interface" / "cli" / "soma_reconstruction.py"
    )
    BLENDER_EXECUTABLE_PATH = (
        Path().resolve() / "blender" / "bbp-blender-3.5" / "blender-bbp" / "blender"
    )

    SWC_TEST_FILE = Path(__file__).parent / "files" / "test.swc"

    EXPECTED_OUTPUT_FILE = Path(__file__).parent / "files" / "test_output.glb"

    def test_nmv_soma_path_exists(self):
        """
        Tests that the soma_reconstruction.py script exists.
        """
        assert self.SOMA_PATH.exists(), "soma_reconstruction.py not found."

    def test_neuromorphovis_path_exists(self):
        """
        Tests that the neuromorphovis.py script exists.
        """
        assert self.NEUROMORPHOVIS_PATH.exists(), "neuromorphovis.py not found."

    def test_nmv_call_with_empty_path(self, tmp_path, tmpdir):
        """
        Tests that NMV script is callable and is expected to fail with a specific message when called with an empty file
        This proves the callable script is integrated, is callable and handles minimal logic.
        """
        filepath = tmp_path / "file"

        command = [
            "python",
            self.NEUROMORPHOVIS_PATH.as_posix(),
            f"--blender={self.BLENDER_EXECUTABLE_PATH.as_posix()}",
            "--input=file",
            f"--morphology-file={filepath.as_posix()}",
            "--export-soma-mesh-blend",
            "--export-soma-mesh-obj",
            f"--output-directory={tmpdir}",
        ]

        result = subprocess.run(command, capture_output=True)

        assert b"Cannot load the morphology file" in result.stdout

    def test_nmv_call_with_working_file(self, tmpdir):
        """
        Tests that NMV script is callable and runs succesfully with a test swc file
            Success is measured by:
                - Blender stdout printing GTLF file was exported
                - NMV script prints "NMV Done" to stdout
        """

        command = [
            "python",
            self.NEUROMORPHOVIS_PATH.as_posix(),
            f"--blender={self.BLENDER_EXECUTABLE_PATH.as_posix()}",
            "--input=file",
            f"--morphology-file={self.SWC_TEST_FILE.as_posix()}",
            "--export-soma-mesh-blend",
            "--export-soma-mesh-obj",
            f"--output-directory={tmpdir}",
        ]

        result = subprocess.run(command, capture_output=True)

        result_lines = result.stdout.splitlines()

        blender_export_stdout = False
        nmv_done = False

        for line in result_lines:
            if b"NMV Done" in line:
                nmv_done = True
                continue
            if b"INFO: Finished glTF 2.0 export" in line:
                blender_export_stdout = True

        assert nmv_done
        assert blender_export_stdout

    def test_nmv_call_produces_correct_output(self, tmpdir):
        """
        Tests that NMV script is callable and runs succesfully with a test swc file
            Success is measured by:
            - GTLF file is found in output directory
            - GLTF file is the same as an expected output.glb

        compares output file with a precomputed test_output.glb
        """

        command = [
            "python",
            self.NEUROMORPHOVIS_PATH.as_posix(),
            f"--blender={self.BLENDER_EXECUTABLE_PATH.as_posix()}",
            "--input=file",
            f"--morphology-file={self.SWC_TEST_FILE.as_posix()}",
            "--export-soma-mesh-blend",
            "--export-soma-mesh-obj",
            f"--output-directory={tmpdir}",
        ]

        _ = subprocess.run(command)

        mesh_output_dir = Path(tmpdir) / "meshes"

        export_found = False
        export_as_expected = False

        for file in mesh_output_dir.iterdir():
            print(file)
            if file.suffix == ".glb":
                export_found = True

                with open(file, "rb") as output, open(
                    self.EXPECTED_OUTPUT_FILE, "rb"
                ) as expected:
                    output_data = output.read()
                    output_expected = expected.read()

                    if output_data == output_expected:
                        export_as_expected = True

        assert export_found
        assert export_as_expected
