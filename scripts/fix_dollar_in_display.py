#!/usr/bin/env python3
"""
Fix KaTeX formula issues in shiclass HTML files.

Problem: Inside $$...$$ display math blocks, each line in \begin{aligned}
environments is wrapped with $...$ delimiters, and line endings have
excessive backslashes followed by $.

Pattern seen in files:
    $$
    \begin{aligned}
    $\text{①} ... \\\\\\$     ← leading $, trailing 14x\ + $
    $\text{②} ... \\\\\\$     ← same
    ...
    $\text{⑤} ... $           ← last line: leading $, trailing $
    \end{aligned}
    $$

Fix:
1. Remove leading '$' (and whitespace after it) that starts content lines inside $$
2. Replace trailing '\\...$' (any even number of \ + $) with just '\\'
3. Remove trailing '$' from the last line (no line break needed)
4. For single-line $$ blocks: remove wrapping $...$
"""

import re
import os
import glob

def fix_display_math_blocks(content):
    """Fix all $$...$$ blocks in the content."""
    
    # Regex to find $$...$$ blocks
    # Match $$, then everything until the next $$
    pattern = re.compile(r'(\$\$)(.*?)\1', re.DOTALL)
    
    def fix_block(match):
        full = match.group(0)
        opener = match.group(1)  # $$
        inner = match.group(2)   # content between $$ and $$
        
        # Don't modify if nothing to fix (no $ inside)
        if '$' not in inner:
            return full
        
        # Split inner into lines
        lines = inner.split('\n')
        fixed_lines = []
        in_aligned = False
        has_fix = False
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Detect aligned/matrix/gathered environments
            if re.match(r'\\\\begin\{(aligned|matrix|pmatrix|bmatrix|vmatrix|gathered|array|split|cases)\}', stripped):
                in_aligned = True
            
            if re.match(r'\\\\end\{(aligned|matrix|pmatrix|bmatrix|vmatrix|gathered|array|split|cases)\}', stripped):
                in_aligned = False
                fixed_lines.append(line)
                continue
            
            if not in_aligned:
                # Not in aligned - check if single $...$ wrapping
                stripped_line = stripped
                if stripped_line.startswith('$') and stripped_line.endswith('$') and stripped_line.count('$') == 2:
                    # Content between the $...$
                    inner_content = stripped_line[1:-1]
                    # But only fix if there's no other $ inside (it's a simple wrapper)
                    if '$' not in inner_content:
                        # Indent preserved replacement
                        indent = line[:len(line) - len(line.lstrip())]
                        fixed_lines.append(indent + inner_content)
                        has_fix = True
                        print(f"    [SINGLE-LINE] Removed $...$ wrapping: {stripped_line[:50]}...")
                        continue
                fixed_lines.append(line)
                continue
            
            # We're inside \begin{aligned}...\end{aligned}
            # Check for leading $
            leading_dollar = False
            line_text = line
            # Check if stripped starts with $
            if stripped.startswith('$'):
                leading_dollar = True
                # Find where the $ is in the original line
                stripped_after_dollar = stripped[1:]
                leading_ws = line[:len(line) - len(line.lstrip())]
                line_text = leading_ws + stripped_after_dollar
                has_fix = True
            
            # Check for trailing $ preceded by backslashes
            rtext = line_text.rstrip('\n').rstrip('\r')
            if rtext.endswith('$'):
                before_dollar = rtext[:-1]
                # Count trailing backslashes
                bs_count = 0
                for c in reversed(before_dollar):
                    if c == '\\':
                        bs_count += 1
                    else:
                        break
                
                if bs_count > 0 and bs_count % 2 == 0:
                    # Even number of trailing \ followed by $
                    # In KaTeX, \\ = one line break
                    # \...$ should be just \\ (one line break)
                    # bs_count backslashes = bs_count//2 LaTeX \\ commands
                    # We want exactly 2 backslashes (one \\) for a line break, but
                    # if this isn't the last line:
                    is_last_content_line = False
                    # Check if next line has \end{aligned}
                    if i + 1 < len(lines):
                        next_stripped = lines[i + 1].strip()
                        if re.match(r'\\\\end\{(aligned|matrix|pmatrix|bmatrix|vmatrix|gathered|array|split|cases)\}', next_stripped):
                            is_last_content_line = True
                    
                    if is_last_content_line:
                        # Last line: just remove trailing $, no line break
                        prefix = before_dollar[:-bs_count]
                        trailing_ws = line_text[len(rtext):]
                        line_text = prefix + trailing_ws
                        print(f"    [LAST-LINE] Removed trailing $ (was {bs_count} trailing \\ + $)")
                    else:
                        # Not last line: replace \\...$ with \\ (one line break)
                        prefix = before_dollar[:-bs_count]
                        trailing_ws = line_text[len(rtext):]
                        line_text = prefix + '\\\\' + trailing_ws
                        print(f"    [LINE-BREAK] Replaced {bs_count}\\ + $ with single \\\\")
                    has_fix = True
                    
                elif bs_count == 0:
                    # Trailing $ with no backslashes before it
                    # This is the closing $ of the $...$ inline math - remove it
                    prefix = before_dollar
                    trailing_ws = line_text[len(rtext):]
                    line_text = prefix + trailing_ws
                    print(f"    [TRAILING-DOLLAR] Removed trailing $ (no backslashes)")
                    has_fix = True
            
            if leading_dollar:
                print(f"    [LEADING-DOLLAR] Removed leading $")
            
            fixed_lines.append(line_text)
        
        if has_fix:
            result = opener + '\n'.join(fixed_lines) + opener
            return result
        return full
    
    result = pattern.sub(fix_block, content)
    return result


def main():
    lessons_dir = '/home/zjq/shiclass/lessons/'
    html_files = sorted(glob.glob(os.path.join(lessons_dir, '*.html')))
    
    total_fixed = 0
    for fpath in html_files:
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        content = fix_display_math_blocks(content)
        
        if content != original:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(content)
            total_fixed += 1
            print(f"✅ FIXED: {fname}")
        else:
            print(f"⏭️  SKIP:  {fname} (no changes)")
    
    print(f"\n{'='*50}")
    print(f"Total files modified: {total_fixed}/{len(html_files)}")


if __name__ == '__main__':
    main()
