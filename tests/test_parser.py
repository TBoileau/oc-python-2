import re
from functools import reduce
from typing import Tuple, List

import pytest
from urllib.parse import ParseResult, urlparse
from werkzeug import Request, Response

from src.crawler.crawler import Crawler
from src.crawler.crawler_interface import CrawlerInterface
from src.entity.category import Category
from src.http.http_client import HttpClient
from src.http.http_client_interface import HttpClientInterface
from src.parser.parser import Parser
from src.parser.parser_interface import ParserInterface
from src.url_generator.url_generator import UrlGenerator
from src.url_generator.url_generator_interface import UrlGeneratorInterface


@pytest.fixture(scope="session")
def httpserver_listen_address() -> Tuple[str, int]:
    return "localhost", 8000

def handler(request: Request):
    url: ParseResult = urlparse(request.url)
    content: str = open(f"fixtures/books.toscrape.com{url.path}").read()
    return Response(content)

def test_get_list_of_categories(httpserver):
    httpserver.expect_request(re.compile('.*')).respond_with_handler(handler)
    url_generator: UrlGeneratorInterface = UrlGenerator('http://localhost:8000')
    http_client: HttpClientInterface = HttpClient()
    crawler: CrawlerInterface = Crawler(url_generator, http_client)
    parser: ParserInterface = Parser(crawler, url_generator)
    categories: List[Category] = parser.parse()
    assert len(categories) == 50
    assert reduce(
        lambda number_of_books, y: y + number_of_books,
        map(lambda category: len(category.books), categories)
    ) == 999
