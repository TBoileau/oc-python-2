"""Imported modules/packages"""
from urllib.parse import urlparse

from src.url_generator.url import Url
from src.url_generator.url_generator_interface import UrlGeneratorInterface


class UrlGenerator(UrlGeneratorInterface):
    """
    UrlGenerator implementation
    """

    def __init__(self, base: str):
        """
        Constructor

        :param base:
        """
        self.__base: str = base

    def generate(self, path: str) -> Url:
        return Url(urlparse(f"{self.__base}{path}"))
