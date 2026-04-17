#!/usr/bin/env python3
"""
claw-eyes.py — Claw Eyes unified script (v2.0.0)
Cross-platform clipboard image reader + vision API caller.
Supports Windows / Linux / macOS.

Usage:
  python claw-eyes.py read                — Read clipboard image + auto-compress
  python claw-eyes.py analyze             — Send image to vision API (default prompt)
  python claw-eyes.py analyze "prompt"    — Send image with custom prompt
  python claw-eyes.py validate            — Test if API key/URL/model combo works

Environment variables (or .env file in script directory):
  CLAW_EYES_SAVE_PATH     — Custom save path (default: <temp>/claw-eyes/clipboard.png)
  CLAW_EYES_API_KEY       — Vision API key
  CLAW_EYES_API_URL       — Vision API endpoint (OpenAI-compatible chat/completions)
  CLAW_EYES_VISION_MODEL  — Vision model name
  CLAW_EYES_LANG          — Prompt language: zh (default) / en

Config priority: env vars > .env file > defaults
"""

import sys
import os
import json
import base64
import tempfile
import platform
import subprocess
from pathlib import Path
from io import BytesIO

# Fix Windows GBK stdout — API responses may contain emoji/unicode
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr.encoding and sys.stderr.encoding.lower() != "utf-8":
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from PIL import Image, ImageGrab
except ImportError:
    print("ERROR:Pillow not installed. Run: pip install Pillow")
    sys.exit(1)

# --- Load .env file (env vars take precedence) ---
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_ENV_FILE = os.path.join(_SCRIPT_DIR, ".env")

if os.path.exists(_ENV_FILE):
    with open(_ENV_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                key, _, value = line.partition("=")
                key = key.strip()
                value = value.strip().strip("'\"")
                # Only set if not already in environment (env vars > .env)
                if key and key not in os.environ:
                    os.environ[key] = value

# --- Constants ---
MAX_FILE_SIZE = 800 * 1024  # 800KB threshold
MAX_DIMENSIONS = (1920, 1080)


def get_save_path():
    """Resolve image save path from env or default."""
    custom = os.environ.get("CLAW_EYES_SAVE_PATH", "").strip()
    if custom:
        return custom
    return os.path.join(tempfile.gettempdir(), "claw-eyes", "clipboard.png")


def _read_clipboard_windows_macos():
    """Read clipboard via Pillow ImageGrab (Windows + macOS)."""
    try:
        img = ImageGrab.grabclipboard()
        if isinstance(img, Image.Image):
            return img
    except Exception:
        pass
    return None


def _read_clipboard_linux():
    """Read clipboard via xclip (X11) or wl-paste (Wayland)."""
    # Try xclip first (X11)
    try:
        result = subprocess.run(
            ["xclip", "-selection", "clipboard", "-t", "image/png", "-o"],
            capture_output=True, timeout=5
        )
        if result.returncode == 0 and result.stdout:
            return Image.open(BytesIO(result.stdout))
    except FileNotFoundError:
        pass
    except Exception:
        pass

    # Try wl-paste (Wayland)
    try:
        result = subprocess.run(
            ["wl-paste", "--type", "image/png"],
            capture_output=True, timeout=5
        )
        if result.returncode == 0 and result.stdout:
            return Image.open(BytesIO(result.stdout))
    except FileNotFoundError:
        pass
    except Exception:
        pass

    return None


def read_clipboard():
    """Read clipboard image, auto-compress if needed, save to disk."""
    save_path = get_save_path()
    save_dir = os.path.dirname(save_path)
    os.makedirs(save_dir, exist_ok=True)

    system = platform.system()

    if system in ("Windows", "Darwin"):
        img = _read_clipboard_windows_macos()
    elif system == "Linux":
        img = _read_clipboard_linux()
    else:
        print(f"ERROR:Unsupported platform: {system}")
        return

    if img is None:
        print("NO_IMAGE")
        return

    # Normalize mode
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")

    w, h = img.size

    # Save first to check file size
    img.save(save_path, "PNG")
    file_size = os.path.getsize(save_path)

    # Auto-compress if exceeds threshold
    if file_size > MAX_FILE_SIZE:
        ratio = min(MAX_DIMENSIONS[0] / w, MAX_DIMENSIONS[1] / h)
        if ratio < 1:
            new_w = int(w * ratio)
            new_h = int(h * ratio)
            img = img.resize((new_w, new_h), Image.LANCZOS)
            img.save(save_path, "PNG")
            w, h = new_w, new_h

    print(f"OK:{save_path} Size:{w}x{h}")


def send_vision_request():
    """Send saved image to vision API (OpenAI-compatible)."""
    import urllib.request
    import urllib.error

    save_path = get_save_path()
    if not os.path.exists(save_path):
        print(f"ERROR:No image file found at {save_path}")
        return

    api_key = os.environ.get("CLAW_EYES_API_KEY", "").strip()
    api_url = os.environ.get("CLAW_EYES_API_URL", "").strip()
    model = os.environ.get("CLAW_EYES_VISION_MODEL", "").strip()

    if not api_key or not api_url or not model:
        print("ERROR:Missing config. Set CLAW_EYES_API_KEY, CLAW_EYES_API_URL, CLAW_EYES_VISION_MODEL")
        return

    # Prompt: custom from CLI args, or default by LANG
    custom_prompt = " ".join(sys.argv[2:]).strip() if len(sys.argv) > 2 else ""
    if custom_prompt:
        prompt = custom_prompt
    else:
        lang = os.environ.get("CLAW_EYES_LANG", "zh").strip()
        prompt = "请详细描述这张图片的内容。" if lang == "zh" else "Describe the content of this image in detail."

    # Read and Base64 encode
    with open(save_path, "rb") as f:
        img_bytes = f.read()
    b64 = base64.b64encode(img_bytes).decode("utf-8")
    data_uri = f"data:image/png;base64,{b64}"

    body = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": data_uri}},
                    {"type": "text", "text": prompt}
                ]
            }
        ],
        "max_tokens": 1024
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            content = result["choices"][0]["message"]["content"]
            print(content)
    except urllib.error.HTTPError as e:
        err_body = ""
        try:
            err_body = e.read().decode("utf-8", errors="replace")
        except Exception:
            pass
        print(f"ERROR:HTTP {e.code} — {err_body[:500]}")
    except Exception as e:
        print(f"ERROR:{e}")


def validate_api():
    """Quick test: send a minimal text request to verify key/url/model."""
    import urllib.request
    import urllib.error

    api_key = os.environ.get("CLAW_EYES_API_KEY", "").strip()
    api_url = os.environ.get("CLAW_EYES_API_URL", "").strip()
    model = os.environ.get("CLAW_EYES_VISION_MODEL", "").strip()

    if not api_key or not api_url or not model:
        print("ERROR:Missing config. Set CLAW_EYES_API_KEY, CLAW_EYES_API_URL, CLAW_EYES_VISION_MODEL")
        return

    body = {
        "model": model,
        "messages": [{"role": "user", "content": "hi"}],
        "max_tokens": 5
    }

    req = urllib.request.Request(
        api_url,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print("API_OK")
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="replace")
        print(f"API_ERROR:HTTP {e.code} — {err_body[:300]}")
    except Exception as e:
        print(f"API_ERROR:{e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python claw-eyes.py <read|analyze|validate> [custom_prompt]")
        sys.exit(1)

    action = sys.argv[1].lower()

    if action == "read":
        read_clipboard()
    elif action == "analyze":
        send_vision_request()
    elif action == "validate":
        validate_api()
    else:
        print(f"ERROR:Unknown action '{action}'. Use read, analyze, or validate.")
        sys.exit(1)


if __name__ == "__main__":
    main()
