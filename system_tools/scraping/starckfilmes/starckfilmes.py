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
import sys

shmodule = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../shell_utilities'))
if shmodule not in sys.path:
    sys.path.append(shmodule)
import shell_utilities


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
        shell_utilities.message("Nenhum titulo encontrada com o filtro especificado.", color=Fore.RED, verbose=verbose)
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
        shell_utilities.message(f"[WARN]: Nenhum link magnet encontrado na página: {pagina_temporada}", color=Fore.YELLOW)

    if len(magnet_links) > 1:
        shell_utilities.message(f"[INFO]: {len(magnet_links)} links magnet encontrados na página: {pagina_temporada}", color=Fore.GREEN)
    # retorna a lista de links magnet encontrados em cada pagina do feed 
    return magnet_links


# mexer no header para aparecer so uma vez no arquivo
def savetofile(filename, content,  clean=False, verbose=True):

    if clean and os.path.exists(filename):
        shell_utilities.message(f"🗑️ Limpando arquivo: {filename}", color=Fore.YELLOW, verbose=verbose)
        os.remove(filename)

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

    with open(filename, 'a') as file:
        if type(content) == list:
            shell_utilities.message(f"📄 Salvando {len(content)} itens da lista em {filename}", verbose=verbose)
            for item in content:
                file.write(f"{item}\n")
        else:
            shell_utilities.message(f"📄 Salvando conteúdo do texto em {filename}", verbose=verbose)
            file.write(content)

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
        shell_utilities.message(f'🌐 Página: {url}', color=Fore.LIGHTCYAN_EX)
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, 'html.parser')

        for a in soup.find_all('a', class_='title', href=True):
            titulo = a.text.strip()
            link = a['href']
            if filtro in titulo.lower():
                titulos.append((titulo, link))

                if mostrar_titulos:
                    shell_utilities.banner(titulo)

                if mostrar_urls:
                    shell_utilities.message(f'🔗 URL: {link}', color=Fore.LIGHTMAGENTA_EX)

                if mostrar_magnets:
                    links = pegar_magnet_links(link)
                    if links:
                        magnet_links.append(f"\n🎬 {titulo.upper()}")
                        magnet_links.extend(links)
                        for m in links:
                            shell_utilities.message(f'🧲 {m}', color=Fore.CYAN)
                    else:
                        shell_utilities.message("⚠️ Nenhum magnet encontrado.", color=Fore.YELLOW)

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

    shell_utilities.clear()
    shell_utilities.rm((args.output or "starckfilmes.link")
    # 🎬 Introdução com efeito visual
    for _ in range(15):
        shell_utilities.banner("Starck Filmes Scraper")
        time.sleep(0.1)

        shell_utilities.clear()
    # 🧪 Verificação do termo de busca
    if not args.search:
        shell_utilities.message("❌ Nenhum termo de busca informado.", color=Fore.RED)
        exit(1)

    # 🔍 Montagem da URL de busca
    termo_busca = args.search.replace(" ", "+")
    url_busca = f'https://www.starckfilmes.online/page/1/?s={termo_busca}'

    shell_utilities.message("🚀 Iniciando varredura nas páginas...", color=Fore.GREEN)

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
        shell_utilities.message(f"\n✅ Total de magnet links encontrados: {total}", color=Fore.LIGHTGREEN_EX)
        if args.output:
            shell_utilities.message(f"📁 Arquivo salvo em: {args.output}", color=Fore.LIGHTYELLOW_EX)
    else:
        shell_utilities.message("⚠️ Nenhum magnet link encontrado na busca.", color=Fore.YELLOW)

    # 🎉 Footer charmoso
    shell_utilities.message("\n╰────── FIM DA EXECUÇÃO ──────╯", color=Fore.MAGENTA)



if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
    except Exception as e:
        shell_utilities.message(f"❌ Erro inesperado: {e}", color=Fore.RED)
        exit(1)

