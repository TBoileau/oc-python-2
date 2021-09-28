"""Imported modules/packages"""
from abc import ABC
from typing import Optional, Generator

from src.entity.book import Book
from src.entity.category import Category


class BookGateway(ABC):
    """
    Book gateway
    """

    def find(self, path: str) -> Optional[Book]:
        """
        Retrieve book by url

        :param path:
        :return:
        """

    def find_by_category(
        self, category: Category, page: int = 1
    ) -> Generator[Book, None, None]:
        """
        Retrieve books by category

        :param page:
        :param category:
        :return:
        """
