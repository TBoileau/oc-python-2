"""Imported modules/packages"""
from abc import ABC
from typing import List

from src.entity.category import Category


class ParserInterface(ABC):
    """
    Parser interface
    """

    def parse(self) -> List[Category]:
        """
        Retrieve list of categories

        :return:
        """
