import logging
from pathlib import Path

import pandas as pd


def count_lines(file_path: Path) -> int:
    logging.info("Reading file: %s", file_path)

    with file_path.open("r", encoding="utf-8") as file:
        line_count = len(file.readlines()) 

    return line_count

def load_csv(
    file_path: Path,
    parse_dates: list[str] | None = None,
) -> pd.DataFrame:
    logging.info("Loading CSV file: %s", file_path)

    try:
        return pd.read_csv(
            file_path,
            parse_dates=parse_dates,
        )

    except FileNotFoundError:
        logging.error("CSV file not found: %s", file_path)
        raise
