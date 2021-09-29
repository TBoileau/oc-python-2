"""Imported modules/packages"""
from abc import ABC

from bs4 import BeautifulSoup


class CrawlerInterface(ABC):
    """
    Crawler interface
    """

    def crawl(self, path: str) -> BeautifulSoup:
        """
        Crawl an url by its path

        :param path:
        :return:
        """
