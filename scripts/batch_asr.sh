#!/bin/bash
# 批量ASR转写：逐一处理缺少SRT的视频（使用本地 Qwen3-ASR，零费用）
# 用法: bash scripts/batch_asr.sh [视频目录] [输出目录]

set -e
VIDEO_DIR="${1:-videos}"
SRT_DIR="${2:-subtitles}"
LOG_FILE="${SRT_DIR}/batch_asr.log"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================" | tee -a "$LOG_FILE"
echo "批量 ASR 转写开始: $(date)" | tee -a "$LOG_FILE"
echo "引擎: Qwen3-ASR-0.6B（本地CPU，零费用）" | tee -a "$LOG_FILE"
echo "视频目录: $VIDEO_DIR" | tee -a "$LOG_FILE"
echo "输出目录: $SRT_DIR" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"

# 需要转写的视频列表（按时间顺序，短的在前面）
VIDEOS=(
  "20260620_施凌_研讨会系列22_组内张健强分享E2Map"
  "20260606_施凌_研讨会系列21_北理工分享"
  "20260517_施凌_研讨会系列18_KF_L15"
  "20260523_施凌_研讨会系列19_KF_L16"
  "20260530_施凌_研讨会系列20_KF_L17"
  "20260627_施凌_研讨会系列23_KF_L18"
)

TOTAL=${#VIDEOS[@]}
COUNT=0
SUCCESS=0
FAIL=0

for vid in "${VIDEOS[@]}"; do
  COUNT=$((COUNT + 1))
  VIDEO_FILE="${VIDEO_DIR}/${vid}.mp4"
  SRT_FILE="${SRT_DIR}/${vid}.srt"
  
  echo "" | tee -a "$LOG_FILE"
  echo "[$COUNT/$TOTAL] 处理: $vid" | tee -a "$LOG_FILE"
  
  # 检查视频文件
  if [ ! -f "$VIDEO_FILE" ] && [ ! -L "$VIDEO_FILE" ]; then
    echo "  ⚠️ 视频文件不存在: $VIDEO_FILE" | tee -a "$LOG_FILE"
    FAIL=$((FAIL + 1))
    continue
  fi
  
  # 检查是否已有SRT
  if [ -f "$SRT_FILE" ] && [ -s "$SRT_FILE" ]; then
    echo "  ✅ 已有SRT，跳过" | tee -a "$LOG_FILE"
    SUCCESS=$((SUCCESS + 1))
    continue
  fi
  
  # 获取时长
  DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$VIDEO_FILE" 2>/dev/null || echo "0")
  DUR_MIN=$(echo "scale=0; $DUR / 60" | bc 2>/dev/null || echo "?")
  echo "  时长: ${DUR_MIN}分钟" | tee -a "$LOG_FILE"
  
  # 运行本地 Qwen3-ASR 转写（无需网络、无需API Key、无限流限制）
  cd "$(dirname "$SCRIPT_DIR")"
  python3 "$SCRIPT_DIR/qwen_asr_transcribe.py" "$VIDEO_FILE" "$SRT_FILE" 2>&1 | tee -a "$LOG_FILE"
  RET=${PIPESTATUS[0]}
  
  if [ $RET -eq 0 ] && [ -f "$SRT_FILE" ] && [ -s "$SRT_FILE" ]; then
    echo "  ✅ 完成: $vid" | tee -a "$LOG_FILE"
    SUCCESS=$((SUCCESS + 1))
  else
    echo "  ⚠️ 可能部分失败: $vid (exit=$RET)" | tee -a "$LOG_FILE"
    FAIL=$((FAIL + 1))
  fi
  
  # Qwen 是本地运行，无需间隔等待
  if [ $COUNT -lt $TOTAL ]; then
    echo "  处理下一个..." | tee -a "$LOG_FILE"
  fi
done

echo "" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
echo "批量 ASR 转写完成: $(date)" | tee -a "$LOG_FILE"
echo "总计: $TOTAL, 成功: $SUCCESS, 失败: $FAIL" | tee -a "$LOG_FILE"
echo "========================================" | tee -a "$LOG_FILE"
