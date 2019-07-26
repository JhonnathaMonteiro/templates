import csv
import requests
from bs4 import BeautifulSoup

# Create a file to store the data and put the header
f = csv.writer(open('z-artist-names.csv', 'w'))
f.writerow(['Name', 'Links'])

pages = []

# Create a list with the links of all pages to be scrapped
for i in range(1, 5):
    url = 'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ' + \
        str(i) + '.htm'
    pages.append(url)

# Loop through all items in "pages" variable
for item in pages:
    # Colect and analysis the item (page)
    page = requests.get(item)
    soup = BeautifulSoup(page.text, 'lxml')

    # Remove unnecessary items
    last_links = soup.find(class_='AlphaNav')
    last_links.decompose()

    # Take all elementos from div BodyText
    artist_name_list = soup.find(class_='BodyText')

    # Retrive the text of all <a> tag instances inside the div BodyText
    artist_name_list_items = artist_name_list.find_all('a')

    # Using .contents to retrive <a> child tag (name and link in this example)
    for artist_name in artist_name_list_items:
        name = artist_name.contents[0]
        links = 'https://web.archive.org' + artist_name.get('href')

        # Write in the CSV file
        f.writerow([name, links])
