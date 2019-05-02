import csv
import requests
from bs4 import BeautifulSoup
import re

# Required:
# BeautifulSoup, Request, lxml

url_example = "http://pointstreak.com/players/players-division-standings.html?divisionid=111166&seasonid=19261"

def ps_scrapy(start_url=url_example,
              base_url="http://www.pointstreak.com/players/"):

    # Getting division SCHEDULE URL
    # just using regular expression, no request needed here
    SCHEDULE_URL = re.sub('\-division-standings\.', '-division-schedule.',
                          start_url)

    # Reuqesting the SCHEDULE page
    SCHEDULE_PAGE = requests.get(SCHEDULE_URL)

    # Creaating Soup
    SCHEDULE_SOUP = BeautifulSoup(SCHEDULE_PAGE.text, 'lxml')

    # Extrating the GAMES URLS
    GAME_URLS = [
        base_url + a["href"] for a in SCHEDULE_SOUP.select(
            'tr.lightGrey > td:nth-of-type(5) > a:first-child')
    ]

    # Game data
    # TODO: modify this to a dataframe (pandas)
    game_id = []
    number = []
    name = []
    G = []
    A = []
    PTS = []
    PIM = []
    GWG = []

    # Extrating the data of every GAME page
    for GAME_URL in GAME_URLS:
        GAME_PAGE = requests.get(GAME_URL)
        GAME_SOUP = BeautifulSoup(GAME_PAGE.text, 'lxml')

        game_id.append(GAME_URL.split('gameid=')[1])
        tr_css_selector = 'table:nth-of-type(6) > tr:nth-of-type(6) > td > table > tr:not(.fields)'
        for tr in GAME_SOUP.select(tr_css_selector):

            # TODO: modify this to a dataframe (pandas)
            number.append(tr.select('td')[0].contents[0])
            name.append(tr.select('a')[0].contents[0])
            G.append(tr.select('td')[0].contents[0])
            A.append(tr.select('td')[1].contents[0])
            PTS.append(tr.select('td')[2].contents[0])
            PIM.append(tr.select('td')[3].contents[0])
            GWG.append(tr.select('td')[4].contents[0])

    return game_id, name, number, G, A, PTS, PIM, GWG
