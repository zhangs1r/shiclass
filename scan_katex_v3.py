#!/usr/bin/env python3
"""KaTeX Formula Issue Scanner v3 — shiclass project."""
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
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    issues = []
    fname = os.path.basename(filepath)

    # CHECK 1: escaped dollar sign (literal backslash + dollar)
    for i, line in enumerate(lines, 1):
        pos = 0
        while True:
            idx = line.find('\$', pos)
            if idx == -1:
                break
            prev_is_dollar = (idx > 0 and line[idx-1] == '$')
            next_is_dollar = (idx + 2 < len(line) and line[idx+2] == '$')
            if not prev_is_dollar and not next_is_dollar:
                ctx = line[max(0, idx-15):idx+15].strip()
                issues.append({
                    'type': 'escaped_dollar',
                    'line': i,
                    'detail': "Translated dollar sign '\\$' — should be '$' as math delimiter",
                    'extract': ctx,
                    'fix': "Replace '\\$' with '$'"
                })
            pos = idx + 2

    # CHECK 2: KaTeX-unsupported commands
    unsupported = ['label', 'tag', 'ref', 'eqref', 'pageref', 'cite',
                   'bibitem', 'nocite', 'bibliographystyle', 'bibliography']
    for i, line in enumerate(lines, 1):
        for cmd in unsupported:
            for m in re.finditer(r'\\' + cmd + r'\b', line):
                issues.append({
                    'type': 'unsupported_command',
                    'line': i,
                    'detail': "'\\" + cmd + "' — KaTeX does not support reference/label commands",
                    'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                    'fix': "Remove '\\" + cmd + "' or replace with KaTeX-compatible equivalent"
                })

    # CHECK 3: 4 backslashes before LaTeX commands
    latex_cmds = [
        'mathbb', 'mathrm', 'mathbf', 'mathsf', 'mathit', 'mathcal', 'mathscr',
        'mathfrak', 'texttt', 'text',
        'sum', 'prod', 'coprod', 'int', 'iint', 'iiint', 'oint',
        'bigcup', 'bigcap', 'bigvee', 'bigwedge', 'bigoplus', 'bigotimes',
        'lim', 'limsup', 'liminf', 'sup', 'inf', 'min', 'max',
        'sin', 'cos', 'tan', 'cot', 'sec', 'csc', 'arcsin', 'arccos', 'arctan',
        'sinh', 'cosh', 'tanh', 'coth', 'log', 'ln', 'lg', 'exp',
        'det', 'dim', 'deg', 'gcd', 'lcm', 'Pr', 'tr', 'rank', 'span', 'proj',
        'equiv', 'approx', 'neq', 'ne', 'leq', 'geq',
        'mapsto', 'to', 'rightarrow', 'Rightarrow', 'leftarrow', 'Leftarrow',
        'leftrightarrow', 'Leftrightarrow',
        'uparrow', 'Uparrow', 'downarrow', 'Downarrow',
        'forall', 'exists', 'emptyset',
        'subset', 'supset', 'subseteq', 'supseteq',
        'cap', 'cup', 'oplus', 'ominus', 'otimes', 'oslash', 'odot',
        'in', 'notin', 'ni', 'setminus', 'mid', 'parallel',
        'left', 'right', 'bigl', 'bigr',
        'lvert', 'rvert', 'lVert', 'rVert', 'langle', 'rangle',
        'cdots', 'vdots', 'ddots', 'ldots',
        'frac', 'tfrac', 'dfrac', 'cfrac', 'binom',
        'partial', 'nabla', 'infty', 'triangle', 'angle',
        'times', 'cdot', 'circ', 'bullet', 'div', 'pm', 'mp', 'ast', 'star',
        'bar', 'tilde', 'hat', 'dot', 'ddot', 'breve', 'check', 'vec',
        'acute', 'grave', 'widetilde', 'widehat',
        'overbrace', 'underbrace', 'overline', 'underline',
        'sqrt', 'root', 'surd',
        'displaystyle', 'textstyle',
        'alpha', 'beta', 'gamma', 'delta', 'epsilon', 'varepsilon', 'zeta',
        'eta', 'theta', 'vartheta', 'iota', 'kappa', 'lambda', 'mu', 'nu',
        'xi', 'omicron', 'pi', 'varpi', 'rho', 'varrho', 'sigma', 'varsigma',
        'tau', 'upsilon', 'phi', 'varphi', 'chi', 'psi', 'omega',
        'Gamma', 'Delta', 'Theta', 'Lambda', 'Xi', 'Pi', 'Sigma',
        'Phi', 'Psi', 'Omega', 'Upsilon',
        'operatorname', 'DeclareMathOperator',
        'proj', 'span', 'cov', 'var', 'diag', 'Re', 'Im',
        'erf', 'erfc', 'arg', 'argmin', 'argmax',
        'bmod', 'pmod', 'mod', 'colon',
        'quad', 'qquad', 'hspace', 'vspace',
    ]
    for i, line in enumerate(lines, 1):
        for cmd in latex_cmds:
            for m in re.finditer(r'(?<!\\)\\\\\\\\(?!\\)(' + cmd + r')\b', line):
                issues.append({
                    'type': 'double_backslash_before_command',
                    'line': i,
                    'detail': "'\\\\" + cmd + "' — KaTeX sees \\\\" + cmd + " (linebreak + cmd), should be \\" + cmd,
                    'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 50),
                    'fix': "Replace '\\\\" + cmd + "' with '\\" + cmd + "'"
                })

    # CHECK 4: left\\{ or right\\{
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'\\(left|right)\\\\\{', line):
            grp = m.group(1)
            issues.append({
                'type': 'triple_bs_leftright_brace',
                'line': i,
                'detail': "'\\" + grp + "\\\\{' — should be '\\" + grp + "\\{'",
                'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                'fix': "Replace '\\" + grp + "\\\\{' with '\\" + grp + "\\{'"
            })

    # CHECK 5: \\{ or \\}
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'(?<!\\)\\\\\{', line):
            issues.append({
                'type': 'double_bs_brace',
                'line': i,
                'detail': "'\\\\{' — double backslash+brace, should be '\\{'",
                'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                'fix': "Replace '\\\\{' with '\\{'"
            })
        for m in re.finditer(r'(?<!\\)\\\\\}', line):
            issues.append({
                'type': 'double_bs_brace',
                'line': i,
                'detail': "'\\\\}' — double backslash+brace, should be '\\}'",
                'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 40),
                'fix': "Replace '\\\\}' with '\\}'"
            })

    # CHECK 6: begin/end mismatches
    all_begins = re.findall(r'\\begin\{(\w+)\}', content)
    all_ends = re.findall(r'\\end\{(\w+)\}', content)
    begin_counter = Counter(all_begins)
    end_counter = Counter(all_ends)

    for env in set(list(begin_counter.keys()) + list(end_counter.keys())):
        diff = begin_counter[env] - end_counter[env]
        if diff > 0:
            issues.append({
                'type': 'unmatched_begin_end',
                'line': 'global',
                'detail': ("'\\begin{" + env + "}' appears " + str(begin_counter[env]) +
                          " times, '\\end{" + env + "}' appears " + str(end_counter[env]) +
                          " times (missing " + str(diff) + " \\end{" + env + "})"),
                'extract': '',
                'fix': "Add corresponding '\\end{" + env + "}'"
            })
        elif diff < 0:
            issues.append({
                'type': 'unmatched_begin_end',
                'line': 'global',
                'detail': ("'\\end{" + env + "}' appears " + str(end_counter[env]) +
                          " times, '\\begin{" + env + "}' appears " + str(begin_counter[env]) +
                          " times (extra " + str(-diff) + " \\end{" + env + "})"),
                'extract': '',
                'fix': "Check for extra '\\end{" + env + "}'"
            })

    # CHECK 7: Excessive consecutive backslashes (8+ in source)
    for i, line in enumerate(lines, 1):
        for m in re.finditer(r'\\\\{6,}', line):
            raw_bs = m.group()
            bs_count = len(raw_bs)
            katex_bs = bs_count // 2
            katex_lb = katex_bs // 2
            if katex_lb >= 2:
                issues.append({
                    'type': 'excessive_backslashes',
                    'line': i,
                    'detail': (str(bs_count) + " consecutive backslashes (KaTeX sees " +
                              str(katex_bs) + " \\ = " + str(katex_lb) + " linebreaks) — excess \\\\"),
                    'extract': get_context(content, sum(len(l)+1 for l in lines[:i-1]) + m.start(), 50),
                    'fix': "Keep only one '\\\\' per formula line, remove extras"
                })

    # CHECK 8: Unclosed $
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
            'line': 'global',
            'detail': (str(single_dollars) + " single $ in file (odd) — unclosed $ boundary exists"),
            'extract': '',
            'fix': "Check all $...$ pairs are properly closed"
        })

    # CHECK 9: cases env issues
    cases_pattern = re.compile(r'\\begin\{cases\}(.*?)\\end\{cases\}', re.DOTALL)
    for m in cases_pattern.finditer(content):
        cc = m.group(1)
        cs = m.start()
        cl = find_line_number(content, cs)
        for b in re.finditer(r'(?<!\\)\\\\\{', cc):
            issues.append({
                'type': 'cases_bs_brace',
                'line': cl,
                'detail': "'\\\\{' inside cases env — should be '\\{'",
                'extract': get_context(content, cs + b.start(), 40),
                'fix': "Replace '\\\\{' with '\\{'"
            })
        for b in re.finditer(r'(?<!\\)\\\\\}', cc):
            issues.append({
                'type': 'cases_bs_brace',
                'line': cl,
                'detail': "'\\\\}' inside cases env — should be '\\}'",
                'extract': get_context(content, cs + b.start(), 40),
                'fix': "Replace '\\\\}' with '\\}'"
            })
        for t in re.finditer(r'\\(left|right)\\\\\{', cc):
            g = t.group(1)
            issues.append({
                'type': 'cases_triple_brace',
                'line': cl,
                'detail': "'\\" + g + "\\\\{' inside cases — should be '\\" + g + "\\{'",
                'extract': get_context(content, cs + t.start(), 40),
                'fix': "Replace '\\" + g + "\\\\{' with '\\" + g + "\\{'"
            })

    # CHECK 10: $ inside $$ (nested math delimiters)
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
        dollar_count = 0
        dollar_positions = []
        i = 0
        while i < len(inner):
            if inner[i:i+2] == '$$':
                i += 2
            elif inner[i] == '$':
                dollar_count += 1
                dollar_positions.append(start + 2 + i)
                i += 1
            else:
                i += 1

        if dollar_count >= 2:
            line_nums = sorted(set(find_line_number(content, p) for p in dollar_positions))
            issues.append({
                'type': 'nested_dollar_in_display',
                'line': ', '.join(str(l) for l in line_nums[:6]),
                'detail': (str(dollar_count) + " solo $ inside $$...$$ (lines " +
                          ', '.join(str(l) for l in line_nums[:6]) +
                          ") — $ renders as literal dollar sign"),
                'extract': inner[:80].replace('\n', '\\n'),
                'fix': "Remove $ inside $$ — already in display math mode"
            })

    # Deduplicate
    seen = set()
    cleaned = []
    for issue in issues:
        if issue['type'] == 'escaped_dollar':
            key = (fname, issue['line'], issue['type'], issue['extract'][:30])
        elif issue['type'] == 'excessive_backslashes':
            key = (fname, issue['line'], issue['type'])
        elif issue['type'] == 'double_backslash_before_command':
            key = (fname, issue['line'], issue['type'])
        elif issue['type'] == 'nested_dollar_in_display':
            key = (fname, issue['line'], issue['type'])
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
    print("  shiclass KaTeX Formula Rendering Issue Scanner — FINAL REPORT")
    print("=" * 80)
    print()

    for fname in html_files:
        fpath = os.path.join(LESSONS_DIR, fname)
        issues = scan_file(fpath)
        if not issues:
            clean_files.append(fname)
        else:
            all_issues[fname] = issues

    print("CLEAN files (no issues):")
    print("-" * 50)
    for fname in clean_files:
        print(f"  [OK] {fname}")
    print(f"  Total: {len(clean_files)} files clean")
    print()

    total_issues = 0
    for fname in sorted(all_issues.keys()):
        issues = all_issues[fname]
        total_issues += len(issues)
        print(f"\n[ISSUES] {fname} — {len(issues)} problem(s)")
        print("-" * 70)

        type_labels = {
            'escaped_dollar': 'Escaped $ \\$',
            'unsupported_command': 'Unsupported KaTeX cmd',
            'double_backslash_before_command': 'Double \\\\ before cmd',
            'triple_bs_leftright_brace': 'Triple \\\\ brace \\left\\\\{',
            'double_bs_brace': 'Double \\\\ brace \\\\{',
            'unmatched_begin_end': '\\begin/\\end mismatch',
            'excessive_backslashes': 'Excessive \\\\',
            'unclosed_dollar': 'Unclosed $',
            'cases_bs_brace': '\\\\{ in cases env',
            'cases_triple_brace': 'Triple \\\\ in cases',
            'nested_dollar_in_display': '$ inside $$',
        }

        for idx, issue in enumerate(issues, 1):
            ls = "line " + str(issue['line']) if issue['line'] != 'global' else 'global'
            tl = type_labels.get(issue['type'], issue['type'])

            print(f"  [{idx}] {ls} | {tl}")
            print(f"       Issue: {issue['detail']}")
            if issue['extract']:
                print(f"       Snippet: {issue['extract'][:100]}")
            print(f"       Fix: {issue['fix']}")
            print()

    problem_files = len(all_issues)
    print("=" * 80)
    print("  SUMMARY")
    print("=" * 80)
    print(f"  Total files:     {len(html_files)}")
    print(f"  Clean:           {len(clean_files)}")
    print(f"  Has issues:      {problem_files}")
    print(f"  Total issues:    {total_issues}")

    if total_issues > 0:
        print(f"\n  Issues by type:")
        type_counts = Counter()
        for fname, issues in all_issues.items():
            for issue in issues:
                type_counts[issue['type']] += 1
        short_labels = {
            'escaped_dollar': 'Escaped \\$',
            'unsupported_command': 'Unsupported cmd',
            'double_backslash_before_command': 'Double \\\\ before cmd',
            'triple_bs_leftright_brace': 'Triple \\\\ brace',
            'double_bs_brace': 'Double \\\\ brace',
            'unmatched_begin_end': '\\begin/\\end mismatch',
            'excessive_backslashes': 'Excessive \\\\',
            'unclosed_dollar': 'Unclosed $',
            'cases_bs_brace': '\\\\{ in cases',
            'cases_triple_brace': 'Triple \\\\ in cases',
            'nested_dollar_in_display': '$ inside $$',
        }
        for t, c in type_counts.most_common():
            sl = short_labels.get(t, t)
            bar = '#' * min(c, 50)
            print(f"  {sl:25s}: {c:3d}  {bar}")


if __name__ == '__main__':
    main()
