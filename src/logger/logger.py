"""Imported modules/packages"""
import datetime
import sys

from src.logger.logger_interface import LoggerInterface


class Logger(LoggerInterface):
    """
    Logger implementation
    """

    def log(self, output: str):
        sys.stdout.write(f"{datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')} {output}\n")
