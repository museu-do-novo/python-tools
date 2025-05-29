import os
import shutil
import tkinter as tk
from tkinter import ttk, messagebox
import psutil
from threading import Thread
import time

class WindowsLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Launcher Didático Windows")
        self.root.geometry("600x450")
        
        # Variáveis para monitoramento
        self.cpu_var = tk.StringVar(value="CPU: 0%")
        self.ram_var = tk.StringVar(value="RAM: 0%")
        self.running = True
        
        # Lista de programas nativos do Windows
        self.programas = {
            "Bloco de Notas": "notepad.exe",
            "Calculadora": "calc.exe",
            "Paint": "mspaint.exe",
            "Gerenciador de Tarefas": "taskmgr.exe",
            "Prompt de Comando": "cmd.exe",
            "Explorador de Arquivos": "explorer.exe",
            "WordPad": "write.exe",
            "Windows Media Player": "wmplayer.exe",
            "Verificador de Arquivos do Sistema": "sfc.exe",
            "Desfragmentador de Disco": "dfrgui.exe"
        }
        
        self.criar_interface()
        self.iniciar_monitoramento()
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_aplicacao)
    
    def criar_interface(self):
        """Método que constrói toda a interface gráfica"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame do título e monitoramento
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=5)
        
        # Label de título (alinhado à esquerda)
        ttk.Label(title_frame, text="Programas Nativos do Windows", 
                 font=('Helvetica', 14, 'bold')).pack(side=tk.LEFT)
        
        # Frame de monitoramento (alinhado à direita)
        monitor_frame = ttk.Frame(title_frame)
        monitor_frame.pack(side=tk.RIGHT)
        
        # Monitoramento em uma única linha
        ttk.Label(monitor_frame, textvariable=self.cpu_var, 
                 font=('Helvetica', 9)).pack(side=tk.LEFT, padx=5)
        ttk.Label(monitor_frame, textvariable=self.ram_var, 
                 font=('Helvetica', 9)).pack(side=tk.LEFT, padx=5)
        
        # Lista de programas
        self.lista_programas = tk.Listbox(main_frame, height=12, selectmode=tk.SINGLE)
        self.lista_programas.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Adicionar programas à lista
        for programa in sorted(self.programas.keys()):
            self.lista_programas.insert(tk.END, programa)
        
        # Configurar duplo-clique
        self.lista_programas.bind('<Double-Button-1>', self.abrir_com_duplo_clique)
        
        # Frame de botões
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(btn_frame, text="Abrir Programa", 
                  command=self.abrir_programa).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Ver Caminho", 
                  command=self.mostrar_caminho).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Info do Sistema", 
                  command=self.info_sistema).pack(side=tk.RIGHT, padx=5)
    
    def abrir_com_duplo_clique(self, event):
        """Método chamado quando ocorre duplo-clique na lista"""
        self.abrir_programa()
    
    def iniciar_monitoramento(self):
        """Inicia uma thread para atualizar CPU e RAM"""
        def monitorar():
            while self.running:
                cpu_percent = psutil.cpu_percent(interval=0.5)
                ram_percent = psutil.virtual_memory().percent
                
                self.cpu_var.set(f"CPU: {cpu_percent:.1f}%")
                self.ram_var.set(f"RAM: {ram_percent:.1f}%")
                time.sleep(1)
        
        self.monitor_thread = Thread(target=monitorar, daemon=True)
        self.monitor_thread.start()
    
   
    def fechar_aplicacao(self):
        """Encerra a aplicação corretamente"""
        self.running = False
        self.root.destroy()
    
    def abrir_programa(self):
        selecao = self.lista_programas.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um programa na lista")
            return
        
        programa_nome = self.lista_programas.get(selecao)
        programa_exe = self.programas[programa_nome]
        
        try:
            os.startfile(programa_exe)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir {programa_nome}:\n{e}")
    
    def mostrar_caminho(self):
        selecao = self.lista_programas.curselection()
        if not selecao:
            messagebox.showwarning("Aviso", "Selecione um programa na lista")
            return
        
        programa_nome = self.lista_programas.get(selecao)
        programa_exe = self.programas[programa_nome]
        
        try:
            caminho = shutil.which(programa_exe)
            if caminho:
                messagebox.showinfo("Caminho", f"{programa_nome} está em:\n{caminho}")
            else:
                messagebox.showinfo("Caminho", f"{programa_nome} é um comando interno do Windows")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível encontrar o caminho:\n{e}")
    
    def info_sistema(self):
        cpu_percent = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        info = f"""
        Informações Detalhadas do Sistema:
        
        CPU:
          Uso atual: {cpu_percent:.1f}%
          Núcleos físicos: {psutil.cpu_count(logical=False)}
          Núcleos lógicos: {psutil.cpu_count(logical=True)}
        
        Memória RAM:
          Uso: {ram.percent:.1f}%
          Total: {ram.total / (1024**3):.2f} GB
          Usado: {ram.used / (1024**3):.2f} GB
          Livre: {ram.available / (1024**3):.2f} GB
        
        Disco Principal:
          Uso: {disk.percent:.1f}%
          Total: {disk.total / (1024**3):.2f} GB
          Usado: {disk.used / (1024**3):.2f} GB
          Livre: {disk.free / (1024**3):.2f} GB
        
        Sistema Operacional: {os.name}
        Diretório Atual: {os.getcwd()}
        """
        messagebox.showinfo("Informações do Sistema", info)

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowsLauncher(root)
    root.mainloop()
