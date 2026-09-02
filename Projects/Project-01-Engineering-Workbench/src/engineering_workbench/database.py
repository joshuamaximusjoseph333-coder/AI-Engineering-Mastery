import sqlite3
from pathlib import Path

import pandas as pd


def create_connection(database_path: Path) -> sqlite3.Connection:
    return sqlite3.connect(database_path)

def create_orders_table(connection: sqlite3.Connection) -> None:
    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            order_date TEXT NOT NULL,
            payment_method TEXT NOT NULL
        )
        """
    )

    connection.commit()

def write_dataframe_to_table(
    connection: sqlite3.Connection,
    data: pd.DataFrame,
    table_name: str,
) -> None:
    data.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False,
    )    

def get_all_orders(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT *
        FROM orders;
        """
    )

    return result.fetchall()

def get_expensive_orders(
    connection: sqlite3.Connection,
    minimum_price: float,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT product, price
        FROM orders
        WHERE price > ?
        ORDER BY price DESC;
        """,
        (minimum_price,),
    )

    return result.fetchall()    

def get_payment_method_counts(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT payment_method, COUNT(*) AS order_count
        FROM orders
        GROUP BY payment_method
        ORDER BY order_count DESC;
        """
    )

    return result.fetchall()

def get_product_quantity_totals(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT product, SUM(quantity) AS total_quantity
        FROM orders
        GROUP BY product
        ORDER BY total_quantity DESC;
        """
    )

    return result.fetchall()

def get_customer_order_details(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT
            orders.order_id,
            customers.customer_name,
            customers.city,
            orders.product,
            orders.quantity,
            orders.price
        FROM orders
        INNER JOIN customers
            ON orders.customer_id = customers.customer_id
        ORDER BY orders.order_id;
        """
    )

    return result.fetchall()

def get_all_customers_with_orders(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT
            customers.customer_id,
            customers.customer_name,
            customers.city,
            orders.order_id,
            orders.product
        FROM customers
        LEFT JOIN orders
            ON customers.customer_id = orders.customer_id
        ORDER BY customers.customer_id;
        """
    )

    return result.fetchall()

def get_customers_without_orders(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT
            customers.customer_id,
            customers.customer_name,
            customers.city
        FROM customers
        LEFT JOIN orders
            ON customers.customer_id = orders.customer_id
        WHERE orders.order_id IS NULL
        ORDER BY customers.customer_id;
        """
    )

    return result.fetchall()

def get_orders_per_customer(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT
            customers.customer_name,
            COUNT(orders.order_id) AS order_count
        FROM customers
        LEFT JOIN orders
            ON customers.customer_id = orders.customer_id
        GROUP BY
            customers.customer_id,
            customers.customer_name
        ORDER BY order_count DESC;
        """
    )

    return result.fetchall()

def get_revenue_by_city(
    connection: sqlite3.Connection,
) -> list[tuple]:
    result = connection.execute(
        """
        SELECT
            customers.city,
            SUM(orders.quantity * orders.price) AS revenue
        FROM customers
        INNER JOIN orders
            ON customers.customer_id = orders.customer_id
        GROUP BY customers.city
        ORDER BY revenue DESC;
        """
    )

    return result.fetchall()
