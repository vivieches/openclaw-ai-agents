---
name: feishu-tts
description: |
  飞书语音消息技能。将文字转换为语音(OPUS格式)并发送到飞书群聊。
  支持多种中文语音，自动转换为飞书要求的格式(单声道16kHz OPUS)。
---

# Feishu TTS 语音技能

将文字转换为语音并发送到飞书，支持直接播放。

## Features

- 🎙️ 多音色选择（男女声、不同风格）
- 🔄 自动转换 OPUS 格式（飞书要求）
- ⏱️ 自动计算语音时长
- 📱 飞书原生语音消息，可直接播放

## Requirements

```bash
# Edge TTS
pip install edge-tts

# FFmpeg（用于格式转换）
sudo apt-get install ffmpeg
```

## Voice Options

### 推荐日常工作使用

| 语音 | 性别 | 风格 | 适用场景 |
|:---|:---:|:---|:---|
| `zh-CN-XiaoxiaoNeural` | 女 | 温暖、专业 | ⭐ **日常工作推荐** |
| `zh-CN-YunyangNeural` | 男 | 专业、可靠 | 正式通知 |
| `zh-CN-YunxiNeural` | 男 | 活泼、阳光 | 轻松内容 |
| `zh-CN-XiaoyiNeural` | 女 | 活泼、卡通 | 趣味内容 |

### 方言特色
- `zh-CN-liaoning-XiaobeiNeural` - 辽宁话（幽默）
- `zh-CN-shaanxi-XiaoniNeural` - 陕西话（明亮）

## Usage

### 方法1：命令行快速使用

```bash
# 进入技能目录
cd ~/.openclaw/workspace/skills/feishu-tts

# 生成语音文件
python3 send_voice.py "你好老大，任务已完成"

# 输出：/tmp/feishu_tts_temp.opus（飞书可用）
```

### 方法2：Python API

```python
import sys
sys.path.insert(0, '~/.openclaw/workspace/skills/feishu-tts')
from send_voice import text_to_opus

# 生成语音
opus_file, duration = text_to_opus(
    "你好，这是测试语音",
    voice="zh-CN-XiaoxiaoNeural"  # 温暖女声
)

print(f"语音文件: {opus_file}")
print(f"时长: {duration}秒")
```

### 方法3：在 Agent 中调用

```python
# 让 Agent 生成语音并报告
sessions_spawn(agentId="creator", task="使用 feishu-tts 技能生成语音：'任务完成'")
```

## Output Files

| 文件 | 格式 | 用途 |
|:---|:---|:---|
| `/tmp/feishu_tts_temp.opus` | OPUS | 飞书直接上传使用 |
| `/tmp/feishu_tts_temp.mp3` | MP3 | 备用/预览 |

## 飞书发送方式

当前版本生成 OPUS 文件后，可以通过以下方式发送到飞书：

1. **手动上传**：在飞书聊天窗口点击"+"→"文件"→选择 OPUS 文件
2. **API 发送**（需配置 Bot Token）：使用 OpenClaw message 工具

## Technical Details

### 飞书语音要求
- **格式**: OPUS
- **采样率**: 16000 Hz
- **声道**: 单声道 (mono)
- **最大大小**: 30 MB

### 转换流程
```
文字 → Edge TTS (MP3) → FFmpeg → OPUS (16kHz mono)
```

## Examples

### 日常汇报
```bash
python3 send_voice.py "老大，今日数据已更新，请查看报表"
# 使用 Xiaoxiao 温暖女声
```

### 紧急通知
```bash
VOICE=zh-CN-YunyangNeural python3 send_voice.py "系统告警，请立即处理"
# 使用 Yunyang 专业男声
```

### 轻松提醒
```bash
VOICE=zh-CN-YunxiNeural python3 send_voice.py "该休息啦，喝杯水吧"
# 使用 Yunxi 活泼男声
```

## Troubleshooting

### 问题：TTS 生成失败
**解决**: 检查 edge-tts 是否安装
```bash
pip install edge-tts
```

### 问题：OPUS 转换失败
**解决**: 检查 FFmpeg 是否安装
```bash
sudo apt-get install ffmpeg
```

### 问题：飞书无法播放
**解决**: 确保是 OPUS 格式，不是 MP3。飞书只支持 OPUS。

## Future Enhancements

- [ ] 自动上传到飞书并发送
- [ ] 支持长文本自动分段
- [ ] 支持语速调节
- [ ] 支持情感风格选择
