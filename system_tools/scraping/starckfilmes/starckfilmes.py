#!/home/nad/myenv/bin/python3
# -*- coding: utf-8 -*-
import os
import time
import json
import random
import argparse
import requests
from bs4 import BeautifulSoup
from colorama import Fore, Back, Style

defaultoutputfile = "starckfilmes.links"

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Connection": "keep-alive",
    "Referer": "https://www.google.com/",
}

def info():
    largura = os.get_terminal_size().columns
    separador = '⚡' * largura
    titulo = "⚔️ STARCKFILMES ULTIMATE SCRAPER ⚔️"
    subtitulo = "O Caçador de Links Magnéticos"
    
    epilogo = f"""
{separador}
{titulo.center(largura)}
{subtitulo.center(largura)}

🔥[MISSÃO]🔥
Scraper supremo para o reino de starckfilmes.online
Extraia filmes e séries com os links magnéticos mais poderosos
Automatize sua busca como um verdadeiro cavaleiro digital!

☠️[AVISO DOS DEUSES]☠️
Este script foi forjado nas profundezas do conhecimento
para funcionar exclusivamente com starckfilmes.online
Lembre-se: A pirataria é um caminho sombrio, use este poder
apenas para fins educativos ou enfrentará a ira dos deuses!

⚡[INVOCAÇÃO]⚡
python starckfilmes.py -s "<sua_quest>" [-f "<filtro_sábio>"] [-o "<grimório_de_saída>"]

✨[EXEMPLOS]✨
➤ python starckfilmes.py -s "O Senhor dos Anéis" -f "A Sociedade do Anel"
➤ python starckfilmes.py -s "Stranger Things" -o "links_sagrados.txt"

🔮[OPÇÕES MÁGICAS]🔮
  -s, --search   Sua busca sagrada (obrigatória)
  -f, --filter   Filtro do oráculo (opcional)
  -o, --output   Tomo para guardar os links (opcional)

{separador}
"""
    print(epilogo)

# Funcao para ajudar a controlar a verbosidade
def print_message(message, color=Fore.WHITE, verbose=False) -> None:
    """
    Imprime uma mensagem com cores para melhor visualizacao.
    Args:
        message (str): A mensagem a ser impressa.
        color (str, optional): A cor da mensagem (padrao: branco).
        verbose (bool, optional): Se a mensagem deve ser impressa (padrao: False).

    Returns:
        None

    """
    print(f"{color}{message}{Style.RESET_ALL}")


def random_color(
    normal_color=True,
    bright_color=True,
    contrast_color=True,
    use_styles=True,
    special_combinations=True
) -> str:
    """
    Retorna uma cor aleatória customizável com base nos tipos de cores disponíveis no colorama.

    Args
        normal_color=(bool): Incluir cores normais (Fore.RED, Fore.GREEN, ...)
        bright_color= (bool): Incluir cores brilhantes (Fore.LIGHTRED_EX, ...)
        contrast_color=(bool): Incluir combinações de Fore + Back
        usar_estilos (bool): Incluir estilos com Style.BRIGHT
        usar_combinacoes_especiais (bool): Incluir misturas visuais únicas com Style + Back

    Returns:
        str: Sequência de estilo/colorama pronta para uso
    """
    cores = []

    if normal_color:
        cores.extend([
            Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW,
            Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE
        ])

    if bright_color:
        cores.extend([
            Fore.LIGHTBLACK_EX, Fore.LIGHTRED_EX, Fore.LIGHTGREEN_EX,
            Fore.LIGHTYELLOW_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX,
            Fore.LIGHTCYAN_EX, Fore.LIGHTWHITE_EX
        ])

    if contrast_color:
        cores.extend([
            Fore.RED + Back.CYAN,
            Fore.GREEN + Back.MAGENTA,
            Fore.YELLOW + Back.BLUE,
            Fore.BLUE + Back.YELLOW,
            Fore.MAGENTA + Back.GREEN,
            Fore.CYAN + Back.RED,
            Fore.WHITE + Back.BLACK
        ])

    if use_styles:
        cores.extend([
            Style.BRIGHT + Fore.RED,
            Style.BRIGHT + Fore.GREEN,
            Style.BRIGHT + Fore.YELLOW,
            Style.BRIGHT + Fore.BLUE,
            Style.BRIGHT + Fore.MAGENTA,
            Style.BRIGHT + Fore.CYAN
        ])

    if special_combinations:
        cores.extend([
            Style.BRIGHT + Fore.WHITE + Back.RED,
            Style.BRIGHT + Fore.YELLOW + Back.BLUE,
            Style.BRIGHT + Fore.CYAN + Back.MAGENTA
        ])

    if not cores:
        return Fore.WHITE  # fallback seguro

    return random.choice(cores)


# BANNER DE MILHOES
def banner(title: str, verbose: bool = True) -> None:

    """
    Mostra o banner colorido com a largura do terminal
    Args:
        title (str): Titulo do banner
        verbose (bool): Flag para habilitar ou desabilitar a impressao das mensagens
    Returns:
        None
    """
    try:
        term_width = os.get_terminal_size().columns
    except:
        term_width = 80  # Fallback width if terminal size can't be determined
    
    title = title.upper()
    title_length = len(title)
    
    # Banner elements
    CORNER_CHAR = '✻'
    TOP_BORDER_CHAR = '═'
    BOTTOM_BORDER_CHAR = '═'
    SIDE_CHAR = '║'
    PADDING_CHAR = ' '
    
    # Calculate available space for title (subtracting corners and side chars)
    available_width = term_width - 4  # 2 corners + 2 side chars
    
    # Create the top and bottom borders
    top_border = CORNER_CHAR + TOP_BORDER_CHAR * (term_width - 2) + CORNER_CHAR
    bottom_border = CORNER_CHAR + BOTTOM_BORDER_CHAR * (term_width - 2) + CORNER_CHAR
    
    # Create title line with centered text
    if title_length > available_width:
        title = title[:available_width-3] + "..."
        title_length = len(title)
    
    padding_total = available_width - title_length
    left_padding = padding_total // 2
    right_padding = padding_total - left_padding
    # MODIFICADO: Formatação simétrica da linha do título
    title_line = f"{SIDE_CHAR}{PADDING_CHAR}{' ' * left_padding}{title}{' ' * right_padding}{PADDING_CHAR}{SIDE_CHAR}"

    
    # Create decorative lines above and below title
    decorative_line = SIDE_CHAR + '─' * (term_width - 2) + SIDE_CHAR
    
    # Print the banner with random colors
    color1 = random_color(
    bright_color=True,
    normal_color=True,
    contrast_color=False,
    use_styles=False,
    special_combinations=False
)
    color2 = random_color(
    bright_color=True,
    normal_color=True,
    contrast_color=False,
    use_styles=False,
    special_combinations=False
)
    color3 = random_color(
    bright_color=True,
    normal_color=True,
    contrast_color=False,
    use_styles=False,
    special_combinations=False
)
    
    print_message('\n' + top_border, color=color1, verbose=verbose)
    print_message(decorative_line, color=color2, verbose=verbose)
    print_message(title_line, color=color3, verbose=verbose)
    print_message(decorative_line, color=color2, verbose=verbose)
    print_message(bottom_border, color=color1, verbose=verbose)



# A BOA E VELHA LIMPADA NA TELA
def clear() -> None:
    """
    Limpa a tela do terminal
    Returns:
        None
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def clearoutputfile(filename):
    if os.path.exists(filename):
        os.remove(filename)

def openinbrowser(url: str) -> None:
    """
    Abre o navegador com a URL fornecida.
    Args:
        url (str): A URL para abrir no navegador.
    Returns:
        None
    """

    os.system(f"firefox --private-window {url}")


def salvar_json(dados, filename="dump.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=2)
        print_message(f"📁 Dump JSON salvo com sucesso em: {filename}", color=Fore.GREEN)
    except Exception as e:
        print_message(f"❌ Falha ao salvar JSON: {e}", color=Fore.RED)


#==================================================================================================================================
#==================================================================================================================================
#==================================================================================================================================

# faz a busca pelo link de pesquisa da pagina starckfilmes.online e localiza o lugar dos resultados que aqui chamei de temporadas
# depois pega os links magnet de cada temporada encontrada (o padrao do site e de que cada temporada tenha um link magnet)
def pegar_links_titulos(busca_url: str, filtro: str = "", verbose: bool = True):
    """
    Raspador dos links de paginas relacionadas ao titulo
    Args:
        busca_url (str): URL da pagina de busca
        filtro (str): Termo de busca para filtrar os resultados e ter uma saida mais limpa
        verbose (bool): Flag para habilitar ou desabilitar a impressao das mensagens
    Returns:
        list: Lista com tuplas (titulo, link)
    """


    # faz a requisicao para a pagina de busca
    res = requests.get(busca_url, headers=headers)
    # verifica se a requisicao foi bem sucedida
    res.raise_for_status()
    # usa o BeautifulSoup para analisar o conteudo HTML
    # aqui eu uso o parser html.parser, mas poderia ser outro como lxml ou html.parser
    soup = BeautifulSoup(res.content, 'html.parser')

    titulos = []
    # aqui eu busco os links das titulos, filtrando pelo filtro passado como argumento
    # o filtro e opcional, se nao for passado, pega todas as resultados que podem nao ter o nome igual ao da busca
    # encontrar todas as tags <a> com a classe 'title' e o atributo href
    for a in soup.find_all('a', class_='title', href=True):
        # extrai o texto de cada anchor
        titulo = a.text.strip()
        # extrai o link de cada anchor
        link = a['href']
        # itera sobre a lista de ancoras e verifica se o filtro esta no titulo
        # se o filtro for vazio, pega todos os links
        if filtro in titulo.lower():
            titulos.append((titulo, link))
    if not titulos:
        print_message("Nenhum titulo encontrada com o filtro especificado.", color=Fore.RED, verbose=verbose)
        exit()
    else:
        # retorna uma lista que contem os resultados encontrados no feed
        return titulos

# aqui eu filtro os magnetlinks de cada temporada encontrada no feed 
def pegar_magnet_links(pagina_temporada):
    """
    Raspador de magnetlinks dos titulos do feed
    Args:
        pagina_temporada (str): URL da pagina do feed

    Returns:
        list: Lista com todos os magnet links de cada titulo

    """

    # faz a requisicao para cada link de pagina encontrado no feed
    res = requests.get(pagina_temporada, headers=headers)
    # verifica se a requisicao foi bem sucedida
    res.raise_for_status()
    # usa o BeautifulSoup para analisar o conteudo HTML
    soup = BeautifulSoup(res.content, 'html.parser')

    # crio uma lista vazia para armazenar os links magnet encontrados
    magnet_links = []
    # itero sonbre todas as tags <a> que possuem o atributo href
    for a in soup.find_all('a', href=True):
        href = a['href']
        # se o href comeca com 'magnet:?' entao adiciona na lista de links magnet
        # outra abordagem melhor para filtrar os magnets seria  'href.startswith("magnet:?xt=urn:btih:"):' ou href.startswith('magnet:?'):
        if href.startswith("magnet:?xt=urn:btih:"):
            # adiciona o link magnet no final da lista
            magnet_links.append(href)
    if not magnet_links:
        print_message(f"[WARN]: Nenhum link magnet encontrado na página: {pagina_temporada}", color=Fore.YELLOW)

    if len(magnet_links) > 1:
        print_message(f"[INFO]: {len(magnet_links)} links magnet encontrados na página: {pagina_temporada}", color=Fore.GREEN)
    # retorna a lista de links magnet encontrados em cada pagina do feed 
    return magnet_links


# mexer no header para aparecer so uma vez no arquivo
def savetofile(filename, content,  clean=False, verbose=True):

    if clean and os.path.exists(filename):
        print_message(f"🗑️ Limpando arquivo: {filename}", color=Fore.YELLOW, verbose=verbose)
        os.remove(filename)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, 'a') as file:
        if type(content) == list:
            print_message(f"📄 Salvando {len(content)} itens da lista em {filename}", verbose=verbose)
            for item in content:
                file.write(f"{item}\n")
        else:
            print_message(f"📄 Salvando conteúdo do texto em {filename}", verbose=verbose)
            file.write(content)


def tests():
    pass

def page_crawler(
    url_inicial: str,
    filtro: str = "",
    max_paginas: int = 20,
    mostrar_titulos: bool = True,
    mostrar_urls: bool = False,
    mostrar_magnets: bool = True,
    salvar_em_arquivo: bool = False,
    arquivo_saida: str = "starckfilmes.link"
):
    """
    Crawler com controle total via parâmetros.
    execucao:
        1   - Limpa a tela
        2   - Imprime o banner
        3   - Verifica se o termo de busca foi fornecido
        4   - Monta a URL de busca
        5   - Executa o crawler com controle varios parametros configuraveis

    Args:
        url_inicial (str): URL inicial com termo de busca
        filtro (str): Filtro para os títulos
        max_paginas (int): Limite de páginas
        mostrar_titulos (bool): Exibe os títulos encontrados
        mostrar_urls (bool): Exibe os URLs das páginas dos títulos
        mostrar_magnets (bool): Mostra os magnet links de cada título
        salvar_em_arquivo (bool): Salva os magnet links em arquivo
        arquivo_saida (str): Caminho do arquivo de saída

    Returns:
        list: Lista com todos os magnet links daquele titulo/pagina/temporada/link de titulo (se encontrados)
    """

    titulos = []
    magnet_links = []
    url = url_inicial
    paginas_visitadas = 0

    # while url and paginas_visitadas < max_paginas:
    while url:
        print_message(f'🌐 Página: {url}', color=Fore.LIGHTCYAN_EX)
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'html.parser')

        for a in soup.find_all('a', class_='title', href=True):
            titulo = a.text.strip()
            link = a['href']
            if filtro in titulo.lower():
                titulos.append((titulo, link))

                if mostrar_titulos:
                    banner(titulo)

                if mostrar_urls:
                    print_message(f'🔗 URL: {link}', color=Fore.LIGHTMAGENTA_EX)

                if mostrar_magnets:
                    links = pegar_magnet_links(link)
                    if links:
                        magnet_links.append(f"\n🎬 {titulo.upper()}")
                        magnet_links.extend(links)
                        for m in links:
                            print_message(f'🧲 {m}', color=Fore.CYAN)
                    else:
                        print_message("⚠️ Nenhum magnet encontrado.", color=Fore.YELLOW)

                if salvar_em_arquivo and mostrar_magnets:
                    savetofile(arquivo_saida, magnet_links, verbose=True)
                    magnet_links.clear()  # limpa pra não duplicar em próxima página

        # Paginação: encontra o próximo link (segunda aparição do botão "prev-active")
        prev_active_buttons = soup.find_all('div', class_='prev-active')
        next_link = None
        if len(prev_active_buttons) >= 2:
            next_tag = prev_active_buttons[1].find('a')
            if next_tag and 'href' in next_tag.attrs:
                next_link = next_tag['href']
        elif len(prev_active_buttons) == 1:
            next_tag = prev_active_buttons[0].find('a')
            if next_tag and '→' in next_tag.text:
                next_link = next_tag['href']
        else:
            break  # fim da paginação

        url = next_link
        paginas_visitadas += 1

    return magnet_links


def main() -> None:
    """
    Função principal que executa o script.
    execucao:
        1 - parseia os argumentos da linha de comando
        2 - Limpa a tela
        3 - Imprime o banner
        4 - Verifica se o termo de busca foi fornecido
        5 - Monta a URL de busca
        6 - Executa o crawler com controle total
        7 - Finaliza o script
    Args:
        None
    Returns:
        None
    """


    # cria um parser de argumentos para receber os parametros da linha de comando
    # precisou ficar no escopo global
    parser = argparse.ArgumentParser(prog=os.path.basename(__file__), description='Starckfilmes.online scraper/RIPPER', epilog=info())
    parser.add_argument('-s', '--search', required=False, default='*', help='Termo de busca')
    parser.add_argument('-f', '--filter', default="", help='Filtro para titulos (opcional)')
    parser.add_argument('-o', '--output', nargs='?', default="starckfilmes.links", help=f'Salvar links em arquivo (padrão: "starckfilmes.link" quando flag usada)')
    args = parser.parse_args()

    clear()
    clearoutputfile(args.output or "starckfilmes.link")
    # 🎬 Introdução com efeito visual
    for _ in range(15):
        banner("Starck Filmes Scraper")
        time.sleep(0.1)

        clear()
    # 🧪 Verificação do termo de busca
    if not args.search:
        print_message("❌ Nenhum termo de busca informado.", color=Fore.RED)
        exit(1)

    # 🔍 Montagem da URL de busca
    termo_busca = args.search.replace(" ", "+")
    url_busca = f'https://www.starckfilmes.online/page/1/?s={termo_busca}'

    print_message("🚀 Iniciando varredura nas páginas...", color=Fore.GREEN)

    # 🧲 Executa o crawler com controle total
    magnet_links = page_crawler(
        url_inicial=url_busca,
        filtro=args.filter.lower(),
        mostrar_titulos=True,
        mostrar_urls=False,
        mostrar_magnets=True,
        salvar_em_arquivo=bool(args.output),
        arquivo_saida=args.output
    )

    # ✅ Finalização com resumo
    total = len(magnet_links)
    if total > 0:
        print_message(f"\n✅ Total de magnet links encontrados: {total}", color=Fore.LIGHTGREEN_EX)
        if args.output:
            print_message(f"📁 Arquivo salvo em: {args.output}", color=Fore.LIGHTYELLOW_EX)
    else:
        print_message("⚠️ Nenhum magnet link encontrado na busca.", color=Fore.YELLOW)

    # 🎉 Footer charmoso
    print_message("\n╰────── FIM DA EXECUÇÃO ──────╯", color=Fore.MAGENTA)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        print_message(f"❌ Erro inesperado: {e}", color=Fore.RED)
        exit(1)

