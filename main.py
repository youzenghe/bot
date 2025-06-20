from audio.mic_record import record_voice
from asr.ifly_asr import recognize_audio
from nlp.chat_api import ask_ai
from tts.sovits import text_to_voice
from audio.play_audio import play_voice

if __name__ == "__main__":
    i = 0
    while True:
        #开始录音
        record_voice("input.wav", duration=5)
        print(f"第{i}次录音结束")
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
