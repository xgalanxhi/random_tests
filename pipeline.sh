#!/bin/bash

# Check if user provided the iteration count
if [ -z "$1" ]; then
  echo "Usage: $0 <number-of-iterations>"
  exit 1
fi

ITERATIONS=$1

for ((i = 1; i <= ITERATIONS; i++)); do
  echo "🔁 Starting iteration $i"

  # Mutate randomly
  python calculator_project/mutate_random_function.py

  # Git commit
  git add calculator_project test_calculator.py
  git commit -m "next iteration $i"

  # Get commit hash
  NAME=$(git rev-parse --short HEAD)

  # Launchable tracking
  launchable record build --name $NAME
  #launchable record session --test-suite "pred" --build $NAME > launchable-session.txt
   launchable record session --test-suite "random_pytest" --observation --build $NAME > launchable-session.txt
  # Subset and test
  cat test_list.txt | launchable subset --build $NAME --target 20% pytest > launchable-subset.txt
  pytest -n auto --junit_family=legacy --junit-xml=test-results/subset.xml @launchable-subset.txt

  # Report to Launchable
  launchable record tests --session $(cat launchable-session.txt) --allow-test-before-build --build $NAME pytest ./test-results/

  # Reset working directory
  rm -rf calculator_project
  cp -r calculator_project_backup/ calculator_project
#  rm -rf test-results

  echo "✅ Completed iteration $i"
  echo
done
