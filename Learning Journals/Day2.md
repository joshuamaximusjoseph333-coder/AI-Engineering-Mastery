# Project 1 — Day 2

## What I Built
A structured Python data-loading application that reads a configured
raw data file, logs the operation, counts its lines, and returns the result.

## Concepts I Learned
- Virtual environments
- Project-specific dependencies
- Modules and packages
- Functions
- Parameters and arguments
- Return values
- pathlib.Path
- Type hints
- File handling
- Configuration
- Logging
- Separation of concerns

## Architecture
- main.py: entry point and coordinator
- config.py: stores configuration such as DATA_PATH
- loader.py: contains reusable file-processing logic
- logger.py: configures application logging

## Problems I Encountered
- PowerShell initially blocked .venv activation because of execution policy.
- Ran main.py from the wrong directory.
- Initially placed count_lines() in logger.py instead of loader.py.
- Needed to distinguish Path() from actually opening/reading a file.

## What I Understand Now
- Why each project should have its own virtual environment.
- How modules and packages organize Python code.
- How parameters receive arguments.
- How Path objects represent filesystem locations.
- Why configuration should be centralized.
- How logging differs from print().
- Why larger applications separate responsibilities across modules.

## Questions / Things to Revisit
- More advanced logging
- Better ways of processing large files
- Automated testing
- More flexible configuration