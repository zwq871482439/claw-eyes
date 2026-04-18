# 👀 虾看 (Claw Eyes)

> 让纯文字推理模型"借一双眼睛" — 跨平台剪贴板图片读取 + 视觉分析
>
> Let text-only reasoning models "borrow eyes" — Cross-platform clipboard image reader + vision analysis

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-green)](https://github.com/zwq871482439/claw-eyes)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org)

---

## TL;DR / 一句话说明

截图，说"看图"，AI 帮你分析图片内容。API 直连优先（稳定），MCP 备用。

Screenshot → say "看图" → AI analyzes it. API-first (reliable), MCP fallback.

**支持平台 / Platforms**: Windows ✅ | macOS ✅ | Linux ✅

**兼容 / Compatible with**: WorkBuddy · OpenClaw · QClaw · 任何基于 Claw 的 AI 助手

---

## Prerequisites / 前置要求

| Requirement | Install / 安装 |
|---|---|
| **Python 3.8+** | [python.org](https://www.python.org/downloads/) |
| **Pillow** | `pip install Pillow` |

> ⚠️ 这两个是必须的。没有 Python 或 Pillow，Claw Eyes 无法运行。
>
> ⚠️ These are required. Without Python or Pillow, Claw Eyes won't work.

---

## Features / 特性一览

- 📋 跨平台剪贴板图片读取（Windows / macOS / Linux）
- 🔍 双模式：API 直连主模式（稳定）+ MCP 备用模式
- 🌐 Top 10 供应商预配置：智谱 / 硅基流动 / 阿里 / 火山 / 百度 / OpenAI / Gemini / Groq / Mistral / Together
- 🆓 免费可用：智谱 `glm-4.6v-flash`、硅基流动 `Qwen2.5-VL` 等
- 💬 自定义提示词：支持带特定问题分析图片
- 🌐 中英双语触发 / Bilingual triggers

---

<a id="english"></a>

## 🇺🇸 English Documentation

### What is this?

Most AI assistants run on text-only reasoning models (GLM-5.1, DeepSeek-R1, etc.) that cannot process images. **Claw Eyes** solves this by letting your AI assistant "borrow eyes" from a vision model:

1. You take a screenshot and say "look at this"
2. Claw Eyes sends the image to a vision model (e.g., free `glm-4.6v-flash`)
3. The vision model converts the image into natural language
4. The description feeds back into the main reasoning model as text

**Key insight:** Your main model stays as the flagship reasoning model, while getting multimodal input on demand. No model switching needed. Already using a provider? Reuse the same API key.

### How It Works

```
Screenshot → Clipboard → Save to disk → Direct API analyzes (primary) → Result
                                           ↓ (if API fails)
                                           MCP analyzes (backup) → Result
                                           ↓ (if MCP also fails)
                                           Guide user to set up
```

- **Direct API mode (primary)** — Calls your provider's vision API directly. More reliable, bypasses MCP instability.
- **MCP mode (backup)** — Uses whatever vision MCP tool is in your session. Zero config when it works.
- **Custom prompts** — `python claw-eyes.py analyze "Diagnose this error"` for targeted analysis.

### Analysis Modes

| Mode | Method | Priority | Config Required | Notes |
|------|--------|----------|-----------------|-------|
| **Mode A** | Direct API | ✅ Primary | API key + URL + model | Most reliable |
| **Mode B** | MCP Tool | Backup | None (auto-detect) | Zero config when available |
| **Mode C** | None | — | — | Guides user to set up |

### Installation

#### Option 1: Let your AI install it (Recommended)

Send this message to your AI assistant:

```
Please install this skill: https://github.com/zwq871482439/claw-eyes
Clone it to my skill directory, then run the post-install setup.
```

#### Option 2: Git clone manually

```bash
# WorkBuddy
git clone https://github.com/zwq871482439/claw-eyes.git ~/.workbuddy/skills/clipboard-reader

# OpenClaw — adjust path to your skill directory
# git clone https://github.com/zwq871482439/claw-eyes.git ~/.openclaw/skills/clipboard-reader
```

#### Post-install Setup

After installing, the AI will walk you through:

1. ✅ **Check Python** (3.8+ required)
2. ✅ **Check Pillow** (auto-installs if missing)
3. ✅ **Confirm save path** (default: `<TEMP>/claw-eyes/clipboard.png`)
4. ✅ **Choose provider** → auto-configure URL + model
5. ✅ **Validate API** key
6. ✅ **Optional: enable MCP backup mode**

### Configuration

All env vars use the `CLAW_EYES_` prefix.

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAW_EYES_SAVE_PATH` | `<TEMP>/claw-eyes/clipboard.png` | Image save path |
| `CLAW_EYES_API_KEY` | (none) | Vision API key |
| `CLAW_EYES_API_URL` | (none) | API endpoint — must match your provider |
| `CLAW_EYES_VISION_MODEL` | (none) | Vision model — must match your provider |
| `CLAW_EYES_MCP_SERVER` | auto-detect | MCP server name (backup mode) |
| `CLAW_EYES_MCP_TOOL` | auto-detect | MCP tool name (backup mode) |
| `CLAW_EYES_LANG` | `zh` | Default prompt language |

> ⚠️ **`API_URL` and `VISION_MODEL` have NO defaults.** They must be set together based on your provider.

### Compatible API Providers (Top 10)

#### 🇨🇳 Domestic / 国内

| Provider | API URL | Free Vision Model | Get Key |
|----------|---------|-------------------|---------|
| **智谱 Zhipu** ⭐ | `open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4.6v-flash` (128K) | [open.bigmodel.cn](https://open.bigmodel.cn) |
| **SiliconFlow** | `api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | [siliconflow.cn](https://siliconflow.cn) |
| **DashScope** | `dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `qwen-vl-max` | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) |
| **Volcengine** | `ark.cn-beijing.volces.com/api/v3/chat/completions` | `doubao-1.5-vision-pro-32k` | [console.volcengine.com/ark](https://console.volcengine.com/ark) |
| **Qianfan** | `qianfan.baidubce.com/v2/chat/completions` | `ernie-4.5-vl` | [console.bce.baidu.com/qianfan](https://console.bce.baidu.com/qianfan) |

#### 🌍 International / 国际

| Provider | API URL | Free Vision Model | Get Key |
|----------|---------|-------------------|---------|
| **OpenAI** | `api.openai.com/v1/chat/completions` | None (paid: `gpt-4o`) | [platform.openai.com](https://platform.openai.com) |
| **Gemini** | `generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-2.0-flash` | [aistudio.google.com](https://aistudio.google.com) |
| **Groq** | `api.groq.com/openai/v1/chat/completions` | `llama-3.2-90b-vision-preview` | [console.groq.com](https://console.groq.com) |
| **Mistral** | `api.mistral.ai/v1/chat/completions` | `pixtral-12b-2409` | [console.mistral.ai](https://console.mistral.ai) |
| **Together AI** | `api.together.xyz/v1/chat/completions` | `meta-llama/Llama-3.2-90B-Vision-Instruct` | [api.together.ai](https://api.together.ai) |

**Local / 本地部署：** Ollama → `API_URL=http://localhost:11434/v1/chat/completions`, `API_KEY=ollama`, `VISION_MODEL=llava`

### Usage

1. Take a screenshot: `Win + Shift + S` (Windows) / `Cmd + Shift + 4` (macOS)
2. Say one of the trigger phrases:
   - 🇨🇳 "看图"、"看看这个"、"帮我看图"、"截图看一下"
   - 🇺🇸 "look at this"、"check screenshot"、"analyze image"
3. The AI reads your clipboard and analyzes the image!

---

<a id="chinese"></a>

## 🇨🇳 中文文档

### 这是什么？

大多数 AI 助手运行在纯文字推理模型上（GLM-5.1、DeepSeek-R1 等），无法处理图片。**Claw Eyes** 让你的 AI 助手从一个视觉模型"借一双眼睛"：

1. 你截图后说"看图"
2. Claw Eyes 把图片发给视觉模型（如免费的 `glm-4.6v-flash`）
3. 视觉模型把图片内容转成自然语言描述
4. 描述回传给主推理模型作为文字输入

**核心理念：** 主模型仍然是旗舰推理模型，按需获得多模态输入。不需要切换模型。已经在用某个供应商？复用同一个 API key。

### 工作原理

```
截图 → 剪贴板 → 保存到本地 → 直连 API 分析（主模式）→ 结果
                                   ↓ （API 失败时）
                                   MCP 分析（备用）→ 结果
                                   ↓ （MCP 也失败时）
                                   引导用户配置
```

- **API 直连模式（主）** — 直接调用供应商视觉 API。最稳定，绕过 MCP 不稳定性。
- **MCP 模式（备用）** — 使用会话中的 MCP 视觉工具。可用时零配置。
- **自定义提示词** — `python claw-eyes.py analyze "请诊断这个错误截图"` 针对性分析。

### 前置要求

| 需要什么 | 怎么装 |
|---|---|
| **Python 3.8+** | [python.org](https://www.python.org/downloads/) |
| **Pillow** | `pip install Pillow` |

### 分析模式

| 模式 | 方式 | 优先级 | 需要配置 | 说明 |
|------|------|--------|----------|------|
| **模式 A** | 直连 API | ✅ 主模式 | API key + URL + 模型 | 最稳定 |
| **模式 B** | MCP 工具 | 备用 | 无（自动检测） | 可用时零配置 |
| **模式 C** | 无 | — | — | 引导用户配置 |

### 安装

#### 方式一：让 AI 来安装（推荐）

把这段话发给你的 AI 助手：

```
请帮我安装这个 skill：https://github.com/zwq871482439/claw-eyes
克隆到我的 skill 目录，安装后运行设置流程。
```

#### 方式二：手动 Git 克隆

```bash
# WorkBuddy
git clone https://github.com/zwq871482439/claw-eyes.git ~/.workbuddy/skills/clipboard-reader

# OpenClaw — 调整路径到你的 skill 目录
# git clone https://github.com/zwq871482439/claw-eyes.git ~/.openclaw/skills/clipboard-reader
```

#### 安装后设置

安装完成后，AI 会引导你完成：

1. ✅ **检查 Python**（需要 3.8+）
2. ✅ **检查 Pillow**（缺失时自动安装）
3. ✅ **确认保存路径**（默认：`<TEMP>/claw-eyes/clipboard.png`）
4. ✅ **选择供应商** → 自动配置 URL 和模型
5. ✅ **验证 API** 密钥
6. ✅ **可选：启用 MCP 备用模式**

### 配置

所有环境变量统一使用 `CLAW_EYES_` 前缀。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CLAW_EYES_SAVE_PATH` | `<TEMP>/claw-eyes/clipboard.png` | 图片保存路径 |
| `CLAW_EYES_API_KEY` | （无） | 视觉模型 API 密钥 |
| `CLAW_EYES_API_URL` | （无） | API 端点，须与供应商匹配 |
| `CLAW_EYES_VISION_MODEL` | （无） | 视觉模型名，须与供应商匹配 |
| `CLAW_EYES_MCP_SERVER` | 自动检测 | MCP 服务名（备用模式） |
| `CLAW_EYES_MCP_TOOL` | 自动检测 | MCP 工具名（备用模式） |
| `CLAW_EYES_LANG` | `zh` | 默认提示语言 |

> ⚠️ **`API_URL` 和 `VISION_MODEL` 没有默认值。** 必须根据供应商一起设置，三者来自同一供应商。

### 兼容的 API 供应商（Top 10）

#### 🇨🇳 国内

| 供应商 | API 地址 | 免费视觉模型 | 获取 Key |
|--------|----------|-------------|----------|
| **智谱 Zhipu** ⭐ | `open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4.6v-flash`（128K） | [open.bigmodel.cn](https://open.bigmodel.cn) |
| **硅基流动** | `api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | [siliconflow.cn](https://siliconflow.cn) |
| **阿里云百炼** | `dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `qwen-vl-max` | [dashscope.console.aliyun.com](https://dashscope.console.aliyun.com) |
| **火山引擎** | `ark.cn-beijing.volces.com/api/v3/chat/completions` | `doubao-1.5-vision-pro-32k` | [console.volcengine.com/ark](https://console.volcengine.com/ark) |
| **百度千帆** | `qianfan.baidubce.com/v2/chat/completions` | `ernie-4.5-vl` | [console.bce.baidu.com/qianfan](https://console.bce.baidu.com/qianfan) |

#### 🌍 国际

| 供应商 | API 地址 | 免费视觉模型 | 获取 Key |
|--------|----------|-------------|----------|
| **OpenAI** | `api.openai.com/v1/chat/completions` | 无（付费：`gpt-4o`） | [platform.openai.com](https://platform.openai.com) |
| **Google Gemini** | `generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-2.0-flash` | [aistudio.google.com](https://aistudio.google.com) |
| **Groq** | `api.groq.com/openai/v1/chat/completions` | `llama-3.2-90b-vision-preview` | [console.groq.com](https://console.groq.com) |
| **Mistral** | `api.mistral.ai/v1/chat/completions` | `pixtral-12b-2409` | [console.mistral.ai](https://console.mistral.ai) |
| **Together AI** | `api.together.xyz/v1/chat/completions` | `meta-llama/Llama-3.2-90B-Vision-Instruct` | [api.together.ai](https://api.together.ai) |

**本地部署：** Ollama → `API_URL=http://localhost:11434/v1/chat/completions`，`API_KEY=ollama`，`VISION_MODEL=llava`

### 使用方法

1. 截图：`Win + Shift + S`（Windows）/ `Cmd + Shift + 4`（macOS）
2. 说触发词：
   - 🇨🇳 "看图"、"看看这个"、"帮我看图"、"截图看一下"
   - 🇺🇸 "look at this"、"check screenshot"、"analyze image"
3. AI 读取剪贴板并分析图片！

---

## Roadmap / 路线图

- [x] 跨平台支持（Windows / macOS / Linux）
- [x] API 直连主模式
- [x] MCP 备用模式
- [x] Top 10 供应商预配置
- [x] 自定义提示词
- [ ] 自动检测 MCP 视觉工具
- [ ] 多图片剪贴板支持
- [ ] 剪贴板历史模式

## File Structure / 文件结构

```
claw-eyes/
├── SKILL.md              # Skill definition / 技能定义（AI 读这个）
├── scripts/
│   └── claw-eyes.py      # Python 脚本（全部逻辑）
├── README.md             # 本文件（给人看的）
├── LICENSE               # MIT License
└── .gitignore
```

## License

[MIT](LICENSE) — Use it however you want! / 随便用！

## Author

**slow** — [GitHub](https://github.com/zwq871482439)
