import pandas as pd

from src.data_loader.statistics import (
    get_descriptive_statistics,
    get_outliers,
    get_skewness_direction,
)

def test_get_descriptive_statistics():
    data = pd.DataFrame(
        {
            "price": [10, 20, 30],
        }
    )

    result = get_descriptive_statistics(
        data,
        "price",
    )

    assert result["mean"] == 20.0
    assert result["median"] == 20.0
    assert result["mode"] == [10, 20, 30]
    assert result["minimum"] == 10.0
    assert result["maximum"] == 30.0
    assert result["range"] == 20.0
    assert result["q1"] == 15.0
    assert result["q3"] == 25.0

def test_get_skewness_direction():
    assert get_skewness_direction(1.5) == "right-skewed"
    assert get_skewness_direction(-1.5) == "left-skewed"
    assert get_skewness_direction(0.0) == "symmetric"

def test_get_outliers():
    data = pd.DataFrame(
        {
            "price": [10, 10, 10, 10, 100],
        }
    )

    result = get_outliers(
        data,
        "price",
    )

    assert result["outliers"] == [100]    