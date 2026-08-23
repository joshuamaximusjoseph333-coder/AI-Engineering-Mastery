# Day 8 — Data-Quality Profiler

## What I Worked On

Today I expanded the existing pandas-based profiler into a more useful data-quality investigation tool.

The profiler originally reported basic information such as:

- Dataset shape
- Column names
- Missing-value counts
- Duplicate-row count
- Data types

Today I extended it to provide deeper information about the dataset.

The main dataset used was:

```text
data/raw/orders_week2.csv
```

---

## Profiler Architecture

The profiling logic is kept inside:

```text
src/data_loader/profiler.py
```

Instead of putting all profiling operations directly inside `main.py`, individual functions are responsible for individual profiling tasks.

The overall flow is:

```text
orders_week2.csv
        ↓
load_csv()
        ↓
Pandas DataFrame
        ↓
Validation
        ↓
profile_data()
        ↓
Individual profiler functions
        ↓
Complete profile dictionary
        ↓
Readable output
```

---

## Existing Profiler Functions

The profiler already contained functions such as:

```python
get_shape()
get_columns()
get_missing_values()
get_duplicate_count()
get_data_types()
```

Each function performs one specific task.

For example:

```python
def get_shape(data: pd.DataFrame) -> tuple[int, int]:
    return data.shape
```

returns:

```text
(rows, columns)
```

For the current orders dataset:

```text
(10, 7)
```

---

## Missing-Value Counts

The profiler uses:

```python
data.isna().sum().to_dict()
```

The operations work as:

```text
data
 ↓
.isna()
 ↓
True/False for missing values
 ↓
.sum()
 ↓
number of missing values per column
 ↓
.to_dict()
 ↓
Python dictionary
```

Example:

```text
{
    "order_id": 0,
    "customer_id": 0,
    "product": 0,
    "quantity": 0,
    "price": 0
}
```

This tells me how many values are missing from each column.

---

## Missing-Value Percentages

I extended the profiler to calculate the percentage of missing values in each column.

This is useful because a raw count alone does not always show how serious a data-quality problem is.

For example:

```text
5 missing values out of 10 rows
→ 50% missing
```

while:

```text
5 missing values out of 100,000 rows
→ 0.005% missing
```

The percentage gives the missing-value count context.

The current orders dataset reported:

```text
0.0%
```

missing values for all columns.

---

## Unique Value Counts

The profiler was extended to report how many unique values each column contains.

Pandas functionality:

```python
data.nunique()
```

Conceptually:

```text
column
 ↓
find distinct values
 ↓
count them
```

For example, the current dataset contains:

```text
10 unique order IDs
5 unique customer IDs
5 unique products
3 unique quantity values
5 unique prices
10 unique order dates
3 unique payment methods
```

Unique counts can help identify:

- Identifier-like columns
- Repeated categories
- Low-cardinality categorical columns
- Suspiciously constant columns

---

## Duplicate Detection

Duplicate rows are detected using:

```python
data.duplicated()
```

and counted using:

```python
data.duplicated().sum()
```

The project converts the result to a Python integer:

```python
int(data.duplicated().sum())
```

The current dataset contains:

```text
0 duplicate rows
```

Duplicate detection is important because repeated records can distort later statistics and analysis.

---

## Data Types

The profiler reports the type of each DataFrame column.

The current orders dataset includes types such as:

```text
order_id        → int64
customer_id     → int64
product         → str
quantity        → int64
price           → int64
order_date      → datetime64
payment_method  → str
```

Data types matter because they determine what operations are appropriate for each column.

For example:

```text
price
→ numeric calculations

product
→ categorical analysis

order_date
→ date/time analysis
```

---

## Numeric Summary

I added descriptive summaries for useful numeric columns.

The profiler reports statistics such as:

```text
count
mean
standard deviation
minimum
25th percentile
median / 50th percentile
75th percentile
maximum
```

These are based on pandas descriptive-statistics functionality.

For the current project, useful numeric analysis focuses on business-measure columns such as:

```text
quantity
price
```

rather than treating identifier columns such as:

```text
order_id
customer_id
```

as meaningful measurements.

For example, calculating the average `order_id` would technically be possible but would not provide useful business information.

This taught me an important lesson:

> A numeric data type does not automatically mean that a column should be statistically analyzed as a numeric measurement.

---

## Categorical Summary

The profiler also analyzes categorical columns.

For the current dataset, examples include:

```text
product
payment_method
```

The profiler reports category frequencies.

Example:

```text
product:

Laptop   → 2
Mouse    → 2
Keyboard → 2
Monitor  → 2
Webcam   → 2
```

and:

```text
payment_method:

Card → 4
UPI  → 4
Cash → 2
```

This helps understand the distribution of categorical data.

---

## `value_counts()`

A useful pandas operation introduced during profiling was:

```python
data[column].value_counts()
```

It counts how many times each distinct value occurs.

Example:

```text
Card
Card
UPI
Cash
UPI
```

becomes approximately:

```text
Card → 2
UPI  → 2
Cash → 1
```

This is useful for categorical profiling.

---

## `select_dtypes()`

Pandas can select columns according to their data type using:

```python
data.select_dtypes(...)
```

This allows the profiler to treat different kinds of columns differently.

Conceptually:

```text
DataFrame
   ↓
inspect data types
   ↓
select appropriate columns
   ↓
numeric analysis / categorical analysis
```

This is useful because numeric and categorical data require different profiling operations.

---

## `describe()`

Pandas provides:

```python
data.describe()
```

for descriptive statistics.

For numeric data it can provide values such as:

```text
count
mean
std
min
25%
50%
75%
max
```

This allowed the project to generate numeric summaries without manually calculating every statistic.

---

## Complete `profile_data()` Function

The individual profiling functions are combined by:

```python
profile_data()
```

Conceptually:

```text
profile_data(data)
      │
      ├── get_shape()
      ├── get_columns()
      ├── get_missing_values()
      ├── get_missing_percentages()
      ├── get_unique_counts()
      ├── get_duplicate_count()
      ├── get_data_types()
      ├── get_numeric_summary()
      └── get_categorical_summary()
              ↓
        profile dictionary
```

This keeps the profiler modular.

Each small function performs one responsibility, while `profile_data()` coordinates them.

---

## Profile Output

The application prints the profile using:

```python
for key, value in profile.items():
    print(f"{key}: {value}")
```

Instead of printing the entire dictionary as one large object, each profiling result appears on a separate line.

Example:

```text
shape: ...
columns: ...
missing_values: ...
missing_percentages: ...
unique_counts: ...
duplicate_count: ...
data_types: ...
numeric_summary: ...
categorical_summary: ...
```

This makes the output easier to inspect.

---

## Automated Testing

The existing profiler tests were expanded to cover the new functionality.

The profiler tests use small controlled DataFrames rather than depending on the real CSV.

Example:

```python
data = pd.DataFrame(
    {
        "order_id": [1, 2, 3],
        "product": ["Laptop", "Mouse", "Keyboard"],
        "price": [50000, None, 2000],
    }
)
```

Because the test data is controlled, I know exactly what the expected result should be.

The tests verify profiler behavior such as:

- Dataset shape
- Column names
- Missing-value counts
- Missing percentages
- Unique-value counts
- Duplicate detection
- Data types
- Numeric summaries
- Categorical summaries
- Complete `profile_data()` output

---

## Important Engineering Lesson

The profiler is not simply:

```text
print some pandas information
```

It is becoming a reusable component:

```text
DataFrame
   ↓
standard profiling functions
   ↓
structured dictionary
   ↓
other parts of the application can use the result
```

This is more useful than tightly coupling the analysis directly to console printing.

---

## Pandas Functionality Practiced

Important pandas functionality used during this stage included:

```python
data.shape
data.columns.tolist()
data.isna()
data.sum()
data.nunique()
data.duplicated()
data.dtypes
data.select_dtypes()
data.describe()
data[column].value_counts()
.to_dict()
```

These operations form part of the core pandas toolkit for investigating structured datasets.

---

## What I Can Explain Now

I can explain:

- What a data-quality profiler does.
- Why profiling should happen after loading and validation.
- How to inspect dataset dimensions.
- How pandas detects missing values.
- Why missing percentages can be more informative than counts.
- How to detect duplicate rows.
- What unique counts tell us about columns.
- Why data types matter.
- How `value_counts()` analyzes categorical data.
- How `describe()` summarizes numeric data.
- Why identifiers should not automatically be treated as meaningful numeric measurements.
- Why individual profiler operations are separated into functions.
- How `profile_data()` combines those functions into one report.
- Why controlled DataFrames are useful in automated tests.

---

## End-of-Day Status

By the end of Day 8, the Engineering Workbench had evolved from basic dataset inspection into a more useful data-quality profiling system.

```text
CSV Dataset
     ↓
Loader
     ↓
DataFrame
     ↓
Validator
     ↓
Data-Quality Profiler
     │
     ├── Shape
     ├── Columns
     ├── Missing counts
     ├── Missing percentages
     ├── Unique counts
     ├── Duplicates
     ├── Data types
     ├── Numeric summary
     └── Categorical summary
     ↓
Structured Profile Report
```

The application and tests were successfully verified locally and inside Docker.