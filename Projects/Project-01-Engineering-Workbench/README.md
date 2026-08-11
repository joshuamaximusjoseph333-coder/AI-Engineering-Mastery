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