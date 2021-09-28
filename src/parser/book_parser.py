"""Imported modules/packages"""
import re
from urllib import parse
from urllib.parse import ParseResult
from typing import Optional, Generator

import requests
from bs4 import BeautifulSoup, ResultSet, Tag

from src.entity.book import Book
from src.entity.category import Category
from src.entity.price import Price
from src.gateway.book_gateway import BookGateway
from src.parser.abstract_parser import AbstractParser


class BookParser(BookGateway, AbstractParser):
    """
    Adapter of port BookGateway
    """

    def find_by_category(
        self, category: Category, page=1
    ) -> Generator[Book, None, None]:
        """
        Retrieve book by category

        :param page:
        :param category:
        :return:
        """

        page_path: str = f"page-{page}.html" if page > 1 else "index.html"

        response: requests.Response = requests.get(
            f"{category.url[0:category.url.rfind('/')]}/{page_path}"
        )
        crawler: BeautifulSoup = BeautifulSoup(response.content, "html.parser")

        books: ResultSet = crawler.select("article.product_pod > h3 > a")

        for book in books:
            yield self.find(
                f"/catalogue/{book['href'].replace('../../../', '')}"
            )

        next_page: Optional[Tag] = crawler.select_one("ul.pager > li.next > a")

        if next_page is not None:
            yield from self.find_by_category(category, page + 1)

    def find(self, path: str) -> Optional[Book]:
        """
        Retrieve books by category

        :param path:
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

        category: Tag = crawler.select_one(
            "ul.breadcrumb > li:nth-child(3) > a"
        )

        return Book(
            category=Category(
                self.generate_url(category["href"]), category.text.strip()
            ),
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
            rating=rating,
            image=f"{parsed_url.scheme}://{parsed_url.netloc}/{image_url}",
        )
