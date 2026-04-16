"""
Read system clipboard image and save to local file.
Supports Windows (current), Linux and macOS (planned).

Usage: python read_clipboard.py [output_path]
Default path is determined by CLAW_EYES_SAVE_PATH env var,
falling back to OS-specific defaults.
"""
import sys
import os
import platform


def get_default_path():
    """Get save path from env var or use OS-specific default."""
    # Env var takes priority
    env_path = os.environ.get("CLAW_EYES_SAVE_PATH")
    if env_path:
        return env_path

    # OS-specific defaults
    system = platform.system()
    if system == "Windows":
        return os.path.join(os.environ.get("TEMP", "C:\\tmp"), "_clipboard", "clipboard.png")
    elif system == "Darwin":  # macOS
        return "/tmp/claw-eyes/clipboard.png"
    else:  # Linux
        return "/tmp/claw-eyes/clipboard.png"


def read_clipboard_windows(output_path):
    """Read clipboard on Windows via PowerShell."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        from PIL import ImageGrab
        img = ImageGrab.grabclipboard()
        if img is None:
            print("NO_IMAGE")
            return
        img.save(output_path, 'PNG')
        print(f"OK:{output_path}")
        return
    except ImportError:
        pass

    # Fallback: PowerShell
    import subprocess
    result = subprocess.run(
        ['powershell', '-Command',
         "Add-Type -AssemblyName System.Windows.Forms; "
         "Add-Type -AssemblyName System.Drawing; "
         "$img = [System.Windows.Forms.Clipboard]::GetImage(); "
         "if ($img -ne $null) { "
         f"$img.Save('{output_path}', [System.Drawing.Imaging.ImageFormat]::Png); "
         "Write-Output 'OK' "
         "} else { Write-Output 'NO_IMAGE' }"],
        capture_output=True, text=True, timeout=10
    )
    print(result.stdout.strip())


def read_clipboard_macos(output_path):
    """Read clipboard on macOS (planned)."""
    # TODO: Implement via osascript or pbpaste + png paste
    print("ERROR:macOS not yet supported")
    print("HINT:macOS support is on the roadmap. See GitHub Issues.")


def read_clipboard_linux(output_path):
    """Read clipboard on Linux (planned)."""
    # TODO: Implement via xclip -selection clipboard -t image/png -o
    # or wl-paste for Wayland
    print("ERROR:Linux not yet supported")
    print("HINT:Linux support is on the roadmap. See GitHub Issues.")


def read_clipboard(output_path=None):
    if output_path is None:
        output_path = get_default_path()

    system = platform.system()
    if system == "Windows":
        read_clipboard_windows(output_path)
    elif system == "Darwin":
        read_clipboard_macos(output_path)
    else:
        read_clipboard_linux(output_path)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    read_clipboard(path)
