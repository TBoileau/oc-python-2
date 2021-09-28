"""Imported modules/packages"""
import re
from urllib import parse
from urllib.parse import ParseResult
from typing import Optional, Generator

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from src.entity.book import Book
from src.entity.price import Price
from src.gateway.book_gateway import BookGateway


class BookParser(BookGateway):
    """
    Adapter of port BookGateway
    """

    def __init__(self, url: str):
        """
        Constructor

        :param url:
        """
        self.__url: ParseResult = parse.urlparse(url)

    def generate_url(self, path: str) -> str:
        """
        Generate url from path

        :param path:
        :return:
        """
        return f"{self.__url.scheme}://{self.__url.netloc}{path}"

    def find_all(self, path: str) -> Generator[Book, None, None]:
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
        for category in categories:
            yield from self.find_by_category(f"/{category['href']}")

    def find_by_category(self, path: str) -> Generator[Book, None, None]:
        """
        Retrieve book by url

        :param path:
        :return:
        """

        response: requests.Response = requests.get(self.generate_url(path))
        crawler: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        books: ResultSet = crawler.select("article.product_pod > h3 > a")

        for book in books:
            yield self.find(
                f"/catalogue/{book['href'].replace('../../../', '')}"
            )

        next_page: Optional[Tag] = crawler.select_one("ul.pager > li.next > a")

        if next_page is not None:
            yield from self.find_by_category(
                f"{path[0:path.rfind('/')]}/{next_page['href']}"
            )

    def find(self, path: str) -> Optional[Book]:
        """
        Retrieve books by category

        :param url:
        :return:
        """
        url: str = self.generate_url(path)
        response: requests.Response = requests.get(url)

        if response.status_code != 200:
            return None

        parsed_url: ParseResult = parse.urlparse(url)
        crawler: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        rating: int = 0

        if "One" in crawler.select_one("p.star-rating")["class"]:
            rating = 1
        elif "Two" in crawler.select_one("p.star-rating")["class"]:
            rating = 2
        elif "Three" in crawler.select_one("p.star-rating")["class"]:
            rating = 3
        elif "Four" in crawler.select_one("p.star-rating")["class"]:
            rating = 4
        elif "Five" in crawler.select_one("p.star-rating")["class"]:
            rating = 5

        price: Price = Price(
            excluding_tax=int(
                float(
                    crawler.select_one(
                        "table > tr:nth-child(3) > td:last-child"
                    )
                    .text.strip()
                    .replace("£", "")
                )
                * 100
            ),
            tax=int(
                float(
                    crawler.select_one(
                        "table > tr:nth-child(5) > td:last-child"
                    )
                    .text.strip()
                    .replace("£", "")
                )
                * 100,
            ),
        )

        image_url: str = crawler.select_one("div#product_gallery img")[
            "src"
        ].replace("../../", "")

        description: Optional[Tag] = crawler.select_one(
            "div#product_description + p"
        )

        return Book(
            url=url,
            code=crawler.select_one(
                "table > tr:nth-child(1) > td:last-child"
            ).text.strip(),
            title=crawler.select_one("h1").text.strip(),
            description=description.text.strip()
            if description is not None
            else "",
            price=price,
            stock=(
                0,
                int(
                    re.match(
                        "^In stock \\((\\d+) available\\)$",
                        crawler.select_one(
                            "p.instock.availability"
                        ).text.strip(),
                    ).groups()[0]
                ),
            )[crawler.select_one("p.instock.availability") is not None],
            category=crawler.select_one(
                "ul.breadcrumb > li:nth-child(3) > a"
            ).text.strip(),
            rating=rating,
            image=f"{parsed_url.scheme}://{parsed_url.netloc}/{image_url}",
        )
