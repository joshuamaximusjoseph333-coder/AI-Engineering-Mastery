# Day 14 — CLI Data Profiler

## What I Built

Today I turned the Engineering Workbench into a usable command-line application.

I added a CLI using Python's built-in `argparse` module.

The CLI now supports:

- `profile` subcommand
- `database` subcommand
- profiling different CSV files through a positional path argument
- selecting one profile section using `--section`
- rejecting invalid section values using `choices`
- installed console command `engineering-workbench`

Example commands:

```powershell
engineering-workbench profile data/raw/orders_week2.csv
engineering-workbench profile data/raw/orders_week2.csv --section shape
engineering-workbench profile data/raw/customers_week2.csv
engineering-workbench database