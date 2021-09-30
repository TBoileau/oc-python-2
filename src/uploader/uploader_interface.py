"""Imported modules/packages"""
from abc import ABC

from src.url_generator.url import Url


class UploaderInterface(ABC):
    """
    Uploader interface
    """

    def upload(self, source: Url) -> Url:
        """
        Upload and return new url

        :param source:
        :return:
        """
