"""Imported modules/packages"""
import csv
import os.path
from typing import List

from urllib.parse import urlparse
from slugify import slugify

from src.entity.category import Category
from src.url_generator.url import Url
from src.writer.writer_interface import WriterInterface


class CsvWriter(WriterInterface):
    """
    Writer implementation
    """

    def write(self, categories: List[Category], directory: str):
        for category in categories:
            destination: Url = Url(urlparse(os.path.join(directory, f"{slugify(category.name)}.csv")))
            with open(destination.url, "w", encoding="UTF8") as file:
                writer = csv.writer(file)
                writer.writerow(
                    [
                        "product_page_url",
                        "universal_product_code",
                        "title",
                        "price_including_tax",
                        "price_excluding_tax",
                        "number_available",
                        "product_description",
                        "category",
                        "review_rating",
                        "image_url",
                    ]
                )
                writer.writerows(
                    map(
                        lambda book, cat=category: [
                            book.url.url,
                            book.code,
                            book.title,
                            book.price.including_tax,
                            book.price.excluding_tax,
                            book.stock,
                            book.description,
                            cat.name,
                            book.rating,
                            book.image.url,
                        ],
                        category.books,
                    )
                )
