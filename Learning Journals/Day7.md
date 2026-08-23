# Day 7 — Real CSV Ingestion and Data Validation

## What I Worked On

Today I moved Project 01 from small development examples toward working with a more realistic CSV dataset.

The main dataset used for Week 2 became:

```text
data/raw/orders_week2.csv
```

The dataset contains:

```text
order_id
customer_id
product
quantity
price
order_date
payment_method
```

The goal was to make the existing engineering pipeline capable of safely loading and validating this real structured dataset before performing deeper analysis.

---

## Application Flow

The application pipeline became:

```text
orders_week2.csv
       ↓
Configuration
       ↓
CSV Loader
       ↓
Pandas DataFrame
       ↓
Validation
       ↓
Profiler
       ↓
Output
```

This helped me understand that loading data successfully does not automatically mean the data is valid.

---

## What I Learned

### CSV Ingestion

The loader reads the CSV into a pandas DataFrame.

The orders dataset also contains:

```text
order_date
```

which can be parsed as a datetime column when loading the dataset.

This allows the application to work with dates as actual date/time data rather than treating them only as plain strings.

---

### Schema Validation

I learned that a dataset can exist and load correctly but still have the wrong structure.

For example, an orders dataset may be missing:

```text
customer_id
quantity
order_date
payment_method
```

The validation layer checks that the required columns exist before the application continues.

If required columns are missing, the program raises:

```text
ValueError
```

This is an example of **fail-fast validation**.

Instead of allowing bad data to travel further through the application, the program stops near the source of the problem.

---

### Value Validation

Validation is not only about checking column names.

A dataset can contain all required columns while still containing invalid values.

The project therefore also validates order values before continuing with analysis.

The general idea is:

```text
Load data
    ↓
Check structure
    ↓
Check values
    ↓
Only then analyze the data
```

---

## Separation of Responsibilities

The project continues to separate responsibilities across modules.

```text
config.py
→ stores configuration such as dataset paths

loader.py
→ loads the CSV

validator.py
→ checks whether the data is valid

profiler.py
→ analyzes the DataFrame

main.py
→ coordinates the application
```

This is better than putting all application logic into one large Python file.

---

## Testing

The validation behavior was covered with automated tests.

The tests help verify that:

- Valid datasets are accepted.
- Missing required columns are detected.
- Invalid data causes the expected failure.
- Existing functionality continues working after changes.

This reinforced the idea that tests are not only used to prove that code works once; they also protect existing behavior as the project evolves.

---

## Debugging / Engineering Lessons

A major lesson was the difference between:

```text
File exists
```

and:

```text
File contains valid data
```

The loader is responsible for successfully obtaining the data.

The validator is responsible for deciding whether that data is acceptable for the application.

Keeping those responsibilities separate makes failures easier to understand and debug.

---

## What I Can Explain Now

I can explain:

- How a CSV becomes a pandas DataFrame.
- Why real datasets need validation.
- The difference between loading and validating data.
- Why required-column validation is useful.
- Why value validation is also necessary.
- What fail-fast validation means.
- Why validation should happen before profiling or analysis.
- Why loaders, validators, and profilers should have separate responsibilities.
- How automated tests protect the data pipeline.

---

## End-of-Day Status

By the end of Day 7, Project 01 could:

```text
Load a real orders CSV
        ↓
Convert it into a DataFrame
        ↓
Validate its structure and values
        ↓
Pass valid data to the profiler
```

This established the Week 2 data-ingestion and validation foundation needed for deeper data-quality analysis.