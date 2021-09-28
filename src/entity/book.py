"""Imported modules/packages"""
from src.entity.category import Category
from src.entity.price import Price


class Book:
    """
    Book entity
    """

    def __init__(
        self,
        category: Category,
        url: str,
        code: str,
        title: str,
        price: Price,
        stock: int,
        description: str,
        rating: int,
        image: str,
    ):
        self.category: Category = category
        self.url: str = url
        self.code: str = code
        self.title: str = title
        self.price: Price = price
        self.stock: int = stock
        self.description: str = description
        self.rating: int = rating
        self.image: str = image
