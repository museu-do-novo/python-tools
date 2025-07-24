import requests
from bs4 import BeautifulSoup
import re
import os
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def savetofile(filename, content):
    with open(filename, 'w') as file:
        # check if content is a list or a string
        # you also can use if type(content) == list: 
        if isinstance(content, list):
            for item in content:
                file.write(f"{item}\n")
        else:
            file.write(content)


def pegar_links_temporadas(busca_url: str, termo_secundario: str = ""):
    res = requests.get(busca_url)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    temporadas = []
    for a in soup.find_all('a', class_='title', href=True):
        titulo = a.text.strip()
        link = a['href']
        # ✅ Filtro para garantir que só pegue temporadas completas da série certa
        if termo_busca in titulo.lower() and termo_secundario in titulo.lower():
            temporadas.append((titulo, link))
    return temporadas


def pegar_magnet_links(pagina_temporada):
    res = requests.get(pagina_temporada)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, 'html.parser')

    magnet_links = []
    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('magnet:?'):
            magnet_links.append(href)
    return magnet_links

def openinbrowser(url):
    os.system(f"firefox --private-window {url} &")

def main():
    clear()
    # old 
    # search_term = "mr+robot"
    search_term = input("🔍 Digite o termo de busca: ").strip()
    secundary_term = input("🔍 Digite o termo secundário (opcional): ").strip()

    url_busca = f'https://www.starckfilmes.online/?s={search_term}'
    temporadas = pegar_links_temporadas(url_busca, secundary_term)

    if not temporadas:
        print("⚠️ Nenhuma temporada encontrada. Verifique o HTML ou o filtro.")
        openinbrowser(url_busca)
        return

    for titulo, link in temporadas:
        print(f'\n🔎 {titulo}')
        magnet_links = pegar_magnet_links(link)
        if magnet_links:
            for magnet in magnet_links:
                print(f'🔗 {magnet}')
                print(f'{magnet}')
                print('=' * 30)
        else:
            print('⚠️ Nenhum magnet link encontrado.')

if __name__ == '__main__':
    main()
