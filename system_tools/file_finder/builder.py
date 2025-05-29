import os
import subprocess
import sys
from pathlib import Path

def build_executable():
    # Verifica se o PyInstaller está instalado
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller não está instalado. Instalando agora...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Configurações do build
    app_name = "FileFinder"
    script_path = "file_finder.py"  # Substitua pelo nome do seu arquivo principal
    icon_path = "file_finder.ico"   # Caminho para o ícone
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        f"--name={app_name}",
        f"--icon={icon_path}",
        "--add-data", f"{icon_path};.",  # Inclui o ícone nos recursos
        "--clean",
        script_path
    ]
    
    # Executa o comando
    print("Iniciando a construção do executável...")
    subprocess.call(cmd)
    
    # Move o executável para a raiz do projeto
    dist_path = Path("dist") / f"{app_name}.exe"
    if dist_path.exists():
        target_path = Path(f"{app_name}.exe")
        if target_path.exists():
            target_path.unlink()
        dist_path.rename(target_path)
        print(f"Executável criado com sucesso: {target_path}")
    else:
        print("Erro: O executável não foi gerado corretamente.")

if __name__ == "__main__":
    build_executable()
