#!/usr/bin/env python3
"""
KaTeX Formula Issue Scanner for shiclass project.
Scans all lessons/*.html files for LaTeX formula issues that could
cause KaTeX rendering failures.
"""
import re
import os
import sys
from collections import defaultdict

LESSONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lessons')

# Known LaTeX commands (used to detect \\command issues)
LATEX_COMMANDS = [
    # Greek letters
    'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'varepsilon', 'zeta', 'eta',
    'theta', 'vartheta', 'iota', 'kappa', 'lambda', 'mu', 'nu', 'xi', 'omicron',
    'pi', 'varpi', 'rho', 'varrho', 'sigma', 'varsigma', 'tau', 'upsilon',
    'phi', 'varphi', 'chi', 'psi', 'omega',
    # Capital Greek
    'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma', 'Phi', 'Psi', 'Omega',
    # Math functions & operators
    'mathbb', 'mathrm', 'mathbf', 'mathsf', 'mathit', 'mathtt', 'mathcal',
    'mathscr', 'mathfrak', 'text', 'textrm', 'textbf', 'textit',
    'sum', 'prod', 'coprod', 'int', 'iint', 'iiint', 'oint', 'oiint',
    'bigcup', 'bigcap', 'bigvee', 'bigwedge', 'bigoplus', 'bigotimes',
    'lim', 'limsup', 'liminf', 'sup', 'inf', 'min', 'max',
    'arg', 'argmin', 'argmax', 'det', 'dim', 'deg', 'exp', 'log', 'ln', 'lg',
    'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'arcsin', 'arccos', 'arctan',
    'sinh', 'cosh', 'tanh', 'coth',
    'gcd', 'lcm', 'mod', 'pmod', 'bmod',
    'operatorname', 'Pr', 'tr', 'rank', 'null', 'span',
    # Relations & arrows
    'equiv', 'approx', 'neq', 'ne', 'leq', 'geq', 'leqslant', 'geqslant',
    'll', 'gg', 'sim', 'simeq', 'cong', 'propto', 'asymp',
    'mapsto', 'to', 'rightarrow', 'Rightarrow', 'leftarrow', 'Leftarrow',
    'leftrightarrow', 'Leftrightarrow', 'longrightarrow', 'Longrightarrow',
    'longleftrightarrow', 'Longleftrightarrow', 'hookrightarrow', 'hookleftarrow',
    'mapsto', 'longmapsto', 'nearrow', 'searrow', 'nwarrow', 'swarrow',
    'uparrow', 'Uparrow', 'downarrow', 'Downarrow', 'updownarrow', 'Updownarrow',
    'leftarrow', 'rightarrow', 'Leftarrow', 'Rightarrow', 'leftharpoonup',
    'leftharpoondown', 'rightharpoonup', 'rightharpoondown',
    'forall', 'exists', 'nexists', 'emptyset', 'varnothing',
    # Set theory
    'subset', 'supset', 'subseteq', 'supseteq', 'subsetneq', 'supsetneq',
    'cap', 'cup', 'oplus', 'ominus', 'otimes', 'oslash', 'odot',
    'in', 'notin', 'ni', 'notni', 'setminus',
    # Brackets & delimiters
    'left', 'right', 'bigl', 'bigr', 'Bigl', 'Bigr', 'biggl', 'biggr', 'Biggl', 'Biggr',
    'lvert', 'rvert', 'lVert', 'rVert', 'langle', 'rangle', 'lceil', 'rceil',
    'lfloor', 'rfloor',
    # Dots & spacing
    'cdots', 'vdots', 'ddots', 'ldots', 'iddots',
    'quad', 'qquad', 'colon', 'medspace', 'thickspace', 'thinspace',
    '!', ':', ';', ',',
    # Fractions & such
    'frac', 'tfrac', 'dfrac', 'cfrac', 'binom', 'tbinom', 'dbinom',
    'partial', 'nabla', 'infty', 'triangle', 'triangledown',
    'angle', 'measuredangle', 'sphericalangle',
    'top', 'bot', 'perp', 'parallel', 'nparallel',
    'backslash', 'setminus',
    'times', 'cdot', 'circ', 'bullet', 'div', 'pm', 'mp', 'ast', 'star',
    'dagger', 'ddagger', 'amalg', 'sqcap', 'sqcup', 'wedge', 'vee',
    'bar', 'tilde', 'hat', 'dot', 'ddot', 'breve', 'check', 'vec',
    'acute', 'grave', 'mathring', 'widetilde', 'widehat',
    'overbrace', 'underbrace', 'overleftarrow', 'overrightarrow',
    'overleftrightarrow', 'overline', 'underline',
    'sqrt', 'root',
    'operatorname', 'text',
    'begin', 'end',
    'displaystyle', 'textstyle', 'scriptstyle', 'scriptscriptstyle',
    'rm', 'cal', 'it', 'bf', 'sf', 'tt',
    'hfill', 'hfil', 'fill',
    'cr', 'hline', 'vline',
    'def', 'newcommand', 'renewcommand', 'providecommand',
    'DeclareMathOperator',
    # Specific commands found in shiclass
    'proj', 'span', 'cov', 'var', 'diag', 'arg', 'Re', 'Im',
    'exp', 'erf', 'erfc',
]

# Known environments that can have \\ as line break
LINEBREAK_ENVIRONMENTS = [
    'cases', 'array', 'matrix', 'pmatrix', 'bmatrix', 'Bmatrix', 'vmatrix',
    'Vmatrix', 'aligned', 'gathered', 'split', 'align', 'alignat',
    'flalign', 'multline', 'eqnarray', 'subarray', 'smallmatrix',
    'alignedat',
]


def extract_dollar_formulas(text):
    """
    Extract all $...$ and $$...$$ formulas from text.
    Returns list of (start_pos, end_pos, formula_text, is_display)
    """
    formulas = []
    pos = 0
    while pos < len(text):
        # Try display math $$...$$
        if text[pos:pos+2] == '$$':
            end = text.find('$$', pos+2)
            if end == -1:
                formulas.append((pos, len(text), text[pos:], True))
                break
            formulas.append((pos, end+2, text[pos:end+2], True))
            pos = end + 2
        # Try inline math $...$
        elif text[pos] == '$':
            end = text.find('$', pos+1)
            if end == -1:
                formulas.append((pos, len(text), text[pos:], False))
                break
            formulas.append((pos, end+1, text[pos:end+1], False))
            pos = end + 1
        else:
            pos += 1
    return formulas


def find_line_number(text, pos):
    """Given a position in text, return the 1-based line number."""
    return text[:pos].count('\n') + 1


def scan_file(filepath):
    """Scan a single HTML file for KaTeX issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    issues = []
    
    # =====================================================
    # CHECK 1: Count total $ (quick unclosed check)
    # =====================================================
    dollar_count = content.count('$')
    if dollar_count % 2 != 0:
        # Find positions of all $ to locate the unclosed one
        positions = [i for i, c in enumerate(content) if c == '$']
        line_nums = [find_line_number(content, p) for p in positions]
        issues.append({
            'file': os.path.basename(filepath),
            'line': ', '.join(str(l) for l in line_nums),
            'type': 'unclosed_dollar',
            'detail': f'文件中共有 {dollar_count} 个 $，为奇数，说明有未闭合的 $ 分隔符',
            'extract': '',
            'fix': '检查所有 $ 和 $$ 对，确保每个开启的都有对应的闭合'
        })
    
    # =====================================================
    # CHECK 2: \$ (escaped dollar sign) - should not exist
    # =====================================================
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'(?<!\$)\\$(?!\$)', line):
            # This is \$ (backslash followed by dollar, not preceded by $ and not followed by $)
            idx = m.start()
            context = line[max(0,idx-15):idx+15]
            issues.append({
                'file': os.path.basename(filepath),
                'line': i,
                'type': 'escaped_dollar',
                'detail': f'"\\$" 转义美元符号 (应该是 "$")',
                'extract': f'...{context.strip()}...',
                'fix': '将 "\\$" 替换为 "$"'
            })
    
    # =====================================================
    # CHECK 3: Look at individual formulas for issues
    # =====================================================
    formulas = extract_dollar_formulas(content)
    
    for start, end, formula_text, is_display in formulas:
        line_start = find_line_number(content, start)
        line_end = find_line_number(content, end)
        formula_content = formula_text[1:-1] if not is_display else formula_text[2:-2]
        
        # --- 3a: Double backslash before LaTeX commands (e.g., \\mathbb) ---
        for cmd in LATEX_COMMANDS:
            # Match \\command but NOT \\\\command (4 backslashes)
            # We want to find patterns like: \\alpha, \\mathbb, etc.
            # But NOT: \\\\alpha (which would be two line-breaks then \alpha)
            # Also NOT: inside a \\\\ sequence that's a line break
            pattern = re.compile(r'(?<!\\)\\\\(?:\\\\)*(' + re.escape(cmd) + r')\b')
            for m in pattern.finditer(formula_content):
                issues.append({
                    'file': os.path.basename(filepath),
                    'line': line_start,
                    'type': 'double_backslash_before_command',
                    'detail': f'"\\\\\\\\{cmd}" 双反斜杠在命令前 (应该用 "\\\\{cmd}")',
                    'extract': formula_text.strip()[:100],
                    'fix': f'将 "\\\\\\\\{cmd}" 替换为 "\\\\{cmd}"'
                })
        
        # --- 3b: Triple backslash \left\\{ or \right\\} ---
        for m in re.finditer(r'\\(left|right)\\\\\{', formula_content):
            issues.append({
                'file': os.path.basename(filepath),
                'line': line_start,
                'type': 'triple_bs_leftright_brace',
                'detail': f'"\\{m.group(1)}\\\\{{" 三反斜杠模式 (应该用 "\\{m.group(1)}{{")',
                'extract': formula_text.strip()[:100],
                'fix': f'将 "\\{m.group(1)}\\\\{{" 替换为 "\\{m.group(1)}{{"'
            })
        
        # --- 3c: \\{ or \\} (double backslash + brace, should be \{ or \}) ---
        for m in re.finditer(r'(?<!\\)\\\\\{', formula_content):
            issues.append({
                'file': os.path.basename(filepath),
                'line': line_start,
                'type': 'double_bs_brace',
                'detail': f'"\\\\{{" 双反斜杠+左大括号 (应该用 "\\{{")',
                'extract': formula_text.strip()[:100],
                'fix': f'将 "\\\\{{" 替换为 "\\{{"'
            })
        for m in re.finditer(r'(?<!\\)\\\\\}', formula_content):
            issues.append({
                'file': os.path.basename(filepath),
                'line': line_start,
                'type': 'double_bs_brace',
                'detail': f'"\\\\}}" 双反斜杠+右大括号 (应该用 "\\}}")',
                'extract': formula_text.strip()[:100],
                'fix': f'将 "\\\\}}" 替换为 "\\}}"'
            })
        
        # --- 3d: \label, \tag, \ref, \cite - KaTeX unsupported ---
        for cmd in ['label', 'tag', 'ref', 'eqref', 'pageref', 'cite', 'bibitem',
                     'nocite', 'bibliographystyle', 'bibliography']:
            pattern = re.compile(r'\\' + re.escape(cmd) + r'\b')
            for m in pattern.finditer(formula_content):
                issues.append({
                    'file': os.path.basename(filepath),
                    'line': line_start,
                    'type': 'unsupported_command',
                    'detail': f'"\\{cmd}" 引用/标签命令 — KaTeX 不支持',
                    'extract': formula_text.strip()[:100],
                    'fix': f'移除 "\\{cmd}" 或替换为 KaTeX 支持的等效命令'
                })
        
        # --- 3e: \begin{xxx} without matching \end{xxx} ---
        begins = re.findall(r'\\begin\{(\w+)\}', formula_content)
        ends = re.findall(r'\\end\{(\w+)\}', formula_content)
        
        # Count unmatched
        begin_counts = defaultdict(int)
        end_counts = defaultdict(int)
        for b in begins:
            begin_counts[b] += 1
        for e in ends:
            end_counts[e] += 1
        
        for env in set(list(begin_counts.keys()) + list(end_counts.keys())):
            diff = begin_counts.get(env, 0) - end_counts.get(env, 0)
            if diff > 0:
                issues.append({
                    'file': os.path.basename(filepath),
                    'line': line_start,
                    'type': 'unmatched_begin_end',
                    'detail': f'"\\begin{{{env}}}" 无对应 "\\end{{{env}}}" (缺少 {diff} 个 \\end{{{env}}})',
                    'extract': formula_text.strip()[:100],
                    'fix': f'添加对应的 "\\end{{{env}}}"'
                })
            elif diff < 0:
                issues.append({
                    'file': os.path.basename(filepath),
                    'line': line_start,
                    'type': 'unmatched_begin_end',
                    'detail': f'"\\end{{{env}}}" 无对应 "\\begin{{{env}}}" (多出 {-diff} 个 \\end{{{env}}})',
                    'extract': formula_text.strip()[:100],
                    'fix': f'检查是否有多余的 "\\end{{{env}}}"'
                })
        
        # --- 3f: HTML tags inside formulas ---
        html_tag_pattern = re.compile(r'<\s*(?:br|div|span|p|a|img|b|i|em|strong|code|pre|h[1-6]|table|tr|td|th)\b[^>]*>', re.IGNORECASE)
        for m in html_tag_pattern.finditer(formula_text):
            # Check if this is display math with embedded HTML (likely a problem)
            context_before = formula_text[max(0, m.start()-10):m.start()]
            context_after = formula_text[m.end():min(len(formula_text), m.end()+10)]
            issues.append({
                'file': os.path.basename(filepath),
                'line': line_start,
                'type': 'html_tag_in_formula',
                'detail': f'公式内包含 HTML 标签: "{m.group()}"',
                'extract': f'...{context_before}|{m.group()}|{context_after}...',
                'fix': '将 HTML 标签移出公式或使用纯 LaTeX 替代'
            })

        # --- 3g: \\ at end of inline $...$ formulas (linebreak in inline math) ---
        if not is_display:
            # Check if there's a \\ that's NOT inside an environment
            # \\ is valid in cases, array, matrix, aligned, gathered, split, etc.
            # But in plain inline math (not in any environment), \\ would error
            
            # Check if this $...$ is inside a known environment
            # Look backwards for \begin{xxx}
            text_before = content[max(0, start-200):start]
            in_environment = False
            for env in LINEBREAK_ENVIRONMENTS:
                if re.search(r'\\begin\{' + re.escape(env) + r'\}', text_before):
                    in_environment = True
                    break
            
            if not in_environment:
                # Check for \\ inside the inline formula
                for m in re.finditer(r'(?<!\\)\\\\', formula_content):
                    # But only flag it if it seems like a standalone \\ (line break)
                    # rather than something like \\{ or \\}
                    after = formula_content[m.end():m.end()+1]
                    if after not in ['{', '}', '\\']:  # Not \\{ or \\} or \\\\
                        issues.append({
                            'file': os.path.basename(filepath),
                            'line': line_start,
                            'type': 'linebreak_in_inline_math',
                            'detail': f'行内公式 $...$ 中的 "\\\\" — KaTeX 会报错 (行内公式不支持换行)',
                            'extract': formula_text.strip()[:100],
                            'fix': '将行内公式改为显示公式 $$...$$ 或移除多余的 "\\\\"'
                        })
        
    # =====================================================
    # CHECK 4: Global \begin/end mismatches across the file
    # =====================================================
    all_begins = re.findall(r'\\begin\{(\w+)\}', content)
    all_ends = re.findall(r'\\end\{(\w+)\}', content)
    
    begin_counts = defaultdict(int)
    end_counts = defaultdict(int)
    for b in all_begins:
        begin_counts[b] += 1
    for e in all_ends:
        end_counts[e] += 1
    
    for env in set(list(begin_counts.keys()) + list(end_counts.keys())):
        diff = begin_counts.get(env, 0) - end_counts.get(env, 0)
        if diff > 0:
            issues.append({
                'file': os.path.basename(filepath),
                'line': 'global',
                'type': 'global_unmatched_begin_end',
                'detail': f'全局: "\\begin{{{env}}}" 出现 {begin_counts[env]} 次，但 "\\end{{{env}}}" 只有 {end_counts[env]} 次 (缺少 {diff})',
                'extract': '',
                'fix': f'检查文件所有 "\\begin{{{env}}}" 是否有对应的 "\\end{{{env}}}"'
            })

    # =====================================================
    # CHECK 5: Excessive backslashes at end of formula lines
    # Check for patterns like \\\\\\\\\\\\\\$ (many backslashes before $)
    # =====================================================
    for i, line in enumerate(lines, 1):
        # Look for 6+ consecutive backslashes (```\\``````) which would be 3+ \\\\ in LaTeX
        for m in re.finditer(r'(?<!\\)(\\\\\\\\){2,}', line):
            count_bs = len(m.group())
            context = line[max(0,m.start()-20):m.end()+10]
            if count_bs >= 6:  # 3 or more \\
                issues.append({
                    'file': os.path.basename(filepath),
                    'line': i,
                    'type': 'excessive_backslashes',
                    'detail': f'连续 {count_bs} 个反斜杠 (计为 {count_bs//2} 个 LaTeX 换行符) — 可能有多余的 \\\\',
                    'extract': f'...{context.strip()}...',
                    'fix': '检查并减少多余的 \\\\ 换行符，通常每个公式行结束只需要一个 \\\\'
                })

    # =====================================================
    # CHECK 6: $ inside $$...$$ (nested math mode)
    # =====================================================
    # Find all $$...$$ blocks and check for $ inside them
    display_positions = []
    pos = 0
    while pos < len(content):
        if content[pos:pos+2] == '$$':
            end = content.find('$$', pos+2)
            if end == -1:
                break
            display_positions.append((pos, end+2))
            pos = end + 2
        else:
            pos += 1
    
    for start, end in display_positions:
        inner = content[start+2:end-2]
        # Count $ inside (but not $$)
        single_dollar_positions = []
        inner_pos = 0
        while inner_pos < len(inner):
            if inner[inner_pos:inner_pos+2] == '$$':
                inner_pos += 2
            elif inner[inner_pos] == '$':
                single_dollar_positions.append(start + 2 + inner_pos)
                inner_pos += 1
            else:
                inner_pos += 1
        
        if single_dollar_positions:
            line_nums = [find_line_number(content, p) for p in single_dollar_positions]
            issues.append({
                'file': os.path.basename(filepath),
                'line': ', '.join(str(l) for l in line_nums[:5]),
                'type': 'nested_dollar_in_display',
                'detail': f'在 $$...$$ 显示公式内发现 {len(single_dollar_positions)} 个单独的 $ (第 {", ".join(str(l) for l in line_nums[:5])} 行) — $ 会显示为美元符号字面量',
                'extract': inner[:80],
                'fix': '移除 $$...$$ 内部的 $ 分隔符，LaTeX 在显示公式中不需要 $'
            })

    return issues


def main():
    html_files = sorted([f for f in os.listdir(LESSONS_DIR) if f.endswith('.html')])
    
    all_issues = defaultdict(list)  # file -> list of issues
    clean_files = []
    
    print("=" * 80)
    print("  KaTeX 公式渲染问题扫描报告 — shiclass 项目")
    print("=" * 80)
    print()
    
    for fname in html_files:
        fpath = os.path.join(LESSONS_DIR, fname)
        issues = scan_file(fpath)
        if not issues:
            clean_files.append(fname)
        else:
            all_issues[fname] = issues
    
    # Print clean files
    print(f"📗 无问题的文件 (Clean): {len(clean_files)}")
    print("-" * 60)
    for fname in clean_files:
        print(f"  ✅ {fname}")
    print()
    
    # Print issues by file
    total_issues = 0
    problem_files = len(all_issues)
    
    if problem_files > 0:
        print(f"📕 有问题的文件: {problem_files}")
        print("=" * 80)
        
        for fname in sorted(all_issues.keys()):
            issues = all_issues[fname]
            total_issues += len(issues)
            print(f"\n🔴 {fname} — {len(issues)} 个问题")
            print("-" * 80)
            
            for idx, issue in enumerate(issues, 1):
                line_str = f"行 {issue['line']}" if issue['line'] != 'global' else '全局'
                
                type_labels = {
                    'unclosed_dollar': '未闭合 $',
                    'escaped_dollar': '转义 $ \\$',
                    'double_backslash_before_command': '命令前双反斜杠 \\\\cmd',
                    'triple_bs_leftright_brace': '三反斜杠 \\left\\\\{',
                    'double_bs_brace': '双反斜杠大括号 \\\\{',
                    'unsupported_command': 'KaTeX 不支持的命令',
                    'unmatched_begin_end': '\\begin/\\end 不匹配',
                    'global_unmatched_begin_end': '全局 \\begin/\\end 不匹配',
                    'html_tag_in_formula': '公式内 HTML 标签',
                    'linebreak_in_inline_math': '行内公式换行符 \\\\',
                    'excessive_backslashes': '过多连续反斜杠',
                    'nested_dollar_in_display': '$$ 内嵌套 $',
                }
                tlabel = type_labels.get(issue['type'], issue['type'])
                
                print(f"  [{idx}] {line_str} | {tlabel}")
                print(f"       问题: {issue['detail']}")
                if issue['extract']:
                    print(f"       片段: {issue['extract'][:100]}")
                print(f"       修复: {issue['fix']}")
                print()
    
    # Summary
    print("=" * 80)
    print(f"  扫描统计总结")
    print("=" * 80)
    print(f"  总文件数:      {len(html_files)}")
    print(f"  无问题文件:    {len(clean_files)} ✅")
    print(f"  有问题文件:    {problem_files} 🔴")
    print(f"  问题总数:      {total_issues}")
    print()
    
    # Group by type
    type_counts = defaultdict(int)
    for fname, issues in all_issues.items():
        for issue in issues:
            type_counts[issue['type']] += 1
    
    if type_counts:
        print("各类型问题分布:")
        for t, c in sorted(type_counts.items(), key=lambda x: -x[1]):
            tlabel = {
                'unclosed_dollar': '未闭合 $',
                'escaped_dollar': '转义 $ \\$',
                'double_backslash_before_command': '命令前双反斜杠 \\\\cmd',
                'triple_bs_leftright_brace': '三反斜杠 \\left\\\\{',
                'double_bs_brace': '双反斜杠大括号 \\\\{',
                'unsupported_command': 'KaTeX 不支持的命令',
                'unmatched_begin_end': '\\begin/\\end 不匹配',
                'global_unmatched_begin_end': '全局 \\begin/\\end 不匹配',
                'html_tag_in_formula': '公式内 HTML 标签',
                'linebreak_in_inline_math': '行内公式换行符 \\\\',
                'excessive_backslashes': '过多连续反斜杠',
                'nested_dollar_in_display': '$$ 内嵌套 $',
            }.get(t, t)
            bar = '#' * min(c, 50)
            print(f"  {tlabel:30s} : {c:3d}  {bar}")


if __name__ == '__main__':
    main()
