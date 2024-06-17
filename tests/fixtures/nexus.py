"""
Nexus-related fixtures definition
"""

import pytest


@pytest.fixture
def morphology_content_url() -> str:
    return (
        "https://bbp.epfl.ch/nexus/v1/files/bbp/mouselight/https%3A%2F%2Fbbp.epfl.ch%2Fnexus%2Fv1%2Fresources%2Fbbp%2Fmouselight%2F_%2F0befd25c-a28a-4916-9a8a-adcd767db118",
    )[0]


@pytest.fixture
def access_token() -> str:
    return ""
