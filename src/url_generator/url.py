"""Imported modules/packages"""
from urllib.parse import ParseResult


class Url:
    """
    Url
    """

    def __init__(self, url: ParseResult):
        """
        Constructor

        :param url:
        """
        self.__url: ParseResult = url

    @property
    def url(self) -> str:
        """
        Get url

        :return:
        """
        return self.__url.geturl()

    @property
    def path(self) -> str:
        """
        Get path

        :return:
        """
        return self.__url.path

    @property
    def partial(self) -> str:
        """
        Get last part of path
        """
        return self.path[self.path.rfind("/") + 1:]
