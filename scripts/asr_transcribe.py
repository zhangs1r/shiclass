#!/usr/bin/env python3
"""
小米 MiMo ASR 转录脚本
把视频/音频文件转为 SRT 字幕
用法: python3 asr_transcribe.py <video_or_audio_path> [output_srt_path]
"""

import os
import sys
import json
import base64
import tempfile
import time
from openai import OpenAI

API_KEY = os.environ.get("MIMO_API_KEY") or os.environ.get("XIAOMI_ASR_API_KEY")
if not API_KEY:
    print("ERROR: 请设置 MIMO_API_KEY 或 XIAOMI_ASR_API_KEY 环境变量")
    sys.exit(1)

client = OpenAI(
    api_key=API_KEY,
    base_url="https://api.xiaomimimo.com/v1"
)

def extract_audio(video_path, output_mp3=None):
    """从视频提取音频"""
    if output_mp3 is None:
        output_mp3 = video_path.rsplit('.', 1)[0] + '_audio.mp3'
    
    # 用 ffmpeg 提取音频为 MP3，降低采样率以减小文件
    os.system(f'ffmpeg -y -i "{video_path}" -vn -acodec libmp3lame -ar 16000 -ac 1 -b:a 32k "{output_mp3}" 2>/dev/null')
    return output_mp3

def split_audio(audio_path, chunk_duration_s=300):
    """将长音频分割为短片段（默认5分钟一段）"""
    import subprocess
    
    # 获取音频时长
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', 
         '-of', 'default=noprint_wrappers=1:nokey=1', audio_path],
        capture_output=True, text=True
    )
    total_duration = float(result.stdout.strip())
    
    chunks = []
    for start in range(0, int(total_duration), chunk_duration_s):
        chunk_path = f"{audio_path.rsplit('.', 1)[0]}_chunk_{start}.mp3"
        end = min(start + chunk_duration_s, int(total_duration))
        os.system(f'ffmpeg -y -i "{audio_path}" -ss {start} -t {end-start} -c copy "{chunk_path}" 2>/dev/null')
        chunks.append((chunk_path, start, end))
    
    return chunks, total_duration

def transcribe_chunk(audio_path, start_time):
    """用 MiMo API 转录音频片段"""
    with open(audio_path, "rb") as f:
        audio_data = f.read()
    
    audio_b64 = base64.b64encode(audio_data).decode('utf-8')
    data_url = f"data:audio/mp3;base64,{audio_b64}"
    
    try:
        response = client.chat.completions.create(
            model="mimo-v2.5",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an ASR transcription assistant. Today is {time.strftime('%A, %B %d, %Y')}. Your knowledge cutoff date is December 2024."
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_audio",
                            "input_audio": {"data": data_url}
                        },
                        {
                            "type": "text",
                            "text": "请完整、准确地转写这段音频的全部中文对话内容，包括语气词。不需要描述，只需要逐字转写。"
                        }
                    ]
                }
            ],
            max_completion_tokens=4096
        )
        
        text = response.choices[0].message.reasoning_content or response.choices[0].message.content or ""
        
        # 简单分段，每段约30字（后续可完善）
        words_per_segment = 30
        words = list(text)
        segments = []
        for i in range(0, len(words), words_per_segment):
            seg_text = ''.join(words[i:i+words_per_segment])
            # 估算时间戳（基于起始时间和片段内位置）
            seg_start = start_time + (i / len(words)) * 300 if len(words) > 0 else start_time
            seg_end = start_time + min((i + words_per_segment) / len(words) * 300, 300) if len(words) > 0 else start_time + 5
            segments.append({
                "start": seg_start,
                "end": seg_end,
                "text": seg_text
            })
        
        return text, segments
        
    except Exception as e:
        print(f"  [ERROR] 转录失败: {e}")
        return "", []

def format_srt_time(seconds):
    """秒数转 SRT 时间格式"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

def segments_to_srt(segments, output_path):
    """将片段列表转为 SRT 文件"""
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, seg in enumerate(segments, 1):
            f.write(f"{i}\n")
            f.write(f"{format_srt_time(seg['start'])} --> {format_srt_time(seg['end'])}\n")
            f.write(f"{seg['text']}\n\n")
    print(f"SRT 已保存: {output_path}")

def main():
    if len(sys.argv) < 2:
        print("用法: python3 asr_transcribe.py <video_or_audio_path> [output_srt_path]")
        sys.exit(1)
    
    input_path = sys.argv[1]
    if not os.path.exists(input_path):
        print(f"文件不存在: {input_path}")
        sys.exit(1)
    
    # 默认输出路径
    if len(sys.argv) >= 3:
        output_srt = sys.argv[2]
    else:
        basename = os.path.splitext(os.path.basename(input_path))[0]
        output_srt = os.path.join(os.path.dirname(input_path) or '.', f"{basename}.srt")
    
    print(f"🎬 处理: {input_path}")
    
    # 如果是视频，先提取音频
    audio_path = input_path
    is_video = input_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv', '.flv'))
    if is_video:
        print(f"📢 提取音频...")
        audio_path = extract_audio(input_path)
        print(f"   音频: {audio_path}")
    
    # 检查音频文件大小
    audio_size_mb = os.path.getsize(audio_path) / (1024 * 1024)
    print(f"   音频大小: {audio_size_mb:.1f} MB")
    
    all_text = []
    all_segments = []
    
    if audio_size_mb > 45:  # 接近50MB限制，需要切分
        print(f"✂️ 音频较大，切分为5分钟片段...")
        chunks, total_dur = split_audio(audio_path)
        print(f"   共 {len(chunks)} 个片段，总长 {total_dur:.0f}s")
        
        for i, (chunk_path, start, end) in enumerate(chunks):
            chunk_size = os.path.getsize(chunk_path) / (1024 * 1024)
            if chunk_size > 45:
                print(f"   片段 {i+1} 仍较大({chunk_size:.0f}MB)，递归切分...")
                sub_chunks, _ = split_audio(chunk_path, 120)
                for sub_path, s_start, s_end in sub_chunks:
                    print(f"   转录子片段 {s_start}-{s_end}s...")
                    text, segs = transcribe_chunk(sub_path, start + s_start)
                    all_text.append(text)
                    all_segments.extend(segs)
                    os.remove(sub_path)
            else:
                print(f"   转录片段 {i+1}/{len(chunks)} ({start}-{end}s)...")
                text, segs = transcribe_chunk(chunk_path, start)
                all_text.append(text)
                all_segments.extend(segs)
            os.remove(chunk_path)
    else:
        print(f"🎙️ 转录中...")
        text, segs = transcribe_chunk(audio_path, 0)
        all_text.append(text)
        all_segments = segs
    
    # 如果是临时音频文件，清理
    if is_video and audio_path != input_path:
        os.remove(audio_path)
    
    full_text = '\n'.join(all_text)
    print(f"\n📝 转录完成！共 {len(full_text)} 字符")
    print(f"   前100字: {full_text[:100]}...")
    
    # 保存 SRT
    if all_segments:
        segments_to_srt(all_segments, output_srt)
    else:
        # 保存纯文本
        txt_path = output_srt.replace('.srt', '.txt')
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        print(f"纯文本已保存: {txt_path}")
    
    # 同时保存纯文本版本
    txt_path = output_srt.replace('.srt', '.txt')
    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(full_text)

if __name__ == '__main__':
    main()
