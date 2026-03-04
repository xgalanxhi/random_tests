#!/bin/bash

echo "=== Verification: Git Changes for Subset 1960714 → 1960719 ==="
echo ""
echo "Subset 1960714 corresponds to build: b5370ab"
echo "Subset 1960719 corresponds to build: 252c374"
echo ""
echo "Git diff between these commits:"
echo "--------------------------------"
git diff --stat b5370ab..252c374
echo ""
echo "Full changes:"
echo "-------------"
git diff b5370ab..252c374
echo ""
echo "=== Smart Tests Claims ==="
echo "Code files affected: src/calculator/custom_op_18.py"
echo ""
echo "=== Actual Git Reality ==="
echo "Files changed: src/calculator/custom_op_30.py, src/calculator/custom_op_39.py"
