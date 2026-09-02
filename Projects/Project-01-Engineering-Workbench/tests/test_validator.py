import pandas as pd
import pytest
from engineering_workbench.validator import (
    validate_order_values,
    validate_required_columns,
)


def test_validate_required_columns_passes():
    data = pd.DataFrame(
        {
            "order_id": [1001, 1002],
            "customer_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "quantity": [1, 2],
            "price": [50000, 1000],
            "order_date": ["2026-08-01", "2026-08-02"],
            "payment_method": ["Card", "UPI"],
        }
    )

    validate_required_columns(data)

def test_validate_order_values_passes():
    data = pd.DataFrame(
        {
            "order_id": [1001, 1002],
            "customer_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "quantity": [1, 2],
            "price": [50000, 1000],
            "order_date": pd.to_datetime(
                ["2026-08-01", "2026-08-02"]
            ),
            "payment_method": ["Card", "UPI"],
        }
    )

    validate_order_values(data)

def test_validate_required_columns_raises_for_missing_column():
    data = pd.DataFrame(
        {
            "order_id": [1001, 1002],
            "customer_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "quantity": [1, 2],
            "price": [50000, 1000],
            "order_date": ["2026-08-01", "2026-08-02"],
            # payment_method intentionally missing
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(data)

def test_validate_order_values_rejects_invalid_quantity():
    data = pd.DataFrame(
        {
            "order_id": [1001],
            "customer_id": [1],
            "product": ["Laptop"],
            "quantity": [0],
            "price": [50000],
            "order_date": pd.to_datetime(["2026-08-01"]),
            "payment_method": ["Card"],
        }
    )

    with pytest.raises(ValueError, match="quantity must be greater than 0"):
        validate_order_values(data)

def test_validate_order_values_rejects_duplicate_order_id():
    data = pd.DataFrame(
        {
            "order_id": [1001, 1001],
            "customer_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "quantity": [1, 2],
            "price": [50000, 1000],
            "order_date": pd.to_datetime(
                ["2026-08-01", "2026-08-02"]
            ),
            "payment_method": ["Card", "UPI"],
        }
    )

    with pytest.raises(ValueError, match="order_id contains duplicate values"):
        validate_order_values(data)
