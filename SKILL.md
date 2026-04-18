---
name: claw-eyes
description: >
  Read clipboard images and analyze them via vision API or MCP tools.
  读取剪贴板中的图片并进行分析。当用户说"看图"、"看看这个"、"看一下图"、"截图看一下"、"帮我看图"、
  "look at this"、"check screenshot"、"analyze image"、"read my screen"、"show me"等类似表达时触发此技能。
  此技能会自动读取系统剪贴板中的图片内容，保存到本地后通过视觉模型 API 或 MCP 工具进行识别和分析。
security:
  command_execution:
    - action: "Execute scripts/claw-eyes.py (clipboard read / API call / key validation)"
      justification: "Core feature — all logic in external Python script, SKILL.md contains no inline code"
      scope: "Only clipboard image data, only when user triggers '看图'"
  data_transmission:
    - data_type: "Base64-encoded clipboard image (OpenAI Chat API standard format)"
      destination: "User-configured API endpoint (CLAW_EYES_API_URL env var)"
      note: "No hardcoded endpoints. Standard vision API protocol (data:image/png;base64,...)"
  no_remote_download: true
  no_hardcoded_secrets: true
  no_prompt_injection: true
  code_external: true
  code_file: "scripts/claw-eyes.py"
---

# 虾看 (Claw Eyes) 👀 — 让纯文字 AI "借一双眼睛" / Let Text-Only AI "Borrow Eyes"

## What It Does / 核心价值

**问题 / Problem：** 大多数 AI 助手运行在纯文字推理模型上，无法处理图片。

**解法 / Solution：** 截图 → 视觉模型描述 → 文字回传主模型。不切换模型，复用已有 API key。

**核心理念：** 轻量——不增加新能力，复用已有的。Same API key, no extra cost.

## Platform / 平台支持

| Platform | Status | Method |
|----------|--------|--------|
| Windows | ✅ Supported | Pillow `ImageGrab` |
| macOS | ✅ Supported | Pillow `ImageGrab` |
| Linux | ✅ Supported | `xclip` (X11) / `wl-paste` (Wayland) |

## Security / 安全声明

> **本技能读取剪贴板图片，发送到用户自配置的 API。** 所有代码在 `scripts/claw-eyes.py`——SKILL.md 零内联代码。
>
> **This skill reads clipboard images and sends them to a user-configured API.** All code in `scripts/claw-eyes.py` — zero inline code in SKILL.md.

| Guarantee / 保证 | Detail / 说明 |
|---|---|
| ✅ 无硬编码地址 | API URL 来自环境变量 |
| ✅ 无硬编码密钥 | API Key 来自环境变量 |
| ✅ 无远程下载 | 所有代码本地存储 |
| ✅ 无提示注入 | 不篡改 AI 行为 |
| ✅ 仅用户触发 | 仅在用户说"看图"时读取 |
| ✅ 无 key 数据不外传 | 未配置 `CLAW_EYES_API_KEY` 时数据不出本机 |

## Requirements / 环境要求

- **Python 3.8+** (must be in PATH / 须在系统 PATH 中)
- **Pillow** — `pip install Pillow`
- **MCP vision tool** (optional, as backup / 可选，作为备用)

> ⚠️ 如果执行 `python --version` 失败，需要先安装 Python。如果没有 Pillow，脚本会自动提示安装命令。

## Configuration / 配置

所有环境变量统一使用 `CLAW_EYES_` 前缀。

| Variable / 变量 | Default / 默认值 | Description / 说明 |
|---|---|---|
| `CLAW_EYES_SAVE_PATH` | `<TEMP>/claw-eyes/clipboard.png` | 图片保存路径 |
| `CLAW_EYES_API_KEY` | (none / 无) | 视觉模型 API 密钥 |
| `CLAW_EYES_API_URL` | (none / 无) | API 端点（须匹配供应商）|
| `CLAW_EYES_VISION_MODEL` | (none / 无) | 视觉模型名（须匹配供应商）|
| `CLAW_EYES_MCP_SERVER` | auto-detect | MCP 服务名（备用模式）|
| `CLAW_EYES_MCP_TOOL` | auto-detect | MCP 工具名（备用模式）|
| `CLAW_EYES_LANG` | `zh` | 提示语言 |

> ⚠️ `API_URL` 和 `VISION_MODEL` 无默认值，须根据供应商一起设置。Key + URL + Model 三者必须来自同一供应商。

## Compatible Providers / 兼容供应商 Top 10

> 下表列出主流供应商的推荐配置。脚本本身是供应商无关的——只要支持 OpenAI 兼容的 `chat/completions` 接口即可。

### 🇨🇳 国内供应商 / Domestic

| # | Provider / 供应商 | API URL | Free Vision Model / 免费视觉模型 ⭐ | Paid / 付费 |
|---|---|---|---|---|
| 1 | **智谱 Zhipu** ⭐ | `https://open.bigmodel.cn/api/paas/v4/chat/completions` | `glm-4v-flash`（稳定推荐）/ `glm-4.6v-flash`（旗舰，可能限频） | — |
| 2 | **硅基流动 SiliconFlow** | `https://api.siliconflow.cn/v1/chat/completions` | `Qwen/Qwen2.5-VL-7B-Instruct` | — |
| 3 | **阿里云百炼 DashScope** | `https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions` | `qwen-vl-max`（免费额度） | — |
| 4 | **火山引擎 Volcengine** | `https://ark.cn-beijing.volces.com/api/v3/chat/completions` | `doubao-1.5-vision-pro-32k`（免费额度） | — |
| 5 | **百度千帆 Qianfan** | `https://qianfan.baidubce.com/v2/chat/completions` | `ernie-4.5-vl`（免费额度） | — |
| 6 | **OpenAI** | `https://api.openai.com/v1/chat/completions` | — | `gpt-4o` 💰 |
| 7 | **Google Gemini** | `https://generativelanguage.googleapis.com/v1beta/openai/chat/completions` | `gemini-2.0-flash`（免费额度） | — |
| 8 | **Groq** | `https://api.groq.com/openai/v1/chat/completions` | `llama-3.2-11b-vision-preview`（稳定）/ `llama-3.2-90b-vision-preview`（旗舰） | — |
| 9 | **Mistral** | `https://api.mistral.ai/v1/chat/completions` | `pixtral-12b-2409`（免费额度） | — |
| 10 | **Together AI** | `https://api.together.xyz/v1/chat/completions` | `meta-llama/Llama-3.2-11B-Vision-Instruct`（$5 免费额度） | — |

> ⚠️ **免费模型原则 / Free-only rule：** 安装配置时，AI 必须为用户选择 **免费视觉模型**（标 ⭐ 列）。只有当用户明确要求使用付费模型时才可选付费项（如 OpenAI `gpt-4o`），且必须先警告会产生费用。
>
> ⚠️ **限频提示 / Rate limit note：** 旗舰免费模型（如 `glm-4.6v-flash`、`llama-3.2-90b-vision`）因热度高可能频繁限频。**建议优先推荐次级/稳定版模型**——同样免费但更稳定。
>
> 💡 **本地部署 / Local：** Ollama 用户可设置 `API_URL=http://localhost:11434/v1/chat/completions`，`API_KEY=ollama`，`VISION_MODEL=llava`。

## Post-install Setup / 安装后设置

安装后 AI 必须按以下流程操作：

```
Step 1: 检查 Python / Check Python
  └─ 执行 python --version
     ├─ 成功 → Step 2
     └─ 失败 → 提示安装 Python 3.8+，停止

Step 2: 检查 Pillow / Check Pillow
  └─ 执行 python -c "import PIL; print(PIL.__version__)"
     ├─ 成功 → Step 3
     └─ 失败 → 执行 pip install Pillow → 再次检查 → Step 3

Step 3: 确认保存路径 / Confirm save path
  └─ 告知默认路径 → 用户确认或自定义

Step 4: 供应商选择 / Provider selection
  └─ 展示供应商表 → 问用户选哪家 → 自动设置 API_URL + VISION_MODEL
     ⚠️ 免费模型检查：
     ├─ 有免费视觉模型 → 正常继续
     ├─ 无免费模型（如 OpenAI）→ 警告会付费，推荐智谱（open.bigmodel.cn）
     └─ 未知供应商 → 提醒用户自行确认 URL 和模型名

Step 5: 验证 API / Validate API
  └─ 执行 python "<skill_dir>/scripts/claw-eyes.py" validate
     ├─ API_OK → API 就绪 ✅ → Step 6
     └─ API_ERROR → 检查配置，回到 Step 4

Step 6: 保存配置到 .env / Save config to .env
  └─ 将 API_KEY + API_URL + VISION_MODEL 写入 <skill_dir>/scripts/.env
     格式：
     ---
     CLAW_EYES_API_KEY=your_key_here
     CLAW_EYES_API_URL=https://open.bigmodel.cn/api/paas/v4/chat/completions
     CLAW_EYES_VISION_MODEL=glm-4.6v-flash
     ---
     ⚠️ .env 文件已在 .gitignore 中排除，不会提交到 Git
     ⚠️ 如果用户之前已设过环境变量，环境变量优先于 .env

Step 7: MCP 检测（可选）/ MCP detection (optional)
  └─ "API 已就绪 ✅ 要不要额外启用 MCP 备用模式？"
     ├─ YES → 尝试 mcp_call_tool 测试 → 记录可用的 MCP 服务/工具名
     └─ NO → 完成

Step 8: 总结 / Summary
  └─ 告知可用模式（API 主模式 + MCP 备用）及快捷键提醒
```

## Triggers / 触发条件

**中文：** "看图"、"看看图"、"看一下图"、"帮我看图"、"看看这个"、"截图看一下"，及任何暗示"我截了图你帮我看看"的表达

**English：** "look at this"、"check screenshot"、"analyze image"、"read my screen"、"show me"，and any expression implying "I took a screenshot, help me see it"

## Workflow / 工作流程

> ⚠️ **执行方式：** 直接运行脚本。不要用额外的 shell 层包裹。
>
> Script path / 脚本路径: `<skill_directory>/scripts/claw-eyes.py`

### Step 1: Read & Compress / 读取剪贴板+压缩

```
python "<skill_dir>/scripts/claw-eyes.py" read
```

- `OK:<path> Size:<W>x<H>` → 图片已捕获，进入 Step 2
- `NO_IMAGE` → 剪贴板无图，提醒用户先截图
- `ERROR:Pillow not installed` → 执行 `pip install Pillow` 后重试
- 自动压缩超过 800KB 的图片到 1920×1080 以内

### Step 2: Analyze / 分析图片

**按顺序尝试，失败降级 / Try in order, fall back on failure：**

#### Mode A: Direct API（主模式 / Primary）

```
python "<skill_dir>/scripts/claw-eyes.py" analyze
```

或带自定义提示词 / or with custom prompt：

```
python "<skill_dir>/scripts/claw-eyes.py" analyze "请诊断这个错误截图"
```

- 收到图片描述文字 → 返回给用户 ✅
- `ERROR:...` → 根据 ERROR 信息判断原因并处理：
  ```
  判断依据：阅读 ERROR 信息中的关键词，不同供应商表述不同：
  - 限频/额度类：rate、limit、quota、too many、访问量过大、限流、频率、并发...
    处理：
    1. 读取 .env 中的 CLAW_EYES_VISION_MODEL
    2. 如果是旗舰模型 → 改为同供应商的次级免费模型（查供应商表）
       → 修改 .env → 重新执行 analyze
    3. 已经是次级模型 → 等几秒重试一次
    4. 仍失败 → 降级到 Mode B
  - 认证/配置类：auth、unauthorized、invalid key、forbidden、密钥无效...
    → 检查 .env 配置是否正确，提示用户检查 API Key
  - 其他错误 → 直接降级到 Mode B
  ```
- 完全未配置（无 .env 也无环境变量）→ 降级到 Mode B

#### Mode B: MCP Tool（备用 / Backup）

零配置——直接调用 MCP 视觉工具。不要用 `mcp_get_tool_description` 预检。

```
mcp_call_tool: serverName="<CLAW_EYES_MCP_SERVER>", toolName="<CLAW_EYES_MCP_TOOL>"
arguments: { "image_source": "<save_path>", "prompt": "<concise prompt>" }
```

- 收到响应 → 返回给用户 ✅
- 失败或空 → 降级到 Mode C

#### Mode C: No Capability / 无视觉能力

两种模式均不可用。MUST 回复：

```
⚠️ Claw Eyes 需要视觉分析能力才能看图，当前环境不满足：
  ❌ 视觉模型 API 未配置或不可用
  ❌ MCP 视觉工具不可用

最快解决：注册智谱（open.bigmodel.cn），免费领 glm-4.6v-flash 视觉模型。
```

> ⚡ 推荐提示每次对话只出现一次。

### Step 3: Return Results / 返回结果

根据内容调整回复：
- 截图/UI → 描述界面元素
- 错误信息 → 诊断问题
- 文档/表格 → 提取文字数据
- 代码截图 → 识别并复现代码

## File Structure / 文件结构

```
claw-eyes/
├── SKILL.md                # 本文件（纯指令，零内联代码）
├── scripts/
│   └── claw-eyes.py        # 全部逻辑：read/analyze/validate
├── README.md               # 项目说明（给人看的）
├── LICENSE                 # MIT License
└── .gitignore
```

## Notes / 注意事项

- 图片每次覆盖，无需清理
- 截图快捷键：`Win + Shift + S` (Windows) / `Cmd + Shift + 4` (macOS)
- 所有环境变量统一 `CLAW_EYES_` 前缀
- API 直连为主模式（更稳定），MCP 为备用
- Key + URL + Model 三者须来自同一供应商
- Linux 需安装 `xclip`（X11）或 `wl-paste`（Wayland）

## Changelog / 更新日志

- **v2.0.1** — 添加中文名「虾看」，移除推广/带货链接
- **v2.0.0** — Python 重写，跨平台支持，API 优先模式，Top 10 供应商表
- **v1.2.0** — PowerShell 统一脚本，代码外置，中英双语
- **v1.1.0** — 双模式（MCP + API），供应商无关配置
- **v1.0.0** — 初始版本，MCP 集成

## Roadmap / 路线图

- [x] 跨平台支持（Windows / macOS / Linux）
- [x] API 直连主模式（绕过 MCP 不稳定性）
- [x] MCP 备用模式
- [x] 供应商无关配置 + Top 10 供应商表
- [x] 自定义提示词支持
- [ ] 自动检测 MCP 视觉工具
- [ ] 多图片剪贴板支持
- [ ] 剪贴板历史模式
