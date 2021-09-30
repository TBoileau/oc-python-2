"""Imported modules/packages"""
from abc import ABC

from src.url_generator.url import Url


class UrlGeneratorInterface(ABC):
    """
    Crawler interface
    """

    def generate(self, path: str) -> Url:
        """
        Generate url with path
        :param path:
        :return:
        """
