"""
Module: dependencies.py

This module provides functions related to user authentication using JWT tokens and 
handling user sessions.
"""
import jwt
from fastapi import HTTPException
from starlette.requests import Request
from user import User


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
        return User(username=decoded.get("preferred_username"), access_token=access_token)
    except jwt.ExpiredSignatureError as exp_signature_error:
        raise HTTPException(status_code=401, detail="Access token has expired") from exp_signature_error
    except jwt.InvalidTokenError as inv_token_error:
        raise HTTPException(status_code=401, detail="Access token is invalid") from inv_token_error
