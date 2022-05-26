"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Insert documentation here.
"""


from typing import Iterable
import pandas as pd
import requests
from bs4 import BeautifulSoup


def yahoo_scrape(url: str) -> object:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    war_history = str(table)
    table = pd.read_html(history)


def main():
    

if __name__ == '__main__':
    main()