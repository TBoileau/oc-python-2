"""Imported modules/packages"""
import re
from concurrent.futures import ThreadPoolExecutor, Future, as_completed
from typing import List, Generator, Optional

from bs4 import ResultSet, BeautifulSoup, Tag
from requests import HTTPError

from src.crawler.crawler_interface import CrawlerInterface
from src.entity.book import Book
from src.entity.category import Category
from src.entity.price import Price
from src.parser.parser_interface import ParserInterface
from src.url_generator.url_generator_interface import UrlGeneratorInterface


class Parser(ParserInterface):
    """ "
    Parser implementation
    """

    def __init__(self, crawler: CrawlerInterface, url_generator: UrlGeneratorInterface):
        self.__crawler: CrawlerInterface = crawler
        self.__url_generator: UrlGeneratorInterface = url_generator

    def __get_products(self, path: str, page: int = 1) -> Generator[Book, None, None]:

        partial: str = f"page-{page}.html" if page > 1 else "index.html"

        bs4: BeautifulSoup = self.__crawler.crawl(f"{path[0:path.rfind('/')]}/{partial}")

        books: ResultSet = bs4.select("article.product_pod > h3 > a")

        with ThreadPoolExecutor() as executor:
            futures: List[Future] = []

            for book in books:
                futures.append(executor.submit(self.__get_book, book["href"]))

            for future in as_completed(futures):
                book: Optional[Book] = future.result()
                if book is not None:
                    yield book

        next_page: Optional[Tag] = bs4.select_one("ul.pager > li.next > a")

        if next_page is not None:
            yield from self.__get_products(path, page + 1)

    def __get_book(self, path: str) -> Optional[Book]:
        path = f"/catalogue/{path[9:]}"

        try:
            bs4: BeautifulSoup = self.__crawler.crawl(path)

            price: Price = Price(
                excluding_tax=int(
                    float(bs4.select_one("table > tr:nth-child(3) > td:last-child").text.strip().replace("£", "")) * 100
                ),
                tax=int(
                    float(bs4.select_one("table > tr:nth-child(5) > td:last-child").text.strip().replace("£", "")) * 100
                ),
            )

            rating: int = 0

            if "One" in bs4.select_one("p.star-rating")["class"]:
                rating = 1
            elif "Two" in bs4.select_one("p.star-rating")["class"]:
                rating = 2
            elif "Three" in bs4.select_one("p.star-rating")["class"]:
                rating = 3
            elif "Four" in bs4.select_one("p.star-rating")["class"]:
                rating = 4
            elif "Five" in bs4.select_one("p.star-rating")["class"]:
                rating = 5

            image_url: str = bs4.select_one("div#product_gallery img")["src"].replace("../../", "")

            description: Optional[Tag] = bs4.select_one("div#product_description + p")

            stock: int = (
                0,
                int(
                    re.match(
                        "^In stock \\((\\d+) available\\)$",
                        bs4.select_one("p.instock").text.strip(),
                    ).groups()[0]
                ),
            )[bs4.select_one("p.instock") is not None]

            return Book(
                url=self.__url_generator.generate(path),
                price=price,
                path=path,
                code=bs4.select_one("table > tr:nth-child(1) > td:last-child").text.strip(),
                title=bs4.select_one("h1").text.strip(),
                stock=stock,
                description=description if description is not None else "",
                rating=rating,
                image=image_url,
            )
        except HTTPError:
            return None

    def __populate_category(self, tag: Tag) -> Category:
        category: Category = Category(self.__url_generator.generate(f"/{tag['href']}"), tag.text.strip())

        for book in self.__get_products(category.url.path):
            category.books.append(book)

        return category

    def parse(self) -> List[Category]:
        bs4: BeautifulSoup = self.__crawler.crawl("/index.html")
        categories: ResultSet = bs4.select("div.side_categories > ul.nav > li > ul > li > a")

        with ThreadPoolExecutor() as executor:
            futures: List[Future] = []

            for category in categories:
                futures.append(executor.submit(self.__populate_category, category))

            return [future.result() for future in as_completed(futures)]
