import pytest
from src.data_loader.loader import count_lines


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