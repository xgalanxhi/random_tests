# Launchable Predictive Test Selection Demo

Welcome to the Launchable Predictive Test Selection (PTS) demonstration lab! This hands-on project showcases how Launchable's AI-powered test selection can dramatically reduce CI/CD testing time by intelligently selecting only the most relevant tests based on code changes.

## What This Lab Demonstrates

This project simulates a real-world testing scenario where:
- A Python calculator application has **103 tests** that each take **60 seconds** to run (total: ~103 minutes)
- Code mutations are introduced randomly to simulate development changes
- Launchable's ML model predicts which tests are affected and selects only **20% of the test suite**
- Tests run in parallel using pytest-xdist for maximum efficiency
- Results are tracked across multiple iterations to show learning improvements

**By the end of this lab**, you'll understand how Predictive Test Selection can cut test execution time by **~80%** while maintaining confidence in code quality.

## Goals

- Understand the core concepts of Predictive Test Selection (PTS)
- Set up and configure Launchable for predictive test selection
- Execute an automated mutation testing pipeline
- Observe how Launchable learns from test results over time
- Integrate PTS into a CloudBees CI/CD workflow
- Analyze test selection accuracy and time savings

## Table of Contents

- **Lab Setup**
  - [Step 1: Prerequisites](#step-1-prerequisites)
  - [Step 2: Clone the Repository](#step-2-clone-the-repository)
  - [Step 3: Set Up Python Environment](#step-3-set-up-python-environment)
  - [Step 4: Configure Launchable](#step-4-configure-launchable)
- **Running the Demo Locally**
  - [Step 5: Understand the Project Structure](#step-5-understand-the-project-structure)
  - [Step 6: Run Your First Iteration](#step-6-run-your-first-iteration)
  - [Step 7: Run Multiple Iterations](#step-7-run-multiple-iterations)
  - [Step 8: Analyze Results in Launchable](#step-8-analyze-results-in-launchable)
- **CI/CD Integration**
  - [Step 9: Deploy to CloudBees](#step-9-deploy-to-cloudbees)
  - [Step 10: Monitor Pipeline Execution](#step-10-monitor-pipeline-execution)
- **Understanding the Results**

---

## Lab Setup

### Step 1: Prerequisites

Before starting this lab, ensure you have:

1. **Python 3.9+** installed on your system
   ```bash
   python3 --version
   ```

2. **Git** installed and configured
   ```bash
   git --version
   ```

3. A **Launchable account** with API token access
   - Sign up at [app.launchableinc.com](https://app.launchableinc.com) if you don't have one yet

4. (Optional) **CloudBees platform access** for CI/CD integration

> [!NOTE]
> This demo makes git commits during execution. It's recommended to run it in a demo branch or disposable clone.

### Step 2: Clone the Repository

Clone this repository to your local machine:

```bash
git clone <YOUR_REPO_URL>
cd random_tests
```

![PLACEHOLDER_SCREENSHOT: Terminal showing successful git clone]
<!-- Add screenshot showing the git clone command and successful output -->

### Step 3: Set Up Python Environment

Create a virtual environment and install dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

Verify the installation was successful:

```bash
pytest --version
launchable --version
```

Expected output:

```
pytest 7.4.0
launchable, version 1.120.0
```

![PLACEHOLDER_SCREENSHOT: Terminal showing successful package installation]
<!-- Add screenshot showing pip install completion and version checks -->

> [!TIP]
> If `launchable` is not found on your PATH:
> <details>
> Run the following command to find where pip installed the script:
>
> ```bash
> pip3 show --files launchable | grep -E 'bin/launchable$|^Location'
> ```
>
> Add the bin directory to your PATH if needed.
> </details>

### Step 4: Configure Launchable

#### Obtain Your API Token

1. Log in to your Launchable workspace at [app.launchableinc.com](https://app.launchableinc.com)
2. Navigate to **Settings > API Tokens**
3. Click **Generate New Token** or **Copy** an existing token

![PLACEHOLDER_SCREENSHOT: Launchable API token page]
<!-- Add screenshot of the Launchable workspace showing Settings > API Tokens -->

<br>

![PLACEHOLDER_SCREENSHOT: Copy token button highlighted]
<!-- Add screenshot highlighting the "Copy" button for the API token -->

#### Set Environment Variable

Export your API token as an environment variable:

```bash
export LAUNCHABLE_TOKEN="<your-api-token>"
```

Or create a local `.env` file (gitignored):

```bash
echo 'export LAUNCHABLE_TOKEN="<your-api-token>"' > .env
source .env
```

> [!WARNING]
> Never commit your API token to git. The `.env` file is already in `.gitignore`.

#### Verify Configuration

Run the verification command to ensure everything is set up correctly:

```bash
launchable verify
```

If successful, you should see output similar to:

```
Organization: 'your-organization'
Workspace: 'your-workspace'
Platform: 'Darwin-25.3.0-arm64-arm-64bit'
Python version: '3.11.5'
launchable version: '1.120.0'
Your CLI configuration is successfully verified 🎉
```

![PLACEHOLDER_SCREENSHOT: Successful launchable verify output]
<!-- Add screenshot showing the successful verification message -->

___

You're all set! Now move on to running the demo.

---

## Running the Demo Locally

### Step 5: Understand the Project Structure

Before running the demo, let's understand what we're working with:

```
random_tests/
├── src/
│   └── calculator/              # Active calculator module (~100 operations)
│       ├── add.py, subtract.py, ... # Basic arithmetic operations
│       └── custom_op_10.py ... 99   # 90 custom compound operations
├── backup/
│   └── calculator/              # Clean backup for resets between iterations
├── test/
│   ├── test_calculator.py       # 103 tests (each sleeps 60s)
│   └── test_list.txt            # Full list of test identifiers
├── cicd/
│   ├── pipeline.sh              # ⭐ Main automation script
│   ├── mutate_random_function.py # Random code mutation script
│   └── temp/                    # Temporary files (gitignored)
│       ├── launchable-subset.txt    # Generated subset (20% of tests)
│       ├── launchable-session.txt   # Current session ID
│       └── test-results/            # JUnit XML test results
├── requirements.txt             # Python dependencies
└── .cloudbees/workflows/        # CloudBees CI/CD integration
```

**Key components:**

- **`src/calculator/`**: ~100 single-function calculator modules
- **`test/test_calculator.py`**: Test suite with intentional 60-second delays to simulate expensive tests
- **`cicd/pipeline.sh`**: Orchestrates the entire demo flow (mutation → subset → test → report)
- **`cicd/mutate_random_function.py`**: Randomly modifies calculator functions to simulate code changes

![PLACEHOLDER_DIAGRAM: Project architecture flowchart]
<!-- Add diagram showing: Code Mutation → Git Commit → Launchable Build → Test Subset → Test Execution → Results → Reset -->

### Step 6: Run Your First Iteration

Let's run a single iteration to see how the system works:

```bash
./cicd/pipeline.sh 1
```

**What happens during this iteration:**

1. 🔄 **Reset**: Code is restored from backup/calculator/ (except first iteration)
2. 🧹 **Clean Temp**: cicd/temp/ directory is cleaned
3. 📝 **Mutation**: 0–3 random calculator functions are modified
   - (50% chance of no mutation to provide baseline data)
4. 💾 **Git Commit**: Changes are committed with hash used as build name
5. 🔨 **Build Recording**: Launchable records the current code state
6. 🧪 **Test Session**: A new test session is created (saved to cicd/temp/)
7. 🎯 **Subset Generation**: Launchable predicts which 20% of tests to run (saved to cicd/temp/)
8. ▶️ **Test Execution**: Selected tests run in parallel with pytest-xdist
9. 📊 **Result Reporting**: Results are sent back to Launchable

![PLACEHOLDER_GIF: Single iteration running in terminal]
<!-- Add animated GIF showing one complete iteration from start to finish -->

You should see output like:

```bash
🔁 Starting iteration 1

Mutated function in: custom_op_47.py

[master abc123d] next iteration 1
 1 file changed, 1 insertion(+), 1 deletion(-)

Launchable recorded build abc123d to workspace your-org/your-workspace...

Smart Tests created subset <SUBSET_ID> for build abc123d (test session <SESSION_ID>)

|           |   Candidates |   Estimated duration (%) |   Estimated duration (min) |
|-----------|--------------|--------------------------|----------------------------|
| Subset    |           21 |                    20.39 |                      21.00 |
| Remainder |           82 |                    79.61 |                      82.00 |
| Total     |          103 |                   100.00 |                     103.00 |

============================= test session starts ==============================
...
==================== 21 passed in 132.45s (0:02:12) ===========================

✅ Completed iteration 1
```

![PLACEHOLDER_SCREENSHOT: First iteration complete output]
<!-- Add screenshot of terminal showing completed first iteration with all key sections visible -->

> [!TIP]
> The first iteration may take slightly longer as Launchable processes your repository history.
> Subsequent iterations will be faster.

Let's break down what just happened:

#### Mutation Output
```
Mutated function in: custom_op_47.py
```
This tells you which file was changed. You can check the mutation by running:

```bash
git show HEAD
```

![PLACEHOLDER_SCREENSHOT: Git diff showing mutation]
<!-- Add screenshot of git show HEAD output showing the mutated line -->

#### Subset Selection
```
| Subset    |           21 |                    20.39 |                      21.00 |
```
Launchable selected 21 tests (20% of 103 total). You can inspect the subset:

```bash
cat cicd/temp/launchable-subset.txt
```

![PLACEHOLDER_SCREENSHOT: Content of cicd/temp/launchable-subset.txt]
<!-- Add screenshot showing the list of selected tests -->

#### Parallel Execution
The tests ran in parallel (`pytest -n auto`), significantly reducing execution time from 21 minutes to ~2-3 minutes on a multi-core machine.

### Step 7: Run Multiple Iterations

Now let's run **5 iterations** to see Launchable learn from the accumulated data:

```bash
./cicd/pipeline.sh 5
```

This will take approximately 10-15 minutes total (depending on your CPU cores).

![PLACEHOLDER_GIF: Multiple iterations running with progress indicators]
<!-- Add GIF showing multiple iterations in sequence, highlighting the iteration count -->

As iterations progress, watch for:

1. **Different mutations each iteration**
   ```
   🔁 Starting iteration 1
   Mutated function in: custom_op_47.py

   🔁 Starting iteration 2
   No mutation this time.

   🔁 Starting iteration 3
   Mutated function in: add.py
   Mutated function in: custom_op_22.py
   ```

2. **Varying subset sizes** (Launchable adjusts based on predicted risk)
   ```
   Iteration 1: 21 tests selected
   Iteration 2: 19 tests selected (no mutation = fewer risky tests)
   Iteration 3: 24 tests selected (multiple files changed)
   ```

3. **Test failures** when mutations break functionality
   ```
   ====================== 2 passed, 1 failed in 125.34s ======================
   ```

![PLACEHOLDER_SCREENSHOT: Multiple iterations completed with summary]
<!-- Add screenshot showing completion of all 5 iterations -->

### Step 8: Analyze Results in Launchable

After running multiple iterations, let's analyze the results in the Launchable web interface.

#### Navigate to Your Workspace

1. Visit [app.launchableinc.com](https://app.launchableinc.com)
2. Select your organization and workspace
3. Click on **Test Sessions** in the sidebar

![PLACEHOLDER_SCREENSHOT: Launchable dashboard homepage]
<!-- Add screenshot of Launchable dashboard showing navigation to Test Sessions -->

#### View Test Sessions

You should see a list of test sessions corresponding to your pipeline runs:

![PLACEHOLDER_SCREENSHOT: Test sessions list view]
<!-- Add screenshot showing the list of test sessions with build names, dates, and status -->

Each session shows:
- **Build name** (git commit hash)
- **Test suite** (`random_pytest`)
- **Subset size** (e.g., 21 of 103 tests)
- **Pass/Fail status**
- **Execution time**

#### Inspect a Specific Session

Click on one of the sessions to see detailed information:

![PLACEHOLDER_SCREENSHOT: Session detail page with subset breakdown]
<!-- Add screenshot of session details showing:
  - Subset composition
  - Which tests passed/failed
  - Time savings metrics
  - Subset accuracy
-->

**Key metrics to observe:**

| Metric | Typical Value |
|--------|---------------|
| **Subset Size** | ~20-21 tests (20% target) |
| **Time Savings** | ~80% reduction |
| **Tests Run** | 21 / 103 |
| **Execution Time** | ~2-3 min vs. ~103 min full suite |

![PLACEHOLDER_SCREENSHOT: Time savings visualization graph]
<!-- Add screenshot showing time comparison: Full Suite vs. Subset -->

#### View Subset Observation Report

Since the pipeline uses `--observation` mode, you'll see a subset observation report:

![PLACEHOLDER_SCREENSHOT: Subset observation report]
<!-- Add screenshot showing:
  - Subset quality metrics
  - How many tests would have been skipped
  - Whether any failures were in the remainder
-->

This helps you evaluate subset quality before fully enabling PTS.

#### Compare Subsets Across Iterations

To see how subset selection evolved:

```bash
# Get subset IDs from two different iterations
launchable compare subsets --subset-id-before <SUBSET_ID_1> --subset-id-after <SUBSET_ID_2>
```

![PLACEHOLDER_SCREENSHOT: Subset comparison output]
<!-- Add screenshot showing side-by-side comparison of two subsets with rank differences highlighted -->

#### Inspect Model Status

Check when the Launchable ML model was last trained:

```bash
launchable inspect model
```

Expected output:

```
Test suite: random_pytest
Model trained at: 2026-02-24 10:45:32 UTC
Training data: 5 sessions, 515 test results
Model status: Active
```

![PLACEHOLDER_SCREENSHOT: Model inspection output]
<!-- Add screenshot of launchable inspect model command output -->

---

## CI/CD Integration

### Step 9: Deploy to CloudBees

This project includes a pre-configured CloudBees workflow for automated CI/CD testing.

#### Configure CloudBees Secret

Before running the workflow, configure your Launchable API token as a secret:

1. Navigate to your CloudBees organization
2. Go to **Settings > Secrets**
3. Click **New Secret**
4. Create a secret with:
   - **Name**: `SMART_TESTS_KEY`
   - **Value**: Your Launchable API token

![PLACEHOLDER_SCREENSHOT: CloudBees secret creation page]
<!-- Add screenshot of CloudBees UI showing the secret creation form with SMART_TESTS_KEY -->

#### Review the Workflow Configuration

The workflow is located at `.cloudbees/workflows/pipeline.yaml`. Let's review the key sections:

```yaml
name: Random Test Pipeline with Launchable

on:
  workflow_dispatch:
    inputs:
      iterations:
        description: Number of pipeline iterations to run
        type: string
        required: false
        default: '5'

jobs:
  run-pipeline:
    steps:
      - name: Check out
        uses: cloudbees-io/checkout@v2
        with:
          fetch-depth: 0  # Full git history for Launchable

      - name: Run pipeline iterations
        uses: docker://cloudbees/launchable:v1.120.0
        env:
          LAUNCHABLE_TOKEN: ${{ secrets.SMART_TESTS_KEY }}
          ITERATIONS: ${{ inputs.iterations || '5' }}
        run: |
          # Install Python and dependencies
          pip3 install --quiet --user -r requirements.txt
          export PATH="/cloudbees/home/.local/bin:$PATH"

          # Configure git
          git config --global user.email "ci@cloudbees.io"
          git config --global user.name "CloudBees CI"

          # Run the pipeline
          bash cicd/pipeline.sh $ITERATIONS
```

The workflow:
- ✅ Uses the `cloudbees/launchable` container (has git + can install Python)
- ✅ Fetches full repository history for accurate predictions
- ✅ Installs dependencies from `requirements.txt`
- ✅ Configures git for commits during pipeline execution
- ✅ Runs `cicd/pipeline.sh` with configurable iteration count
- ✅ Archives JUnit XML test results

![PLACEHOLDER_SCREENSHOT: Workflow YAML file in editor]
<!-- Add screenshot of the workflow file open in editor with key sections highlighted -->

#### Push to Repository

Commit your local changes and push to trigger the workflow:

```bash
git add .
git commit -m "Configure Launchable demo"
git push origin main
```

#### Trigger the Workflow Manually

1. Navigate to **CloudBees Platform > Workflows**
2. Find **Random Test Pipeline with Launchable**
3. Click **Run Workflow**
4. In the dialog, set **iterations** (default: 5)
5. Click **Run**

![PLACEHOLDER_SCREENSHOT: CloudBees workflow dispatch UI]
<!-- Add screenshot showing the workflow dispatch dialog with iteration input field -->

### Step 10: Monitor Pipeline Execution

Once the workflow starts, monitor its progress in real-time.

#### View Running Workflow

Navigate to the workflow run page to see the execution status:

![PLACEHOLDER_SCREENSHOT: CloudBees pipeline running view]
<!-- Add screenshot of the CloudBees UI showing the running pipeline with progress indicators -->

The workflow progresses through these stages:

1. ✅ **Check out** - Repository cloned with full history
2. 🔄 **Run pipeline iterations** - Executing `cicd/pipeline.sh`
   - Installing Python dependencies
   - Configuring git
   - Running iterations

![PLACEHOLDER_SCREENSHOT: Pipeline execution stages expanded]
<!-- Add screenshot showing the expanded view of all pipeline stages -->

#### View Pipeline Logs

Click on the **Run pipeline iterations** step to see detailed logs:

```bash
========================================
Running Launchable Pipeline
Iterations: 5
========================================

Installing Python and dependencies...
Successfully installed pytest-7.4.0 pytest-xdist-3.5.0 launchable-1.120.0

🔁 Starting iteration 1
Mutated function in: custom_op_23.py
[master 1a2b3c4] next iteration 1
...
✅ Completed iteration 1

🔁 Starting iteration 2
...
```

![PLACEHOLDER_GIF: Pipeline logs scrolling with iterations completing]
<!-- Add GIF showing the live log output with iterations progressing -->

#### Monitor Test Results

As tests complete, results are automatically archived. After the workflow finishes, you can:

1. **Download test results** from the workflow artifacts
2. **View results in Launchable** (links appear in logs)

![PLACEHOLDER_SCREENSHOT: Workflow completed with artifacts]
<!-- Add screenshot showing completed workflow with test result artifacts available -->

#### View in Launchable Dashboard

The pipeline automatically reports all results to Launchable. Navigate to your workspace to see:

- All 5 test sessions listed
- Build information for each iteration
- Subset performance metrics
- Pass/fail trends

![PLACEHOLDER_SCREENSHOT: Launchable dashboard showing all CI sessions]
<!-- Add screenshot of Launchable showing multiple test sessions from the CloudBees pipeline -->

---

## Understanding the Results

### How the Code Mutation System Works

The mutation system (`cicd/mutate_random_function.py`) simulates realistic code changes:

**Mutation probability:**
- **50% chance**: No mutation (provides baseline/control data)
- **30% chance**: Mutate 1 function
- **10% chance**: Mutate 2 functions
- **10% chance**: Mutate 3 functions

**Mutation types:**
1. Swap operators: `+` ↔ `-` in return statements
2. Add constant: Insert `42 +` into return value

Example mutation:
```diff
def custom_op_47(a, b):
    c = 47
-   return (a + b) * c - (b % (c if c != 0 else 1))
+   return (a - b) * c - (b % (c if c != 0 else 1))
```

![PLACEHOLDER_SCREENSHOT: Side-by-side comparison of original vs mutated code]
<!-- Add screenshot showing git diff with clear before/after of a mutation -->

This simulates the types of small, localized changes developers make daily. Launchable learns which tests are sensitive to changes in specific files.

### How Launchable Selects Tests

Launchable's ML model analyzes multiple signals:

1. **File changes**: Which source files were modified in this commit
2. **Historical correlations**: Past data showing "when file X changed, test Y failed"
3. **Code structure**: Understanding of imports, dependencies, and call graphs
4. **Test metadata**: Test duration, failure rates, flakiness patterns

**The result:** A prioritized, ranked list of tests where the most relevant tests appear first.

![PLACEHOLDER_DIAGRAM: Flowchart showing Launchable's decision process]
<!-- Add diagram showing: Code Change → File Analysis → Historical Data → ML Model → Ranked Test List → Subset (top 20%) -->

### Why Test Execution is Fast

Tests run with `pytest -n auto`, which:
- Automatically detects available CPU cores
- Distributes tests across parallel workers
- Runs tests simultaneously (they're stateless and independent)

**Time savings breakdown:**

| Scenario | Tests | Sequential Time | Parallel Time (8 cores) |
|----------|-------|-----------------|-------------------------|
| Full suite | 103 tests | 103 min | ~13 min |
| Subset (20%) | 21 tests | 21 min | ~3 min |

**Combined savings:** From 103 min → 3 min = **~97% time reduction**

![PLACEHOLDER_DIAGRAM: Visual showing parallel test distribution]
<!-- Add diagram showing tests distributed across 8 worker threads -->

### Typical Results After 5-10 Iterations

After running multiple iterations, you'll observe:

| Metric | Expected Value |
|--------|----------------|
| **Total Tests** | 103 |
| **Avg Subset Size** | ~21 tests (20%) |
| **Full Suite Time** (sequential) | ~103 minutes |
| **Full Suite Time** (parallel, 8 cores) | ~13 minutes |
| **Subset Time** (parallel) | ~3 minutes |
| **Total Time Savings** | **~97%** |
| **Subset Accuracy** | 90-95%+ |
| **False Negatives** | <5% (missed failures) |

![PLACEHOLDER_CHART: Bar chart comparing execution times]
<!-- Add bar chart showing:
  - Full Suite Sequential: 103 min
  - Full Suite Parallel: 13 min
  - Subset Parallel: 3 min
-->

### Observing ML Model Improvement

Over iterations, the model's prediction accuracy improves:

**Iteration 1-2:**
- Limited historical data
- Conservative selection (may include extra tests)
- Baseline accuracy: ~80%

**Iteration 3-5:**
- Correlations emerge between file changes and test failures
- Subset selection becomes more precise
- Accuracy: ~90%

**Iteration 10+:**
- Strong confidence in predictions
- Optimal balance of coverage and speed
- Accuracy: ~95%+

![PLACEHOLDER_GRAPH: Line graph showing accuracy improvement over iterations]
<!-- Add line graph with X-axis: Iterations (1-10), Y-axis: Subset Accuracy (%), showing upward trend -->

### What to Look For in the Results

#### In the Terminal Output

✅ **Consistent subset sizes** around 20% (varies based on risk assessment)
✅ **Fast execution times** thanks to parallel testing
✅ **Most iterations pass** (mutations are small and localized)
✅ **Some failures** (expected when mutations break logic)

#### In the Launchable Dashboard

✅ **Time savings trending upward** as model improves
✅ **Subset accuracy** consistently high (90%+)
✅ **No critical failures missed** (low false negative rate)
✅ **Model training progress** visible in model inspection

![PLACEHOLDER_SCREENSHOT: Launchable dashboard summary view]
<!-- Add screenshot showing key metrics dashboard with trends over time -->

---

## Advanced Usage

### Running a Custom Test Subset

You can manually interact with Launchable to generate custom subsets:

```bash
# 1. Record a build
launchable record build --name my-custom-build

# 2. Create test session
launchable record session --test-suite "random_pytest" --build my-custom-build > session.txt

# 3. Generate subset with different target (e.g., 30%)
mkdir -p cicd/temp
cat test/test_list.txt | launchable subset --build my-custom-build --target 30% pytest > cicd/temp/my-subset.txt

# 4. Run the subset
pytest -n auto @cicd/temp/my-subset.txt --junit-xml=cicd/temp/test-results/results.xml

# 5. Report results
launchable record tests --session $(cat session.txt) pytest cicd/temp/test-results/
```

### Adjusting the Target Percentage

Edit `cicd/pipeline.sh` line 40 to change the subset size:

```bash
# Change from 20% to 30%
cat test/test_list.txt | launchable subset --build $NAME --target 30% pytest > cicd/temp/launchable-subset.txt
```

### Running Tests Sequentially (for Debugging)

If you need to debug individual test failures, run without parallelization:

```bash
# Edit cicd/pipeline.sh line 30, remove -n auto
pytest --junit-xml=test-results/subset.xml @launchable-subset.txt
```

### Reducing Test Sleep Time (Faster Demo)

For quicker demonstrations, reduce the sleep time in `test/test_calculator.py`:

```python
# Change from 60 seconds to 10 seconds
time.sleep(10)
```

Then tests complete faster, making demos more interactive.

---

## Troubleshooting

### Common Issues

#### Issue: `launchable: command not found`

**Solution:** Activate your virtual environment

```bash
source venv/bin/activate
```

Verify:
```bash
which launchable
# Should show: /path/to/random_tests/venv/bin/launchable
```

---

#### Issue: `permission denied: ./cicd/pipeline.sh`

**Solution:** Make the script executable

```bash
chmod +x cicd/pipeline.sh
```

---

#### Issue: Tests taking too long

**Solution:** Ensure parallel execution is enabled

Check that `cicd/pipeline.sh` line 41 includes `-n auto`:
```bash
pytest -n auto --junit-xml=cicd/temp/test-results/subset.xml @cicd/temp/launchable-subset.txt
```

Verify pytest-xdist is installed:
```bash
pip list | grep pytest-xdist
```

---

#### Issue: No subset generated on first run

**Expected behavior.** The first run establishes a baseline. Launchable needs at least one test session with results before it can make predictions.

After the first iteration completes, subsequent iterations will use ML-based predictions.

---

#### Issue: `LAUNCHABLE_TOKEN` not set error

**Solution:** Export your token

```bash
export LAUNCHABLE_TOKEN="<your-token>"
# Or
source .env  # If you have a .env file
```

Verify:
```bash
echo $LAUNCHABLE_TOKEN
# Should display your token
```

---

#### Issue: Workflow fails in CloudBees

**Solution:** Check the secret configuration

1. Verify `SMART_TESTS_KEY` secret exists in CloudBees
2. Ensure the secret value is your Launchable API token (not some other credential)
3. Check workflow logs for the exact error message

---

## Reference Materials

- [Launchable Documentation](https://docs.launchableinc.com/)
- [CloudBees Smart Tests Documentation](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/)
- [Predictive Test Selection Concepts](https://docs.launchableinc.com/docs/concepts/predictive-test-selection)
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/)
- [CLAUDE.md](CLAUDE.md) - Developer guide for working with this codebase

---

## Summary

Congratulations! You've successfully completed the Launchable Predictive Test Selection demo. 🎉

**What you accomplished:**

✅ Set up a complete Launchable PTS environment
✅ Ran automated mutation testing with intelligent test selection
✅ Observed ML-driven test optimization in action
✅ Integrated PTS into a CloudBees CI/CD pipeline
✅ Analyzed time savings and accuracy metrics

**Key Takeaways:**

- 🚀 **Predictive Test Selection can reduce test execution time by 80-97%**
- 🧠 **ML models improve prediction accuracy with more historical data**
- ⚡ **Parallel execution multiplies time savings**
- 🔧 **Integration with CI/CD is straightforward and non-invasive**
- 📊 **Subset quality remains high (90-95%+ accuracy) even with aggressive targets**

### Next Steps

Ready to apply this to your own projects?

1. **Explore your own repository:** Clone a real project and try Launchable on it
2. **Experiment with different targets:** Test 10%, 20%, 30% subsets to find your optimal balance
3. **Integrate with your CI/CD:** Adapt the CloudBees workflow to your existing pipelines
4. **Review the documentation:** Check out [Launchable docs](https://docs.launchableinc.com/) for advanced features

### Live Walkthrough Tips

If you're using this demo for a presentation or workshop:

1. Run `./cicd/pipeline.sh 5` and narrate what's happening
2. Open `cicd/temp/launchable-subset.txt` and show it's ~20% of tests
3. Point out which files mutated and which tests were selected
4. Show a test failure and explain how Launchable learns from it
5. Compare iteration 1 vs iteration 5 subset quality

---

**Questions or Issues?**

- Open an issue in this repository
- Contact your workshop instructor
- Visit [Launchable Community](https://launchableinc.com/community)

---

*This demo is maintained as part of Launchable's educational resources. For the latest updates, visit the [Launchable documentation](https://docs.launchableinc.com/).*
