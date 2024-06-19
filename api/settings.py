"""
Module to setup the environment variables of the application
"""

import os
import matplotlib
from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic_settings import BaseSettings
from api.models.enums import Environment

matplotlib.use("agg")

# Load environment variables from the .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Defines basic global settings that can be used throughout the application.

    Variables are retrieved from environment variables but also calculated based on environment variables
    """

    # Define your environment variables with default values if needed
    WHITELISTED_CORS_URLS: str = ""
    BASE_PATH: str = ""
    ENVIRONMENT: Environment = Environment.LOCAL
    SENTRY_DSN: str = ""

    class Config:
        """
        Basic configuration of settings
        """

        env_file = ".env"

    @property
    def debug_mode(self) -> bool:
        """
        Only "local" and "development" have debug_mode = True
        """
        return self.ENVIRONMENT in (Environment.LOCAL, Environment.DEVELOPMENT)


# Initialize settings
try:
    settings = Settings()
except ValidationError as e:
    raise EnvironmentError(f"Configuration validation error: {e}") from e
