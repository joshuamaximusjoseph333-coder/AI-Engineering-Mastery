import pandas as pd
import pytest

from src.data_loader.validator import validate_required_columns

def test_validate_required_columns_passes():
    data = pd.DataFrame(
        {
            "order_id": [1, 2],
            "product": ["Laptop", "Mouse"],
            "price": [50000, 1000],
        }
    )

    validate_required_columns(data)

def test_validate_required_columns_raises_for_missing_column():
    data = pd.DataFrame(
        {
            "order_id": [1, 2],
            "product": ["Laptop", "Mouse"],
        }
    )

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_required_columns(data)