# Day 9 — SQL Foundations and SQLite Integration

## What I Worked On

Today I introduced SQL and relational database concepts into Project 01.

Until this point, the application mainly worked with:

```text
CSV
 ↓
Pandas DataFrame
 ↓
Validation
 ↓
Profiling
```

Today the architecture was extended to include SQLite:

```text
CSV
 ↓
Pandas DataFrame
 ↓
Validation / Profiling
 ↓
SQLite Database
 ↓
SQL Queries
 ↓
Analysis Results
```

The purpose was not to replace pandas.

Instead, the goal was to understand how structured data can be persisted and queried using a relational database.

---

## Database vs Table

A database is the larger organized collection that can contain tables.

Example:

```text
workbench.db
     ↓
Database
     ↓
orders table
```

A table is a rectangular structure made of:

```text
rows
+
columns
```

It is conceptually similar to a CSV or pandas DataFrame.

Example:

```text
orders

order_id | product | price
---------|---------|------
1001     | Laptop  | 50000
1002     | Mouse   | 1000
```

---

## Why SQL When Pandas Can Analyze Data?

Pandas is excellent for:

```text
DataFrame manipulation
Data cleaning
Profiling
Statistics
In-memory analysis
```

SQL databases are useful for:

```text
Persistent structured storage
Querying stored data
Working with relational tables
Handling larger application data systems
Supporting multiple related entities
```

The project uses both:

```text
Pandas
→ process and investigate data

SQLite / SQL
→ persist and query structured data
```

This helped me understand that pandas and SQL are complementary rather than direct replacements for each other.

---

# SQL Foundations

## SELECT

`SELECT` specifies which columns should be returned.

```sql
SELECT product, price
FROM orders;
```

Meaning:

```text
orders table
     ↓
take product and price
     ↓
return those columns
```

To retrieve every column:

```sql
SELECT *
FROM orders;
```

`*` means all columns.

---

## FROM

`FROM` specifies the table being queried.

```sql
SELECT product
FROM orders;
```

Meaning:

```text
SELECT → what data do I want?
FROM   → where should SQL get it from?
```

---

## WHERE

`WHERE` filters rows.

```sql
SELECT product, price
FROM orders
WHERE price > 3000;
```

Only rows satisfying the condition are returned.

General flow:

```text
table
 ↓
WHERE condition
 ↓
matching rows
 ↓
SELECT columns
```

---

## SQL Statement Terminator

A semicolon:

```sql
;
```

marks the end of the SQL statement.

Correct:

```sql
SELECT product, price
FROM orders
WHERE price > 3000;
```

Not:

```sql
SELECT product, price
FROM orders;
WHERE price > 3000;
```

The first semicolon would end the query before `WHERE`.

---

## AND, OR and NOT

Multiple filtering conditions can be combined.

### AND

```sql
WHERE price > 2000
AND payment_method = 'UPI'
```

Both conditions must be true.

### OR

```sql
WHERE payment_method = 'UPI'
OR payment_method = 'Card'
```

At least one condition must be true.

### NOT

```sql
WHERE NOT payment_method = 'Cash'
```

Excludes rows satisfying the specified condition.

---

## ORDER BY

`ORDER BY` sorts query results.

Ascending:

```sql
ORDER BY price ASC;
```

Descending:

```sql
ORDER BY price DESC;
```

Example:

```sql
SELECT product, price
FROM orders
WHERE price > 2000
ORDER BY price DESC;
```

---

## LIMIT

`LIMIT` restricts how many rows are returned.

```sql
SELECT product, price
FROM orders
ORDER BY price DESC
LIMIT 2;
```

This returns only the first two rows after sorting.

---

## DISTINCT

`DISTINCT` removes repeated values from the query result.

```sql
SELECT DISTINCT payment_method
FROM orders;
```

Instead of repeated payment methods, SQL returns each distinct payment method once.

---

# Aggregate Functions

Aggregate functions calculate a result from multiple rows.

Important functions learned:

```text
COUNT()
SUM()
AVG()
MIN()
MAX()
```

---

## COUNT()

Counts records.

```sql
SELECT COUNT(*)
FROM orders;
```

---

## SUM()

Calculates a total.

```sql
SELECT SUM(quantity)
FROM orders;
```

Revenue can also be calculated using:

```sql
SELECT SUM(quantity * price)
FROM orders;
```

because:

```text
revenue = quantity × price
```

---

## AVG()

Calculates an average.

```sql
SELECT AVG(price)
FROM orders;
```

---

## MIN() and MAX()

```sql
SELECT MIN(price)
FROM orders;
```

returns the minimum price.

```sql
SELECT MAX(price)
FROM orders;
```

returns the maximum price.

---

# SQL Aliases

`AS` gives a query result a temporary readable name.

Example:

```sql
SELECT AVG(price) AS average_price
FROM orders;
```

This does not permanently rename the database column.

It only names the result produced by the query.

---

# GROUP BY

`GROUP BY` groups rows containing the same value so aggregate calculations can be performed for each group.

Example:

```sql
SELECT payment_method, COUNT(*) AS order_count
FROM orders
GROUP BY payment_method;
```

Conceptually:

```text
orders
   ↓
GROUP BY payment_method
   ↓
Card group
UPI group
Cash group
   ↓
COUNT each group
```

Current result:

```text
UPI  → 4
Card → 4
Cash → 2
```

---

## GROUP BY with SUM()

The project also calculates total product quantities:

```sql
SELECT
    product,
    SUM(quantity) AS total_quantity
FROM orders
GROUP BY product
ORDER BY total_quantity DESC;
```

Current result:

```text
Webcam   → 5
Mouse    → 3
Keyboard → 3
Monitor  → 2
Laptop   → 2
```

---

# WHERE vs HAVING

I learned an important distinction between:

```text
WHERE
```

and:

```text
HAVING
```

`WHERE` filters individual rows before grouping.

```text
Rows
 ↓
WHERE
 ↓
GROUP BY
```

`HAVING` filters groups after aggregation.

```text
Rows
 ↓
GROUP BY
 ↓
Aggregate
 ↓
HAVING
```

Example:

```sql
SELECT
    product,
    SUM(quantity) AS total_quantity
FROM orders
GROUP BY product
HAVING SUM(quantity) > 2;
```

Rule:

```text
WHERE
→ filter rows

HAVING
→ filter aggregated groups
```

---

# SQLite Integration

## Why SQLite?

SQLite provides a lightweight relational database that can be used directly from Python without running a separate database server.

The project database is:

```text
data/processed/workbench.db
```

Python provides SQLite support through:

```python
import sqlite3
```

---

## Database Layer

I added:

```text
src/data_loader/database.py
```

This module contains reusable database functionality.

This maintains separation of responsibilities:

```text
loader.py
→ load data

validator.py
→ validate data

profiler.py
→ profile data

database.py
→ database operations and SQL queries

main.py
→ coordinate the application
```

---

## Database Connection

The database connection is created using:

```python
sqlite3.connect(database_path)
```

The project wraps this in:

```python
create_connection()
```

Conceptually:

```text
DATABASE_PATH
      ↓
create_connection()
      ↓
sqlite3.connect()
      ↓
SQLite connection
      ↓
workbench.db
```

The connection is then used to execute SQL statements.

---

# CREATE TABLE

I learned how SQL tables can be explicitly created.

Example:

```sql
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    order_date TEXT NOT NULL,
    payment_method TEXT NOT NULL
);
```

Important concepts introduced:

```text
INTEGER
REAL
TEXT
PRIMARY KEY
NOT NULL
```

`IF NOT EXISTS` prevents an error when the table already exists.

---

## PRIMARY KEY

A primary key uniquely identifies a row.

Example:

```sql
order_id INTEGER PRIMARY KEY
```

Each order should have a unique `order_id`.

---

## NOT NULL

`NOT NULL` means the column is not allowed to contain a SQL `NULL` value.

Example:

```sql
product TEXT NOT NULL
```

---

# Committing Database Changes

After database-changing operations, SQLite changes can be committed using:

```python
connection.commit()
```

This saves the current transaction.

---

# Pandas DataFrame → SQLite

The project uses pandas:

```python
data.to_sql(
    table_name,
    connection,
    if_exists="replace",
    index=False,
)
```

This allows a DataFrame to be written directly into SQLite.

Flow:

```text
orders_week2.csv
       ↓
load_csv()
       ↓
Pandas DataFrame
       ↓
to_sql()
       ↓
SQLite
       ↓
orders table
```

---

## `if_exists="replace"`

```python
if_exists="replace"
```

means:

```text
If the table already exists
        ↓
replace it
        ↓
write the current DataFrame
```

This makes development convenient but has an important architectural consequence:

A table manually created with constraints can be replaced by a new pandas-generated table.

Therefore manually defined constraints such as:

```text
PRIMARY KEY
NOT NULL
```

may not remain after replacement.

This became important when thinking about the future relational database architecture.

---

## `index=False`

A pandas DataFrame normally has an index:

```text
0
1
2
3
...
```

Using:

```python
index=False
```

prevents this pandas index from becoming an unnecessary SQL table column.

---

# Executing SQL from Python

SQL can be executed through the SQLite connection.

Example:

```python
result = connection.execute(
    """
    SELECT *
    FROM orders;
    """
)
```

Flow:

```text
Python
 ↓
connection.execute()
 ↓
SQL statement
 ↓
SQLite
 ↓
query result
```

---

# `fetchall()`

After executing a query:

```python
result.fetchall()
```

retrieves all remaining rows.

Example:

```python
[
    ("UPI", 4),
    ("Card", 4),
    ("Cash", 2),
]
```

---

# `fetchone()`

```python
result.fetchone()
```

retrieves one row from the query result.

---

# Inspecting SQLite Tables

SQLite stores information about its schema in:

```text
sqlite_master
```

I used:

```sql
SELECT name
FROM sqlite_master
WHERE type = 'table';
```

Initially:

```text
[]
```

showed that the database contained no tables.

After creating/writing the orders table:

```text
[('orders',)]
```

confirmed that the table existed.

---

# Parameterized Queries

I learned to pass dynamic values separately from the SQL query.

Example:

```python
result = connection.execute(
    """
    SELECT product, price
    FROM orders
    WHERE price > ?
    ORDER BY price DESC;
    """,
    (minimum_price,),
)
```

Here:

```text
?
```

is the SQL parameter placeholder.

And:

```python
(minimum_price,)
```

contains the value supplied to it.

This is preferable to directly inserting dynamic values into SQL strings.

---

## One-Element Tuple

Python syntax:

```python
(minimum_price,)
```

creates a tuple containing one item.

The comma is important.

```python
(3000,)   # tuple

(3000)    # integer inside parentheses
```

---

# Reusable SQL Functions

The database layer was expanded with reusable SQL operations.

Examples included:

```text
create_connection()
create_orders_table()
write_dataframe_to_table()
get_all_orders()
get_expensive_orders()
get_payment_method_counts()
get_product_quantity_totals()
```

This means `main.py` does not need to contain all the SQL itself.

Instead:

```text
main.py
   ↓
database.py
   ↓
SQL
   ↓
SQLite
```

---

# Expensive Orders Query

The project uses a parameterized query to retrieve orders above a chosen price.

Example call:

```python
get_expensive_orders(
    connection,
    minimum_price=3000,
)
```

Current result:

```text
Laptop  → 50000
Laptop  → 50000
Monitor → 15000
Monitor → 15000
```

---

# Payment Method Analysis

Using:

```sql
GROUP BY payment_method
```

with:

```sql
COUNT(*)
```

the project calculates how many orders use each payment method.

Current result:

```text
UPI  → 4
Card → 4
Cash → 2
```

---

# Product Quantity Analysis

Using:

```sql
GROUP BY product
```

with:

```sql
SUM(quantity)
```

the project calculates total quantities ordered for each product.

Current result:

```text
Webcam   → 5
Mouse    → 3
Keyboard → 3
Monitor  → 2
Laptop   → 2
```

---

# Automated Database Testing

I added:

```text
tests/test_database.py
```

The database layer is tested using temporary SQLite databases.

Example:

```python
database_path = tmp_path / "test.db"
```

This means:

```text
pytest
 ↓
creates temporary directory
 ↓
test.db
 ↓
run database test
 ↓
temporary test environment removed later
```

The real:

```text
data/processed/workbench.db
```

is not modified by the tests.

This keeps database tests isolated and repeatable.

---

## What the Database Tests Verify

The Day 9 database tests verify functionality such as:

```text
Database connection
Table creation
DataFrame → SQLite persistence
SQL filtering
SQL sorting
GROUP BY + COUNT
GROUP BY + SUM
```

After implementing the database layer, the complete project test suite passed.

---

# Generated Database File and Git

During the Git workflow, the generated:

```text
workbench.db
```

was accidentally committed.

I learned that a generated local database usually does not need to be stored in Git when the application can recreate it.

The file was removed from Git tracking using:

```bash
git rm --cached Projects/Project-01-Engineering-Workbench/data/processed/workbench.db
```

`--cached` means:

```text
stop tracking with Git
but
keep the local file
```

---

# `.gitignore`

I added:

```text
*.db
```

to `.gitignore`.

Purpose:

```text
*.db
 ↓
Git ignores generated SQLite database files
```

---

# `.dockerignore`

I also added:

```text
*.db
```

to `.dockerignore`.

Purpose:

```text
*.db
 ↓
existing local database files are not copied
into the Docker image during docker build
```

The application can create its own database when it runs.

---

# Important Distinction

```text
.gitignore
→ controls what Git tracks

.dockerignore
→ controls what Docker copies into the image
```

The same pattern:

```text
*.db
```

can therefore serve two different purposes depending on which file contains it.

---

# Engineering Lessons

## Pandas and SQL Solve Different Problems

I learned not to think:

```text
Pandas OR SQL
```

but rather:

```text
Pandas + SQL
```

For this project:

```text
Pandas
→ loading
→ validation support
→ profiling
→ DataFrame analysis

SQLite / SQL
→ persistent relational storage
→ structured queries
→ aggregation
→ foundation for multi-table relationships
```

---

## Database Logic Belongs in Its Own Layer

Instead of placing SQL everywhere in `main.py`, database operations are encapsulated in:

```text
database.py
```

This makes the application easier to:

```text
understand
test
modify
debug
reuse
```

---

## Tests Should Not Depend on the Real Database

Using:

```python
tmp_path
```

with temporary SQLite databases gives each test a controlled environment.

This follows the same principle already used in the file-loader tests:

> Tests should control their own inputs and avoid depending unnecessarily on real application files.

---

# What I Can Explain Now

I can explain:

- What a database is.
- What a database table is.
- Why SQL is useful even though pandas can analyze data.
- What `SELECT` and `FROM` do.
- How `WHERE` filters rows.
- How `ORDER BY` sorts results.
- How `LIMIT` restricts results.
- What `DISTINCT` does.
- What `COUNT`, `SUM`, `AVG`, `MIN`, and `MAX` do.
- What SQL aliases are.
- How `GROUP BY` works.
- The difference between `WHERE` and `HAVING`.
- What SQLite is.
- How Python connects to SQLite.
- What `CREATE TABLE` does.
- What `PRIMARY KEY` and `NOT NULL` mean.
- How a pandas DataFrame can be written into SQLite.
- What `if_exists="replace"` does.
- Why `index=False` is used.
- How `connection.execute()` sends SQL to SQLite.
- The difference between `fetchall()` and `fetchone()`.
- What a parameterized query is.
- Why `(value,)` has a comma.
- Why database tests use temporary databases.
- Why generated `.db` files are ignored by Git and Docker.

---

# End-of-Day Status

By the end of Day 9, Project 01 had evolved from:

```text
CSV
 ↓
Pandas
 ↓
Validation
 ↓
Profiling
```

into:

```text
CSV
 ↓
Pandas DataFrame
 ↓
Validation
 ↓
Profiling
 ↓
SQLite Database
 ↓
SQL Queries
 ↓
Analysis Results
```

The application could now:

```text
Load structured data
        ↓
Validate and profile it
        ↓
Persist it in SQLite
        ↓
Execute reusable SQL queries
        ↓
Return analysis results to Python
```

This established the SQL foundation required for Day 10, where the project would move from a single `orders` table to multiple related tables and relational SQL analysis.

The application and complete automated test suite were successfully verified locally and inside Docker.