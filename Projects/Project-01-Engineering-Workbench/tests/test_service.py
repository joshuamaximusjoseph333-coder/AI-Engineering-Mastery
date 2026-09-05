import pandas as pd
import pytest
from engineering_workbench.service import (
    run_analysis,
    run_database_analysis,
)


def test_run_analysis_returns_expected_sections():
    results = run_analysis()

    assert "orders" in results
    assert "profile" in results
    assert "price_statistics" in results
    assert "price_outliers" in results

def test_run_database_analysis_returns_expected_sections():
    results = run_database_analysis()

    assert "expensive_orders" in results
    assert "payment_counts" in results
    assert "product_totals" in results
    assert "customer_order_details" in results
    assert "all_customers_with_orders" in results
    assert "customers_without_orders" in results
    assert "orders_per_customer" in results
    assert "revenue_by_city" in results

def test_run_analysis_stops_on_invalid_order_data(monkeypatch):
    invalid_orders = pd.DataFrame(
        {
            "order_id": [1],
            "customer_id": [101],
            "product": ["Laptop"],
            "quantity": [0],
            "price": [50000],
            "order_date": pd.to_datetime(["2026-01-01"]),
            "payment_method": ["Card"],
        }
    )

    monkeypatch.setattr(
        "engineering_workbench.service.load_csv",
        lambda *args, **kwargs: invalid_orders,
    )

    with pytest.raises(
        ValueError,
        match="quantity must be greater than 0",
    ):
        run_analysis()

def test_run_analysis_propagates_file_not_found(monkeypatch):
    def fake_load_csv(*args, **kwargs):
        raise FileNotFoundError("orders file not found")

    monkeypatch.setattr(
        "engineering_workbench.service.load_csv",
        fake_load_csv,
    )

    with pytest.raises(
        FileNotFoundError,
        match="orders file not found",
    ):
        run_analysis()

def test_run_database_analysis_closes_connection_on_failure(monkeypatch):
    class FakeConnection:
        def __init__(self):
            self.closed = False

        def close(self):
            self.closed = True

    fake_connection = FakeConnection()

    monkeypatch.setattr(
        "engineering_workbench.service.load_and_validate_orders",
        lambda: pd.DataFrame(),
    )

    monkeypatch.setattr(
        "engineering_workbench.service.load_csv",
        lambda *args, **kwargs: pd.DataFrame(),
    )

    monkeypatch.setattr(
        "engineering_workbench.service.create_connection",
        lambda *args, **kwargs: fake_connection,
    )

    def fail_write(*args, **kwargs):
        raise RuntimeError("database write failed")

    monkeypatch.setattr(
        "engineering_workbench.service.write_dataframe_to_table",
        fail_write,
    )

    with pytest.raises(
        RuntimeError,
        match="database write failed",
    ):
        run_database_analysis()

    assert fake_connection.closed is True
    