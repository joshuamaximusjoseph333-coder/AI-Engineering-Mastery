# Day 12 — Data Investigation Report

## What I Worked On

Today I completed the final investigation stage of Week 2.

Days 7–11 built the individual technical capabilities required to work with data:

```text
Day 7
CSV Ingestion
      ↓
Day 8
Data Profiling
      ↓
Day 9
SQL Foundations
      ↓
Day 10
Relational SQL Analysis
      ↓
Day 11
Descriptive Statistics
```

Day 12 combined these capabilities into a structured data investigation.

The main goal was not to add another isolated Python feature.

The goal was to learn how to take analytical results and turn them into findings whose conclusions are supported by evidence.

---

# From Analysis to Investigation

Before Day 12, the application could produce results such as:

```text
Mean price = ₹14,200
Median price = ₹3,000

Webcam quantity = 5

Priya orders = 3

Chennai revenue = ₹52,000
```

However, producing numbers is not the same as performing an investigation.

The Day 12 process is:

```text
Data
 ↓
Analysis
 ↓
Result
 ↓
Finding
 ↓
Interpretation
 ↓
Conclusion / Recommendation
```

This introduced the distinction between calculating a result and understanding what the result actually supports.

---

# Result vs Finding vs Interpretation

A result is the direct output of an analysis.

Example:

```text
Mean price = ₹14,200
Median price = ₹3,000
```

A finding identifies something noteworthy:

```text
The mean price is substantially higher than the median.
```

An interpretation explains the finding:

```text
Higher-priced observations are pulling the mean upward,
which is consistent with the right-skewed price distribution.
```

The interpretation should remain grounded in the available evidence.

---

# Question-Driven Investigation

An important lesson was that analysis should begin with questions.

Instead of:

```text
I know SQL.
What queries can I run?
```

the better workflow is:

```text
What do I want to know?
        ↓
What data can answer it?
        ↓
What analysis technique is appropriate?
        ↓
What evidence does it produce?
```

The Project 01 investigation focused on questions such as:

```text
Is the dataset suitable for analysis?

What does the price distribution look like?

Are there statistically unusual prices?

Which products have the highest purchased quantity?

Which payment methods occur most frequently?

Which customers place the most orders?

Are there customers without matching orders?

Which cities generated the most revenue?
```

---

# Mapping Questions to Engineering Layers

The investigation reused the system already built during Week 2.

```text
Question
   ↓
Appropriate Project Layer
```

For data quality:

```text
validator.py
profiler.py
```

For price statistics:

```text
statistics.py
```

For product and payment analysis:

```text
database.py
```

For customer and geographic analysis:

```text
database.py
+
relational SQL
```

This demonstrated why the modular architecture built during previous days is useful.

---

# Data Investigation Report

I created:

```text
reports/data_investigation_report.md
```

The report is a professional project output.

Its purpose is different from this Learning Journal.

```text
data_investigation_report.md
→ What did I discover about the data?

Day12.md
→ What did I learn while performing the investigation?
```

The report contains:

```text
1. Investigation Objective
2. Dataset Overview
3. Data Quality Findings
4. Price and Statistical Analysis
5. Product Analysis
6. Payment Method Analysis
7. Customer Analysis
8. Geographic Revenue Analysis
9. Key Findings
10. Limitations
11. Recommendations and Next Steps
```

---

# Investigation Objective

The report begins by defining what the investigation is trying to understand.

This is important because analysis should have a purpose.

The investigation covers:

```text
Data quality
Price behavior
Statistical outliers
Product quantity
Payment usage
Customer activity
Unmatched customers
City-level revenue
```

The objective is stated neutrally before conclusions are formed.

---

# Dataset Overview

The investigation uses:

```text
orders_week2.csv
customers_week2.csv
```

The orders dataset contains:

```text
10 rows
7 columns
```

The customer and order datasets are logically related using:

```text
customer_id
```

Conceptually:

```text
customers
    │
    │ customer_id
    ↓
orders
```

This relationship allows customer information such as city to be combined with order information.

---

# Data Quality Investigation

The current orders dataset contains:

```text
10 rows
7 columns
0 duplicate rows
0 missing values
```

The required columns are present and the current validation checks pass.

However, I learned an important distinction:

```text
Validation Passed
       ≠
Real-World Accuracy Guaranteed
```

The validator can determine whether values satisfy implemented rules.

For example:

```text
price exists
price is numeric
price is positive
```

It cannot independently prove that a recorded transaction happened exactly as represented.

Therefore a professional statement is:

```text
No problems were detected by the implemented validation checks.
```

rather than:

```text
The dataset is guaranteed to be completely accurate.
```

---

# Statistical Investigation

The price analysis produced:

```text
Mean                 ₹14,200
Median                ₹3,000
Standard deviation   ≈₹19,611.79
Q1                    ₹2,000
Q3                   ₹15,000
Skewness               1.486
Direction             Right-skewed
```

The mean is much larger than the median.

Combined with positive skewness, this provides evidence that high-priced observations are pulling the distribution toward the right.

The standard deviation also indicates substantial price variation.

---

# Outlier Interpretation

IQR analysis produced:

```text
Q1          ₹2,000
Q3         ₹15,000
IQR        ₹13,000

Lower Bound   -₹17,500
Upper Bound    ₹34,500
```

Two observations:

```text
₹50,000
₹50,000
```

were identified as potential statistical outliers.

However, these values correspond to laptops.

This reinforced:

```text
Statistical Outlier
        ≠
Data Error
```

The correct process is:

```text
Detect
 ↓
Investigate
 ↓
Apply Context
 ↓
Decide
```

The values were therefore not automatically treated as invalid.

---

# Product Investigation

The SQL analysis produced:

```text
Webcam       5
Mouse        3
Keyboard     3
Monitor      2
Laptop       2
```

Therefore:

```text
Webcam has the highest total purchased quantity
in the current dataset.
```

Initially, this type of result could easily lead to:

```text
Webcam is the most profitable product.
```

But that conclusion is unsupported.

I learned:

```text
Quantity ≠ Revenue
```

and:

```text
Revenue ≠ Profit
```

For example:

```text
Webcam:
5 × ₹3,000 = ₹15,000

Laptop:
2 × ₹50,000 = ₹100,000
```

A product can have lower quantity but higher revenue.

Profit would additionally require cost information.

---

# Payment Investigation

The current payment results are:

```text
UPI      4
Card     4
Cash     2
```

Therefore the supported finding is:

```text
UPI and Card are tied as the most frequently
occurring payment methods in the current dataset.
```

It would be inaccurate to say:

```text
UPI is the most popular payment method.
```

because Card has the same count.

It would also be too broad to conclude:

```text
Customers generally prefer UPI and Card.
```

because the dataset contains only 10 orders.

---

# Customer Investigation

Orders per customer:

```text
Priya     3
Arjun     2
Rahul     2
Aisha     2
Neha      1
Kiran     0
```

Priya has the highest order count in the current dataset.

However:

```text
Highest Order Count
        ≠
Most Valuable Customer
```

Customer value could require:

```text
Total spending
Average order value
Profit generated
Repeat purchase behavior
Customer lifetime value
```

which are not all measured by the current analysis.

---

# Customers Without Orders

Kiran exists in:

```text
customers_week2.csv
```

but has no matching order.

Using a `LEFT JOIN` preserves Kiran in the result.

This demonstrates an important relational use case:

```text
customers
   ↓
LEFT JOIN orders
   ↓
Keep every customer
   ↓
Matching order?
   ├── Yes → order information
   └── No  → NULL
```

This allows customers with no matching orders to be identified.

However, I should not automatically describe Kiran as a permanently inactive customer because the dataset may represent only a limited period.

---

# Geographic Investigation

Revenue by city:

```text
Chennai       ₹52,000
Kochi         ₹51,000
Bengaluru     ₹26,000
Hyderabad     ₹21,000
Mumbai         ₹4,000
```

The supported finding is:

```text
Chennai generated the highest revenue
in the current dataset.
```

A stronger statement such as:

```text
Chennai is the company's strongest market.
```

is not supported.

The dataset is too small and limited to justify such a broad conclusion.

---

# Avoiding Overgeneralization

One of the most important concepts from Day 12 was avoiding overgeneralization.

Example:

```text
Evidence:
Chennai = ₹52,000

Supported:
Chennai generated the highest revenue
in the current dataset.

Not supported:
Chennai is the best city for future investment.
```

The strength of the conclusion must match the strength of the evidence.

---

# Understanding Metrics

I learned that metrics must be interpreted according to exactly what they measure.

```text
Quantity
→ how many units were purchased

Revenue
→ money represented by sales

Profit
→ revenue minus costs

Order count
→ ordering frequency
```

These should not be treated as interchangeable.

For example:

```text
High Quantity
    ≠
High Profit

High Revenue
    ≠
High Profit

High Order Count
    ≠
High Customer Value
```

---

# Limitations

A professional investigation should explain what its data cannot establish.

The Project 01 investigation has several limitations:

```text
Only 10 orders
Small number of customers
Limited time coverage
Only five products
No product-cost information
No profit-margin information
```

These limitations mean the findings should not be generalized into broad business conclusions.

I learned that acknowledging limitations strengthens an analysis because it communicates the boundaries of the evidence.

---

# Recommendations

Recommendations should also match the evidence.

For example:

Unsupported recommendation:

```text
Invest more money in Chennai.
```

Better recommendation:

```text
Analyze city-level sales across more orders
and longer time periods before making
geographic investment decisions.
```

Other next steps include:

```text
Collect more order data
Analyze longer time periods
Add product costs
Calculate product revenue
Analyze customer spending
Investigate repeat purchasing
Expand geographic analysis
```

---

# Key Findings vs Full Analysis

The report contains a separate Key Findings section.

The purpose is not to repeat every result.

Instead:

```text
Detailed Investigation
        ↓
Select Most Important Evidence
        ↓
Key Findings
```

This allows a reader to understand the major conclusions quickly.

---

# Report Verification

Because the investigation report was written manually, I verified its values against the actual application.

I ran:

```text
python main.py
```

and checked the report against:

```text
Data quality results
Price statistics
Outlier results
Product quantities
Payment counts
Customer order counts
Customers without orders
City revenue
```

The report values matched the application output.

---

# Regression Testing

After completing the report, I ran the complete automated test suite.

```text
python -m pytest
```

The existing tests passed.

No new application functionality was added on Day 12, so new automated tests were not created solely for the Markdown report.

This reinforced an engineering principle:

```text
Add tests where they provide meaningful verification,
not simply because every day must contain new tests.
```

---

# Why Docker Was Not Rebuilt

Day 12 did not change application behavior or dependencies.

The new project artifact was:

```text
reports/data_investigation_report.md
```

The software had already been verified in Docker after the Day 11 implementation.

Therefore rebuilding the Docker image solely because a Markdown report was added was unnecessary.

---

# Week 2 Integration

At the end of Day 12, the complete Week 2 flow is:

```text
Raw CSV
   ↓
load_csv()
   ↓
Pandas DataFrames
   ↓
Validation
   ↓
Data Profiling
   ↓
Descriptive Statistics
   ↓
SQLite Persistence
   ↓
SQL Analysis
   ↓
Relational SQL Analysis
   ↓
Evidence
   ↓
Interpretation
   ↓
Data Investigation Report
```

Each day contributed a different part:

```text
Day 7
→ Real CSV ingestion

Day 8
→ Data-quality profiling

Day 9
→ SQL foundations

Day 10
→ Relational modelling and SQL analysis

Day 11
→ Descriptive statistics

Day 12
→ Data investigation and reporting
```

---

# Important Engineering Lessons

## 1. Start With Questions

Analysis should answer a question rather than exist only because a technique is available.

```text
Question
 ↓
Technique
 ↓
Evidence
```

---

## 2. Know What the Metric Measures

Never give a metric a meaning it does not have.

```text
Quantity ≠ Profit
Revenue ≠ Profit
Order Count ≠ Customer Value
```

---

## 3. Conclusions Must Match Evidence

A limited dataset supports limited conclusions.

Do not turn:

```text
highest in this dataset
```

into:

```text
best overall
```

without additional evidence.

---

## 4. Limitations Matter

A professional report explains the boundaries of its evidence.

Limitations prevent misleading conclusions.

---

## 5. Reporting Is Part of Engineering

A technically correct system that produces unreadable or unexplained results is less useful.

The final step is communicating:

```text
What happened?
Why does it matter?
How certain are we?
What should happen next?
```

---

## 6. Reuse Existing Layers

Day 12 did not require duplicating the functionality built during Days 7–11.

Instead:

```text
loader
validator
profiler
statistics
database
```

were reused to answer investigation questions.

This demonstrates the benefit of modular software design.

---

# What I Can Explain Now

I can explain:

- The difference between a result, finding, and interpretation.
- Why analysis should begin with questions.
- How to map an investigation question to an analytical technique.
- What evidence-based conclusions are.
- What overgeneralization means.
- Why a conclusion should not be stronger than its evidence.
- Why quantity does not equal revenue.
- Why revenue does not equal profit.
- Why order frequency does not equal customer value.
- Why validation cannot guarantee real-world correctness.
- Why statistical outliers require context.
- Why limitations belong in a professional report.
- Why recommendations should follow from evidence.
- Why not every calculated metric needs to appear in a report.
- The purpose of a Key Findings section.
- The difference between a project report and a Learning Journal.
- How Days 7–11 combine into a complete data investigation workflow.
- Why Day 12 did not require unnecessary new Python functions or tests.

---

# End-of-Day Status

By the end of Day 12, the Engineering Workbench evolved from a collection of analysis capabilities into a system capable of supporting a structured data investigation.

```text
Data
 ↓
Engineering Pipeline
 ↓
Analysis
 ↓
Evidence
 ↓
Interpretation
 ↓
Limitations
 ↓
Recommendations
 ↓
Professional Report
```

The final investigation report was verified against the actual program output, and the full regression test suite passed.

Day 12 completes Week 2 of Project 01:

```text
WEEK 2 — DATA INVESTIGATION + SQL + STATISTICS

Day 7   Real CSV Ingestion                    ✅
Day 8   Data-Quality Profiler                 ✅
Day 9   SQL Foundations                       ✅
Day 10  Relational Modelling + SQL Analysis   ✅
Day 11  Descriptive Statistics                ✅
Day 12  Data Investigation Report             ✅
```

The project is now ready to move into the production-service stage of Project 01.