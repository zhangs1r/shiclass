#!/usr/bin/env python3
"""
KaTeX Formula Issue Scanner v2 — shiclass project.
Focuses on REAL KaTeX-breaking issues with minimal false positives.
"""
import re
import os
from collections import defaultdict, Counter

LESSONS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lessons')


def find_line_number(text, pos):
    return text[:pos].count('\n') + 1


def get_context(text, pos, width=50):
    start = max(0, pos - width)
    end = min(len(text), pos + width)
    ctx = text[start:end].replace('\n', '\\n')
    if start > 0:
        ctx = '...' + ctx
    if end < len(text):
        ctx = ctx + '...'
    return ctx


def scan_file(filepath):
    """Scan a single HTML file for KaTeX issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    issues = []
    fname = os.path.basename(filepath)

    # ======================================================================
    # CHECK 1: escaped dollar sign (leftover from bulk fix)
    # ======================================================================
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'(?<!\$)\\$(?!\$)', line):
            issues.append({
                'type': 'escaped_dollar',
                'line': i,
                'detail': "转义美元符号 '\\$' — 应该是 '$'",
                'extract': get_context(content, content.find('\\$', sum(len(l)+1 for l in lines[:i-1])), 40),
                'fix': "将 '\\$' 替换为 '$'"
            })

    # ======================================================================
    # CHECK 2: KaTeX-unsupported commands
    # ======================================================================
    unsupported_cmds = ['label', 'tag', 'ref', 'eqref', 'pageref', 'cite',
                        'bibitem', 'nocite', 'bibliographystyle', 'bibliography']
    for i, line in enumerate(lines, 1):
        for cmd in unsupported_cmds:
            for m in re.finditer(r'\\' + re.escape(cmd) + r'\b', line):
                issues.append({
                    'type': 'unsupported_command',
                    'line': i,
                    'detail': "'\\" + cmd + "' — KaTeX 不支持引用/标签命令",
                    'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                    'fix': "移除 '" + cmd + "' 或替换为 KaTeX 支持的等效表达"
                })

    # ======================================================================
    # CHECK 3: Double backslash before LaTeX commands (\\mathbb, etc.)
    # In HTML source, \\ renders as \ in DOM (correct), \\\\ renders as \\
    # So if we see \\\\cmd in source, DOM has \\cmd which KaTeX sees as \ + cmd = WRONG
    # ======================================================================
    # Only check inside math contexts (between $ or $$ delimiters)
    latex_cmds = [
        'mathbb', 'mathrm', 'mathbf', 'mathsf', 'mathit', 'mathcal', 'mathscr',
        'mathfrak', 'texttt', 'text',
        'sum', 'prod', 'coprod', 'int', 'iint', 'iiint', 'oint',
        'bigcup', 'bigcap', 'bigvee', 'bigwedge', 'bigoplus', 'bigotimes',
        'lim', 'limsup', 'liminf', 'sup', 'inf', 'min', 'max',
        'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'arcsin', 'arccos', 'arctan',
        'sinh', 'cosh', 'tanh', 'coth', 'log', 'ln', 'lg', 'exp',
        'det', 'dim', 'deg', 'gcd', 'lcm', 'Pr', 'tr', 'rank', 'span', 'proj',
        'equiv', 'approx', 'neq', 'ne', 'leq', 'geq', 'leqslant', 'geqslant',
        'll', 'gg', 'sim', 'simeq', 'cong', 'propto',
        'mapsto', 'to', 'rightarrow', 'Rightarrow', 'leftarrow', 'Leftarrow',
        'leftrightarrow', 'Leftrightarrow', 'longrightarrow', 'Longrightarrow',
        'uparrow', 'Uparrow', 'downarrow', 'Downarrow', 'updownarrow',
        'forall', 'exists', 'nexists', 'emptyset', 'varnothing',
        'subset', 'supset', 'subseteq', 'supseteq', 'subsetneq', 'supsetneq',
        'cap', 'cup', 'oplus', 'ominus', 'otimes', 'oslash', 'odot',
        'in', 'notin', 'ni', 'setminus', 'mid', 'parallel', 'nmid', 'nparallel',
        'left', 'right', 'bigl', 'bigr', 'Bigl', 'Bigr', 'biggl', 'biggr',
        'lvert', 'rvert', 'lVert', 'rVert', 'langle', 'rangle',
        'cdots', 'vdots', 'ddots', 'ldots', 'iddots',
        'frac', 'tfrac', 'dfrac', 'cfrac', 'binom', 'tbinom', 'dbinom',
        'partial', 'nabla', 'infty', 'triangle', 'angle',
        'times', 'cdot', 'circ', 'bullet', 'div', 'pm', 'mp', 'ast', 'star',
        'dagger', 'ddagger',
        'bar', 'tilde', 'hat', 'dot', 'ddot', 'breve', 'check', 'vec',
        'acute', 'grave', 'widetilde', 'widehat',
        'overbrace', 'underbrace', 'overline', 'underline',
        'sqrt', 'root', 'surd',
        'displaystyle', 'textstyle', 'scriptstyle',
        'hfill', 'hfil', 'fill', 'cr', 'hline', 'vline',
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'varepsilon', 'zeta',
        'eta', 'theta', 'vartheta', 'iota', 'kappa', 'lambda', 'mu', 'nu',
        'xi', 'omicron', 'pi', 'varpi', 'rho', 'varrho', 'sigma', 'varsigma',
        'tau', 'upsilon', 'phi', 'varphi', 'chi', 'psi', 'omega',
        'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma',
        'Phi', 'Psi', 'Omega', 'Upsilon',
        'operatorname', 'DeclareMathOperator',
        'proj', 'span', 'cov', 'var', 'diag', 'Re', 'Im',
        'erf', 'erfc', 'arg', 'argmin', 'argmax',
        'liminf', 'limsup', 'bmod', 'pmod', 'mod',
        'colon', 'medspace', 'thickspace', 'thinspace',
        'quad', 'qquad', 'hspace', 'vspace',
        'tag', 'label', 'ref', 'eqref',
    ]

    for i, line in enumerate(lines, 1):
        for cmd in latex_cmds:
            # Pattern: \\\\cmd (4 backslashes + cmd) → in DOM: \\cmd → KaTeX sees \\ + cmd = WRONG
            # But NOT: \\\\\\cmd (6 backslashes) which is \\\ in DOM = \\ + \cmd = weird
            # Also NOT: \\cmd (2 backslashes) → in DOM: \cmd = CORRECT
            
            # We want to match cases where there are 4 backslashes then the command
            # 4 backslashes in source = 2 backslashes in DOM = \\ + cmd = the problem
            for m in re.finditer(r'(?<!\\)\\\\\\\\(?!\\)(' + re.escape(cmd) + r')\b', line):
                # Check what's before the 4 backslashes — if preceded by even more
                # backslashes, skip
                pre = line[:m.start()]
                if pre.endswith('\\\\'):
                    # More than 4 backslashes, skip (handled by excessive check)
                    continue
                    
                issues.append({
                    'type': 'double_backslash_before_command',
                    'line': i,
                    'detail': "'\\\\\\\\" + cmd + "' — 命令前有 2 个反斜杠 (KaTeX看到 \\\\" + cmd + "，应该是 \\" + cmd + ")",
                    'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 50),
                    'fix': "将 '\\\\\\\\" + cmd + "' 替换为 '\\" + cmd + "' (删除一个反斜杠)"
                })

    # ======================================================================
    # CHECK 4: \left\\{ or \right\\} — triple backslash patterns
    # ======================================================================
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'\\(left|right)\\\\\{', line):
            issues.append({
                'type': 'triple_bs_leftright_brace',
                'line': i,
                'detail': "'\\" + m.group(1) + "\\\\{' — 三反斜杠模式，应该是 '\\" + m.group(1) + "\\{'",
                'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                'fix': "将 '\\" + m.group(1) + "\\\\{' 替换为 '\\" + m.group(1) + "\\{'"
            })

    # ======================================================================
    # CHECK 5: \\{ or \\} — double backslash + brace (should be \{ or \})
    # ======================================================================
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'(?<!\\)\\\\\{', line):
            issues.append({
                'type': 'double_bs_brace',
                'line': i,
                'detail': "'\\\\{' — 双反斜杠+左大括号，应该是 '\\{'",
                'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                'fix': "将 '\\\\{' 替换为 '\\{'"
            })
        for m in re.finditer(r'(?<!\\)\\\\\}', line):
            issues.append({
                'type': 'double_bs_brace',
                'line': i,
                'detail': "'\\\\}' — 双反斜杠+右大括号，应该是 '\\}'",
                'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                'fix': "将 '\\\\}' 替换为 '\\}'"
            })

    # ======================================================================
    # CHECK 6: \begin{xxx} / \end{xxx} mismatch
    # ======================================================================
    all_begins = re.findall(r'\\begin\{(\w+)\}', content)
    all_ends = re.findall(r'\\end\{(\w+)\}', content)

    begin_counter = Counter(all_begins)
    end_counter = Counter(all_ends)

    for env in set(list(begin_counter.keys()) + list(end_counter.keys())):
        diff = begin_counter[env] - end_counter[env]
        if diff > 0:
            issues.append({
                'type': 'unmatched_begin_end',
                'line': '全局',
                'detail': ("'\\begin{" + env + "}' 出现 " + str(begin_counter[env]) +
                          " 次，'\\end{" + env + "}' 出现 " + str(end_counter[env]) +
                          " 次 (缺少 " + str(diff) + " 个 \\end{" + env + "})"),
                'extract': '',
                'fix': "为每个 '\\begin{" + env + "}' 添加对应的 '\\end{" + env + "}'"
            })
        elif diff < 0:
            issues.append({
                'type': 'unmatched_begin_end',
                'line': '全局',
                'detail': ("'\\end{" + env + "}' 出现 " + str(end_counter[env]) +
                          " 次，'\\begin{" + env + "}' 出现 " + str(begin_counter[env]) +
                          " 次 (多出 " + str(-diff) + " 个 \\end{" + env + "})"),
                'extract': '',
                'fix': "检查是否有多余的 '\\end{" + env + "}'"
            })

    # ======================================================================
    # CHECK 7: Excessive consecutive backslashes (6+ in source = 3+ in DOM)
    # ======================================================================
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'\\\\{6,}', line):
            raw_bs = m.group()
            bs_count = len(raw_bs)
            katex_bs = bs_count // 2
            katex_linebreaks = katex_bs // 2

            if katex_linebreaks >= 2:
                issues.append({
                    'type': 'excessive_backslashes',
                    'line': i,
                    'detail': ("连续 " + str(bs_count) + " 个反斜杠 (KaTeX看到 " + str(katex_bs) +
                              " 个 \\ = " + str(katex_linebreaks) + " 个换行符) — 很可能有多余 \\\\"),
                    'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 50),
                    'fix': "每个公式行结束只需要一个 '\\\\' 换行符，删除多余的"
                })

    # ======================================================================
    # CHECK 8: Unclosed $ (odd single $ count)
    # ======================================================================
    single_dollars = 0
    pos = 0
    while pos < len(content):
        if content[pos:pos+2] == '$$':
            pos += 2
        elif content[pos] == '$':
            single_dollars += 1
            pos += 1
        else:
            pos += 1

    if single_dollars % 2 != 0:
        issues.append({
            'type': 'unclosed_dollar',
            'line': '全局',
            'detail': ("文件中共有 " + str(single_dollars) + " 个单独的 $（不含 $$），"
                      "数量为奇数，说明有未闭合的 $ 边界"),
            'extract': '',
            'fix': "检查所有 $...$ 对，确保每个开启的 $ 都有对应的闭合 $"
        })

    # ======================================================================
    # CHECK 9: \\{ or \\} inside \begin{cases}...\end{cases}
    # ======================================================================
    cases_pattern = re.compile(r'\\begin\{cases\}(.*?)\\end\{cases\}', re.DOTALL)
    for m in cases_pattern.finditer(content):
        cases_content = m.group(1)
        cases_start = m.start()
        cases_line = find_line_number(content, cases_start)

        for bs_brace in re.finditer(r'(?<!\\)\\\\\{', cases_content):
            issues.append({
                'type': 'cases_bs_brace',
                'line': cases_line,
                'detail': "在 cases 环境中发现 '\\\\{' — 应该是 '\\{'",
                'extract': get_context(content, cases_start + bs_brace.start(), 40),
                'fix': "将 '\\\\{' 替换为 '\\{'"
            })
        for bs_brace in re.finditer(r'(?<!\\)\\\\\}', cases_content):
            issues.append({
                'type': 'cases_bs_brace',
                'line': cases_line,
                'detail': "在 cases 环境中发现 '\\\\}' — 应该是 '\\}'",
                'extract': get_context(content, cases_start + bs_brace.start(), 40),
                'fix': "将 '\\\\}' 替换为 '\\}'"
            })

        for triple in re.finditer(r'\\(left|right)\\\\\{', cases_content):
            issues.append({
                'type': 'cases_triple_brace',
                'line': cases_line,
                'detail': ("在 cases 环境中发现 '\\" + triple.group(1) + "\\\\{' "
                          "— 应该是 '\\" + triple.group(1) + "\\{'"),
                'extract': get_context(content, cases_start + triple.start(), 40),
                'fix': ("将 '\\" + triple.group(1) + "\\\\{' "
                       "替换为 '\\" + triple.group(1) + "\\{'")
            })

    # ======================================================================
    # CHECK 10: HARD — \\ inside $...$ (inline math) outside any environment
    # Only flag when \\ is NOT inside bmatrix, aligned, cases, etc.
    # ======================================================================
    inline_envs = [
        'cases', 'array', 'matrix', 'pmatrix', 'bmatrix', 'Bmatrix',
        'vmatrix', 'Vmatrix', 'aligned', 'gathered', 'split',
        'align', 'alignat', 'flalign', 'multline', 'eqnarray',
        'smallmatrix', 'alignedat', 'subarray'
    ]
    env_pattern = r'\\begin\{(?:' + '|'.join(inline_envs) + r')\}'

    # Find all $...$ ranges
    dollar_ranges = []
    pos = 0
    while pos < len(content):
        if content[pos:pos+2] == '$$':
            pos += 2
        elif content[pos] == '$':
            end = content.find('$', pos+1)
            if end == -1:
                break
            dollar_ranges.append((pos+1, end, False))
            pos = end + 1
        else:
            pos += 1

    for start, end, _is_display in dollar_ranges:
        formula = content[start:end]
        formula_line = find_line_number(content, start)

        # Check if this $...$ is inside an environment that allows \\
        text_before = content[max(0, start-400):start]
        has_env = bool(re.search(env_pattern, text_before))

        if not has_env:
            # Check for \\ in the formula (that is NOT \\{ or \\} or \\\\)
            for bs_m in re.finditer(r'(?<!\\)\\\\', formula):
                after_idx = bs_m.end()
                after_char = formula[after_idx:after_idx+1] if after_idx < len(formula) else ''
                if after_char not in ['{', '}', '\\', ' ', '', '.', ',', ';', ':', '-', '+', '=']:
                    # Likely a line break in inline math
                    issues.append({
                        'type': 'inline_math_linebreak',
                        'line': formula_line,
                        'detail': "行内公式 $...$ 中的 '\\\\' — 在不含 aligned/cases/matrix 等环境的行内公式中不支持换行",
                        'extract': get_context(content, start, 60),
                        'fix': "将行内公式改为显示公式 $$...$$，或移除多余的 '\\\\'"
                    })
                    break  # Only flag once per formula

    # ======================================================================
    # Deduplicate
    # ======================================================================
    seen = set()
    cleaned = []
    for issue in issues:
        if issue['type'] == 'escaped_dollar':
            key = (fname, issue['line'], issue['type'], issue['extract'][:30])
        elif issue['type'] == 'double_backslash_before_command':
            key = (fname, issue['line'], issue['type'], issue['extract'][:40])
        else:
            key = (fname, issue['line'], issue['type'])
        if key not in seen:
            seen.add(key)
            issue.setdefault('file', fname)
            cleaned.append(issue)

    return cleaned


def main():
    html_files = sorted([f for f in os.listdir(LESSONS_DIR) if f.endswith('.html')])

    all_issues = defaultdict(list)
    clean_files = []

    print("=" * 80)
    print("  shiclass KaTeX 公式渲染问题扫描报告 v2")
    print("  (仅检测可能造成渲染失败的真实问题，尽量减少假阳性)")
    print("=" * 80)
    print()

    for fname in html_files:
        fpath = os.path.join(LESSONS_DIR, fname)
        issues = scan_file(fpath)
        if not issues:
            clean_files.append(fname)
        else:
            all_issues[fname] = issues

    print("无问题的文件 (Clean):")
    print("-" * 50)
    for fname in clean_files:
        print(f"  ✅ {fname}")
    print(f"  共 {len(clean_files)} 个文件无问题")
    print()

    total_issues = 0
    for fname in sorted(all_issues.keys()):
        issues = all_issues[fname]
        total_issues += len(issues)
        print(f"\n🔴 {fname} — {len(issues)} 个问题")
        print("-" * 70)

        type_labels = {
            'escaped_dollar': '转义美元符 \\$',
            'unsupported_command': 'KaTeX 不支持的命令',
            'double_backslash_before_command': '命令前多余反斜杠 \\\\cmd',
            'triple_bs_leftright_brace': '三反斜杠括号 \\left\\\\{',
            'double_bs_brace': '双反斜杠大括号 \\\\{',
            'unmatched_begin_end': '\\begin/\\end 不匹配',
            'excessive_backslashes': '过多连续反斜杠',
            'unclosed_dollar': '未闭合 $',
            'cases_bs_brace': 'cases内双反斜杠括号 \\\\{',
            'cases_triple_brace': 'cases内三反斜杠括号',
            'inline_math_linebreak': '行内公式换行符 \\\\',
        }

        for idx, issue in enumerate(issues, 1):
            line_str = "行 " + str(issue['line']) if issue['line'] != '全局' else '全局'
            tlabel = type_labels.get(issue['type'], issue['type'])

            print(f"  [{idx}] {line_str} | {tlabel}")
            print(f"       问题: {issue['detail']}")
            if issue['extract']:
                print(f"       片段: {issue['extract'][:100]}")
            print(f"       修复: {issue['fix']}")
            print()

    problem_files = len(all_issues)
    print("=" * 80)
    print("  扫描统计总结")
    print("=" * 80)
    print(f"  文件总数:      {len(html_files)}")
    print(f"  无问题:        {len(clean_files)} ✅")
    print(f"  有问题:        {problem_files} 🔴")
    print(f"  问题总数:      {total_issues}")

    if total_issues > 0:
        print(f"\n  各类型问题分布:")
        type_counts = Counter()
        type_labels_short = {
            'escaped_dollar': '转义 \\$',
            'unsupported_command': '不支持的命令',
            'double_backslash_before_command': '命令前多余 \\\\',
            'triple_bs_leftright_brace': '三反斜杠括号',
            'double_bs_brace': '双反斜杠大括号',
            'unmatched_begin_end': '\\begin/\\end 不匹配',
            'excessive_backslashes': '过多连续 \\\\',
            'unclosed_dollar': '未闭合 $',
            'cases_bs_brace': 'cases中 \\\\{',
            'cases_triple_brace': 'cases中三反斜杠',
            'inline_math_linebreak': '行内 \\\\ 换行',
        }
        for fname, issues in all_issues.items():
            for issue in issues:
                type_counts[issue['type']] += 1
        for t, c in type_counts.most_common():
            tlabel = type_labels_short.get(t, t)
            bar = '█' * min(c, 50)
            print(f"  {tlabel:20s}: {c:3d}  {bar}")


if __name__ == '__main__':
    main()
