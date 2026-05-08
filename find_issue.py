with open('scaffold_ethio_council.py', encoding='utf-8') as f:
    lines = f.readlines()

# Check each dictionary entry
i = 1815  # Start from line 1816 (0-indexed)
while i < min(1895, len(lines)):
    line = lines[i]
    if '"""' in line and ':' in line:
        # This is a dictionary entry start
        start = i
        print(f"\nDict entry at line {i+1}: {line.strip()[:70]}")
        # Find where it ends
        i += 1
        while i < len(lines):
            if lines[i].strip() in ['"""', '""",']:
                print(f"  Ends at line {i+1}: {lines[i].strip()}")
                break
            i += 1
        if i >= len(lines):
            print(f"  ERROR: Never found closing triple quotes!")
            break
    i += 1
