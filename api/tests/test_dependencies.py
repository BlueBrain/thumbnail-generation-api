"""
Testing the dependencies module
"""

import jwt
import pytest
from fastapi import HTTPException
from api.dependencies import retrieve_user
from api.user import User


class TestRetrieveUser:
    """
    Test class for the retrieve_user function in the dependencies module.

    This class contains test cases for the retrieve_user function, covering scenarios with both
    valid and invalid tokens.

    Attributes:
    - None

    Methods:
    - test_valid_token: Tests the retrieve_user function with a valid token.
    - test_invalid_token: Tests the retrieve_user function with an invalid token.

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
        monkeypatch.setattr(jwt, "decode", lambda token, options: {"preferred_username": "user123"})

        request = MockRequest(headers={"authorization": f"Bearer {valid_token}"})
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

        request = MockRequest(headers={"authorization": f"Bearer {invalid_token}"})
        with pytest.raises(HTTPException) as exc_info:
            retrieve_user(request)

        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Access token is invalid"


# Mock Request object for testing
class MockRequest:
    """
    Mock class for simulating a Request object in FastAPI.
    """

    def __init__(self, headers):
        self.headers = headers
