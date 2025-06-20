# mic_record.py 可爱版录音模块ฅ(>ω<*ฅ)
import pyaudio
import wave

def record_voice(filename="input.wav", duration=5):
    CHUNK = 1024  # 音频块大小
    FORMAT = pyaudio.paInt16  # 16位采样
    CHANNELS = 1  # 单声道
    RATE = 16000  # 采样率16k，适配讯飞语音识别

    print("小羽:")

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
