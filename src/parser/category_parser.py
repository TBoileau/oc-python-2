"""Imported modules/packages"""
from typing import Generator

import requests
from bs4 import BeautifulSoup, ResultSet

from src.entity.category import Category
from src.gateway.category_gateway import CategoryGateway
from src.parser.abstract_parser import AbstractParser


class CategoryParser(CategoryGateway, AbstractParser):
    """
    Adapter of port BookGateway
    """

    def find_all(self, path: str) -> Generator[Category, None, None]:
        """
        Retrieve all books

        :param path:
        :return:
        """

        response: requests.Response = requests.get(self.generate_url(path))
        crawler: BeautifulSoup = BeautifulSoup(response.content, "html.parser")
        categories: ResultSet = crawler.select(
            "div.side_categories > ul.nav > li > ul > li > a"
        )

        yield from [
            Category(
                self.generate_url(f"/{category['href']}"),
                category.text.strip(),
            )
            for category in categories
        ]
