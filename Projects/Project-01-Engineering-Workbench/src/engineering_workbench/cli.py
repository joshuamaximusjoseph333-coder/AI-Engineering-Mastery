import argparse

from engineering_workbench import (
    run_analysis,
    run_database_analysis,
    run_profile,
)


def handle_profile(args):
    profile = run_profile(args.path)

    print("\n=== Data Profile ===")

    if args.section:
        print(f"{args.section}: {profile[args.section]}")
    else:
        for key, value in profile.items():
            print(f"{key}: {value}")


def handle_database():
    analysis_results = run_analysis()

    database_results = run_database_analysis(
        analysis_results["orders"]
    )

    print("\n=== Database Analysis ===")

    for key, value in database_results.items():
        print(f"\n{key}:")

        for row in value:
            print(row)


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="engineering-workbench",
        description="Analyze and profile Engineering Workbench data.",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    profile_parser = subparsers.add_parser(
        "profile",
        help="Profile the orders dataset.",
    )

    profile_parser.add_argument(
    "path",
    help="Path to the CSV file to profile.",
)

    profile_parser.add_argument(
        "--section",
        choices=[
            "shape",
            "columns",
            "missing_values",
            "missing_percentages",
            "unique_counts",
            "duplicate_count",
            "data_types",
            "numeric_summary",
            "categorical_summary",
        ],
        help="Display only one section of the data profile.",
    )

    subparsers.add_parser(
        "database",
        help="Run database analysis.",
    )

    args = parser.parse_args(argv)
    if args.command == "profile":
        handle_profile(args)

    if args.command == "database":
        handle_database()


if __name__ == "__main__":
    main()