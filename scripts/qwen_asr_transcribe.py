#!/usr/bin/env python3
"""
Qwen3-ASR 本地语音识别脚本（替代 MiMo API）
把视频/音频文件转写为 SRT 字幕 + 纯文本
全部在本地 CPU/GPU 运行，无需 API Key，无调用费用。

用法:
  python3 qwen_asr_transcribe.py <视频或音频路径> [输出srt路径]

依赖:
  pip install qwen-asr torch

模型:
  Qwen3-ASR-0.6B（本地 ~1.88GB，2GB 显存即可跑）
  或 Qwen3-ASR-1.7B（更准但需要 4-6GB）

首次运行会自动从 ModelScope 下载模型（国内速度快）。
模型缓存位置: ~/models/qwen3-asr/
"""

import os
import sys
import json
import math
import re
import time
import subprocess
import argparse
import torch
from qwen_asr import Qwen3ASRModel

# ── 配置 ──────────────────────────────────────────

# 模型路径（直接从本地缓存加载，不需要联网）
# 已经通过 ModelScope 下载到本地：
#   /home/zjq/models/qwen3-asr/models/Qwen--Qwen3-ASR-0.6B/snapshots/master/
MODEL_PATH = "/home/zjq/models/qwen3-asr/models/Qwen--Qwen3-ASR-0.6B/snapshots/master"
# 备用：如果上面的路径不存在，自动从 ModelScope 下载
MODEL_NAME = "Qwen/Qwen3-ASR-0.6B"
MODEL_CACHE_DIR = os.path.expanduser("~/models/qwen3-asr")

# 音频处理参数
AUDIO_SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1

# Qwen3-ASR-0.6B 最长支持 ~20 分钟音频
MAX_AUDIO_MINUTES = 20

# ── 全局模型（避免重复加载） ──────────────────────
_model_instance = None


def get_model():
    """获取或加载模型（单例）"""
    global _model_instance
    if _model_instance is not None:
        return _model_instance

    print("🔄 加载 Qwen3-ASR-0.6B 模型（首次加载约 10-30 秒）...")
    t0 = time.time()

    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if device == "cuda" else torch.float32

    print(f"   设备: {device.upper()}, 精度: {dtype}")

    # 优先从本地缓存加载（不用联网）
    model_path = MODEL_PATH
    if not os.path.exists(model_path):
        print(f"   本地缓存不存在，从 ModelScope 下载...")
        try:
            from modelscope import snapshot_download
            model_path = snapshot_download(MODEL_NAME, cache_dir=MODEL_CACHE_DIR)
            print(f"   下载完成: {model_path}")
        except Exception as e:
            print(f"   ❌ ModelScope 下载失败: {e}")
            print(f"   请手动运行:")
            print(f"   pip install modelscope")
            print(f"   python3 -c \"from modelscope import snapshot_download; snapshot_download('{MODEL_NAME}', cache_dir='{MODEL_CACHE_DIR}')\"")
            sys.exit(1)

    print(f"   模型路径: {model_path}")
    _model_instance = Qwen3ASRModel.from_pretrained(
        model_path,
        dtype=dtype,
        device_map=device,
        max_new_tokens=512,
    )

    t1 = time.time()
    print(f"   ✅ 模型加载完成 ({t1 - t0:.1f}s)")
    return _model_instance


# ── 音频处理 ──────────────────────────────────────


def extract_audio(video_path, output_wav=None):
    """
    从视频提取音频为 16kHz 单声道 WAV。
    Qwen3-ASR 原生支持 WAV，不需要 MP3 压缩。
    """
    if output_wav is None:
        stem = video_path.rsplit('.', 1)[0]
        output_wav = f"{stem}_audio.wav"

    subprocess.run([
        'ffmpeg', '-y', '-i', video_path,
        '-vn',
        '-ar', str(AUDIO_SAMPLE_RATE),
        '-ac', str(AUDIO_CHANNELS),
        '-sample_fmt', 's16',
        output_wav
    ], capture_output=True, timeout=600)
    return output_wav


def get_audio_duration(path):
    """获取音频时长（秒）"""
    r = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
         '-of', 'default=noprint_wrappers=1:nokey=1', path],
        capture_output=True, text=True, timeout=30
    )
    return float(r.stdout.strip())


def split_audio(input_path, max_duration_s=900):
    """
    把长音频切成多段（Qwen-ASR 原生支持约 20 分钟）。
    每段最长 max_duration_s 秒。
    返回 [(chunk_path, start_sec, end_sec), ...]
    """
    total_dur = get_audio_duration(input_path)
    if total_dur <= max_duration_s:
        return [(input_path, 0, total_dur)]

    stem = input_path.rsplit('.', 1)[0]
    ext = input_path.rsplit('.', 1)[-1]
    chunks = []

    start = 0
    while start < total_dur:
        end = min(start + max_duration_s, total_dur)
        chunk_path = f"{stem}_chunk_{int(start)}.{ext}"
        subprocess.run([
            'ffmpeg', '-y', '-i', input_path,
            '-ss', str(start), '-t', str(end - start),
            '-c', 'copy',
            chunk_path
        ], capture_output=True, timeout=300)
        chunks.append((chunk_path, start, end))
        start = end

    return chunks


# ── ASR 转写 ──────────────────────────────────────


def transcribe_file(audio_path, language=None):
    """
    用 Qwen3-ASR 转写一段音频文件。
    返回 [(start_sec, end_sec, text), ...]
    """
    model = get_model()

    dur = get_audio_duration(audio_path)

    print(f"   🎙️ 识别中 ({dur:.0f}s)...", end=" ", flush=True)
    t0 = time.time()

    kwargs = {}
    if language:
        kwargs["language"] = language

    results = model.transcribe(audio=audio_path, **kwargs)

    t1 = time.time()
    if results and len(results) > 0:
        text = results[0].text
        lang = results[0].language if hasattr(results[0], 'language') else '?'
        print(f"✓ {len(text)} 字 [{lang}] ({t1 - t0:.1f}s)")
        return [(0, dur, text)]
    else:
        print(f"⚠️ 无返回 ({t1 - t0:.1f}s)")
        return [(0, dur, "")]


# ── SRT 生成（带时间戳估计） ──────────────────────


def fmt_srt_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    ms = int((sec % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def estimate_timings(text, total_duration):
    """
    把转写文本按标点分句后均匀分配到时间轴上。
    返回 [(idx, start_sec, end_sec, sentence), ...]
    """
    if not text.strip():
        return []

    # 按标点或换行分句
    sentences = re.split(r'([。！？\n])', text)
    merged = []
    buf = ""
    for part in sentences:
        buf += part
        if part in ('。', '！', '？') or '\n' in part:
            s = buf.strip()
            if s:
                merged.append(s)
            buf = ""
    if buf.strip():
        merged.append(buf.strip())

    if not merged:
        merged = [text]

    total_chars = sum(len(s) for s in merged)
    if total_chars == 0:
        return []

    entries = []
    char_pos = 0
    for idx, sent in enumerate(merged, 1):
        sent_len = len(sent)
        t_start = (char_pos / total_chars) * total_duration
        t_end = ((char_pos + sent_len) / total_chars) * total_duration
        if t_end - t_start < 2.0:
            t_end = t_start + 2.0
        entries.append((idx, t_start, min(t_end, total_duration), sent))
        char_pos += sent_len

    return entries


def write_srt(entries, path):
    with open(path, 'w', encoding='utf-8') as f:
        for idx, start, end, text in entries:
            f.write(f"{idx}\n")
            f.write(f"{fmt_srt_time(start)} --> {fmt_srt_time(end)}\n")
            f.write(f"{text}\n\n")


# ── 主流程 ──────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(description="Qwen3-ASR 本地语音转文字")
    parser.add_argument("input", help="音频或视频文件路径")
    parser.add_argument("output", nargs="?", help="输出 SRT 文件路径（可选）")
    parser.add_argument("--language", "-l", default=None,
                        help="指定语言（如 Chinese, English），默认自动检测")
    parser.add_argument("--model", default="0.6B",
                        choices=["0.6B", "1.7B"],
                        help="模型大小（默认 0.6B，1.7B 需要更多内存）")
    args = parser.parse_args()

    input_path = args.input
    if not os.path.exists(input_path):
        print(f"❌ 文件不存在: {input_path}")
        sys.exit(1)

    # 输出路径
    if args.output:
        output_srt = args.output
    else:
        stem = os.path.splitext(os.path.basename(input_path))[0]
        output_srt = os.path.join(
            os.path.dirname(os.path.abspath(input_path)) or '.',
            f"{stem}.srt"
        )

    print(f"🎬 Qwen3-ASR 本地转写: {input_path}")

    is_video = input_path.lower().endswith(
        ('.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm'))

    # Step 1: 提取音频（如果是视频）
    audio_path = input_path
    if is_video:
        print("📢 提取音频 (16kHz/单声道)...")
        audio_path = extract_audio(input_path)
        print(f"    → {audio_path}")
    else:
        # 非 WAV 格式先转 WAV（Qwen-ASR 推荐）
        if not input_path.lower().endswith('.wav'):
            print("📢 转码为 WAV 格式...")
            stem = input_path.rsplit('.', 1)[0]
            wav_path = f"{stem}.wav"
            subprocess.run([
                'ffmpeg', '-y', '-i', input_path,
                '-ar', str(AUDIO_SAMPLE_RATE),
                '-ac', str(AUDIO_CHANNELS),
                '-sample_fmt', 's16',
                wav_path
            ], capture_output=True, timeout=600)
            audio_path = wav_path
            print(f"    → {audio_path}")

    total_mb = os.path.getsize(audio_path) / (1024 * 1024)
    total_duration = get_audio_duration(audio_path)
    print(f"   时长: {total_duration:.0f}s | 大小: {total_mb:.1f}MB")

    # Step 2: 切分长音频
    max_duration_s = MAX_AUDIO_MINUTES * 60
    chunk_files = split_audio(audio_path, max_duration_s)

    if len(chunk_files) > 1:
        print(f"✂️ 音频超过 {MAX_AUDIO_MINUTES} 分钟，切为 {len(chunk_files)} 段")

    # Step 3: 逐段转写
    chunk_results = []
    for i, (chunk_path, seg_start, seg_end) in enumerate(chunk_files):
        if len(chunk_files) > 1:
            print(f"   第 {i+1}/{len(chunk_files)} 段 ({seg_start:.0f}s-{seg_end:.0f}s)")

        texts = transcribe_file(chunk_path, language=args.language)

        for (_, _, text) in texts:
            chunk_results.append((seg_start, seg_end, text))

        # 清理临时切分文件
        if chunk_path != audio_path:
            os.remove(chunk_path)

    # Step 4: 生成 SRT
    all_text = "\n".join(t for _, _, t in chunk_results if t.strip())

    if all_text:
        entries = []
        for start, end, text in chunk_results:
            if text.strip():
                sub_entries = estimate_timings(text, end - start)
                # 调整时间偏移
                adjusted = []
                for idx, s, e, t in sub_entries:
                    adjusted.append((len(entries) + idx, s + start, e + start, t))
                entries.extend(adjusted)

        print(f"\n📝 转写完成！共 {len(all_text)} 字符，{len(entries)} 条字幕")
        if all_text:
            print(f"   开头: {all_text[:150]}...")

        write_srt(entries, output_srt)
        print(f"✅ SRT 已保存: {output_srt}")

        # 同时保存纯文本
        txt_path = output_srt.replace('.srt', '.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(all_text)
        print(f"✅ 纯文本已保存: {txt_path}")
    else:
        print("⚠️ 转写结果为空，未生成文件")

    # 清理提取的临时音频
    if is_video and audio_path != input_path and os.path.exists(audio_path):
        os.remove(audio_path)

    print("🎉 完成！（零费用，本地运行）")


if __name__ == '__main__':
    main()
