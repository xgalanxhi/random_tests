# Smart Tests Predictive Test Selection Demo

Welcome to the Smart Tests Predictive Test Selection (PTS) demonstration lab! This hands-on project showcases how Smart Tests's AI-powered test selection can dramatically reduce CI/CD testing time by intelligently selecting only the most relevant tests based on code changes.

## What This Lab Demonstrates

This project simulates a real-world testing scenario where:
- A Python calculator application has **103 tests** that simulate expensive operations (configurable: 10-60 seconds each)
- Code mutations are introduced randomly to simulate development changes
- Smart Tests uses LLM-based code analysis to predict which tests are affected and selects only **20% of the test suite**
- Tests run in parallel using pytest-xdist for maximum efficiency
- Results are tracked across multiple iterations to show learning improvements
- Pipeline uses 10-second test delay for practical demos (configurable via `TEST_SLEEP_TIME`)

**By the end of this lab**, you'll understand how Predictive Test Selection can cut test execution time by **~80%** while maintaining confidence in code quality.

## Project Structure & Organization

This project follows a clean, organized structure that separates concerns:

```
random_tests/
├── src/calculator/          # Source code
├── backup/calculator/       # Clean backup for resets
├── test/                    # Test suite and identifiers
├── cicd/                    # CI/CD automation
│   ├── pipeline.sh
│   ├── mutate_random_function.py
│   ├── check_learning_progress.sh
│   └── temp/               # Temporary files (gitignored)
├── tools/                   # Utility tools
│   ├── validate_junit_xml.py
│   └── README.md
└── .cloudbees/workflows/    # CloudBees CI/CD integration
```

**Key Benefits:**
- ✅ **Clean separation** - Source, tests, CI/CD, and backups in dedicated directories
- ✅ **Organized temp files** - All temporary files grouped in `cicd/temp/` (gitignored)
- ✅ **Logical flow** - Pipeline resets at start → mutates → tests → reports
- ✅ **Easy navigation** - Clear directory names following Python best practices

## Goals

- Understand the core concepts of Predictive Test Selection (PTS)
- Set up and configure Smart Tests for predictive test selection
- Execute an automated mutation testing pipeline
- Observe how Smart Tests learns from test results over time
- Integrate PTS into a CloudBees CI/CD workflow
- Analyze test selection accuracy and time savings

## Table of Contents

- **Lab Setup**
  - [Step 1: Prerequisites](#step-1-prerequisites)
  - [Step 2: Clone the Repository](#step-2-clone-the-repository)
  - [Step 3: Set Up Python Environment](#step-3-set-up-python-environment)
  - [Step 4: Configure Smart Tests](#step-4-configure-smart-tests)
- **Running the Demo Locally**
  - [Step 5: Understand the Project Structure](#step-5-understand-the-project-structure)
  - [Step 6: Run Your First Iteration](#step-6-run-your-first-iteration)
  - [Step 7: Run Multiple Iterations](#step-7-run-multiple-iterations)
  - [Step 8: Analyze Results in Smart Tests](#step-8-analyze-results-in-smart-tests)
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

3. A **Smart Tests account** with API token access
   - Sign up at [cloudbees.io](https://cloudbees.io) if you don't have one yet

4. (Optional) **CloudBees platform access** for CI/CD integration

5. **Operating System**: Linux or macOS recommended. Windows users should use
   WSL or Git Bash — `pipeline.sh` requires a bash shell. Parallel test
   execution (`pytest -n auto`) uses all available CPU cores.

6. **Network Access**: The Smart Tests CLI communicates with the SaaS backend.
   Ensure outbound HTTPS access to `*.launchableinc.com` and `*.cloudbees.io`.
   See [Running under restricted networks](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/sending-data-to-smart-tests/recording-builds/running-under-restricted-networks)
   for proxy configurations.

> [!NOTE]
> This demo makes git commits during execution. It's recommended to run it in a demo branch or disposable clone.

> **PTS Requirements** (from the
> [onboarding guide](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/resources/onboarding-guide)):
>
> - Tests must report **binary pass/fail** results (performance/metric-only tests are not supported)
> - Tests must have **no inter-test dependencies** — PTS re-orders tests by priority
> - Test framework must support **test-to-file mapping** (mapping a test back to its source file)
> - Test results must be in **JUnit XML format** (see [tools/README.md](tools/README.md) for a validator)
> - Your team must be able to **edit CI scripts** to add Smart Tests CLI commands
> - The CLI requires **outbound HTTPS** access to the Smart Tests SaaS backend

### Supported Test Frameworks

This demo uses **pytest**, but Smart Tests supports 20+ test runners natively:

Android Debug Bridge (adb), Ant, Bazel, Behave, CTest, Cucumber, Cypress,
dotnet test, Go Test, GoogleTest, Gradle, Jest, Karma, Maven, minitest,
Playwright, prove (Perl), **pytest**, Robot, and RSpec.

For other frameworks, use the `file` or `raw` CLI profiles with
[JUnit XML](https://github.com/testmoapp/junitxml) output.
A [validator script](tools/README.md) is included in this repo to check your
XML reports before sending them to Smart Tests.

See the full [Integrations list](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/integrations/)
in the Smart Tests docs.

### Step 2: Clone the Repository

Clone this repository to your local machine:

```bash
git clone <YOUR_REPO_URL>
cd random_tests
```


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

The key dependencies installed are:

- `smart-tests-cli~=2.0` — Smart Tests CLI for predictive test selection
- `pytest` — Python test framework
- `pytest-xdist` — Parallel test execution (`-n auto`)

You can also install the CLI standalone via [uv](https://docs.astral.sh/uv/):

```bash
uv tool install smart-tests-cli~=2.0
```

Verify the installation was successful:

```bash
pytest --version
smart-tests --version
```

Expected output:

```
pytest 8.x.x
smart-tests version: '2.2.0'
```


> [!TIP]
> If `smart-tests` is not found on your PATH:
> <details>
> Run the following command to find where pip installed the script:
>
> ```bash
> pip3 show --files smart-tests | grep -E 'bin/smart-tests$|^Location'
> ```
>
> Add the bin directory to your PATH if needed.
> </details>

### Step 4: Configure Smart Tests

#### Obtain Your API Token

1. Log in to your Smart Tests workspace at [cloudbees.io](https://cloudbees.io)
2. Navigate to **Settings > API Tokens**
3. Click **Generate New Token** or **Copy** an existing token


<br>


#### Set Environment Variable

Export your API token as an environment variable:

```bash
export SMART_TESTS_TOKEN="<your-api-token>"
```

Or create a local `.env` file (gitignored):

```bash
echo 'export SMART_TESTS_TOKEN="<your-api-token>"' > .env
source .env
```

> [!WARNING]
> Never commit your API token to git. The `.env` file is already in `.gitignore`.

#### Verify Configuration

Run the verification command to ensure everything is set up correctly:

```bash
smart-tests verify
```

If successful, you should see output similar to:

```
Organization: 'your-organization'
Workspace: 'your-workspace'
Platform: 'Darwin-25.3.0-arm64-arm-64bit'
Python version: '3.13.x'
smart-tests version: '2.2.0'
Your CLI configuration is successfully verified 🎉
```


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
│   ├── test_calculator.py       # 103 tests (configurable sleep: 10-60s)
│   └── test_list.txt            # Full list of test identifiers
├── cicd/
│   ├── pipeline.sh              # ⭐ Main automation script
│   ├── mutate_random_function.py # Random code mutation script
│   ├── check_learning_progress.sh # Analyze Smart Tests learning across iterations
│   ├── subset_history.txt       # All subset IDs from pipeline runs
│   └── temp/                    # Temporary files (gitignored)
│       ├── subset.txt    # Generated subset (20% of tests)
│       ├── session.txt   # Current session ID
│       └── test-results/            # JUnit XML test results
├── requirements.txt             # Python dependencies
└── .cloudbees/workflows/        # CloudBees CI/CD integration
```

**Directory Organization:**

This project was refactored to follow Python best practices and CI/CD conventions:

**Source Code (`src/calculator/`)**
- ~100 single-function calculator modules (add.py, subtract.py, custom_op_10-99.py)
- Clean production code separate from tests and CI/CD
- Imported by tests via path manipulation

**Tests (`test/`)**
- `test_calculator.py` - Test suite with configurable delays (10-60s via `TEST_SLEEP_TIME`) to simulate expensive tests
- `test_list.txt` - Full list of test identifiers for Smart Tests

**CI/CD (`cicd/`)**
- `pipeline.sh` - Main automation script orchestrating the entire demo flow
- `mutate_random_function.py` - Randomly modifies calculator functions to simulate code changes
- `check_learning_progress.sh` - Analyzes how Smart Tests predictions evolved across iterations
- `subset_history.txt` - Tracks all subset IDs created by the pipeline (auto-generated)
- `temp/` - **All temporary files (gitignored)**:
  - `session.txt` - Current test session ID
  - `subset.txt` - Generated 20% test subset
  - `test-results/` - JUnit XML test output

**Backup (`backup/calculator/`)**
- Clean copy used to reset state between pipeline iterations
- Never modified during pipeline execution

**Benefits of this structure:**
- Clean separation between production code, tests, and CI/CD tooling
- All temporary files organized in one gitignored location
- Easy to navigate and understand
- Follows Python project conventions


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
5. 🔨 **Build Recording**: Smart Tests records the current code state
6. 🧪 **Test Session**: A new test session is created (saved to cicd/temp/)
7. 🎯 **Subset Generation**: Smart Tests predicts which 20% of tests to run (saved to cicd/temp/)
8. ▶️ **Test Execution**: Selected tests run in parallel with pytest-xdist
9. 📊 **Result Reporting**: Results are sent back to Smart Tests

> **⏱️ Test Execution Time:**
> The test suite is designed to simulate expensive tests with configurable sleep time:
>
> - **Default:** 60 seconds per test (simulates real-world expensive operations)
> - **Pipeline override:** 10 seconds per test (set via `TEST_SLEEP_TIME=10` for faster demos)
>
> This means:
> - **Full suite (103 tests):** ~103 min (60s/test) or ~17 min (10s/test) sequential
> - **Subset (21 tests, 20%):** ~21 min (60s/test) or ~3-4 min (10s/test) sequential
> - **With parallel execution (`-n auto`):** Time divided by number of CPU cores
>
> The pipeline uses the 10-second setting for practical demonstration purposes. You can:
> - Adjust it in `cicd/pipeline.sh` line 51: `export TEST_SLEEP_TIME=10`
> - Remove the line entirely to use the full 60-second delay
> - Set it to any value: `export TEST_SLEEP_TIME=5` for even faster demos

You should see output like:

```bash
🔁 Starting iteration 1

Mutated function in: custom_op_47.py

[master abc123d] next iteration 1
 1 file changed, 1 insertion(+), 1 deletion(-)

Smart Tests recorded build abc123d to workspace your-org/your-workspace...

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


> [!TIP]
> The first iteration may take slightly longer as Smart Tests processes your repository history.
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


#### Subset Selection
```
| Subset    |           21 |                    20.39 |                      21.00 |
```
Smart Tests selected 21 tests (20% of 103 total). You can inspect the subset:

```bash
cat cicd/temp/subset.txt
```


#### Parallel Execution
The tests ran in parallel (`pytest -n auto`), significantly reducing execution time from 21 minutes to ~2-3 minutes on a multi-core machine.

#### Going Live

The pipeline runs in **observation mode** (`--observation` flag on
`smart-tests record session`). In this mode, Smart Tests tracks what
the subset *would have* selected but still runs all tests — letting you
evaluate prediction quality without risk.

When you're confident in the predictions (the official onboarding guide
recommends 1–2 weeks of data), remove the flag:

```diff
- smart-tests record session --build $NAME --observation --test-suite ...
+ smart-tests record session --build $NAME --test-suite ...
```

Start with a conservative target (e.g. `--target 80%` or `--confidence 95%`)
and adjust based on observed results.

> **Always report results, even on failure.** Smart Tests needs to see both
> passing and failing test runs to make accurate predictions.
>
> | CI System | Pattern |
> |-----------|---------|
> | GitHub Actions | `if: always()` on the record tests step |
> | Jenkins | `post { always { } }` block |
> | CloudBees Workflows | `if: always()` |
> | Shell scripts | Capture exit code: `pytest ... || TEST_EXIT=$?` then report, then `exit ${TEST_EXIT:-0}` |

### Step 7: Run Multiple Iterations

Now let's run **5 iterations** to see Smart Tests learn from the accumulated data:

```bash
./cicd/pipeline.sh 5
```

This will take approximately 10-15 minutes total (depending on your CPU cores).


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

2. **Varying subset sizes** (Smart Tests adjusts based on predicted risk)
   ```
   Iteration 1: 21 tests selected
   Iteration 2: 19 tests selected (no mutation = fewer risky tests)
   Iteration 3: 24 tests selected (multiple files changed)
   ```

3. **Test failures** when mutations break functionality
   ```
   ====================== 2 passed, 1 failed in 125.34s ======================
   ```


### Step 8: Analyze Results in Smart Tests

After running multiple iterations, let's analyze the results in the Smart Tests web interface.

#### Navigate to Your Workspace

1. Visit [cloudbees.io](https://cloudbees.io) and navigate to Smart Tests
2. Select your organization and workspace
3. Click on **Test Sessions** in the sidebar


#### View Test Sessions

You should see a list of test sessions corresponding to your pipeline runs:


Each session shows:
- **Build name** (git commit hash)
- **Test suite** (`random_pytest`)
- **Subset size** (e.g., 21 of 103 tests)
- **Pass/Fail status**
- **Execution time**

#### Inspect a Specific Session

Click on one of the sessions to see detailed information:

  - Subset composition
  - Which tests passed/failed
  - Time savings metrics
  - Subset accuracy

**Key metrics to observe:**

| Metric | Typical Value |
|--------|---------------|
| **Subset Size** | ~20-21 tests (20% target) |
| **Time Savings** | ~80% reduction |
| **Tests Run** | 21 / 103 |
| **Execution Time** | ~2-3 min vs. ~103 min full suite |


#### View Subset Observation Report

Since the pipeline uses `--observation` mode, you'll see a subset observation report:

  - Subset quality metrics
  - How many tests would have been skipped
  - Whether any failures were in the remainder

This helps you evaluate subset quality before fully enabling PTS.

#### Compare Subsets Across Iterations

To see how subset selection evolved, you can compare individual subsets:

```bash
# Get subset IDs from two different iterations
smart-tests compare subsets --subset-id-before <SUBSET_ID_1> --subset-id-after <SUBSET_ID_2>
```

This shows which tests were promoted (↑) or demoted (↓) in priority, helping you understand how Smart Tests adapts to code changes.

#### Automated Learning Progress Analysis

The project includes a convenience script to automatically compare all consecutive subsets from your pipeline runs:

```bash
./cicd/check_learning_progress.sh
```

**What it does:**
- Reads all subset IDs from `cicd/subset_history.txt` (automatically populated by the pipeline)
- Compares each consecutive pair of subsets (1→2, 2→3, 3→4, etc.)
- Shows detailed ranking changes for all 102 tests across all comparisons
- Displays which code files affected each ranking change

**Example output:**

```
🔍 Smart Tests Learning Progress Analysis
===========================================
Total subsets in history: 12

📊 Comparison 1: Subset 1960631 → 1960637
-------------------------------------------
PTS subset change summary:
────────────────────────────────
-> 102 tests analyzed | 52 ↑ promoted | 48 ↓ demoted
-> Code files affected: src/calculator/custom_op_55.py
────────────────────────────────

Δ Rank      Subset Rank  Test Name                                           Reason
--------  -------------  --------------------------------------------------  ------------
↑16                   1  test_floor_divide                                   Changed file: ...
↑32                   2  test_custom_operations[custom_op_66-441]          Changed file: ...
...
```

**When to use it:**
- After running multiple pipeline iterations to see how predictions evolved
- To validate that Smart Tests correctly identifies changed files
- To demonstrate ML learning progression in demos
- To troubleshoot unexpected subset selections

**Behind the scenes:**
The pipeline automatically captures each subset ID and appends it to `cicd/subset_history.txt`. The learning progress script then uses the Smart Tests CLI to compare all consecutive pairs, showing you the complete learning journey.

---

## CI/CD Integration

### Step 9: Deploy to CloudBees

This project includes a pre-configured CloudBees workflow for automated CI/CD testing.

#### Configure CloudBees Secret

Before running the workflow, configure your Smart Tests API token as a secret:

1. Navigate to your CloudBees organization
2. Go to **Settings > Secrets**
3. Click **New Secret**
4. Create a secret with:
   - **Name**: `SMART_TESTS_KEY`
   - **Value**: Your Smart Tests API token
      (found in your workspace at **Settings > API Tokens**)


#### Review the Workflow Configuration

The workflow is located at `.cloudbees/workflows/pipeline.yaml`. Let's review the key sections:

```yaml
name: Random Test Pipeline with Smart Tests

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
          fetch-depth: 0  # Full git history for Smart Tests

      - name: Run pipeline iterations
        uses: docker://python:3.11-slim
        env:
          SMART_TESTS_TOKEN: ${{ secrets.SMART_TESTS_KEY }}
          SMART_TESTS_ORGANIZATION: ${{ vars.SMART_TESTS_ORG || '' }}
          SMART_TESTS_WORKSPACE: ${{ vars.SMART_TESTS_WS || '' }}
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
- ✅ Uses Python 3.11 container with git pre-installed
- ✅ Fetches full repository history for accurate predictions
- ✅ Installs dependencies from `requirements.txt`
- ✅ Configures git for commits during pipeline execution
- ✅ Runs `cicd/pipeline.sh` with configurable iteration count
- ✅ Archives JUnit XML test results

> **Why `fetch-depth: 0`?** Smart Tests needs full Git history to analyze code
> changes across commits. CI systems default to shallow clones (depth 1), which
> limits Smart Tests to only the latest commit. In Jenkins, ensure your SCM
> checkout is not configured for shallow clones. See
> [Dealing with shallow clones](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/sending-data-to-smart-tests/recording-builds/dealing-with-shallow-clones).

#### Push to Repository

Commit your local changes and push to trigger the workflow:

```bash
git add .
git commit -m "Configure Smart Tests demo"
git push origin main
```

#### Trigger the Workflow Manually

1. Navigate to **CloudBees Platform > Workflows**
2. Find **Random Test Pipeline with Smart Tests**
3. Click **Run Workflow**
4. In the dialog, set **iterations** (default: 5)
5. Click **Run**


### Step 10: Monitor Pipeline Execution

Once the workflow starts, monitor its progress in real-time.

#### View Running Workflow

Navigate to the workflow run page to see the execution status:


The workflow progresses through these stages:

1. ✅ **Check out** - Repository cloned with full history
2. 🔄 **Run pipeline iterations** - Executing `cicd/pipeline.sh`
   - Installing Python dependencies
   - Configuring git
   - Running iterations


#### View Pipeline Logs

Click on the **Run pipeline iterations** step to see detailed logs:

```bash
========================================
Running Smart Tests Pipeline
Iterations: 5
========================================

Installing Python and dependencies...
Successfully installed pytest-7.4.0 pytest-xdist-3.5.0 smart-tests-cli-2.0

🔁 Starting iteration 1
Mutated function in: custom_op_23.py
[master 1a2b3c4] next iteration 1
...
✅ Completed iteration 1

🔁 Starting iteration 2
...
```


#### Monitor Test Results

As tests complete, results are automatically archived. After the workflow finishes, you can:

1. **Download test results** from the workflow artifacts
2. **View results in Smart Tests** (links appear in logs)


#### View in Smart Tests Dashboard

The pipeline automatically reports all results to Smart Tests. Navigate to your workspace to see:

- All 5 test sessions listed
- Build information for each iteration
- Subset performance metrics
- Pass/fail trends


### Jenkins Integration

Smart Tests integrates with Jenkins in two ways:

**Option A: Jenkins Plugin (Recommended)**

Install the [Smart Tests Jenkins plugin](https://docs.cloudbees.com/docs/cloudbees-smart-tests/)
to automatically forward test results to Smart Tests via Jenkins' `junit` step.
No CLI commands needed in your Jenkinsfile — the plugin intercepts results
Jenkins is already collecting.

After installing the `.hpi` file, configure the API token in
**Manage Jenkins → System Configuration**.

**Option B: CLI Commands in Jenkinsfile**

```groovy
pipeline {
    agent any
    environment {
        SMART_TESTS_TOKEN = credentials('smart-tests-token')
    }
    stages {
        stage('Setup') {
            steps {
                sh 'pip install smart-tests-cli~=2.0'
                sh 'smart-tests verify'
            }
        }
        stage('Record Build') {
            steps {
                sh "smart-tests record build --build ${env.BUILD_NUMBER}"
            }
        }
        stage('Subset & Test') {
            steps {
                sh '''
                    smart-tests record session --build ${BUILD_NUMBER} \
                        --test-suite my-suite > session.txt
                    smart-tests subset pytest --session @session.txt \
                        --target 20% test/test_list.txt > subset.txt
                    pytest -n auto --junit-xml=test-results/results.xml @subset.txt
                '''
            }
            post {
                always {
                    sh 'smart-tests record tests pytest --session @session.txt test-results/'
                    junit 'test-results/*.xml'
                }
            }
        }
    }
}
```

**Important:** Use `post { always { } }` so test results are reported to
Smart Tests even when tests fail. Without this, failures never reach
Smart Tests and predictions cannot improve.

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


This simulates the types of small, localized changes developers make daily. Smart Tests learns which tests are sensitive to changes in specific files.

### How Smart Tests Selects Tests

Smart Tests uses large language models (LLMs) to understand your code changes
and automatically identify the most relevant tests to run. By analyzing both
source code and test files, Smart Tests builds a deep understanding of how your
code is structured and how different components relate to one another.

Using commit information, it calculates the similarity between changed files
and test files to determine which tests are most likely impacted — producing
an optimized test execution plan where critical tests are prioritized and
redundant ones are safely skipped.

**The result:** A prioritized, ranked list of tests where the most relevant
tests appear first.


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

  - Full Suite Sequential: 103 min
  - Full Suite Parallel: 13 min
  - Subset Parallel: 3 min

### Improving Prediction Quality Over Time

Smart Tests predictions improve as it collects more data from your test runs:

**First few iterations:** Smart Tests analyzes code structure and test file
similarity. Predictions are useful immediately but become more precise with data.

**With accumulated history:** As Smart Tests sees which tests pass and fail
across different code changes, it refines its understanding of which tests
are sensitive to which parts of the codebase.

Recording both passing and failing test sessions contributes to prediction
quality. This is why the official onboarding guide recommends starting in
observation mode to accumulate data before going live.

### Defensive Runs (Production Best Practice)

When using PTS in production, always run the **full test suite** at some point
in your delivery pipeline — typically post-merge or as a nightly job. This
catches any issues the subset may have missed.

Record these full runs with `smart-tests record tests` so Smart Tests can
use the complete results to improve future predictions.

See [Use-cases for Predictive Test Selection](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/features/predictive-test-selection/use-cases-for-predictive-test-selection)
for recommended pipeline topologies.

### What to Look For in the Results

#### In the Terminal Output

✅ **Consistent subset sizes** around 20% (varies based on risk assessment)
✅ **Fast execution times** thanks to parallel testing
✅ **Most iterations pass** (mutations are small and localized)
✅ **Some failures** (expected when mutations break logic)

#### In the Smart Tests Dashboard

✅ **Time savings trending upward** as model improves
✅ **Subset accuracy** consistently high (90%+)
✅ **No critical failures missed** (low false negative rate)
✅ **Model training progress** visible in model inspection


---

## Advanced Usage

### Running a Custom Test Subset

You can manually interact with Smart Tests to generate custom subsets:

```bash
# 1. Record a build
smart-tests record build --name my-custom-build

# 2. Create test session
smart-tests record session --test-suite "random_pytest" --build my-custom-build > session.txt

# 3. Generate subset with different target (e.g., 30%)
mkdir -p cicd/temp
cat test/test_list.txt | smart-tests subset --build my-custom-build --target 30% pytest > cicd/temp/my-subset.txt

# 4. Run the subset
pytest -n auto @cicd/temp/my-subset.txt --junit-xml=cicd/temp/test-results/results.xml

# 5. Report results
smart-tests record tests --session $(cat session.txt) pytest cicd/temp/test-results/
```

### Adjusting the Target Percentage

Edit `cicd/pipeline.sh` line 40 to change the subset size:

```bash
# Change from 20% to 30%
cat test/test_list.txt | smart-tests subset --build $NAME --target 30% pytest > cicd/temp/subset.txt
```

### Running Tests Sequentially (for Debugging)

If you need to debug individual test failures, run without parallelization:

```bash
# Edit cicd/pipeline.sh line 30, remove -n auto
pytest --junit-xml=test-results/subset.xml @subset.txt
```

### Adjusting Test Sleep Time

Tests simulate expensive operations with configurable sleep time. The pipeline defaults to **10 seconds** for practical demos.

**Option 1: Modify the pipeline (recommended)**

Edit `cicd/pipeline.sh` line 51:

```bash
# Current: 10 seconds (fast demos)
export TEST_SLEEP_TIME=10

# For faster testing
export TEST_SLEEP_TIME=5

# For realistic simulation (60 seconds)
export TEST_SLEEP_TIME=60

# Or remove the line entirely to use default (60s)
```

**Option 2: Set environment variable before running**

```bash
TEST_SLEEP_TIME=5 ./cicd/pipeline.sh 3
```

**Option 3: Edit the test file directly**

Modify `test/test_calculator.py` line 24:

```python
# Change default from 60 to another value
TEST_SLEEP_TIME = int(os.getenv('TEST_SLEEP_TIME', '30'))
```

The environment variable approach (Options 1-2) is recommended as it doesn't require code changes.

### Analyzing Learning Progress

After running multiple iterations, analyze how Smart Tests predictions evolved:

```bash
./cicd/check_learning_progress.sh
```

This script:
- Reads all subset IDs from your pipeline runs (`cicd/subset_history.txt`)
- Compares consecutive subsets to show test ranking changes
- Displays which code files affected the changes
- Provides a complete view of the ML learning journey

Perfect for demos, troubleshooting, and validating that Smart Tests correctly identifies changed files. See [Step 8: Analyze Results](#step-8-analyze-results-in-smart-tests) for detailed output examples.

---

## Project Organization & Refactoring

This project has been carefully organized to follow best practices for Python projects and CI/CD workflows.

### Directory Structure Benefits

**Clean Separation of Concerns:**
- **`src/`** - Production source code only
- **`test/`** - All test-related files
- **`cicd/`** - CI/CD automation scripts and temporary files
- **`backup/`** - Clean state for resets

**Why `cicd/temp/` for Temporary Files:**

All temporary files generated during the pipeline are stored in `cicd/temp/`:
```
cicd/temp/
├── session.txt    # Current test session
├── subset.txt     # Selected 20% test subset
└── test-results/             # JUnit XML output
    └── subset.xml
```

**Benefits:**
1. **Organized** - All CI/CD files (scripts + temp) in one place
2. **Clean root** - No temporary files cluttering the workspace
3. **Logical grouping** - Temp files live with scripts that create them
4. **Git-friendly** - Single `.gitignore` entry: `cicd/temp/`
5. **Easy cleanup** - Just run `rm -rf cicd/temp/*`

### Pipeline Flow Improvements

The pipeline has been optimized for clarity and efficiency:

**Reset at the Beginning (Not the End):**
```bash
for iteration in 1..N:
  1. Reset to clean state (if iteration > 1)  ← Moved here!
  2. Clean cicd/temp/
  3. Mutate code
  4. Commit & test
  5. Report results
```

**Why this is better:**
- Each iteration starts with a known clean state
- More logical: prepare → execute → report
- Failed iterations don't leave dirty state for next run
- Easier to understand and debug

### Migration from Old Structure

**Before:**
```
calculator_project/          → src/calculator/
calculator_project_backup/   → backup/calculator/
test_calculator.py          → test/test_calculator.py
test_list.txt              → test/test_list.txt
pipeline.sh                → cicd/pipeline.sh
(root temp files)          → cicd/temp/
```

All code, documentation, and workflows have been updated to reflect this new structure.

---

## Troubleshooting

### Common Issues

#### Issue: `smart-tests: command not found`

**Solution:** Activate your virtual environment

```bash
source venv/bin/activate
```

Verify:
```bash
which smart-tests
# Should show: /path/to/random_tests/venv/bin/smart-tests
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
pytest -n auto --junit-xml=cicd/temp/test-results/subset.xml @cicd/temp/subset.txt
```

Verify pytest-xdist is installed:
```bash
pip list | grep pytest-xdist
```

---

#### Issue: No subset generated on first run

**Expected behavior.** The first run establishes a baseline. Smart Tests needs at least one test session with results before it can make predictions.

After the first iteration completes, subsequent iterations will use ML-based predictions.

---

#### Issue: `SMART_TESTS_TOKEN` not set error

**Solution:** Export your token

```bash
export SMART_TESTS_TOKEN="<your-token>"
# Or
source .env  # If you have a .env file
```

Verify:
```bash
echo $SMART_TESTS_TOKEN
# Should display your token
```

---

#### Issue: `smart-tests record tests` fails or shows unexpected results

**Solution:** Validate your JUnit XML reports before sending them:

```bash
python3 tools/validate_junit_xml.py cicd/temp/test-results/
```

See [tools/README.md](tools/README.md) for details on what the validator checks.
Common issues include missing `classname` attributes (required for PTS file mapping)
and missing `time` attributes (required for accurate subset duration estimates).

---

#### Issue: Workflow fails in CloudBees

**Solution:** Check the secret configuration

1. Verify `SMART_TESTS_KEY` secret exists in CloudBees
2. Ensure the secret value is your Smart Tests API token (not some other credential)
3. Check workflow logs for the exact error message

---

## Reference Materials

- [Smart Tests Documentation](https://docs.cloudbees.com/docs/cloudbees-smart-tests/)
- [CloudBees Smart Tests Documentation](https://docs.cloudbees.com/docs/cloudbees-smart-tests/latest/)
- [Predictive Test Selection Concepts](https://docs.cloudbees.com/docs/cloudbees-smart-tests/docs/concepts/predictive-test-selection)
- [pytest-xdist Documentation](https://pytest-xdist.readthedocs.io/)
- [CLAUDE.md](CLAUDE.md) - Developer guide for working with this codebase

---

## Summary

Congratulations! You've successfully completed the Smart Tests Predictive Test Selection demo. 🎉

**What you accomplished:**

✅ Set up a complete Smart Tests PTS environment
✅ Understood a clean, well-organized project structure following Python best practices
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
- 📁 **Clean project structure separates source, tests, and CI/CD concerns**

### Next Steps

Ready to apply this to your own projects?

1. **Explore your own repository:** Clone a real project and try Smart Tests on it
2. **Experiment with different targets:** Test 10%, 20%, 30% subsets to find your optimal balance
3. **Integrate with your CI/CD:** Adapt the CloudBees workflow to your existing pipelines
4. **Review the documentation:** Check out [Smart Tests docs](https://docs.cloudbees.com/docs/cloudbees-smart-tests/) for advanced features

### Live Walkthrough Tips

If you're using this demo for a presentation or workshop:

1. Run `./cicd/pipeline.sh 5` and narrate what's happening
2. Open `cicd/temp/subset.txt` and show it's ~20% of tests
3. Point out which files mutated and which tests were selected
4. Show a test failure and explain how Smart Tests learns from it
5. Compare iteration 1 vs iteration 5 subset quality

---

**Questions or Issues?**

- Open an issue in this repository
- Contact your workshop instructor
- Visit [Smart Tests Community](https://cloudbees.com/community)

---

*This demo is maintained as part of Smart Tests's educational resources. For the latest updates, visit the [Smart Tests documentation](https://docs.cloudbees.com/docs/cloudbees-smart-tests/).*
