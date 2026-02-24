# Refactoring Summary

## Changes Made

The project has been refactored to follow a cleaner directory structure:

### Before:
```
random_tests/
├── calculator_project/
├── calculator_project_backup/
├── test_calculator.py
├── test_list.txt
└── pipeline.sh
```

### After:
```
random_tests/
├── src/
│   └── calculator/              # Source code
├── backup/
│   └── calculator/              # Backup copy
├── test/
│   ├── test_calculator.py       # Tests
│   └── test_list.txt           # Test identifiers
└── cicd/
    ├── pipeline.sh             # Pipeline automation
    └── mutate_random_function.py  # Mutation script
```

## Files Updated

### Code Files:
- ✅ `test/test_calculator.py` - Updated imports to use `from calculator import ...`
- ✅ `cicd/pipeline.sh` - Updated all path references
- ✅ `cicd/mutate_random_function.py` - Updated to point to `src/calculator/`
- ✅ `test/test_list.txt` - Updated test paths to `test/test_calculator.py::`

### Configuration Files:
- ✅ `.cloudbees/workflows/pipeline.yaml` - Updated to use `cicd/pipeline.sh`

### Documentation:
- ✅ `CLAUDE.md` - Updated all path references and examples
- ✅ `README.md` - Updated directory structure and all path references

## How to Use

Run tests:
```bash
pytest test/
```

Run pipeline:
```bash
./cicd/pipeline.sh <iterations>
```

Run mutation script:
```bash
python3 cicd/mutate_random_function.py
```

## Verification

The refactoring has been tested and verified:
- ✅ Calculator module imports correctly
- ✅ Directory structure is organized
- ✅ All paths have been updated
- ✅ Documentation reflects new structure
