## Data Profiler Architecture

### What I Built

- Added pandas as a project dependency.
- Added `load_csv()` to load CSV files into pandas DataFrames.
- Created `profiler.py`.
- Implemented functions to profile:
  - Dataset shape
  - Column names
  - Missing values
  - Duplicate rows
  - Column data types
- Created `profile_data()` to combine the individual profiling operations into one profile report.
- Simplified `main.py` so it coordinates the loader and profiler instead of performing profiling itself.

### Architecture

```text
DATA_PATH
    ↓
load_csv()
    ↓
DataFrame
    ↓
profile_data()
    ↓
Profile Report