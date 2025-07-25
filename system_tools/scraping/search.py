#!/home/nad/myenv/bin/python3
# -*- coding: utf-8 -*-

import sys
import argparse
import webbrowser
import urllib.parse
import os
import requests
from bs4 import BeautifulSoup as bs

# o autocompletar me retornou isso e quero checkar se essa api existe:
# proxyapi = "https://api.proxycrawl.com/?token=YOUR_TOKEN&url={url}"

proxiapi = "https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text&timeout=5000"
proxylist = requests.get(proxiapi).text.splitlines()
proxysfile = 'proxyscrape.txt'

VERSION = "1.0"
DEFAULT_ENGINE = "google"


# função para salvar o arquivo
def savetofile(filename, content,  clean=False, verbose=False):
    if clean and os.path.exists(filename):
        if verbose:
            print(f"🗑️ Limpando arquivo: {filename}")
        os.remove(filename)
    with open(filename, 'a') as file:
        if type(content) == list:
            if verbose:
                print(f"📄 Salvando {len(content)} itens da lista em {filename}")
            for item in content:
                file.write(f"{item}\n")
        else:
            if verbose:
                print(f"📄 Salvando conteúdo do texto em {filename}")
            file.write(content)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


SEARCH_ENGINES = {
    # General
    "google": "https://www.google.com/search?q={query}",
    "ddg": "https://duckduckgo.com/?q={query}",
    "brave": "https://search.brave.com/search?q={query}",
    "startpage": "https://www.startpage.com/search?q={query}",
    "yandex": "https://yandex.com/search/?text={query}",
    "baidu": "https://www.baidu.com/s?wd={query}",
    "ecosia": "https://www.ecosia.org/search?q={query}",
    "mojeek": "https://www.mojeek.com/search?q={query}",
    "qwant": "https://www.qwant.com/?q={query}",
    "searx": "https://searx.be/search?q={query}",
    
    # Tech & Dev
    "github": "https://github.com/search?q={query}",
    "gitlab": "https://gitlab.com/search?search={query}",
    "bitbucket": "https://bitbucket.org/repo/all?name={query}",
    "stackoverflow": "https://stackoverflow.com/search?q={query}",
    "npm": "https://www.npmjs.com/search?q={query}",
    "dockerhub": "https://hub.docker.com/search?q={query}",
    "pypi": "https://pypi.org/search/?q={query}",
    "rubygems": "https://rubygems.org/search?query={query}",
    "packagist": "https://packagist.org/search/?q={query}",
    "cargo": "https://crates.io/search?q={query}",
    "nuget": "https://www.nuget.org/packages?q={query}",
    "maven": "https://search.maven.org/search?q={query}",
    "pubdev": "https://pub.dev/packages?q={query}",
    "brew": "https://formulae.brew.sh/search/?q={query}",
    "aur": "https://aur.archlinux.org/packages/?K={query}",
    "debian": "https://packages.debian.org/search?keywords={query}",
    "ubuntu": "https://packages.ubuntu.com/search?keywords={query}",
    "ctan": "https://ctan.org/search?phrase={query}",
    "grepapp": "https://grep.app/search?q={query}",
    "sourcegraph": "https://sourcegraph.com/search?q={query}",
    "codeberg": "https://codeberg.org/explore/repos?q={query}",
    "readthedocs": "https://readthedocs.org/search/?q={query}",
    "godoc": "https://pkg.go.dev/search?q={query}",
    "pkgx": "https://web.pkgx.dev/pkg?q={query}",
    "replit": "https://replit.com/search?q={query}",
    
    # Academic
    "arxiv": "https://arxiv.org/search/?query={query}",
    "scholar": "https://scholar.google.com/scholar?q={query}",
    "pubmed": "https://pubmed.ncbi.nlm.nih.gov/?term={query}",
    "springer": "https://link.springer.com/search?query={query}",
    "ieee": "https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText={query}",
    "scihub": "https://sci-hub.se/{query}",
    "semanticscholar": "https://www.semanticscholar.org/search?q={query}",
    "researchgate": "https://www.researchgate.net/search?q={query}",
    "osf": "https://osf.io/search/?q={query}",
    "paperswithcode": "https://paperswithcode.com/search?q={query}",
    
    # Media
    "youtube": "https://www.youtube.com/results?search_query={query}",
    "odysee": "https://odysee.com/$/search?q={query}",
    "peertube": "https://search.joinpeertube.org/search?search={query}",
    "soundcloud": "https://soundcloud.com/search?q={query}",
    "spotify": "https://open.spotify.com/search/{query}/tracks",
    "bandcamp": "https://bandcamp.com/search?q={query}",
    "vimeo": "https://vimeo.com/search?q={query}",
    "twitch": "https://www.twitch.tv/search?term={query}",
    "dailymotion": "https://www.dailymotion.com/search/{query}",
    "flickr": "https://www.flickr.com/search/?text={query}",
    "imgur": "https://imgur.com/search?q={query}",
    "giphy": "https://giphy.com/search/{query}",
    "tenor": "https://tenor.com/search/{query}-gifs",
    "pixabay": "https://pixabay.com/images/search/{query}/",
    "unsplash": "https://unsplash.com/s/photos/{query}",
    "pexels": "https://www.pexels.com/search/{query}/",
    "shutterstock": "https://www.shutterstock.com/search/{query}",
    "starckfilmes": "https://www.starckfilmes.online/?s={query}",
    "the pirate bay": "https://thepiratebay.org/search/{query}/0/99/0",
    
    # Shopping
    "amazon": "https://www.amazon.com/s?k={query}",
    "ebay": "https://www.ebay.com/sch/i.html?_nkw={query}",
    "aliexpress": "https://www.aliexpress.com/wholesale?SearchText={query}",
    "shopee": "https://shopee.com/search?keyword={query}",
    "mercadolivre": "https://www.mercadolivre.com.br/ofertas?q={query}",
    "olx": "https://www.olx.com.br/q/{query}/",
    
    # Specialized
    "annas-archive": "https://annas-archive.org/search?query={query}",
    "wolfram": "https://www.wolframalpha.com/input/?i={query}",
    "imdb": "https://www.imdb.com/find?q={query}",
    "ted": "https://www.ted.com/search?q={query}",
    "linguee": "https://www.linguee.com.br/search?source=auto&query={query}",
    "deepl": "https://www.deepl.com/translator#auto/auto/{query}",
    "openlibrary": "https://openlibrary.org/search?q={query}",
    "archive": "https://archive.org/search.php?query={query}",
    "zlibrary": "https://singlelogin.re/search?q={query}",
    "libgen": "https://libgen.rs/search.php?req={query}",
    "perplexity": "https://www.perplexity.ai/search?q={query}",
    
    # AI
    "openai": "https://openai.com/research/#{query}",
    "huggingface": "https://huggingface.co/models?search={query}",
    "replicate": "https://replicate.com/explore?search={query}",
    "civitai": "https://civitai.com/search/models?query={query}",
    
    # Social / Forums
    "medium": "https://medium.com/search?q={query}",
    "reddit": "https://www.reddit.com/search/?q={query}",
    "twitter": "https://twitter.com/search?q={query}",
    "linkedin": "https://www.linkedin.com/search/results/all/?keywords={query}",
    "quora": "https://www.quora.com/search?q={query}",
    "patreon": "https://www.patreon.com/search?q={query}",
    "lemmy": "https://lemmy.ml/search?q={query}&type=All",
    "4chan": "https://find.4chan.org/?q={query}",
    "8kun": "https://8kun.top/search.php?q={query}",
    "raddle": "https://raddle.me/search?q={query}",
    
    # Onion / Dark Web Indexers (via clearnet frontends)
    "ahmia": "https://ahmia.fi/search/?q={query}",
    "darksearch": "https://darksearch.io/search?query={query}",
    "onionland": "https://onionlandsearchengine.com/search?q={query}",
    "oniondir": "https://dirnxxdraygbifgc.onion.to/search/?q={query}",
    
    # Wikipedia
    "wikipedia": "https://en.wikipedia.org/w/index.php?search={query}",
    "wikipt": "https://pt.wikipedia.org/w/index.php?search={query}",
    "wikies": "https://es.wikipedia.org/w/index.php?search={query}",
    "wikifr": "https://fr.wikipedia.org/w/index.php?search={query}",
    "wikide": "https://de.wikipedia.org/w/index.php?search={query}",
    "wikidata": "https://www.wikidata.org/w/index.php?search={query}",
    "wikibooks": "https://en.wikibooks.org/w/index.php?search={query}",
}

# listar os motores de busca
def list_engines():
    print("🔧 Motores disponíveis:")
    for engine in sorted(SEARCH_ENGINES):
        print(f" - {engine}")
    sys.exit(0)


# abrir o navegador com a url, eu preciso de uma opcao com guia anonima (hardcoded)
def open_search(engine, query, incognito=True):
    if engine not in SEARCH_ENGINES:
        print(f"❌ Engine inválido: {engine}")
        list_engines()

    encoded_query = urllib.parse.quote_plus(query)
    url = SEARCH_ENGINES[engine].replace("{query}", encoded_query)
    print(f"🌐 Abrindo [{engine}]: {url}")

    if incognito:
        # Altere o navegador conforme seu sistema
        os.system(f"firefox --private-window {url} &")  
    else:
        webbrowser.open(url)

# isso pega a lista e chama a funcao de abrir o navegador para cada motor
def process_query(engines, query):
    for engine in engines:
        open_search(engine, query)

# acho que isso e um suporte a um arquivo com varias palavras a pesquisar
def process_file(engines, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                query = line.strip()
                if query:
                    print(f"🔎 Buscando: {query}")
                    process_query(engines, query)
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {filename}")
        sys.exit(1)


# e preciso melhorar a funcao de help
def main():
    clear()
    parser = argparse.ArgumentParser(
        description="🔍 Search Helper - multi-motor de busca em linha de comando"
    )
    parser.add_argument("-e", "--engine", help="Selecionar motor de busca", default=DEFAULT_ENGINE)
    parser.add_argument("-m", "--multi", help="Buscar em múltiplos motores (separados por vírgula)")
    parser.add_argument("-a", "--all", action="store_true", help="Buscar em todos os motores disponíveis")
    parser.add_argument("-f", "--file", help="Buscar termos de um arquivo de texto")
    parser.add_argument("-l", "--list", action="store_true", help="Listar motores disponíveis")
    parser.add_argument("-V", "--version", action="store_true", help="Mostrar versão")
    parser.add_argument("query", nargs="*", help="Termo(s) para busca")

    args = parser.parse_args()

    # versao e uma coisa sem necessidade ppois meu codigoe para uso pessoal. remova essas coisas de versao
    if args.version:
        print(f"🔄 Versão: {VERSION}")
        sys.exit(0)

    if args.list:
        list_engines()

    # escolhendo os motores de busca
    if args.all:
        engines = list(SEARCH_ENGINES.keys())
    elif args.multi:
        engines = args.multi.split(",")
    else:
        engines = [args.engine]

    # eu preciso entender como esse arquivo esta funcionando
    if args.file:
        process_file(engines, args.file)
    elif args.query:
        query_str = " ".join(args.query)
        process_query(engines, query_str)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
