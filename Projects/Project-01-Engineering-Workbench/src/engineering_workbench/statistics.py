import pandas as pd


def get_descriptive_statistics(
    data: pd.DataFrame,
    column: str,
) -> dict:
    series = data[column]

    skewness = float(series.skew())


    return {
        "mean": float(series.mean()),
        "median": float(series.median()),
        "mode": series.mode().tolist(),
        "minimum": float(series.min()),
        "maximum": float(series.max()),
        "range": float(series.max() - series.min()),
        "variance": float(series.var()),
        "standard_deviation": float(series.std()),
        "q1": float(series.quantile(0.25)),
        "q3": float(series.quantile(0.75)),
        "skewness": float(series.skew()),
        "skewness_direction": get_skewness_direction(skewness),
    }

def get_outliers(
    data: pd.DataFrame,
    column: str,
) -> dict:
    series = data[column]

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)

    iqr = q3 - q1

    lower_bound = q1 - (1.5 * iqr)
    upper_bound = q3 + (1.5 * iqr)

    outliers = series[
        (series < lower_bound) | (series > upper_bound)
    ]

    return {
        "q1": float(q1),
        "q3": float(q3),
        "iqr": float(iqr),
        "lower_bound": float(lower_bound),
        "upper_bound": float(upper_bound),
        "outliers": outliers.tolist(),
    }

def get_skewness_direction(skewness: float) -> str:
    if skewness > 0:
        return "right-skewed"

    if skewness < 0:
        return "left-skewed"

    return "symmetric"
