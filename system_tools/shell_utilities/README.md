Repositório: shell_utilities

Descrição:
Um conjunto de ferramentas para testes de penetração éticos, auditorias de segurança e simulação de ataques controlados. Desenvolvido para profissionais de segurança, pentesters e entusiastas de TI.

⚠️ AVISO LEGAL:
Use apenas em sistemas onde você tem permissão explícita. O uso não autorizado é ilegal e pode resultar em consequências jurídicas.
📦 Estrutura do Projeto
bash

.
├── builder.py               # Script para compilar o projeto em executável
├── malware.py               # Ferramentas de simulação de ataques (renomeie para pentest_tools.py)
├── main.py                  # Ponto de entrada do toolkit
├── shell_utilities.py       # Utilitários de sistema (comandos personalizados)
├── file_handler.py          # Manipulação segura de arquivos
├── script.py                # Exemplos de uso dos utilitários
├── requirements.txt         # Dependências do projeto
└── README.md                # Este arquivo

🚀 Como Usar
1. Pré-requisitos

    Python 3.8+

    Pip (gerenciador de pacotes)

    Sistema operacional: Windows/Linux/macOS (testado em Windows 10/11 e Kali Linux)

2. Instalação

# Clone o repositório
git clone https://github.com/museu-do-novo/python-tools.git

# Instale as dependências
entre na pasta de cada projeto e digite:
pip install -r requirements.txt

3. Execução
Modo Interativo (main.py)

python main.py

    Abre o Chrome enquanto executa testes de segurança em segundo plano.

Build do Executável (builder.py)

python builder.py --clean

    Compila o projeto em um único arquivo executável (útil para testes em sistemas alvo).

Ferramentas Individuais

    Auditoria de Sistema:
    python

python malware.py  # Renomeie para pentest_tools.py

    Coleta informações do sistema, verifica vulnerabilidades e gera relatórios.

Utilitários de Rede:
python

    python script.py

        Exemplos de ping, varredura de portas e comandos customizados.

🔧 Ferramentas Disponíveis
Arquivo	Função
malware.py	Coleta de informações, varredura de portas, análise de vulnerabilidades.
shell_utilities.py	Comandos Unix-like (ping, ls, grep, criptografia, upload para MEGA).
file_handler.py	Cópia segura de arquivos com auditoria de permissões.
builder.py	Compilação do projeto em executável (PyInstaller).
📌 Exemplos de Comandos
1. Coleta de Informações do Sistema
python

from malware import system_recon
data = system_recon(verbose=True)  # Retorna JSON com detalhes do sistema

2. Varredura de Portas
python

from malware import port_scan
open_ports = port_scan(target="192.168.1.1", ports="1-1024")

3. Criptografia de Arquivos
python

from shell_utilities import encrypt_files
encrypt_files(["secret.txt"])  # Criptografa com AES-256 (extensão .666)

4. Upload para MEGA.nz
python

from shell_utilities import mega_login, mega_upload
mega_login("email@protonmail.com", "senha123")
mega_upload("relatorio.html")

⚠️ Boas Práticas

    Renomeie malware.py para pentest_tools.py para evitar falsos positivos em antivírus.

    Use ambientes isolados (Docker/Virtualenv) para testes.

    Documente todas as ações durante testes reais.

    Nunca use em produção sem autorização por escrito.

📄 Licença

MIT License - Consulte LICENSE para detalhes.

🔗 Links Úteis

    OWASP Testing Guide

    MITRE ATT&CK Framework

✉️ Contato

    Autor: museu-do-novo

    E-mail: seu-email@protonmail.com

📌 Nota Final:
Este projeto é apenas para fins educacionais. Use com responsabilidade!