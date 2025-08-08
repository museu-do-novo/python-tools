from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import os
import time
import json

os.system('clear')

def get_soup(url):
    opts = Options()
    opts.add_argument('--headless')
    opts.add_argument('--disable-gpu')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=opts)
    driver.get(url)
    time.sleep(2)  # aguarda o JS carregar
    html = driver.page_source
    driver.quit()
    return bs(html, 'lxml')

# URL base
base_url = 'https://thepiratebay.org'
start_path = '/search.php?q=top100:recent'
soup = get_soup(base_url + start_path)

# Lista de todas as páginas
paginas = [start_path] + [a['href'] for a in soup.select('center a') if a.get('href')]
paginas = list(dict.fromkeys(paginas))  # remove duplicatas

# Dicionário para armazenar título -> magnet link
resultados = {}

# Loop pelas páginas
for path in paginas:
    url = base_url + path
    soup = get_soup(url)

    titulos = soup.select('span.item-name.item-title')
    links = soup.select('span.item-icons a[href^="magnet:?"]')

    for titulo, link in zip(titulos, links):
        texto = titulo.get_text(strip=True)
        magnet = link['href']
        if texto not in resultados:
            resultados[texto] = magnet

# Exibe no terminal
for nome, magnet in resultados.items():
    print(f'{nome}\n{magnet}\n')

# Salva em arquivo JSON
with open('resultados.json', 'w', encoding='utf-8') as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

print(f'\n[{len(resultados)}] resultados salvos em "resultados.json"')
