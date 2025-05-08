import os
import platform

def get_desktop_path():
    sistema = platform.system()
    if sistema == "Windows":
        return os.path.join(os.getenv("USERPROFILE"), "Desktop")
    elif sistema in ["Linux", "Darwin"]:  # Darwin = macOS
        return os.path.join(os.path.expanduser("~"), "Desktop")
    else:
        return None

desktop_path = get_desktop_path()

if desktop_path:
    pasta = os.path.join(desktop_path, "dan was here")
    print(f"[i] Pasta será criada em: {pasta}")
    
    try:
        os.mkdir(pasta)
        print(f"[+] criação da pasta: {pasta}")
    except Exception as e:
        print(f"[-] Erro ao criar a pasta: {e}")
else:
    print("[-] Não foi possível determinar a pasta Desktop.")
