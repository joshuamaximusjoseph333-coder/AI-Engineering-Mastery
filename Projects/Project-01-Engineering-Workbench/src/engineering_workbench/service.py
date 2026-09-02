from engineering_workbench.loader import load_csv
from engineering_workbench.profiler import profile_data
from engineering_workbench.statistics import (
    get_descriptive_statistics,
    get_outliers,
)
from engineering_workbench.validator import (
    validate_order_values,
    validate_required_columns,
)
from engineering_workbench.config import (
    CUSTOMERS_DATA_PATH,
    DATABASE_PATH,
    ORDERS_DATA_PATH,
)
from engineering_workbench.database import (
    create_connection,
    get_all_customers_with_orders,
    get_customer_order_details,
    get_customers_without_orders,
    get_expensive_orders,
    get_orders_per_customer,
    get_payment_method_counts,
    get_product_quantity_totals,
    get_revenue_by_city,
    write_dataframe_to_table,
)

def run_analysis():
    orders = load_csv(
        ORDERS_DATA_PATH,
        parse_dates=["order_date"],
    )

    validate_required_columns(orders)
    validate_order_values(orders)

    profile = profile_data(orders)

    price_statistics = get_descriptive_statistics(
        orders,
        "price",
    )

    price_outliers = get_outliers(
        orders,
        "price",
    )

    return {
        "orders": orders,
        "profile": profile,
        "price_statistics": price_statistics,
        "price_outliers": price_outliers,
    }

def run_database_analysis(orders):
    customers = load_csv(CUSTOMERS_DATA_PATH)

    connection = create_connection(DATABASE_PATH)

    try:
        write_dataframe_to_table(
            connection,
            orders,
            "orders",
        )

        write_dataframe_to_table(
            connection,
            customers,
            "customers",
        )

        expensive_orders = get_expensive_orders(
            connection,
            minimum_price=3000,
        )

        payment_counts = get_payment_method_counts(connection)
        product_totals = get_product_quantity_totals(connection)
        customer_order_details = get_customer_order_details(connection)
        all_customers_with_orders = get_all_customers_with_orders(connection)
        customers_without_orders = get_customers_without_orders(connection)
        orders_per_customer = get_orders_per_customer(connection)
        revenue_by_city = get_revenue_by_city(connection)

        return {
            "expensive_orders": expensive_orders,
            "payment_counts": payment_counts,
            "product_totals": product_totals,
            "customer_order_details": customer_order_details,
            "all_customers_with_orders": all_customers_with_orders,
            "customers_without_orders": customers_without_orders,
            "orders_per_customer": orders_per_customer,
            "revenue_by_city": revenue_by_city,
        }

    finally:
        connection.close()