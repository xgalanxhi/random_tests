# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a Launchable predictive test selection demonstration project. It contains a Python calculator library with 100+ operations and corresponding tests. The project uses intentional code mutations and Launchable's ML-powered test selection to demonstrate how predictive test selection can optimize CI/CD pipelines.

## Setup

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

- **src/calculator/** - Active calculator module with ~100 operations (basic arithmetic + 90 custom operations)
- **backup/calculator/** - Clean backup used to reset state between pipeline iterations
- **test/test_calculator.py** - Test suite with 103 tests, each with 60-second sleep to simulate expensive tests
- **test/test_list.txt** - Full list of all test identifiers
- **cicd/pipeline.sh** - Automated testing pipeline that mutates code, selects test subsets, and reports results
- **cicd/mutate_random_function.py** - Script that randomly mutates calculator functions
- **cicd/temp/** - Temporary files generated during pipeline execution (gitignored)
  - **cicd/temp/launchable-subset.txt** - Launchable-selected test subset (20% of total tests)
  - **cicd/temp/launchable-session.txt** - Current Launchable test session metadata
  - **cicd/temp/test-results/** - JUnit XML test results

## Running Tests

Run all tests:
```bash
pytest test/
```

Run all tests in parallel (uses all CPU cores):
```bash
pytest -n auto test/
```

Run a single test:
```bash
pytest test/test_calculator.py::test_add
```

Run tests with JUnit XML output:
```bash
pytest --junit-xml=test-results/results.xml test/
```

Run only the Launchable-selected subset (with parallel execution):
```bash
pytest -n auto @cicd/temp/launchable-subset.txt
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
mkdir -p cicd/temp
cat test/test_list.txt | launchable subset --build <build-name> --target 20% pytest > cicd/temp/launchable-subset.txt
```

Report test results:
```bash
launchable record tests --session <session-id> --allow-test-before-build --build <build-name> pytest cicd/temp/test-results/
```

## Pipeline Automation

### Local Execution

The cicd/pipeline.sh script automates the testing workflow. Run multiple iterations:
```bash
./cicd/pipeline.sh <number-of-iterations>
```

Each iteration:
1. Resets to clean state from backup/calculator/ (except first iteration)
2. Cleans cicd/temp/ directory
3. Mutates 0-3 random calculator functions using cicd/mutate_random_function.py
4. Commits changes with git
5. Records the build with Launchable
6. Generates a 20% test subset based on mutation prediction (saved to cicd/temp/)
7. Runs the selected tests with pytest in parallel (`-n auto`)
8. Reports results to Launchable

### CloudBees Workflow

The CloudBees workflow (`.cloudbees/workflows/pipeline.yaml`) runs the pipeline in CI/CD:
- Triggered via workflow_dispatch with configurable iteration count (default: 5)
- Sets up Python and pytest
- Configures git for commits
- Runs cicd/pipeline.sh with Launchable integration
- Archives test results

Required secret: `SMART_TESTS_KEY` (Launchable API token)

## Code Mutation System

The cicd/mutate_random_function.py script randomly modifies calculator operations:
- 50% chance: No mutation
- 30% chance: Mutate 1 function
- 10% chance: Mutate 2 functions
- 10% chance: Mutate 3 functions

Mutations swap operators in return statements (+ to -, - to +, or add +42).

## Architecture Notes

### Calculator Module Structure
All calculator operations follow a simple pattern:
- Located in src/calculator/
- Each operation is in its own file (e.g., add.py, custom_op_10.py)
- All exports are aggregated in __init__.py
- Custom operations (custom_op_10 through custom_op_99) use compound arithmetic with the operation number as a coefficient

### Test Structure
- All tests import functions from src.calculator package (via path manipulation in test/test_calculator.py)
- Custom operations use pytest parametrization for 87 similar tests
- Three special custom operations (custom_op_97, custom_op_98, custom_op_99) have dedicated test functions
- Tests include expected value adjustments (e.g., `expected + 17`) to match mutation patterns
- Tests are stateless and can run in parallel using pytest-xdist (`-n auto`)
- Each test sleeps for 60 seconds to simulate expensive tests; parallel execution significantly reduces total runtime

## Git Workflow

The project uses git to track mutations across iterations. The pipeline automatically:
- Commits each mutation with message "next iteration N"
- Uses short commit hashes as build identifiers
- Main branch is `main`, current working branch is `master`
