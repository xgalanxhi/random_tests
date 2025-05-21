import os
import random

base_dir = os.path.dirname(__file__)

# List all function files except helpers
function_files = [f for f in os.listdir(base_dir) if f.endswith(".py") and f not in {"main.py", "mutate_random_function.py"}]

# Pick one randomly
file_to_modify = random.choice(function_files)
file_path = os.path.join(base_dir, file_to_modify)

# Read and mutate the function
with open(file_path, "r") as f:
    lines = f.readlines()

mutated_lines = []
mutated = False
for line in lines:
    if not mutated and line.strip().startswith("return"):
        # Mutate the return line
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

print(f"Mutated function in: {file_to_modify}")
