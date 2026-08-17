import pandas as pd

from src.data_loader.profiler import (
    get_shape,
    get_columns,
    get_missing_values,
    get_missing_percentages,
    get_unique_counts,
    get_duplicate_count,
    get_data_types,
    get_numeric_summary,
    get_categorical_summary,
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

def test_get_missing_percentages():
    data = pd.DataFrame(
        {
            "order_id": [1, 2, 3, 4],
            "product": ["Laptop", "Mouse", None, None],
            "price": [50000, 1000, 2000, 3000],
        }
    )

    result = get_missing_percentages(data)

    assert result["order_id"] == 0.0
    assert result["product"] == 50.0
    assert result["price"] == 0.0

def test_get_unique_counts():
    data = pd.DataFrame(
        {
            "product": ["Laptop", "Mouse", "Mouse", "Laptop"],
            "payment_method": ["Card", "UPI", "Card", "Card"],
        }
    )

    result = get_unique_counts(data)

    assert result["product"] == 2
    assert result["payment_method"] == 2

def test_get_numeric_summary():
    data = pd.DataFrame(
        {
            "order_id": [1001, 1002, 1003],
            "customer_id": [1, 2, 3],
            "quantity": [1, 2, 3],
            "price": [1000, 2000, 3000],
        }
    )

    result = get_numeric_summary(data)

    assert "order_id" not in result
    assert "customer_id" not in result

    assert result["quantity"]["min"] == 1.0
    assert result["quantity"]["max"] == 3.0
    assert result["price"]["mean"] == 2000.0

def test_get_categorical_summary():
    data = pd.DataFrame(
        {
            "product": ["Laptop", "Mouse", "Mouse", "Laptop"],
            "payment_method": ["Card", "UPI", "Card", "Card"],
        }
    )

    result = get_categorical_summary(data)

    assert result["product"] == {
        "Laptop": 2,
        "Mouse": 2,
    }

    assert result["payment_method"] == {
        "Card": 3,
        "UPI": 1,
    }

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
    assert "missing_percentages" in result
    assert "unique_counts" in result
    assert "numeric_summary" in result
    assert "categorical_summary" in result
