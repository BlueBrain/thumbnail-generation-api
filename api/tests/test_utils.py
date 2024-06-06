import pytest

from ..util import get_file_content, get_buffer
from ..router import swc
from ..exceptions import InvalidUrlParameterException, ResourceNotFoundException
from requests.exceptions import RequestException
from fastapi import HTTPException

from neurom.view import matplotlib_utils

class TestGetFileContent:
    @staticmethod
    def test_malformed_url():
        """
        Tests if get_file_content raises InvalidUrlParameterException 
        in cases when the provided content URL is malformed and doesn't follow the expected structure.
        Such cases can arise from data corruption through network or partial data received.
        """
        invalid_url = "this_is_not//:www.an.url"

        with pytest.raises(InvalidUrlParameterException):
            get_file_content(content_url=invalid_url)

    @staticmethod
    def test_invalid_url():
        """
        Tests if get_file_content raises RequestException for cases when an invalid URL that doesn't resolve.
        """
        invalid_url = "https://www.rust-l4ng.org/"

        with pytest.raises(RequestException):
            get_file_content(content_url=invalid_url)

    @staticmethod
    def test_missing_url_parts():
        """
        Tests if get_file_content raises InvalidUrlParameterException 
        in cases when the provided content URL is malformed and doesn't follow the expected structure.
        Such cases can arise from data corruption through network or partial data received.
        """
        incomplete_url = "://w.example.com"

        with pytest.raises(InvalidUrlParameterException):
            get_file_content(content_url=incomplete_url)

    @staticmethod
    def test_unauthorized_get_file():
        """
        Tests if get_file_content raises RequestException in cases where getting URLs require authorization
        """
        unauthorized_url = "https://httpbin.org/status/401"

        with pytest.raises(RequestException):
            get_file_content(content_url=unauthorized_url)

    @staticmethod
    def test_not_found():
        """
        Tests if get_file_content raises ResourceNotFoundException for cases when
        the provided content URL points to a non-existent resource (404 Not Found).
        """
        unauthorized_url = "https://httpbin.org/status/404"

        with pytest.raises(ResourceNotFoundException):
            get_file_content(content_url=unauthorized_url)

    @staticmethod
    def test_get_file_content():
        """
        Tests if get_file_content retrieves content for a valid URL with status code 200.
        In cases when the provided content URL is valid and returns a successful response (200 OK),
        """
        valid_url = "https://httpbin.org/status/200"

        content = get_file_content(content_url=valid_url)
        assert content == b""

        valid_url = "https://httpbin.org/json"

        content = get_file_content(content_url=valid_url)
        assert len(content) > 0



class TestGetFileContentSwC:
    @staticmethod
    def test_malformed_url():
        """
        Tests if get_file_content raises InvalidUrlParameterException 
        in cases when the provided content URL is malformed and doesn't follow the expected structure.
        Such cases can arise from data corruption through network or partial data received.
        """
        invalid_url = "this_is_not//:www.an.url"

        with pytest.raises(HTTPException):
            swc.get_file_content(authorization="test", content_url=invalid_url)

    @staticmethod
    def test_invalid_url():
        """
        Tests if get_file_content raises HTTPException for cases when an invalid URL that doesn't resolve.
        """
        invalid_url = "https://www.rust-l4ng.org/"

        with pytest.raises(HTTPException):
            swc.get_file_content(authorization="test", content_url=invalid_url)

    @staticmethod
    def test_missing_url_parts():
        """
        Tests if get_file_content raises HTTPException 
        in cases when the provided content URL is malformed and doesn't follow the expected structure.
        Such cases can arise from data corruption through network or partial data received.
        """
        incomplete_url = "://w.example.com"

        with pytest.raises(HTTPException):
            swc.get_file_content(authorization="test", content_url=incomplete_url)

    @staticmethod
    def test_unauthorized_get_file():
        """
        Tests if get_file_content raises HTTPException in cases where getting URLs require authorization
        """
        unauthorized_url = "https://httpbin.org/status/401"

        with pytest.raises(HTTPException):
            swc.get_file_content(authorization="test", content_url=unauthorized_url)

    @staticmethod
    def test_not_found():
        """
        Tests if get_file_content raises HTTPException for cases when
        the provided content URL points to a non-existent resource (404 Not Found).
        """
        unauthorized_url = "https://httpbin.org/status/404"

        with pytest.raises(HTTPException):
            swc.get_file_content(authorization="test", content_url=unauthorized_url)

    @staticmethod
    def test_get_file_content():
        """
        Tests if get_file_content retrieves content for a valid URL with status code 200.
        In cases when the provided content URL is valid and returns a successful response (200 OK),
        """
        valid_url = "https://httpbin.org/status/200"

        content = swc.get_file_content(authorization="test", content_url=valid_url)
        assert content == b""

        valid_url = "https://httpbin.org/json"

        content = swc.get_file_content(authorization="test", content_url=valid_url)
        assert len(content) > 0


class TestGetBuffer:
    @staticmethod
    def test_bytes_from_empty_figure():
        """
        Tests if get_buffer returns a buffer of bytes from an empty figure
        """
        figure, _ = matplotlib_utils.get_figure()
        buffer = get_buffer(figure, dpi=None)

        assert isinstance(buffer.read(0), bytes)

    @staticmethod
    def test_bytes_from_a_know_figure():
        """
        Tests if get_buffer returns a known buffer of bytes from a known figure
        """
        ...
