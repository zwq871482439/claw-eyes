# 👀 Claw Eyes

> **Universal clipboard image reader for any Claw-based AI assistant — read screenshots, analyze via MCP or vision APIs**
>
> 通用剪贴板图片读取器，适配任何基于 Claw 的 AI 助手 — 读取截图，MCP 优先 / 直连 API 备选

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue)](https://github.com/zwq871482439/claw-eyes)

---

## What is this? / 这是什么？

When using Claw-based AI assistants (WorkBuddy, OpenClaw, QClaw, etc.), you sometimes can't directly paste images into the chat. **Claw Eyes** solves this by reading your system clipboard and analyzing the image via MCP vision tools or direct API calls.

在使用基于 Claw 的 AI 助手（WorkBuddy、OpenClaw、QClaw 等）时，有时无法直接在聊天中粘贴图片。**Claw Eyes** 通过读取系统剪贴板并分析图片来解决这个问题。

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
- 🔍 **Dual analysis modes**: MCP (primary, zero config) + Direct API (reliable fallback)
- 🚀 **MCP first**: Auto-detects available MCP vision tools, no setup needed
- 🛡️ **Direct API fallback**: Bypasses MCP response bugs on some platforms
- 🔌 **Provider-agnostic**: Supports Zhipu, SiliconFlow, Kimi, OpenAI, local Ollama — picks the right URL/model per provider
- 🆓 **Free options**: glm-4.6v-flash, Qwen2.5-VL, llava — all free
- ⚙️ Configurable via `CLAW_EYES_*` environment variables
- 🌐 Bilingual triggers (Chinese + English)
- 🔄 Compatible with **all Claw variants** (WorkBuddy, OpenClaw, QClaw, etc.)

## Requirements / 环境要求

- **OS**: Windows (Linux/macOS coming soon)
- **Primary**: A vision-capable MCP tool in your session (auto-detected)
- **Optional**: A vision API key for Direct API fallback mode
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

After installing, the AI will walk you through:

1. ✅ **Confirm save path** (default: `%TEMP%\claw-eyes\clipboard.png`)
2. ✅ **Detect MCP vision tools** (primary mode, zero config)
3. ✅ **Ask about Direct API mode** (optional enhancement)
4. ✅ If Direct API → **Ask which provider** → configure URL/model accordingly

## Configuration / 配置

All env vars use the `CLAW_EYES_` prefix for consistency.

所有环境变量统一使用 `CLAW_EYES_` 前缀。

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAW_EYES_SAVE_PATH` | `%TEMP%\claw-eyes\clipboard.png` (Win) | Image save path / 图片保存路径 |
| `CLAW_EYES_API_KEY` | (none) | Vision API key (Direct API mode) |
| `CLAW_EYES_API_URL` | (none) | Vision API endpoint — **must match your provider** |
| `CLAW_EYES_VISION_MODEL` | (none) | Vision model — **must match your provider** |
| `CLAW_EYES_MCP_SERVER` | auto-detect | MCP server name (primary mode) |
| `CLAW_EYES_MCP_TOOL` | auto-detect | MCP tool name (primary mode) |
| `CLAW_EYES_LANG` | `zh` | Default prompt language / 默认提示语言 |

> ⚠️ **`API_URL` and `VISION_MODEL` have NO defaults.** They must be set together based on your provider. Don't mix providers!

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

| Provider | API URL | Free Vision Model | How to get key |
|----------|---------|-------------------|----------------|
| 智谱 Zhipu ⭐ | `open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4.6v-flash` (128K, video/docs) | [open.bigmodel.cn](https://open.bigmodel.cn) |
| 硅基流动 SiliconFlow | `api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | [siliconflow.cn](https://siliconflow.cn) |
| Kimi (月之暗面) | `api.moonshot.cn/v1/chat/completions` | Check latest docs | [platform.moonshot.cn](https://platform.moonshot.cn) |
| OpenAI | `api.openai.com/v1/chat/completions` | None (paid, `gpt-4o`) | [platform.openai.com](https://platform.openai.com) |
| 本地 Ollama | `localhost:11434/v1/chat/completions` | `llava`, `minicpm-v` | No key needed |

## Usage / 使用方法

1. Take a screenshot: `Win + Shift + S` (Windows)
2. Say one of the trigger phrases:
   - 🇨🇳 "看图"、"看看这个"、"帮我看图"、"截图看一下"
   - 🇺🇸 "look at this"、"check screenshot"、"analyze image"
3. The AI reads your clipboard and analyzes the image!

## Analysis Modes / 分析模式

| Mode | Method | Priority | Config Required | Notes |
|------|--------|----------|-----------------|-------|
| **Mode A** | MCP Tool | ✅ Primary | None | Auto-detects MCP vision tools. Works out of the box. |
| **Mode B** | Direct API | Fallback | API key + URL + model | Bypasses MCP bugs. Reliable fallback. |
| **Mode C** | None | — | — | Guides user to set up a vision capability. |

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
Screenshot → Clipboard → Save to disk → MCP analyzes (primary) → Result
                                          ↓ (if MCP fails)
                                          Direct API analyzes (fallback) → Result
```

**MCP mode (primary)** — Uses whatever vision MCP tool is in your session. Zero config, just works.

**Direct API mode (fallback)** — When MCP fails (response loss, timeout, etc.), falls back to calling your provider's vision API directly. More reliable but requires setup.

## Roadmap / 路线图

- [x] MCP vision tool integration (primary mode, zero config)
- [x] Direct API fallback mode (bypass MCP response bugs)
- [x] Provider-agnostic setup (auto-configure based on user's provider)
- [x] `glm-4.6v-flash` as recommended free model
- [ ] Linux support (`xclip` / `wl-paste`)
- [ ] macOS support (`osascript` / `pbpaste`)
- [ ] Auto-detect available MCP vision tools
- [ ] Multi-image clipboard support
- [ ] Clipboard history mode

## License / 开源协议

[MIT](LICENSE) — Use it however you want! / 随便用！

## Author / 作者

**slow** — [GitHub](https://github.com/zwq871482439)
