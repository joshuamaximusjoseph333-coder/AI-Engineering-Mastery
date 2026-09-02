import pandas as pd

REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "product",
    "quantity",
    "price",
    "order_date",
    "payment_method",
}


def validate_required_columns(data: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

def validate_order_values(data: pd.DataFrame) -> None:
    if data["order_id"].isna().any():
        raise ValueError("order_id contains missing values")

    if data["order_id"].duplicated().any():
        raise ValueError("order_id contains duplicate values")

    if data["customer_id"].isna().any():
        raise ValueError("customer_id contains missing values")

    if data["product"].isna().any():
        raise ValueError("product contains missing values")

    if (data["quantity"] <= 0).any():
        raise ValueError("quantity must be greater than 0")

    if (data["price"] <= 0).any():
        raise ValueError("price must be greater than 0")

    if data["order_date"].isna().any():
        raise ValueError("order_date contains missing values")

    if data["payment_method"].isna().any():
        raise ValueError("payment_method contains missing values")
