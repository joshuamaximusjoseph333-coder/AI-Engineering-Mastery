from typing import Literal

from fastapi import FastAPI

from engineering_workbench import (
    run_database_analysis,
    run_profile,
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

    return run_profile(data_path)

@app.get("/database")
def database_analysis():
    return run_database_analysis()