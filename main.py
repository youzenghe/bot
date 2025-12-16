from audio.mic_record import record_voice
from asr.baidu_asr import recognize_audio
from nlp.chat_api import ask_ai
from tts.sovits import text_to_voice
from audio.play_audio import play_voice

if __name__ == "__main__":
    while True:
        # 开始录音
        record_voice("input.wav", duration=5)

        # 录音识别
        user_text = recognize_audio("input.wav")

        # AI回复
        reply = ask_ai(user_text)
        print("小识：" + reply)

        # 合成语音
        text_to_voice(reply, "output.wav")

        # 播放语音
        play_voice("output.wav")
