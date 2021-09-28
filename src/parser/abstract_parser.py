"""Imported modules/packages"""
from abc import ABC
from urllib import parse

from urllib.parse import ParseResult


class AbstractParser(ABC):
    """
    Abstract parser
    """

    def __init__(self, url: str):
        """
        Constructor

        :param url:
        """
        self.__url: ParseResult = parse.urlparse(url)

    def generate_url(self, path: str) -> str:
        """
        Generate url from path

        :param path:
        :return:
        """
        return f"{self.__url.scheme}://{self.__url.netloc}{path}"
