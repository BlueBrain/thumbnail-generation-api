"""
Definition of application enums
"""

from enum import Enum


class MetaType(Enum):
    """
    Meta type definition for element selection in trace thumbnail  generation
    """

    CELL = "cell"
    REPETITION = "repetition"
    SWEEP = "sweep"


class Environment(str, Enum):
    """
    Defines the different environments that the application can be deployed in

    LOCAL: the local environment
    DEVELOPMENT: the development environment (dev branch deployment)
    STAGING: the staging environment
    PRODUCTION: the production environment
    """

    LOCAL = "local"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
