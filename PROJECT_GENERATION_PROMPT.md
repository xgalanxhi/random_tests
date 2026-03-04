# Smart Tests Evaluation Project - Generation Guide

## Project Overview

Generate a complete Python project designed to evaluate CloudBees Smart Tests (Predictive Test Selection). This project will serve as **enablement material** to demonstrate how Smart Tests intelligently selects which tests to run based on code changes.

## Core Requirements

### 1. Application Domain
Create a **mathematical calculator library** with ~100 operations organized as individual modules. Each operation should:
- Be in its own Python file
- Implement a distinct mathematical function
- Include special `# MUTATOR_TAG` comments marking mutation points
- Be simple enough to understand quickly (this is enablement material)

Example operation categories:
- Basic arithmetic (add, subtract, multiply, divide, modulo, power)
- Trigonometric functions (sin, cos, tan, radians conversion)
- Statistical operations (mean, median, mode, standard deviation)
- Geometric calculations (area, perimeter, volume for various shapes)
- Number theory (factorial, fibonacci, prime checks, GCD, LCM)
- Matrix operations (simple 2x2 operations)
- String-to-number conversions
- Temperature conversions
- Other creative mathematical operations

### 2. Project Structure

```
smart-tests-demo/
├── README.md                          # Comprehensive setup and usage guide
├── requirements.txt                   # Python dependencies
├── .gitignore                         # Standard Python gitignore
├── .github/
│   └── workflows/
│       └── smart-tests.yaml           # GitHub Actions workflow
├── src/
│   └── calculator/
│       ├── __init__.py
│       ├── add.py                     # ~100 operation files
│       ├── subtract.py
│       ├── ...
│       └── trig_sin.py
├── tests/
│   ├── pytest/                        # Pytest test suite
│   │   ├── __init__.py
│   │   ├── test_arithmetic.py
│   │   ├── test_trigonometry.py
│   │   ├── ...
│   │   └── test_list.txt              # List of all test paths for Smart Tests
│   └── junit/                         # (Empty for now, future expansion)
├── automation/
│   ├── mutator.py                     # Code mutation script
│   ├── pipeline.sh                    # Main pipeline orchestration
│   └── reset.sh                       # Reset to clean state
├── backup/
│   └── calculator/                    # Clean backup of all source files
└── .smarttests/                       # Smart Tests temp files (gitignored)
```

### 3. Source Code Guidelines

**Each operation file should:**

```python
# src/calculator/add.py

def add(a, b):
    """Add two numbers.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    result = a + b  # MUTATOR_TAG: change to subtraction
    return result
```

**Key principles:**
- Include `# MUTATOR_TAG:` comments at mutation points with description
- Keep functions simple (3-10 lines max)
- Add docstrings for clarity
- Use meaningful variable names
- Each file = one function (for easy test mapping)

### 4. Test Suite Design

**Organize tests by category** (tests/pytest/test_arithmetic.py):

```python
# tests/pytest/test_arithmetic.py
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import pytest
from calculator.add import add
from calculator.subtract import subtract

# Configurable test sleep time for demo purposes
TEST_SLEEP_TIME = int(os.getenv('TEST_SLEEP_TIME', '0'))

def test_add_positive_numbers():
    """Test adding two positive numbers."""
    if TEST_SLEEP_TIME > 0:
        import time
        time.sleep(TEST_SLEEP_TIME)
    assert add(2, 3) == 5
    assert add(10, 20) == 30

def test_add_negative_numbers():
    """Test adding negative numbers."""
    if TEST_SLEEP_TIME > 0:
        import time
        time.sleep(TEST_SLEEP_TIME)
    assert add(-5, -3) == -8
    assert add(-10, 5) == -5

# ... more tests
```

**Test requirements:**
- ~100 total tests across multiple files
- Group related operations (arithmetic, trig, geometric, etc.)
- Each test should have clear docstrings
- Use descriptive test names
- Optional configurable sleep time (TEST_SLEEP_TIME env var)
- Create `tests/pytest/test_list.txt` with all test paths

### 5. Mutation System

**Create `automation/mutator.py`:**

```python
#!/usr/bin/env python3
"""
Smart mutation system for code changes.

Randomly selects one source file and mutates code at MUTATOR_TAG locations.
Tracks mutations in a JSON file for transparency and reproducibility.
"""
```

**Mutator requirements:**
- Parse all files in `src/calculator/` for `# MUTATOR_TAG` comments
- Randomly select ONE file per iteration
- Apply mutation based on tag description (e.g., "change to subtraction")
- Log mutation to `automation/mutation_log.json`:
  ```json
  {
    "iteration": 5,
    "file": "src/calculator/add.py",
    "line": 12,
    "original": "result = a + b",
    "mutated": "result = a - b",
    "description": "change to subtraction"
  }
  ```
- 70% chance of mutation, 30% no mutation (configurable)
- Predictable: same tag type = same mutation

**Mutation types to support:**
- Arithmetic operator changes (+, -, *, /)
- Comparison operator changes (<, >, <=, >=, ==, !=)
- Off-by-one errors (n to n+1)
- Sign flips (+ to -)
- Logic inversions (and/or)

### 6. Pipeline Automation

**Create `automation/pipeline.sh`:**

```bash
#!/bin/bash
# Smart Tests evaluation pipeline
# Usage: ./automation/pipeline.sh <iterations>

ITERATIONS=$1
TEMP_DIR=".smarttests"

# Validation
if [ -z "$ITERATIONS" ]; then
  echo "Usage: $0 <number-of-iterations>"
  exit 1
fi

# Setup
mkdir -p "$TEMP_DIR"

for ((i = 1; i <= ITERATIONS; i++)); do
  echo "=========================================="
  echo "Iteration $i/$ITERATIONS"
  echo "=========================================="

  # Reset to clean state
  if [ $i -gt 1 ]; then
    echo "Resetting to clean state..."
    rm -rf src/calculator
    cp -r backup/calculator/ src/calculator/
  fi

  # Clean temp files
  rm -rf "$TEMP_DIR"/*

  # Apply mutation
  python3 automation/mutator.py

  # Git commit
  git add src/calculator automation/mutation_log.json
  git commit -m "Iteration $i: $(cat automation/mutation_log.json | grep 'file' | tail -1)"

  BUILD_NAME=$(git rev-parse --short HEAD)

  # Smart Tests: Record build
  smart-tests record build --build "$BUILD_NAME"

  # Smart Tests: Create session
  smart-tests record session \
    --test-suite "pytest" \
    --observation \
    --build "$BUILD_NAME" \
    > "$TEMP_DIR/session.txt"

  SESSION=$(cat "$TEMP_DIR/session.txt")

  # Smart Tests: Get subset (20% target)
  cat tests/pytest/test_list.txt | \
    smart-tests subset \
      --session "$SESSION" \
      --target 20% \
      pytest > "$TEMP_DIR/subset.txt"

  # Run subset tests
  export TEST_SLEEP_TIME=0
  pytest -n auto \
    -o junit_family=legacy \
    --junit-xml="$TEMP_DIR/results.xml" \
    @"$TEMP_DIR/subset.txt"

  # Smart Tests: Record results
  smart-tests record tests \
    --session "$SESSION" \
    --build "$BUILD_NAME" \
    pytest "$TEMP_DIR/"

  echo "✅ Completed iteration $i"
  echo
done

echo "=========================================="
echo "Pipeline complete!"
echo "View results: https://app.cloudbees.com/smart-tests"
echo "=========================================="
```

### 7. GitHub Actions Workflow

**Create `.github/workflows/smart-tests.yaml`:**

```yaml
name: Smart Tests Evaluation

on:
  workflow_dispatch:
    inputs:
      iterations:
        description: 'Number of pipeline iterations'
        required: false
        default: '5'
  push:
    branches: [main]

jobs:
  evaluate-smart-tests:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Configure Git
        run: |
          git config --global user.email "github-actions[bot]@users.noreply.github.com"
          git config --global user.name "GitHub Actions"

      - name: Run Smart Tests Pipeline
        env:
          SMART_TESTS_TOKEN: ${{ secrets.SMART_TESTS_TOKEN }}
          ITERATIONS: ${{ github.event.inputs.iterations || '5' }}
        run: |
          chmod +x automation/pipeline.sh
          bash automation/pipeline.sh $ITERATIONS

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: .smarttests/results.xml
```

### 8. Documentation Requirements

**README.md should include:**

1. **Overview**: What is this project? Why Smart Tests?
2. **Quick Start**:
   - Prerequisites (Python 3.11+, git)
   - Installation steps
   - Get Smart Tests token
3. **Project Structure**: Explain directory layout
4. **Running Locally**:
   ```bash
   # Setup
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt

   # Configure Smart Tests
   export SMART_TESTS_TOKEN="your-token"

   # Run pipeline
   bash automation/pipeline.sh 10
   ```
5. **How It Works**:
   - Mutation strategy
   - Smart Tests integration
   - Test selection logic
6. **Understanding Results**: How to interpret Smart Tests output
7. **Extending**: How to add new test frameworks (JUnit, etc.)
8. **Troubleshooting**: Common issues

**requirements.txt:**
```
# Testing framework
pytest>=7.4.0
pytest-xdist>=3.5.0

# Smart Tests CLI
smart-tests-cli~=2.0
```

### 9. Best Practices to Follow

1. **Code Quality**:
   - Clear, descriptive names
   - Comprehensive docstrings
   - Type hints where helpful
   - Keep functions under 10 lines

2. **Test Quality**:
   - Descriptive test names (test_operation_scenario)
   - Clear assertions
   - Test edge cases
   - Group related tests

3. **Git Hygiene**:
   - Meaningful commit messages
   - .gitignore for temp files, venv, __pycache__
   - Clean history

4. **Documentation**:
   - Clear README with examples
   - Inline comments where code isn't obvious
   - Mutation tags explain intent

5. **Maintainability**:
   - Consistent formatting
   - Modular structure
   - Easy to extend with new test frameworks

### 10. Implementation Notes

**Mutation predictability:** When mutator sees `# MUTATOR_TAG: change to subtraction`, it should:
- Parse the next line of code
- Identify the operator (e.g., `+`)
- Replace with specified operator (e.g., `-`)
- Be deterministic: same tag = same mutation

**Test-to-code mapping:** Since each source file has one function and is clearly named:
- `src/calculator/add.py` → tests in `tests/pytest/test_arithmetic.py::test_add_*`
- When `add.py` mutates, Smart Tests should select `test_add_*` tests
- This makes results easy to verify

**Future expansion readiness:**
- `tests/junit/` directory reserved for Java/JUnit tests
- Pipeline script structured to support multiple test commands
- Smart Tests `--test-suite` parameter ready for multiple suites

## Deliverables

Generate a complete, working project that includes:

1. ✅ ~100 source files in `src/calculator/`
2. ✅ ~100 tests in `tests/pytest/`
3. ✅ Backup of clean source in `backup/`
4. ✅ `automation/mutator.py` with MUTATOR_TAG parsing
5. ✅ `automation/pipeline.sh` with Smart Tests integration
6. ✅ `.github/workflows/smart-tests.yaml`
7. ✅ Comprehensive README.md
8. ✅ requirements.txt
9. ✅ .gitignore
10. ✅ All code working and tested

## Success Criteria

The generated project should:
- Run successfully on first try locally
- Work in GitHub Actions
- Demonstrate clear test selection by Smart Tests
- Be readable and educational
- Serve as enablement material for Smart Tests
- Be easily extendable for new test frameworks

---

**Instructions for Claude:**
Generate this complete project structure with all files. Follow Python best practices, keep code readable and well-documented, and ensure the mutation system creates predictable, demonstrable test selection by Smart Tests.
