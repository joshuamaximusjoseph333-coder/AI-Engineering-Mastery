# Day 11 — Descriptive Statistics and Statistical Analysis

## What I Worked On

Today I extended Project 01 with a dedicated statistical analysis layer.

Before Day 11, the Engineering Workbench could already:

```text
Load CSV data
      ↓
Validate data
      ↓
Profile data
      ↓
Store data in SQLite
      ↓
Run relational SQL analysis
```

The Day 8 profiler already produced some basic numerical statistics, but Day 11 focused on understanding and using descriptive statistics for deeper investigation.

The application now follows:

```text
Raw CSV Data
      ↓
Pandas DataFrames
      ↓
Validation
      ↓
Profiling
      ↓
Descriptive Statistical Analysis
      │
      ├── Central Tendency
      ├── Spread
      ├── Quartiles
      ├── Distribution / Skewness
      └── Outlier Detection
      ↓
SQLite
      ↓
Relational SQL Analysis
      ↓
Readable Results
```

---

# Why Add a Statistics Layer?

The existing `profiler.py` already produced:

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

through its numeric summary.

However, profiling and statistical investigation have different purposes.

```text
profiler.py
    ↓
"What does this dataset look like?"

statistics.py
    ↓
"What can I understand statistically about a variable?"
```

The statistics layer adds deeper analysis such as:

```text
Median
Mode
Range
Variance
Skewness
Skewness direction
IQR
Outlier bounds
Potential outliers
```

There is some intentional overlap because basic descriptive statistics are useful during both profiling and deeper analysis.

---

# Creating the Statistics Module

I created:

```text
src/data_loader/statistics.py
```

This keeps statistical calculations separate from:

```text
main.py
```

The responsibility is:

```text
statistics.py
     ↓
Perform statistical calculations

main.py
     ↓
Coordinate the complete application
```

This follows the same modular design used elsewhere in Project 01.

---

# Working With a Pandas Series

The statistical functions accept:

```python
data: pd.DataFrame
column: str
```

Inside the function:

```python
series = data[column]
```

For example:

```python
get_descriptive_statistics(
    orders,
    "price",
)
```

means:

```text
data   = orders
column = "price"
```

Therefore:

```python
series = data[column]
```

becomes:

```python
series = orders["price"]
```

The function can therefore be reused for other numerical columns instead of being hard-coded specifically for price.

---

# Descriptive Statistics Function

I implemented:

```python
get_descriptive_statistics()
```

The function calculates:

```text
Mean
Median
Mode
Minimum
Maximum
Range
Variance
Standard deviation
Q1
Q3
Skewness
Skewness direction
```

This provides a more complete statistical description of a numerical variable.

---

# Mean, Median and Mode

The application uses:

```python
series.mean()
series.median()
series.mode()
```

For the current price data:

```text
Mean   = 14,200
Median = 3,000
```

The large difference between the two became important when investigating the shape of the distribution.

The price dataset contains:

```text
1000
1000
2000
2000
3000
3000
15000
15000
50000
50000
```

Every distinct price occurs twice.

Therefore pandas returns:

```python
[1000, 2000, 3000, 15000, 50000]
```

for the mode because all values tie for the highest frequency.

There is no single dominant mode.

---

# Measures of Spread

The statistical layer calculates:

```text
Range
Variance
Standard deviation
```

The range is:

```text
Maximum - Minimum
```

For price:

```text
50,000 - 1,000 = 49,000
```

The project also produced:

```text
Standard deviation ≈ 19,611.79
```

This indicates substantial variation in the order prices.

The prices are not tightly concentrated around a single value.

---

# Quartiles

The application calculates:

```python
q1 = series.quantile(0.25)
q3 = series.quantile(0.75)
```

For the price dataset:

```text
Q1 = 2,000
Q3 = 15,000
```

These values are also used for IQR-based outlier detection.

---

# IQR

The Interquartile Range is calculated as:

```text
IQR = Q3 - Q1
```

For the current data:

```text
IQR = 15,000 - 2,000
    = 13,000
```

IQR measures the spread of the middle portion of the distribution and is useful for identifying unusually distant observations.

---

# Outlier Detection

I implemented:

```python
get_outliers()
```

using the IQR method.

The boundaries are calculated as:

```text
Lower Bound = Q1 - 1.5 × IQR

Upper Bound = Q3 + 1.5 × IQR
```

For the price dataset:

```text
Lower Bound = -17,500
Upper Bound = 34,500
```

Therefore values above:

```text
34,500
```

are flagged as potential high outliers.

The function detected:

```text
50,000
50,000
```

---

# Boolean Filtering

One important Pandas concept learned today was boolean filtering.

The outlier function contains:

```python
outliers = series[
    (series < lower_bound) | (series > upper_bound)
]
```

This initially looked complicated because multiple operations are combined into one expression.

The first condition:

```python
series < lower_bound
```

checks every value and creates a boolean Series.

The second:

```python
series > upper_bound
```

does the same for the upper boundary.

Conceptually:

```text
Value     Below Lower?     Above Upper?

1000         False            False
2000         False            False
3000         False            False
15000        False            False
50000        False            True
```

The operator:

```text
|
```

means element-wise OR for Pandas conditions.

Therefore:

```python
(series < lower_bound) | (series > upper_bound)
```

asks:

```text
Is the value below the lower bound
OR
above the upper bound?
```

The resulting True/False values form a:

```text
boolean mask
```

Then:

```python
series[mask]
```

keeps only values where the mask is `True`.

Therefore:

```python
series[
    (series < lower_bound) | (series > upper_bound)
]
```

means:

> Keep only the values outside the IQR boundaries.

---

# Statistical Outlier vs Bad Data

An important lesson from Day 11 was:

```text
Statistical Outlier
        ≠
Incorrect Data
```

The IQR method flagged:

```text
₹50,000
```

as an outlier.

However, the corresponding product is a laptop.

₹50,000 is a plausible laptop price.

Therefore the correct engineering workflow is:

```text
Detect Outlier
      ↓
Investigate
      ↓
Check Business Context
      ↓
Valid?
 ┌────┴────┐
Yes        No
 ↓          ↓
Keep     Correct /
         Remove
```

Outlier detection should therefore be used as an investigation tool rather than an automatic deletion rule.

---

# Distribution

I learned that a distribution describes how observations are spread across their possible values.

Important shapes include:

```text
Symmetric
Right-skewed
Left-skewed
```

---

# Symmetric Distribution

A symmetric distribution has similar behavior on both sides of its center.

Often:

```text
Mean ≈ Median
```

However, mean and median alone do not mathematically define skewness.

---

# Right Skew / Positive Skew

A right-skewed distribution has a longer or heavier tail toward larger values.

Conceptually:

```text
      /\
     /  \____________→
                  right tail
```

High observations tend to pull the mean upward.

Therefore a right-skewed distribution often has:

```text
Mean > Median
```

Right skew is also called:

```text
Positive Skew
```

---

# Left Skew / Negative Skew

A left-skewed distribution has a longer or heavier tail toward smaller values.

Conceptually:

```text
←____________/\
             /  \
```

Low observations tend to pull the mean downward.

Therefore it often has:

```text
Mean < Median
```

Left skew is also called:

```text
Negative Skew
```

The direction of skew refers to the direction of the tail, not where most observations are located.

---

# Measuring Skewness

Pandas provides:

```python
series.skew()
```

General interpretation:

```text
Positive → right-skewed
Negative → left-skewed
Near zero → roughly symmetric
```

For Project 01:

```text
skewness ≈ 1.486
```

The value is positive.

Therefore the price distribution is:

```text
right-skewed
```

This agrees with the observation that:

```text
Mean   = 14,200
Median = 3,000
```

The high-price observations pull the mean substantially upward.

---

# Skewness Direction Helper

I added:

```python
get_skewness_direction()
```

to convert the numerical skewness value into a human-readable result.

Conceptually:

```text
series.skew()
      ↓
1.486
      ↓
get_skewness_direction()
      ↓
"right-skewed"
```

The descriptive statistics output now contains both:

```text
skewness: 1.486...
skewness_direction: right-skewed
```

This allows the application to retain the actual statistical value while also providing an easier interpretation.

---

# Project 01 Statistical Results

The current price analysis produced:

```text
Mean                 = 14,200
Median               = 3,000
Minimum              = 1,000
Maximum              = 50,000
Range                = 49,000
Variance             ≈ 384,622,222.22
Standard deviation   ≈ 19,611.79
Q1                   = 2,000
Q3                   = 15,000
Skewness             ≈ 1.486
Skewness direction   = right-skewed
```

Outlier analysis produced:

```text
IQR                   = 13,000
Lower bound           = -17,500
Upper bound           = 34,500
Potential outliers    = [50,000, 50,000]
```

---

# Statistical Interpretation

The important Day 11 lesson was that statistics should not only be calculated.

They should be interpreted together.

For the current dataset:

```text
Mean >> Median
        ↓
high observations are affecting the average

Positive skewness
        ↓
right-skewed distribution

Large standard deviation
        ↓
substantial price variation

IQR detects ₹50,000
        ↓
statistically unusual observations

Business context
        ↓
₹50,000 is plausible for laptops

Conclusion
        ↓
keep the observations
```

This is more useful than simply printing statistical numbers without understanding them.

---

# Improving Console Output

As the application grew, the terminal output became difficult to read.

Previously, dictionaries and SQL result lists were printed directly:

```python
print("Price statistics:", price_statistics)
```

which produced large single-line outputs.

I reorganized `main.py` into visible application stages and added console sections such as:

```text
=== Data Profile ===

=== Price Statistics ===

=== Price Outlier Analysis ===

=== SQL Analysis ===
```

Dictionary results are now printed using:

```python
for key, value in price_statistics.items():
    print(f"{key}: {value}")
```

This prints one statistic per line.

SQL query results are printed using:

```python
for row in payment_counts:
    print(row)
```

This prints one database result row at a time instead of printing an entire list on one line.

---

# Dictionary Iteration

For:

```python
for key, value in price_statistics.items():
```

`.items()` provides each dictionary key and its corresponding value.

Conceptually:

```text
mean                 → 14200
median               → 3000
skewness             → 1.486
skewness_direction   → right-skewed
```

This produces cleaner console output.

---

# SQL Result Iteration

SQL functions return lists containing tuples.

For example:

```python
[
    ("UPI", 4),
    ("Card", 4),
    ("Cash", 2),
]
```

Using:

```python
for row in payment_counts:
    print(row)
```

prints:

```text
('UPI', 4)
('Card', 4)
('Cash', 2)
```

instead of dumping the entire list on one line.

---

# Updated main.py Structure

The main application is now visually organized as:

```text
IMPORTS
   ↓
LOAD DATA
   ↓
VALIDATE
   ↓
PROFILE
   ↓
STATISTICAL ANALYSIS
   ↓
PRINT PROFILE / STATISTICS
   ↓
CREATE DATABASE CONNECTION
   ↓
WRITE TABLES
   ↓
SQL ANALYSIS
   ↓
PRINT SQL RESULTS
   ↓
CLOSE CONNECTION
```

This did not fundamentally change the program logic.

It made the execution flow easier to understand and the output easier to inspect.

---

# Automated Statistical Testing

I created:

```text
tests/test_statistics.py
```

The tests use small controlled DataFrames whose expected statistical results are known.

For example:

```python
data = pd.DataFrame(
    {
        "price": [10, 20, 30],
    }
)
```

This makes values such as:

```text
Mean   = 20
Median = 20
Range  = 20
Q1     = 15
Q3     = 25
```

easy to verify independently.

---

# Testing Skewness Direction

The helper function is tested independently using known inputs:

```text
positive number
      ↓
right-skewed

negative number
      ↓
left-skewed

zero
      ↓
symmetric
```

This verifies all branches of the helper function.

---

# Testing Outlier Detection

A controlled dataset was used:

```text
10
10
10
10
100
```

The expected outlier is:

```text
100
```

The automated test verifies that:

```python
get_outliers()
```

returns the expected value.

This reinforces the testing principle:

```text
Small controlled input
        ↓
Known expected result
        ↓
Run function
        ↓
Assert actual == expected
```

---

# Regression Testing

After adding the statistical functionality, I ran:

```text
python -m pytest
```

to execute the complete project test suite.

This verifies not only the new statistics functions but also checks that existing functionality still works.

The regression suite covers the existing:

```text
Loader
Validator
Profiler
Database layer
SQL analysis
Relational SQL functionality
```

along with the new statistics layer.

---

# Docker Verification

After local verification, I rebuilt the Docker image and ran the application inside the container.

I also ran the complete automated test suite inside Docker.

This verifies that Day 11 works in both:

```text
Windows development environment
            +
Docker Linux environment
```

The Day 11 implementation and tests passed in both environments.

---

# Important Engineering Lessons

## 1. Calculation Is Not Interpretation

A tool can calculate:

```text
mean = 14200
```

but an engineer must understand what that number means.

The median, spread, skewness, outliers, and business context should be considered together.

---

## 2. Statistical Rules Produce Signals

The IQR rule does not decide whether a record is valid.

It produces a signal:

```text
"This observation is unusual."
```

The engineer then investigates the observation.

---

## 3. Reusable Functions Should Not Be Hard-Coded

Instead of creating:

```text
get_price_statistics()
```

the function accepts:

```text
DataFrame + column name
```

allowing the same logic to analyze different numerical variables.

---

## 4. Separate Responsibilities

The project now separates:

```text
profiler.py
→ broad dataset profiling

statistics.py
→ statistical investigation

database.py
→ persistence and SQL analysis

main.py
→ application orchestration
```

This makes the application easier to understand and extend.

---

## 5. Readability Matters

Correct output is not necessarily good output.

As applications grow, results should be organized so humans can inspect them easily.

The console-output cleanup improved presentation without changing the underlying analysis.

---

# What I Can Explain Now

I can explain:

- What descriptive statistics are.
- Why descriptive statistics are useful during data investigation.
- The difference between a DataFrame and a selected Series.
- Mean, median and mode.
- Why the mean can be affected by extreme values.
- Range, variance and standard deviation.
- Quartiles and IQR.
- How the IQR outlier rule works.
- What a Pandas boolean mask is.
- How `|` combines Pandas conditions.
- Why a statistical outlier is not automatically bad data.
- What a distribution represents.
- What symmetric, right-skewed and left-skewed distributions mean.
- Why skew direction refers to the tail.
- What positive and negative skewness mean.
- Why mean greater than median can suggest positive skew.
- Why mean vs median is a clue rather than the definition of skewness.
- How `series.skew()` measures asymmetry.
- Why the Project 01 price distribution is right-skewed.
- Why the ₹50,000 observations should be investigated rather than automatically deleted.
- Why `statistics.py` exists separately from `profiler.py`.
- How reusable statistical functions accept a DataFrame and column name.
- How dictionary `.items()` can be used for readable output.
- How SQL result rows can be printed individually.
- Why statistical functions should be tested using small controlled datasets.
- Why the full regression suite should be run after adding a new application layer.

---

# End-of-Day Status

By the end of Day 11, Project 01 evolved from:

```text
Data ingestion
      ↓
Validation
      ↓
Profiling
      ↓
SQL analysis
```

into:

```text
Data ingestion
      ↓
Validation
      ↓
Profiling
      ↓
Statistical Investigation
      │
      ├── Center
      ├── Spread
      ├── Quartiles
      ├── Distribution
      ├── Skewness
      └── Outliers
      ↓
SQLite
      ↓
Relational SQL Analysis
      ↓
Readable Results
```

The application can now not only profile and query data but also statistically investigate numerical variables and interpret unusual patterns.

The complete implementation and automated test suite were successfully verified locally and inside Docker.

Day 11 established the descriptive-statistics foundation needed for the final Week 2 data investigation report.