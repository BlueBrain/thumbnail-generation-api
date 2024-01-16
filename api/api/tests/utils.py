from fastapi import Depends
from fastapi.security import HTTPBearer


def get_current_user(token: str = Depends(HTTPBearer())):
    # Your actual authentication logic here, e.g., validating the token
    # This function should return the current user if authentication is successful
    # Otherwise, raise an HTTPException with the appropriate status code and message
    # For testing, you can mock the behavior or provide a test user
    pass


def mock_authentication(token: str = Depends(HTTPBearer())):
    # Mocking the authentication logic
    # For testing, you can return a test user or raise an HTTPException
    # to simulate authentication failure
    return {"username": "testuser", "id": 123}
