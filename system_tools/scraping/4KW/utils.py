#!/usr/bin/python3
import requests
from bs4 import BeautifulSoup as bs
import os
import re
import json
import time
from colorama import Fore, Style


def abrir_pdfs(json_path: str) -> bool:
    """
    Opens all PDF links found in the JSON file in a private Firefox window.

    Args:
        json_path (str): Path to the JSON file containing the results.

    Returns:
        bool: True if successful, False otherwise.
    """
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

def downloader(url: str, path: str=os.path.expanduser("~/Documents/4kw_downloads")):
    """
    Downloads a file from the given URL to the specified path using aria2c.

    Args:
        url (str): The URL of the file to download.
        path (str): The path where the file will be saved.

    """
     
    os.makedirs(path, exist_ok=True)
    os.system(f"aria2c {url} -d {path}")

def baixar_epubs(json_path: str, path) -> bool:
    """
    Downloads all EPUB links found in the JSON file.

    Args:
        json_path (str): Path to the JSON file containing the results.

    Returns:
        bool: True if successful, False otherwise.
    """
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
            downloader(url=link, path=downloadpath)

        return True

    except Exception as e:
        print(f"Erro: {str(e)}")
        return False


def salvar_em_json(dados, nome_arquivo):
    with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


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