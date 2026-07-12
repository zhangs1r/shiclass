import re

# The pattern in scan_katex_v2.py for escaped dollar:
# r'(?<!\$)\\$(?!\$)'  
#
# Let's decode this:
pattern_old = r'(?<!\$)\\$(?!\$)'
print(f"Old pattern: {repr(pattern_old)}")
print(f"Old pattern length: {len(pattern_old)}")
for i, c in enumerate(pattern_old):
    print(f"  [{i}] {repr(c)} (U+{ord(c):04X})")

print()

# What does this regex actually match?
test_str = r"hello \$world $formula$ $$display$$"
print(f"Test string: {repr(test_str)}")
for m in re.finditer(pattern_old, test_str):
    print(f"  Match: {repr(m.group())} at pos {m.start()}")
    print(f"  Context: ...{test_str[max(0,m.start()-3):m.end()+3]}...")

print()

# Now let's write the CORRECT pattern for matching \$ (backslash + dollar)
# In regex: \\ matches \, \$ matches $
# So the pattern to match \$ is: \\\$
# In Python raw string: r'\\\$'
correct = r'\\\$'
print(f"Correct pattern: {repr(correct)}")
print(f"Correct pattern length: {len(correct)}")
for i, c in enumerate(correct):
    print(f"  [{i}] {repr(c)} (U+{ord(c):04X})")

for m in re.finditer(correct, test_str):
    print(f"  Match: {repr(m.group())} at pos {m.start()}")
    print(f"  Context: ...{test_str[max(0,m.start()-3):m.end()+3]}...")

print()

# With negative lookarounds to avoid $$
full_correct = r'(?<!\$)\\\$(?!\$)'
print(f"Full correct pattern: {repr(full_correct)}")
for m in re.finditer(full_correct, test_str):
    print(f"  Match: {repr(m.group())} at pos {m.start()}")
    print(f"  Context: ...{test_str[max(0,m.start()-3):m.end()+3]}...")
