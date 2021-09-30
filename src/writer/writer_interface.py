"""Imported modules/packages"""
from abc import ABC
from typing import List

from src.entity.category import Category


class WriterInterface(ABC):
    """
    Writer interface
    """

    def write(self, categories: List[Category], directory: str):
        """
        Upload and return new url

        :param categories:
        :param directory:
        :return:
        """
