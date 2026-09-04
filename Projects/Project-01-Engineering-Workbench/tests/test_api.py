from fastapi.testclient import TestClient

from engineering_workbench.api import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Engineering Workbench API",
    }


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
    }

def test_profile_orders():
    response = client.get(
        "/profile",
        params={"dataset": "orders"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["shape"] == [10, 7]
    assert "columns" in data
    assert "numeric_summary" in data
    assert "categorical_summary" in data

def test_profile_invalid_dataset():
    response = client.get(
        "/profile",
        params={"dataset": "banana"},
    )

    assert response.status_code == 422

def test_profile_customers():
    response = client.get(
        "/profile",
        params={"dataset": "customers"},
    )

    assert response.status_code == 200

    data = response.json()

    assert "shape" in data
    assert "columns" in data
    assert "missing_values" in data

def test_database_analysis():
    response = client.get("/database")

    assert response.status_code == 200

    data = response.json()

    assert "expensive_orders" in data
    assert "payment_counts" in data
    assert "product_totals" in data
    assert "revenue_by_city" in data    
