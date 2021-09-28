"""Imported modules/packages"""
from abc import ABC
from typing import Generator

from src.entity.category import Category


class CategoryGateway(ABC):
    """
    Category gateway
    """

    def find_all(self, path: str) -> Generator[Category, None, None]:
        """
        Retrieve all books

        :param path:
        :return:
        """
