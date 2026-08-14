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

- 4 loader tests
- 6 profiler tests
- 2 validator tests
- 12 tests total

All 12 tests pass locally and inside Docker.

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