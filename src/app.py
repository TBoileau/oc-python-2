"""Imported modules/packages"""
import datetime
import os
from typing import List

from src.crawler.crawler import Crawler
from src.crawler.crawler_interface import CrawlerInterface
from src.entity.category import Category
from src.http.http_client import HttpClient
from src.http.http_client_interface import HttpClientInterface
from src.parser.parser import Parser
from src.parser.parser_interface import ParserInterface
from src.uploader.uploader import Uploader
from src.uploader.uploader_interface import UploaderInterface
from src.url_generator.url_generator import UrlGenerator
from src.url_generator.url_generator_interface import UrlGeneratorInterface
from src.writer.csv_writer import CsvWriter
from src.writer.writer_interface import WriterInterface


class App:
    """
    App class
    """

    def __init__(self, url: str):
        """
        Constructor

        :param url:
        """
        self.__url: str = url
        self.__folder: str = os.path.join(os.getcwd(), "dist", datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
        self.image_folder: str = os.path.join(self.__folder, "images")
        self.csv_folder: str = os.path.join(self.__folder, "csv")

    def __create_folders(self):
        """
        Create folder that contains images and csv files

        :return:
        """
        os.mkdir(self.__folder)
        os.mkdir(self.image_folder)
        os.mkdir(self.csv_folder)

    def run(self):
        """
        Run the application

        :return:
        """
        self.__create_folders()
        url_generator: UrlGeneratorInterface = UrlGenerator(self.__url)
        http_client: HttpClientInterface = HttpClient()
        crawler: CrawlerInterface = Crawler(url_generator, http_client)
        uploader: UploaderInterface = Uploader(http_client, self.image_folder)
        parser: ParserInterface = Parser(crawler, url_generator, uploader)
        categories: List[Category] = parser.parse()
        writer: WriterInterface = CsvWriter()
        writer.write(categories, self.csv_folder)
