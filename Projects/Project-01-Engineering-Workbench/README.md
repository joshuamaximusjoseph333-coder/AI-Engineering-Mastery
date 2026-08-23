# Engineering Workbench

A Python engineering project focused on building a reliable and maintainable data-processing application using modular design, automated testing, logging, validation, data profiling, and Docker.

## Project Objective

The goal of this project is to build an engineering workbench that can reliably ingest CSV datasets, validate their structure and values, analyze their basic characteristics, and produce a readable data profile.

The project is also used to practice software engineering principles such as:

- Modular Python architecture
- Separation of concerns
- Configuration management
- Operational logging
- Error handling and fail-fast validation
- Automated testing with pytest
- Data analysis with pandas
- Docker containerization
- Debugging and recovery workflows
- Git-based version control

## Current Application Flow

CSV Dataset
    ↓
Configuration
    ↓
Loader / Ingestion
    ↓
Pandas DataFrame
    ↓
Schema Validation
    ↓
Value Validation
    ↓
Profiler
    ↓
Profile Report

## Project Structure

```text
Project-01-Engineering-Workbench/
│
├── data/
│   ├── raw/
│   │   ├── orders_week2.csv
│   │   └── orders.csv
│   └── processed/
│
├── src/
│   └── data_loader/
│       ├── __init__.py
│       ├── config.py
│       ├── loader.py
│       ├── logger.py
│       ├── profiler.py
│       └── validator.py
│
├── tests/
│   ├── test_loader.py
│   ├── test_profiler.py
│   └── test_validator.py
│
├── .dockerignore
├── Dockerfile
├── main.py
├── README.md
└── requirements.txt
```

## Running the Project

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the application:

```bash
python main.py
```

Run the automated tests:

```bash
python -m pytest
```

## Running with Docker

Build the Docker image:

```bash
docker build -t engineering-workbench .
```

Run the application:

```bash
docker run --rm engineering-workbench
```

Run the test suite inside Docker:

```bash
docker run --rm engineering-workbench python -m pytest
```

---

## Current Progress

### Day 2

* Created a project-specific Python virtual environment.
* Structured the application using packages and modules.
* Created reusable file-loading logic.
* Added type hints using `Path` and `int`.
* Centralized the raw-data path in `config.py`.
* Added application logging.
* Successfully loaded and counted lines from a raw CSV file.

### Day 3

#### Testing

The project uses pytest for automated testing.

The test suite currently verifies:

* Counting lines in a normal file
* Handling an empty file
* Raising `FileNotFoundError` for a missing file
* Counting a single-line file

Run the tests locally with:

```bash
python -m pytest
```

### Day 4

#### Docker Containerization

The project was containerized using Docker so that the application can run in a consistent Linux-based environment without depending on the local Windows Python environment.

The Docker setup includes:

* A `Dockerfile` for defining how the project image is built
* Python 3.13 Slim as the base image
* `/app` as the working directory inside the image
* Installation of Python dependencies from `requirements.txt`
* Project files copied into the Docker image
* A default command to run `main.py` when the container starts
* A `.dockerignore` file to exclude unnecessary local files such as `.venv`
* Support for running the pytest test suite inside Docker

Build the Docker image with:

```bash
docker build -t engineering-workbench .
```

Run the application inside a temporary container with:

```bash
docker run --rm engineering-workbench
```

Run the automated tests inside Docker with:

```bash
docker run --rm engineering-workbench python -m pytest
```

The application was successfully executed inside the Docker container and produced the expected result.

The complete pytest test suite was also executed inside the Linux container:

```text
4 passed
```

This confirms that the project and its automated tests can run successfully both in the local development environment and inside Docker.

### Day 5

#### Data Profiler Architecture

Implemented a reusable data profiling pipeline using pandas.

The application now:

- Loads CSV datasets into pandas DataFrames.
- Reports dataset shape (rows and columns).
- Reports column names.
- Detects missing values per column.
- Detects duplicate rows.
- Reports column data types.
- Combines individual profiling operations into a complete profile report.
- Separates data loading and data profiling responsibilities.

The profiler architecture follows this flow:

```text
CSV Dataset
    ↓
Loader
    ↓
DataFrame
    ↓
Profiler
    ↓
Profile Report
```
### Day 6

#### Data Validation

Added a validation layer in `validator.py` to ensure that order datasets contain the required columns:

- `order_id`
- `product`
- `price`

The validator uses fail-fast validation. If required columns are missing, the application raises a clear `ValueError` before profiling continues.

The application flow is now:

CSV Dataset
    ↓
Loader
    ↓
DataFrame
    ↓
Validator
    ↓
Profiler
    ↓
Profile Report

#### Operational Logging

Improved the CSV loader with operational error logging.

The loader records an INFO log before attempting to load a dataset:

`INFO | Loading CSV file: ...`

If the file does not exist, it records an ERROR log:

`ERROR | CSV file not found: ...`

The loader uses `try` / `except` to catch `FileNotFoundError`, log the failure, and then uses `raise` to re-raise the original exception.

This ensures that the failure is recorded without hiding it or allowing the application to continue with invalid data.

#### Automated Testing

Added tests for the new validation layer:

- Valid datasets containing all required columns
- Invalid datasets with missing required columns
- Expected exceptions using `pytest.raises()`

The complete test suite now contains:

- 6 loader tests
- 6 profiler tests
- 2 validator tests
- 14 tests total

All 14 tests pass locally and inside Docker.

#### Debugging and Recovery

Practiced diagnosing several types of failures:

- Missing file → `FileNotFoundError`
- Missing DataFrame column → `KeyError`
- Invalid dataset schema → `ValueError`
- Incorrect program output → pytest assertion failure
- Regression caused by breaking previously working profiler logic

Practiced the complete recovery workflow:

Break
    ↓
Observe
    ↓
Diagnose
    ↓
Recover
    ↓
Verify application
    ↓
Verify pytest
    ↓
Verify Docker

#### Output Readability

Improved profile output using:

`for key, value in profile.items():`

This prints each profiler result on a separate line instead of displaying the entire profile dictionary on one line.

### Day 7

#### Real CSV Ingestion

Expanded the project from basic CSV loading into a more configurable ingestion workflow.

The CSV loader now supports optional date parsing:

```python
def load_csv(
    file_path: Path,
    parse_dates: list[str] | None = None,
) -> pd.DataFrame:
```

This allows source-specific ingestion requirements to be supplied by the caller instead of hard-coding them into the reusable loader.

For the Week 2 orders dataset, `order_date` is parsed as a datetime during ingestion.

#### Week 2 Orders Dataset

Added `orders_week2.csv` with the following schema:

- `order_id`
- `customer_id`
- `product`
- `quantity`
- `price`
- `order_date`
- `payment_method`

This dataset provides a richer foundation for Week 2 data investigation, relational analysis, SQL, and statistics.

#### Data Contract

Expanded the orders data contract from the original three-column Week 1 schema to the complete Week 2 schema.

The application now expects all seven order columns to be present.

Basic value rules were also introduced:

- `order_id` must not be missing and must be unique.
- `customer_id` must not be missing.
- `product` must not be missing.
- `quantity` must be greater than zero.
- `price` must be greater than zero.
- `order_date` must not be missing.
- `payment_method` must not be missing.

#### Schema and Value Validation

Validation is now separated into two responsibilities:

```text
validate_required_columns()
→ verifies required structure

validate_order_values()
→ verifies basic value rules
```

The application performs schema validation before value validation so that value checks only access columns after their existence has been confirmed.

The pipeline now follows:

```text
Raw CSV
    ↓
Ingestion
    ↓
Pandas DataFrame
    ↓
Schema Validation
    ↓
Value Validation
    ↓
Data Profiling
    ↓
Profile Report
```

#### Ingestion Investigation

Explored important real-world CSV ingestion behavior, including:

- Missing-value interpretation
- Explicit data types
- Date parsing
- Alternative delimiters
- File encodings
- Malformed rows
- Column selection
- Sampling rows
- Chunked ingestion
- Metadata and skipped rows
- Headerless files
- Default NA handling
- Comment lines

These investigations were used to understand why successful file loading does not necessarily mean that the source data was interpreted correctly.

#### Testing

Updated the existing validator tests to reflect the new Week 2 data contract.

Added tests for value-validation behavior, including:

- Accepting valid order data
- Rejecting invalid quantities
- Rejecting duplicate order IDs

The complete application and test suite were verified both locally and inside Docker.

#### Day 7 Engineering Outcome

By the end of Day 7, Project 01 had progressed from:

```text
Load CSV
    ↓
Profile data
```

to:

```text
Understand source requirements
    ↓
Configure ingestion
    ↓
Load CSV
    ↓
Validate schema
    ↓
Validate values
    ↓
Profile data
```

This establishes the ingestion and validation foundation for the remaining Week 2 data investigation work.

### Day 8

#### Data-Quality Profiler

Expanded the existing basic profiler into a richer data-quality profiling system.

The profiler now reports:

- Dataset shape
- Column names
- Data types
- Missing-value counts
- Missing-value percentages
- Unique-value counts
- Duplicate-row count
- Numeric statistical summaries
- Categorical value frequencies

The profiler remains modular, with individual functions responsible for specific profiling operations and `profile_data()` combining them into a complete profile.

#### Missing-Value Analysis

Added missing-value percentages in addition to the existing missing-value counts.

This makes it possible to understand not only how many values are missing, but also how significant the missing data is relative to the size of the dataset.

The profiler uses:

```python
data.isna().mean().mul(100).round(2)
```

to calculate the percentage of missing values in each column.

#### Unique-Value Analysis

Added unique-value counts using:

```python
data.nunique()
```

This provides information about the cardinality of each column and helps distinguish characteristics such as unique identifiers and low-cardinality categorical fields.

#### Numeric Profiling

Added statistical summaries for meaningful numeric columns using pandas `describe()`.

The numeric profile includes:

- Count
- Mean
- Standard deviation
- Minimum
- 25th percentile
- Median / 50th percentile
- 75th percentile
- Maximum

Identifier columns such as `order_id` and `customer_id` are excluded from the numeric statistical summary because a numeric data type does not necessarily imply meaningful numeric analysis.

The current numeric analysis therefore focuses on measurements such as:

- `quantity`
- `price`

#### Categorical Profiling

Added categorical value-frequency analysis for text-based columns.

The profiler uses:

```python
value_counts()
```

to report how frequently each category occurs.

For the Week 2 orders dataset, this provides frequency information for fields such as:

- `product`
- `payment_method`

#### Validator and Profiler Responsibilities

The project maintains a separation between validation and profiling:

```text
Validator
→ enforces required data rules
→ may reject invalid data

Profiler
→ measures and describes data characteristics
→ produces information for investigation
```

The application pipeline remains:

```text
Raw CSV
    ↓
Configuration
    ↓
Configurable Ingestion
    ↓
Pandas DataFrame
    ↓
Schema Validation
    ↓
Value Validation
    ↓
Data-Quality Profiling
    ↓
Profile Report
```

#### Automated Testing

Expanded the profiler test suite to cover the new Day 8 functionality.

New tests verify:

- Missing-value percentage calculations
- Unique-value counts
- Numeric statistical summaries
- Exclusion of identifier columns from numeric analysis
- Categorical value frequencies
- Integration of the new metrics into `profile_data()`

The complete test suite was successfully verified both locally and inside Docker.

#### Day 8 Engineering Outcome

The profiler evolved from a basic structural summary:

```text
Shape
Columns
Missing counts
Duplicate rows
Data types
```

into a more complete data-quality profile:

```text
Dataset Structure
    ↓
Completeness Analysis
    ↓
Uniqueness Analysis
    ↓
Data-Type Analysis
    ↓
Numeric Analysis
    ↓
Categorical Analysis
    ↓
Complete Data-Quality Profile
```

This provides the data investigation foundation needed for the upcoming SQL and statistical analysis stages of Project 01.

### Day 9

#### SQL Foundations and SQLite Integration

Added relational database functionality to the Engineering Workbench using Python's built-in SQLite support.

The application now:

- Connects to an SQLite database.
- Creates an `orders` table with a defined schema.
- Transfers pandas DataFrames into SQLite.
- Executes SQL queries from Python.
- Retrieves SQL query results back into Python.
- Uses parameterized queries for dynamic values.
- Performs filtering, sorting, grouping, and aggregation with SQL.

#### SQL Concepts Implemented

Practiced and implemented:

- `SELECT` and `FROM`
- `WHERE`
- `AND`, `OR`, and `NOT`
- `ORDER BY`
- `LIMIT`
- `DISTINCT`
- `COUNT()`
- `SUM()`
- `AVG()`
- `MIN()` and `MAX()`
- `GROUP BY`
- `HAVING`
- SQL aliases with `AS`
- `CREATE TABLE`
- Primary keys and `NOT NULL` constraints
- Parameterized SQL queries

#### Database Layer

Added:

```text
src/data_loader/database.py
```

The database layer contains reusable functions for:

```text
Database connection
DataFrame → SQLite persistence
Table creation
Retrieving orders
Filtering expensive orders
Counting orders by payment method
Aggregating quantities by product
```

The application architecture now includes:

```text
CSV Dataset
    ↓
Loader
    ↓
Pandas DataFrame
    ↓
Validator
    ↓
Profiler
    ↓
SQLite Database
    ↓
SQL Queries
    ↓
Analysis Results
```

#### Database Testing

Added:

```text
tests/test_database.py
```

Database tests use pytest's `tmp_path` to create isolated temporary SQLite databases instead of modifying the real application database.

The tests verify:

- Database connection
- SQL table creation
- DataFrame-to-SQL persistence
- SQL filtering and sorting
- `GROUP BY` with `COUNT()`
- `GROUP BY` with `SUM()`

The application and complete automated test suite were successfully verified both locally and inside Docker.

### Day 10

#### Relational Modelling and SQL Analysis

Extended the Engineering Workbench from single-table SQL analysis to a relational database model using multiple related datasets.

Added a second dataset:

```text
data/raw/customers_week2.csv
```

The application now works with two related entities:

```text
customers
├── customer_id
├── customer_name
└── city

orders
├── order_id
├── customer_id
├── product
├── quantity
├── price
├── order_date
└── payment_method
```

The tables are logically related through `customer_id`, creating a one-to-many relationship:

```text
customers                          orders

customer_id  ──────────────────── customer_id
     1                                  many
```

One customer can therefore be associated with multiple orders.

#### Relational SQL

Implemented relational SQL queries using:

- `INNER JOIN`
- `LEFT JOIN`
- Join conditions with `ON`
- Qualified column names such as `customers.customer_id`
- `NULL` and `IS NULL`
- `JOIN` with `GROUP BY`
- `COUNT(column)` for non-NULL values
- Multi-table aggregation using `SUM()`

The application can now:

- Combine customer and order information.
- Preserve customers who do not have matching orders.
- Identify customers who have never placed an order.
- Calculate the number of orders placed by each customer.
- Calculate total revenue generated by each city.
- Rank aggregated SQL results.

Example relational flow:

```text
orders_week2.csv              customers_week2.csv
       ↓                              ↓
orders DataFrame               customers DataFrame
       ↓                              ↓
orders table                   customers table
       │                              │
       └─────── customer_id ──────────┘
                      ↓
                 SQL JOIN
                      ↓
             Relational Analysis
                      ↓
          GROUP BY / COUNT / SUM
```

#### INNER JOIN and LEFT JOIN

`INNER JOIN` is used when only matching records from both tables are required.

`LEFT JOIN` is used when every record from the left table must be preserved, including records without a match.

A customer with no orders was included in the customer dataset to verify this behavior.

The application can identify unmatched customers using the pattern:

```sql
LEFT JOIN orders
    ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL
```

#### Relational Analysis Functions

Expanded `database.py` with reusable relational analysis functions for:

```text
Customer and order details
All customers with their orders
Customers without orders
Orders per customer
Revenue by city
```

This keeps SQL logic inside the database layer while `main.py` coordinates the overall application workflow.

#### Database Testing

Extended `tests/test_database.py` with automated tests for the Day 10 relational functionality.

The tests verify:

- `INNER JOIN` behavior
- `LEFT JOIN` behavior
- Preservation of customers without orders
- Detection of customers with no matching orders
- `LEFT JOIN + GROUP BY + COUNT`
- Correct zero-order counts using `COUNT(orders.order_id)`
- Multi-table revenue aggregation using `JOIN + GROUP BY + SUM`

Temporary SQLite databases are created using pytest's `tmp_path`, keeping tests isolated from the real application database.

#### Current Database Architecture

The application now follows:

```text
Raw CSV Data
     ↓
Pandas DataFrames
     ↓
Validation + Profiling
     ↓
SQLite Persistence
     ↓
┌──────────────────────────┐
│ customers       orders   │
│     │              │     │
│     └─ customer_id ┘     │
└──────────────────────────┘
     ↓
Relational SQL Queries
     ↓
Business Analysis Results
```

The complete application and automated test suite were successfully verified both locally and inside Docker.

> Note: The current `customer_id` primary-key/foreign-key relationship is a logical relational model used by the SQL queries. Because the current pandas persistence layer uses `to_sql(..., if_exists="replace")`, SQLite is not yet enforcing the relationship as an actual foreign-key constraint.