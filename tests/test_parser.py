import re
from functools import reduce
from os import getcwd
from typing import Tuple, List

import pytest
from urllib.parse import ParseResult, urlparse

from requests import get
from werkzeug import Request, Response

from src.crawler.crawler import Crawler
from src.crawler.crawler_interface import CrawlerInterface
from src.entity.category import Category
from src.http.http_client import HttpClient
from src.http.http_client_interface import HttpClientInterface
from src.parser.parser import Parser
from src.parser.parser_interface import ParserInterface
from src.uploader.uploader import Uploader
from src.uploader.uploader_interface import UploaderInterface
from src.url_generator.url_generator import UrlGenerator
from src.url_generator.url_generator_interface import UrlGeneratorInterface

@pytest.fixture(scope="session")
def httpserver_listen_address() -> Tuple[str, int]:
    return "localhost", 8000

def image_handler(request: Request):
    url: ParseResult = urlparse(request.url)
    print(url.path)
    content: bytes = open(f"fixtures/{url.path}", 'rb').read()
    return Response(content)

def handler(request: Request):
    url: ParseResult = urlparse(request.url)
    mode: str = 'r'
    if url.path.endswith('.jpg'):
        mode = 'rb'
    content = open(f"fixtures/{url.path}", mode).read()
    return Response(content)

def test_get_list_of_categories(httpserver):
    httpserver.expect_request(re.compile('.*')).respond_with_handler(handler)
    url_generator: UrlGeneratorInterface = UrlGenerator('http://localhost:8000')
    http_client: HttpClientInterface = HttpClient()
    crawler: CrawlerInterface = Crawler(url_generator, http_client)
    uploader: UploaderInterface = Uploader(http_client, f'{getcwd()}/dist/images')
    parser: ParserInterface = Parser(crawler, url_generator, uploader)
    categories: List[Category] = parser.parse()
    assert len(categories) == 50
    assert reduce(
        lambda number_of_books, y: y + number_of_books,
        map(lambda category: len(category.books), categories)
    ) == 1000
