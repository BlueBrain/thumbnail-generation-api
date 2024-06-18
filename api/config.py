"""
Module to setup the environment variables of the application
"""

import os
from dotenv import load_dotenv
import matplotlib

matplotlib.use("agg")

load_dotenv()

WHITELISTED_CORS_URLS = os.environ.get("WHITELISTED_CORS_URLS", "")
DEBUG_MODE = os.environ.get("DEBUG_MODE", False) == "True"
BASE_PATH = os.environ.get("BASE_PATH", "")
