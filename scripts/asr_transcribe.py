#!/usr/bin/env python3
"""
小米 MiMo-V2.5-ASR 语音识别脚本
把视频/音频文件转写为 SRT 字幕 + 纯文本
用法:
  python3 asr_transcribe.py <视频或音频路径> [输出srt路径]

依赖: pip install openai
API Key 通过环境变量 MIMO_API_KEY 设置

模型: mimo-v2.5-asr (专用 ASR 模型)
文档: https://mimo.mi.com/docs/zh-CN/quick-start/usage-guide/audio/Speech-Recognition
"""

import os
import sys
import json
import base64
import math
import subprocess
from openai import OpenAI

# ── 配置 ──────────────────────────────────────────
API_KEY = os.environ.get("MIMO_API_KEY") or os.environ.get("XIAOMI_ASR_API_KEY")
if not API_KEY:
    print("ERROR: 请设置 MIMO_API_KEY 或 XIAOMI_ASR_API_KEY 环境变量")
    print("  export MIMO_API_KEY=\"your-key-here\"")
    sys.exit(1)

client = OpenAI(api_key=API_KEY, base_url="https://api.xiaomimimo.com/v1")

# ASR 专用模型
ASR_MODEL = "mimo-v2.5-asr"

# Base64 大小限制（MiMo 文档：10MB）
MAX_B64_SIZE_MB = 8  # 留余量

# ── 音频处理 ──────────────────────────────────────

def get_audio_duration(path):
    """获取音频时长（秒）"""
    r = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', path],
        capture_output=True, text=True, timeout=30
    )
    return float(r.stdout.strip())


def extract_audio(video_path, output_mp3=None):
    """从视频提取音频为 MP3（16kHz 单声道，码率 16k 以压缩体积）"""
    if output_mp3 is None:
        stem = video_path.rsplit('.', 1)[0]
        output_mp3 = f"{stem}_audio.mp3"
    subprocess.run([
        'ffmpeg', '-y', '-i', video_path,
        '-vn', '-acodec', 'libmp3lame',
        '-ar', '16000', '-ac', '1', '-b:a', '16k',
        output_mp3
    ], capture_output=True, timeout=600)
    return output_mp3


def split_audio_by_size(audio_path, target_size_mb=6):
    """
    把音频切成多段，使每段 base64 后不超过 target_size_mb。
    先获取总时长和总文件大小，按比例估算切割时长。
    """
    total_dur = get_audio_duration(audio_path)
    total_bytes = os.path.getsize(audio_path)
    bytes_per_sec = total_bytes / total_dur if total_dur > 0 else 0

    # base64 会膨胀约 4/3，预留余量
    # 目标：每段 base64 后 ≤ target_size_mb × 0.85
    safe_bytes = target_size_mb * 1024 * 1024 * 0.7  # 原始音频字节数上限
    chunk_dur = safe_bytes / bytes_per_sec if bytes_per_sec > 0 else 120
    chunk_dur = max(30, min(chunk_dur, 600))  # 30s~10min

    stem = audio_path.rsplit('.', 1)[0]
    ext = audio_path.rsplit('.', 1)[-1]

    chunks = []
    start = 0
    while start < total_dur:
        end = min(start + chunk_dur, total_dur)
        chunk_path = f"{stem}_chunk_{int(start)}.{ext}"
        subprocess.run([
            'ffmpeg', '-y', '-i', audio_path,
            '-ss', str(start), '-t', str(end - start),
            '-c', 'copy' if ext == 'mp3' else 'copy',
            chunk_path
        ], capture_output=True, timeout=300)
        # 如果切出来还太大，递归缩小
        actual_mb = os.path.getsize(chunk_path) / (1024 * 1024)
        if actual_mb > target_size_mb:
            os.remove(chunk_path)
            # 更细的切分
            finer = split_audio_by_size(audio_path, target_size_mb * 0.5)
            return finer  # 递归返回更细的结果
        chunks.append((chunk_path, start, end))
        start = end

    return chunks


# ── ASR 调用 ──────────────────────────────────────

def transcribe_segment(audio_path):
    """
    用 MiMo-V2.5-ASR 转写一段音频。
    返回 (完整文本, 原始API响应JSON)
    """
    with open(audio_path, "rb") as f:
        audio_bytes = f.read()
    b64 = base64.b64encode(audio_bytes).decode("utf-8")
    data_url = f"data:audio/mpeg;base64,{b64}"

    try:
        resp = client.chat.completions.create(
            model=ASR_MODEL,
            messages=[{
                "role": "user",
                "content": [{
                    "type": "input_audio",
                    "input_audio": {"data": data_url}
                }]
            }],
            extra_body={"asr_options": {"language": "zh"}}
        )
        text = (resp.choices[0].message.content or "").strip()
        return text, resp

    except Exception as e:
        print(f"  [ERROR] ASR 调用失败: {e}", file=sys.stderr)
        return "", None


# ── SRT 生成 ──────────────────────────────────────

def estimate_timings_from_texts(text_segments, chunk_duration_map):
    """
    把各段的转写文本按时间均匀分配到对应时间窗内。
    chunk_duration_map: [(start_sec, end_sec, text), ...]
    返回 SRT 格式的字幕条目。
    """
    entries = []
    idx = 1

    for start, end, text in chunk_duration_map:
        if not text.strip():
            continue
        dur = end - start
        # 按标点分句
        import re
        sentences = re.split(r'([。！？\n])', text)
        merged = []
        buf = ""
        for part in sentences:
            buf += part
            if part in ('。', '！', '？') or '\n' in part:
                merged.append(buf.strip())
                buf = ""
        if buf.strip():
            merged.append(buf.strip())

        if not merged:
            merged = [text]

        total_chars = sum(len(s) for s in merged)
        if total_chars == 0:
            continue

        char_pos = 0
        for sent in merged:
            sent_len = len(sent)
            t_start = start + (char_pos / total_chars) * dur
            t_end = start + ((char_pos + sent_len) / total_chars) * dur
            # 至少给 2 秒
            if t_end - t_start < 2:
                t_end = t_start + 2

            entries.append((idx, t_start, t_end, sent))
            idx += 1
            char_pos += sent_len

    return entries


def fmt_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_srt(entries, path):
    with open(path, 'w', encoding='utf-8') as f:
        for idx, start, end, text in entries:
            f.write(f"{idx}\n")
            f.write(f"{fmt_srt_time(start)} --> {fmt_srt_time(end)}\n")
            f.write(f"{text}\n\n")


# ── 主流程 ──────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("用法: python3 asr_transcribe.py <视频或音频路径> [输出.srt路径]")
        sys.exit(1)

    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"文件不存在: {input_path}")
        sys.exit(1)

    # 输出路径
    if len(sys.argv) >= 3:
        output_srt = sys.argv[2]
    else:
        stem = os.path.splitext(os.path.basename(input_path))[0]
        output_srt = os.path.join(os.path.dirname(os.path.abspath(input_path)) or '.', f"{stem}.srt")

    print(f"🎬 处理: {input_path}")

    is_video = input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv'))

    # Step 1: 提取音频
    audio_path = input_path
    if is_video:
        print("📢 提取音频(16kHz/单声道/低码率)...")
        audio_path = extract_audio(input_path)
        print(f"    → {audio_path}")

    total_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"   音频大小: {total_mb:.1f} MB")

    # Step 2: 如果音频太大，切分成多段
    segment_files = []
    if total_mb > MAX_B64_SIZE_MB:
        print(f"✂️ 音频超过 {MAX_B64_SIZE_MB}MB 限制，自动切分...")
        chunks = split_audio_by_size(audio_path, target_size_mb=6)
        print(f"   切成 {len(chunks)} 段")
        segment_files = chunks
    else:
        segment_files = [(audio_path, 0, get_audio_duration(audio_path))]

    # Step 3: 逐段 ASR 转写
    chunk_texts = []  # [(start, end, text), ...]
    for i, (seg_path, seg_start, seg_end) in enumerate(segment_files):
        seg_mb = os.path.getsize(seg_path) / (1024 * 1024)
        print(f"🎙️ ASR 转写 第{i+1}/{len(segment_files)}段 ({seg_start:.0f}s-{seg_end:.0f}s, {seg_mb:.1f}MB)...")
        text, _ = transcribe_segment(seg_path)
        if text:
            print(f"   ✓ {len(text)} 字")
        else:
            print(f"   ⚠️ 本段无返回")

        chunk_texts.append((seg_start, seg_end, text))

        # 清理临时文件
        if seg_path != audio_path:
            os.remove(seg_path)

    # Step 4: 生成 SRT
    all_text = "\n".join(t for _, _, t in chunk_texts if t.strip())
    entries = estimate_timings_from_texts(chunk_texts, chunk_texts)

    print(f"\n📝 转写完成！共 {len(all_text)} 字符，{len(entries)} 条字幕")
    if all_text:
        print(f"   开头: {all_text[:120]}...")

    write_srt(entries, output_srt)
    print(f"✅ SRT 已保存: {output_srt}")

    # 同时保存纯文本
    txt_path = output_srt.replace('.srt', '.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(all_text)
    print(f"✅ 纯文本已保存: {txt_path}")

    # 清理提取的音频
    if is_video and audio_path != input_path and os.path.exists(audio_path):
        os.remove(audio_path)

    print("🎉 完成！")


if __name__ == '__main__':
    main()
