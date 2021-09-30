"""Imported modules/packages"""
from os.path import isfile
from typing import Optional

from urllib.parse import urlparse
from requests import Response

from src.http.http_client_interface import HttpClientInterface
from src.uploader.uploader_interface import UploaderInterface
from src.url_generator.url import Url


class Uploader(UploaderInterface):
    """
    Uploader implementation
    """

    def __init__(self, http_client: HttpClientInterface, destination: str):
        """
        Constructor

        :param http_client:
        :param destination:
        """
        self.__http_client: HttpClientInterface = http_client
        self.__destination: str = destination

    def upload(self, source: Url) -> Optional[Url]:
        response: Response = self.__http_client.request(source.url)
        if response.status_code != 200:
            return None

        destination_url: Url = Url(urlparse(f"{self.__destination}/{source.partial}"))
        if not isfile(destination_url.url):
            with open(destination_url.url, "wb") as file:
                file.write(response.content)

        return destination_url
