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

### Day 11

#### Descriptive Statistics and Statistical Analysis

Extended the Engineering Workbench with a dedicated statistical analysis layer for investigating numerical data beyond the basic summaries already provided by the data profiler.

Added:

```text
src/data_loader/statistics.py
```

The application can now perform dedicated descriptive statistical analysis on numerical DataFrame columns.

The Day 11 statistical workflow is:

```text
orders_week2.csv
       ↓
Pandas DataFrame
       ↓
Validation
       ↓
Data Profiling
       ↓
Descriptive Statistics
       │
       ├── Central Tendency
       ├── Spread
       ├── Quartiles
       ├── Distribution / Skewness
       └── Outlier Detection
       ↓
Statistical Interpretation
```

#### Descriptive Statistics

Implemented reusable statistical analysis for numerical columns including:

- Mean
- Median
- Mode
- Minimum
- Maximum
- Range
- Variance
- Standard deviation
- First quartile (Q1)
- Third quartile (Q3)
- Skewness

The statistical functions accept a DataFrame and column name, allowing the same analysis logic to be reused for different numerical variables.

Example:

```python
get_descriptive_statistics(
    orders,
    "price",
)
```

This selects the `price` Series from the orders DataFrame and calculates its descriptive statistics.

#### Distribution and Skewness

Added skewness analysis to measure the asymmetry of a numerical distribution.

Pandas calculates skewness using:

```python
series.skew()
```

The application also converts the numerical skewness result into a human-readable direction:

```text
Positive skewness → right-skewed
Negative skewness → left-skewed
Zero             → symmetric
```

For the current order-price dataset:

```text
Mean       = 14,200
Median     = 3,000
Skewness   ≈ 1.486
Direction  = right-skewed
```

The mean is substantially larger than the median because higher-priced observations pull the arithmetic mean upward.

The positive skewness value supports the interpretation that the price distribution is right-skewed.

#### IQR Outlier Detection

Implemented reusable outlier detection using the Interquartile Range (IQR) method.

The analysis calculates:

```text
IQR = Q3 - Q1

Lower Bound = Q1 - 1.5 × IQR
Upper Bound = Q3 + 1.5 × IQR
```

Values outside these boundaries are identified using Pandas boolean filtering:

```python
outliers = series[
    (series < lower_bound) | (series > upper_bound)
]
```

For the current price dataset:

```text
Q1          = 2,000
Q3          = 15,000
IQR         = 13,000
Lower Bound = -17,500
Upper Bound = 34,500

Potential Outliers:
50,000
50,000
```

The ₹50,000 observations are therefore statistical outliers according to the IQR rule.

However, statistical outliers are not automatically treated as invalid data. These observations represent plausible expensive products such as laptops, so they should be investigated in context rather than automatically removed.

The engineering workflow is:

```text
Detect
   ↓
Investigate
   ↓
Validate Against Context
   ↓
Keep / Correct / Remove
```

#### Statistical Interpretation

Day 11 extends the project beyond simply calculating statistics.

The application results can now be interpreted together:

```text
Mean                 = 14,200
Median               = 3,000
Standard Deviation   ≈ 19,611.79
Skewness             ≈ 1.486
Skew Direction       = right-skewed
IQR Outliers         = [50,000, 50,000]
```

These results indicate that:

- Order prices have substantial variation.
- Higher-priced observations pull the mean well above the median.
- The price distribution is positively/right skewed.
- ₹50,000 observations are unusually high according to the IQR rule.
- Statistical unusualness does not necessarily indicate incorrect data.

This separates statistical calculation from statistical interpretation.

#### Profiler vs Statistical Analysis

The existing `profiler.py` continues to provide a broad overview of the dataset:

```text
Shape
Columns
Missing values
Missing percentages
Unique counts
Duplicates
Data types
Basic numeric summary
Categorical summary
```

The new `statistics.py` layer provides deeper analysis of individual numerical variables:

```text
Mean / Median / Mode
Range
Variance
Standard Deviation
Quartiles
Skewness
Skewness Direction
IQR
Outlier Bounds
Potential Outliers
```

There is intentional overlap between the profiler and statistical analysis because basic descriptive statistics are useful during profiling, while the dedicated statistics layer supports deeper investigation and interpretation.

#### Statistical Analysis Functions

Added reusable functions in `statistics.py` for:

```text
get_descriptive_statistics()
get_outliers()
get_skewness_direction()
```

This keeps statistical logic separate from application orchestration in `main.py`.

The responsibility is:

```text
statistics.py
     ↓
Perform statistical calculations

main.py
     ↓
Coordinate the application and display results
```

#### Readable Console Reporting

Improved the application output by separating results into readable sections:

```text
=== Data Profile ===

=== Price Statistics ===

=== Price Outlier Analysis ===

=== SQL Analysis ===
```

Dictionary results are printed one key/value pair at a time, while SQL query results are printed one row at a time.

This improves readability without changing the underlying analysis logic.

#### Statistical Testing

Added:

```text
tests/test_statistics.py
```

Automated tests verify:

- Descriptive statistical calculations
- Mean and median
- Mode behavior
- Minimum and maximum
- Range
- Quartiles
- Positive skew direction
- Negative skew direction
- Symmetric skew direction
- IQR-based outlier detection

Tests use small controlled DataFrames with known expected results so the statistical functions can be verified independently.

The complete regression test suite was also run to ensure the new statistical layer did not break existing:

```text
CSV loading
Validation
Profiling
SQLite persistence
SQL analysis
Relational SQL functionality
```

#### Updated Application Architecture

The Engineering Workbench now follows:

```text
Raw CSV Data
      ↓
Pandas DataFrames
      ↓
Validation
      ↓
Data Profiling
      ↓
Descriptive Statistical Analysis
      │
      ├── Center
      ├── Spread
      ├── Quartiles
      ├── Skewness
      └── Outliers
      ↓
SQLite Persistence
      ↓
Relational SQL Analysis
      ↓
Readable Analysis Results
```

The complete Day 11 application and automated test suite were successfully verified both locally and inside Docker.

### Day 12

#### Data Investigation and Reporting

Completed the Week 2 data investigation by combining the Engineering Workbench's existing ingestion, validation, profiling, statistical, and relational SQL capabilities into a structured analytical investigation.

Added:

```text
reports/data_investigation_report.md
```

The report converts raw analytical results into evidence-based findings, interpretations, limitations, and recommendations.

The investigation follows:

```text
Business / Investigation Question
              ↓
        Required Data
              ↓
       Analysis Method
              ↓
            Result
              ↓
           Finding
              ↓
        Interpretation
              ↓
     Evidence-Based Conclusion
```

#### Investigation Scope

The report investigates:

- Dataset structure and data quality.
- Missing values and duplicate records.
- Price distribution and variation.
- Statistical outliers.
- Product purchase quantities.
- Payment method usage.
- Customer ordering activity.
- Customers without matching orders.
- Revenue by city.

The analysis reuses the existing Project 01 layers rather than duplicating their functionality.

```text
loader.py
    ↓
Data Ingestion

validator.py
    ↓
Data Validation

profiler.py
    ↓
Data Quality Investigation

statistics.py
    ↓
Statistical Investigation

database.py
    ↓
SQL and Relational Investigation

        ↓

Data Investigation Report
```

#### Data Quality Findings

The current orders dataset contains:

```text
Rows:        10
Columns:      7
Duplicates:   0
Missing:      0
```

The dataset passed the structural and value checks currently implemented by the Engineering Workbench.

Successful validation is treated as evidence that the data satisfies the implemented rules, not as a guarantee that every value is correct in the real world.

#### Statistical Findings

Price analysis identified:

```text
Mean                 ₹14,200
Median                ₹3,000
Standard Deviation   ≈₹19,611.79
Q1                    ₹2,000
Q3                   ₹15,000
Skewness               1.486
Direction             Right-skewed
```

The mean is substantially higher than the median, while the positive skewness value indicates a right-skewed price distribution.

IQR analysis identified two ₹50,000 observations above the calculated upper bound of ₹34,500.

These observations correspond to plausible laptop prices and are therefore treated as statistical signals requiring context rather than automatically being removed as data errors.

#### Product Findings

Total purchased quantity by product:

```text
Webcam       5
Mouse        3
Keyboard     3
Monitor      2
Laptop       2
```

Webcam has the highest total purchased quantity in the current dataset.

The result measures quantity only and is not interpreted as profitability or overall product performance.

#### Payment Findings

Order counts by payment method:

```text
UPI      4
Card     4
Cash     2
```

UPI and Card are tied as the most frequently occurring payment methods in the current dataset.

Because only 10 orders are available, the result is not generalized into broader customer payment preferences.

#### Customer Findings

Order counts by customer:

```text
Priya     3
Arjun     2
Rahul     2
Aisha     2
Neha      1
Kiran     0
```

Priya has the highest order count in the current dataset.

Kiran exists in the customer dataset but has no matching orders.

The relational analysis uses `LEFT JOIN` so customers without matching orders remain visible in the results.

Order frequency is not treated as equivalent to customer value, profitability, loyalty, or lifetime value.

#### Geographic Revenue Findings

Revenue represented in the current dataset by city:

```text
Chennai       ₹52,000
Kochi         ₹51,000
Bengaluru     ₹26,000
Hyderabad     ₹21,000
Mumbai         ₹4,000
```

Chennai generated the highest revenue in the current dataset, followed closely by Kochi.

These results describe only the available records and are not sufficient to conclude that Chennai is the company's strongest overall market or the best location for future investment.

#### Evidence-Based Interpretation

Day 12 introduced an important distinction between:

```text
Result
   ↓
Finding
   ↓
Interpretation
   ↓
Conclusion
```

For example:

```text
Result:
Chennai revenue = ₹52,000

Finding:
Chennai generated the highest revenue
in the current dataset.

Unsupported overgeneralization:
Chennai is the company's strongest market.
```

Conclusions are intentionally limited to what the available evidence supports.

#### Investigation Limitations

The report explicitly records several limitations:

- Only 10 order records are available.
- Only a small number of customers are represented.
- Time coverage is limited.
- Product coverage is limited.
- Product cost information is unavailable.
- Profit margins cannot currently be calculated.
- Order frequency does not measure complete customer value.
- Revenue does not measure profitability.
- Statistical outliers are not automatically data errors.
- Validation cannot guarantee real-world correctness.

These limitations prevent the results from being generalized beyond the available evidence.

#### Recommendations and Next Steps

The investigation recommends:

- Collecting a larger order dataset.
- Analyzing longer historical periods.
- Adding product cost information.
- Expanding customer spending analysis.
- Comparing product quantity with revenue and eventually profit.
- Investigating geographic performance across more data.
- Continuing to investigate statistical outliers using business context.
- Extending the Engineering Workbench toward a reusable production service.

#### Week 2 Final Architecture

At the end of Day 12, the Engineering Workbench follows:

```text
Raw CSV Data
      ↓
CSV Ingestion
      ↓
Validation
      ↓
Data Profiling
      ↓
Statistical Analysis
      ↓
SQLite Persistence
      ↓
Relational SQL Analysis
      ↓
Evidence
      ↓
Interpretation
      ↓
Data Investigation Report
```

The report was manually verified against the actual application output, and the complete regression test suite was successfully executed.

Day 12 completes the Week 2 Data Investigation, SQL, and Statistics stage of Project 01.

## Week 3 — Production Service

### Day 13 — Refactor Into a Professional Package

Day 13 refactored the Engineering Workbench from a collection of data-processing modules into a structured, installable Python package suitable for reuse by future CLI and API interfaces.

### Key Changes

- Renamed the package from `data_loader` to `engineering_workbench` to better represent its expanded responsibilities.
- Retained a professional `src` project layout.
- Added `pyproject.toml` for Python package configuration and package discovery.
- Installed the project in editable mode for development.
- Replaced `src.engineering_workbench` imports with clean `engineering_workbench` imports.
- Added `service.py` as an orchestration/service layer.
- Refactored `main.py` into a thin application entry point.
- Added a public package interface through `__init__.py`.
- Added service-level tests for the new orchestration boundary.
- Added guaranteed database connection cleanup using `try/finally`.
- Updated Docker packaging so the `engineering_workbench` package is installed inside the container.

### Current Architecture

```text
main.py
   ↓
engineering_workbench
   ↓
service.py
   ↓
├── loader.py
├── validator.py
├── profiler.py
├── statistics.py
└── database.py
```

The service layer now contains the high-level application workflows:

```python
run_analysis()
run_database_analysis(orders)
```

This creates a reusable architecture for upcoming interfaces:

```text
              service.py
             ↗    ↑    ↖
          main    CLI    API
```

### Verification

The refactored application was verified through:

- Full local test suite
- Local application execution
- Docker image rebuild
- Application execution inside Docker
- Full test suite inside Docker

The refactoring preserved existing application behavior while establishing a cleaner package and service architecture for Week 3.

## Day 14 — CLI Data Profiler

The Engineering Workbench now provides an installable command-line interface for profiling CSV datasets and running database analysis.

### CLI Commands

Profile a CSV dataset:

```powershell
engineering-workbench profile data/raw/orders_week2.csv

## Day 15 — FastAPI Fundamentals

The Engineering Workbench now includes a basic FastAPI web interface.

### API Module

```text
src/engineering_workbench/api.py
```

The current production API exposes:

```text
GET /
GET /health
```

### Root Endpoint

```text
GET /
```

Returns:

```json
{
  "message": "Engineering Workbench API"
}
```

### Health Endpoint

```text
GET /health
```

Returns:

```json
{
  "status": "ok"
}
```

### Run the API Locally

```powershell
uvicorn engineering_workbench.api:app --reload
```

Then open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

FastAPI automatically provides interactive Swagger documentation at:

```text
/docs
```

### API Testing

API tests are located in:

```text
tests/test_api.py
```

Run only the API tests:

```powershell
python -m pytest tests/test_api.py -v
```

Run the complete regression suite:

```powershell
python -m pytest -v
```

Day 15 verification result:

```text
41 passed
```

with one third-party Starlette/AnyIO deprecation warning.

### Docker Verification

Rebuild the image after dependency changes:

```powershell
docker build -t engineering-workbench .
```

Run the test suite inside Docker:

```powershell
docker run --rm engineering-workbench python -m pytest
```

Run the FastAPI application inside Docker:

```powershell
docker run --rm -p 8000:8000 engineering-workbench uvicorn engineering_workbench.api:app --host 0.0.0.0 --port 8000
```

This maps:

```text
Windows port 8000
        ↓
Container port 8000
        ↓
Uvicorn
        ↓
FastAPI
```

### Current Week 3 Architecture

```text
                 ┌───────────┐
                 │    CLI    │
                 └─────┬─────┘
                       │
                       ▼
                Service Layer

                 ┌───────────┐
                 │    API    │
                 └───────────┘
```

At the end of Day 15, the FastAPI interface is established and verified independently.

The next step is to connect the API layer to the existing Engineering Workbench service layer so that HTTP endpoints can expose real analytical functionality instead of only basic application and health responses.

## Day 16 — Analytical API Endpoint

Day 16 connected the FastAPI application to the Engineering Workbench service layer, allowing HTTP clients to execute real analytical workflows.

### Analytical API Endpoints

The API now provides:

```text
GET /profile
GET /database
```

Profile a supported dataset:

```text
GET /profile?dataset=orders
```

Supported datasets:

```text
orders
customers
```

The dataset parameter uses Python `Literal` typing, allowing FastAPI to automatically validate supported values and expose the available choices through Swagger documentation.

### Database Analysis Endpoint

```text
GET /database
```

This endpoint delegates to the existing database-analysis service and returns results including:

- expensive orders
- payment method counts
- product quantity totals
- customer/order details
- customers without orders
- orders per customer
- revenue by city

### Service-Layer Refactor

Shared orders preparation was extracted into:

```python
load_and_validate_orders()
```

Both:

```python
run_analysis()
run_database_analysis()
```

can now reuse the same loading and validation workflow without requiring one service operation to execute the other.

The resulting architecture is:

```text
CLI ─────┐
         │
         ├──→ Service Layer
         │        ↓
API ─────┘   Application Logic
                  ↓
        Loader / Validator / Profiler / Database
```

This keeps the CLI and API thin while allowing both interfaces to reuse the same underlying application logic.

### API Testing

The FastAPI test suite now covers:

- root endpoint
- health endpoint
- orders profiling
- customers profiling
- invalid dataset validation
- database analysis

Example:

```python
response = client.get(
    "/profile",
    params={"dataset": "orders"},
)
```

Invalid dataset values are rejected by FastAPI with HTTP `422` because the `dataset` parameter is restricted to the supported values.

### Verification

Day 16 was verified through:

```text
Swagger/manual API testing
API TestClient tests
full regression testing
Docker regression testing
```

The full regression suite also detected an outdated service test after the `run_database_analysis()` interface was refactored. Updating that test confirmed that the new service contract remained compatible with the rest of the application.

### Current API

```text
GET /            → API identification
GET /health      → health check
GET /profile     → dataset profiling
GET /database    → database analysis
```

Statistics and outlier analysis remain available through the internal `run_analysis()` service workflow but were not exposed as a dedicated API endpoint during Day 16.

## Day 17 — Integration + Failure Testing

Day 17 focused on verifying how the Engineering Workbench behaves when realistic failures occur across the service, database and API layers.

### Failure Scenarios Covered

The project now includes tests for:

- invalid order data reaching the analysis workflow
- missing order files
- database-operation failure
- database connection cleanup during failure
- unexpected internal API failures
- controlled API translation of missing dataset files

### Integration Testing

Service-level tests verify that components are connected correctly.

For example:

```text
run_analysis()
      ↓
load_and_validate_orders()
      ↓
load_csv()
      ↓
validation
```

A representative invalid-order test confirms that the service actually invokes validation before continuing with analysis.

### Failure Simulation with `monkeypatch`

Pytest's `monkeypatch` fixture is used to temporarily replace dependencies during tests.

This allows failures to be simulated without modifying real project files or databases.

Examples include:

```text
load_csv() → invalid DataFrame
load_csv() → FileNotFoundError
database write → RuntimeError
API service call → RuntimeError
```

The original dependencies are restored automatically after each test.

### Database Cleanup

The database service already uses:

```python
try:
    ...
finally:
    connection.close()
```

A failure test now verifies that the connection is still closed even when a database operation raises an exception.

This confirms that resource cleanup occurs on unsuccessful paths as well as successful ones.

### API Failure Behaviour

The API now demonstrates several different failure categories:

```text
Invalid dataset value
→ 422 Unprocessable Content

Configured profile file missing
→ 404 Not Found

Unexpected internal server failure
→ 500 Internal Server Error
```

A known `FileNotFoundError` from the profile workflow is translated at the API boundary into a controlled `404` response:

```json
{
    "detail": "Dataset 'orders' file not found"
}
```

The service layer remains independent of HTTP and continues to use normal Python exceptions.

### TestClient Server Errors

API failure tests use:

```python
TestClient(
    app,
    raise_server_exceptions=False,
)
```

when the goal is to inspect the actual HTTP `500` response instead of having the original Python exception re-raised into the test.

### Verification

Day 17 was verified through:

```text
focused failure tests
full local regression testing
Docker regression testing
Dockerized API verification
```

The emphasis was on meaningful failure behaviour rather than adding repetitive tests for every possible invalid value.

### Day 17 Result

The Engineering Workbench now has evidence that it behaves predictably when:

- input data is invalid
- required files are unavailable
- database operations fail
- resources require cleanup after failure
- API-facing failures need to be classified and communicated