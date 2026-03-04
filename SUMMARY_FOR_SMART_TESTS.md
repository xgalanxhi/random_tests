# Smart Tests Bug Report: Incorrect File Change Detection

**Date:** March 4, 2026
**Workspace:** `8c8df396-03d5-4d10-9a7d-151e00947166/e8c3f3f1-8a16-4443-a345-58fddf4bb34d`
**Severity:** High - Affects core change detection functionality

---

## Problem Statement

The `smart-tests compare subsets` command consistently reports **incorrect files** as the cause of test ranking changes. In 10/10 test cases, Smart Tests identified the wrong source files.

---

## Quick Evidence

| Comparison | Smart Tests Says | Git Actually Changed | Correct? |
|------------|------------------|---------------------|----------|
| 1960637 → 1960670 | custom_op_55.py | custom_op_60.py | ❌ NO |
| 1960670 → 1960672 | custom_op_55.py | custom_op_60.py, custom_op_63.py | ❌ NO |
| 1960672 → 1960674 | custom_op_55.py | custom_op_50.py, custom_op_63.py | ❌ NO |
| 1960674 → 1960680 | custom_op_55.py | custom_op_46.py, custom_op_50.py | ❌ NO |
| 1960680 → 1960686 | custom_op_55.py | custom_op_46.py, custom_op_89.py | ❌ NO |
| 1960686 → 1960694 | custom_op_55.py | custom_op_62.py, custom_op_89.py | ❌ NO |
| 1960694 → 1960705 | custom_op_18.py | custom_op_62.py, custom_op_89.py | ❌ NO |
| 1960705 → 1960708 | custom_op_18.py | custom_op_81.py, custom_op_89.py | ❌ NO |
| 1960708 → 1960714 | custom_op_18.py | custom_op_49.py, custom_op_81.py | ❌ NO |
| 1960714 → 1960719 | custom_op_18.py | custom_op_49.py, custom_op_50.py | ❌ NO |

**Accuracy: 0/10 (0%)**

---

## Detailed Example

### Comparison: Subset 1960714 → 1960719

**Smart Tests Output:**
```
PTS subset change summary:
────────────────────────────────
-> 102 tests analyzed | 52 ↑ promoted | 49 ↓ demoted
-> Code files affected: src/calculator/custom_op_18.py  <-- WRONG!
────────────────────────────────
```

**Git Reality:**
```bash
$ git show --stat 252c374
commit 252c3744de878cf59e1fbe0e5ad886c22264c6ce
Date:   Wed Mar 4 11:31:01 2026 +0100

    next iteration 10

 src/calculator/custom_op_49.py | 2 +-
 src/calculator/custom_op_50.py | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
```

**Verification:**
- Subset 1960714 → Build `b5370ab` (iteration 9)
- Subset 1960719 → Build `252c374` (iteration 10)
- Files that changed: `custom_op_49.py`, `custom_op_50.py`
- File Smart Tests reported: `custom_op_18.py` ❌

**Note:** File `custom_op_18.py` was NEVER modified in any iteration!

---

## Complete Data Set

### Build/Subset Mapping

| Iter | Commit | Build Name | Subset ID | Files Actually Changed |
|------|--------|------------|-----------|------------------------|
| 1 | b1f2e5d | b1f2e5d | 1960670 | custom_op_60.py |
| 2 | c73f300 | c73f300 | 1960672 | custom_op_60.py, custom_op_63.py |
| 3 | eb7e141 | eb7e141 | 1960674 | custom_op_50.py, custom_op_63.py |
| 4 | 2c567d3 | 2c567d3 | 1960680 | custom_op_46.py, custom_op_50.py |
| 5 | 91387c5 | 91387c5 | 1960686 | custom_op_46.py, custom_op_89.py |
| 6 | 2f17c1e | 2f17c1e | 1960694 | custom_op_62.py, custom_op_89.py |
| 7 | 4717f41 | 4717f41 | 1960705 | custom_op_62.py, custom_op_89.py |
| 8 | 233fa5d | 233fa5d | 1960708 | custom_op_81.py, custom_op_89.py |
| 9 | b5370ab | b5370ab | 1960714 | custom_op_49.py, custom_op_81.py |
| 10 | 252c374 | 252c374 | 1960719 | custom_op_49.py, custom_op_50.py |

### What Smart Tests Reported

| Comparison | Subset IDs | Smart Tests Claimed |
|------------|------------|---------------------|
| 2 | 1960637 → 1960670 | custom_op_55.py |
| 3 | 1960670 → 1960672 | custom_op_55.py |
| 4 | 1960672 → 1960674 | custom_op_55.py |
| 5 | 1960674 → 1960680 | custom_op_55.py |
| 6 | 1960680 → 1960686 | custom_op_55.py |
| 7 | 1960686 → 1960694 | custom_op_55.py |
| 8 | 1960694 → 1960705 | custom_op_18.py |
| 9 | 1960705 → 1960708 | custom_op_18.py |
| 10 | 1960708 → 1960714 | custom_op_18.py |
| 11 | 1960714 → 1960719 | custom_op_18.py |

**Files Smart Tests blamed: custom_op_18.py, custom_op_55.py**
**Files actually changed: custom_op_46, 49, 50, 60, 62, 63, 81, 89**
**Overlap: NONE**

---

## How We Recorded Builds

```bash
# Mutate code
python cicd/mutate_random_function.py

# Commit changes
git add src/calculator
git commit -m "next iteration $i"

# Get commit hash for build name
NAME=$(git rev-parse --short HEAD)

# Record build with Smart Tests
smart-tests record build --build $NAME

# Create test session
smart-tests record session --test-suite "random_pytest" --observation --build $NAME

# Generate subset
cat test/test_list.txt | smart-tests subset --session $(cat cicd/temp/session.txt) --target 20% pytest
```

The workflow is correct - commits happen before builds are recorded.

---

##Files Attached

1. **smart_tests_issue_report.md** - Full detailed report
2. **example_comparison_output.txt** - Raw Smart Tests comparison output
3. **verify_git_changes.sh** - Script to verify git changes
4. **cicd/subset_history.txt** - All subset IDs from pipeline runs
5. **cicd/pipeline.sh** - Pipeline script showing workflow

---

## Impact

- ❌ Users cannot trust change detection
- ❌ Cannot validate ML model is learning correctly
- ❌ Cannot debug test selection issues
- ❌ Undermines confidence in Smart Tests predictions

---

## Reproduction

```bash
# Run pipeline
./cicd/pipeline.sh 10

# Compare any two consecutive subsets
smart-tests compare subsets --subset-id-before 1960714 --subset-id-after 1960719

# Verify with git
git show --stat 252c374

# Observe mismatch
```

---

## Questions

1. How does `compare subsets` determine changed files?
2. Does it use git diff of the associated builds?
3. Could there be caching causing stale results?
4. How can we debug what Smart Tests sees for a build's changes?

---

## Contact

**Xhesi Galanxhi**
xgalanxhi@cloudbees.com
CloudBees
