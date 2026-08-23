# Day 10 — Relational Modelling and SQL Analysis

## What I Worked On

Today I extended Project 01 from working with a single SQL table into working with multiple related tables.

Before Day 10, the database mainly contained:

```text
orders
```

Today I introduced:

```text
customers
```

and connected the two tables using:

```text
customer_id
```

This allowed the project to move from single-table SQL queries to relational SQL analysis using joins.

---

# Starting Architecture

At the beginning of Day 10, the project already had:

```text
orders_week2.csv
       ↓
Pandas DataFrame
       ↓
Validation
       ↓
Profiling
       ↓
SQLite
       ↓
orders table
       ↓
SQL analysis
```

The main limitation was that all SQL analysis was based on one table.

To learn relational databases properly, I needed multiple related entities.

---

# Creating the Customers Dataset

I created:

```text
data/raw/customers_week2.csv
```

with columns:

```text
customer_id
customer_name
city
```

The dataset contains customers corresponding to the customer IDs already present in the orders dataset.

I also added:

```text
Kiran
customer_id = 6
city = Pune
```

without creating an order for him.

This deliberately created an unmatched customer so I could understand the difference between `INNER JOIN` and `LEFT JOIN`.

---

# Multiple Dataset Configuration

Previously, the project had a generic:

```python
DATA_PATH
```

Once the application started working with multiple datasets, this name became unclear.

I changed the configuration to use:

```python
ORDERS_DATA_PATH
CUSTOMERS_DATA_PATH
DATABASE_PATH
```

Example:

```python
ORDERS_DATA_PATH = Path("data/raw/orders_week2.csv")
CUSTOMERS_DATA_PATH = Path("data/raw/customers_week2.csv")
DATABASE_PATH = Path("data/processed/workbench.db")
```

This taught me that configuration names should become more specific as an application grows.

---

# Loading Multiple DataFrames

The application now loads both datasets:

```python
orders = load_csv(
    ORDERS_DATA_PATH,
    parse_dates=["order_date"],
)

customers = load_csv(CUSTOMERS_DATA_PATH)
```

This produces:

```text
orders_week2.csv
       ↓
orders DataFrame

customers_week2.csv
       ↓
customers DataFrame
```

The orders dataset uses:

```python
parse_dates=["order_date"]
```

because it contains a date column.

The customers dataset does not require date parsing.

---

# Relational Modelling

The two datasets represent different entities:

```text
CUSTOMERS

customer_id
customer_name
city
```

and:

```text
ORDERS

order_id
customer_id
product
quantity
price
order_date
payment_method
```

The common column is:

```text
customer_id
```

This column creates the logical relationship between the two tables.

---

# Primary Key

A Primary Key uniquely identifies a row in its own table.

Conceptually:

```text
customers.customer_id
        ↓
PRIMARY KEY
```

For example:

```text
1 → Arjun
2 → Priya
3 → Rahul
4 → Neha
5 → Aisha
6 → Kiran
```

Each customer has a unique customer ID.

---

# Foreign Key

A Foreign Key refers to a key in another table.

Conceptually:

```text
orders.customer_id
        ↓
FOREIGN KEY
        ↓
customers.customer_id
```

For example:

```text
order 1002
customer_id = 2
       ↓
customers.customer_id = 2
       ↓
Priya
```

This allows an order to be associated with the correct customer.

---

# One-to-Many Relationship

The relationship between customers and orders is:

```text
ONE customer
     ↓
can have
     ↓
MANY orders
```

For example:

```text
Priya
customer_id = 2
      │
      ├── order 1002
      ├── order 1004
      └── order 1010
```

Therefore:

```text
customers 1 ─────────< many orders
```

This is a one-to-many relationship.

---

# Important Architectural Limitation

The current project uses:

```python
data.to_sql(
    table_name,
    connection,
    if_exists="replace",
    index=False,
)
```

This means pandas can recreate the SQLite table.

Therefore, although I model:

```text
customers.customer_id → Primary Key
orders.customer_id    → Foreign Key
```

the relationship is currently logical rather than an SQLite-enforced foreign-key constraint.

The SQL queries use the relationship correctly, but SQLite is not currently enforcing it.

A stricter future design could explicitly create the schema and insert data without replacing the tables.

---

# Writing Multiple Tables to SQLite

The application now writes both DataFrames into SQLite:

```python
write_dataframe_to_table(
    connection,
    orders,
    "orders",
)

write_dataframe_to_table(
    connection,
    customers,
    "customers",
)
```

The database therefore contains:

```text
workbench.db
│
├── orders
│
└── customers
```

This created the foundation for relational SQL queries.

---

# INNER JOIN

I implemented my first relational SQL JOIN.

The query combines customer information with order information:

```sql
SELECT
    orders.order_id,
    customers.customer_name,
    customers.city,
    orders.product,
    orders.quantity,
    orders.price
FROM orders
INNER JOIN customers
    ON orders.customer_id = customers.customer_id
ORDER BY orders.order_id;
```

The important part is:

```sql
INNER JOIN customers
    ON orders.customer_id = customers.customer_id
```

Meaning:

```text
Take an order
     ↓
look at its customer_id
     ↓
find a customer with the same customer_id
     ↓
combine the information
```

Example:

```text
orders:

1002 | customer_id 2 | Mouse
                │
                │ match
                ▼
customers:

2 | Priya | Bengaluru
```

Result:

```text
1002 | Priya | Bengaluru | Mouse | 2 | 1000
```

---

# INNER JOIN Rule

The main rule I learned is:

```text
INNER JOIN
→ returns rows where a matching relationship exists
  in both tables
```

If a customer has no corresponding order, that customer does not appear when the query requires a matching order.

---

# Qualified Column Names

When multiple tables are involved, columns can be written as:

```sql
orders.order_id
customers.customer_name
customers.city
orders.product
```

The format is:

```text
table.column
```

This clearly identifies which table a column belongs to.

It becomes especially important because both tables contain:

```text
customer_id
```

Therefore:

```sql
orders.customer_id
```

and:

```sql
customers.customer_id
```

are explicitly distinguishable.

---

# The `ON` Clause

The `ON` clause defines the relationship used by a JOIN.

Project 01 uses:

```sql
ON orders.customer_id = customers.customer_id
```

This tells SQL which rows from the two tables belong together.

---

# LEFT JOIN

I then learned `LEFT JOIN`.

Example:

```sql
FROM customers
LEFT JOIN orders
    ON customers.customer_id = orders.customer_id
```

A `LEFT JOIN` keeps every row from the table on the left.

Since:

```text
customers
```

is the left table, every customer remains in the result.

---

# Why Kiran Was Added

Kiran has:

```text
customer_id = 6
```

but there is no order with:

```text
customer_id = 6
```

With an `INNER JOIN`, there is no matching order.

With:

```sql
FROM customers
LEFT JOIN orders
```

Kiran is still retained.

The result looks conceptually like:

```text
6 | Kiran | Pune | NULL | NULL
```

This allowed me to see the practical difference between the two JOIN types.

---

# INNER JOIN vs LEFT JOIN

```text
INNER JOIN
→ keep matching rows

LEFT JOIN
→ keep every row from the left table
→ attach matching right-table data
→ use NULL when no match exists
```

Example:

```text
Customer    Has Order    INNER JOIN    LEFT JOIN
-------------------------------------------------
Arjun          Yes           Yes           Yes
Priya          Yes           Yes           Yes
Kiran          No            No            Yes
```

---

# SQL NULL and Python None

When SQL has no value for a joined column, it uses:

```sql
NULL
```

When SQLite returns that result to Python, it becomes:

```python
None
```

Example:

```text
SQL:

Kiran | Pune | NULL | NULL
```

becomes:

```python
(6, "Kiran", "Pune", None, None)
```

---

# Finding Customers Without Orders

I implemented:

```python
get_customers_without_orders()
```

using:

```sql
SELECT
    customers.customer_id,
    customers.customer_name,
    customers.city
FROM customers
LEFT JOIN orders
    ON customers.customer_id = orders.customer_id
WHERE orders.order_id IS NULL;
```

The important pattern is:

```sql
LEFT JOIN ...
WHERE right_table.key IS NULL
```

Flow:

```text
customers
    ↓
LEFT JOIN orders
    ↓
keep all customers
    ↓
customers without orders receive NULL
    ↓
WHERE orders.order_id IS NULL
    ↓
only unmatched customers
```

The result identifies:

```text
Kiran
```

as the customer without an order.

---

# `IS NULL`

SQL checks for NULL values using:

```sql
IS NULL
```

For example:

```sql
WHERE orders.order_id IS NULL
```

I should not use:

```sql
= NULL
```

for this check.

---

# JOIN + GROUP BY

I then combined the Day 9 `GROUP BY` knowledge with Day 10 JOINs.

The first business question was:

> How many orders has each customer placed?

The query uses:

```sql
SELECT
    customers.customer_name,
    COUNT(orders.order_id) AS order_count
FROM customers
LEFT JOIN orders
    ON customers.customer_id = orders.customer_id
GROUP BY
    customers.customer_id,
    customers.customer_name
ORDER BY order_count DESC;
```

Flow:

```text
customers
    +
orders
    ↓
LEFT JOIN
    ↓
combined rows
    ↓
GROUP BY customer
    ↓
COUNT orders
    ↓
ORDER BY count
```

The result was:

```text
Priya → 3
Arjun → 2
Rahul → 2
Aisha → 2
Neha  → 1
Kiran → 0
```

---

# COUNT(*) vs COUNT(column)

This was an important SQL detail.

```sql
COUNT(*)
```

counts rows.

But:

```sql
COUNT(orders.order_id)
```

counts only non-NULL `order_id` values.

For Kiran, the LEFT JOIN creates a row with:

```text
order_id = NULL
```

Therefore:

```sql
COUNT(orders.order_id)
```

returns:

```text
0
```

for Kiran.

This is why the project uses:

```sql
COUNT(orders.order_id)
```

instead of blindly using:

```sql
COUNT(*)
```

---

# Multi-Table Business Analysis

The next question was:

> Which city generated the most revenue?

The required information exists in two tables:

```text
customers
→ city

orders
→ quantity
→ price
```

Neither table alone contains everything required.

Therefore I used an `INNER JOIN`.

---

# Revenue by City

The query is:

```sql
SELECT
    customers.city,
    SUM(orders.quantity * orders.price) AS revenue
FROM customers
INNER JOIN orders
    ON customers.customer_id = orders.customer_id
GROUP BY customers.city
ORDER BY revenue DESC;
```

The calculation for each order is:

```text
revenue = quantity × price
```

SQL performs this with:

```sql
orders.quantity * orders.price
```

Then:

```sql
SUM(orders.quantity * orders.price)
```

calculates total revenue.

Finally:

```sql
GROUP BY customers.city
```

calculates the total separately for each city.

---

# Revenue Results

The project produced:

```text
Chennai    → 52000
Kochi      → 51000
Bengaluru  → 26000
Hyderabad  → 21000
Mumbai     → 4000
```

This demonstrated how SQL can combine information from different tables to answer a business question.

---

# Relational Analysis Pattern

A major pattern learned today was:

```text
JOIN
 ↓
combine related tables
 ↓
GROUP BY
 ↓
create analytical groups
 ↓
COUNT / SUM
 ↓
calculate metrics
 ↓
ORDER BY
 ↓
rank results
```

---

# Database Functions Added

The database layer was expanded with reusable relational functions including:

```text
get_customer_order_details()
get_all_customers_with_orders()
get_customers_without_orders()
get_orders_per_customer()
get_revenue_by_city()
```

This keeps relational SQL logic inside:

```text
database.py
```

instead of putting raw SQL throughout `main.py`.

---

# Updated Application Architecture

The application now follows:

```text
orders_week2.csv             customers_week2.csv
       ↓                             ↓
orders DataFrame              customers DataFrame
       │                             │
       ├─────────────┬───────────────┤
                     ↓
              SQLite Database
                     ↓
           ┌───────────────────┐
           │ orders  customers │
           └─────────┬─────────┘
                     │
                customer_id
                     ↓
                  JOINs
                     ↓
            Relational Analysis
                     ↓
        COUNT / SUM / GROUP BY
                     ↓
            Business Results
```

---

# Automated Testing

I expanded:

```text
tests/test_database.py
```

to test the relational database functionality.

The tests use:

```python
tmp_path
```

to create isolated temporary SQLite databases.

This prevents tests from modifying:

```text
data/processed/workbench.db
```

---

# INNER JOIN Test

I created controlled:

```text
orders
+
customers
```

DataFrames and verified that the JOIN produced the expected combined rows.

This confirms that:

```text
orders.customer_id
```

is being matched correctly with:

```text
customers.customer_id
```

---

# LEFT JOIN Test

The LEFT JOIN test included a customer without an order.

Expected result:

```python
(2, "Kiran", "Pune", None, None)
```

This verifies that unmatched customers are preserved.

---

# Customers Without Orders Test

I tested:

```python
get_customers_without_orders()
```

using a controlled customer with no matching order.

The expected result contained only the unmatched customer.

This verifies:

```sql
LEFT JOIN
+
IS NULL
```

behavior.

---

# Orders Per Customer Test

The controlled test contained:

```text
Arjun → 2 orders
Priya → 1 order
Kiran → 0 orders
```

The test verifies:

```text
LEFT JOIN
+
GROUP BY
+
COUNT(orders.order_id)
```

It also confirms that a customer without an order receives a count of:

```text
0
```

rather than `1`.

---

# Revenue by City Test

I created controlled order values where the expected revenue could be calculated manually.

Example:

```text
Kochi:

1 × 1000 = 1000
2 × 500  = 1000

Total = 2000
```

and:

```text
Pune:

3 × 200 = 600
```

The SQL result was tested against these known values.

This reinforced the idea that tests should use small inputs whose expected outputs can be calculated independently.

---

# Regression Testing

After adding the relational functionality, I ran the complete project test suite:

```bash
python -m pytest
```

The full suite passed.

This confirmed that the new relational database functionality did not break the existing:

```text
loader
validator
profiler
Day 9 database functionality
```

---

# Docker Verification

After the local tests passed, I rebuilt the Docker image:

```bash
docker build -t engineering-workbench .
```

I then ran the application:

```bash
docker run --rm engineering-workbench
```

and ran the complete test suite inside Docker:

```bash
docker run --rm engineering-workbench python -m pytest
```

Both succeeded.

This verifies that the expanded relational application works in both:

```text
Local Windows development environment
                +
Docker Linux environment
```

---

# Problems / Debugging

## Undefined `orders`

While refactoring from:

```python
data
```

to:

```python
orders
```

VS Code reported `orders` as undefined.

The cause was that variable names need to remain consistent.

If I create:

```python
data = load_csv(...)
```

then:

```python
validate_required_columns(orders)
```

cannot work because `orders` was never defined.

The fix was:

```python
orders = load_csv(...)
```

and then consistently using:

```python
orders
```

throughout the application.

---

## Using a Closed Database Connection

While editing `main.py`, I accidentally duplicated database operations after:

```python
connection.close()
```

This would attempt to use a database connection after it had already been closed.

Correct lifecycle:

```text
create connection
      ↓
write tables
      ↓
execute queries
      ↓
retrieve results
      ↓
close connection
```

Not:

```text
close connection
      ↓
attempt more database operations
```

I removed the duplicated block and kept:

```python
connection.close()
```

as the final database operation.

---

# Important Engineering Lessons

## Applications Evolve Beyond Generic Names

When only one dataset existed:

```python
DATA_PATH
```

was understandable.

When multiple datasets were introduced:

```python
ORDERS_DATA_PATH
CUSTOMERS_DATA_PATH
```

became clearer.

Variable and configuration names should evolve as the application becomes more complex.

---

## Relationships Unlock New Questions

With only `orders`, I could answer:

```text
Which products are expensive?
How many orders use UPI?
How many units of each product were ordered?
```

After introducing `customers`, I could answer:

```text
Who placed each order?
Which customers have no orders?
How many orders did each customer place?
Which city generated the most revenue?
```

This is the main benefit of relational modelling.

---

## SQL Queries Can Combine Concepts

SQL concepts are not isolated.

A real analytical query can combine:

```text
JOIN
+
GROUP BY
+
SUM
+
ORDER BY
```

or:

```text
LEFT JOIN
+
WHERE
+
IS NULL
```

Understanding how these pieces work together is more important than memorizing them individually.

---

## Tests Should Include Edge Cases

Kiran was intentionally given no orders.

This created an edge case that allowed me to test:

```text
LEFT JOIN
NULL
IS NULL
COUNT(column)
```

Testing only customers with existing orders would not have properly verified these behaviors.

---

# What I Can Explain Now

I can explain:

- Why relational databases use multiple tables.
- Why customer information should not be unnecessarily repeated in every order.
- What a Primary Key is.
- What a Foreign Key is.
- What a one-to-many relationship is.
- How `customer_id` relates customers and orders.
- The current difference between the project's logical relationship and an SQLite-enforced foreign key.
- What an `INNER JOIN` does.
- What a `LEFT JOIN` does.
- The difference between `INNER JOIN` and `LEFT JOIN`.
- What the `ON` clause does.
- Why qualified column names such as `orders.customer_id` are useful.
- What SQL `NULL` means.
- Why SQLite `NULL` becomes Python `None`.
- Why SQL uses `IS NULL`.
- How to find records without a related record.
- How `JOIN` and `GROUP BY` work together.
- The difference between `COUNT(*)` and `COUNT(column)`.
- How to calculate orders per customer.
- How to calculate revenue across related tables.
- Why relational database functions belong in `database.py`.
- How to test JOIN behavior using temporary SQLite databases.
- Why edge cases such as customers without orders should be tested.
- Why a database connection must remain open while queries are being executed.

---

# End-of-Day Status

By the end of Day 10, Project 01 evolved from:

```text
One SQL table
      ↓
single-table analysis
```

into:

```text
customers ────────┐
                  │ customer_id
                  ↓
               SQL JOIN
                  ↑
                  │ customer_id
orders ───────────┘
       ↓
Relational SQL Analysis
       ↓
Business Results
```

The project can now:

```text
Load multiple related datasets
        ↓
Store them as separate SQL tables
        ↓
Model a one-to-many relationship
        ↓
Combine tables with JOINs
        ↓
Find unmatched relationships
        ↓
Aggregate across tables
        ↓
Produce relational business analysis
```

The complete application and automated test suite were successfully verified locally and inside Docker.

Day 10 established the relational SQL foundation needed for more advanced data investigation and analysis in the remaining Week 2 work.