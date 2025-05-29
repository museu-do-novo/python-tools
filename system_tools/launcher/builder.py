import os
import subprocess

APP_NAME = "LauncherWindows"
ICON_PATH = "launcher.ico"  # Use o ícone que quiser (deixe esse arquivo na mesma pasta)
SCRIPT = "launcher.py"

def build_exe():
    comando = [
        "pyinstaller",
        "--noconfirm",
        "--onefile",  # gera 1 único .exe
        "--windowed",  # sem console
        f"--name={APP_NAME}",
    ]

    if os.path.exists(ICON_PATH):
        comando.append(f"--icon={ICON_PATH}")
    else:
        print("[!] Ícone não encontrado. Continuando sem ícone...")

    comando.append(SCRIPT)

    print("[+] Iniciando compilação com PyInstaller...")
    subprocess.run(comando)

if __name__ == "__main__":
    build_exe()

