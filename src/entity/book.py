"""Imported modules/packages"""
from src.entity.price import Price
from src.url_generator.url import Url


class Book:
    """
    Book entity
    """

    def __init__(
        self,
        url: Url,
        price: Price,
        path: str,
        code: str,
        title: str,
        stock: int,
        description: str,
        rating: int,
        image: str,
    ):
        """
        Constructor

        :param price:
        :param url:
        :param path:
        :param code:
        :param title:
        :param stock:
        :param description:
        :param rating:
        :param image:
        """
        self.price: Price = price
        self.url: Url = url
        self.path: str = path
        self.code: str = code
        self.title: str = title
        self.stock: int = stock
        self.description: str = description
        self.rating: int = rating
        self.image: str = image
