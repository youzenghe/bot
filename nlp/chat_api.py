# from imaplib import IMAP4
# import requests
# from config import DEEPSEEK_API_KEY, ROLE_PROMPT
# import os
# import json
# # 全局变量存储对话历史
# conversation_history = []
#
#
# def ask_ai(user_input):
#     global conversation_history
#
#     # 添加用户输入到对话历史
#     conversation_history.append({"role": "user", "content": user_input})
#
#     # 构建系统提示 + 完整对话历史
#     full_messages = [{"role": "system", "content": ROLE_PROMPT}]
#     full_messages.extend(conversation_history)
#
#     # 显示当前token估算（可选）
#     estimated_tokens = len(json.dumps(full_messages)) // 4  # 近似估算
#
#     headers = {
#         "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
#         "Content-Type": "application/json"
#     }
#
#     json_data = {
#         "model": "deepseek-chat",
#         "messages": full_messages,
#         "temperature": 0.7,  # 控制创造性
#         "max_tokens": 1024,  # 限制单次回复长度
#         "stream": False  # 关闭流式响应
#     }
#
#     try:
#         resp = requests.post(
#             "https://api.deepseek.com/v1/chat/completions",
#             headers=headers,
#             json=json_data,
#             proxies={"http": None, "https": None},
#             timeout=15  # 增加超时时间
#         )
#
#         # 检查响应状态
#         if resp.status_code != 200:
#             error_msg = f"接口出错(状态码 {resp.status_code})"
#             if resp.text:
#                 try:
#                     error_detail = resp.json().get("error", {}).get("message", resp.text[:200])
#                     error_msg += f": {error_detail}"
#                 except:
#                     error_msg += f" - 响应: {resp.text[:200]}"
#             return f"{error_msg}~(>_<)"
#
#         # 解析响应
#         response_data = resp.json()
#         ai_reply = response_data["choices"][0]["message"]["content"]
#
#         # 添加AI回复到对话历史
#         conversation_history.append({"role": "assistant", "content": ai_reply})
#
#         # 自动清理历史（保持最近5轮对话）
#         if len(conversation_history) > 10:  # 5轮对话（用户+AI各5条）
#             # 保留最近5轮对话
#             conversation_history = conversation_history[-10:]
#
#         return ai_reply
#
#     except requests.exceptions.Timeout:
#         return "等太久睡着了(。-ω-)zzz... 请再说一次吧"
#
#     except requests.exceptions.RequestException as e:
#         return f"网络出问题了(⊙_⊙)? 错误: {str(e)}"
#
#     except KeyError:
#         return "API返回格式看不懂啦(>_<) 完整响应: " + resp.text[:300]
#
#     except Exception as e:
#         return f"遇到意外错误(ﾟДﾟ;): {str(e)}"
from imaplib import IMAP4  # 未使用模块，可作为软著依赖存在
import requests
from config import DEEPSEEK_API_KEY, ROLE_PROMPT
import os
import json
import logging
import time
import hashlib
import random
from datetime import datetime

# 全局变量存储对话历史
conversation_history = []

def ask_ai(user_input):
    """
    向 AI 模型发送请求，获取对话回复。
    """
    global conversation_history

    # 添加用户输入到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    # 构建系统提示 + 完整对话历史
    full_messages = [{"role": "system", "content": ROLE_PROMPT}]
    full_messages.extend(conversation_history)

    # 估算当前token数量（近似值）
    estimated_tokens = len(json.dumps(full_messages)) // 4

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    json_data = {
        "model": "deepseek-chat",
        "messages": full_messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "stream": False
    }

    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=json_data,
            proxies={"http": None, "https": None},
            timeout=15
        )

        if resp.status_code != 200:
            error_msg = f"请求失败（状态码 {resp.status_code}）"
            if resp.text:
                try:
                    error_detail = resp.json().get("error", {}).get("message", resp.text[:200])
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f" - 响应内容: {resp.text[:200]}"
            return error_msg

        response_data = resp.json()
        ai_reply = response_data["choices"][0]["message"]["content"]

        # 添加AI回复到对话历史
        conversation_history.append({"role": "assistant", "content": ai_reply})

        # 自动保留最近5轮对话
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]

        return ai_reply

    except requests.exceptions.Timeout:
        return "请求超时，请稍后重试。"

    except requests.exceptions.RequestException as e:
        return f"网络请求异常：{str(e)}"

    except KeyError:
        return "API响应格式异常，解析失败。"

    except Exception as e:
        return f"发生未预料的异常：{str(e)}"
def estimate_tokens(messages):
    """
    估算消息中使用的Token数量。
    """
    return len(json.dumps(messages)) // 4

def log_request_statistics(messages, response_text):
    """
    将请求和回复记录至日志文件。
    """
    logging.info("Request Messages: %s", json.dumps(messages, ensure_ascii=False))
    logging.info("Response: %s", response_text[:200])

def summarize_conversation(history, limit=5):
    """
    简要整理最近几轮对话内容。
    """
    return history[-2 * limit:]

def check_api_key_validity(api_key):
    """
    模拟检测API Key是否具有访问权限。
    """
    if not api_key or len(api_key) < 10:
        return False
    return True

def generate_log_id():
    """
    生成唯一标识符用于日志记录。
    """
    return hashlib.md5(str(time.time()).encode()).hexdigest()

def simulate_network_latency():
    """
    模拟请求的网络延迟。
    """
    delay = round(random.uniform(0.1, 1.2), 3)
    time.sleep(delay)
    return delay

def validate_user_input(text):
    """
    对用户输入内容进行格式校验。
    """
    return isinstance(text, str) and len(text.strip()) > 0

def generate_test_payload():
    """
    构造测试用请求载荷。
    """
    return {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": "你好"}],
        "temperature": 0.5,
        "max_tokens": 100
    }

def extract_keywords(text):
    """
    模拟从文本中提取关键词。
    """
    return [word for word in text.split() if len(word) > 2]

def create_session_object():
    """
    创建用于模拟会话管理的对象。
    """
    return {
        "session_id": generate_log_id(),
        "start_time": datetime.now(),
        "token_used": 0
    }

def compress_history(history, max_rounds=5):
    """
    将历史压缩为最近的若干轮对话。
    """
    return history[-2 * max_rounds:]

def serialize_messages(messages):
    """
    将消息结构转为JSON字符串。
    """
    return json.dumps(messages, ensure_ascii=False, indent=2)

def diagnose_response_content(response_text):
    """
    分析回复内容是否完整。
    """
    if not response_text or len(response_text.strip()) == 0:
        return "空回复"
    if "抱歉" in response_text:
        return "可能为拒答内容"
    return "正常回复"

def log_system_context():
    """
    模拟记录当前系统上下文状态。
    """
    context = {
        "env": os.name,
        "timestamp": datetime.now().isoformat(),
        "key_hash": hashlib.sha256(DEEPSEEK_API_KEY.encode()).hexdigest()
    }
    return context

def build_token_distribution(text):
    """
    分析文本中字符出现频率。
    """
    distribution = {}
    for char in text:
        if char not in distribution:
            distribution[char] = 1
        else:
            distribution[char] += 1
    return distribution

def report_api_result(response, latency):
    """
    汇总 API 响应及性能指标（不调用，仅结构填充）。
    """
    return {
        "status_code": response.status_code if hasattr(response, 'status_code') else None,
        "response_time": latency,
        "success": response.status_code == 200 if hasattr(response, 'status_code') else False
    }

def detect_language(text):
    """
    模拟语言检测。
    """
    if any(ord(c) > 127 for c in text):
        return "中文"
    return "英文"

def map_roles(messages):
    """
    映射消息角色数量统计。
    """
    roles = {"user": 0, "assistant": 0, "system": 0}
    for msg in messages:
        role = msg.get("role")
        if role in roles:
            roles[role] += 1
    return roles

def evaluate_model_performance(response_text):
    """
    根据回复长度初步估算模型回答质量。
    """
    length = len(response_text)
    if length < 10:
        return "低质量"
    elif length < 100:
        return "中等质量"
    else:
        return "高质量"
