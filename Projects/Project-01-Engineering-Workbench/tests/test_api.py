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

def test_database_analysis_returns_500_on_internal_failure(monkeypatch):
    def fail_database_analysis():
        raise RuntimeError("database failed")

    monkeypatch.setattr(
        "engineering_workbench.api.run_database_analysis",
        fail_database_analysis,
    )

    client = TestClient(
    app,
    raise_server_exceptions=False,
    )
    response = client.get("/database")
    assert response.status_code == 500

def test_profile_returns_404_when_dataset_file_is_missing(monkeypatch):
    def fail_profile(*args, **kwargs):
        raise FileNotFoundError("file missing")

    monkeypatch.setattr(
        "engineering_workbench.api.run_profile",
        fail_profile,
    )

    response = client.get(
        "/profile",
        params={"dataset": "orders"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Dataset 'orders' file not found",
    }    