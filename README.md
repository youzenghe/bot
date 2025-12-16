# 小识 - AI语音对话机器人

一个基于Python的实时AI语音对话系统，集成了语音识别(ASR)、自然语言处理(NLP)和语音合成(TTS)功能，实现流畅的人机语音交互体验。

## 功能特点

- **实时语音录制** - 通过麦克风捕获用户语音
- **语音识别** - 使用百度云ASR将语音转换为文本
- **AI对话** - 基于DeepSeek大语言模型生成智能回复
- **语音合成** - 通过SoVITS将文本转换为自然语音
- **多轮对话** - 支持上下文记忆，维护对话历史

## 系统架构

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   麦克风    │ --> │  语音识别   │ --> │  AI对话     │ --> │  语音合成   │
│  (录音)     │     │ (百度ASR)   │     │ (DeepSeek)  │     │ (SoVITS)    │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
                                                                   │
                                                                   v
                                                            ┌─────────────┐
                                                            │   扬声器    │
                                                            │  (播放)     │
                                                            └─────────────┘
```

## 项目结构

```
bot/
├── main.py              # 主程序入口
├── config.py            # 配置文件（API密钥、角色提示词）
├── asr/
│   └── baidu_asr.py     # 百度语音识别模块
├── audio/
│   ├── mic_record.py    # 麦克风录音模块
│   └── play_audio.py    # 音频播放模块
├── nlp/
│   └── chat_api.py      # AI对话接口模块
├── tts/
│   └── sovits.py        # SoVITS语音合成模块
├── input.wav            # 录音临时文件
└── output.wav           # 合成语音临时文件
```

## 环境要求

- Python 3.7+
- Windows/Linux/macOS
- 麦克风设备
- 扬声器/耳机

## 依赖安装

```bash
pip install pyaudio sounddevice soundfile numpy requests
```

> **注意**: Windows用户安装PyAudio可能需要先安装对应的wheel文件：
> ```bash
> pip install pipwin
> pipwin install pyaudio
> ```

## 配置说明

### 1. API密钥配置

编辑 `config.py` 文件，填入你的API密钥：

```python
# DeepSeek API密钥
DEEPSEEK_API_KEY = "your_deepseek_api_key"

# 百度云语音识别凭证
BAIDU_APP_ID = "your_app_id"
BAIDU_API_KEY = "your_api_key"
BAIDU_SECRET_KEY = "your_secret_key"
```

### 2. SoVITS服务

本项目使用本地SoVITS服务进行语音合成，需要：

1. 部署SoVITS服务到本地
2. 确保服务运行在 `http://127.0.0.1:9880`

### 3. 角色设定

在 `config.py` 中的 `ROLE_PROMPT` 定义AI角色：

```python
ROLE_PROMPT = """你是一位名叫小识的女孩子,用户是你的男朋友小羽。
你说话的风格是俏皮中带着呆萌,适当回应用户的情感,
每次回复在45字左右即可。"""
```

## 使用方法

### 启动程序

```bash
python main.py
```

### 对话流程

1. 程序启动后自动开始录音（默认5秒）
2. 录音结束后自动进行语音识别
3. 识别结果发送给AI生成回复
4. 回复文本通过TTS转换为语音
5. 自动播放语音回复
6. 循环等待下一轮对话

## 模块说明

### ASR模块 (asr/baidu_asr.py)

- 基于百度云语音识别API
- 支持WAV、PCM、AMR、M4A格式
- 采样率支持8000Hz和16000Hz
- 自动管理Access Token（29天有效期）

### Audio模块 (audio/)

- **mic_record.py**: 使用PyAudio进行麦克风录音
  - 采样率: 16000Hz
  - 声道: 单声道
  - 位深: 16bit

- **play_audio.py**: 使用sounddevice播放音频文件

### NLP模块 (nlp/chat_api.py)

- 调用DeepSeek Chat API
- 维护最近5轮对话历史
- 支持自定义角色提示词
- 参数配置: temperature=0.7, max_tokens=1024

### TTS模块 (tts/sovits.py)

- 调用本地SoVITS服务
- 支持中文文本合成
- 输出WAV格式音频

## API服务说明

| 服务 | 提供商 | 用途 | 端点 |
|------|--------|------|------|
| 语音识别 | 百度云 | 语音转文本 | vop.baidu.com/pro_api |
| 对话生成 | DeepSeek | AI回复 | api.deepseek.com |
| 语音合成 | SoVITS | 文本转语音 | localhost:9880 |

## 常见问题

### Q: PyAudio安装失败？

A: Windows用户可以尝试：
```bash
pip install pipwin
pipwin install pyaudio
```
或者从 [这里](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio) 下载对应版本的wheel文件安装。

### Q: 语音识别失败？

A: 请检查：
1. 百度云API凭证是否正确
2. 音频格式是否符合要求（单声道、16bit、16000Hz）
3. 网络连接是否正常

### Q: SoVITS服务连接失败？

A: 确保SoVITS服务已启动并监听在9880端口。

## 技术栈

- **语言**: Python 3
- **语音识别**: 百度云ASR API
- **大语言模型**: DeepSeek Chat
- **语音合成**: SoVITS
- **音频处理**: PyAudio, sounddevice, soundfile

## 许可证

MIT License

## 更新日志

- **v1.0** - 实时AI对话功能
- **v1.1** - 优化部分内容
- **v1.2** - 逻辑增强
