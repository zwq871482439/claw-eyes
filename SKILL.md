---
name: claw-eyes
description: >
  Read clipboard images and analyze them via MCP vision tools.
  读取剪贴板中的图片并进行分析。当用户说"看图"、"看看这个"、"看一下图"、"截图看一下"、"帮我看图"、
  "look at this"、"check screenshot"、"analyze image"、"read my screen"、"show me"等类似表达时触发此技能。
  此技能会自动读取系统剪贴板中的图片内容，保存到本地后通过MCP图像分析工具进行识别和分析。
---

# Claw Eyes 👀 — Universal Clipboard Image Reader for Claw

## Overview / 概述

Claw Eyes is a universal clipboard image reader skill designed for **any Claw-based AI assistant** (WorkBuddy, OpenClaw, QClaw, etc.). It reads system clipboard images and passes them to MCP vision tools for analysis.

Claw Eyes 是一个通用的剪贴板图片读取技能，设计用于**任何基于 Claw 的 AI 助手**（WorkBuddy、OpenClaw、QClaw 等）。通过读取系统剪贴板并将图片传给 MCP 视觉分析工具来工作。

## Platform Support / 平台支持

| Platform | Status | Notes |
|----------|--------|-------|
| Windows | ✅ Supported | Uses `System.Windows.Forms` |
| Linux | 🔜 Planned | Will use `xclip`/`wl-paste` |
| macOS | 🔜 Planned | Will use `osascript`/`pbpaste` |

> **Current version only supports Windows.** Linux and macOS support is on the roadmap.
>
> **当前版本仅支持 Windows。** Linux 和 macOS 支持已在路线图中。

## Requirements / 环境要求

- **OS**: Windows (Linux/macOS coming soon)
- **Vision API**: A vision-capable API key (free options available, see below)
- **Optional**: MCP vision tool (e.g., `zai/analyze_image`) as fallback
- **Optional**: Python with Pillow (`pip install Pillow`) for enhanced clipboard support
- **Compatible with**: Any Claw-based AI assistant (WorkBuddy, OpenClaw, QClaw, etc.)

## Configuration / 配置

All configuration uses environment variables with the `CLAW_EYES_` prefix for consistency across different Claw platforms.

所有配置使用 `CLAW_EYES_` 前缀的环境变量，确保跨平台一致性。

### Environment Variables / 环境变量

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAW_EYES_SAVE_PATH` | (auto-detect, see below) | Path where clipboard image is saved |
| `CLAW_EYES_API_KEY` | (none) | Vision API key for Direct API mode |
| `CLAW_EYES_API_URL` | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | Vision API endpoint |
| `CLAW_EYES_VISION_MODEL` | `glm-4.6v-flash` | Vision model name |
| `CLAW_EYES_MCP_SERVER` | (auto-detect) | MCP server name (fallback mode) |
| `CLAW_EYES_MCP_TOOL` | (auto-detect) | MCP tool name (fallback mode) |
| `CLAW_EYES_LANG` | `zh` | Default prompt language (`zh` / `en`) |

**Default save path logic / 默认保存路径逻辑** (when `CLAW_EYES_SAVE_PATH` is not set):

| Platform | Default Path |
|----------|-------------|
| Windows | `%TEMP%\claw-eyes\clipboard.png` |
| Linux | `/tmp/claw-eyes/clipboard.png` |
| macOS | `$TMPDIR/claw-eyes/clipboard.png` |

The directory is auto-created on first use. No manual setup needed unless you want a custom location.

目录会在首次使用时自动创建，无需手动设置（除非你想自定义位置）。

### Post-install Confirmation / 安装后确认

**This step is mandatory.** After installing this skill, the AI assistant MUST:

**此步骤必做。** 安装此技能后，AI 助手必须：

1. ✅ Tell the user the resolved save path (default or custom)
2. ✅ **Ask the user to confirm** if they want to keep that path or change it
3. ✅ If the user wants a different path, set `CLAW_EYES_SAVE_PATH` accordingly
4. ✅ Run the **Vision Capability Check** below to determine which analysis mode to use

Example interaction / 示例交互：

```
AI: "Claw Eyes 已安装！剪贴板图片将保存到：
     C:\Users\xxx\AppData\Local\Temp\claw-eyes\clipboard.png
     这个路径可以吗？还是你想换一个？"
User: "换成 D:\screenshots\clip.png 吧"
AI: [sets CLAW_EYES_SAVE_PATH env var] "搞定！已改为 D:\screenshots\clip.png"
```

### Vision Capability Check / 视觉能力检测

**Run this check after installation to determine available analysis mode.**

**安装后运行此检测，确定可用的分析模式。**

Check in this order / 按以下顺序检测：

```
Step 1: Check CLAW_EYES_API_KEY env var
  ├─ Set? → Run Step 2 (API validation)
  └─ Not set? → Check Step 3 (MCP availability)

Step 2: Validate API key (probe request)
  Execute this PowerShell to test the key works:

  $testBody = @{
      model = "<CLAW_EYES_VISION_MODEL or glm-4.6v-flash>"
      messages = @(
          @{ role = "user"; content = "hi" }
      )
      max_tokens = 5
  } | ConvertTo-Json -Depth 5
  $headers = @{
      "Authorization" = "Bearer <CLAW_EYES_API_KEY>"
      "Content-Type" = "application/json"
  }
  try {
      $resp = Invoke-RestMethod -Uri "<CLAW_EYES_API_URL>" -Method POST -Headers $headers -Body $testBody -TimeoutSec 15
      Write-Output "API_OK"
  } catch {
      Write-Output "API_ERROR: $($_.Exception.Message)"
  }

  ├─ API_OK → Mode A ready ✅ (vision will be tested on first use)
  └─ API_ERROR → Key invalid or endpoint unreachable, inform user

Step 3: Check MCP vision tool availability
  ├─ mcp_get_tool_description returns tool info? → Mode B ready ✅
  └─ No MCP vision tool found? → inform user (see below)

Step 4: No vision capability found at all
  → Tell the user:
     "⚠️ Claw Eyes needs a vision-capable API to analyze images. Please do ONE of:
      1. Get a free API key from:
         - 智谱 (open.bigmodel.cn) → glm-4.6v-flash (free, recommended, supports video/docs)
         - 硅基流动 (siliconflow.cn) → Qwen2.5-VL (free tier)
      2. Set it: set CLAW_EYES_API_KEY=your_key
      3. Or install a vision MCP server (e.g. @z_ai/mcp-server)
      4. Or run a local vision model via Ollama (llava, minicpm-v)
     Then reload this skill."
```

**Compatible API providers / 兼容的 API 提供商:**

| Provider | Base URL | Free Models | How to get key |
|----------|----------|-------------|----------------|
| 智谱 Zhipu | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4.6v-flash` (recommended) | open.bigmodel.cn 注册 |
| 硅基流动 SiliconFlow | `https://api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | siliconflow.cn 注册 |
| OpenAI | `https://api.openai.com/v1/chat/completions` | None (paid) | platform.openai.com |
| 本地 Ollama | `http://localhost:11434/v1/chat/completions` | `llava`, `minicpm-v` | No key needed |

**⚠️ Important: Not all models support vision!**
- ❌ Pure text models (GPT-3.5, glm-4-flash, Qwen2.5-7B etc.) CANNOT analyze images
- ✅ Vision models (glm-4.6v-flash, gpt-4o, Qwen2.5-VL, llava etc.) CAN analyze images
- The model name must contain vision capability: check provider docs before configuring

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

Resolve the save path and execute PowerShell to save clipboard image:

```powershell
$savePath = if ($env:CLAW_EYES_SAVE_PATH) { $env:CLAW_EYES_SAVE_PATH } else { Join-Path $env:TEMP 'claw-eyes\clipboard.png' }
$dir = Split-Path $savePath -Parent
if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$img = [System.Windows.Forms.Clipboard]::GetImage()
if ($img -ne $null) {
    $img.Save($savePath, [System.Drawing.Imaging.ImageFormat]::Png)
    Write-Output "OK:$savePath Size:$($img.Width)x$($img.Height)"
} else {
    Write-Output "NO_IMAGE"
}
```

- Output `OK:...` → Image found, proceed to step 2
- Output `NO_IMAGE` → No image in clipboard, remind user to screenshot first

### Step 2: Optimize Image / 第二步：图片优化（可选）

If the saved image is larger than **800KB**, auto-compress to reduce API transfer time:

```powershell
$fileSize = (Get-Item $savePath).Length
if ($fileSize -gt 819200) {
    Add-Type -AssemblyName System.Drawing
    $bmp = [System.Drawing.Image]::FromFile($savePath)
    $ratio = [Math]::Min(1920 / $bmp.Width, 1080 / $bmp.Height)
    if ($ratio -lt 1) {
        $newW = [int]($bmp.Width * $ratio)
        $newH = [int]($bmp.Height * $ratio)
        $newBmp = [System.Drawing.Bitmap]::new($newW, $newH)
        $g = [System.Drawing.Graphics]::FromImage($newBmp)
        $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
        $g.DrawImage($bmp, 0, 0, $newW, $newH)
        $newBmp.Save($savePath, [System.Drawing.Imaging.ImageFormat]::Png)
        $g.Dispose(); $newBmp.Dispose()
    }
    $bmp.Dispose()
    Write-Output "COMPRESSED"
} else {
    Write-Output "SKIP"
}
```

This step is optional. If compression is not needed or not possible, skip to Step 3.

### Step 3: Analyze Image / 第三步：分析图片

**Analysis strategy (pick one in priority order) / 分析策略（按优先级选择）:**

#### Mode A: Direct API (Recommended) / 模式 A：直连 API（推荐）

Call vision model API directly via `execute_command`. Response comes as command output → **guaranteed to reach AI context**.

通过 `execute_command` 直接请求视觉模型 API，响应作为命令输出 → **必定注入 AI 上下文**。

**Environment variables / 环境变量:**

| Variable | Default | Description |
|----------|---------|-------------|
| `CLAW_EYES_API_KEY` | (none) | Vision API key (e.g. Zhipu, SiliconFlow) |
| `CLAW_EYES_API_URL` | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | Vision API endpoint |
| `CLAW_EYES_VISION_MODEL` | `glm-4.6v-flash` | Vision model name |

**PowerShell script / PowerShell 脚本:**

```powershell
$imgPath = "<save_path>"
$bytes = [System.IO.File]::ReadAllBytes($imgPath)
$base64 = [Convert]::ToBase64String($bytes)
$dataUri = "data:image/png;base64,$base64"
$body = @{
    model = "<CLAW_EYES_VISION_MODEL or glm-4.6v-flash>"
    messages = @(
        @{
            role = "user"
            content = @(
                @{ type = "image_url"; image_url = @{ url = $dataUri } }
                @{ type = "text"; text = "<prompt based on CLAW_EYES_LANG>" }
            )
        }
    )
    max_tokens = 1024
} | ConvertTo-Json -Depth 10
$headers = @{
    "Authorization" = "Bearer <CLAW_EYES_API_KEY>"
    "Content-Type" = "application/json"
}
$resp = Invoke-RestMethod -Uri "<CLAW_EYES_API_URL>" -Method POST -Headers $headers -Body $body -TimeoutSec 60
$resp.choices[0].message.content
```

**Supported models / 支持的模型:**

| Provider | Model | Free? | Notes |
|----------|-------|-------|-------|
| 智谱 Zhipu | `glm-4.6v-flash` | ✅ Free | **Recommended**. Best Chinese support, 128K context, supports video/docs/OCR |
| 智谱 Zhipu | `glm-4v-flash` | ✅ Free | Older generation, still good |
| 硅基流动 SiliconFlow | `Qwen/Qwen2.5-VL-7B-Instruct` | ✅ Free tier | Domestic, fast |
| 智谱 Zhipu | `glm-4v` | Paid | Higher quality |

#### Mode B: MCP Tool (Fallback) / 模式 B：MCP 工具（备选）

If Direct API is not configured (`CLAW_EYES_API_KEY` not set), try MCP:

如果未配置 Direct API（`CLAW_EYES_API_KEY` 未设置），尝试 MCP：

```
mcp_call_tool: serverName="<CLAW_EYES_MCP_SERVER>", toolName="<CLAW_EYES_MCP_TOOL>"
arguments: {
    "image_source": "<save_path>",
    "prompt": "<concise prompt>"
}
```

⚠️ **Known issue**: On some platforms, MCP responses may not reach AI context. If the user reports seeing results but AI got nothing, suggest switching to Mode A.

#### Mode C: No Capability / 模式 C：无视觉能力

If neither Mode A nor Mode B is available:

如果 Mode A 和 Mode B 都不可用：

1. Tell the user: "当前没有可用的视觉分析能力，无法分析截图"
2. Ask the user to configure one of the options in the Vision Capability Check section
3. Suggest free options first (智谱 glm-4.6v-flash, 硅基流动 Qwen2.5-VL)
4. For local model users: suggest installing Ollama + a vision model (llava, minicpm-v)

### Step 4: Return Results / 第四步：返回分析结果

Return the analysis in natural language. Adapt response based on content:

- **Screenshot/UI** → Describe interface elements and visible info
- **Error message** → Provide diagnostic suggestions
- **Document/table** → Extract text and data
- **Code screenshot** → Recognize and reproduce code content

## File Structure / 文件结构

```
claw-eyes/
├── SKILL.md                    # This file / 本文件
├── scripts/
│   └── read_clipboard.py       # Python clipboard reader / Python 剪贴板读取脚本
├── README.md                   # Project README
├── LICENSE                     # MIT License
└── .gitignore
```

## Notes / 注意事项

- Image is overwritten on each use — no cleanup needed
- Windows-only in current version (Linux/macOS coming soon)
- If user hasn't screenshot yet, remind them: `Win + Shift + S` (Windows)
- The Python script (`scripts/read_clipboard.py`) supports Pillow with PowerShell fallback
- All env vars use `CLAW_EYES_` prefix — consistent across Claw platforms
- **Known issue**: On some platforms, MCP tool responses may not reach AI context. Direct API mode (Mode A) bypasses this by using `execute_command` to call vision API directly — response is guaranteed to reach AI context as command output.
- **Recommended setup**: Set `CLAW_EYES_API_KEY` to enable Direct API mode for reliable image analysis.
- **Never hardcode API keys in SKILL.md or any skill files.** All keys come from user-configured environment variables.

## Roadmap / 路线图

- [x] Direct API mode (bypass MCP, call vision model directly via execute_command)
- [x] Vision Capability Check (validate API key + detect vision support)
- [ ] Linux support (`xclip`/`wl-paste` clipboard access)
- [ ] macOS support (`osascript`/`pbpaste` clipboard access)
- [ ] Auto-detect available MCP vision tools (not just `zai`)
- [ ] Multi-image clipboard support (if multiple images copied)
- [ ] Clipboard history mode (analyze previously copied images)
