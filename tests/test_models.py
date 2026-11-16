import pytest

from models import (
    DiscountedSaleTransaction,
    InvalidTransactionError,
    SaleTransaction,
    TaxedSaleTransaction,
)


def test_polymorphic_totals():
    assert SaleTransaction("Food", 10, 2).calculate_total() == 20
    assert DiscountedSaleTransaction("Food", 10, 2, 0.1).calculate_total() == pytest.approx(18)
    assert TaxedSaleTransaction("Food", 10, 2, 0.05).calculate_total() == pytest.approx(21)


@pytest.mark.parametrize(
    "args",
    [("", 10, 2), ("Food", -1, 2), ("Food", 10, 0), ("Food", 10, 2, 11)],
)
def test_invalid_transactions_rejected(args):
    with pytest.raises(InvalidTransactionError):
        SaleTransaction(*args)