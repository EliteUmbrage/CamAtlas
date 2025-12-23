#!/usr/bin/env python3

import subprocess
import sys

packages = [
    "requests",
    "beautifulsoup4",
    "rich",
    "prompt_toolkit"
]

print("=== CamAtlas Setup ===")
print("The following Python packages are required:\n")
for pkg in packages:
    print(f"- {pkg}")
print("\nInstalling packages...\n")

# Install each package
for pkg in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

print("\n✅ All packages installed successfully!")
print("You can now run CamAtlas with: python3 camatlas_tui.py")

