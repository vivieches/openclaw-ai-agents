---
name: vetmew-consultation
description: 专业宠物（猫、狗及异宠）多轮医疗问诊。基于 VetMew 3.0 API 提供症状分析与诊断建议。
license: MIT
compatibility: 需要 Python 3.12+ 及有效的 VetMew API 凭据。
metadata:
  author: AI-Consultant
  version: "1.1"
---

# VetMew 宠物问诊 Skill

## 简介
这是一个接入了 VetMew 开放平台 (VetMew Open Platform) 的专业宠物问诊技能。它能够处理复杂的宠物档案（涵盖犬、猫及龙猫、豚鼠等异宠），并通过 HMAC-SHA256 安全认证调用深度学习模型，为宠物提供专业的医疗咨询建议。

## Setup & Configuration

本技能需要 VetMew 开放平台的 API 凭据才能运行。

### 1. 获取凭据
请前往 [VetMew 开放平台](https://open.vetmew.com/) 申请 `API_KEY` 和 `API_SECRET`。

### 2. 配置环境变量
在技能安装目录下创建一个 `.env` 文件（或编辑自动生成的文件），内容模板如下：

```env
# VetMew API 凭据
VETMEW_API_KEY=你的_API_KEY
VETMEW_API_SECRET=你的_API_SECRET
```

> **安全提示**：请勿将包含真实密钥的 `.env` 文件提交到版本控制系统。

## Usage

> **注意**：执行以下脚本前，请确保当前工作目录 (CWD) 为脚本所在的根目录。

### 1. 宠物医疗问诊
`python3 scripts/consultation.py --name <name> --breed <breed> --pet_type <pet_type> --birth <YYYY-MM-DD> --gender <1|2> --fertility <1|2> --msg <question> [--conversation_id <id>] [--thinking]`

### 2. 养宠知识问答 (轻量)
`python3 scripts/free_chat.py --msg <question> [--online] [--conversation_id <id>]`

### 3. 异宠医疗问诊
`python3 scripts/exotic_consultation.py --name <name> --breed <breed> --pet_type 3 --gender <1|2> --msg <question> [--conversation_id <id>] [--thinking]`

## Input (输入参数)

### 1. 医疗问诊参数 (仅适用于 `consultation.py`)
- `--name`: **宠物昵称** (String)。宠物在家庭中的常用名。
- `--breed`: **品种名称** (String)。必须是标准中文品种名，如“金毛”、“布偶猫”。
- `--pet_type`: **宠物类型** (String)。"1" 代表猫，"2" 代表狗。必须与品种所属物种一致。
- `--birth`: **生日** (YYYY-MM-DD)。用于计算宠物的生理阶段。
- `--gender`: **性别** (Integer)。1 为公，2 为母。
- `--fertility`: **绝育情况** (Integer)。1 为未绝育，2 为已绝育。
- `--thinking`: **深度思考开关** (Flag)。开启后 API 会返回更详尽的推理逻辑（Deep Thinking）。

### 2. 异宠问诊参数 (仅适用于 `exotic_consultation.py`)
- `--name`: **宠物昵称** (String)。
- `--breed`: **品种名称** (String)。如“龙猫”、“豚鼠”、“松鼠”。
- `--pet_type`: **宠物类型** (String)。必须固定为 "3"。
- `--gender`: **性别** (Integer)。1 为公，2 为母。
- `--thinking`: **深度思考开关** (Flag)。

### 3. 知识问答参数 (仅适用于 `free_chat.py`)
- `--msg`: **用户提问** (String)。长度上限 200 字符。
- `--online`: **联网搜索开关** (Flag)。开启后 AI 会获取最新联网资讯进行回答。

### 3. 通用交互信息
- `--msg`: **用户提问/症状描述** (String)。请尽可能详细描述宠物的精神、饮食、排泄等异常表现。
- `--conversation_id`: **会话 ID** (Optional)。在多轮对话中，Agent 应自动提取并传递此 ID 以维持上下文。**注意：必须确保传入的 ID 与当前触发的脚本路径（医疗 vs 问答）一致。**

## Steps (工作流程)

1. **意图识别**: 当用户表达出对宠物健康的担忧或寻求专业建议时，触发此技能。
2. **槽位映射 (Session Slotting)**: Agent 必须维护三个独立的槽位以隔离会话：
    - `VETMEW_MEDICAL_SESSION`: 存储来自 `consultation.py` 的 ID。
    - `VETMEW_EXOTIC_SESSION`: 存储来自 `exotic_consultation.py` 的 ID。
    - `VETMEW_CHAT_SESSION`: 存储来自 `free_chat.py` 的 ID。
3. **参数收集**: Agent 检查必选参数。如果用户未提及品种或年龄（针对犬猫），Agent 必须主动发起追问。
4. **安全认证**: 脚本自动读取环境变量中的 `VETMEW_API_KEY` 和 `VETMEW_API_SECRET` 生成 HMAC 签名。
5. **流式消费**: 实时解析来自 VetMew 的 SSE 数据块，提取 `msg` 内容并即时渲染。
6. **状态捕获**: 脚本在正常结束时会输出 `CONVERSATION_ID: <id>`。
    - 若执行的是 `consultation.py`，必须将 ID 更新至 `VETMEW_MEDICAL_SESSION`。
    - 若执行的是 `exotic_consultation.py`，必须将 ID 更新至 `VETMEW_EXOTIC_SESSION`。
    - 若执行的是 `free_chat.py`，必须将 ID 更新至 `VETMEW_CHAT_SESSION`。
7. **异常回退**: 若脚本返回“会话无效或隔离冲突”错误，Agent 必须清除对应槽位的旧 ID 并提示用户重新发起会话。

## Output (输出示例)

### 诊断中 (流式 Markdown)
> "根据大黄（金毛，8个月，未绝育）的呕吐频率，初步判断可能存在急性胃炎风险。建议：
> 1. 禁食 12 小时...
> 2. 观察精神状态..."

### 诊断结束 (状态标识)
> "--------------------"
> "CONVERSATION_ID: v2-chat-session-88291"

## Guardrails (护栏)

- **品种映射限制**: 若输入品种无法在官方库中找到，脚本将返回错误并要求用户更正。
- **物种匹配校验**: 系统将校验品种是否属于指定的 `pet_type`。禁止跨物种问诊。
- **安全红线**: 严禁在输出中包含任何 API 秘钥或原始签名字符串。
- **医疗免责**: 输出内容仅供参考，危急情况下请务必引导用户前往线下宠物医院。

## Technical Dependencies
- Python 3.12+
- `requests`, `python-dotenv`
- `consultation.py` (主程序)
- `breed_manager.py` (品种管理)
