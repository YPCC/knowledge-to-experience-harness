#!/usr/bin/env python3
"""
Cross-platform setup script for the Knowledge-to-Experience Harness.

Detects macOS or Windows and installs requisite software:
  - Python packages: pdfplumber, python-pptx
  - ffmpeg (via Homebrew on macOS, winget/chocolatey on Windows, or guidance)
  - Optional: Node.js (for the React consumption platform)

Usage (from repository root):
  python3 scripts/setup_environment.py

On Windows you can also run:
  py scripts/setup_environment.py
"""

import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REQUIREMENTS = ["pdfplumber", "python-pptx"]

def run(cmd, check=False, capture=True):
    try:
        result = subprocess.run(
            cmd,
            shell=isinstance(cmd, str),
            check=check,
            capture_output=capture,
            text=True,
            timeout=300,
        )
        return result.returncode == 0, (result.stdout or "") + (result.stderr or "")
    except Exception as e:
        return False, str(e)

def which(name):
    return shutil.which(name) is not None

def detect_os():
    system = platform.system().lower()
    if system == "darwin":
        return "macos"
    if system == "windows":
        return "windows"
    if system == "linux":
        return "linux"
    return "unknown"

def check_python():
    print(f"Python: {sys.version.split()[0]} ({sys.executable})")
    return True

def ensure_pip_packages():
    print("\n=== Python packages ===")
    missing = []
    for pkg in REQUIREMENTS:
        ok, _ = run([sys.executable, "-c", f"import {pkg.replace('-', '_')}"])
        if not ok:
            missing.append(pkg)
        else:
            print(f"  ✓ {pkg}")
    if missing:
        print(f"  Installing: {', '.join(missing)}")
        ok, out = run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"] + missing)
        if ok:
            print("  ✓ Packages installed")
        else:
            print(f"  ✗ pip install failed:\n{out}")
            return False
    return True

def ensure_ffmpeg_macos():
    if which("ffmpeg"):
        print("  ✓ ffmpeg already installed")
        return True
    print("  ffmpeg not found. Attempting Homebrew…")
    if which("brew"):
        ok, out = run("brew install ffmpeg")
        if ok and which("ffmpeg"):
            print("  ✓ ffmpeg installed via Homebrew")
            return True
        print(f"  brew install failed or ffmpeg still missing:\n{out[:500]}")
    print("  Please install ffmpeg manually:")
    print("    brew install ffmpeg")
    print("  or download from https://ffmpeg.org/download.html")
    return False

def ensure_ffmpeg_windows():
    if which("ffmpeg"):
        print("  ✓ ffmpeg already installed")
        return True
    print("  ffmpeg not found. Trying winget…")
    if which("winget"):
        ok, out = run("winget install --id Gyan.FFmpeg -e --accept-source-agreements --accept-package-agreements")
        if ok or which("ffmpeg"):
            print("  ✓ ffmpeg installed via winget (restart terminal if not in PATH)")
            return True
        print(f"  winget result: {out[:400]}")
    if which("choco"):
        print("  Trying Chocolatey…")
        ok, _ = run("choco install ffmpeg -y")
        if ok or which("ffmpeg"):
            print("  ✓ ffmpeg installed via Chocolatey")
            return True
    print("  Please install ffmpeg manually:")
    print("    winget install Gyan.FFmpeg")
    print("  or download a static build from https://www.gyan.dev/ffmpeg/builds/")
    print("  and add the bin folder to your PATH.")
    return False

def ensure_ffmpeg_linux():
    if which("ffmpeg"):
        print("  ✓ ffmpeg already installed")
        return True
    print("  ffmpeg not found. On Debian/Ubuntu try:")
    print("    sudo apt update && sudo apt install -y ffmpeg")
    print("  On Fedora: sudo dnf install ffmpeg")
    return False

def ensure_node():
    print("\n=== Optional: Node.js (for React platform) ===")
    if which("node") and which("npm"):
        ok, out = run("node --version")
        ver = out.strip() if ok else "unknown"
        print(f"  ✓ Node.js {ver}")
        return True
    system = detect_os()
    if system == "macos" and which("brew"):
        print("  Installing Node.js via Homebrew…")
        ok, _ = run("brew install node")
        if ok and which("node"):
            print("  ✓ Node.js installed")
            return True
    if system == "windows" and which("winget"):
        print("  Installing Node.js via winget…")
        ok, _ = run("winget install --id OpenJS.NodeJS.LTS -e --accept-source-agreements --accept-package-agreements")
        if ok or which("node"):
            print("  ✓ Node.js installed (restart terminal if needed)")
            return True
    print("  Node.js not found. Optional — only needed for the React consumption platform.")
    print("  Install from https://nodejs.org/ or via your package manager.")
    return True  # non-blocking

def ensure_dirs():
    print("\n=== Directories ===")
    for d in ["uploads", "generated", "generator-ui"]:
        p = ROOT / d
        p.mkdir(exist_ok=True)
        print(f"  ✓ {p.relative_to(ROOT)}")
    return True

def main():
    print("Knowledge-to-Experience Harness — Environment Setup")
    print("=" * 55)
    system = detect_os()
    print(f"Detected OS: {system} ({platform.platform()})")
    print(f"Repository root: {ROOT}\n")

    check_python()
    ok = ensure_pip_packages()

    print("\n=== ffmpeg ===")
    if system == "macos":
        ensure_ffmpeg_macos()
    elif system == "windows":
        ensure_ffmpeg_windows()
    else:
        ensure_ffmpeg_linux()

    ensure_node()
    ensure_dirs()

    print("\n=== Summary ===")
    print("Core packages:", "ok" if ok else "check above")
    print("ffmpeg:", "found" if which("ffmpeg") else "missing (see notes above)")
    print("\nNext steps:")
    print("  python3 scripts/generator_server.py")
    print("  then open http://localhost:8765")
    print("\nDone.")

if __name__ == "__main__":
    main()
