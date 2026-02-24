# Launchable Predictive Test Selection Demo (Python)

This repository is a **hands-on demo** for Launchable predictive test selection.

It intentionally simulates a project with **many slow tests** and **small, localized code changes** so it’s easy to see:

- why running *all* tests every build is expensive, and
- how Launchable can learn correlations between code changes and the tests that fail.

## What happens in the demo

Each pipeline iteration:

1. Randomly mutates **0–3** calculator operation modules under `calculator_project/`.
   - (The occasional “no mutation” iteration is intentional: it provides baseline examples.)
2. Commits the change (so the commit hash can be used as the Launchable **build name**).
3. Records the build + creates a Launchable test session.
4. Asks Launchable for a **subset** (target: 20%) of tests to run.
5. Runs only that subset (in parallel) and records the results back to Launchable.
6. Resets the working directory back to a clean state from `calculator_project_backup/`.

Over multiple iterations, Launchable accumulates signal like:

- “This file changed” → “These tests tend to fail”

In real projects the correlations can be more complex; this repo is designed to make the relationship easy to grasp.

## Repo layout

- `calculator_project/` — calculator operations (about ~100 single-function modules)
- `calculator_project_backup/` — clean reset copy used between iterations
- `test_calculator.py` — test suite (intentionally slow; each test sleeps)
- `test_list.txt` — canonical list of test identifiers used by Launchable
- `pipeline.sh` — the end-to-end demo pipeline
- `launchable-subset.txt` — Launchable-selected subset output (overwritten each run)
- `launchable-session.txt` — Launchable session ID (overwritten each run)
- `.cloudbees/workflows/pipeline.yaml` — CI workflow that runs `pipeline.sh`

## Prerequisites

- Python 3.9+ (any recent Python 3 should work)
- `git`
- Launchable CLI (installed via `requirements.txt`)
- A Launchable token available as `LAUNCHABLE_TOKEN`

> Note: this repo includes a `.env` file that is gitignored. If you use it, keep it local and never commit real tokens.

## Setup (local)

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Configure Launchable token

Set your token in the environment:

```bash
export LAUNCHABLE_TOKEN="<your-token>"
```

Or, if you maintain a local `.env` file that contains `export LAUNCHABLE_TOKEN=...`:

```bash
source .env
```

Verify the Launchable CLI + token are set up correctly:

```bash
launchable verify
```

## Run the demo pipeline

Run N iterations (more iterations = more training examples):

```bash
./pipeline.sh 20
```

### What to look at while it runs

- Mutated files are printed by `calculator_project/mutate_random_function.py`.
- The subset Launchable chose is written to `launchable-subset.txt`.
- The Launchable session ID is written to `launchable-session.txt`.

## Running tests yourself

Run all tests:

```bash
pytest test_calculator.py
```

Run all tests in parallel:

```bash
pytest -n auto test_calculator.py
```

Run a single test:

```bash
pytest test_calculator.py::test_add
```

Run the current Launchable-selected subset:

```bash
pytest -n auto @launchable-subset.txt
```

## How Launchable is used here

The pipeline uses the Launchable CLI roughly like this:

- Record a build:
  - `launchable record build --name <git-sha>`
- Record a test session:
  - `launchable record session --test-suite "random_pytest" --observation --build <git-sha>`
- Ask for a test subset:
  - `cat test_list.txt | launchable subset --build <git-sha> --target 20% pytest`
- Record test results:
  - `launchable record tests --session <session-id> --allow-test-before-build --build <git-sha> pytest ./test-results/`

### Inspect model training status

To see when the Launchable model was last trained (and other model metadata), run:

```bash
launchable inspect model
```

## CloudBees workflow

If you’re running this via CloudBees, see `.cloudbees/workflows/pipeline.yaml`.

It uses the `cloudbees/launchable` container image and expects a secret named:

- `SMART_TESTS_KEY` → exported as `LAUNCHABLE_TOKEN`

You can trigger it with a custom iteration count via `workflow_dispatch`.

## Notes / gotchas

- The pipeline makes git commits during execution. Run it in a disposable clone or a demo branch.
- Each test sleeps intentionally to make the “subset vs full run” time difference obvious.
- `test_list.txt` is the source of truth for Launchable’s test identifiers.

---

If you want this demo to feel even more interactive, a good live walkthrough is:

1. Run `./pipeline.sh 5`
2. Open `launchable-subset.txt` and point out it’s ~20% of the tests
3. Highlight which files mutated in each iteration and which tests failed
4. Repeat with more iterations and show subset quality improving over time
