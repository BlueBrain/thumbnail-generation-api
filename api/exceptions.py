"""
Module: exceptions.py

This module defines a custom exception classes
"""

from fastapi import HTTPException
import sentry_sdk


class SentryReportedException(HTTPException):
    """
    Defines exceptions that will be reported to sentry
    """

    def __init__(self, status_code, detail):
        sentry_sdk.capture_exception(self)
        super().__init__(status_code=status_code, detail=detail)


# Authentication


class InvalidAccessToken(HTTPException):
    """Exception raised when the provided access token is invalid."""

    def __init__(self):
        super().__init__(status_code=401, detail="Access token is invalid")


class ExpiredAccessToken(HTTPException):
    """Exception raised when the provided access token has expired"""

    def __init__(self):
        super().__init__(status_code=401, detail="The access token has expired")


class AuthenticationIssueException(HTTPException):
    """Exception raised when Nexus throws authorization error"""

    def __init__(self):
        super().__init__(status_code=401, detail="The user is not authenticated")


class AuthorizationIssueException(HTTPException):
    """Exception raised when Nexus throws authorization error"""

    def __init__(self):
        super().__init__(status_code=403, detail="The user does not have access in the content")


# Nexus


class ResourceNotFoundException(HTTPException):
    """Exception raised when a requested resource is not found.

    This exception is typically used to indicate that a resource, such as a file, database record,
    or network endpoint, is expected to exist but cannot be located.
    """

    def __init__(self):
        super().__init__(status_code=404, detail="The resource is not found")


class InvalidUrlParameterException(HTTPException):
    """Exception raised when a URL parameter is empty or invalid.

    This exception is typically used to indicate that a parameter, such as a content_url, is expected to exist,
    and be valid, but instead is either an empty string or simply not a valid URL.
    """

    def __init__(self) -> None:
        super().__init__(status_code=422, detail="Invalid content_url parameter in request")


# Electrophysiology


class NoCellFound(SentryReportedException):
    "Thrown when no cell is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain a 'cell'")


class NoRepetitionFound(SentryReportedException):
    "Thrown when no repetition is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain a 'repetition'")


class NoSweepFound(SentryReportedException):
    "Thrown when no sweep is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain a 'sweep'")


class NoProtocolFound(SentryReportedException):
    "Thrown when no protocol is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain a 'protocol'")


class NoResponseFound(SentryReportedException):
    "Thrown when no Response data is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain any Response data.")


class NoUnitFound(SentryReportedException):
    "Thrown when no unit is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain a 'unit'.")


class NoRateFound(SentryReportedException):
    "Thrown when no rate is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain a 'rate'.")


class NoConversionFound(SentryReportedException):
    "Thrown when no conversion is found."

    def __init__(self):
        super().__init__(status_code=404, detail="The NWB file didn't contain a 'conversion'.")
