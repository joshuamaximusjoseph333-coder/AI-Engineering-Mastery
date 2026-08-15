import pandas as pd

from src.data_loader.profiler import (
    get_shape,
    get_columns,
    get_missing_values,
    get_duplicate_count,
    get_data_types,
    profile_data,
)

def test_get_shape():
    data = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "product": ["Laptop", "Mouse", "Keyboard"],
            "price": [50000, 1000, 2000],
        }
    )

    result = get_shape(data)

    assert result == (3, 3)

def test_get_columns():
    data = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "product": ["Laptop", "Mouse", "Keyboard"],
            "price": [50000, 1000, 2000],
        }
    )

    result = get_columns(data)

    assert result == ["order_id", "product", "price"]

def test_get_missing_values():
    data = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "product": ["Laptop", "Mouse", "Keyboard"],
            "price": [50000, None, 2000],
        }
    )

    result = get_missing_values(data)

    assert result == {
        "order_id": 0,
        "product": 0,
        "price": 1,
    }    

def test_get_duplicate_count():
    data = pd.DataFrame(
        {
            "order_id": [1, 2, 2, 3],
            "product": ["Laptop", "Mouse", "Mouse", "Keyboard"],
            "price": [50000, 1000, 1000, 2000],
        }
    )

    result = get_duplicate_count(data)

    assert result == 1

def test_get_data_types():
    data = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "product": ["Laptop", "Mouse", "Keyboard"],
            "price": [50000, 1000, 2000],
        }
    )

    result = get_data_types(data)

    assert result["order_id"].startswith("int")
    assert result["product"] in {"str", "object"}
    assert result["price"].startswith("int")

def test_profile_data():
    data = pd.DataFrame(
        {
            "order_id": [1, 2, 2, 3],
            "product": ["Laptop", "Mouse", "Mouse", "Keyboard"],
            "price": [50000, None, None, 2000],
        }
    )

    result = profile_data(data)

    assert result["shape"] == (4, 3)
    assert result["columns"] == ["order_id", "product", "price"]
    assert result["missing_values"]["price"] == 2
    assert result["duplicate_count"] == 1    

        