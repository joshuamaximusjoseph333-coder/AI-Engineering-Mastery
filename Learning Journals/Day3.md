# Day 3 — Unit Testing and Systematic Debugging

## What I Worked On

Today I introduced automated testing into Project 01 using `pytest`.

The main goal was to verify the behaviour of the `count_lines()` function in `loader.py` using controlled test data instead of depending on the real `orders.csv` dataset.

I also deliberately introduced bugs into the loader and used pytest failures and tracebacks to diagnose their root causes systematically.

---

## 1. Installing and Running Pytest

Pytest was already installed inside the project's virtual environment.

I verified it using:

`python -m pip install pytest`

Tests are executed using:

`python -m pytest`

Pytest automatically discovers files and functions that follow its test naming conventions, such as:

* `test_loader.py`
* `test_count_lines()`

---

## 2. Why I Avoided Testing Directly With orders.csv

Originally, the loader could be tested using the real `orders.csv` file.

However, this creates a fragile test because the contents of `orders.csv` may change later.

For example, if a test expects four lines but more orders are added to the dataset, the test would fail even though `count_lines()` is working correctly.

Instead, I used controlled temporary test data where the expected result is known in advance.

---

## 3. Using pytest tmp_path

`tmp_path` is a pytest fixture that provides a temporary directory as a Python `Path` object.

Example:

`file_path = tmp_path / "sample.txt"`

Here:

* `tmp_path` represents the temporary directory.
* `/` combines Path components.
* `"sample.txt"` is the filename chosen for the test.
* `file_path` stores the resulting Path object.

Creating a Path does not automatically create the file.

The file is created when I use:

`file_path.write_text(...)`

For example:

`file_path.write_text("apple\nbanana\norange\n", encoding="utf-8")`

This creates the temporary file containing three lines.

---

## 4. Tests Created

I tested four behaviours of `count_lines()`.

### Normal File

A temporary file containing three lines is created.

Expected result:

`3`

### Empty File

An empty temporary file is created.

Expected result:

`0`

### Single-Line File

A temporary file containing one line is created.

Expected result:

`1`

### Missing File

A Path is created for a file that does not actually exist.

Expected behaviour:

`FileNotFoundError`

This test uses:

`pytest.raises(FileNotFoundError)`

`pytest.raises()` verifies that the expected exception is raised.

---

## 5. How test_loader.py Connects to loader.py

The test file imports the real function from the production code:

`from src.data_loader.loader import count_lines`

The workflow is:

`test_loader.py`

→ creates controlled test input

→ calls `count_lines(file_path)`

→ `loader.py` performs the real line-counting operation

→ returns a result or raises an exception

→ `test_loader.py` verifies the behaviour

The test file does not perform the actual line counting itself.

---

## 6. First Deliberate Bug — Incorrect Count

I deliberately changed the counting logic from:

`len(file.readlines())`

to:

`len(file.readlines()) + 1`

This caused the normal and empty-file tests to fail because every successfully read file returned one more than the correct count.

The missing-file test still passed because `FileNotFoundError` occurred while opening the file, before execution reached the broken counting logic.

This demonstrated that different tests exercise different execution paths.

---

## 7. Second Deliberate Bug — Wrong File Mode

I changed the file mode from:

`"r"`

to:

`"w"`

`"r"` means read mode, while `"w"` means write mode.

The loader then attempted:

`file.readlines()`

on a write-only file object.

Python raised:

`io.UnsupportedOperation: not readable`

The missing-file test also failed because opening a nonexistent path with `"w"` can create the file instead of raising `FileNotFoundError`.

The root cause was therefore not `readlines()` itself. The root cause was opening the file using the wrong mode.

---

## 8. Third Deliberate Bug — Wrong Return Type

I changed:

`return line_count`

to:

`return str(line_count)`

The numerical information was still correct, but the function returned strings instead of integers.

For example:

`"3"` instead of `3`

This caused assertions such as:

`assert result == 3`

to fail because a string and an integer are different types.

It also violated the function's declared return type:

`def count_lines(file_path: Path) -> int:`

---

## 9. Systematic Debugging Workflow

Instead of randomly changing code when something fails, I learned to debug systematically.

My workflow is:

**Error → Location → Operation → Root Cause → Fix → Verify**

More specifically:

1. Read the traceback, usually starting near the bottom.
2. Identify the exception or assertion failure.
3. Find the relevant file and line number.
4. Identify which operation failed.
5. Inspect the code leading to that operation.
6. Determine the root cause instead of only treating the symptom.
7. Make the smallest justified fix.
8. Rerun the test suite to verify the fix.

---

## 10. Symptom vs Root Cause

A symptom is the observable failure.

A root cause is the underlying reason that produced the failure.

For the wrong-file-mode bug:

**Symptom:**

`io.UnsupportedOperation: not readable`

The failure appeared when `readlines()` executed.

**Root cause:**

The file had been opened using `"w"` instead of `"r"`.

Therefore, changing or blaming `readlines()` would not address the actual problem.

---

## 11. Important Terminology

### Parameter

A variable declared in a function definition that receives input.

Example:

`def count_lines(file_path):`

Here, `file_path` is a parameter.

### Argument

The actual value or object supplied when calling a function.

Example:

`count_lines(file_path)`

Here, the supplied `file_path` is an argument.

### Exception

A Python mechanism that signals an exceptional condition during program execution.

Example:

`FileNotFoundError`

### Failed Assertion

Occurs when the actual result does not satisfy the condition expected by a test.

Example:

`assert "3" == 3`

### Regression

A software change that causes previously working functionality to stop working.

Automated tests help detect regressions.

---

## Key Takeaways

* Automated tests give confidence that known behaviours continue to work.
* Tests should use controlled and predictable inputs when possible.
* `tmp_path` allows tests to create isolated temporary files.
* `assert` verifies expected conditions and return values.
* `pytest.raises()` verifies expected exceptions.
* Different tests can exercise different execution paths.
* A failing line is not necessarily the root cause.
* Tracebacks should be investigated systematically rather than followed by random code changes.
* After fixing a bug, the entire test suite should be rerun.
* Passing tests increase confidence in the behaviours covered by those tests, but they do not prove that a program contains no bugs.

## Day 3 Result

By the end of Day 3, Project 01 has an automated pytest test suite covering normal, edge, and failure behaviour for the data loader, and I have practiced deliberately breaking, diagnosing, repairing, and verifying the loader.
