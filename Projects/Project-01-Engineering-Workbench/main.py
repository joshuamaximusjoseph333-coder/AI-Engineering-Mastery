import src.data_loader.logger

from src.data_loader.config import (
    ORDERS_DATA_PATH,
    CUSTOMERS_DATA_PATH,
    DATABASE_PATH,
)
from src.data_loader.loader import load_csv
from src.data_loader.profiler import profile_data
from src.data_loader.validator import (
    validate_order_values,
    validate_required_columns,
)
from src.data_loader.database import (
    create_connection,
    get_expensive_orders,
    get_payment_method_counts,
    get_product_quantity_totals,
    write_dataframe_to_table,
    get_customer_order_details,
    get_all_customers_with_orders,
    get_customers_without_orders,
    get_orders_per_customer,
    get_revenue_by_city,
)

orders = load_csv(
    ORDERS_DATA_PATH,
    parse_dates=["order_date"],
)

customers = load_csv(CUSTOMERS_DATA_PATH)

validate_required_columns(orders)
validate_order_values(orders)

profile = profile_data(orders)

for key, value in profile.items():
    print(f"{key}: {value}")

connection = create_connection(DATABASE_PATH)

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

all_customers_with_orders = get_all_customers_with_orders(connection)

customer_order_details = get_customer_order_details(connection)

customers_without_orders = get_customers_without_orders(connection)

expensive_orders = get_expensive_orders(
    connection,
    minimum_price=3000,
)

orders_per_customer = get_orders_per_customer(connection)

revenue_by_city = get_revenue_by_city(connection)

payment_counts = get_payment_method_counts(connection)

product_totals = get_product_quantity_totals(connection)

print("Expensive orders:", expensive_orders)
print("Payment method counts:", payment_counts)
print("Product quantity totals:", product_totals)
print("Customer order details:", customer_order_details)
print("All customers with orders:", all_customers_with_orders)
print("Customers without orders:", customers_without_orders)
print("Orders per customer:", orders_per_customer)
print("Revenue by city:", revenue_by_city)

connection.close()
