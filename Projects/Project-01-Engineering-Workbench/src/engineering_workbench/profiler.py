import pandas as pd


def get_shape(data: pd.DataFrame) -> tuple[int, int]:
    return data.shape

def get_columns(data: pd.DataFrame) -> list[str]:
    return data.columns.tolist()

def get_missing_values(data: pd.DataFrame) -> dict[str, int]:
    return data.isna().sum().to_dict()

def get_missing_percentages(data: pd.DataFrame) -> dict[str, float]:
    return (
        data.isna().mean().mul(100).round(2).to_dict()
    )

def get_unique_counts(data: pd.DataFrame) -> dict[str, int]:
    return data.nunique().to_dict()

def get_duplicate_count(data: pd.DataFrame) -> int:
    return int(data.duplicated().sum())

def get_data_types(data: pd.DataFrame) -> dict[str, str]:
    return {column: str(dtype) for column, dtype in data.dtypes.items()}

def get_numeric_summary(data: pd.DataFrame) -> dict:
    numeric_data = data.select_dtypes(include="number")

    identifier_columns = ["order_id", "customer_id"]

    numeric_data = numeric_data.drop(
        columns=identifier_columns,
        errors="ignore",
    )

    return numeric_data.describe().to_dict()

def get_categorical_summary(data: pd.DataFrame) -> dict:
    categorical_data = data.select_dtypes(include=["object", "string"])

    return {
        column: categorical_data[column].value_counts().to_dict()
        for column in categorical_data.columns
    }

def profile_data(data: pd.DataFrame) -> dict:
    return {
        "shape": get_shape(data),
        "columns": get_columns(data),
        "missing_values": get_missing_values(data),
        "missing_percentages": get_missing_percentages(data),
        "unique_counts": get_unique_counts(data),
        "duplicate_count": get_duplicate_count(data),
        "data_types": get_data_types(data),
        "numeric_summary": get_numeric_summary(data),
        "categorical_summary": get_categorical_summary(data),
    }
