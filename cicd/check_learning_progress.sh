#!/bin/bash

# Script to check Smart Tests learning progress by comparing consecutive subsets

SUBSET_HISTORY="cicd/subset_history.txt"

# Check if subset history file exists
if [ ! -f "$SUBSET_HISTORY" ]; then
  echo "❌ Error: $SUBSET_HISTORY not found"
  echo "Run the pipeline first to generate subset history"
  exit 1
fi

# Read all subset IDs into an array (compatible with older bash)
SUBSETS=()
while IFS= read -r line; do
  # Skip empty lines
  if [ -n "$line" ]; then
    SUBSETS+=("$line")
  fi
done < "$SUBSET_HISTORY"

# Check if we have at least 2 subsets to compare
if [ ${#SUBSETS[@]} -lt 2 ]; then
  echo "❌ Error: Need at least 2 subsets to compare"
  echo "Found ${#SUBSETS[@]} subset(s) in history"
  exit 1
fi

echo "🔍 Smart Tests Learning Progress Analysis"
echo "==========================================="
echo "Total subsets in history: ${#SUBSETS[@]}"
echo ""

# Compare consecutive subsets
for ((i = 0; i < ${#SUBSETS[@]} - 1; i++)); do
  SUBSET_BEFORE=${SUBSETS[$i]}
  SUBSET_AFTER=${SUBSETS[$((i + 1))]}

  echo "📊 Comparison $((i + 1)): Subset $SUBSET_BEFORE → $SUBSET_AFTER"
  echo "-------------------------------------------"

  smart-tests compare subsets --subset-id-before "$SUBSET_BEFORE" --subset-id-after "$SUBSET_AFTER" | tee

  echo ""
  echo ""
done

echo "✅ Learning progress analysis complete!"
