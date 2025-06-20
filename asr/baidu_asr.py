import os
import time
import json
import wave
import base64
import requests
from config import BAIDU_APP_ID, BAIDU_API_KEY, BAIDU_SECRET_KEY, BAIDU_TOKEN_URL, BAIDU_ASR_URL



class BaiduASR:
    def __init__(self):
        self.app_id = BAIDU_APP_ID
        self.api_key = BAIDU_API_KEY
        self.secret_key = BAIDU_SECRET_KEY
        self.token_url = BAIDU_TOKEN_URL
        self.asr_url = BAIDU_ASR_URL
        self.access_token = None
        self.token_expires_time = 0

    def get_access_token(self):
        """获取百度API访问令牌"""
        current_time = time.time()

        # 如果token未过期，直接返回
        if self.access_token and current_time < self.token_expires_time:
            return self.access_token

        # 获取新的access_token
        params = {
            'grant_type': 'client_credentials',
            'client_id': self.api_key,
            'client_secret': self.secret_key
        }

        try:
            response = requests.post(self.token_url, params=params, timeout=10)
            result = response.json()

            if 'access_token' in result:
                self.access_token = result['access_token']
                # token有效期一般为30天，这里设置为29天后过期
                self.token_expires_time = current_time + result.get('expires_in', 2592000) - 86400
                return self.access_token
            else:
                return None

        except Exception as e:
            return None

    def validate_audio(self, file_path):
        """验证音频文件格式"""
        try:
            with wave.open(file_path, 'rb') as wf:
                nchannels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                framerate = wf.getframerate()
                nframes = wf.getnframes()

                valid = True
                if nchannels != 1:
                    valid = False
                if sampwidth != 2:
                    valid = False

                # 百度API只支持特定采样率
                supported_rates = [8000, 16000]
                if framerate not in supported_rates:
                    valid = False

                duration = nframes / float(framerate)
                if duration < 0.3:
                    valid = False
                elif duration > 60:
                    valid = False

                if valid:
                    return True, framerate, duration
                return False, None, None

        except Exception as e:
            return False, None, None

    def recognize_audio(self, file_path):
        """语音识别主函数"""
        # 验证音频格式
        is_valid, sample_rate, duration = self.validate_audio(file_path)
        if not is_valid:
            return "音频格式不符合要求喵~"

        # 获取access_token
        access_token = self.get_access_token()
        if not access_token:
            return "获取访问令牌失败，请检查API密钥喵~"

        # 读取音频文件并编码
        try:
            with open(file_path, 'rb') as f:
                audio_data = f.read()

            # base64编码
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')

            # 确定音频格式
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext == '.wav':
                format_type = 'wav'
            elif file_ext == '.pcm':
                format_type = 'pcm'
            elif file_ext == '.amr':
                format_type = 'amr'
            elif file_ext == '.m4a':
                format_type = 'm4a'
            else:
                format_type = 'wav'  # 默认wav格式

            # 修复：确保采样率为整数，并根据百度API要求进行规范化
            if sample_rate == 16000:
                api_rate = 16000
            elif sample_rate == 8000:
                api_rate = 8000
            else:
                # 如果采样率不是标准值，使用最接近的标准值
                api_rate = 16000 if sample_rate > 12000 else 8000

            # 构建请求数据 - 注意：百度ASR使用POST请求，参数放在body中
            data = {
                'format': format_type,
                'rate': api_rate,  # 确保使用标准采样率
                'channel': 1,
                'speech': audio_base64,
                'len': len(audio_data),
                'cuid': 'python_client_v3',  # 修改cuid
                'token': access_token,
                'dev_pid':80001  # 改为普通话(纯中文识别)，如果还有问题可以尝试15372
            }


            # 设置请求头
            headers = {
                'Content-Type': 'application/json; charset=utf-8'
            }

            # 发送识别请求 - 注意：所有参数都在body中，不使用URL参数
            response = requests.post(
                self.asr_url,
                data=json.dumps(data),
                headers=headers,
                timeout=30
            )

            # 打印响应状态码和内容，用于调试
            result = response.json()

            # 处理识别结果
            if result.get('err_no') == 0:
                # 识别成功
                if 'result' in result and result['result']:
                    recognized_text = ''.join(result['result'])
                    print(f"{recognized_text}")
                    return recognized_text
                else:
                    return "识别不到内容喵~"
            else:
                # 识别失败
                error_msg = result.get('err_msg', '未知错误')

                # 提供更详细的错误信息
                if result.get('err_no') == 3311:
                    return f"采样率参数错误喵~ 请确保音频采样率为8000Hz或16000Hz"
                elif result.get('err_no') == 3300:
                    return f"输入参数不正确喵~ 请检查音频格式"
                elif result.get('err_no') == 3301:
                    return f"音频质量问题喵~ 请检查音频文件是否损坏"
                else:
                    return f"识别失败喵~ 错误信息: {error_msg}"

        except FileNotFoundError:
            return "找不到音频文件喵~"
        except requests.exceptions.RequestException as e:
            return "网络请求失败喵~"
        except Exception as e:
            return "识别过程发生异常喵~"


# 全局ASR实例
_asr_instance = None


def get_asr_instance():
    """获取ASR实例（单例模式）"""
    global _asr_instance
    if _asr_instance is None:
        _asr_instance = BaiduASR()
    return _asr_instance


def validate_audio(file_path):
    """验证音频文件格式（保持原有函数名）"""
    asr = get_asr_instance()
    is_valid, _, _ = asr.validate_audio(file_path)
    return is_valid


def recognize_audio(file_path):
    """语音识别函数（保持原有函数名和功能）"""
    asr = get_asr_instance()
    return asr.recognize_audio(file_path)


# 本地调试入口
if __name__ == "__main__":
    file_path = "../input.wav"
    recognize_audio(file_path)