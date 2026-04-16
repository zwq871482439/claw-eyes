# 👀 Claw Eyes

> **Universal clipboard image reader for any Claw-based AI assistant — read screenshots, analyze via vision APIs or MCP tools**
>
> 通用剪贴板图片读取器，适配任何基于 Claw 的 AI 助手 — 读取截图，通过视觉 API 或 MCP 工具分析

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue)](https://github.com/zwq871482439/claw-eyes)

---

## What is this? / 这是什么？

When using Claw-based AI assistants (WorkBuddy, OpenClaw, QClaw, etc.), you sometimes can't directly paste images into the chat. **Claw Eyes** solves this by reading your system clipboard and passing the image to vision APIs for analysis.

在使用基于 Claw 的 AI 助手（WorkBuddy、OpenClaw、QClaw 等）时，有时无法直接在聊天中粘贴图片。**Claw Eyes** 通过读取系统剪贴板并将图片传给视觉 API 来解决这个问题。

Just screenshot something, then say "看图" or "look at this" — done!

截图，然后说"看图"或"look at this"——搞定！

## Platform Support / 平台支持

| Platform | Status | Method |
|----------|--------|--------|
| Windows | ✅ Supported | `System.Windows.Forms` / Pillow |
| Linux | 🔜 Planned | `xclip` / `wl-paste` |
| macOS | 🔜 Planned | `osascript` / `pbpaste` |

## Features / 特性

- 📋 Reads images directly from system clipboard
- 🔍 **Dual analysis modes**: Direct API (recommended) + MCP fallback
- 🚀 **Direct API mode**: Calls vision model API directly — bypasses MCP response bugs on some platforms
- 🆓 **Free models supported**: `glm-4.6v-flash` (recommended), `Qwen2.5-VL` (SiliconFlow free tier)
- ⚙️ Configurable via `CLAW_EYES_*` environment variables
- 🌐 Bilingual triggers (Chinese + English)
- 🔄 Compatible with **all Claw variants** (WorkBuddy, OpenClaw, QClaw, etc.)
- 🔑 API key validation on installation — guides users to free options if unconfigured

## Requirements / 环境要求

- **OS**: Windows (Linux/macOS coming soon)
- **Vision API** (one of):
  - A vision-capable API key (智谱 Zhipu, 硅基流动 SiliconFlow, OpenAI, or local Ollama)
  - A vision MCP tool in your session (fallback mode)
- **Python** (optional): With Pillow for enhanced clipboard support

## Installation / 安装

### Option 1: Let your AI install it / 让你的 AI 来安装（推荐 Recommended）

Just send this message to your AI assistant:

把这段话发给你的 AI 助手即可：

```
请帮我安装这个 skill：https://github.com/zwq871482439/claw-eyes
克隆到我的 skill 目录，安装后运行 Vision Capability Check 检测视觉分析能力。
```

### Option 2: Git clone manually / 手动克隆

```powershell
# WorkBuddy
git clone https://github.com/zwq871482439/claw-eyes.git "$env:USERPROFILE\.workbuddy\skills\clipboard-reader"

# OpenClaw — adjust path to your skill directory
# git clone https://github.com/zwq871482439/claw-eyes.git "~/.openclaw/skills/clipboard-reader"
```

### Post-install Setup / 安装后设置

After installing, you need:

1. ✅ **Set a vision API key** (recommended — enables Direct API mode):
   ```powershell
   # Free key from open.bigmodel.cn → glm-4.6v-flash (free, 128K, video/docs)
   $env:CLAW_EYES_API_KEY = "your_key_here"
   ```
2. ✅ Or have a **vision MCP tool** available in your session (fallback mode)
3. ✅ The AI will run **Vision Capability Check** to detect which mode to use

## Configuration / 配置

All env vars use the `CLAW_EYES_` prefix for consistency.

所有环境变量统一使用 `CLAW_EYES_` 前缀。

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAW_EYES_SAVE_PATH` | `%TEMP%\claw-eyes\clipboard.png` (Win) | Image save path / 图片保存路径 |
| `CLAW_EYES_API_KEY` | (none) | Vision API key for Direct API mode / 视觉 API 密钥 |
| `CLAW_EYES_API_URL` | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | Vision API endpoint / 视觉 API 地址 |
| `CLAW_EYES_VISION_MODEL` | `glm-4.6v-flash` | Vision model name / 视觉模型名称 |
| `CLAW_EYES_MCP_SERVER` | auto-detect | MCP server name (fallback) / MCP 服务名（备选） |
| `CLAW_EYES_MCP_TOOL` | auto-detect | MCP tool name (fallback) / MCP 工具名（备选） |
| `CLAW_EYES_LANG` | `zh` | Default prompt language / 默认提示语言 |

```powershell
# Example: 智谱 Zhipu (free, recommended)
$env:CLAW_EYES_API_KEY = "your_zhipu_key"
$env:CLAW_EYES_API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "glm-4.6v-flash"

# Example: 硅基流动 SiliconFlow (free tier)
$env:CLAW_EYES_API_KEY = "your_siliconflow_key"
$env:CLAW_EYES_API_URL = "https://api.siliconflow.cn/v1/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "Qwen/Qwen2.5-VL-7B-Instruct"

# Example: Local Ollama (no key needed)
$env:CLAW_EYES_API_KEY = "ollama"
$env:CLAW_EYES_API_URL = "http://localhost:11434/v1/chat/completions"
$env:CLAW_EYES_VISION_MODEL = "llava"
```

## Compatible API Providers / 兼容的 API 提供商

| Provider | Base URL | Free Models | How to get key |
|----------|----------|-------------|----------------|
| 智谱 Zhipu | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4.6v-flash` ⭐ | [open.bigmodel.cn](https://open.bigmodel.cn) |
| 硅基流动 SiliconFlow | `https://api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | [siliconflow.cn](https://siliconflow.cn) |
| OpenAI | `https://api.openai.com/v1/chat/completions` | None (paid) | [platform.openai.com](https://platform.openai.com) |
| 本地 Ollama | `http://localhost:11434/v1/chat/completions` | `llava`, `minicpm-v` | No key needed |

## Usage / 使用方法

1. Take a screenshot: `Win + Shift + S` (Windows)
2. Say one of the trigger phrases:
   - 🇨🇳 "看图"、"看看这个"、"帮我看图"、"截图看一下"
   - 🇺🇸 "look at this"、"check screenshot"、"analyze image"
3. The AI reads your clipboard and analyzes the image!

## Analysis Modes / 分析模式

| Mode | Method | Priority | Notes |
|------|--------|----------|-------|
| **Mode A** | Direct API | ✅ Recommended | Calls vision API directly via `execute_command`. Response guaranteed to reach AI context. |
| **Mode B** | MCP Tool | Fallback | Uses MCP vision tool if available. May fail on some platforms due to MCP response bugs. |
| **Mode C** | None | — | Guides user to set up a vision capability. |

## File Structure / 文件结构

```
claw-eyes/
├── SKILL.md              # Skill definition & workflow / 技能定义和工作流程
├── scripts/
│   └── read_clipboard.py # Python clipboard reader (cross-platform ready)
├── README.md             # This file / 本文件
├── LICENSE               # MIT License
└── .gitignore
```

## How It Works / 工作原理

```
Screenshot → Clipboard → Save to disk → Vision API/MCP analyzes → Result
截图       → 剪贴板   → 保存到本地     → 视觉 API/MCP 分析        → 结果
```

**Direct API mode (Mode A)** uses `execute_command` to call vision APIs directly — this bypasses MCP entirely and is the most reliable method on all Claw platforms.

**MCP mode (Mode B)** uses whatever vision MCP tool is available in your session — simpler setup but less reliable on some platforms.

## Roadmap / 路线图

- [x] Direct API mode (bypass MCP, call vision model directly)
- [x] Vision Capability Check (validate API key + detect vision support)
- [x] `glm-4.6v-flash` as default model (free, 128K, video/docs)
- [ ] Linux support (`xclip` / `wl-paste`)
- [ ] macOS support (`osascript` / `pbpaste`)
- [ ] Auto-detect available MCP vision tools
- [ ] Multi-image clipboard support
- [ ] Clipboard history mode

## License / 开源协议

[MIT](LICENSE) — Use it however you want! / 随便用！

## Author / 作者

**slow** — [GitHub](https://github.com/zwq871482439)
