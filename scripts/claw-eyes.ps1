# claw-eyes.ps1 — Claw Eyes unified script
# All-in-one: clipboard read, image compress, vision API call, key validation
# Usage:
#   .\claw-eyes.ps1 -Action read      — Read clipboard image + auto-compress
#   .\claw-eyes.ps1 -Action analyze   — Send image to vision API
#   .\claw-eyes.ps1 -Action validate  — Test if API key/URL/model combo works
#
# Environment variables:
#   CLAW_EYES_SAVE_PATH     — Custom save path (default: %TEMP%\claw-eyes\clipboard.png)
#   CLAW_EYES_API_KEY       — Vision API key
#   CLAW_EYES_API_URL       — Vision API endpoint
#   CLAW_EYES_VISION_MODEL  — Vision model name
#   CLAW_EYES_LANG          — Prompt language (default: zh)

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("read", "analyze", "validate")]
    [string]$Action
)

$ErrorActionPreference = "Stop"

# --- Resolve save path ---
function Get-SavePath {
    if ($env:CLAW_EYES_SAVE_PATH) { return $env:CLAW_EYES_SAVE_PATH }
    return Join-Path $env:TEMP 'claw-eyes\clipboard.png'
}

# --- Read clipboard image and auto-compress ---
function Read-ClipboardImage {
    $savePath = Get-SavePath
    $dir = Split-Path $savePath -Parent
    if (!(Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }

    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    $img = [System.Windows.Forms.Clipboard]::GetImage()
    if ($null -eq $img) {
        Write-Output "NO_IMAGE"
        return
    }

    # Auto-compress if > 800KB
    $img.Save($savePath, [System.Drawing.Imaging.ImageFormat]::Png)
    $w = $img.Width
    $h = $img.Height
    $img.Dispose()

    $fileSize = (Get-Item $savePath).Length
    if ($fileSize -gt 819200) {
        $bmp = [System.Drawing.Image]::FromFile($savePath)
        $ratio = [Math]::Min(1920 / $bmp.Width, 1080 / $bmp.Height)
        if ($ratio -lt 1) {
            $newW = [int]($bmp.Width * $ratio)
            $newH = [int]($bmp.Height * $ratio)
            $newBmp = New-Object System.Drawing.Bitmap($newW, $newH)
            $g = [System.Drawing.Graphics]::FromImage($newBmp)
            $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
            $g.DrawImage($bmp, 0, 0, $newW, $newH)
            $newBmp.Save($savePath, [System.Drawing.Imaging.ImageFormat]::Png)
            $g.Dispose()
            $newBmp.Dispose()
            $w = $newW
            $h = $newH
        }
        $bmp.Dispose()
    }

    Write-Output "OK:$savePath Size:${w}x${h}"
}

# --- Send image to vision API ---
function Send-VisionRequest {
    $imgPath = Get-SavePath
    if (!(Test-Path $imgPath)) {
        Write-Output "ERROR:No image file found at $imgPath"
        return
    }

    if (!$env:CLAW_EYES_API_KEY -or !$env:CLAW_EYES_API_URL -or !$env:CLAW_EYES_VISION_MODEL) {
        Write-Output "ERROR:Missing config. Set CLAW_EYES_API_KEY, CLAW_EYES_API_URL, CLAW_EYES_VISION_MODEL"
        return
    }

    $lang = if ($env:CLAW_EYES_LANG) { $env:CLAW_EYES_LANG } else { "zh" }
    $prompt = if ($lang -eq "zh") { "请详细描述这张图片的内容。" } else { "Describe the content of this image in detail." }

    $bytes = [System.IO.File]::ReadAllBytes($imgPath)
    $base64 = [Convert]::ToBase64String($bytes)
    $dataUri = "data:image/png;base64,$base64"

    $body = @{
        model = $env:CLAW_EYES_VISION_MODEL
        messages = @(
            @{
                role = "user"
                content = @(
                    @{ type = "image_url"; image_url = @{ url = $dataUri } }
                    @{ type = "text"; text = $prompt }
                )
            }
        )
        max_tokens = 1024
    } | ConvertTo-Json -Depth 10

    $headers = @{
        "Authorization" = "Bearer $($env:CLAW_EYES_API_KEY)"
        "Content-Type" = "application/json"
    }

    try {
        $resp = Invoke-RestMethod -Uri $env:CLAW_EYES_API_URL -Method POST -Headers $headers -Body $body -TimeoutSec 60
        Write-Output $resp.choices[0].message.content
    } catch {
        $statusCode = $_.Exception.Response.StatusCode.value__
        if ($statusCode -eq 429) {
            Write-Output "RATE_LIMITED:API rate limit reached. Please wait a moment and try again."
        } else {
            Write-Output "ERROR:$($_.Exception.Message)"
        }
    }
}

# --- Validate API key ---
function Test-VisionApi {
    if (!$env:CLAW_EYES_API_KEY -or !$env:CLAW_EYES_API_URL -or !$env:CLAW_EYES_VISION_MODEL) {
        Write-Output "ERROR:Missing config. Set CLAW_EYES_API_KEY, CLAW_EYES_API_URL, CLAW_EYES_VISION_MODEL"
        return
    }

    $testBody = @{
        model = $env:CLAW_EYES_VISION_MODEL
        messages = @( @{ role = "user"; content = "hi" } )
        max_tokens = 5
    } | ConvertTo-Json -Depth 5

    $headers = @{
        "Authorization" = "Bearer $($env:CLAW_EYES_API_KEY)"
        "Content-Type" = "application/json"
    }

    try {
        $resp = Invoke-RestMethod -Uri $env:CLAW_EYES_API_URL -Method POST -Headers $headers -Body $testBody -TimeoutSec 15
        Write-Output "API_OK"
    } catch {
        Write-Output "API_ERROR:$($_.Exception.Message)"
    }
}

# --- Main dispatcher ---
switch ($Action) {
    "read"     { Read-ClipboardImage }
    "analyze"  { Send-VisionRequest }
    "validate" { Test-VisionApi }
}
