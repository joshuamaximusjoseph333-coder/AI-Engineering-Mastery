import src.data_loader.logger

from src.data_loader.config import (
    CUSTOMERS_DATA_PATH,
    DATABASE_PATH,
    ORDERS_DATA_PATH,
)
from src.data_loader.database import (
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
from src.data_loader.loader import load_csv
from src.data_loader.profiler import profile_data
from src.data_loader.statistics import (
    get_descriptive_statistics,
    get_outliers,
)
from src.data_loader.validator import (
    validate_order_values,
    validate_required_columns,
)


# Load data
orders = load_csv(
    ORDERS_DATA_PATH,
    parse_dates=["order_date"],
)

customers = load_csv(CUSTOMERS_DATA_PATH)


# Validate orders
validate_required_columns(orders)
validate_order_values(orders)


# Profile orders
profile = profile_data(orders)


# Statistical analysis
price_statistics = get_descriptive_statistics(
    orders,
    "price",
)

price_outliers = get_outliers(
    orders,
    "price",
)


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


# Create database connection
connection = create_connection(DATABASE_PATH)


# Write data to SQLite
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


# Run SQL analysis
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


# Close database connection
connection.close()