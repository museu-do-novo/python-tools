# builder.py
import os
import subprocess

APP_NAME = "chrome"
ENTRY_POINT = "main.py"
ICON = "chrome.ico"

def build():
    print("[*] Iniciando build...")
    cmd = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        f"--name={APP_NAME}",
        f"--icon={ICON}",
        ENTRY_POINT
    ]
    subprocess.run(cmd)
    print("[+] Build finalizada! Veja a pasta 'dist/'")

if __name__ == "__main__":
    build()
