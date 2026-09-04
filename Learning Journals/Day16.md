# Day 16 — Analytical API Endpoint

## Day 16 Goal

The goal of Day 16 was to move beyond the basic FastAPI endpoints created on Day 15 and connect the API to the real functionality of the Engineering Workbench.

Day 15 proved that FastAPI, Uvicorn, routing, HTTP responses, Swagger and API testing worked.

Day 16 focused on:

- exposing real profiling functionality through FastAPI
- exposing database analysis through FastAPI
- keeping API routes thin
- reusing the existing service layer
- improving the service architecture where necessary
- validating API inputs safely
- testing the new endpoints
- ensuring existing CLI and service functionality still worked after refactoring
- verifying the application inside Docker

The main architectural goal was:

```text
Client
  ↓
HTTP Request
  ↓
FastAPI
  ↓
Service Layer
  ↓
Existing Engineering Workbench Logic
  ↓
JSON Response
```

Rather than rebuilding profiler or database logic inside the API.


---

# What I Built

## 1. Real `/profile` Endpoint

I added a real analytical endpoint:

```text
GET /profile
```

A request can specify one of the supported datasets:

```text
GET /profile?dataset=orders
```

or:

```text
GET /profile?dataset=customers
```

The API then maps the logical dataset name to the actual server-side file path and calls the existing:

```python
run_profile(...)
```

service function.

The flow is:

```text
HTTP request
    ↓
FastAPI /profile
    ↓
dataset selection
    ↓
server-controlled file path
    ↓
run_profile()
    ↓
load_csv()
    ↓
profile_data()
    ↓
profile result
    ↓
JSON response
```

I tested the endpoint through Swagger and confirmed that it returned the real profiler output, including information such as:

```text
shape
columns
missing values
missing percentages
unique counts
duplicate count
data types
numeric summary
categorical summary
```


---

## 2. Real `/database` Endpoint

I also added:

```text
GET /database
```

The route delegates directly to:

```python
run_database_analysis()
```

The API itself does not contain SQL or database-processing logic.

The flow is:

```text
GET /database
      ↓
FastAPI
      ↓
run_database_analysis()
      ↓
load and validate orders
      ↓
load customers
      ↓
SQLite database operations
      ↓
SQL analysis
      ↓
results
      ↓
JSON response
```

The returned database analysis includes sections such as:

```text
expensive_orders
payment_counts
product_totals
customer_order_details
all_customers_with_orders
customers_without_orders
orders_per_customer
revenue_by_city
```


---

# Major Design Decisions

## Decision 1 — Do Not Accept Arbitrary File Paths from API Clients

One of the first API designs considered was:

```text
/profile?path=data/raw/orders_week2.csv
```

This would allow the client to specify the server filesystem path directly.

After discussing the design, I realized this was not a good public API contract.

### Problems with this approach

#### Security

A client should not have unrestricted control over which server-side filesystem path is accessed.

Poorly controlled paths can potentially create unintended file-access or path-traversal problems.

#### Encapsulation

A client should not need to understand the internal directory structure of the application.

The client should know:

```text
orders
```

rather than:

```text
data/raw/orders_week2.csv
```

#### Maintainability

If the server directory structure changes later, clients should not have to change their requests.

### Solution Chosen

I used logical dataset names:

```text
/profile?dataset=orders
```

with a server-controlled mapping:

```python
DATASETS = {
    "orders": "data/raw/orders_week2.csv",
    "customers": "data/raw/customers_week2.csv",
}
```

This means:

```text
Client chooses WHAT it wants
          ↓
Server decides WHERE it exists
```


---

## Decision 2 — How Should Invalid Dataset Names Be Handled?

Initially the endpoint parameter could simply be:

```python
dataset: str
```

The problem is that `str` accepts any string.

For example:

```text
orders
customers
banana
hello
xyz
```

would all satisfy the Python type requirement.

### First Solution Considered

One option was manual validation:

```python
if dataset not in DATASETS:
    raise HTTPException(
        status_code=404,
        detail=f"Dataset '{dataset}' not found",
    )
```

This would allow the application to manually reject unknown datasets.

I also considered improving Swagger documentation using FastAPI's `Query` functionality so users could understand what values were expected.

### Better Solution Chosen

Because the list of datasets is small and fixed, I used:

```python
from typing import Literal
```

and:

```python
dataset: Literal["orders", "customers"]
```

Now the API contract itself says that only these two values are valid.

Benefits:

- FastAPI performs the validation automatically.
- Invalid values are rejected before the route executes.
- Swagger can show the allowed values.
- The user does not have to guess what dataset names are accepted.
- Manual validation code is unnecessary for this particular constraint.

An invalid request such as:

```text
/profile?dataset=banana
```

produces:

```text
422
```

because the supplied input violates the declared request constraint.

This also helped me understand the difference between:

```text
404 → requested resource could not be found

422 → request input does not satisfy the declared validation requirements
```


---

# Major Service-Layer Refactor

## Original Situation

Before the refactor, database analysis expected an orders DataFrame:

```python
run_database_analysis(orders)
```

The CLI obtained that DataFrame through:

```python
analysis_results = run_analysis()
```

and then:

```python
run_database_analysis(
    analysis_results["orders"]
)
```

Conceptually:

```text
CLI
 ↓
run_analysis()
 ↓
load orders
 ↓
validate orders
 ↓
profile
 ↓
statistics
 ↓
outliers
 ↓
return orders
 ↓
extract orders
 ↓
run_database_analysis(orders)
```

This worked, but it meant database analysis depended on executing a much broader analysis workflow simply to obtain validated orders.


---

## Initial Refactoring Idea

The first idea was to make:

```python
run_database_analysis()
```

load the orders dataset itself.

That would allow the CLI and API to simply call:

```python
run_database_analysis()
```

However, there was an important issue with doing this carelessly.


---

## Problem I Caught — `run_analysis()` Was Doing More Than Loading

`run_analysis()` did not simply load the orders dataset.

It also performed:

```python
validate_required_columns(orders)
validate_order_values(orders)
```

Therefore simply removing `run_analysis()` from the database workflow and loading the CSV directly could have accidentally removed validation.

That would have created a weaker database workflow.

The correct question became:

> What part of `run_analysis()` is genuinely shared by both workflows?

The answer was:

```text
load orders
+
validate orders
```


---

## Final Solution — `load_and_validate_orders()`

I extracted the shared preparation work into:

```python
def load_and_validate_orders():
    orders = load_csv(
        ORDERS_DATA_PATH,
        parse_dates=["order_date"],
    )

    validate_required_columns(orders)
    validate_order_values(orders)

    return orders
```

Now both service workflows can reuse it.

### `run_analysis()`

```text
run_analysis()
      ↓
load_and_validate_orders()
      ↓
profile
      ↓
statistics
      ↓
outliers
```

### `run_database_analysis()`

```text
run_database_analysis()
      ↓
load_and_validate_orders()
      ↓
load customers
      ↓
database operations
      ↓
SQL analysis
```

The resulting architecture is:

```text
                 load_and_validate_orders()
                         │
              ┌──────────┴──────────┐
              ↓                     ↓
       run_analysis()       run_database_analysis()
              ↓                     ↓
           Profile               SQLite
         Statistics                SQL
          Outliers               Analysis
```

This was cleaner because neither major workflow has to execute the other just to obtain shared prepared data.


---

# Difficulties and Errors Encountered

## Difficulty 1 — Refactoring Without Losing Validation

The database service initially depended on data returned from:

```python
run_analysis()
```

It was tempting to remove that dependency by simply loading orders directly inside database analysis.

However, this would have overlooked the validation performed inside `run_analysis()`.

### Solution

I separated the genuinely shared responsibility into:

```python
load_and_validate_orders()
```

### Lesson

When refactoring, I should not only ask:

> What data does this function return?

I should also ask:

> What important work happens before that data is returned?

Otherwise, simplifying a dependency can accidentally remove important behavior.


---

## Difficulty 2 — Indentation Problem During the Service Refactor

While editing `service.py`, the structure around the database connection and `try/finally` block became incorrect.

This produced an error indicating that the `try` statement did not have the required matching structure.

The problem came from incorrect indentation during the refactor.

### Solution

I restored the intended structure so that the database operations remained inside:

```python
try:
    ...
finally:
    connection.close()
```

### Why `finally` Matters

The database connection should be closed even if an error occurs during one of the database operations.

The structure therefore remains:

```text
open connection
      ↓
try
      ↓
perform database work
      ↓
finally
      ↓
close connection
```

### Lesson

Python indentation is not cosmetic.

Indentation determines program structure, especially around constructs such as:

```text
functions
if statements
loops
try/finally
```

During refactoring, moving blocks of code can accidentally change the structure of the program.


---

## Difficulty 3 — Accidentally Removing `run_analysis()`

During the service-layer refactor, `run_analysis()` was accidentally removed from `service.py`.

This caused an import error similar to:

```text
ImportError:
cannot import name 'run_analysis'
from 'engineering_workbench.service'
```

### Why It Happened

The package interface still expected:

```python
run_analysis
```

to exist.

However, the actual function definition had disappeared from `service.py`.

Therefore the package import chain could no longer resolve the function.

### Solution

I restored:

```python
run_analysis()
```

and changed it to reuse:

```python
load_and_validate_orders()
```

instead of duplicating the loading and validation logic.

### Lesson

Refactoring shared code does not mean existing public operations should automatically be deleted.

I need to distinguish between:

```text
extracting shared implementation
```

and:

```text
removing an existing service capability
```


---

## Difficulty 4 — New API Tests Passed but the Full Suite Failed

After implementing the new API functionality, the API-specific tests worked.

However, running the full regression suite revealed a failure in an older service test.

The error was:

```text
TypeError:
run_database_analysis() takes 0 positional arguments
but 1 was given
```

The old test still did:

```python
analysis_results = run_analysis()

results = run_database_analysis(
    analysis_results["orders"]
)
```

But the new service contract was:

```python
run_database_analysis()
```

### Cause

The production function had been refactored, but an existing caller in the test suite still expected the old interface.

### Solution

The service test was updated to:

```python
results = run_database_analysis()
```

The existing assertions checking the database-analysis sections were retained.

### Lesson

This was an important demonstration of why new-feature tests alone are not enough.

The new API could work correctly while another part of the application still expected the old service interface.

Therefore:

```text
new feature tests
        ≠
proof that the whole application still works
```

Full regression testing is required after refactoring.


---

# API Tests Added

The API test suite now verifies more than the basic Day 15 endpoints.

## Orders Profile

A request is made using:

```python
response = client.get(
    "/profile",
    params={"dataset": "orders"},
)
```

The test checks:

```python
assert response.status_code == 200
```

and important response properties such as:

```text
shape
columns
numeric_summary
categorical_summary
```


---

## Invalid Dataset

The test sends:

```python
params={"dataset": "banana"}
```

and verifies:

```python
assert response.status_code == 422
```

This confirms that FastAPI is enforcing the `Literal` constraint.


---

## Customers Profile

The customers dataset is also tested to make sure `/profile` is not accidentally limited to orders.

Important profile sections are checked in the returned JSON.


---

## Database Analysis

The `/database` endpoint is tested and important sections are verified, including:

```text
expensive_orders
payment_counts
product_totals
revenue_by_city
```

The API test focuses on whether the HTTP layer correctly exposes the database service.

The detailed correctness of individual SQL operations belongs primarily to the lower-level database tests.


---

# Testing Strategy Used Today

Day 16 used multiple levels of verification.

## 1. Swagger / Manual Verification

I ran the FastAPI application and used:

```text
/docs
```

to manually execute the new endpoints.

This helped verify:

- Swagger displayed the dataset choices
- `/profile` accepted valid datasets
- real profiler data was returned
- `/database` executed the real database workflow


---

## 2. API Tests

`TestClient` was used to automatically test the HTTP interface.

This verifies the application without manually using the browser every time.


---

## 3. Full Regression Suite

After the API-specific tests worked, I ran the complete project test suite.

This caught the outdated call to:

```python
run_database_analysis(orders)
```

in the existing service test.

That failure demonstrated the practical value of regression testing.


---

## 4. Docker Verification

Because application source code changed, the Docker image was rebuilt.

The test suite was then executed inside the container.

This verifies that the current application works not only in my local virtual environment but also inside the isolated Docker environment.


---

# CLI Impact

The database CLI previously obtained orders indirectly through:

```python
run_analysis()
```

After the service refactor, the CLI can directly call:

```python
run_database_analysis()
```

This gives a cleaner flow:

```text
CLI database command
        ↓
run_database_analysis()
        ↓
load_and_validate_orders()
        ↓
database analysis
```

instead of:

```text
CLI
 ↓
run_analysis()
 ↓
perform unrelated analysis work
 ↓
extract orders
 ↓
run_database_analysis()
```

The CLI remains an interface rather than becoming responsible for preparing internal service data.


---

# Statistics and Outliers — Scope Decision

During Day 16 I noticed that:

```python
run_analysis()
```

still contains important analytical functionality:

```text
profile
price statistics
price outliers
```

However, this functionality is not currently exposed through a dedicated API endpoint.

I considered adding something such as:

```text
GET /analysis
```

but decided not to add it during Day 16.

One complication is that `run_analysis()` also returns the orders DataFrame for internal Python use.

An HTTP API should have a deliberate JSON response contract rather than automatically exposing every internal service return value.

Therefore the decision was:

```text
Current API:
    /profile
    /database

Internal service:
    run_analysis()
        ├── profile
        ├── statistics
        └── outliers
```

A future `/statistics` or `/analysis` endpoint can be designed if there is a real requirement for it.

This taught me that:

> Not every internal function automatically needs a corresponding API endpoint.

The public interface should be designed intentionally.


---

# Current Application Architecture

At the end of Day 16:

```text
                         Users / Clients
                               │
                  ┌────────────┴────────────┐
                  ↓                         ↓
                 CLI                     FastAPI
                  │                         │
                  └────────────┬────────────┘
                               ↓
                         Service Layer
                               │
                ┌──────────────┼──────────────┐
                ↓              ↓              ↓
              Loader       Validator       Profiler
                │              │              │
                └──────────────┼──────────────┘
                               ↓
                         Prepared Data
                               │
                        ┌──────┴──────┐
                        ↓             ↓
                    Statistics     Database
                                      ↓
                                  SQLite / SQL
```

The important point is that the CLI and API are different interfaces over the same application logic.


---

# Current API Surface

The API now contains:

```text
GET /
GET /health
GET /profile
GET /database
```

Responsibilities:

```text
/           → identify the API

/health     → verify the API is running

/profile    → profile a supported dataset

/database   → execute database analysis
```


---

# Key Things I Learned Today

## API Design

I learned that creating an API is not simply putting HTTP routes around every function in a project.

The API needs its own carefully designed public contract.


## Security and Encapsulation

Allowing clients to specify arbitrary internal filesystem paths is usually a poor interface.

Logical resource names allow the server to retain control over its internal implementation.


## Type-Driven Validation

Using:

```python
Literal["orders", "customers"]
```

allows Python type information to become part of the API contract.

FastAPI can use that information for:

- request validation
- error responses
- OpenAPI generation
- Swagger documentation


## Service-Layer Design

If two workflows require the same preparation step, I should identify and extract the genuinely shared responsibility instead of making one large workflow depend on another.


## Refactoring

Refactoring requires understanding everything a function currently does.

Removing a dependency without checking hidden responsibilities such as validation can introduce bugs.


## Regression Testing

A new feature passing its own tests does not guarantee the existing application still works.

The full suite can detect old callers that were broken by a changed service contract.


## Interface Separation

The CLI and API should primarily translate user/client requests into calls to the service layer.

Core application logic should remain reusable and independent of a particular interface.


## API Scope

Not every service capability has to be exposed immediately.

A smaller, deliberate API is better than exposing internal structures simply because they already exist.


---

# Day 16 Final State

By the end of Day 16:

- FastAPI is connected to real Engineering Workbench functionality.
- `/profile` exposes the profiler through HTTP.
- Orders and customers are supported through logical dataset names.
- `Literal` provides automatic dataset validation.
- Swagger communicates the supported dataset values.
- `/database` exposes the database-analysis workflow.
- API routes reuse the service layer instead of duplicating logic.
- shared order loading and validation were extracted into `load_and_validate_orders()`.
- `run_analysis()` continues to provide profiling, statistics and outlier functionality internally.
- `run_database_analysis()` can now operate independently.
- the CLI database workflow was adapted to the new service contract.
- API tests cover valid and invalid profile requests and database analysis.
- the full regression suite was run after the refactor.
- an outdated service test was discovered and corrected.
- the application was rebuilt and tested inside Docker.
- statistics/outliers were deliberately not added as another API endpoint during Day 16.

---

# Next — Day 17

The roadmap continues with:

```text
Day 17 — Integration + Failure Testing
```

The focus will move from proving the normal successful workflows toward examining how the production service behaves when components, inputs or integrations fail.