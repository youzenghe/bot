import sounddevice as sd
import soundfile as sf

def play_voice(file_path):
    data, samplerate = sf.read(file_path)
    sd.play(data, samplerate)
    sd.wait()  # 关键：阻塞直到播放完成