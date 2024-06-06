"""
Module to setup the environment variables of the application
"""

import os
from dotenv import load_dotenv
import matplotlib

matplotlib.use("agg")

load_dotenv()


WHITELISTED_CORS_URLS = os.environ.get("WHITELISTED_CORS_URLS", "")


DEBUG_MODE: bool  # fastapi expects a bool, os.environ returns a str
debug_mode = os.environ.get("DEBUG_MODE", "false")

if debug_mode == "true":
    DEBUG_MODE = True
else:
    DEBUG_MODE = False
