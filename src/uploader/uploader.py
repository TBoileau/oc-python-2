"""Imported modules/packages"""
from typing import Optional

from urllib.parse import urlparse

import os
from requests import Response

from src.http.http_client_interface import HttpClientInterface
from src.logger.logger_interface import LoggerInterface
from src.uploader.uploader_interface import UploaderInterface
from src.url_generator.url import Url


class Uploader(UploaderInterface):
    """
    Uploader implementation
    """

    def __init__(self, http_client: HttpClientInterface, directory: str, logger: LoggerInterface):
        """
        Constructor

        :param http_client:
        :param directory:
        :param logger:
        """
        self.__http_client: HttpClientInterface = http_client
        self.__logger: LoggerInterface = logger
        self.__directory: str = directory

    def upload(self, source: Url) -> Optional[Url]:
        response: Response = self.__http_client.request(source.url)
        if response.status_code != 200:
            return None

        url: Url = Url(urlparse(os.path.join(self.__directory, source.partial)))
        if not os.path.isfile(url.url):
            with open(url.url, "wb") as file:
                self.__logger.log(f"Upload image : {url.partial}")
                file.write(response.content)

        return url
