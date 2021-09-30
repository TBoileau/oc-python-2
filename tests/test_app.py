import re
from typing import Tuple

import os
import pytest
from urllib.parse import ParseResult, urlparse

from werkzeug import Request, Response

from src.app import App


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

def test_app(httpserver):
    httpserver.expect_request(re.compile('.*')).respond_with_handler(handler)
    app: App = App('http://localhost:8000')
    app.run()
    assert 1000 == len([name for name in os.listdir(app.image_folder)])
    assert 50 == len([name for name in os.listdir(app.csv_folder)])
