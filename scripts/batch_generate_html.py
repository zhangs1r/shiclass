#!/usr/bin/env python3
"""
批量生成课程 HTML —— 从 SRT 字幕 + MinerU MD 笔记生成结构化的课程页面。
生成到 lessons/ 目录，遵循 shiclass 模板风格（暖色 PaperLesson 风 + MathJax）。
"""

import os, glob, re, html

# ── 配置 ──
SRT_DIR = "/home/zjq/shiclass/subtitles"
MD_DIR = "/home/zjq/shiclass/pdf-md"
LESSONS_DIR = "/home/zjq/shiclass/lessons"
COURSE_NOTES_DIR = "/home/zjq/shiclass/course-notes"

# HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · 施老师大课堂</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Serif+SC:wght@600;700;900&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/shiclass.css">
<script>
window.MathJax = {{
  tex: {{
    inlineMath: [['$', '$'], ['\\\\\\(', '\\\\\\)']],
    displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
  }},
  svg: {{ fontCache: 'global' }}
}};
</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-svg.js"></script>
</head>
<body>
<div class="page">

  <div class="hero">
    <div class="eyebrow">{eyebrow}</div>
    <h1>{title}</h1>
    <p class="subtitle">{subtitle}</p>
    <div class="hero-meta">
      {meta_tags}
    </div>
  </div>

  <main>
    {content}
  </main>

  <footer class="section-card" style="margin-top:2rem;text-align:center;">
    <div class="nav-links">
      <a href="../index.html">← 返回课程馆</a>
      {next_prev}
    </div>
    <p class="foot-note" style="margin-top:1.5rem;color:var(--text-light);font-size:0.85rem;">
      内容基于施凌老师课堂录制整理，结合 SRT 字幕与板书笔记生成。
    </p>
  </footer>

</div>
</body>
</html>"""

SECTION_TEMPLATE = """
  <section class="section-card">
    <h2>{heading}</h2>
    {body}
  </section>
"""

def parse_srt(srt_path):
    """从SRT提取文本内容"""
    if not os.path.exists(srt_path):
        return []
    with open(srt_path, encoding='utf-8', errors='ignore') as f:
        text = f.read()
    # 提取文本行（非序号、非时间行）
    lines = []
    for line in text.split('\n'):
        line = line.strip()
        if not line:
            continue
        if line.isdigit():
            continue
        if '-->' in line:
            continue
        lines.append(line)
    return lines

def read_md(md_path):
    """读取MinerU输出的MD"""
    if not os.path.exists(md_path):
        return ""
    with open(md_path, encoding='utf-8', errors='ignore') as f:
        return f.read()

def get_best_md(course_name):
    """找最匹配的MinerU MD文件"""
    # 找pdf-md下名称最接近的
    for d in sorted(glob.glob(f"{MD_DIR}/*{course_name}*"), reverse=True):
        md = os.path.join(d, "document.md")
        if os.path.exists(md):
            # "md文档"版本优先
            if "md文档" in d:
                return md
    # 没有md文档就取第一个
    for d in sorted(glob.glob(f"{MD_DIR}/*{course_name}*")):
        md = os.path.join(d, "document.md")
        if os.path.exists(md):
            return md
    # 更模糊的搜索
    for d in sorted(glob.glob(f"{MD_DIR}/*{course_name.split('KF_L')[1]}*")):
        md = os.path.join(d, "document.md")
        if os.path.exists(md):
            return md
    return None

def read_course_notes(course_key):
    """从course-notes读取现成的笔记"""
    for f in sorted(glob.glob(f"{COURSE_NOTES_DIR}/*{course_key}*")):
        with open(f, encoding='utf-8', errors='ignore') as fh:
            return fh.read()
    return None

def md_to_html_sections(md_text, max_sections=6):
    """把MD文本转换成HTML sections"""
    if not md_text.strip():
        return "<p>暂无板书笔记。</p>"
    
    sections = []
    lines = md_text.split('\n')
    current_heading = "核心内容"
    current_content = []
    
    for line in lines:
        if line.startswith('#'):
            if current_content:
                sections.append((current_heading, '\n'.join(current_content)))
                if len(sections) >= max_sections:
                    break
            current_heading = line.lstrip('#').strip()
            current_content = []
        else:
            current_content.append(line)
    
    if current_content and len(sections) < max_sections:
        sections.append((current_heading, '\n'.join(current_content)))
    
    result = ""
    for heading, content in sections:
        # 基本markdown到HTML转换
        content = html_escape(content)
        content = re.sub(r'\$\$(.*?)\$\$', r'$$\1$$', content, flags=re.DOTALL)
        content = re.sub(r'\$(.*?)\$', r'$\1$', content)
        content = content.replace('\n\n', '</p><p>').replace('\n', '<br>')
        result += SECTION_TEMPLATE.format(heading=heading, body=f'<p>{content}</p>')
    
    return result

def html_escape(text):
    """转义HTML但保留LaTeX语法"""
    # 先保护LaTeX
    latex_blocks = re.findall(r'\$\$.*?\$\$', text, re.DOTALL)
    latex_inline = re.findall(r'\$(?!\$)(.*?)\$', text)
    
    # 简单转义
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    return text

def generate_stub_html(lesson_num, title, eyebrow, subtitle, tags, srt_text, md_text):
    """为 stub 课程生成完整 HTML"""
    next_prev = ""
    
    # 从SRT提取内容要点
    srt_lines = srt_text[:30] if len(srt_text) > 30 else srt_text
    srt_summary = '\n'.join(srt_lines[:15]) if srt_lines else ""
    
    meta_html = '\n      '.join([f'<span>{t}</span>' for t in tags])
    
    # 课程内容
    content_sections = ""
    
    # 第一部分：课程概览（来自SRT）
    if srt_summary:
        content_sections += SECTION_TEMPLATE.format(
            heading="课程概览",
            body=f"<p>以下内容基于课堂实录整理：</p><blockquote style='background:var(--bg-subtle);padding:1rem;border-left:3px solid var(--accent);'>{html.escape(srt_summary[:2000])}</blockquote>"
        )
    
    # 第二部分：板书要点（来自MinerU MD）
    if md_text:
        content_sections += md_to_html_sections(md_text)
    else:
        content_sections += SECTION_TEMPLATE.format(
            heading="内容提要",
            body="<p>本课程内容基于课堂实录整理。建议配合视频学习。</p>"
        )
    
    # 练习与思考
    content_sections += SECTION_TEMPLATE.format(
        heading="练习与思考",
        body="""
        <div class="exercise-box">
          <ol>
            <li><details class="exercise-answer"><summary>回顾本节课的核心概念，你能用自己的话复述吗？</summary><div>尝试关闭视频，凭记忆把本节课讲的主要思路写下来。</div></details></li>
            <li><details class="exercise-answer"><summary>板书中的关键公式，你能独立推导一遍吗？</summary><div>建议手推一遍，不要直接看板书。</div></details></li>
          </ol>
        </div>
        """
    )
    
    filename = f"{lesson_num:04d}-{title.split('：')[0] if '：' in title else title[:20]}.html"
    filename = re.sub(r'[^\w\-\u4e00-\u9fff]+', '-', filename).strip('-') + '.html'
    
    html_content = HTML_TEMPLATE.format(
        title=title,
        eyebrow=eyebrow,
        subtitle=subtitle,
        meta_tags=meta_html,
        content=content_sections,
        next_prev=next_prev
    )
    
    return filename, html_content

# ── 主流程 ──
def main():
    # 定义需要生成的 stub 课程
    stubs = [
        {
            "num": 0,
            "eyebrow": "特邀分享 · 杨熙丞",
            "title": "图像算法在安防行业的应用",
            "subtitle": "特邀杨熙丞分享图像算法在安防行业中的实际应用案例与技术经验",
            "tags": ["📅 2025-10-25", "🧩 图像算法", "🎯 安防应用", "👤 杨熙丞"],
            "srt_keywords": ["杨熙丞", "图像算法"],
            "md_keywords": []
        },
        {
            "num": 1,
            "eyebrow": "研讨会系列 · 第1期",
            "title": "研究共同体与方向地图",
            "subtitle": "如何构建高效的研究共同体？绘制领域方向地图，找到自己的研究定位",
            "tags": ["📅 2025-11-01", "🧩 研究规范", "🎯 学术入门", "👤 施凌"],
            "srt_keywords": ["系列1"],
            "md_keywords": []
        },
        {
            "num": 2,
            "eyebrow": "研讨会系列 · 第2期",
            "title": "组规、学术规范与职业习惯",
            "subtitle": "研究生阶段应养成的学术规范与职业习惯",
            "tags": ["📅 2025-11-08", "🧩 学术规范", "🎯 职业习惯", "👤 施凌"],
            "srt_keywords": ["系列2"],
            "md_keywords": []
        },
        {
            "num": 3,
            "eyebrow": "研讨会系列 · 第3期",
            "title": "演讲技巧与学术表达",
            "subtitle": "如何做好学术演讲？从结构设计到表达技巧的全方位指南",
            "tags": ["📅 2025-11-15", "🧩 演讲技巧", "🎯 学术表达", "👤 施凌"],
            "srt_keywords": ["系列3", "演讲技巧"],
            "md_keywords": ["演讲技巧"]
        },
        {
            "num": 4,
            "eyebrow": "KF 系列 · L1",
            "title": "KF L1：矩阵特征值、SVD与正定性",
            "subtitle": "Kalman Filter 的数学基础：特征值分解、奇异值分解、正定矩阵",
            "tags": ["📅 2025-11-22", "🧩 矩阵理论", "📐 SVD", "🎯 KF基础", "👤 施凌"],
            "srt_keywords": ["KF_L1", "系列4"],
            "md_keywords": ["KF_L1", "系列4"]
        },
        {
            "num": 5,
            "eyebrow": "KF 系列 · L2",
            "title": "KF L2：矩阵求逆引理、状态空间与协方差",
            "subtitle": "矩阵求逆引理、状态空间模型、协方差传播与更新",
            "tags": ["📅 2025-11-29", "🧩 矩阵运算", "📐 状态空间", "🎯 KF基础", "👤 施凌"],
            "srt_keywords": ["KF_L2", "系列5"],
            "md_keywords": ["KF_L2", "系列5"]
        },
        {
            "num": 29,
            "eyebrow": "KF 系列 · L15",
            "title": "KF L15：新息过程与卡尔曼滤波",
            "subtitle": "新息过程的定义、正交性与协方差，以及其在卡尔曼滤波中的应用",
            "tags": ["📅 2026-05-17", "🧩 新息过程", "🔄 Kalman Filter", "👤 施凌"],
            "srt_keywords": ["KF_L15", "系列18"],
            "md_keywords": ["KF_L15", "系列18"]
        },
        {
            "num": 30,
            "eyebrow": "特邀请 · 北理工",
            "title": "北理工分享：扩散模型与具身智能",
            "subtitle": "北理工同学分享扩散模型在具身动作生成中的应用",
            "tags": ["📅 2026-06-06", "🧩 扩散模型", "🤖 具身智能", "👤 北理工"],
            "srt_keywords": ["北理工", "系列21"],
            "md_keywords": []
        },
        {
            "num": 31,
            "eyebrow": "组内分享 · E2Map",
            "title": "E2Map：体验与情绪地图",
            "subtitle": "让机器人拥有记忆和情感的建图范式——张健强组内分享",
            "tags": ["📅 2026-06-20", "🧩 情绪地图", "🤖 机器人", "🎯 E2Map"],
            "srt_keywords": ["E2Map", "系列22"],
            "md_keywords": []
        },
    ]
    
    generated = []
    for s in stubs:
        # 找SRT
        srt_path = None
        for kw in s["srt_keywords"]:
            for f in glob.glob(f"{SRT_DIR}/*{kw}*"):
                if f.endswith('.srt') and os.path.getsize(f) > 100:
                    srt_path = f
                    break
            if srt_path:
                break
        
        srt_lines = parse_srt(srt_path) if srt_path else []
        
        # 找MD
        md_text = ""
        for kw in s["md_keywords"]:
            md_path = get_best_md(kw)
            if md_path:
                md_text = read_md(md_path)
                break
        if not md_text:
            # 尝试从course-notes读
            for kw in s["srt_keywords"]:
                notes = read_course_notes(kw)
                if notes:
                    md_text = notes
                    break
        
        fn, html = generate_stub_html(
            s["num"], s["title"], s["eyebrow"], s["subtitle"], 
            s["tags"], srt_lines, md_text
        )
        
        out_path = os.path.join(LESSONS_DIR, fn)
        # 检查是否已有大文件（非stub）
        existing = None
        for f in glob.glob(f"{LESSONS_DIR}/{s['num']:04d}*"):
            existing = f
            break
        
        if existing and os.path.getsize(existing) > 5000:
            print(f"⏭️ [{s['num']}] {s['title']} — 已有完整课程 ({os.path.getsize(existing)//1024}KB)，跳过")
            continue
        
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        size = os.path.getsize(out_path)
        print(f"✅ [{s['num']}] {s['title']} — {size//1024}KB (SRT: {len(srt_lines)}行{'✅' if srt_path else '❌'}, MD: {len(md_text)}字{'✅' if md_text else '❌'})")
        
        generated.append(fn)
    
    print(f"\n🎉 生成了 {len(generated)} 个课程 HTML")
    if generated:
        print("文件列表:")
        for fn in generated:
            print(f"  lessons/{fn}")

if __name__ == '__main__':
    main()
