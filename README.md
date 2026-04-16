# 👀 Claw Eyes

> **Read Windows clipboard images and analyze them via MCP vision tools — a WorkBuddy/Claw skill**
>
> 读取 Windows 剪贴板图片并通过 MCP 视觉工具分析 — 一个 WorkBuddy/Claw 技能

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## What is this? / 这是什么？

When using AI assistants like WorkBuddy's Claw, you sometimes can't directly paste images into the chat. **Claw Eyes** solves this by reading your system clipboard and passing the image to MCP vision tools for analysis.

在使用 WorkBuddy 的 Claw 等 AI 助手时，有时无法直接在聊天中粘贴图片。**Claw Eyes** 通过读取系统剪贴板并将图片传给 MCP 视觉分析工具来解决这个问题。

Just screenshot something (`Win + Shift + S`), then say "看图" or "look at this" — done!

截图（`Win + Shift + S`），然后说"看图"或"look at this"——搞定！

## Features / 特性

- 📋 Reads images directly from Windows clipboard
- 🔍 Analyzes via MCP vision tools (e.g., `zai/analyze_image`)
- 🐍 Python script with PowerShell fallback (no Pillow required)
- ⚙️ Configurable save path via environment variable
- 🌐 Bilingual triggers (Chinese + English)

## Requirements / 环境要求

- **OS**: Windows (uses `System.Windows.Forms` for clipboard access)
- **MCP**: A vision-capable MCP tool must be available in your WorkBuddy session
- **Python** (optional): With Pillow for enhanced clipboard support

## Installation / 安装

### Option 1: Let your AI install it / 让你的 AI 来安装（推荐 Recommended）

Just send this message to your WorkBuddy AI assistant:

把这段话发给你的 WorkBuddy AI 助手即可：

```
请帮我安装这个 skill：https://github.com/zwq871482439/claw-eyes
克隆到 ~/.workbuddy/skills/claw-eyes 目录，安装后检查 CLIPBOARD_SAVE_PATH 环境变量和 MCP 视觉工具是否可用。
```

The AI will clone the repo, install the skill, and verify everything for you.

AI 会自动克隆仓库、安装 skill、并检查环境是否就绪。

### Option 2: Git clone manually / 手动克隆

```powershell
git clone https://github.com/zwq871482439/claw-eyes.git "$env:USERPROFILE\.workbuddy\skills\claw-eyes"
```

### Post-install Verification / 安装后验证

After installing, verify that:

1. ✅ The save directory exists (default: `C:\tmp\_clipboard\`)
2. ✅ A vision MCP tool is available in your session
3. ✅ Optionally set `CLIPBOARD_SAVE_PATH` if you want a custom location

## Configuration / 配置

### Environment Variable / 环境变量

| Variable | Default | Description |
|----------|---------|-------------|
| `CLIPBOARD_SAVE_PATH` | `C:\tmp\_clipboard\clipboard.png` | Path where clipboard image is saved / 剪贴板图片保存路径 |

```powershell
# Custom path / 自定义路径
$env:CLIPBOARD_SAVE_PATH = "D:\screenshots\clip.png"
```

## Usage / 使用方法

1. Take a screenshot: `Win + Shift + S`
2. Say one of the trigger phrases:
   - 🇨🇳 "看图"、"看看这个"、"帮我看图"、"截图看一下"
   - 🇺🇸 "look at this"、"check screenshot"、"analyze image"
3. The AI reads your clipboard and analyzes the image!

## File Structure / 文件结构

```
claw-eyes/
├── SKILL.md              # Skill definition & workflow / 技能定义和工作流程
├── scripts/
│   └── read_clipboard.py # Python clipboard reader / Python 剪贴板读取脚本
├── README.md             # This file / 本文件
├── LICENSE               # MIT License
└── .gitignore
```

## How It Works / 工作原理

```
Screenshot → Clipboard → PowerShell/PIL saves image → MCP vision tool analyzes → Result
截图       → 剪贴板   → PowerShell/PIL 保存图片       → MCP 视觉工具分析          → 结果
```

## License / 开源协议

[MIT](LICENSE) — Use it however you want! / 随便用！

## Author / 作者

**slow** — [GitHub](https://github.com/zwq871482439)
