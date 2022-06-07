'''
This file tests the most fundamental and most confusing part of this project:
scraping the war wikipedia and making the most out of the tables.
'''
import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
    url = 'https://en.wikipedia.org/wiki/List_of_wars:_1900-1944'
    response = requests.get(url)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table')
    war = pd.read_html((str(table)))
    print(war)


if __name__ == '__main__':
    main()
