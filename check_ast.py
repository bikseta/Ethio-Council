import ast
import traceback

try:
    with open('scaffold_ethio_council.py', encoding='utf-8') as f:
        code = f.read()
    ast.parse(code)
except SyntaxError as e:
    print(f"SyntaxError on line {e.lineno}, column {e.offset}: {e.msg}")
    print(f"Text: {repr(e.text)}")
    # Show context
    lines = code.split('\n')
    for i in range(max(0, e.lineno - 3), min(len(lines), e.lineno + 2)):
        prefix = ">>> " if i == e.lineno - 1 else "    "
        print(f"{prefix}{i+1}: {lines[i][:120]}")
