#!/home/nad/myenv/bin/python3
import os
import requests
from bs4 import BeautifulSoup as bs

import sys
shmodulepath = '/workspaces/python-tools/system_tools/shell_utilities/' 
sys.path.append(shmodulepath)
import shell_utilities



def soup(url, save=False, show=False):
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    if show:
        print(soup.prettify())
    if save:
        with open("index.html", "w") as f:
            f.write(soup.prettify())
    return soup

def salvarcifra(content, path):
    with open(path, "w") as f:
        f.write(content)

def firefox(url):
    os.system(f"firefox --private-window '{url}'")

def pesquisa_artista(artista):
    artista_url = f"https://www.cifraclub.com.br/{artista.replace(' ', '-')}/"
    soupa = soup(artista_url)
    soupa = soupa.find_all('ul', class_='list-links art_musics alf all artistMusics--allSongs')
    infos = []
    for listafaixassite in soupa:
        for a in listafaixassite.find_all('a', class_="art_music-link", href=True):
            infos.append({
                "title": a['title'],
                "href": "https://www.cifraclub.com.br" + a['href']
            })
    return infos

def manipule_printer(artista_musica, openfile=False, show=False):
    artista_musica = artista_musica.strip("/")
    filename = artista_musica.replace("/", "-").replace("-", "_")

    savedir = f'{os.path.dirname(os.path.abspath(__file__))}/cifras'
    if not os.path.exists(savedir):
        os.mkdir(savedir)
    cifrafile = f"{savedir}/{filename}.txt"

    printer_url = f"https://www.cifraclub.com.br/{artista_musica}/imprimir.html"

    soupa = soup(printer_url)
    cifra_tag = soupa.find("pre")
    if not cifra_tag:
        print("❌ Não foi possível encontrar a cifra.")
        return

    cifra = cifra_tag.text.strip()
    salvarcifra(content=cifra, path=cifrafile)

    if show:
        openfile = False
        shell_utilities.clear()
        shell_utilities.banner(f'{artista_musica.replace("-", " ").replace("/", " - ").title()}')
        print('')
        shell_utilities.message(cifra, color=shell_utilities.Fore.GREEN)

    shell_utilities.message(f"\n✅ Cifra salva em: {cifrafile}", color=shell_utilities.Fore.CYAN)
    if openfile:
        os.system(f'nano "{cifrafile}"')


# Execução principal
if __name__ == "__main__":
    shell_utilities.clear()
    shell_utilities.banner("CIFRA CLUB")

    entrada = input("Digite o nome do artista ou artista + música: ").strip()

    if "/" in entrada:
        # Caso já venha no formato artista/musica
        manipule_printer(entrada, show=True, openfile=False)
    else:
        # Pesquisa músicas do artista
        musicas = pesquisa_artista(entrada)
        if musicas:
            print(f"\n🎵 Músicas encontradas para '{entrada}':\n")
            for i, item in enumerate(musicas, 1):
                print(f"{i:02d}. {item['title']}  →  {item['href']}")
        else:
            print("❌ Nenhuma música encontrada.")
