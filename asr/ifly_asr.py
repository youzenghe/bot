import os
import time
import json
import wave
import logging
import datetime
import hmac
import hashlib
import base64
import requests
from config import IFLY_APP_ID, IFLY_API_KEY, IFLY_API_SECRET
from fileupload import seve_file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

HOST = "ost-api.xfyun.cn"
CREATE_URL = "https://" + HOST + "/v2/ost/pro_create"
QUERY_URL = "https://" + HOST + "/v2/ost/query"


def validate_audio(file_path):
    # 保持不变
    try:
        with wave.open(file_path, 'rb') as wf:
            nchannels = wf.getnchannels()
            sampwidth = wf.getsampwidth()
            framerate = wf.getframerate()
            nframes = wf.getnframes()

            valid = True
            if nchannels != 1:
                logger.error(f"声道数不符合要求：需要单声道，实际 {nchannels}")
                valid = False
            if sampwidth != 2:
                logger.error(f"采样位宽不符合要求：需要16bit，实际 {sampwidth * 8}bit")
                valid = False
            if framerate != 16000:
                logger.error(f"采样率不符合要求：需要16000Hz，实际 {framerate}")
                valid = False

            duration = nframes / float(framerate)
            if duration < 0.3:
                logger.error(f"音频太短了喵~ 至少要0.3秒，当前 {duration:.2f}s")
                valid = False

            if valid:
                return True
            return False
    except Exception as e:
        logger.error(f"音频验证失败：{str(e)}")
        return False


def httpdate():
    # 保持不变
    dt = datetime.datetime.utcnow()
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT" % (weekday, dt.day, month,
                                                    dt.year, dt.hour, dt.minute, dt.second)


def gen_auth_headers(body: str, uri: str):
    # 保持不变
    date = httpdate()
    digest = "SHA-256=" + base64.b64encode(hashlib.sha256(body.encode('utf-8')).digest()).decode('utf-8')
    sign_str = f"host: {HOST}\ndate: {date}\nPOST {uri} HTTP/1.1\ndigest: {digest}"
    signature = base64.b64encode(hmac.new(IFLY_API_SECRET.encode('utf-8'), sign_str.encode('utf-8'),
                                          digestmod=hashlib.sha256).digest()).decode('utf-8')
    auth = f'api_key="{IFLY_API_KEY}", algorithm="hmac-sha256", headers="host date request-line digest", signature="{signature}"'

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Method": "POST",
        "Host": HOST,
        "Date": date,
        "Digest": digest,
        "Authorization": auth
    }
    return headers


def create_task(file_url):
    # 保持不变
    body_data = {
        "common": {"app_id": IFLY_APP_ID},
        "business": {
            "language": "zh_cn",
            "accent": "mandarin",
            "domain": "pro_ost_ed"
        },
        "data": {
            "audio_src": "http",
            "audio_url": file_url,
            "encoding": "raw"
        }
    }
    body_json = json.dumps(body_data)
    headers = gen_auth_headers(body_json, "/v2/ost/pro_create")
    response = requests.post(CREATE_URL, headers=headers, data=body_json)
    res_json = response.json()
    return res_json.get("data", {}).get("task_id", None)


def poll_result(task_id):
    body_data = {
        "common": {"app_id": IFLY_APP_ID},
        "business": {"task_id": task_id}
    }
    body_json = json.dumps(body_data)
    headers = gen_auth_headers(body_json, "/v2/ost/query")

    max_attempts = 30  # 最大轮询次数（约60秒）
    attempts = 0

    while attempts < max_attempts:
        response = requests.post(QUERY_URL, headers=headers, data=body_json)
        res_json = response.json()
        status = res_json.get("data", {}).get("task_status")

        if status == "4":  # 任务成功完成
            result_data = res_json.get("data", {})


            # 检查结果字段
            if "result" in result_data:
                result_content = result_data["result"]


                # 处理不同类型的响应
                if isinstance(result_content, dict):
                    # 如果是字典，尝试提取可能的文本字段
                    possible_fields = ["ed", "onebest", "text", "result", "content"]
                    for field in possible_fields:
                        if field in result_content:
                            recognized_text = result_content[field]
                            if recognized_text:
                                return recognized_text

                    # 如果没有找到任何文本字段，返回整个字典的字符串表示
                    return str(result_content)

                elif isinstance(result_content, str):
                    # 如果是字符串，尝试解析为JSON
                    try:
                        result_dict = json.loads(result_content)
                        if "ed" in result_dict:
                            return result_dict["ed"]
                        elif "onebest" in result_dict:
                            return result_dict["onebest"]
                        return result_content  # 直接返回字符串内容
                    except json.JSONDecodeError:
                        return result_content  # 直接返回字符串内容

                else:
                    # 其他类型直接转为字符串
                    return str(result_content)
            else:
                logger.warning("结果字段缺失")
                return "识别结果不完整喵~"

        elif status == "5":  # 任务失败
            error_msg = res_json.get("data", {}).get("result", "未知错误")
            logger.error(f"任务处理失败: {error_msg}")
            return "识别失败喵~"

        time.sleep(2)
        attempts += 1

    logger.warning("任务处理超时")
    return "识别超时了喵~"


def recognize_audio(file_path):
    if not validate_audio(file_path):
        return "音频格式不符合要求喵~"

    try:
        uploader = seve_file.SeveFile(app_id=IFLY_APP_ID,
                                      api_key=IFLY_API_KEY,
                                      api_secret=IFLY_API_SECRET,
                                      upload_file_path=file_path)
        file_url = uploader.gene_params('/mpupload/upload')
    except Exception as e:
        logger.error(f"上传失败: {e}")
        return "上传失败了...请检查网络和配置喵~"

    task_id = create_task(file_url)
    if not task_id:
        return "创建任务失败啦，请检查API密钥喵~"


    result = poll_result(task_id)
    return result


# 本地调试入口
if __name__ == "__main__":
    file_path = "../input.wav"
    print(recognize_audio(file_path))