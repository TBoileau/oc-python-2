"""Imported modules/packages"""
from bs4 import BeautifulSoup
from requests import Response, HTTPError

from src.crawler.crawler_interface import CrawlerInterface
from src.http.http_client_interface import HttpClientInterface
from src.url_generator.url_generator_interface import UrlGeneratorInterface


class Crawler(CrawlerInterface):
    """ "
    Crawler implementation
    """

    def __init__(self, url_generator: UrlGeneratorInterface, http_client: HttpClientInterface):
        """
        Constructor

        :param url_generator:
        :param http_client:
        """
        self.__url_generator: UrlGeneratorInterface = url_generator
        self.__http_client: HttpClientInterface = http_client

    def crawl(self, path: str) -> BeautifulSoup:
        response: Response = self.__http_client.request(self.__url_generator.generate(path).url)
        if response.status_code != 200:
            raise HTTPError("Not found")
        return BeautifulSoup(response.content, "html.parser")
