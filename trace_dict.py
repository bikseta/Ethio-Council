import re

with open('scaffold_ethio_council.py', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Track dictionary entries
current_dict_entry_start = None
in_string = False
string_start_line = None

for i, line in enumerate(lines, 1):
    stripped = line.strip()
    
    # Check for dictionary entry start: key: """
    if not in_string and ':' in line and '"""' in line:
        # This starts a dictionary entry
        print(f"Dict entry starts at line {i}: {line[:80]}")
        in_string = True
        string_start_line = i
        # Check if it also ends on same line
        if line.count('"""') >= 2:
            print(f"  ... and ends on same line")
            in_string = False
    elif in_string and '"""' in line and i != string_start_line:
        # This could end the string
        print(f"String might end at line {i}: {line[:80]}")
        if line.strip() == '""",' :
            print(f"  ✓ This closes the string with a comma")
            in_string = False
        elif line.strip() == '"""':
            print(f"  ⚠ This closes the string but missing comma?")
        else:
            print(f"  ⚠ Unknown format")
    
    if i >= 1815 and i <= 1900:
        if i == string_start_line:
            print(f">>> {i}: {line[:80]}")
        elif in_string:
            print(f"... {i}: {line[:80]}")
