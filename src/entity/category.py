"""Imported modules/packages"""


class Category:
    """
    Category entity
    """

    def __init__(self, url: str, name: str):
        """
        Constructor

        :param url:
        :param name:
        """
        self.url: str = url
        self.name: str = name
