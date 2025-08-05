#!/home/nad/myenv/bin/python3
import os
import requests
from bs4 import BeautifulSoup as bs
import sys

os.system('clear')


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
    artista_url = f"https://www.cifraclub.com.br/{artista.replace(" ", "-")}/"
    soupa = soup(artista_url)
    soupa = soupa.find_all('ul', class_='list-links art_musics alf all artistMusics--allSongs')
    infos = []
    for listafaixassite in soupa:
        for a in listafaixassite.find_all('a', class_="art_music-link", href=True):
            infos.append({"title":a['title'], "href":a['href']})
    return infos

def manipule_printer(artista_musica, openfile=False):
    if artista_musica.startswith("/"):
        artista_musica = artista_musica[1:]
    if artista_musica.endswith("/"):
        artista_musica = artista_musica[:-1]
    
    filename = artista_musica.replace("/", "-").replace("-", "_")
    cifrafile = os.path.expanduser(f"~/Documents/cifras/{filename}.txt")
    printer_url = f"https://www.cifraclub.com.br/{artista_musica}/imprimir.html"
    
    soupa = soup(printer_url)
    cifra = soupa.find("pre").text.strip()
    salvarcifra(content=cifra, path=cifrafile)
    if openfile:
        os.system(f'l3afpad {cifrafile} &')


def mostrar_menu(itens, selecionados=None):
    if selecionados is None:
        selecionados = []
    
    print("\n" + "="*os.get_terminal_size().columns)
    print("MENU DE SELEÇÃO".center(os.get_terminal_size().columns))
    print("="*os.get_terminal_size().columns)
    
    for idx, item in enumerate(itens, start=1):
        marcacao = "[X]" if idx-1 in selecionados else "[ ]"
        print(f"{marcacao} {idx}. {item['title']}")
    
    print("\nOpções:")
    print("  [número] - Selecionar/Deselecionar item")
    print("  A - Selecionar Todos")
    print("  N - Deselecionar Todos")
    print("  C - Confirmar seleção")
    print("  S - Sair")
    print("="*os.get_terminal_size().columns)

def menu_wizard(itens):
    selecionados = []
    
    while True:
        mostrar_menu(itens, selecionados)
        opcao = input("\nDigite sua opção: ").upper()
        
        if opcao == 'A':
            selecionados = list(range(len(itens)))
            print("Todos os itens selecionados!")
        elif opcao == 'N':
            selecionados = []
            print("Todos os itens deselecionados!")
        elif opcao == 'C':
            if not selecionados:
                print("Nenhum item selecionado. Deseja continuar? (S/N)")
                if input().upper() != 'S':
                    continue
            return [itens[i] for i in selecionados] if selecionados else []
        elif opcao == 'S':
            print("Saindo sem selecionar...")
            sys.exit(0)
        else:
            try:
                num = int(opcao)
                if 1 <= num <= len(itens):
                    idx = num - 1
                    if idx in selecionados:
                        selecionados.remove(idx)
                        print(f"Item '{itens[idx]['title']}' deselecionado.")
                    else:
                        selecionados.append(idx)
                        print(f"Item '{itens[idx]['title']}' selecionado.")
                else:
                    print("Número inválido. Tente novamente.")
            except ValueError:
                print("Opção inválida. Tente novamente.")

# Exemplo de uso
if __name__ == "__main__":
    artista = input("Digite o nome do artista: ")
    selecao = menu_wizard(pesquisa_artista(artista))
    
    if selecao:
        print("\nItens selecionados:")
        for item in selecao:
            print(f"- {item['title']} ({item['href']})")
            manipule_printer(item['href'], openfile=True)
    else:
        print("Nenhum item foi selecionado.")
