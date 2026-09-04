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