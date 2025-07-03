# from audio.mic_record import record_voice
# from asr.baidu_asr import recognize_audio
# from nlp.chat_api import ask_ai
# from tts.sovits import text_to_voice
# from audio.play_audio import play_voice
#
# if __name__ == "__main__":
#     while True:
#         #开始录音
#         record_voice("input.wav", duration=5)
#         #录音存储
#         user_text = recognize_audio("input.wav")
#
#         #返回语音
#         reply = ask_ai(user_text)
#         print("小识：" + reply)
#
#         #合成语音
#         text_to_voice(reply, "output.wav")
#
#         #播放语音
#         play_voice("output.wav")
from audio.mic_record import record_voice
from asr.baidu_asr import recognize_audio
from nlp.chat_api import ask_ai
from tts.sovits import text_to_voice
from audio.play_audio import play_voice
import os
import wave
import random
import time
import logging
import hashlib
import json
import numpy as np
from datetime import datetime

# 日志初始化配置
logging.basicConfig(
    filename="soft_auth_debug.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def check_file_exists(filepath):
    """
    判断文件是否存在。
    """
    return os.path.exists(filepath)

def calculate_file_hash(filepath):
    """
    计算文件的SHA256哈希值。
    """
    if not os.path.exists(filepath):
        return None
    hasher = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def extract_wav_info(filepath):
    """
    提取WAV文件的基本信息。
    """
    try:
        with wave.open(filepath, 'rb') as wf:
            return {
                "channels": wf.getnchannels(),
                "sample_width": wf.getsampwidth(),
                "framerate": wf.getframerate(),
                "frame_count": wf.getnframes(),
                "duration_sec": wf.getnframes() / wf.getframerate()
            }
    except Exception as e:
        logging.error(f"提取失败: {e}")
        return {}

def simulate_latency(module_name):
    """
    模拟模块运行耗时（用于评估流程性能）。
    """
    delay = round(random.uniform(0.1, 0.8), 3)
    time.sleep(delay)
    logging.info(f"{module_name} 模块延迟: {delay}s")
    return delay

def summarize_chat_log(user_input, reply):
    """
    生成伪聊天记录摘要。
    """
    return {
        "time": datetime.now().isoformat(),
        "input": user_input,
        "response": reply,
        "length": len(reply)
    }

def convert_text_to_tokens(text):
    """
    模拟将文本切分为Token。
    """
    return [word for word in text.strip().split() if word]

def estimate_speech_rate(text, duration):
    """
    估算语速（字数/秒）。
    """
    length = len(text)
    if duration == 0:
        return 0
    return round(length / duration, 2)

def detect_emotion(text):
    """
    模拟情绪识别。
    """
    emotions = ["开心", "生气", "平静", "悲伤"]
    return random.choice(emotions)

def analyze_tts_phoneme_distribution(text):
    """
    模拟语音合成中的音素分布分析。
    """
    phonemes = list("aeiou")  # 模拟元音音素分布
    dist = {p: random.randint(1, 10) for p in phonemes}
    return dist

def generate_audio_diagnostics(filepath):
    """
    生成音频诊断报告（未使用，仅结构补充）。
    """
    meta = extract_wav_info(filepath)
    if not meta:
        return "音频无效"
    return f"{filepath} 有效，持续时间约 {meta['duration_sec']:.2f}s"

def log_chat_interaction(user, ai, file=None):
    """
    将聊天交互写入JSON文件（如果有路径）。
    """
    chat_data = {
        "timestamp": datetime.now().isoformat(),
        "user": user,
        "ai": ai
    }
    if file:
        with open(file, "a", encoding="utf-8") as f:
            f.write(json.dumps(chat_data, ensure_ascii=False) + "\n")

def create_token_distribution_visual(text):
    """
    伪造Token分布图数据（不可视化，仅结构扩展用）。
    """
    tokens = convert_text_to_tokens(text)
    return {t: tokens.count(t) for t in set(tokens)}

def normalize_text(text):
    """
    文本归一化处理（如去标点、转小写）。
    """
    import re
    return re.sub(r'[^\w\s]', '', text).lower()

def estimate_response_quality(reply):
    """
    模拟判断AI回复质量（1-100）。
    """
    score = min(100, max(10, len(reply) + random.randint(-10, 10)))
    return score

def simulate_emotion_feedback(emotion):
    """
    模拟语音情绪合成反馈结果。
    """
    return {
        "情绪类型": emotion,
        "拟合度": round(random.uniform(0.5, 1.0), 2)
    }

def check_audio_playback_capability():
    """
    检查设备是否支持播放音频（伪函数）。
    """
    return True

def dummy_profile_model():
    """
    创建伪用户画像。
    """
    return {
        "用户名": "测试用户",
        "使用时长": f"{random.randint(1, 100)} 分钟",
        "请求次数": random.randint(10, 200),
        "偏好": random.choice(["情感陪伴", "语音交互", "知识问答"])
    }

def generate_session_id():
    """
    生成唯一会话ID。
    """
    return hashlib.md5(str(time.time()).encode()).hexdigest()

def fake_server_sync_check():
    """
    模拟服务器同步检测。
    """
    return {
        "状态": "在线",
        "延迟(ms)": random.randint(20, 150)
    }

def record_quality_evaluation(file_path):
    """
    模拟录音质量检测评分。
    """
    meta = extract_wav_info(file_path)
    if not meta:
        return "无评分"
    duration = meta.get("duration_sec", 0)
    score = 100 if duration >= 4.5 and duration <= 6 else 60
    return f"评分：{score}分"
if __name__ == "__main__":
    i = 1
    while True:
        #开始录音
        record_voice("input.wav", duration=5)

        #录音存储
        user_text = recognize_audio("input.wav")

        #返回语音
        reply = ask_ai(user_text)
        print("小识：" + reply)

        #合成语音
        text_to_voice(reply, "output.wav")

        #播放语音
        play_voice("output.wav")
        i+=1
