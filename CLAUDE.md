# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Launchable predictive test selection demonstration project. It contains a Python calculator library with 100+ operations and corresponding tests. The project uses intentional code mutations and Launchable's ML-powered test selection to demonstrate how predictive test selection can optimize CI/CD pipelines.

## Project Structure

- **calculator_project/** - Active calculator module with ~100 operations (basic arithmetic + 90 custom operations)
- **calculator_project_backup/** - Clean backup used to reset state between pipeline iterations
- **test_calculator.py** - Test suite with 103 tests, each with 60-second sleep to simulate expensive tests
- **pipeline.sh** - Automated testing pipeline that mutates code, selects test subsets, and reports results
- **test_list.txt** - Full list of all test identifiers
- **launchable-subset.txt** - Launchable-selected test subset (20% of total tests)
- **launchable-session.txt** - Current Launchable test session metadata

## Running Tests

Run all tests:
```bash
pytest test_calculator.py
```

Run a single test:
```bash
pytest test_calculator.py::test_add
```

Run tests with JUnit XML output:
```bash
pytest --junit-xml=test-results/results.xml test_calculator.py
```

Run only the Launchable-selected subset:
```bash
pytest @launchable-subset.txt
```

## Launchable Workflow

Record a build:
```bash
launchable record build --name <build-name>
```

Create a test session:
```bash
launchable record session --test-suite "random_pytest" --observation --build <build-name>
```

Generate test subset (20% target):
```bash
cat test_list.txt | launchable subset --build <build-name> --target 20% pytest > launchable-subset.txt
```

Report test results:
```bash
launchable record tests --session <session-id> --allow-test-before-build --build <build-name> pytest ./test-results/
```

## Pipeline Automation

The pipeline.sh script automates the testing workflow. Run multiple iterations:
```bash
./pipeline.sh <number-of-iterations>
```

Each iteration:
1. Mutates 0-3 random calculator functions using mutate_random_function.py
2. Commits changes with git
3. Records the build with Launchable
4. Generates a 20% test subset based on mutation prediction
5. Runs the selected tests with pytest
6. Reports results to Launchable
7. Resets to clean state from calculator_project_backup/

## Code Mutation System

The mutate_random_function.py script randomly modifies calculator operations:
- 50% chance: No mutation
- 30% chance: Mutate 1 function
- 10% chance: Mutate 2 functions
- 10% chance: Mutate 3 functions

Mutations swap operators in return statements (+ to -, - to +, or add +42).

## Architecture Notes

### Calculator Module Structure
All calculator operations follow a simple pattern:
- Located in calculator_project/
- Each operation is in its own file (e.g., add.py, custom_op_10.py)
- All exports are aggregated in __init__.py
- Custom operations (custom_op_10 through custom_op_99) use compound arithmetic with the operation number as a coefficient

### Test Structure
- All tests import functions from calculator_project package
- Custom operations use pytest parametrization for 87 similar tests
- Three special custom operations (custom_op_97, custom_op_98, custom_op_99) have dedicated test functions
- Tests include expected value adjustments (e.g., `expected + 17`) to match mutation patterns

## Git Workflow

The project uses git to track mutations across iterations. The pipeline automatically:
- Commits each mutation with message "next iteration N"
- Uses short commit hashes as build identifiers
- Main branch is `main`, current working branch is `master`
