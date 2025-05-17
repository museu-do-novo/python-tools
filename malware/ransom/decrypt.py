import os
from cryptography.fernet import Fernet

# Caminho base dos arquivos criptografados
RootDir = r"/home/nad/Desktop/harpy_tools/py/system tools/ransomware/"

key_path = "key.key"

# Carrega a chave existente
def carregar_chave():
    if not os.path.exists(key_path):
        print("[!] Arquivo key.key não encontrado. Sem chave, sem festa.")
        exit(1)
    with open(key_path, "rb") as f:
        return f.read()

# Encontra arquivos com extensão .harpy
def encontrar_arquivos_criptografados(diretorio_base):
    arquivos_para_descriptografar = []

    for root, dirs, files in os.walk(diretorio_base):
        for file in files:
            if file.endswith(".666"):
                caminho_absoluto = os.path.abspath(os.path.join(root, file))
                arquivos_para_descriptografar.append(caminho_absoluto)

    return arquivos_para_descriptografar

# Descriptografa e restaura nome original
def descriptografar_arquivos(arquivos, fernet):
    for file_path in arquivos:
        try:
            with open(file_path, "rb") as f:
                dados_criptografados = f.read()

            dados_descriptografados = fernet.decrypt(dados_criptografados)

            # Sobrescreve com conteúdo original
            with open(file_path, "wb") as f:
                f.write(dados_descriptografados)

            # Remove extensão .666
            nome_original = file_path.replace(".666", "")
            os.rename(file_path, nome_original)

            print(f"[+] Descriptografado e restaurado: {nome_original}")

        except Exception as e:
            print(f"[!] Falha ao descriptografar {file_path}: {e}")

# Execução principal
if __name__ == "__main__":
    print("[🔓] DECRYPT MODE ATIVO")

    chave = carregar_chave()
    fernet = Fernet(chave)

    arquivos = encontrar_arquivos_criptografados(RootDir)

    if not arquivos:
        print("[!] Nenhum arquivo .666 encontrado.")
    else:
        descriptografar_arquivos(arquivos, fernet)
        print("[✅] Processo completo.")

