import pandas as pd

from src.data_loader.database import (
    create_connection,
    create_orders_table,
    get_all_orders,
    get_expensive_orders,
    get_payment_method_counts,
    get_product_quantity_totals,
    write_dataframe_to_table,
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