---
name: claw-eyes
description: >
  Read clipboard images and analyze them via MCP vision tools.
  读取剪贴板中的图片并进行分析。当用户说"看图"、"看看这个"、"看一下图"、"截图看一下"、"帮我看图"、
  "look at this"、"check screenshot"、"analyze image"、"read my screen"、"show me"等类似表达时触发此技能。
  此技能会自动读取Windows剪贴板中的图片内容，保存到本地后通过MCP图像分析工具进行识别和分析。
---

# Claw Eyes 👀 - Clipboard Image Reader & Analyzer

## Overview / 概述

This skill reads images from the Windows system clipboard and analyzes them using MCP vision tools.
It bridges the gap when users cannot directly send images through the chat interface.

此技能用于在用户无法通过聊天框直接发送图片时，通过读取Windows系统剪贴板来获取图片内容并进行分析。

## Requirements / 环境要求

- **OS**: Windows (relies on `System.Windows.Forms`)
- **MCP**: A vision-capable MCP tool (e.g., `zai/analyze_image`)
- **Optional**: Python with Pillow (`pip install Pillow`) for enhanced clipboard support

## Configuration / 配置

### Environment Variable / 环境变量

| Variable | Default | Description |
|----------|---------|-------------|
| `CLIPBOARD_SAVE_PATH` | `C:\tmp\_clipboard\clipboard.png` | Path where clipboard image is saved |

Set it before using if you want a custom location:

```powershell
# PowerShell
$env:CLIPBOARD_SAVE_PATH = "D:\my-path\clip.png"
```

```bash
# Bash
export CLIPBOARD_SAVE_PATH="/tmp/clip.png"
```

### Pre-install Check / 安装前检查

When installing this skill, the AI assistant should verify:

1. The save directory exists (or can be created automatically)
2. The `CLIPBOARD_SAVE_PATH` environment variable is set (or the default path is acceptable)
3. A vision-capable MCP tool is available in the current session

## Triggers / 触发条件

**Chinese / 中文:**
- "看图"、"看看图"、"看一下图"
- "帮我看图"、"帮我看一下这个截图"
- "看看这个"、"看下这个"
- "截图看一下"、"看截图"
- 任何暗示"我截了图，你帮我看看"的表达

**English / 英文:**
- "look at this"、"look at my screen"
- "check screenshot"、"check this screenshot"
- "analyze image"、"analyze this"
- "read my screen"、"show me this"
- Any expression implying "I took a screenshot, help me see it"

## Workflow / 工作流程

### Step 1: Read Clipboard Image / 第一步：读取剪贴板图片

Execute PowerShell to save clipboard image:

```powershell
$savePath = if ($env:CLIPBOARD_SAVE_PATH) { $env:CLIPBOARD_SAVE_PATH } else { 'C:\tmp\_clipboard\clipboard.png' }
$dir = Split-Path $savePath -Parent
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
powershell -Command "Add-Type -AssemblyName System.Windows.Forms; Add-Type -AssemblyName System.Drawing; $img = [System.Windows.Forms.Clipboard]::GetImage(); if ($img -ne $null) { $img.Save('$savePath', [System.Drawing.Imaging.ImageFormat]::Png); Write-Output 'OK' } else { Write-Output 'NO_IMAGE' }"
```

- Output `OK` → Image found, proceed to step 2
- Output `NO_IMAGE` → No image in clipboard, remind user to screenshot first

### Step 2: Analyze Image / 第二步：分析图片

Use MCP tool to analyze the saved image:

```
mcp_call_tool: serverName="zai", toolName="analyze_image"
arguments: {"image_source": "<CLIPBOARD_SAVE_PATH value>", "prompt": "请详细描述这张图片的内容，包括文字、界面元素、数据等所有可见信息。Please describe the content of this image in detail, including text, UI elements, data, and all visible information."}
```

**Important**: Use the actual `CLIPBOARD_SAVE_PATH` value (or default) as `image_source`.

If `zai/analyze_image` is unavailable, try any other vision-capable MCP tool.

### Step 3: Return Results / 第三步：返回分析结果

Return the analysis in natural language. Adapt response based on content:

- **Screenshot/UI** → Describe interface elements and visible info
- **Error message** → Provide diagnostic suggestions
- **Document/table** → Extract text and data
- **Code screenshot** → Recognize and reproduce code content

## Notes / 注意事项

- Image is overwritten on each use — no cleanup needed
- Windows-only (depends on `System.Windows.Forms`)
- If user hasn't screenshot yet, remind them: `Win + Shift + S`
- The Python script (`scripts/read_clipboard.py`) is an alternative — it supports Pillow with PowerShell fallback
