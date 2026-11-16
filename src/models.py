"""Domain models for sale transactions (OOP part of the project).

Encapsulation : attributes are private (name-mangled) and exposed via read-only properties.
Inheritance   : DiscountedSaleTransaction and TaxedSaleTransaction extend SaleTransaction.
Polymorphism  : every class implements calculate_total() differently.
"""


class InvalidTransactionError(Exception):
    """Raised when a transaction has invalid or missing data."""


class SaleTransaction:
    def __init__(self, product_line, unit_price, quantity, rating=None):
        if not product_line or not str(product_line).strip():
            raise InvalidTransactionError("Product line is missing.")
        if unit_price is None or unit_price <= 0:
            raise InvalidTransactionError(f"Invalid unit price: {unit_price}")
        if quantity is None or quantity <= 0:
            raise InvalidTransactionError(f"Invalid quantity: {quantity}")
        if rating is not None and not (0 <= rating <= 10):
            raise InvalidTransactionError(f"Invalid rating: {rating}")
        self.__product_line = str(product_line).strip()
        self.__unit_price = float(unit_price)
        self.__quantity = quantity
        self.__rating = rating

    @property
    def product_line(self):
        return self.__product_line

    @property
    def unit_price(self):
        return self.__unit_price

    @property
    def quantity(self):
        return self.__quantity

    @property
    def rating(self):
        return self.__rating

    def calculate_total(self):
        return self.__unit_price * self.__quantity

    def __str__(self):
        return f"{self.__product_line} | Total: {self.calculate_total():.2f}"


class DiscountedSaleTransaction(SaleTransaction):
    def __init__(self, product_line, unit_price, quantity, discount, rating=None):
        super().__init__(product_line, unit_price, quantity, rating)
        if discount is None or not (0 <= discount <= 1):
            raise InvalidTransactionError(f"Invalid discount: {discount}")
        self.__discount = discount

    @property
    def discount(self):
        return self.__discount

    def calculate_total(self):
        return self.unit_price * self.quantity * (1 - self.__discount)


class TaxedSaleTransaction(SaleTransaction):
    def __init__(self, product_line, unit_price, quantity, tax_rate=0.05, rating=None):
        super().__init__(product_line, unit_price, quantity, rating)
        if tax_rate is None or tax_rate < 0:
            raise InvalidTransactionError(f"Invalid tax rate: {tax_rate}")
        self.__tax_rate = tax_rate

    @property
    def tax_rate(self):
        return self.__tax_rate

    def calculate_total(self):
        return self.unit_price * self.quantity * (1 + self.__tax_rate)