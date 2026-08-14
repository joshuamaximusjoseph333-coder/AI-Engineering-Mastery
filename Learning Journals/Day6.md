# Day 6 — Break, Debug, and Operate

## Objective

Learn how to deliberately break the application, observe failures, diagnose their root causes, recover the system, and verify that the application works correctly again.

This session corresponds to the original roadmap topic:

**Break / Debug / Operate the Program**

---

## 1. Debugging a Missing File

The configured dataset path was intentionally changed to a CSV file that did not exist.

This caused:

```text
FileNotFoundError
```

Execution flow:

```text
main.py
    ↓
load_csv(DATA_PATH)
    ↓
pd.read_csv(file_path)
    ↓
File does not exist
    ↓
FileNotFoundError
```

### Key Learning

A traceback should be used to identify:

- Exception type
- Failed operation
- Location of the failure
- Root cause

In this case:

- Exception: `FileNotFoundError`
- Failed operation: `pd.read_csv(file_path)`
- Component: `loader.py`
- Root cause: `DATA_PATH` pointed to a nonexistent file

---

## 2. Testing an Unexpected Dataset Structure

A temporary CSV was created without the `price` column.

Example:

```csv
order_id,product
1,Laptop
2,Mouse
3,Keyboard
```

Pandas successfully loaded the CSV because it was still a valid CSV file.

The profiler also successfully generated:

```text
shape: (3, 2)
columns: ['order_id', 'product']
```

### Key Learning

A program can execute successfully while still receiving data that is invalid for the application's requirements.

There is a difference between:

```text
Valid CSV
```

and:

```text
Valid orders dataset
```

---

## 3. Missing Column and KeyError

The following code was temporarily used:

```python
data["price"]
```

This asks pandas to return the DataFrame column named `price`.

Because the temporary dataset did not contain that column, pandas raised:

```text
KeyError: 'price'
```

### Key Learning

- Missing file → `FileNotFoundError`
- Missing DataFrame column → `KeyError`

---

## 4. Adding a Validation Layer

Created:

```text
src/data_loader/validator.py
```

The application now defines the required columns:

```python
REQUIRED_COLUMNS = {"order_id", "product", "price"}
```

Validation function:

```python
def validate_required_columns(data: pd.DataFrame) -> None:
    missing_columns = REQUIRED_COLUMNS - set(data.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )
```

### How It Works

```text
Required columns
        -
Actual DataFrame columns
        =
Missing columns
```

If required columns are missing, the validator deliberately raises a `ValueError`.

Example:

```text
ValueError: Missing required columns: ['price']
```

### Fail-Fast Validation

Instead of allowing invalid data to travel deeper into the application and fail later, the application detects the problem immediately.

Updated application flow:

```text
CSV
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
```

---

## 5. Testing the Validator

Created:

```text
tests/test_validator.py
```

Two validation situations were tested.

### Valid Dataset

A DataFrame containing:

- `order_id`
- `product`
- `price`

should complete validation without raising an exception.

### Invalid Dataset

A DataFrame without `price` should raise:

```text
ValueError
```

The test uses:

```python
with pytest.raises(ValueError, match="Missing required columns"):
    validate_required_columns(data)
```

### Key Learning

`pytest.raises()` tells pytest that an exception is the expected behavior.

Without `pytest.raises()`, an unexpected exception normally causes the test to fail.

After adding validator tests:

```text
Loader tests:     4
Profiler tests:   6
Validator tests:  2
-------------------
Total tests:     12
```

All 12 tests passed.

---

## 6. Debugging a Regression

The profiler was intentionally broken by changing:

```python
return data.shape
```

to:

```python
return (0, 0)
```

The program could still execute because `(0, 0)` is valid Python.

However, the result was incorrect.

Pytest detected the regression:

```text
2 failed, 10 passed
```

The failures occurred in:

- `test_get_shape`
- `test_profile_data`

Both tests depended on the behavior of `get_shape()`.

### Key Learning

A bug does not always produce an exception.

Sometimes:

```text
Program runs successfully
        ↓
Wrong result is produced
        ↓
Automated tests detect the regression
```

A regression is when previously working behavior becomes incorrect after a change.

---

## 7. Improving Profile Output

Previously:

```python
print(profile)
```

printed the entire dictionary on one line.

It was changed to:

```python
for key, value in profile.items():
    print(f"{key}: {value}")
```

`profile.items()` provides each dictionary key-value pair.

The loop prints each result separately.

Example:

```text
shape: (3, 3)
columns: ['order_id', 'product', 'price']
missing_values: {'order_id': 0, 'product': 0, 'price': 0}
duplicate_count: 0
data_types: {'order_id': 'int64', 'product': 'str', 'price': 'int64'}
```

---

## 8. Operational Error Logging

The CSV loader was improved using `try` / `except`.

```python
def load_csv(file_path: Path) -> pd.DataFrame:
    logging.info(f"Loading CSV file: {file_path}")

    try:
        return pd.read_csv(file_path)

    except FileNotFoundError:
        logging.error(f"CSV file not found: {file_path}")
        raise
```

### Execution When the File Exists

```text
try
 ↓
pd.read_csv()
 ↓
DataFrame returned
 ↓
except block skipped
```

### Execution When the File Does Not Exist

```text
pd.read_csv()
 ↓
FileNotFoundError
 ↓
except catches the exception
 ↓
logging.error() records the failure
 ↓
raise re-raises the same exception
 ↓
application stops
```

### Why `raise` Is Important

The exception is temporarily caught so that the failure can be logged.

`raise` then allows the original exception to continue.

Without `raise`, the function could finish without returning a DataFrame, potentially causing confusing failures later.

### Key Learning

```text
logging.error()
→ records the failure

raise
→ propagates the failure
```

---

## 9. Final Recovery and Verification

The complete operational workflow practiced was:

```text
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
Verify automated tests
 ↓
Verify Docker
```

After restoring the correct application state:

```text
DATA_PATH → data/raw/orders.csv
```

the application was verified locally.

All tests passed:

```text
12 passed
```

The Docker image was rebuilt:

```bash
docker build -t engineering-workbench .
```

The application was verified inside Docker:

```bash
docker run --rm engineering-workbench
```

The complete test suite was also verified inside Docker:

```bash
docker run --rm engineering-workbench python -m pytest
```

Result:

```text
12 passed
```

---

## Final Architecture

```text
config.py
   ↓
DATA_PATH
   ↓
loader.py
   ↓
DataFrame
   ↓
validator.py
   ↓
profiler.py
   ↓
Profile Report
```

Supporting engineering systems:

```text
Logging
   ↓
Observe application behavior

Pytest
   ↓
Verify correctness and detect regressions

Docker
   ↓
Verify the application in a reproducible environment

Git
   ↓
Track project history
```

---

## Day 6 Key Takeaways

- Learned how to read and diagnose Python tracebacks.
- Distinguished root causes from exceptions.
- Understood `FileNotFoundError`, `KeyError`, `ValueError`, and assertion failures.
- Learned that valid input syntax does not guarantee valid application data.
- Added fail-fast schema validation.
- Learned how `pytest.raises()` tests expected exceptions.
- Learned what a software regression is.
- Improved application output readability.
- Added operational ERROR logging.
- Learned `try`, `except`, and re-raising with `raise`.
- Practiced the complete break → diagnose → recover → verify workflow.
- Expanded the test suite to 12 tests.
- Verified the recovered application and all tests inside Docker.