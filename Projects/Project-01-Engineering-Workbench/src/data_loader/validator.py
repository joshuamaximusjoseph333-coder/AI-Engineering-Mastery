import pandas as pd

REQUIRED_COLUMNS = {"order_id", "product", "price"}


def validate_required_columns(data: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )