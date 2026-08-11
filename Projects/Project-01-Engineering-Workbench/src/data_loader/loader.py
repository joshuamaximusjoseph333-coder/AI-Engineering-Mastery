import logging
from pathlib import Path

import pandas as pd


def count_lines(file_path: Path) -> int:
    logging.info("Reading file: %s", file_path)

    with file_path.open("r", encoding="utf-8") as file:
        line_count = len(file.readlines()) 

    return line_count

def load_csv(file_path: Path) -> pd.DataFrame:
    logging.info(f"Loading CSV file: {file_path}")

    return pd.read_csv(file_path)