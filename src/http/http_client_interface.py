"""Imported modules/packages"""
from abc import ABC

from requests import Response


class HttpClientInterface(ABC):
    """
    HttpClient interface
    """

    def request(self, url: str) -> Response:
        """
        Send http request to return a http response

        :param url:
        :return:
        """
