import pytest
from engineering_workbench.loader import count_lines, load_csv


def test_count_lines(tmp_path):
    file_path = tmp_path / "sample.txt"

    file_path.write_text(
    "apple\nbanana\norange\n",
    encoding="utf-8",
    )

    result = count_lines(file_path)

    assert result == 3

def test_count_lines_empty_file(tmp_path):
    file_path = tmp_path / "empty.txt"

    file_path.write_text("", encoding="utf-8")

    result = count_lines(file_path)

    assert result == 0    

def test_count_lines_missing_file(tmp_path):
    file_path = tmp_path / "does_not_exist.txt"

    with pytest.raises(FileNotFoundError):
        count_lines(file_path)    

def test_count_lines_one_line(tmp_path):
    file_path = tmp_path / "one_line.txt"

    file_path.write_text("hello\n", encoding="utf-8")

    result = count_lines(file_path)

    assert result == 1

def test_load_csv(tmp_path):
    file_path = tmp_path / "sample.csv"

    file_path.write_text(
        "order_id,product,price\n"
        "1,Laptop,50000\n"
        "2,Mouse,1000\n",
        encoding="utf-8",
    )

    data = load_csv(file_path)

    assert data.shape == (2, 3)
    assert data.columns.tolist() == ["order_id", "product", "price"]

def test_load_csv_missing_file(tmp_path):
    file_path = tmp_path / "missing.csv"

    with pytest.raises(FileNotFoundError):
        load_csv(file_path)
