# 👀 Claw Eyes

> **Universal clipboard image reader for any Claw-based AI assistant — read screenshots, analyze via MCP vision tools**
>
> 通用剪贴板图片读取器，适配任何基于 Claw 的 AI 助手 — 读取截图，通过 MCP 视觉工具分析

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows-blue)](https://github.com/zwq871482439/claw-eyes)

---

## What is this? / 这是什么？

When using Claw-based AI assistants (WorkBuddy, OpenClaw, QClaw, etc.), you sometimes can't directly paste images into the chat. **Claw Eyes** solves this by reading your system clipboard and passing the image to MCP vision tools for analysis.

在使用基于 Claw 的 AI 助手（WorkBuddy、OpenClaw、QClaw 等）时，有时无法直接在聊天中粘贴图片。**Claw Eyes** 通过读取系统剪贴板并将图片传给 MCP 视觉分析工具来解决这个问题。

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
- 🔍 Analyzes via any MCP vision tool (auto-detects available tools)
- 🐍 Python script with PowerShell fallback (no Pillow required on Windows)
- ⚙️ Configurable via `CLAW_EYES_*` environment variables
- 🌐 Bilingual triggers (Chinese + English)
- 🔄 Compatible with **all Claw variants** (WorkBuddy, OpenClaw, QClaw, etc.)

## Requirements / 环境要求

- **OS**: Windows (Linux/macOS coming soon)
- **MCP**: A vision-capable MCP tool must be available in your session
- **Python** (optional): With Pillow for enhanced clipboard support

## Installation / 安装

### Option 1: Let your AI install it / 让你的 AI 来安装（推荐 Recommended）

Just send this message to your AI assistant:

把这段话发给你的 AI 助手即可：

```
请帮我安装这个 skill：https://github.com/zwq871482439/claw-eyes
克隆到我的 skill 目录，安装后检查 CLAW_EYES_SAVE_PATH 环境变量和 MCP 视觉工具是否可用。
```

### Option 2: Git clone manually / 手动克隆

```powershell
# WorkBuddy
git clone https://github.com/zwq871482439/claw-eyes.git "$env:USERPROFILE\.workbuddy\skills\claw-eyes"

# OpenClaw — adjust path to your skill directory
# git clone https://github.com/zwq871482439/claw-eyes.git "~/.openclaw/skills/claw-eyes"
```

### Post-install Verification / 安装后验证

After installing, verify that:

1. ✅ The save directory exists (default: `C:\tmp\_clipboard\` on Windows)
2. ✅ A vision MCP tool is available in your session
3. ✅ Optionally set env vars if defaults don't suit you

## Configuration / 配置

All env vars use the `CLAW_EYES_` prefix for consistency.

所有环境变量统一使用 `CLAW_EYES_` 前缀。

| Variable | Default (Win) | Description |
|----------|---------------|-------------|
| `CLAW_EYES_SAVE_PATH` | `C:\tmp\_clipboard\clipboard.png` | Image save path / 图片保存路径 |
| `CLAW_EYES_MCP_SERVER` | auto-detect | MCP server name for vision / MCP 视觉服务名 |
| `CLAW_EYES_MCP_TOOL` | auto-detect | MCP tool name for vision / MCP 视觉工具名 |
| `CLAW_EYES_LANG` | `zh` | Default prompt language / 默认提示语言 |

```powershell
# Example: custom config / 示例：自定义配置
$env:CLAW_EYES_SAVE_PATH = "D:\screenshots\clip.png"
$env:CLAW_EYES_MCP_SERVER = "zai"
$env:CLAW_EYES_MCP_TOOL = "analyze_image"
$env:CLAW_EYES_LANG = "en"
```

## Usage / 使用方法

1. Take a screenshot: `Win + Shift + S` (Windows)
2. Say one of the trigger phrases:
   - 🇨🇳 "看图"、"看看这个"、"帮我看图"、"截图看一下"
   - 🇺🇸 "look at this"、"check screenshot"、"analyze image"
3. The AI reads your clipboard and analyzes the image!

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
Screenshot → Clipboard → Save to disk → MCP vision tool analyzes → Result
截图       → 剪贴板   → 保存到本地     → MCP 视觉工具分析          → 结果
```

## Roadmap / 路线图

- [ ] Linux support (`xclip` / `wl-paste`)
- [ ] macOS support (`osascript` / `pbpaste`)
- [ ] Auto-detect available MCP vision tools
- [ ] Multi-image clipboard support
- [ ] Clipboard history mode

## License / 开源协议

[MIT](LICENSE) — Use it however you want! / 随便用！

## Author / 作者

**slow** — [GitHub](https://github.com/zwq871482439)
