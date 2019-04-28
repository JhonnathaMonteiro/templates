import csv
import requests
from bs4 import BeautifulSoup

# Criar um arquivo para gravar os dados, adicionar linha de cabecalhos
f = csv.writer(open('z-artist-names.csv', 'w'))
f.writerow(['Name', 'Links'])

pages = []

for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + \
        str(i) + '.htm'
    pages.append(url)

for item in pages:
    # Coletar e analisar a primeira página
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'lxml')

    # Remover links inferiores indesejados
    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    # Pegar todo o texto da div BodyText
    artist_name_list = soup.find(class_='BodyText')

    # Pegar o texto de todas as instâncias da tag <a> dentro da div BodyText
    artist_name_list_items = artist_name_list.find_all('a')

    # Usar .contents para pegar as tags <a> filhas
    for artist_name in artist_name_list_items:
        name = artist_name.contents[0]
        links = 'https://web.archive.org' + artist_name.get('href')

        # Adicionar em uma linha o nome de cada artista e o link associado
        f.writerow([name, links])
