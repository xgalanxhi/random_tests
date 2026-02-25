#!/bin/bash

# Check if user provided the iteration count
if [ -z "$1" ]; then
  echo "Usage: $0 <number-of-iterations>"
  exit 1
fi

ITERATIONS=$1

# Create temp directory for temporary files
mkdir -p cicd/temp

for ((i = 1; i <= ITERATIONS; i++)); do
  echo "🔁 Starting iteration $i"

  # Reset working directory at the start
  if [ $i -gt 1 ]; then
    echo "Resetting to clean state..."
    rm -rf src/calculator
    cp -r backup/calculator/ src/calculator
  fi

  # Clean temp directory
  rm -rf cicd/temp/*

  # Mutate randomly
  python cicd/mutate_random_function.py

  # Git commit
  git add src/calculator test/test_calculator.py
  git commit -m "next iteration $i"

  # Get commit hash
  NAME=$(git rev-parse --short HEAD)

  # Smart Tests tracking
  smart-tests record build --name $NAME
  smart-tests record session --test-suite "random_pytest" --observation --build $NAME > cicd/temp/session.txt

  # Subset and test
  cat test/test_list.txt | smart-tests subset --build $NAME --target 20% pytest > cicd/temp/subset.txt
  pytest -n 50 -o junit_family=legacy --junit-xml=cicd/temp/test-results/subset.xml @cicd/temp/subset.txt

  # Report to Smart Tests
  smart-tests record tests --session $(cat cicd/temp/session.txt) --allow-test-before-build --build $NAME pytest cicd/temp/test-results/

  echo "✅ Completed iteration $i"
  echo
done
