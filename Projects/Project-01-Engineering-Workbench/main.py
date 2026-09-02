import engineering_workbench.logger

from engineering_workbench import (
    run_analysis,
    run_database_analysis,
)


def main():
    # Run data analysis
    analysis_results = run_analysis()

    profile = analysis_results["profile"]
    price_statistics = analysis_results["price_statistics"]
    price_outliers = analysis_results["price_outliers"]

    # Run database analysis
    database_results = run_database_analysis(
        analysis_results["orders"]
    )

    expensive_orders = database_results["expensive_orders"]
    payment_counts = database_results["payment_counts"]
    product_totals = database_results["product_totals"]
    customer_order_details = database_results["customer_order_details"]
    all_customers_with_orders = database_results[
        "all_customers_with_orders"
    ]
    customers_without_orders = database_results[
        "customers_without_orders"
    ]
    orders_per_customer = database_results["orders_per_customer"]
    revenue_by_city = database_results["revenue_by_city"]

    # Print data profile
    print("\n=== Data Profile ===")

    for key, value in profile.items():
        print(f"{key}: {value}")

    # Print price statistics
    print("\n=== Price Statistics ===")

    for key, value in price_statistics.items():
        print(f"{key}: {value}")

    # Print outlier analysis
    print("\n=== Price Outlier Analysis ===")

    for key, value in price_outliers.items():
        print(f"{key}: {value}")

    # Print SQL analysis
    print("\n=== SQL Analysis ===")

    print("\nExpensive orders:")
    for row in expensive_orders:
        print(row)

    print("\nPayment method counts:")
    for row in payment_counts:
        print(row)

    print("\nProduct quantity totals:")
    for row in product_totals:
        print(row)

    print("\nCustomer order details:")
    for row in customer_order_details:
        print(row)

    print("\nAll customers with orders:")
    for row in all_customers_with_orders:
        print(row)

    print("\nCustomers without orders:")
    for row in customers_without_orders:
        print(row)

    print("\nOrders per customer:")
    for row in orders_per_customer:
        print(row)

    print("\nRevenue by city:")
    for row in revenue_by_city:
        print(row)


if __name__ == "__main__":
    main()