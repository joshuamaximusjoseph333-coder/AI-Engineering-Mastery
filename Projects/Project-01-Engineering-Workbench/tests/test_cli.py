import pytest

from engineering_workbench.cli import main


def test_profile_section_output(capsys):
    main([
        "profile",
        "data/raw/orders_week2.csv",
        "--section",
        "shape",
    ])

    captured = capsys.readouterr()

    assert "shape: (10, 7)" in captured.out


def test_profile_customers_shape(capsys):
    main([
        "profile",
        "data/raw/customers_week2.csv",
        "--section",
        "shape",
    ])

    captured = capsys.readouterr()

    assert "shape: (6, 3)" in captured.out


def test_invalid_profile_section():
    with pytest.raises(SystemExit):
        main([
            "profile",
            "data/raw/orders_week2.csv",
            "--section",
            "banana",
        ])

def test_analysis_command(capsys):
    main(["analysis"])

    captured = capsys.readouterr()

    assert "=== Price Statistics ===" in captured.out
    assert "mean:" in captured.out
    assert "median:" in captured.out
    assert "skewness:" in captured.out
    assert "skewness_direction:" in captured.out
    assert "=== Price Outliers ===" in captured.out        