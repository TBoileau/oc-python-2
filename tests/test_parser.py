from functools import reduce
from typing import Tuple, List

from src.crawler.crawler import Crawler
from src.crawler.crawler_interface import CrawlerInterface
from src.entity.category import Category
from src.http.http_client import HttpClient
from src.http.http_client_interface import HttpClientInterface
from src.parser.parser import Parser
from src.parser.parser_interface import ParserInterface
from src.url_generator.url_generator import UrlGenerator
from src.url_generator.url_generator_interface import UrlGeneratorInterface


def test_get_list_of_categories():
    url_generator: UrlGeneratorInterface = UrlGenerator('https://books.toscrape.com/')
    http_client: HttpClientInterface = HttpClient()
    crawler: CrawlerInterface = Crawler(url_generator, http_client)
    parser: ParserInterface = Parser(crawler, url_generator)
    categories: List[Category] = parser.parse()
    assert len(categories) == 50
    assert reduce(
        lambda number_of_books, y: y + number_of_books,
        map(lambda category: len(category.books), categories)
    ) == 1000
