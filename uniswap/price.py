from fraction import Fraction
from currency_amount import CurrencyAmount

class Price(Fraction):

    def __init__(self, base_currency, quote_currency, denominator, numerator) -> None:
        super().__init__(numerator, denominator)
        self.base_currency = base_currency
        self.quote_currency = quote_currency
        self.scalar = 1 # We will default this for now as we assume the tokens from UniSwap are all represented with the same number of decimals.

    def invert(self):
        return Price(self.quote_currency, self.base_currency, self.numerator, self.denominator)

    def multiply(self, other: 'Price'):
        """
        Multiply the price by another price, returning a new price. 
        The other price must have the same base currency as this price's quote currency
        """
        if self.base_currency != other.base_currency:
            raise Exception('Prices must have the same base currency.')
        fraction = super(Price, self).multiply(other)
        return Price(self.base_currency, self. quote_currency, fraction.denominator, fraction.numerator)

    def quote(self, currency_amount: CurrencyAmount):
        """
        Return the amount of quote currency corresponding to a given amount of the base currency.
        """
        if self.base_currency != currency_amount.currency:
            raise Exception('Prices must have the same base currency.')

        result = super(Price, self).multiply(currency_amount)
        return CurrencyAmount.from_fractional_amount(self.quote_currency, result.numerator, result.denominator)
