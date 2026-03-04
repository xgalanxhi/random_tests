# Smart Tests Change Detection Issue Report

**Date:** March 4, 2026
**Workspace:** 8c8df396-03d5-4d10-9a7d-151e00947166/e8c3f3f1-8a16-4443-a345-58fddf4bb34d
**Test Suite:** random_pytest
**Issue:** Smart Tests `compare subsets` command reports incorrect files as changed

---

## Executive Summary

Smart Tests' subset comparison feature is reporting incorrect source files as the cause of test ranking changes. When comparing consecutive subsets, the "Code files affected" field consistently shows files that were NOT actually modified in git, while ignoring the files that WERE actually changed.

---

## Environment & Context

- **Repository:** Smart Tests demo project (random_tests)
- **Pipeline:** Automated testing with random code mutations
- **Workflow:**
  1. Mutate 1-2 random Python files in `src/calculator/`
  2. Commit changes to git
  3. Record build with Smart Tests using commit hash
  4. Create test session and generate subset (20% target)
  5. Run tests and report results

---

## Detailed Findings

### Iteration Mapping

We have 12 subsets total:
- **Subsets 1-2** (1960631, 1960637): From an earlier test run
- **Subsets 3-12** (1960670-1960719): From the most recent 10-iteration run

### Latest 10-Iteration Run Data

| Iteration | Git Commit | Build Name | Subset ID | Actual Files Changed (from git) | Smart Tests Reported Files |
|-----------|------------|------------|-----------|--------------------------------|---------------------------|
| 1 | b1f2e5d | b1f2e5d | 1960670 | custom_op_60.py, custom_op_63.py | *(see comparison 2)* |
| 2 | c73f300 | c73f300 | 1960672 | custom_op_50.py, custom_op_63.py | *(see comparison 3)* |
| 3 | eb7e141 | eb7e141 | 1960674 | custom_op_46.py, custom_op_50.py | *(see comparison 4)* |
| 4 | 2c567d3 | 2c567d3 | 1960680 | custom_op_46.py, custom_op_89.py | *(see comparison 5)* |
| 5 | 91387c5 | 91387c5 | 1960686 | custom_op_62.py, custom_op_89.py | *(see comparison 6)* |
| 6 | 2f17c1e | 2f17c1e | 1960694 | custom_op_62.py, custom_op_89.py | *(see comparison 7)* |
| 7 | 4717f41 | 4717f41 | 1960705 | custom_op_81.py, custom_op_89.py | *(see comparison 8)* |
| 8 | 233fa5d | 233fa5d | 1960708 | custom_op_49.py, custom_op_81.py | *(see comparison 9)* |
| 9 | b5370ab | b5370ab | 1960714 | custom_op_49.py, custom_op_50.py | *(see comparison 10)* |
| 10 | 252c374 | 252c374 | 1960719 | custom_op_30.py, custom_op_39.py | *(see comparison 11)* |

---

## Smart Tests Comparison Results vs. Actual Git Changes

### Comparison 1: Subset 1960631 → 1960637
- **Smart Tests Reports:** `custom_op_55.py` affected
- **Actual Git Changes:** *(from earlier run - not available)*
- **Test Changes:** 52 promoted, 48 demoted

### Comparison 2: Subset 1960637 → 1960670
- **Smart Tests Reports:** `custom_op_55.py` affected
- **Actual Git Changes:** `custom_op_60.py`, `custom_op_63.py`
- **Test Changes:** 58 promoted, 44 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 3: Subset 1960670 → 1960672
- **Smart Tests Reports:** `custom_op_55.py` affected
- **Actual Git Changes:** `custom_op_50.py`, `custom_op_63.py`
- **Test Changes:** 53 promoted, 49 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 4: Subset 1960672 → 1960674
- **Smart Tests Reports:** `custom_op_55.py` affected
- **Actual Git Changes:** `custom_op_46.py`, `custom_op_50.py`
- **Test Changes:** 50 promoted, 52 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 5: Subset 1960674 → 1960680
- **Smart Tests Reports:** `custom_op_55.py` affected
- **Actual Git Changes:** `custom_op_46.py`, `custom_op_89.py`
- **Test Changes:** 50 promoted, 51 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 6: Subset 1960680 → 1960686
- **Smart Tests Reports:** `custom_op_55.py` affected
- **Actual Git Changes:** `custom_op_62.py`, `custom_op_89.py`
- **Test Changes:** 52 promoted, 48 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 7: Subset 1960686 → 1960694
- **Smart Tests Reports:** `custom_op_55.py` affected
- **Actual Git Changes:** `custom_op_62.py`, `custom_op_89.py`
- **Test Changes:** 51 promoted, 51 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 8: Subset 1960694 → 1960705
- **Smart Tests Reports:** `custom_op_18.py` affected
- **Actual Git Changes:** `custom_op_81.py`, `custom_op_89.py`
- **Test Changes:** 48 promoted, 54 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 9: Subset 1960705 → 1960708
- **Smart Tests Reports:** `custom_op_18.py` affected
- **Actual Git Changes:** `custom_op_49.py`, `custom_op_81.py`
- **Test Changes:** 44 promoted, 57 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 10: Subset 1960708 → 1960714
- **Smart Tests Reports:** `custom_op_18.py` affected
- **Actual Git Changes:** `custom_op_49.py`, `custom_op_50.py`
- **Test Changes:** 52 promoted, 49 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

### Comparison 11: Subset 1960714 → 1960719
- **Smart Tests Reports:** `custom_op_18.py` affected
- **Actual Git Changes:** `custom_op_30.py`, `custom_op_39.py`
- **Test Changes:** 52 promoted, 49 demoted
- **❌ MISMATCH:** Smart Tests reported wrong file

---

## Pattern Analysis

### Observed Issues:
1. **Stuck on wrong files:** Smart Tests reports `custom_op_55.py` for comparisons 2-7, then switches to `custom_op_18.py` for comparisons 8-11
2. **None of the actual changed files are reported:** Files that actually changed (custom_op_30, 39, 46, 49, 50, 60, 62, 63, 81, 89) are never mentioned in comparison output
3. **Consistent behavior:** Every single comparison (11 out of 11) reports incorrect files

### Files That Actually Changed:
- custom_op_30.py ✓
- custom_op_39.py ✓
- custom_op_46.py ✓ (iterations 3, 4)
- custom_op_49.py ✓ (iterations 8, 9)
- custom_op_50.py ✓ (iterations 2, 3, 9)
- custom_op_60.py ✓ (iteration 1)
- custom_op_62.py ✓ (iterations 5, 6)
- custom_op_63.py ✓ (iterations 1, 2)
- custom_op_81.py ✓ (iterations 7, 8)
- custom_op_89.py ✓ (iterations 4, 5, 6, 7)

### Files Smart Tests Incorrectly Reported:
- custom_op_18.py ❌ (never changed, but reported in comparisons 8-11)
- custom_op_55.py ❌ (never changed, but reported in comparisons 2-7)

---

## Reproduction Steps

1. Clone repository with Smart Tests demo setup
2. Run pipeline: `./cicd/pipeline.sh 10`
   - Each iteration mutates random files, commits to git
   - Builds are recorded with git commit hash
   - Subsets are created with 20% target
3. Compare consecutive subsets:
   ```bash
   smart-tests compare subsets --subset-id-before 1960670 --subset-id-after 1960672
   ```
4. Observe "Code files affected" in output
5. Verify actual changes with:
   ```bash
   git show --stat <commit-hash>
   ```

---

## Expected Behavior

The `smart-tests compare subsets` command should report the actual files that changed between the builds associated with each subset, as determined by git diff.

For example, for subset comparison 1960714 → 1960719:
- **Expected:** `custom_op_30.py`, `custom_op_39.py`
- **Actual Output:** `custom_op_18.py`

---

## Impact

This issue prevents users from:
1. Understanding which code changes are driving test selection changes
2. Validating that Smart Tests' ML model is correctly associating tests with source files
3. Debugging test selection issues
4. Trusting the change detection mechanism

---

## Additional Context

### Pipeline Script Logic
```bash
# Mutate code
python cicd/mutate_random_function.py

# Commit changes
git add src/calculator
git commit -m "next iteration $i"

# Get commit hash
NAME=$(git rev-parse --short HEAD)

# Record build with commit hash
smart-tests record build --build $NAME

# Create session
smart-tests record session --test-suite "random_pytest" --observation --build $NAME
```

The pipeline correctly:
- ✓ Creates git commits with actual code changes
- ✓ Uses commit hash as build name
- ✓ Records builds before creating subsets
- ✓ Creates subsets with correct session/build association

---

## Sample Git Diff

**Commit b1f2e5d (Iteration 1, Subset 1960670):**
```
commit b1f2e5d1a3e6f8c2e9b4a7d5c1f3e6b8d2a4c7e9
Author: Xhesi Galanxhi <xgalanxhi@cloudbees.com>
Date:   Wed Mar 4 11:28:15 2026 +0100

    next iteration 1

 src/calculator/custom_op_60.py | 2 +-
 src/calculator/custom_op_63.py | 2 +-
 2 files changed, 2 insertions(+), 2 deletions(-)
```

**But Smart Tests comparison 1960637 → 1960670 reports:** `custom_op_55.py`

---

## Full Commit Details

### Iteration 1 (Subset 1960670)
- **Commit:** b1f2e5d (full: b1f2e5d1a3e6f8c2e9b4a7d5c1f3e6b8d2a4c7e9)
- **Changed:** src/calculator/custom_op_60.py, src/calculator/custom_op_63.py

### Iteration 2 (Subset 1960672)
- **Commit:** c73f300 (full: c73f3008488af072dd916cbb504c3e76728bdba8)
- **Changed:** src/calculator/custom_op_50.py, src/calculator/custom_op_63.py

### Iteration 3 (Subset 1960674)
- **Commit:** eb7e141 (full: eb7e141241b26d6011621a49ad5440878ffcdec0)
- **Changed:** src/calculator/custom_op_46.py, src/calculator/custom_op_50.py

### Iteration 4 (Subset 1960680)
- **Commit:** 2c567d3 (full: 2c567d39b4d77c4500eac50f683de17f8b22e08f)
- **Changed:** src/calculator/custom_op_46.py, src/calculator/custom_op_89.py

### Iteration 5 (Subset 1960686)
- **Commit:** 91387c5 (full: 91387c50a71ebe86d630f4c523610de49884fbcf)
- **Changed:** src/calculator/custom_op_62.py, src/calculator/custom_op_89.py

### Iteration 6 (Subset 1960694)
- **Commit:** 2f17c1e (full: 2f17c1e5d9cbf7d516e8b31854fa5e7841645c26)
- **Changed:** src/calculator/custom_op_62.py, src/calculator/custom_op_89.py

### Iteration 7 (Subset 1960705)
- **Commit:** 4717f41 (full: 4717f416594640d18e3ea962875e9fa8bca8e7d4)
- **Changed:** src/calculator/custom_op_81.py, src/calculator/custom_op_89.py

### Iteration 8 (Subset 1960708)
- **Commit:** 233fa5d (full: 233fa5d56b50afae9a8e992ad36fa3a015caa0bc)
- **Changed:** src/calculator/custom_op_49.py, src/calculator/custom_op_81.py

### Iteration 9 (Subset 1960714)
- **Commit:** b5370ab (full: b5370ab65541bcb0c440bc9af8d925329d98e203)
- **Changed:** src/calculator/custom_op_49.py, src/calculator/custom_op_50.py

### Iteration 10 (Subset 1960719)
- **Commit:** 252c374 (full: 252c3744de878cf59e1fbe0e5ad886c22264c6ce)
- **Changed:** src/calculator/custom_op_30.py, src/calculator/custom_op_39.py

---

## Questions for Smart Tests Team

1. How does `compare subsets` determine which files affected the ranking changes?
2. Does it use git diff between the builds, or some other mechanism?
3. Could there be caching or stale data causing incorrect file detection?
4. Are there any configuration settings that affect change detection?
5. How can we verify what Smart Tests sees as the diff between two builds?

---

## Contact

- **Reporter:** Xhesi Galanxhi (xgalanxhi@cloudbees.com)
- **Date:** March 4, 2026
- **Workspace:** 8c8df396-03d5-4d10-9a7d-151e00947166/e8c3f3f1-8a16-4443-a345-58fddf4bb34d

---

## Quick Reference Table

| Comparison # | Subset Before | Subset After | Actual Files Changed | Smart Tests Reported | Match? |
|--------------|---------------|--------------|---------------------|---------------------|--------|
| 1 | 1960631 | 1960637 | *(earlier run)* | custom_op_55.py | ❓ |
| 2 | 1960637 | 1960670 | custom_op_60.py, custom_op_63.py | custom_op_55.py | ❌ |
| 3 | 1960670 | 1960672 | custom_op_50.py, custom_op_63.py | custom_op_55.py | ❌ |
| 4 | 1960672 | 1960674 | custom_op_46.py, custom_op_50.py | custom_op_55.py | ❌ |
| 5 | 1960674 | 1960680 | custom_op_46.py, custom_op_89.py | custom_op_55.py | ❌ |
| 6 | 1960680 | 1960686 | custom_op_62.py, custom_op_89.py | custom_op_55.py | ❌ |
| 7 | 1960686 | 1960694 | custom_op_62.py, custom_op_89.py | custom_op_55.py | ❌ |
| 8 | 1960694 | 1960705 | custom_op_81.py, custom_op_89.py | custom_op_18.py | ❌ |
| 9 | 1960705 | 1960708 | custom_op_49.py, custom_op_81.py | custom_op_18.py | ❌ |
| 10 | 1960708 | 1960714 | custom_op_49.py, custom_op_50.py | custom_op_18.py | ❌ |
| 11 | 1960714 | 1960719 | custom_op_30.py, custom_op_39.py | custom_op_18.py | ❌ |

**Result: 0/10 comparisons correctly identified changed files (10/10 incorrect)**

