import pandas as pd

from engineering_workbench.database import (
    create_connection,
    create_orders_table,
    get_all_orders,
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

def test_create_connection(tmp_path):
    database_path = tmp_path / "test.db"

    connection = create_connection(database_path)

    assert connection is not None

    connection.close()

def test_write_dataframe_to_table(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    data = pd.DataFrame(
        {
            "order_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "price": [50000, 1000],
        }
    )

    write_dataframe_to_table(
        connection,
        data,
        "orders",
    )

    result = connection.execute(
        "SELECT * FROM orders;"
    ).fetchall()

    assert len(result) == 2

    connection.close()

def test_get_expensive_orders(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    data = pd.DataFrame(
        {
            "product": ["Laptop", "Mouse", "Monitor"],
            "price": [50000, 1000, 15000],
        }
    )

    write_dataframe_to_table(connection, data, "orders")

    result = get_expensive_orders(
        connection,
        minimum_price=3000,
    )

    assert result == [
        ("Laptop", 50000),
        ("Monitor", 15000),
    ]

    connection.close()

def test_get_payment_method_counts(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    data = pd.DataFrame(
        {
            "payment_method": [
                "Card",
                "UPI",
                "Card",
                "Card",
            ]
        }
    )

    write_dataframe_to_table(connection, data, "orders")

    result = get_payment_method_counts(connection)

    assert result == [
        ("Card", 3),
        ("UPI", 1),
    ]

    connection.close()

def test_create_orders_table(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    create_orders_table(connection)

    result = connection.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name = 'orders';
        """
    ).fetchone()

    assert result == ("orders",)

    connection.close()

def test_get_customer_order_details(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    orders = pd.DataFrame(
        {
            "order_id": [1001, 1002],
            "customer_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "quantity": [1, 2],
            "price": [50000, 1000],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "customer_name": ["Arjun", "Priya"],
            "city": ["Kochi", "Bengaluru"],
        }
    )

    write_dataframe_to_table(connection, orders, "orders")
    write_dataframe_to_table(connection, customers, "customers")

    result = get_customer_order_details(connection)

    assert result == [
        (1001, "Arjun", "Kochi", "Laptop", 1, 50000),
        (1002, "Priya", "Bengaluru", "Mouse", 2, 1000),
    ]

    connection.close()

def test_get_all_customers_with_orders(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    orders = pd.DataFrame(
        {
            "order_id": [1001],
            "customer_id": [1],
            "product": ["Laptop"],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "customer_name": ["Arjun", "Kiran"],
            "city": ["Kochi", "Pune"],
        }
    )

    write_dataframe_to_table(connection, orders, "orders")
    write_dataframe_to_table(connection, customers, "customers")

    result = get_all_customers_with_orders(connection)

    assert result == [
        (1, "Arjun", "Kochi", 1001, "Laptop"),
        (2, "Kiran", "Pune", None, None),
    ]

    connection.close()

def test_get_customers_without_orders(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    orders = pd.DataFrame(
        {
            "order_id": [1001],
            "customer_id": [1],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "customer_name": ["Arjun", "Kiran"],
            "city": ["Kochi", "Pune"],
        }
    )

    write_dataframe_to_table(connection, orders, "orders")
    write_dataframe_to_table(connection, customers, "customers")

    result = get_customers_without_orders(connection)

    assert result == [
        (2, "Kiran", "Pune"),
    ]

    connection.close()

def test_get_orders_per_customer(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    orders = pd.DataFrame(
        {
            "order_id": [1001, 1002, 1003],
            "customer_id": [1, 1, 2],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": [1, 2, 3],
            "customer_name": ["Arjun", "Priya", "Kiran"],
        }
    )

    write_dataframe_to_table(connection, orders, "orders")
    write_dataframe_to_table(connection, customers, "customers")

    result = get_orders_per_customer(connection)

    assert result == [
        ("Arjun", 2),
        ("Priya", 1),
        ("Kiran", 0),
    ]

    connection.close()

def test_get_revenue_by_city(tmp_path):
    database_path = tmp_path / "test.db"
    connection = create_connection(database_path)

    orders = pd.DataFrame(
        {
            "customer_id": [1, 1, 2],
            "quantity": [1, 2, 3],
            "price": [1000, 500, 200],
        }
    )

    customers = pd.DataFrame(
        {
            "customer_id": [1, 2],
            "city": ["Kochi", "Pune"],
        }
    )

    write_dataframe_to_table(connection, orders, "orders")
    write_dataframe_to_table(connection, customers, "customers")

    result = get_revenue_by_city(connection)

    assert result == [
        ("Kochi", 2000),
        ("Pune", 600),
    ]

    connection.close()
