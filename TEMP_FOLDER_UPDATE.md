# Temp Folder Location Update

## Final Structure

The `temp/` folder is now located inside `cicd/`:

```
cicd/
├── pipeline.sh
├── mutate_random_function.py
└── temp/                        # Temporary files (gitignored)
    ├── launchable-session.txt
    ├── launchable-subset.txt
    └── test-results/
        └── subset.xml
```

## Changes Made

### 1. Pipeline Script (`cicd/pipeline.sh`)
- ✅ Creates `cicd/temp/` directory at start
- ✅ All temporary files saved to `cicd/temp/`:
  - `cicd/temp/launchable-session.txt`
  - `cicd/temp/launchable-subset.txt`
  - `cicd/temp/test-results/`

### 2. Git Configuration (`.gitignore`)
```
__pycache__/
.pytest_cache
cicd/temp/     ← All temp files in cicd directory
.env
```

### 3. CloudBees Workflow (`.cloudbees/workflows/pipeline.yaml`)
```yaml
results-path: source/cicd/temp/test-results/*.xml
```

### 4. Documentation
- ✅ Updated `CLAUDE.md` - all references to `cicd/temp/`
- ✅ Updated `README.md` - all references to `cicd/temp/`

## Benefits

1. ✅ **Organized structure** - All CI/CD-related files in one place
2. ✅ **Cleaner root** - No temp files in workspace root
3. ✅ **Logical grouping** - Temp files with the scripts that generate them
4. ✅ **Easy cleanup** - `rm -rf cicd/temp/*`
5. ✅ **Git-friendly** - Single gitignore entry

## Usage

Run pipeline:
```bash
./cicd/pipeline.sh 5
```

Check generated files:
```bash
ls cicd/temp/
cat cicd/temp/launchable-subset.txt
```

Clean temp directory:
```bash
rm -rf cicd/temp/*
```
