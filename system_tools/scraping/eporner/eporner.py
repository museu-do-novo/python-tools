import re
from pathlib import Path
from rich.console import Console
from InquirerPy import inquirer
import requests
from bs4 import BeautifulSoup as bs
from yt_dlp import YoutubeDL
console=Console()
console.clear()
console.rule(title="[hot_pink]BAIXAR VIDEOS[/]", characters="*")
baseurl="https://www.eporner.com"
query=inquirer.text(message="pesquise ai: ", default="curvy latina natalia", raise_keyboard_interrupt=False).execute().replace(" ", "-")
linksfile="links.txt"
downloadpath=Path('~/Videos/eporner/').expanduser()
Path.mkdir(downloadpath, exist_ok=True)
def downloadvideos(linksfile, path):
    if not Path(linksfile).exists():
        console.print(f"[red]Arquivo '{linksfile}' não encontrado.")
        return
    Path.mkdir(path, exist_ok=True)
    with open(linksfile, 'r') as f:
        links=[linha.strip() for linha in f if linha.strip()]
    if not links:
        console.print("[red]Nenhum link válido encontrado no arquivo.")
        return
    ytdlp_opts={
        'format': 'bestvideo+bestaudio/best', 'merge_output_format': 'mp4',
        'outtmpl': str(Path(path).joinpath('%(title).80s.%(ext)s')),
        'noplaylist': True, 'nooverwrites': True,
        'quiet': False, 'ignoreerrors': True, 'continue': True }
    console.print(f"[green]Baixando vídeos de [yellow]'{linksfile}' [green]para [magenta]'{path}'[green]...\n")
    with YoutubeDL(ytdlp_opts) as ydl:
        ydl.download(links)
    console.print(f"\n[blink green]Download concluído com sucesso para [/][magenta]{len(links)}[blink green] links.")
def savefile(filename, inputlist):
    Path(filename).unlink(missing_ok=True)
    with open(filename, 'a') as file:
        for i in inputlist:
            file.write(f"{i}\n")
def main():
    console.clear()
    clean_link=[]
    page=1
    while True:
        console.rule(title=f":page_facing_up: [magenta]Página: [blue]{page}", style="yellow")
        url=f"{baseurl}/tag/{query}/{page}/"
        response=requests.get(url, timeout=15)
        soup=bs(response.text, 'html.parser')
        # CSS Selector: div.mbcontent a[href]
        for a in soup.select('div.mbcontent a[href]'):
            href=a.get('href', '').strip()
            # Regex para capturar apenas URLs do tipo /video-xxxx
            if re.match(r'^/video-\w+', href):
                video_url=baseurl + href
                if video_url not in clean_link:
                    clean_link.append(video_url)
                    console.print(f":film_projector: [sea_green1] --  {video_url}")
        next_button = soup.select_one('a.nmnext')
        if not next_button:
            console.print("[bold red3 blink]Última página alcançada.")
            break
        page += 1
    savefile(filename=linksfile, inputlist=clean_link)
    console.rule(title=f"[blue]{len(clean_link)}[green blink] links salvos em [/][dark_slate_gray2]{linksfile}")
    downloadvideos(linksfile=linksfile, path=downloadpath)
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.rule(title="adios")
