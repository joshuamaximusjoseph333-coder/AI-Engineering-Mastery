import logging
from pathlib import Path


def count_lines(file_path: Path) -> int:
    logging.info("Reading file: %s", file_path)

    with file_path.open("r", encoding="utf-8") as file:
        line_count = len(file.readlines())

    return line_count