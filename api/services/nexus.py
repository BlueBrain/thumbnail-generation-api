"""
Nexus service to expose business logic of interacting with Nexus
"""

from urllib.parse import urlparse
import requests
from api.exceptions import (
    AuthenticationIssueException,
    AuthorizationIssueException,
    InvalidUrlParameterException,
    ResourceNotFoundException,
)


def fetch_file_content(access_token: str, content_url: str = "") -> bytes:
    """
        Gets the File content of a Nexus distribution (by requesting the resource from its content_url).

        Parameters:
            - authorization (str): Authorization header containing the access token.
            - content_url (str): URL of the distribution.

        Returns:
            str: File content as a string.

    Raises:
        InvalidUrlParameterException: If the content_url is malformed.
        ResourceNotFoundException: If the file is not found (404).
        AuthenticationIssueException: If authentication fails (401).
        AuthorizationIssueException: If access is forbidden (403).
        requests.exceptions.RequestException: For other types of request failures.
    """
    parsed_content_url = urlparse(content_url)

    if not all([parsed_content_url.scheme, parsed_content_url.netloc, parsed_content_url.path]):
        raise InvalidUrlParameterException

    response = requests.get(content_url, headers={"authorization": f"Bearer {access_token}"}, timeout=15)

    if response.status_code == 200:
        return response.content
    if response.status_code == 404:
        raise ResourceNotFoundException
    if response.status_code == 401:
        raise AuthenticationIssueException
    if response.status_code == 403:
        raise AuthorizationIssueException

    raise requests.exceptions.RequestException
