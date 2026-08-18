import src.data_loader.logger

from src.data_loader.config import DATA_PATH, DATABASE_PATH
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
)

data = load_csv(
    DATA_PATH,
    parse_dates=["order_date"],
)

validate_required_columns(data)
validate_order_values(data)

profile = profile_data(data)

for key, value in profile.items():
    print(f"{key}: {value}")

connection = create_connection(DATABASE_PATH)

write_dataframe_to_table(
    connection,
    data,
    "orders",
)

expensive_orders = get_expensive_orders(
    connection,
    minimum_price=3000,
)

payment_counts = get_payment_method_counts(connection)

product_totals = get_product_quantity_totals(connection)

print("Expensive orders:", expensive_orders)
print("Payment method counts:", payment_counts)
print("Product quantity totals:", product_totals)

connection.close()