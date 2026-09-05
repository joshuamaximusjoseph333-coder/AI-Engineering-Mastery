# Day 17 — Integration + Failure Testing

## Objective

The goal of Day 17 was to test how the Engineering Workbench behaves when realistic failures occur across multiple layers of the application.

Unlike earlier testing, which mostly verified successful behaviour, Day 17 focused on:

- integration testing
- failure testing
- exception propagation
- resource cleanup
- API error behaviour
- controlled exception translation

The main principle followed was:

```text
Create a realistic failure
        ↓
Observe current behaviour
        ↓
Decide whether that behaviour is acceptable
        ↓
Change production code only where necessary
```

This helped avoid adding unnecessary `try/except` blocks before knowing what actually needed improvement.


---

## Starting Point

At the beginning of Day 17, the project already had:

- loader tests
- validator tests
- profiler tests
- statistics tests
- database tests
- service tests
- CLI tests
- FastAPI endpoint tests

The successful API routes from Day 16 included:

```text
/
/health
/profile
/database
```

The next step was to verify how these layers behave when failures occur.


---

## Integration Testing vs Unit Testing

One of the first concepts I learned was the distinction between unit testing and integration testing.

A unit test checks a relatively small component.

For example:

```text
validate_order_values()
```

can be tested directly with invalid data.

That proves the validator itself works.

However, this does not prove that:

```text
run_analysis()
```

actually uses the validator correctly.

An integration test checks how components work together.

For example:

```text
run_analysis()
      ↓
load_and_validate_orders()
      ↓
load_csv()
      ↓
validation
      ↓
analysis
```

This means a validator unit test and a service integration test are not duplicates.

They protect different things.


---

## Failure Boundary 1 — Invalid Order Data

The first failure scenario tested whether invalid order data actually stops the service workflow.

I created a DataFrame containing:

```text
quantity = 0
```

which violates the rule:

```python
quantity must be greater than 0
```

Instead of reading the real CSV, I temporarily replaced:

```python
engineering_workbench.service.load_csv
```

using pytest's `monkeypatch` fixture.

The replacement returned the controlled invalid DataFrame.

The test expected:

```python
ValueError
```

with:

```text
quantity must be greater than 0
```

The test passed.

### What this proved

This did not merely prove that the validator works.

It proved that:

```text
run_analysis()
      ↓
load_and_validate_orders()
      ↓
validate_order_values()
```

is correctly connected.

If validation were accidentally removed from the service later, this test would fail even if the validator's own unit tests still passed.


---

## Learning `monkeypatch`

Before Day 17, I was not familiar with pytest's `monkeypatch`.

I learned that it allows a test to temporarily replace an attribute used by the application.

Example:

```python
monkeypatch.setattr(
    "engineering_workbench.service.load_csv",
    replacement,
)
```

The replacement exists only for the duration of the test.

After the test finishes, pytest restores the original function automatically.

This is useful because I can simulate difficult situations without damaging real project files.

For example, I do not need to delete the real CSV just to simulate a missing file.


---

## Why the Patch Target Matters

An important point was that I should patch the function where the code under test actually uses it.

The service module imports and uses:

```python
load_csv
```

Therefore the correct patch target was:

```text
engineering_workbench.service.load_csv
```

rather than blindly patching the original function somewhere else.

This is because the service is using its own imported reference.


---

## Failure Boundary 2 — Missing Orders File

The next test simulated a loader failure.

I created:

```python
def fake_load_csv(*args, **kwargs):
    raise FileNotFoundError("orders file not found")
```

Then temporarily replaced:

```python
engineering_workbench.service.load_csv
```

with this fake function.

The test called:

```python
run_analysis()
```

and expected:

```python
FileNotFoundError
```

The test passed.

### What this proved

The execution path became:

```text
run_analysis()
      ↓
load_and_validate_orders()
      ↓
load_csv()
      ↓
FileNotFoundError
      ↑
service
      ↑
caller
```

I learned that this behaviour is called **exception propagation**.

The service does not hide the loader failure.

Instead, the exception travels upward.


---

## Why I Did Not Add `try/except` Immediately

A major Day 17 lesson was that every exception does not need to be caught.

It would have been easy to add:

```python
try:
    ...
except Exception:
    ...
```

around service operations.

However, doing that without a clear recovery plan could hide useful errors.

For the service layer, allowing a meaningful Python exception such as:

```python
FileNotFoundError
```

to propagate can be the correct behaviour.

The interface above the service can decide whether that exception needs another representation.


---

## Failure Boundary 3 — Database Cleanup

The next scenario focused on database resource cleanup.

The service contains:

```python
try:
    ...
finally:
    connection.close()
```

The question was:

> If a database operation crashes inside the `try` block, will the connection still close?

To test this, I created a small fake connection:

```python
class FakeConnection:
    def __init__(self):
        self.closed = False

    def close(self):
        self.closed = True
```

I then patched:

```python
create_connection
```

so the service received this fake object instead of a real database connection.

I also patched the database write operation so that it deliberately raised:

```python
RuntimeError("database write failed")
```

The test expected the RuntimeError and then checked:

```python
assert fake_connection.closed is True
```

The test passed.


---

## What the Database Failure Test Proved

The complete failure path was:

```text
run_database_analysis()
        ↓
create connection
        ↓
enter try block
        ↓
database write fails
        ↓
RuntimeError
        ↓
finally executes
        ↓
connection.close()
        ↓
RuntimeError continues upward
```

This proved that cleanup occurs even when the operation fails.

This was an important lesson because tests can verify more than output values.

They can also verify guarantees such as:

- resource cleanup
- exception propagation
- interaction between components


---

## Failure Boundary 4 — Unexpected Failure Through the API

The next failure was tested at the FastAPI boundary.

I patched:

```python
engineering_workbench.api.run_database_analysis
```

so that it raised:

```python
RuntimeError("database failed")
```

I then sent:

```text
GET /database
```

I expected to inspect:

```text
HTTP 500
```

but the test failed differently.

Instead of returning a response, the test directly raised:

```text
RuntimeError: database failed
```


---

## Difficulty — TestClient Re-Raised the Exception

This was the main unexpected issue during Day 17.

Initially, I assumed:

```python
response = client.get("/database")
```

would simply return a response with:

```text
500 Internal Server Error
```

However, the default FastAPI/Starlette `TestClient` behaviour is to re-raise server exceptions inside the test process.

The original client was:

```python
client = TestClient(app)
```

That meant:

```text
application raises RuntimeError
        ↓
TestClient
        ↓
RuntimeError raised directly into pytest
```

So the response could not be inspected.


---

## Solution — `raise_server_exceptions=False`

To test the actual HTTP failure response, I changed the test client to:

```python
client = TestClient(
    app,
    raise_server_exceptions=False,
)
```

With this configuration:

```text
application raises RuntimeError
        ↓
server generates HTTP failure response
        ↓
TestClient returns response
        ↓
test checks status code
```

After making this change, the test passed with:

```text
500
```

### Lesson

There is a difference between:

```text
testing the raw Python exception
```

and:

```text
testing the HTTP response produced by that exception
```

For Day 17, the second behaviour was what I wanted.


---

## HTTP 422 vs 500

This also helped reinforce the difference between client-side input problems and server-side failures.

Example:

```text
/profile?dataset=banana
```

violates:

```python
Literal["orders", "customers"]
```

so FastAPI returns:

```text
422
```

This means the request input is invalid.

In contrast:

```text
/database
```

is a valid request.

If the internal service unexpectedly crashes, the failure belongs to the server:

```text
500 Internal Server Error
```


---

## Controlled Exception Translation

The next design question was whether every internal failure should remain a generic 500.

For `/profile`, I considered this scenario:

```text
GET /profile?dataset=orders
        ↓
dataset name is valid
        ↓
configured CSV file is missing
        ↓
FileNotFoundError
```

Instead of letting this become a generic server error, I decided to deliberately translate this known failure at the API boundary.


---

## Production Code Change

I updated the FastAPI import to include:

```python
HTTPException
```

Then modified the `/profile` route to catch only:

```python
FileNotFoundError
```

and raise:

```python
HTTPException(
    status_code=404,
    detail=f"Dataset '{dataset}' file not found",
)
```

The resulting architecture became:

```text
Service layer
      ↓
FileNotFoundError
      ↓
API boundary
      ↓
HTTPException
      ↓
404 response
```


---

## Why HTTP Handling Stayed Out of the Service

One important design decision was not to raise FastAPI `HTTPException` inside the service layer.

The service is also used by:

```text
CLI
tests
future interfaces
```

If the service itself knew about HTTP status codes, it would become tightly coupled to FastAPI.

Instead:

```text
Service
→ speaks Python/application exceptions

API
→ speaks HTTP
```

This preserves separation of concerns.


---

## Failure Boundary 5 — Testing the 404 Translation

After adding the controlled API translation, I wrote a focused test.

I patched:

```python
engineering_workbench.api.run_profile
```

so that it raised:

```python
FileNotFoundError
```

Then I sent:

```text
GET /profile?dataset=orders
```

The test checked:

```python
assert response.status_code == 404
```

and also checked:

```python
assert response.json() == {
    "detail": "Dataset 'orders' file not found",
}
```

The test passed.

### Why both assertions matter

The status code verifies the failure category.

The JSON body verifies the API's intended error message.

Together they verify the complete controlled error contract.


---

## Final Failure Behaviour

By the end of Day 17, I had verified these failure paths:

```text
Invalid order data
    ↓
ValueError

Missing orders file through service
    ↓
FileNotFoundError

Database write failure
    ↓
RuntimeError
    ↓
connection still closes

Unexpected internal database failure through API
    ↓
HTTP 500

Configured profile file missing through API
    ↓
HTTP 404

Unsupported dataset input
    ↓
HTTP 422
```


---

## Why I Did Not Add More Failure Tests

At this point, the important architecture boundaries had representative tests.

Adding dozens of similar invalid-value cases would have created repetition without teaching or protecting much additional architecture.

The focus remained on meaningful failure boundaries rather than maximizing the number of tests.


---

## Full Regression Testing

After the focused Day 17 tests passed, I ran the entire project test suite.

The complete local regression suite passed.

This confirmed that the Day 17 testing changes and API error handling did not break the existing:

- loader behaviour
- validation
- profiling
- statistics
- database functionality
- service workflows
- CLI
- API success paths


---

## Docker Verification

Because production code and tests had changed, I rebuilt the Docker image:

```text
engineering-workbench
```

The full test suite was also run inside the container.

The Dockerized API was started through Uvicorn and the normal routes were verified.

This gave confidence that the same project behaviour works inside the packaged runtime environment.


---

## Key Difficulties

### 1. Understanding why the invalid-data service test was not redundant

At first, the test looked similar to an existing validator test.

The important distinction was:

```text
validator unit test
→ proves validator logic

service integration test
→ proves service actually invokes validator
```

This helped me understand why integration tests exist.


### 2. Learning `monkeypatch`

I initially needed clarification about what `monkeypatch` was doing.

I learned that it temporarily replaces dependencies during tests and restores them afterward.


### 3. Understanding why the API 500 test failed

I expected the HTTP response immediately, but `TestClient` re-raised the Python exception.

The fix was:

```python
raise_server_exceptions=False
```

This allowed the real HTTP 500 response to be inspected.


### 4. Deciding where exception translation belongs

I learned that Python exceptions should generally remain in the service layer, while HTTP-specific translation belongs at the API boundary.


---

## Important Lessons

- Unit testing and integration testing protect different failure modes.
- Failure tests intentionally exercise unsuccessful paths.
- A test can be both an integration test and a failure test.
- `monkeypatch` is useful for creating controlled test conditions.
- Fake functions and fake objects can simulate difficult external conditions.
- `pytest.raises()` verifies expected Python exceptions.
- Exceptions can propagate upward instead of being hidden.
- `finally` ensures cleanup can still happen after failure.
- Resource cleanup is behaviour worth testing.
- FastAPI TestClient normally re-raises server exceptions.
- `raise_server_exceptions=False` is useful when testing actual HTTP 500 responses.
- Different failures should be represented differently at the API boundary.
- Service-layer logic should remain independent of HTTP.
- Known failures can be translated deliberately.
- Unexpected failures should not automatically be hidden.
- Full regression testing is necessary after focused changes.
- Docker verification confirms behaviour in the packaged runtime.


---

## Final State

Day 17 strengthened the Engineering Workbench by proving that the system behaves predictably when realistic failures occur.

The project now has coverage for:

```text
successful execution
        +
invalid data
        +
missing files
        +
database failure
        +
resource cleanup
        +
exception propagation
        +
HTTP 422
        +
HTTP 404
        +
HTTP 500
```

The project is now ready for:

```text
Day 18 — Final Demo + Mastery Gate
```