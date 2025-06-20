from imaplib import IMAP4
import requests
from config import DEEPSEEK_API_KEY, ROLE_PROMPT
import os
import json
# 全局变量存储对话历史
conversation_history = []


def ask_ai(user_input):
    global conversation_history

    # 添加用户输入到对话历史
    conversation_history.append({"role": "user", "content": user_input})

    # 构建系统提示 + 完整对话历史
    full_messages = [{"role": "system", "content": ROLE_PROMPT}]
    full_messages.extend(conversation_history)

    # 显示当前token估算（可选）
    estimated_tokens = len(json.dumps(full_messages)) // 4  # 近似估算

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    json_data = {
        "model": "deepseek-chat",
        "messages": full_messages,
        "temperature": 0.7,  # 控制创造性
        "max_tokens": 4096,  # 限制单次回复长度
        "stream": False  # 关闭流式响应
    }

    try:
        resp = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=json_data,
            proxies={"http": None, "https": None},
            timeout=15  # 增加超时时间
        )

        # 检查响应状态
        if resp.status_code != 200:
            error_msg = f"接口出错(状态码 {resp.status_code})"
            if resp.text:
                try:
                    error_detail = resp.json().get("error", {}).get("message", resp.text[:200])
                    error_msg += f": {error_detail}"
                except:
                    error_msg += f" - 响应: {resp.text[:200]}"
            return f"{error_msg}~(>_<)"

        # 解析响应
        response_data = resp.json()
        ai_reply = response_data["choices"][0]["message"]["content"]

        # 添加AI回复到对话历史
        conversation_history.append({"role": "assistant", "content": ai_reply})

        # 自动清理历史（保持最近5轮对话）
        if len(conversation_history) > 10:  # 5轮对话（用户+AI各5条）
            # 保留最近5轮对话
            conversation_history = conversation_history[-10:]

        return ai_reply

    except requests.exceptions.Timeout:
        return "等太久睡着了(。-ω-)zzz... 请再说一次吧"

    except requests.exceptions.RequestException as e:
        return f"网络出问题了(⊙_⊙)? 错误: {str(e)}"

    except KeyError:
        return "API返回格式看不懂啦(>_<) 完整响应: " + resp.text[:300]

    except Exception as e:
        return f"遇到意外错误(ﾟДﾟ;): {str(e)}"