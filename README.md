# 👀 Claw Eyes

> 让纯文字推理模型"借一双眼睛" — 通用剪贴板图片读取器，适配所有 Claw 平台
>
> Let text-only reasoning models "borrow eyes" — Universal clipboard image reader for all Claw platforms

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue)](https://github.com/zwq871482439/claw-eyes)

---

## TL;DR / 一句话说明

截图，说"看图"，AI 帮你分析图片内容。MCP 零配置优先，API 直连降级备选。

Screenshot → say "看图" → AI analyzes it. MCP-first (zero config), Direct API fallback.

**支持平台 / Platforms**: Windows ✅ | Linux 🔜 | macOS 🔜

**兼容 / Compatible with**: WorkBuddy · OpenClaw · QClaw · 任何基于 Claw 的 AI 助手

---

## Features / 特性一览

- 📋 读取系统剪贴板图片 / Read images from system clipboard
- 🔍 双模式：MCP 主模式（零配置）+ API 降级模式 / Dual mode: MCP (primary) + API (fallback)
- 🔌 多供应商：智谱 / 硅基流动 / Kimi / OpenAI / Ollama / Multi-provider support
- 🆓 免费可用：glm-4.6v-flash、Qwen2.5-VL 等 / Free options available
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

**Key insight:** Your main model stays as the flagship reasoning model, while getting multimodal input on demand. No model switching needed. Already using Kimi? Reuse the same API key. Running local models? Register a free Zhipu account.

### How It Works

```
Screenshot → Clipboard → Save to disk → MCP analyzes (primary) → Result
                                          ↓ (if MCP fails)
                                          Direct API analyzes (fallback) → Result
```

- **MCP mode (primary)** — Uses whatever vision MCP tool is in your session. Zero config, just works.
- **Direct API mode (fallback)** — When MCP fails (response loss, timeout, etc.), falls back to calling your provider's vision API directly. More reliable but requires setup.

### Analysis Modes

| Mode | Method | Priority | Config Required | Notes |
|------|--------|----------|-----------------|-------|
| **Mode A** | MCP Tool | ✅ Primary | None | Auto-detects MCP vision tools |
| **Mode B** | Direct API | Fallback | API key + URL + model | Bypasses MCP bugs |
| **Mode C** | None | — | — | Guides user to set up vision capability |

### Installation

#### Option 1: Let your AI install it (Recommended)

Send this message to your AI assistant:

```
Please install this skill: https://github.com/zwq871482439/claw-eyes
Clone it to my skill directory, then run Vision Capability Check after installation.
```

#### Option 2: Git clone manually

```powershell
# WorkBuddy
git clone https://github.com/zwq871482439/claw-eyes.git "$env:USERPROFILE\.workbuddy\skills\clipboard-reader"

# OpenClaw — adjust path to your skill directory
# git clone https://github.com/zwq871482439/claw-eyes.git "~/.openclaw/skills/clipboard-reader"
```

#### Post-install Setup

After installing, the AI will walk you through:

1. ✅ **Confirm save path** (default: `%TEMP%\claw-eyes\clipboard.png`)
2. ✅ **Detect MCP vision tools** (primary mode, zero config)
3. ✅ **Ask about Direct API mode** (optional enhancement)
4. ✅ If Direct API → **Ask which provider** → configure URL/model accordingly

### Configuration

All env vars use the `CLAW_EYES_` prefix.

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAW_EYES_SAVE_PATH` | `%TEMP%\claw-eyes\clipboard.png` | Image save path |
| `CLAW_EYES_API_KEY` | (none) | Vision API key (Direct API mode) |
| `CLAW_EYES_API_URL` | (none) | Vision API endpoint — must match your provider |
| `CLAW_EYES_VISION_MODEL` | (none) | Vision model — must match your provider |
| `CLAW_EYES_MCP_SERVER` | auto-detect | MCP server name (primary mode) |
| `CLAW_EYES_MCP_TOOL` | auto-detect | MCP tool name (primary mode) |
| `CLAW_EYES_LANG` | `zh` | Default prompt language |

> ⚠️ **`API_URL` and `VISION_MODEL` have NO defaults.** They must be set together based on your provider.

### Compatible API Providers

| Provider | API URL | Free Vision Model | How to get key |
|----------|---------|-------------------|----------------|
| 智谱 Zhipu ⭐ | `open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4.6v-flash` (128K, video/docs) | [open.bigmodel.cn](https://open.bigmodel.cn) |
| SiliconFlow | `api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | [siliconflow.cn](https://siliconflow.cn) |
| Kimi | `api.moonshot.cn/v1/chat/completions` | Check latest docs | [platform.moonshot.cn](https://platform.moonshot.cn) |
| OpenAI | `api.openai.com/v1/chat/completions` | None (paid, `gpt-4o`) | [platform.openai.com](https://platform.openai.com) |
| Local Ollama | `localhost:11434/v1/chat/completions` | `llava`, `minicpm-v` | No key needed |

```powershell
# Example: Zhipu (free, recommended)
$env:CLAW_EYES_API_KEY = "your_zhipu_key"
$env:CLAW_EYES_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "glm-4.6v-flash"

# Example: SiliconFlow (free tier)
$env:CLAW_EYES_API_KEY = "your_siliconflow_key"
$env:CLAW_EYES_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"

# Example: Local Ollama (no key needed)
$env:CLAW_EYES_API_KEY = "ollama"
$env:CLAW_EYES_API_URL = "http://localhost:11434/v1/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "llava"
```

### Usage

1. Take a screenshot: `Win + Shift + S` (Windows)
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

**核心理念：** 主模型仍然是旗舰推理模型，按需获得多模态输入。不需要切换模型。已经在用 Kimi？复用同一个 API key。跑的是本地模型？注册一个免费智谱账号即可。

### 工作原理

```
截图 → 剪贴板 → 保存到本地 → MCP 分析（主模式）→ 结果
                                  ↓ （MCP 失败时）
                                  直连 API 分析（降级）→ 结果
```

- **MCP 模式（主）** — 使用会话中的 MCP 视觉工具，零配置开箱即用。
- **直连 API 模式（备选）** — MCP 失败时（响应丢失、超时等），直接调用供应商的视觉 API。更稳定但需要配置。

### 分析模式

| 模式 | 方式 | 优先级 | 需要配置 | 说明 |
|------|------|--------|----------|------|
| **模式 A** | MCP 工具 | ✅ 主模式 | 无 | 自动检测 MCP 视觉工具 |
| **模式 B** | 直连 API | 降级备选 | API key + URL + 模型 | 绕过 MCP 响应问题 |
| **模式 C** | 无 | — | — | 引导用户配置视觉能力 |

### 安装

#### 方式一：让 AI 来安装（推荐）

把这段话发给你的 AI 助手：

```
请帮我安装这个 skill：https://github.com/zwq871482439/claw-eyes
克隆到我的 skill 目录，安装后运行 Vision Capability Check 检测视觉分析能力。
```

#### 方式二：手动 Git 克隆

```powershell
# WorkBuddy
git clone https://github.com/zwq871482439/claw-eyes.git "$env:USERPROFILE\.workbuddy\skills\clipboard-reader"

# OpenClaw — 调整路径到你的 skill 目录
# git clone https://github.com/zwq871482439/claw-eyes.git "~/.openclaw/skills/clipboard-reader"
```

#### 安装后设置

安装完成后，AI 会引导你完成：

1. ✅ **确认保存路径**（默认：`%TEMP%\claw-eyes\clipboard.png`）
2. ✅ **检测 MCP 视觉工具**（主模式，零配置）
3. ✅ **询问是否配置直连 API**（可选增强）
4. ✅ 如果配直连 API → **选择供应商** → 自动配置 URL/模型

### 配置

所有环境变量统一使用 `CLAW_EYES_` 前缀。

| 变量 | 默认值 | 说明 |
|------|--------|------|
| `CLAW_EYES_SAVE_PATH` | `%TEMP%\claw-eyes\clipboard.png` | 图片保存路径 |
| `CLAW_EYES_API_KEY` | （无） | 视觉模型 API 密钥（直连模式） |
| `CLAW_EYES_API_URL` | （无） | 视觉 API 端点，必须与供应商匹配 |
| `CLAW_EYES_VISION_MODEL` | （无） | 视觉模型名称，必须与供应商匹配 |
| `CLAW_EYES_MCP_SERVER` | 自动检测 | MCP 服务名（主模式） |
| `CLAW_EYES_MCP_TOOL` | 自动检测 | MCP 工具名（主模式） |
| `CLAW_EYES_LANG` | `zh` | 默认提示语言 |

> ⚠️ **`API_URL` 和 `VISION_MODEL` 没有默认值。** 必须根据供应商一起设置，不能混用。

### 兼容的 API 供应商

| 供应商 | API 地址 | 免费视觉模型 | 获取 Key |
|--------|----------|-------------|----------|
| 智谱 Zhipu ⭐ | `open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4.6v-flash`（128K，支持视频/文档） | [open.bigmodel.cn](https://open.bigmodel.cn) |
| 硅基流动 SiliconFlow | `api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | [siliconflow.cn](https://siliconflow.cn) |
| Kimi（月之暗面） | `api.moonshot.cn/v1/chat/completions` | 查看最新文档 | [platform.moonshot.cn](https://platform.moonshot.cn) |
| OpenAI | `api.openai.com/v1/chat/completions` | 无（付费，`gpt-4o`） | [platform.openai.com](https://platform.openai.com) |
| 本地 Ollama | `localhost:11434/v1/chat/completions` | `llava`、`minicpm-v` | 无需 key |

```powershell
# 示例：智谱（免费，推荐）
$env:CLAW_EYES_API_KEY = "你的智谱_key"
$env:CLAW_EYES_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "glm-4.6v-flash"

# 示例：硅基流动（免费额度）
$env:CLAW_EYES_API_KEY = "你的硅基流动_key"
$env:CLAW_EYES_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"

# 示例：本地 Ollama（无需 key）
$env:CLAW_EYES_API_KEY = "ollama"
$env:CLAW_EYES_API_URL = "http://localhost:11434/v1/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "llava"
```

### 使用方法

1. 截图：`Win + Shift + S`（Windows）
2. 说触发词：
   - 🇨🇳 "看图"、"看看这个"、"帮我看图"、"截图看一下"
   - 🇺🇸 "look at this"、"check screenshot"、"analyze image"
3. AI 读取剪贴板并分析图片！

---

## Roadmap / 路线图

- [x] MCP 视觉工具集成（主模式，零配置）/ MCP vision integration
- [x] 直连 API 降级模式 / Direct API fallback
- [x] 供应商无关配置 / Provider-agnostic setup
- [x] `glm-4.6v-flash` 推荐免费模型 / Recommended free model
- [ ] Linux 支持（`xclip` / `wl-paste`）/ Linux support
- [ ] macOS 支持（`osascript` / `pbpaste`）/ macOS support
- [ ] 自动检测 MCP 视觉工具 / Auto-detect MCP tools
- [ ] 多图片剪贴板支持 / Multi-image clipboard
- [ ] 剪贴板历史模式 / Clipboard history

## File Structure / 文件结构

```
claw-eyes/
├── SKILL.md              # Skill definition / 技能定义
├── scripts/
│   └── read_clipboard.py # Python clipboard reader / Python 读取脚本
├── README.md             # This file / 本文件
├── LICENSE               # MIT License
└── .gitignore
```

## License

[MIT](LICENSE) — Use it however you want! / 随便用！

## Author

**slow** — [GitHub](https://github.com/zwq871482439)
