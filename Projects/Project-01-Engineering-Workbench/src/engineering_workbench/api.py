from typing import Literal

from fastapi import FastAPI, HTTPException

from engineering_workbench import (
    run_database_analysis,
    run_profile,
    run_analysis
)

app = FastAPI()

DATASETS = {
    "orders": "data/raw/orders_week2.csv",
    "customers": "data/raw/customers_week2.csv",
}

@app.get("/")
def root():
    return {
        "message": "Engineering Workbench API",
    }


@app.get("/health")
def health():
    return {
        "status": "ok",
    }

@app.get("/profile")
def profile(dataset: Literal["orders", "customers"]):
    data_path = DATASETS[dataset]

    try:
        return run_profile(data_path)
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Dataset '{dataset}' file not found",
        )
@app.get("/analysis")
def analysis():
    results = run_analysis()

    return {
        "profile": results["profile"],
        "price_statistics": results["price_statistics"],
        "price_outliers": results["price_outliers"],
    }

@app.get("/database")
def database_analysis():
    return run_database_analysis()