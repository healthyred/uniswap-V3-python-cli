from constants import (
    Rounding,
    MAX_UINT_256,
    BigintIsh
)

# NOTE: Implement only if we need it.

from fraction import Fraction

class CurrencyAmount(Fraction):

    def __init__(self, currency, numerator, denominator = None):
        super().__init__(numerator, denominator)
        self.currency = currency

    def from_fractional_amount(currency, numerator, denominator):
        return CurrencyAmount(currency, numerator, denominator)