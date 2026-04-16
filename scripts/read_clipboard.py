"""
Read Windows clipboard image and save to local file.
Usage: python read_clipboard.py [output_path]
Default path is determined by CLIPBOARD_SAVE_PATH env var, falling back to C:\\tmp\\_clipboard\\clipboard.png
"""
import sys
import os


def get_default_path():
    """Get save path from env var or use default."""
    return os.environ.get(
        "CLIPBOARD_SAVE_PATH",
        r"C:\tmp\_clipboard\clipboard.png"
    )


def read_clipboard(output_path=None):
    if output_path is None:
        output_path = get_default_path()

    # Ensure directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        from PIL import ImageGrab
    except ImportError:
        # Fallback: use PowerShell
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
        return

    img = ImageGrab.grabclipboard()
    if img is None:
        print("NO_IMAGE")
        return

    img.save(output_path, 'PNG')
    print(f"OK:{output_path}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    read_clipboard(path)
