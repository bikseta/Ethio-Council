with open('scaffold_ethio_council.py', encoding='utf-8') as f:
    content = f.read()

# Count triple quotes
triple_quote_count = content.count('"""')
print(f"Total triple quotes: {triple_quote_count}")
print(f"Should be even: {triple_quote_count % 2 == 0}")

# Find all triple quotes around line 1880-1890
import re
for match in re.finditer(r'"""', content):
    line_num = content[:match.start()].count('\n') + 1
    if line_num >= 1878 and line_num <= 1892:
        context_start = max(0, match.start() - 30)
        context_end = min(len(content), match.end() + 30)
        context = content[context_start:context_end].replace('\n', '\\n')
        print(f"Line {line_num}: {repr(context)}")
