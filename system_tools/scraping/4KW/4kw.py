#!/usr/bin/python3
import os
import re
import argparse
import time
import sys

shmodule = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../shell_utilities'))
if shmodule not in sys.path:
    sys.path.append(shmodule)
import shell_utilities
import utils

def totalpaginas(soup: str) -> int:
    # 🧪 Caso 1 — Formato clássico: <span class="pages">Page X of Y</span>
    page_info = soup.select_one('span.pages')
    if page_info:
        match = re.search(r'Page\s+\d+\s+of\s+(\d+)', page_info.get_text(strip=True))
        if match:
            total = int(match.group(1))
            shell_utilities.message(f'[Clássico] Total de páginas: {total}', verbose=True, color=shell_utilities.Fore.GREEN)
            return total

    # 🧪 Caso 2 — Formato moderno: <ul class="page-numbers">…</ul>
    page_items = soup.select('ul.page-numbers li > .page-numbers')

    numeros = []
    for item in page_items:
        text = item.get_text(strip=True)
        if text.isdigit():
            numeros.append(int(text))

    if numeros:
        total = max(numeros)
        shell_utilities.message(f'[Moderno] Total de páginas: {total}', verbose=True, color=shell_utilities.Fore.GREEN)
        return total

    # Fallback padrão
    shell_utilities.message('[Fallback] Nenhuma paginação encontrada. Retornando 1.', verbose=True, color=shell_utilities.Fore.YELLOW)
    return 1


def paginacao(search: str, totalpags: int) -> list:
    return [f"https://4kw.in/page/{i}/?s={search}" for i in range(1, totalpags + 1)]


def resultadosbusca(soup: str) -> list:
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


def downloadpage(post_url: str) -> dict:
    soup = shell_utilities.soup(post_url)

    # Verifica se a página é realmente baixável
    if not utils.is_downloadable(soup):
        return {
            "link": None,
            "info_bruta": "not_found",
            "baixavel": False
        }

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

def main():

    parser = argparse.ArgumentParser(description="Script para buscar e baixar arquivos de 4kw.in")
    parser.add_argument("-s", "--search", required=True, help="Termo de pesquisa")
    parser.add_argument("-o", "--open", action="store_true", help="Abrir os links de download no navegador")
    parser.add_argument("-e", "--epub", action="store_true", help="Baixar os arquivos de download")
    parser.add_argument("-p", "--pdf", action="store_true", help="Abrir os links de download no navegador")
    args = parser.parse_args()

    jsonspath = os.path.expanduser("~/Documents/4kw_jsons")
    os.makedirs(jsonspath, exist_ok=True)
    jsonfile = os.path.join(jsonspath, f"4kw_{args.search}.json")

    search = args.search
    page = 1
    first_url = f"https://4kw.in/page/{page}/?s={search}"
    soup = shell_utilities.soup(first_url)
    total_pags = totalpaginas(soup)
    all_pages = paginacao(search=search, totalpags=total_pags)

    todos_os_resultados = []

    for pagina in all_pages:
        print(f"🔍 {pagina}".center(os.get_terminal_size().columns))
        print(f"{all_pages.index(pagina) + 1}/ {total_pags}".center(os.get_terminal_size().columns))
        
        conteudo = shell_utilities.soup(pagina)
        resultados = resultadosbusca(conteudo)
        
        if not resultados:
            print("Nenhum resultado encontrado nesta página.")
            continue  # continua para a próxima página

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

    # === AGORA SIM: salvar fora do loop ===
    if todos_os_resultados:
        shell_utilities.save_json(content=todos_os_resultados, filepath=jsonfile, verbose=True)
    else:
        print("\n⚠️ Nenhum resultado encontrado em nenhuma página. Nada foi salvo.")

    # Pós-processamento
    if args.pdf:
        utils.abrir_pdfs(json_path=jsonfile)

    if args.epub:
        utils.baixar_epubs(json_path=jsonfile)

    if args.open:
        for item in todos_os_resultados:
            if item.get("baixavel"):
                link = item.get("download")
                if link and link.startswith("http"):
                    shell_utilities.openinbrowser(link)
                    time.sleep(0.1)


if __name__ == '__main__':
    try:
        shell_utilities.clear()
        main()
    except KeyboardInterrupt:
        exit()
