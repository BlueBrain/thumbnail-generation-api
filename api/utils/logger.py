"""This module contains the logger configuration for the ThumbnailAPI."""

import logging


def setup_logger():
    """Configure the logger to log messages to the console."""
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    return logging.getLogger("ThumbnailAPI")


logger = setup_logger()
