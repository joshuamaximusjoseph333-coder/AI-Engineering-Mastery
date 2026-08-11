import pandas as pd


def get_shape(data: pd.DataFrame) -> tuple[int, int]:
    return data.shape

def get_columns(data: pd.DataFrame) -> list[str]:
    return data.columns.tolist()

def get_missing_values(data: pd.DataFrame) -> dict[str, int]:
    return data.isna().sum().to_dict()

def get_duplicate_count(data: pd.DataFrame) -> int:
    return int(data.duplicated().sum())

def get_data_types(data: pd.DataFrame) -> dict[str, str]:
    return {column: str(dtype) for column, dtype in data.dtypes.items()}

def profile_data(data: pd.DataFrame) -> dict:
    return {
        "shape": get_shape(data),
        "columns": get_columns(data),
        "missing_values": get_missing_values(data),
        "duplicate_count": get_duplicate_count(data),
        "data_types": get_data_types(data),
    }