"""
Module: dependencies.py

This module provides functions related to user authentication using JWT tokens and 
handling user sessions.
"""

import time
import jwt
from starlette.requests import Request
from api.user import User
from api.exceptions import ExpiredAccessToken, InvalidAccessToken


def token_has_expired(decoded: dict) -> bool:
    """
    Checks whether the JWT token has expired or not

    Parameters:
        - decoded (dict): The decoded jwt token

    Returns:
        bool: whether the token has expired or not
    """
    # Get the expiration time from the token
    exp_time = decoded.get("exp")
    if exp_time is None:
        raise InvalidAccessToken
    return time.time() > exp_time


def retrieve_user(request: Request) -> User:
    """
    Retrieves user from BBP auth endpoint. If token is invalid, throws 401 error

    :param request: FastAPI Request object.
    :return: User object containing username and access token.
    :raises HTTPException: Thrown with a 401 status code if the access token is invalid or has expired.
    """
    access_token = request.headers.get("authorization").replace("Bearer ", "")
    try:
        decoded = jwt.decode(access_token, options={"verify_signature": False})
        if token_has_expired(decoded):
            raise ExpiredAccessToken
        return User(username=decoded.get("preferred_username"), access_token=access_token)
    except jwt.InvalidTokenError as inv_token_error:
        raise InvalidAccessToken from inv_token_error
