from typing import Union
from constants import (Rounding)


class Fraction: 

    def __init__(self, numerator, denominator = 1):
        self.numerator = numerator
        self.denominator = denominator

    def quotient(self):
        return self.numerator // self.denominator

    def remainder(self):
        return self.numerator % self.denominator

    def invert(self):
        return Fraction(self.denominator, self.numerator)

    def add(self, other: Union['Fraction', int]):
        other_parsed = tryParseFraction(other)
        if self.denominator == other_parsed.denominator:
            return Fraction(self.numerator + other_parsed.numerator, self.denominator)

        return Fraction(
            self.numerator * other_parsed.denominator + other_parsed.numerator * self.denominator,
            self.denominator * other_parsed.denominator
        )

    def subtract(self, other: Union['Fraction', int]):
        other_parsed = tryParseFraction(other)
        if self.denominator == other_parsed.denominator:
            return Fraction(self.numerator - other_parsed.numerator, self.denominator)

        return Fraction(
            self.numerator * other_parsed.denominator - other_parsed.numerator * self.denominator,
            self.denominator * other_parsed.denominator
        )

    def less_than(self, other: Union['Fraction', int]):
        other_parsed = tryParseFraction(other)
        return self.numerator * other_parsed.denominator < other_parsed.numerator * self.denominator

    def greater_than(self, other: Union['Fraction', int]):
        other_parsed = tryParseFraction(other)
        return self.numerator * other_parsed.denominator > other_parsed.numerator * self.denominator

    def equal_to(self, other: Union['Fraction', int]):
        other_parsed = tryParseFraction(other)
        return self.numerator * other_parsed.denominator == other_parsed.numerator * self.denominator

    def multiply(self, other: Union['Fraction', int]):
        other_parsed = tryParseFraction(other)
        return Fraction(
            self.numerator * other_parsed.numerator,
            self.denominator * other_parsed.denominator
        )

    def divide(self, other: Union['Fraction', int]):
        other_parsed = tryParseFraction(other)
        return Fraction(
            self.numerator * other_parsed.denominator,
            self.denominator * other_parsed.numerator
        )

    def to_significant(
        self,
        significant_digits: int,
        format,
        rounding: Rounding = Rounding.ROUND_HALF_UP
    ):
        pass

    def to_fixed(
        self,
        decimal_places,
        format,
        rounding: Rounding = Rounding.ROUND_HALF_UP
    ):
        pass


def tryParseFraction(fractionish: Union[int, Fraction]):
    if type(fractionish) == Fraction or type(fractionish) == int or type(fractionish) == str:
        return Fraction(fractionish)

    if fractionish.numerator != None and fractionish.denominator != None:
        return fractionish

    raise Exception('Could not parse fraction')