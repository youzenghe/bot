import requests

def text_to_voice(text, output_path="output.wav"):
    url = "http://127.0.0.1:9880"

    payload = {
        "text": text,
        "text_language": "zh",
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                f.write(response.content)
        else:
            print(f"(请求失败，状态码是 {response.status_code}，内容是 {response.text}")
    except Exception as e:
        print(f"(撞到墙了……错误是：{e}")
