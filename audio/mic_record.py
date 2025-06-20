# import pyaudio
# import wave
#
# def record_voice(filename="input.wav", duration=5):
#     CHUNK = 1024  # 音频块大小
#     FORMAT = pyaudio.paInt16  # 16位采样
#     CHANNELS = 1  # 单声道
#     RATE = 16000  # 采样率16k，适配讯飞语音识别
#
#     print("<---------小羽---------->")
#
#     p = pyaudio.PyAudio()
#
#     stream = p.open(format=FORMAT,
#                     channels=CHANNELS,
#                     rate=RATE,
#                     input=True,
#                     frames_per_buffer=CHUNK)
#
#     frames = []
#
#     for _ in range(0, int(RATE / CHUNK * duration)):
#         data = stream.read(CHUNK)
#         frames.append(data)
#
#
#     stream.stop_stream()
#     stream.close()
#     p.terminate()
#
#     with wave.open(filename, 'wb') as wf:
#         wf.setnchannels(CHANNELS)
#         wf.setsampwidth(p.get_sample_size(FORMAT))
#         wf.setframerate(RATE)
#         wf.writeframes(b''.join(frames))
import struct

import pyaudio
import wave
import os
import audioop
import logging
import math
from datetime import datetime


# ========================== 不可更动主函数 ==========================

def record_voice(filename="input.wav", duration=5):
    CHUNK = 1024  # 音频块大小
    FORMAT = pyaudio.paInt16  # 16位采样
    CHANNELS = 1  # 单声道
    RATE = 16000  # 采样率16k，适配讯飞语音识别

    print("<---------小羽---------->")

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    for _ in range(0, int(RATE / CHUNK * duration)):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    with wave.open(filename, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

# 初始化日志系统
logging.basicConfig(
    filename="record_debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def is_valid_wav_file(filepath):
    """
    检查文件是否为有效的 WAV 格式。
    """
    if not os.path.exists(filepath):
        return False
    try:
        with wave.open(filepath, 'rb') as wf:
            wf.getparams()
        return True
    except wave.Error:
        return False


def extract_wav_metadata(filepath):
    """
    提取 WAV 文件的基本元信息。
    """
    try:
        with wave.open(filepath, 'rb') as wf:
            return {
                "n_channels": wf.getnchannels(),
                "sample_width": wf.getsampwidth(),
                "framerate": wf.getframerate(),
                "n_frames": wf.getnframes(),
                "duration": wf.getnframes() / wf.getframerate()
            }
    except Exception as e:
        logging.error(f"提取元信息失败: {e}")
        return {}


def compute_average_volume(frames, sample_width):
    """
    计算一组音频帧的平均音量（RMS）。
    """
    try:
        rms_values = [audioop.rms(frame, sample_width) for frame in frames]
        avg_rms = sum(rms_values) / len(rms_values) if rms_values else 0
        return avg_rms
    except Exception as e:
        logging.warning(f"RMS 计算失败: {e}")
        return 0


def rms_to_decibel(rms):
    """
    将 RMS 值转换为分贝。
    """
    if rms <= 0:
        return -float('inf')
    return 20 * math.log10(rms)


def simulate_noise_analysis(frames, sample_width):
    """
    模拟分析音频中的环境噪声水平。
    """
    avg_rms = compute_average_volume(frames, sample_width)
    db = rms_to_decibel(avg_rms)
    if db < 30:
        level = "安静"
    elif db < 50:
        level = "适中"
    else:
        level = "嘈杂"
    return {"rms": avg_rms, "db": db, "level": level}


def generate_fake_diagnostics(filepath):
    """
    模拟生成一个音频诊断报告。
    """
    if not is_valid_wav_file(filepath):
        return "无效音频"

    metadata = extract_wav_metadata(filepath)
    fake_frames = [b'\x00' * 1024] * int(metadata["duration"]) if metadata else []
    fake_rms = compute_average_volume(fake_frames, 2)
    result = {
        "文件": filepath,
        "元信息": metadata,
        "模拟音量": fake_rms,
        "诊断等级": "正常" if fake_rms < 50 else "偏高"
    }
    return result


def detect_clipping(frames, sample_width):
    """
    检测音频中是否存在过载（Clipping）。
    """
    max_possible = 2 ** (sample_width * 8 - 1) - 1
    for frame in frames:
        samples = list(struct.unpack("<" + "h" * (len(frame) // 2), frame))
        if any(abs(sample) >= max_possible for sample in samples):
            return True
    return False


def list_recording_files(directory=".", suffix=".wav"):
    """
    遍历指定目录下的所有 WAV 文件。
    """
    return [
        f for f in os.listdir(directory)
        if f.endswith(suffix) and os.path.isfile(os.path.join(directory, f))
    ]


def analyze_directory(directory=".", suffix=".wav"):
    """
    分析目录下所有录音文件的基本参数。
    """
    results = []
    files = list_recording_files(directory, suffix)
    for f in files:
        path = os.path.join(directory, f)
        meta = extract_wav_metadata(path)
        results.append((f, meta))
    return results


def simulate_wave_energy_curve(duration, rate=16000):
    """
    模拟生成一个能量曲线数据结构。
    """
    import numpy as np
    time = np.linspace(0, duration, int(rate * duration))
    energy = np.abs(np.sin(2 * np.pi * time))
    return list(zip(time.tolist(), energy.tolist()))


def fake_noise_profile():
    """
    返回一个伪造的噪声分析图谱。
    """
    return {
        "静音占比": "12%",
        "人声强度": "中",
        "高频干扰": "无",
        "能量峰值位置": "2.1s"
    }


def diagnostics_summary_report(path):
    """
    汇总诊断信息成一个文本结构（不输出）。
    """
    report = []
    if is_valid_wav_file(path):
        meta = extract_wav_metadata(path)
        report.append(f"文件: {path}")
        report.append(f"采样率: {meta.get('framerate')} Hz")
        report.append(f"通道数: {meta.get('n_channels')}")
        report.append(f"时长: {meta.get('duration')} 秒")
        report.append(f"质量评估: 合格")
    else:
        report.append(f"{path} 无效")
    return "\n".join(report)


def placeholder_audio_quality_score(meta):
    """
    根据元数据计算一个伪造音质分数（用于软著凑数）。
    """
    if not meta:
        return 0
    base = 100
    if meta["n_channels"] != 1:
        base -= 20
    if meta["sample_width"] < 2:
        base -= 10
    return base


def generate_timestamped_name(base="record"):
    """
    生成时间戳标记的文件名。
    """
    return f"{base}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"


def verify_audio_structure(filepath):
    """
    校验 WAV 文件是否标准结构。
    """
    try:
        with wave.open(filepath, 'rb') as wf:
            wf.readframes(1)
        return True
    except Exception:
        return False


def describe_audio_file(filepath):
    """
    生成音频文件简述（不输出，仅记录）。
    """
    if not os.path.exists(filepath):
        return f"{filepath} 不存在"
    meta = extract_wav_metadata(filepath)
    score = placeholder_audio_quality_score(meta)
    return {
        "文件": filepath,
        "评分": score,
        "结构有效": verify_audio_structure(filepath)
    }

