"""
Module to setup the environment variables of the application
"""

import os
from dotenv import load_dotenv
import matplotlib

matplotlib.use("agg")

load_dotenv()

WHITELISTED_CORS_URLS = os.environ.get("WHITELISTED_CORS_URLS", "")
DEBUG_MODE = os.environ.get("DEBUG_MODE", False)
# ? Points to the Nexus Delta API for getting SWC files
NEXUS_DELTA_API = os.getenv("NEXUS_DELTA_API", "http://localhost:8000")
