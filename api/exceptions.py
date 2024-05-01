"""
Module: exceptions.py

This module defines a custom exception classes
"""


class ResourceNotFoundException(Exception):
    """Exception raised when a requested resource is not found.

    This exception is typically used to indicate that a resource, such as a file, database record,
    or network endpoint, is expected to exist but cannot be located.
    """


class InvalidUrlParameterException(Exception):
    """Exception raised when a URL parameter is empty or invalid.

    This exception is typically used to indicate that a parameter, such as a content_url, is expected to exist,
    and be valid, but instead is either an empty string or simply not a valid URL.
    """


class NoCellFound(Exception):
    "Thrown when no cell is found."


class NoRepetitionFound(Exception):
    "Thrown when no repetition is found."


class NoSweepFound(Exception):
    "Thrown when no sweep is found."


class NoProtocolFound(Exception):
    "Thrown when no protocol is found."


class NoIcDataFound(Exception):
    "Thrown when no Ic data is found."


class NoUnitFound(Exception):
    "Thrown when no unit is found."


class NoRateFound(Exception):
    "Thrown when no rate is found."


class NoConversionFound(Exception):
    "Thrown when no conversion is found."


# TODO: Add custom exceptions for NeuroMorphoVis specific things and use them accordingly in the code
