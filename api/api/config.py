"""
Module to setup the environment variables of the application
"""

import os

WHITELISTED_CORS_URLS = os.environ.get("WHITELISTED_CORS_URLS", "")
DEBUG_MODE = os.environ.get("DEBUG_MODE", False)
