#!env_eporner/bin/python3

import requests
from bs4 import BeautifulSoup as bs
import re
import os
from yt_dlp import YoutubeDL

# variables
baseurl = "https://www.eporner.com"
search_path = "/search/curvy-latina-natalia/"
linksfile = "links.txt"
# mexer enssa parte para funcionar em outras maquinas adicionar os.mkdirs para verificar e mudar o caminho
downloadpath = os.path.expanduser('~/Videos/eporner/')
os.makedirs(downloadpath, exist_ok=True)

def downloadvideos(linksfile, path):
    # Verifica se o arquivo de links existe
    if not os.path.exists(linksfile):
        print(f"❌ Arquivo '{linksfile}' não encontrado.")
        return

    # Cria a pasta de destino, se não existir
    os.makedirs(path, exist_ok=True)

    # Lê os links do arquivo
    with open(linksfile, 'r') as f:
        links = [linha.strip() for linha in f if linha.strip()]

    if not links:
        print("⚠️ Nenhum link válido encontrado no arquivo.")
        return

    # Opções do yt-dlp
    ytdlp_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': os.path.join(path, '%(title).80s.%(ext)s'),
        'noplaylist': True,
        'nooverwrites': True,
        'quiet': False,
        'ignoreerrors': True,
        'continue': True
    }

    print(f"🚀 Baixando vídeos de '{linksfile}' para '{path}'...\n")

    with YoutubeDL(ytdlp_opts) as ydl:
        ydl.download(links)

    print(f"\n✅ Download concluído com sucesso para {len(links)} links.")




def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def savefile(filename, inputinfo, clean=False):
    if clean and os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'a') as file:
        if isinstance(inputinfo, list):
            for info in inputinfo:
                file.write(f"{info}\n")
        else:
            file.write(inputinfo)

def openinbrowser(url):
    os.system(f"firefox --private-window {url} &")



def main():
    clear()
    clean_link = []
    page = 1

    while True:
        print(f"📄 Página: {page}")
        url = f"{baseurl}{search_path}{page}/"
        response = requests.get(url)
        soup = bs(response.text, 'html.parser')
        # openinbrowser(url)
        # Extrair os links de vídeo
        for a in soup.find_all('a', href=True):
            if re.search(r'^/video-\w+', a['href']):
                video_url = baseurl + a['href']
                if video_url not in clean_link:
                    clean_link.append(video_url)
                    print(f"🎥 {video_url}")

        # Verifica se existe botão "NEXT"
        next_button = soup.find('a', class_='nmnext')
        if not next_button:
            print("🚫 Última página alcançada.")
            break

        page += 1

    savefile(linksfile, clean_link, clean=True)
    print(f"\n✅ {len(clean_link)} links salvos em {linksfile}")
    downloadvideos(linksfile=linksfile, path=downloadpath)

if __name__ == "__main__":
    main()
