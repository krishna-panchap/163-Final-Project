"""
Krishna Panchapagesan, Mark Pock
CSE 163
This module will scrape the war table on the
"List of conflicts by duration" Wikipedia page
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def main():
    # getting request from
    wiki_url = 'https://en.wikipedia.org/wiki/List_of_conflicts_by_duration'
    response = requests.get(wiki_url)

    # parsing the file using bs4
    soup = BeautifulSoup(response.content, 'html.parser')  # soup setup
    table = soup.find_all('table')  # finds all occurences of a soup object
    war_history = str(table[2])  # selects the right table
    listwar = pd.read_html(war_history)  # extracts list from html table
    wartable = pd.DataFrame(listwar[0])  # converts list to data frame
    wartable.to_csv('list_of_wars.csv')


if __name__ == '__main__':
    main()
