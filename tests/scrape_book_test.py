import re
from typing import Tuple
from urllib import parse

from urllib.parse import ParseResult

import pytest
from werkzeug import Request, Response

from src.entity.book import Book
from src.gateway.book_gateway import BookGateway
from src.parser.book_parser import BookParser

@pytest.fixture(scope="session")
def httpserver_listen_address() -> Tuple[str, int]:
    return "localhost", 8000

def handler(request: Request):
    parsed_url: ParseResult = parse.urlparse(request.url)
    return Response(open(f"fixtures/books.toscrape.com{parsed_url.path if parsed_url.path.strip('/') != '' else '/index.html'}").read())

def test_find_book(httpserver):
    httpserver.expect_request(re.compile('/.*')).respond_with_handler(handler)
    book_gateway: BookGateway = BookParser('http://localhost:8000')
    book: Book = book_gateway.find('/catalogue/its-only-the-himalayas_981/index.html')
    assert book.url == 'http://localhost:8000/catalogue/its-only-the-himalayas_981/index.html'
    assert book.code == 'a22124811bfa8350'
    assert book.title == 'It\'s Only the Himalayas'
    assert book.stock > 0
    assert book.price.excluding_tax == 4517
    assert book.price.including_tax == 4517
    assert book.price.tax == 0
    assert book.price.tax_rate == 0.0
    assert book.category == 'Travel'
    assert book.rating == 2
    assert book.image == 'http://localhost:8000/media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg'

def test_find_books_by_category(httpserver):
    httpserver.expect_request(re.compile('/.*')).respond_with_handler(handler)
    book_gateway: BookGateway = BookParser('http://localhost:8000')
    assert len(list(book_gateway.find_by_category('/catalogue/category/books/mystery_3/index.html'))) == 32

def test_find_all_books(httpserver):
    httpserver.expect_request(re.compile('/.*')).respond_with_handler(handler)
    book_gateway: BookGateway = BookParser('http://localhost:8000')
    assert len(list(book_gateway.find_all('/'))) == 1000
