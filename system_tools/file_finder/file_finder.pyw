# Importações necessárias para o funcionamento do programa
import os  # Para operações com sistema de arquivos
import random  # Para geração de cores aleatórias
import tkinter as tk  # Para a interface gráfica
from tkinter import filedialog, messagebox, scrolledtext  # Componentes específicos do Tkinter


def gerar_cor_clara():
    """
    Gera uma cor hexadecimal aleatória evitando tons muito escuros
    Returns:
        str: Cor no formato hexadecimal (#RRGGBB)
    """
    # Gera valores entre 128 e 255 para cada componente RGB
    # Isso garante cores claras (não muito escuras)
    r = random.randint(128, 255)  # Componente vermelho
    g = random.randint(128, 255)  # Componente verde
    b = random.randint(128, 255)  # Componente azul
    # Formata os valores para hexadecimal de 2 dígitos e concatena
    return f"#{r:02x}{g:02x}{b:02x}".upper()


class FileFinderApp:
    """
    Classe principal da aplicação File Finder
    Responsável por toda a interface e funcionalidades do programa
    """

    def __init__(self, root):
        """
        Inicializa a aplicação
        Args:
            root: Janela principal do Tkinter
        """
        self.root = root
        self.bgcolor = gerar_cor_clara()  # Define uma cor de fundo aleatória
        self.setup_ui()  # Configura a interface do usuário

    def setup_ui(self):
        """Configura todos os elementos da interface gráfica"""
        # Configurações básicas da janela principal
        self.root.title("File Finder")  # Título da janela
        self.root.geometry("800x500")  # Tamanho inicial
        self.root.resizable(True, True)  # Permite redimensionamento
        self.root.configure(background=self.bgcolor, padx=13, pady=13)  # Cor de fundo e margens
        self.root.maxsize(width=1000, height=700)  # Tamanho máximo
        self.root.minsize(width=700, height=400)  # Tamanho mínimo

        # Variável de controle para o status da operação
        self.status_var = tk.StringVar()

        # Criação dos componentes da interface
        self.create_file_name_widgets()  # Campo para nome do arquivo
        self.create_search_path_widgets()  # Campo para caminho de busca
        self.create_buttons()  # Botões de ação
        self.create_status_label()  # Label de status
        self.create_results_text()  # Área de resultados

        # Configuração de expansão dos componentes
        self.root.grid_rowconfigure(6, weight=1)  # Expande a linha do resultado
        self.root.grid_columnconfigure(0, weight=1)  # Expande colunas
        self.root.grid_columnconfigure(1, weight=1)

    def create_file_name_widgets(self):
        """Cria os widgets para entrada do nome do arquivo"""
        # Label explicativo
        tk.Label(self.root, text="Nome (ou parte) do arquivo:", 
                anchor='w', bg=self.bgcolor).grid(row=0, column=0, sticky='w', padx=5)
        
        # Campo de entrada para o nome do arquivo
        self.entrada_nome = tk.Entry(self.root)
        self.entrada_nome.grid(row=1, column=0, columnspan=2, sticky='we', padx=5, pady=(0, 10))

    def create_search_path_widgets(self):
        """Cria os widgets para seleção do caminho de busca"""
        # Label explicativo
        tk.Label(self.root, text="Caminho inicial da busca:", 
                anchor='w', bg=self.bgcolor).grid(row=2, column=0, sticky='w', padx=5)

        # Frame para agrupar o campo de entrada e botão
        frame_caminho = tk.Frame(self.root, bg=self.bgcolor)
        frame_caminho.grid(row=3, column=0, columnspan=2, sticky='we', padx=5, pady=(0, 15))
        frame_caminho.columnconfigure(0, weight=1)  # Expande a coluna do campo de entrada

        # Campo de entrada para o caminho
        self.entrada_caminho = tk.Entry(frame_caminho)
        self.entrada_caminho.grid(row=0, column=0, sticky='we')

        # Botão para abrir o diálogo de seleção de pasta
        botao_escolher = tk.Button(frame_caminho, text="Selecionar pasta...", 
                                 width=20, command=self.escolher_diretorio)
        botao_escolher.grid(row=0, column=1, padx=(10, 0))

    def create_buttons(self):
        """Cria os botões de ação da aplicação"""
        # Frame para agrupar os botões
        frame_botoes = tk.Frame(self.root, bg=self.bgcolor)
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=(5, 5))

        # Botão para iniciar a busca
        botao_buscar = tk.Button(frame_botoes, text="🔍 Buscar", 
                               width=20, command=self.buscar_arquivos)
        botao_buscar.grid(row=0, column=0, padx=(0, 40))

        # Botão para limpar os campos
        botao_limpar = tk.Button(frame_botoes, text="🧹 Limpar", 
                               width=20, command=self.limpar_campos)
        botao_limpar.grid(row=0, column=1, padx=0)

    def create_status_label(self):
        """Cria o label que exibe o status da operação"""
        status_label = tk.Label(self.root, textvariable=self.status_var, 
                              fg="blue", anchor='w', bg=self.bgcolor)
        status_label.grid(row=5, column=0, columnspan=2, sticky='w', padx=5)

    def create_results_text(self):
        """Cria a área de texto rolável para exibir os resultados"""
        self.resultado_text = scrolledtext.ScrolledText(self.root, wrap=tk.WORD)
        self.resultado_text.grid(row=6, column=0, columnspan=2, 
                                sticky='nsew', padx=5, pady=10)

    def buscar_arquivos(self):
        """
        Realiza a busca pelos arquivos que correspondem ao critério informado
        e exibe os resultados na interface
        """
        # Limpa a área de resultados
        self.resultado_text.delete('1.0', tk.END)
        # Atualiza o status para indicar que a busca está em andamento
        self.status_var.set("🔍 Buscando...")
        self.root.update_idletasks()  # Atualiza a interface imediatamente

        # Obtém os valores dos campos de entrada
        nome_procurado = self.entrada_nome.get().strip()
        caminho_inicial = self.entrada_caminho.get().strip()

        # Validação dos campos
        if not nome_procurado or not caminho_inicial:
            messagebox.showwarning("Campos vazios", "Preencha todos os campos.")
            self.status_var.set("⚠️ Preencha todos os campos.")
            return

        # Verifica se o caminho é válido
        if not os.path.isdir(caminho_inicial):
            messagebox.showerror("Erro", "Caminho inicial inválido.")
            self.status_var.set("❌ Caminho inválido.")
            return

        # Realiza a busca recursiva no diretório
        resultados = []
        for raiz, dirs, arquivos in os.walk(caminho_inicial):
            for arquivo in arquivos:
                # Busca case-insensitive (não diferencia maiúsculas/minúsculas)
                if nome_procurado.lower() in arquivo.lower():
                    resultados.append(os.path.join(raiz, arquivo))

        # Exibe os resultados
        if resultados:
            for r in resultados:
                self.resultado_text.insert(tk.END, r + "\n")
            self.status_var.set(f"✅ {len(resultados)} arquivo(s) encontrado(s).")
        else:
            self.resultado_text.insert(tk.END, "Nenhum arquivo encontrado.\n")
            self.status_var.set("⚠️ Nenhum arquivo encontrado.")

    def escolher_diretorio(self):
        """
        Abre um diálogo para seleção de diretório
        e preenche o campo de caminho com o diretório selecionado
        """
        caminho = filedialog.askdirectory()
        if caminho:
            self.entrada_caminho.delete(0, tk.END)
            self.entrada_caminho.insert(0, caminho)

    def limpar_campos(self):
        """Limpa todos os campos da interface e reinicia o status"""
        self.entrada_nome.delete(0, tk.END)
        self.entrada_caminho.delete(0, tk.END)
        self.resultado_text.delete('1.0', tk.END)
        self.status_var.set("")


def main():
    """
    Função principal que inicia a aplicação
    """
    
    root = tk.Tk()  # Cria a janela principal
    app = FileFinderApp(root)  # Instancia nossa aplicação
    root.mainloop()  # Inicia o loop principal da interface


if __name__ == "__main__":
    # Este bloco só é executado quando o script é rodado diretamente
    main()
