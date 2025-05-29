import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from threading import Thread
import time

try:
    from ttkthemes import ThemedTk
except ImportError:
    print("Instale o pacote necessário com: pip install ttkthemes")
    exit(1)

class WindowsLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Launcher de Ferramentas do Windows")
        self.root.geometry("800x600")
        self.root.minsize(600, 400)

        self.cpu_var = tk.StringVar(value="CPU: 0%")
        self.ram_var = tk.StringVar(value="RAM: 0%")
        self.status_var = tk.StringVar(value="Inicializando...")
        self.running = True

        self._estilo_moderno()

        self.programas = {
            # Utilitários padrão
            "Bloco de Notas": "notepad.exe",
            "Calculadora": "calc.exe",
            "Paint": "mspaint.exe",
            "WordPad": "write.exe",
            "Explorador de Arquivos": "explorer.exe",
            "Prompt de Comando": "cmd.exe",
            "PowerShell": "powershell.exe",

            # Configurações e sistema
            "Painel de Controle": "control.exe",
            "Configurações do Windows": "ms-settings:",
            "Informações do Sistema": "msinfo32.exe",
            "Editor de Registro": "regedit.exe",
            "Política de Grupo Local": "gpedit.msc",

            # Diagnóstico e manutenção
            "Verificador de Arquivos do Sistema": "sfc.exe",
            "Ferramenta DirectX": "dxdiag.exe",
            "Limpeza de Disco": "cleanmgr.exe",
            "Desfragmentador de Disco": "dfrgui.exe",

            # Gerenciamento avançado
            "Gerenciador de Tarefas": "taskmgr.exe",
            "Gerenciamento de Disco": "diskmgmt.msc",
            "Agendador de Tarefas": "taskschd.msc",
            "Visualizador de Eventos": "eventvwr.msc",
            "Monitor de Recursos": "resmon.exe",
            "Gerenciamento do Computador": "compmgmt.msc",

            # Acessibilidade e conectividade
            "Conexões de Rede": "ncpa.cpl",
            "Central de Acessibilidade": "utilman.exe",
            "Windows Media Player": "wmplayer.exe",

            # Avançado
            "Prompt Avançado (Admin)": "powershell.exe -Command Start-Process powershell -Verb runAs"
        }

        self._criar_interface()
        self._iniciar_monitoramento()
        self.root.protocol("WM_DELETE_WINDOW", self._fechar_aplicacao)

    def _estilo_moderno(self):
        style = ttk.Style(self.root)
        style.theme_use("arc")
        self.root.configure(bg=style.lookup("TFrame", "background"))

    def _criar_interface(self):
        self._criar_menu()

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=0, sticky="nsew")

        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Header
        header = ttk.Frame(main_frame)
        header.grid(row=0, column=0, sticky="ew")

        ttk.Label(header, text="Launcher de Ferramentas do Windows", font=("Segoe UI", 14, "bold")).pack(side=tk.LEFT)
        ttk.Label(header, textvariable=self.cpu_var).pack(side=tk.RIGHT, padx=5)
        ttk.Label(header, textvariable=self.ram_var).pack(side=tk.RIGHT, padx=5)

        # Lista de programas
        lista_frame = ttk.LabelFrame(main_frame, text="Ferramentas Disponíveis")
        lista_frame.grid(row=1, column=0, sticky="nsew", pady=10)

        lista_frame.columnconfigure(0, weight=1)
        lista_frame.rowconfigure(0, weight=1)

        self.lista_programas = tk.Listbox(lista_frame, font=("Segoe UI", 10), selectbackground="#cce6ff", selectforeground="#000000")
        self.lista_programas.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(lista_frame, orient="vertical", command=self.lista_programas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.lista_programas.config(yscrollcommand=scrollbar.set)

        for nome in sorted(self.programas.keys()):
            self.lista_programas.insert(tk.END, nome)
        self.lista_programas.bind("<Double-Button-1>", self._abrir_com_duplo_clique)

        # Botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=2, column=0, pady=10)

        ttk.Button(btn_frame, text="Abrir Programa", command=self._abrir_programa).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Ver Caminho", command=self._mostrar_caminho).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="Info do Sistema", command=self._info_sistema).pack(side=tk.RIGHT, padx=10)

        # Barra de status
        status = ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief=tk.SUNKEN)
        status.grid(row=1, column=0, sticky="ew")

    def _criar_menu(self):
        menu_bar = tk.Menu(self.root)
        menu_arquivo = tk.Menu(menu_bar, tearoff=0)
        menu_arquivo.add_command(label="Sair", command=self._fechar_aplicacao)
        menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)

        menu_ajuda = tk.Menu(menu_bar, tearoff=0)
        menu_ajuda.add_command(label="Sobre", command=self._mostrar_sobre)
        menu_bar.add_cascade(label="Ajuda", menu=menu_ajuda)

        self.root.config(menu=menu_bar)

    def _mostrar_sobre(self):
        messagebox.showinfo("Sobre", "Launcher de Ferramentas do Windows\nVisual moderno com tema 'arc'.\nVersão 3.0")

    def _abrir_com_duplo_clique(self, _):
        self._abrir_programa()

    def _abrir_programa(self):
        selecao = self.lista_programas.curselection()
        if not selecao:
            self.status_var.set("Selecione uma ferramenta para abrir.")
            return
        nome = self.lista_programas.get(selecao)
        comando = self.programas[nome]
        try:
            os.startfile(comando)
            self.status_var.set(f"Abrindo: {nome}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir {nome}:\n{e}")
            self.status_var.set("Erro ao abrir o programa.")

    def _mostrar_caminho(self):
        selecao = self.lista_programas.curselection()
        if not selecao:
            return
        nome = self.lista_programas.get(selecao)
        exe = self.programas[nome]
        caminho = shutil.which(exe)
        if caminho:
            messagebox.showinfo("Caminho Encontrado", f"{nome} está localizado em:\n{caminho}")
        else:
            messagebox.showinfo("Caminho", f"{nome} é um comando interno ou reservado.")
        self.status_var.set(f"Verificado caminho de: {nome}")

    def _info_sistema(self):
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disco = psutil.disk_usage("/")

        info = f"""
🧠 CPU:
  Uso: {cpu:.1f}%
  Núcleos: {psutil.cpu_count(logical=True)} (Físicos: {psutil.cpu_count(logical=False)})

💾 RAM:
  Total: {ram.total / (1024**3):.2f} GB
  Uso: {ram.used / (1024**3):.2f} GB ({ram.percent}%)
  Livre: {ram.available / (1024**3):.2f} GB

📁 Disco:
  Total: {disco.total / (1024**3):.2f} GB
  Uso: {disco.used / (1024**3):.2f} GB ({disco.percent}%)
  Livre: {disco.free / (1024**3):.2f} GB

📌 Sistema:
  OS: {os.name}
  Dir Atual: {os.getcwd()}
"""
        messagebox.showinfo("Informações do Sistema", info.strip())
        self.status_var.set("Info do sistema exibida.")

    def _iniciar_monitoramento(self):
        def monitor():
            while self.running:
                self.cpu_var.set(f"CPU: {psutil.cpu_percent():.1f}%")
                self.ram_var.set(f"RAM: {psutil.virtual_memory().percent:.1f}%")
                time.sleep(1)
        Thread(target=monitor, daemon=True).start()

    def _fechar_aplicacao(self):
        self.running = False
        self.root.destroy()


# Execução com tema moderno
if __name__ == "__main__":
    root = ThemedTk(theme="arc")  # 👈 Tema moderno, plano e limpo
    app = WindowsLauncher(root)
    root.mainloop()
