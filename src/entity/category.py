"""Imported modules/packages"""
from typing import List

from src.entity.book import Book
from src.url_generator.url import Url


class Category:
    """
    Category entity
    """

    def __init__(self, url: Url, name: str):
        """
        Constructor

        :param path:
        :param name:
        """
        self.url: Url = url
        self.name: str = name
        self.books: List[Book] = []
