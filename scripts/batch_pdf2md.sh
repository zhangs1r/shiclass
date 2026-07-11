#!/bin/bash
# 批量 PDF → MD 转换 (MinerU)
# 用法: bash scripts/batch_pdf2md.sh

set -e
SCRIPT=/home/zjq/.hermes/skills/mineru-pdf-reader/scripts/convert_pdf.py
PDF_DIR="pdfs"
OUT_DIR="pdf-md"
LOG_FILE="pdf-md/convert_all.log"
FAIL_LOG="pdf-md/convert_fail.log"

mkdir -p "$OUT_DIR"
rm -f "$FAIL_LOG"
source /home/zjq/.hermes/.env

echo "========================================" | tee -a "$LOG_FILE"
echo "批量 PDF→MD 转换开始: $(date)" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

TOTAL=$(ls "$PDF_DIR"/*.pdf 2>/dev/null | wc -l)
COUNT=0
SUCCESS=0
FAIL=0

for pdf in "$PDF_DIR"/*.pdf; do
  COUNT=$((COUNT + 1))
  base=$(basename "$pdf" .pdf)
  out_dir="$OUT_DIR/$base"
  
  echo "" | tee -a "$LOG_FILE"
  echo "[$COUNT/$TOTAL] $base" | tee -a "$LOG_FILE"
  
  # 跳过已转换的
  if [ -f "$out_dir/document.md" ]; then
    echo "  ✅ 已有 document.md，跳过" | tee -a "$LOG_FILE"
    SUCCESS=$((SUCCESS + 1))
    continue
  fi
  
  # 转换
  unset http_proxy https_proxy
  python3 "$SCRIPT" "$PWD/$pdf" "$PWD/$out_dir" 2>&1 | tee -a "$LOG_FILE"
  RET=${PIPESTATUS[0]}
  
  if [ $RET -eq 0 ] && [ -f "$out_dir/document.md" ]; then
    echo "  ✅ 完成: $base" | tee -a "$LOG_FILE"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "  ⚠️ 失败: $base" | tee -a "$LOG_FILE"
    echo "$pdf" >> "$FAIL_LOG"
    FAIL=$((FAIL + 1))
  fi
  
  # 等待一下避免API压力
  sleep 3
done

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "转换完成: $(date)" | tee -a "$LOG_FILE"
echo "总计: $TOTAL, 成功: $SUCCESS, 失败: $FAIL" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
