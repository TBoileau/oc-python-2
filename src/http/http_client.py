"""Imported modules/packages"""
from requests import get, Response

from src.http.http_client_interface import HttpClientInterface


class HttpClient(HttpClientInterface):
    """
    HttpClient implementation
    """

    def request(self, url: str) -> Response:
        return get(url)
