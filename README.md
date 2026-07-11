# ShiClass 施老师大课堂

## 项目简介
施老师（施凌）研讨会系列课程的学习网站，基于 teach skill 构建。
包含 Kalman Filter、演讲技巧、学术表达等系列课程的交互式 HTML 讲义。

## 课程来源
视频 + 板书 PDF 来自江南大学云盘，定期更新。

## 目录结构
```
shiclass/
├── index.html              # 主页
├── .gitignore              # 忽略视频/PDF等大文件
├── data/
│   └── course-catalog.js   # 课程目录数据
├── lessons/
│   └── assets/             # CSS/JS 资源
├── videos/                 # 视频（gitignored）
├── pdfs/                   # 板书 PDF（gitignored）
├── pdf-md/                 # PDF 转 MD（gitignored）
├── subtitles/              # SRT 字幕（gitignored）
├── course-notes/           # 教材版笔记（gitignored）
├── scripts/
│   ├── asr_transcribe.py   # 小米 MiMo ASR 转写
│   └── setup_env.sh        # 环境变量配置
└── .github/
    └── workflows/
        └── deploy.yml      # GitHub Pages 部署
```
