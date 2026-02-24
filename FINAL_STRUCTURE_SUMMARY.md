# Final Project Structure

## ✅ Complete Directory Organization

```
random_tests/
├── src/
│   └── calculator/              # Source code
│       ├── __init__.py
│       ├── add.py, subtract.py, ...
│       └── custom_op_10.py ... 99
├── backup/
│   └── calculator/              # Clean backup copy
├── test/
│   ├── test_calculator.py       # Test suite
│   └── test_list.txt           # Test identifiers
├── cicd/
│   ├── pipeline.sh             # Main automation script
│   ├── mutate_random_function.py # Mutation script
│   └── temp/                   # Temporary files (gitignored)
│       ├── launchable-session.txt
│       ├── launchable-subset.txt
│       └── test-results/
│           └── subset.xml
├── requirements.txt
├── CLAUDE.md
├── README.md
└── .cloudbees/workflows/
    └── pipeline.yaml
```

## Key Changes Summary

### 1. Directory Refactoring
- ✅ Source code: `calculator_project/` → `src/calculator/`
- ✅ Backup: `calculator_project_backup/` → `backup/calculator/`
- ✅ Tests: root → `test/`
- ✅ CI/CD scripts: root → `cicd/`
- ✅ Temp files: root → `cicd/temp/`

### 2. Pipeline Improvements
- ✅ Reset moved to **beginning** of loop
- ✅ All temp files in `cicd/temp/`
- ✅ Clean temp at start of each iteration

### 3. Configuration
```gitignore
__pycache__/
.pytest_cache
cicd/temp/        ← All CI/CD temporary files
.env
```

### 4. Documentation
- ✅ CLAUDE.md - Complete developer guide
- ✅ README.md - Step-by-step lab instructions
- ✅ All paths updated to new structure

## Benefits

1. **Clean separation** - Source, tests, CI/CD, and backups in separate directories
2. **Organized temp files** - All temporary files grouped with CI/CD scripts
3. **Logical flow** - Reset at start → mutate → test → report
4. **Git-friendly** - Single gitignore entry for all temp files
5. **Easy navigation** - Clear directory names and hierarchy

## Running the Project

```bash
# Set up environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run tests
pytest test/

# Run pipeline
./cicd/pipeline.sh 5

# Check results
cat cicd/temp/launchable-subset.txt
ls cicd/temp/test-results/
```

## File Organization

### Source Code (`src/`)
- Production calculator code
- Imported by tests

### Tests (`test/`)
- Test suite
- Test identifiers

### CI/CD (`cicd/`)
- Pipeline automation
- Mutation scripts
- Temporary files (gitignored)

### Backup (`backup/`)
- Clean state for reset
- Not modified during pipeline

This structure follows best practices for Python project organization while keeping CI/CD concerns separate from source code.
