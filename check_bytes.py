import ast

# Read file with UTF-8
with open('scaffold_ethio_council.py', encoding='utf-8') as f:
    lines = f.readlines()

# Check lines around 1816-1820
for i in range(1815, 1825):
    line = lines[i]
    print(f"{i+1}: {repr(line)}")

print("\n\n--- Checking for quote characters ---")
# Check for non-standard quotes
for i in range(1815, 1850):
    line = lines[i]
    for j, char in enumerate(line):
        if ord(char) > 127:  # Non-ASCII
            print(f"Line {i+1}, pos {j}: {repr(char)} (ord={ord(char)})")
