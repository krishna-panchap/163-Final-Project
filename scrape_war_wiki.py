"""
Krishna Panchapagesan, Mark Pock
CSE 163
This module will scrape the war table on the
"List of conflicts by duration" Wikipedia page
and output into a csv file 'list_of_wars.csv'
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup


def extract_data_frame(url):
    '''
    this helper function takes in a wiki url and returns a dataframe containing
    information about the tables on the wiki
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')  # soup setup
    table = soup.find_all('table')  # finds all occurences of a soup object
    df_war = pd.concat(
                      [df[0] for df in [pd.read_html(str(table[i]))
                       for i in range(len(table) - 1)]]
                    )
    return df_war


def get_old_data(urls):
    '''
    extracts the dataframes from each of the inputted list of urls
    '''
    list_of_dfs = []
    for url in urls:
        list_of_dfs.append(extract_data_frame(url))
    return pd.concat(list_of_dfs)


def get_present_data(url):
    '''
    this function returns the dataframe with the tables in the given url
    '''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    war_history = soup.find('table', {'class': 'wikitable sortable'})
    war_df = pd.DataFrame(pd.read_html(str(war_history))[0])
    return war_df


def main():
    url_1900_1944 = 'https://en.wikipedia.org/wiki/List_of_wars:_1900-1944'
    url_1945_1989 = 'https://en.wikipedia.org/wiki/List_of_wars:_1945-1989'
    url_1990_2002 = 'https://en.wikipedia.org/wiki/List_of_wars:_1990-2002'
    urls = [url_1900_1944, url_1945_1989, url_1990_2002]
    new_url = 'https://en.wikipedia.org/wiki/List_of_wars:_2003-present'
    old_df = get_old_data(urls)
    new_df = get_present_data(new_url)
    combined_df = old_df.append(new_df)
    combined_df.to_csv('updated_list_of_wars.csv')
    combined_df = pd.read_csv('updated_list_of_wars.csv')
    combined_df = combined_df.fillna("")
    combined_df['Finish'] = combined_df['Finish'].astype(str) + \
        combined_df['Finished'].astype(str)
    combined_df['Name of Conflict'] = \
        combined_df['Name of Conflict'].astype(str) + \
        combined_df['Name of conflict'].astype(str)
    relevant_columns = ['Start', 'Finish', 'Name of Conflict']
    wars = combined_df[relevant_columns]
    wars.to_csv('updated_list_of_wars.csv')


if __name__ == '__main__':
    main()
