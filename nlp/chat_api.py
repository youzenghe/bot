import requests
from config import DEEPSEEK_API_KEY, ROLE_PROMPT

# 全局变量存储对话历史
conversation_history = []

def ask_ai(user_input):
    """向 AI 模型发送请求，获取对话回复。"""
    global conversation_history

    # 添加用户输入到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    # 构建系统提示 + 完整对话历史
    full_messages = [{"role": "system", "content": ROLE_PROMPT}]
    full_messages.extend(conversation_history)

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
