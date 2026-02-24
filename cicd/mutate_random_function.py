import os
import random
from pathlib import Path

# Get the calculator source directory (src/calculator)
script_dir = Path(__file__).parent
base_dir = script_dir.parent / "src" / "calculator"

# List all function files except helpers
function_files = [f for f in os.listdir(base_dir)
                  if f.endswith(".py") and f not in {"main.py", "mutate_random_function.py", "restore_original_functions.py", "__init__.py"}]

# Decide how many files to mutate
roll = random.random()

if roll < 0.5:
    print("No mutation this time.")
    exit(0)
elif roll < 0.8:
    num_to_mutate = 1
elif roll < 0.9:
    num_to_mutate = 2
else:
    num_to_mutate = 3

files_to_modify = random.sample(function_files, min(num_to_mutate, len(function_files)))

def mutate_file(file_path):
    with open(file_path, "r") as f:
        lines = f.readlines()

    mutated_lines = []
    mutated = False
    for line in lines:
        if not mutated and line.strip().startswith("return"):
            if "+" in line:
                line = line.replace("+", "-")
            elif "-" in line:
                line = line.replace("-", "+")
            else:
                line = line.replace("return", "return 42 +")
            mutated = True
        mutated_lines.append(line)

    with open(file_path, "w") as f:
        f.writelines(mutated_lines)

# Apply mutations
for file_name in files_to_modify:
    file_path = os.path.join(base_dir, file_name)
    mutate_file(file_path)
    print(f"Mutated function in: {file_name}")
