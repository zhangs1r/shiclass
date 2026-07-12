#!/usr/bin/env python3
"""
Properly fix trailing backslashes inside $$...$$ aligned blocks.
After the first pass removed $...$ wrapping, the trailing \\\\\\\\... still has
14+ backslashes where there should be just 2 (one LaTeX line break).
"""
import glob, re, os

lessons_dir = '/home/zjq/shiclass/lessons/'

def count_trailing_backslashes(s):
    """Count trailing backslash characters in a string."""
    count = 0
    for c in reversed(s):
        if c == '\\':
            count += 1
        else:
            break
    return count

def fix_trailing_bs(content):
    """Inside $$...$$ blocks with aligned environments, normalize trailing backslashes."""
    
    # Pattern to match $$...$$ blocks
    pat = re.compile(r'(\$\$)(.*?)(\$\$)', re.DOTALL)
    
    def fix_block(m):
        opener = m.group(1)
        inner = m.group(2)
        closer = m.group(3)
        
        lines = inner.split('\n')
        in_aligned = False
        changed = False
        new_lines = []
        
        for line in lines:
            stripped = line.strip()
            stripped_rstrip = line.rstrip('\n').rstrip('\r')
            
            # Detect start of aligned environment
            # In the file: '\begin{aligned}' (single backslash)
            if re.match(r'\\begin\{(aligned|matrix|pmatrix|bmatrix|vmatrix|gathered|array|split|cases)\}', stripped):
                in_aligned = True
                new_lines.append(line)
                continue
            
            # Detect end
            if re.match(r'\\end\{(aligned|matrix|pmatrix|bmatrix|vmatrix|gathered|array|split|cases)\}', stripped):
                in_aligned = False
                new_lines.append(line)
                continue
            
            if not in_aligned:
                new_lines.append(line)
                continue
            
            # Inside aligned: check for trailing backslashes
            trailing = count_trailing_backslashes(stripped_rstrip)
            if trailing >= 4:  # 4+ trailing backslashes is excessive
                # Calculate the content before the trailing backslashes
                prefix = stripped_rstrip[:-trailing]
                # Restore leading whitespace
                leading_ws = line[:len(line) - len(line.lstrip())]
                # Replace with just 2 backslashes (one LaTeX line break)
                new_lines.append(leading_ws + prefix + '\\\\')
                changed = True
                print(f"  Fixed {trailing} trailing \\ → just 2: {stripped[:40]}...")
            else:
                new_lines.append(line)
        
        if changed:
            return opener + '\n'.join(new_lines) + closer
        return m.group(0)
    
    return pat.sub(fix_block, content)


def main():
    files = sorted(glob.glob(os.path.join(lessons_dir, '*.html')))
    for fpath in files:
        fname = os.path.basename(fpath)
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        updated = fix_trailing_bs(content)
        
        if updated != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(updated)
            print(f"✅ FIXED: {fname}")
        else:
            print(f"⏭️  SKIP:  {fname} (no changes)")

if __name__ == '__main__':
    main()
