"""Imported modules/packages"""
import datetime


class Price:
    """
    Price entity
    """

    def __init__(self, excluding_tax: int, tax: int):
        self.excluding_tax: int = excluding_tax
        self.tax: int = tax
        self.logged_at = datetime.datetime.now()

    @property
    def tax_rate(self) -> float:
        """
        Get tax rate
        :return:
        """
        return 1 - self.excluding_tax / self.including_tax

    @property
    def including_tax(self) -> int:
        """
        Get price including tax
        :return:
        """
        return self.excluding_tax + self.tax
