import datetime
import re
from functools import reduce
from typing import Tuple, List

import os
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
from src.uploader.uploader import Uploader
from src.uploader.uploader_interface import UploaderInterface
from src.url_generator.url_generator import UrlGenerator
from src.url_generator.url_generator_interface import UrlGeneratorInterface
from src.writer.csv_writer import CsvWriter
from src.writer.writer_interface import WriterInterface


@pytest.fixture(scope="session")
def httpserver_listen_address() -> Tuple[str, int]:
    return "localhost", 8000

def handler(request: Request):
    url: ParseResult = urlparse(request.url)
    mode: str = 'r'
    if url.path.endswith('.jpg'):
        mode = 'rb'
    content = open(os.path.join(os.getcwd(), "fixtures", url.path[1:]), mode).read()
    return Response(content)

def test_get_list_of_categories(httpserver):
    image_folder = os.path.join(os.getcwd(), 'dist/images')
    csv_folder = os.path.join(os.getcwd(), 'dist/csv', datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
    os.mkdir(csv_folder)
    httpserver.expect_request(re.compile('.*')).respond_with_handler(handler)
    url_generator: UrlGeneratorInterface = UrlGenerator('http://localhost:8000')
    http_client: HttpClientInterface = HttpClient()
    crawler: CrawlerInterface = Crawler(url_generator, http_client)
    uploader: UploaderInterface = Uploader(http_client, image_folder)
    parser: ParserInterface = Parser(crawler, url_generator, uploader)
    categories: List[Category] = parser.parse()
    writer: WriterInterface = CsvWriter()
    writer.write(categories, csv_folder)
    assert len(categories) == 50
    assert reduce(
        lambda number_of_books, y: y + number_of_books,
        map(lambda category: len(category.books), categories)
    ) == 1000
    assert 1000 == (len([name for name in os.listdir(image_folder)]) - 1)
    assert 50 == len([name for name in os.listdir(csv_folder)])
