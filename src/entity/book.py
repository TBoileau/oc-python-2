"""Imported modules/packages"""
from src.entity.price import Price


class Book:
    """
    Book entity
    """

    def __init__(
        self,
        url: str,
        code: str,
        title: str,
        price: Price,
        stock: int,
        description: str,
        category: str,
        rating: int,
        image: str,
    ):
        self.url: str = url
        self.code: str = code
        self.title: str = title
        self.price: Price = price
        self.stock: int = stock
        self.description: str = description
        self.category: str = category
        self.rating: int = rating
        self.image: str = image
