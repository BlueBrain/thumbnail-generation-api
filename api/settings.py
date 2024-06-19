"""
Module to setup the environment variables of the application
"""

import matplotlib
from dotenv import load_dotenv
from pydantic import ValidationError
from pydantic_settings import BaseSettings, SettingsConfigDict
from api.models.enums import Environment

matplotlib.use("agg")

# Load environment variables from the .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Defines basic global settings that can be used throughout the application.

    Variables are retrieved from environment variables but also calculated based on environment variables
    """

    model_config = SettingsConfigDict(env_file=".env")

    whitelisted_cors_urls: str = ""
    base_path: str = ""
    environment: Environment = Environment.LOCAL
    sentry_dsn: str = ""

    @property
    def debug_mode(self) -> bool:
        """
        Only "local" and "development" have debug_mode = True
        """
        return self.environment in (Environment.LOCAL, Environment.DEVELOPMENT)


settings = Settings()
