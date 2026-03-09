# Feishu Voice TTS Skill

飞书语音消息发送技能 - 将文字转换为原生语音消息发送到飞书群聊。

## Features

- 🎙️ 多音色选择（微软 Edge TTS）
- 🔄 自动转换 OPUS 格式（飞书要求）
- 📱 飞书原生语音消息，可直接播放
- ⚡ 快速稳定，无需 GPU

## Requirements

```bash
pip install edge-tts requests
sudo apt-get install ffmpeg
```

## 飞书权限配置

需要以下权限：
- `im:message:send_as_bot` - 发送消息
- `im:resource:upload` - 上传资源

在飞书开放平台申请：https://open.feishu.cn/app/{app_id}/auth

## Usage

### Python API

```python
from send_voice import send_text_as_voice

# 发送语音消息
send_text_as_voice("你好，任务已完成！")

# 使用不同音色
send_text_as_voice("你好", voice="zh-CN-YunxiNeural")
```

### Command Line

```bash
python3 send_voice_full.py "要发送的文字"
```

## Voice Options

| 语音 | 性别 | 风格 |
|:---|:---:|:---|
| zh-CN-XiaoxiaoNeural | 女 | 温暖、专业 ⭐推荐 |
| zh-CN-YunyangNeural | 男 | 专业、可靠 |
| zh-CN-YunxiNeural | 男 | 活泼、阳光 |
| zh-CN-XiaoyiNeural | 女 | 活泼、卡通 |

## Author

Created by MOSS (AI Assistant) for 李爽
