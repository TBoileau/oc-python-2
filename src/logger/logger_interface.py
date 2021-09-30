"""Imported modules/packages"""
from abc import ABC


class LoggerInterface(ABC):
    """
    Logger interface
    """

    def log(self, output: str):
        """
        Log

        :param output:
        :return:
        """
