"""Imported modules/packages"""
from abc import ABC
from typing import Optional, Generator

from src.entity.book import Book


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

    def find_by_category(self, path: str) -> Generator[Book, None, None]:
        """
        Retrieve books by category

        :param path:
        :return:
        """

    def find_all(self, path: str) -> Generator[Book, None, None]:
        """
        Retrieve all books

        :param path:
        :return:
        """
