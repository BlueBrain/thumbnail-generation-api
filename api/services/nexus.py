from exceptions import InvalidUrlParameterException, ResourceNotFoundException


import requests


from urllib.parse import urlparse


def get_file_content(authorization: str = "", content_url: str = "") -> bytes:
    """
    Gets the File content of a Nexus distribution (by requesting the resource from its content_url).

    Parameters:
        - authorization (str): Authorization header containing the access token.
        - content_url (str): URL of the distribution.

    Returns:
        str: File content as a string.

    Raises:
        str: Error message if the request to the content_url fails.
    """
    parsed_content_url = urlparse(content_url)

    if not all([parsed_content_url.scheme, parsed_content_url.netloc, parsed_content_url.path]):
        raise InvalidUrlParameterException

    response = requests.get(content_url, headers={"authorization": authorization}, timeout=15)

    if response.status_code == 200:
        return response.content
    if response.status_code == 404:
        raise ResourceNotFoundException
    raise requests.exceptions.RequestException
