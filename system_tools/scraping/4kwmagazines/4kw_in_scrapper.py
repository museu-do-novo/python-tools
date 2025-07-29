#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup as bs
import os
import re
import json
import argparse
import time
import subprocess

def sopinha(url):
    response = requests.get(url).content
    soup = bs(response, 'html.parser')
    return soup

def paginacao(search, totalpags):
    return [f"https://4kw.in/page/{i}/?s={search}" for i in range(1, totalpags + 1)]

def totalpaginas(soup):
    page_text = soup.select_one('div.wp-pagenavi span.pages')
    if page_text:
        match = re.search(r'Page \d+ of (\d+)', page_text.text)
        if match:
            return int(match.group(1))
    return 1  # Default to 1 if no pagination found

def resultadosbusca(soup):
    resultados = []
    for div in soup.find_all("div", class_="view view-first"):
        a_tag = div.find("a", href=True)
        title_tag = div.find("h2")
        if a_tag and title_tag:
            resultados.append({
                "titulo": title_tag.text.strip(),
                "pag_titulo": a_tag['href'].strip()
            })
    return resultados

def is_downloadable(soup):
    # recebe soup de downloadpage
    msg_div = soup.find("div", class_="message_page_body")
    if msg_div:
        texto = msg_div.get_text(strip=True).lower()
        return not any(x in texto for x in [
            "file is unavailable", 
            "has been deleted",
            "file not found",
            "page not found"
        ])
    return True  # Se a div de erro não está presente, assume que está OK

def downloadpage(post_url):
    soup = sopinha(post_url)

    # Verifica se a página é realmente baixável
    if not is_downloadable(soup):
        return {
            "link": None,
            "info_bruta": "not_found",
            "baixavel": False
        }

    # Extrai texto de informação (ex: Size : ...)
    info_text = None
    info_tag = soup.find("p", class_="has-text-align-center has-medium-font-size")
    if info_tag:
        info_text = info_tag.get_text(strip=True)

    # Tenta extrair o link via múltiplos métodos
    download_link = None

    # 1. Método <p> com <a> (seletor amplo)
    if not download_link:
        p_link = soup.select_one('p.has-text-align-center a[href]')
        if p_link:
            download_link = p_link['href']

    # 2. Método botão <a class="wp-block-button__link">
    if not download_link:
        button_link = soup.select_one('a.wp-block-button__link[href]')
        if button_link:
            download_link = button_link['href']

    return {
        "link": download_link,
        "info_bruta": info_text,
        "baixavel": True
    }

def salvar_em_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)

def downloader(url, path):
    os.system(f"aria2c {url} -d {path}")

def openinbrowser(url):
    os.system(f"firefox --private-window {url}")

"""

baixar todos os epubs:
    clear; for epub in $(jq '.[] | select(.info | test("\\bepub\\b"; "i"))'  /home/nad/Documents/4kw_jsons/4kw_homemade.json | jq '.download'); do echo $epub | awk -F\" '{print $2}' >> links.txt; done; cat links.txt; aria2c -i links.txt
    os.system('clear; '
          'jq -r \'.[] | select(.info | test("\\\\bepub\\\\b"; "i")) | .download\' '
          '/home/nad/Documents/4kw_jsons/4kw_homemade.json > links.txt; '
          'cat links.txt; '
          'aria2c -i links.txt')
"""

def baixar_epubs(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Filtra links que contenham 'epub' na info e que sejam baixáveis
        links = [
            item['download'] for item in dados
            if item.get("baixavel") and item.get("info") and re.search(r'\bepub\b', item["info"], re.IGNORECASE)
            and item.get("download")
        ]
        
        if not links:
            print("Nenhum link EPUB encontrado.")
            return False

        print(f"Encontrados {len(links)} links EPUB:")
        for i, link in enumerate(links, 1):
            print(f"{i}. {link}")

        for link in links:
            print(f"\nBaixando: {link}")
            downloader(url=link, path=json_path)

        return True

    except Exception as e:
        print(f"Erro: {str(e)}")
        return False

def abrir_pdfs(json_path):
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        # Filtra links que contenham 'pdf' na info e que sejam baixáveis
        links = [
            item['download'] for item in dados
            if item.get("baixavel") and item.get("info") and re.search(r'\bpdf\b', item["info"], re.IGNORECASE)
            and item.get("download")
        ]
        
        if not links:
            print("Nenhum link PDF encontrado.")
            return False

        print(f"Encontrados {len(links)} links PDF:")
        for i, link in enumerate(links, 1):
            print(f"{i}. {link}")

        for link in links:
            print(f"\nAbrindo: {link}")
            os.system(f"firefox --private-window {link}")
            time.sleep(0.1)  # pequeno delay para evitar avalanche de abas

        return True
    except Exception as e:
        print(f"Erro: {str(e)}")
        return False

parser = argparse.ArgumentParser(description="Script para buscar e baixar arquivos de 4kw.in")
parser.add_argument("-s", "--search", required=True, help="Termo de pesquisa")
parser.add_argument("-o", "--open", action="store_true", help="Abrir os links de download no navegador")
parser.add_argument("-e", "--epub", action="store_true", help="Baixar os arquivos de download")
parser.add_argument("-p", "--pdf", action="store_true", help="Abrir os links de download no navegador")

args = parser.parse_args()

jsonspath = os.path.expanduser("~/Documents/4kw_jsons")
os.makedirs(jsonspath, exist_ok=True)
jsonfile = os.path.join(jsonspath, f"4kw_{args.search}.json")

if __name__ == '__main__':
    try:
        os.system('clear' if os.name == 'posix' else 'cls')

        search = args.search
        page = 1
        first_url = f"https://4kw.in/page/{page}/?s={search}"

        soup = sopinha(first_url)
        total_pags = totalpaginas(soup)
        all_pages = paginacao(search=search, totalpags=total_pags)

        todos_os_resultados = []

        for pagina in all_pages:
            print(f"🔍 {pagina}".center(os.get_terminal_size().columns))
            print(f"{all_pages.index(pagina) + 1}/ {total_pags}".center(os.get_terminal_size().columns))
            conteudo = sopinha(pagina)
            resultados = resultadosbusca(conteudo)
            if not resultados:
                print("Nenhum resultado encontrado nesta página.")
                continue

            for resultado in resultados:
                info = downloadpage(resultado['pag_titulo'])
                downloadlink = info.get("link")
                info_texto = info.get("info_bruta")
                baixavel = info.get("baixavel", False)

                print(f"📄 {resultado['titulo']}")
                print(f"🔗 {resultado['pag_titulo']}")
                print(f"📥 {downloadlink}")
                print(f"📜 {info_texto}")
                print(f"✅ Baixável: {'Sim' if baixavel else 'Não'}\n")
                print('-' * os.get_terminal_size().columns)

                todos_os_resultados.append({
                    "titulo": resultado["titulo"],
                    "pagina": resultado["pag_titulo"],
                    "download": downloadlink,
                    "info": info_texto,
                    "baixavel": baixavel
                })

        if todos_os_resultados:
            salvar_em_json(todos_os_resultados, jsonfile)
            print(f"\n✅ json salvo em {jsonfile}")
        else:
            print("\n⚠️ Nenhum resultado encontrado em nenhuma página. Nada foi salvo.")

        if args.pdf:
            abrir_pdfs(jsonfile)

        if args.epub:
            baixar_epubs(jsonfile)

        if args.open:
            for item in todos_os_resultados:
                if item.get("baixavel"):
                    link = item.get("download")
                    if link and link.startswith("http"):
                        openinbrowser(link)
                        time.sleep(0.1)

    except KeyboardInterrupt:
        exit()
