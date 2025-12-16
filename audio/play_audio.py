import sounddevice as sd
import soundfile as sf

def play_voice(file_path):
    """播放音频文件"""
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()  # 阻塞直到播放完成
