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
import re  # needed to make use of regex to clean dates in list of wars dataset


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


def clean_values(date):
    date_arr = re.split('[^0-9a-zA-Z]', date)
    print(date_arr)
    max = 0
    for value in date_arr:
        try:
            value = int(value)
            if value > max:
                max = value
        except ValueError:
            pass
    return max


def main():
    # pull dataframes from website
    url_1900_1944 = 'https://en.wikipedia.org/wiki/List_of_wars:_1900-1944'
    url_1945_1989 = 'https://en.wikipedia.org/wiki/List_of_wars:_1945-1989'
    url_1990_2002 = 'https://en.wikipedia.org/wiki/List_of_wars:_1990-2002'
    urls = [url_1900_1944, url_1945_1989, url_1990_2002]
    new_url = 'https://en.wikipedia.org/wiki/List_of_wars:_2003-present'
    old_df = get_old_data(urls)
    new_df = get_present_data(new_url)
    combined_df = old_df.append(new_df)
    combined_df.to_csv('final_list_of_wars.csv')
    combined_df = pd.read_csv('final_list_of_wars.csv')

    # combine columns of dataframe
    combined_df = combined_df.fillna("")
    combined_df['Finish'] = combined_df['Finish'].astype(str) + \
        combined_df['Finished'].astype(str)
    combined_df['Name of Conflict'] = \
        combined_df['Name of Conflict'].astype(str) + \
        combined_df['Name of conflict'].astype(str)
    relevant_columns = ['Start', 'Finish', 'Name of Conflict']
    wars = combined_df[relevant_columns]

    # clean up dates and convert to integers. export
    wars['Start'] = wars['Start'].apply(clean_values).apply(int)
    wars['Finish'] = wars['Finish'].apply(clean_values).apply(int)
    wars['Start'] = wars['Start'].replace(to_replace=0, value=2023)
    wars['Finish'] = wars['Finish'].replace(to_replace=0, value=2023)
    wars.to_csv('final_list_of_wars.csv')


if __name__ == '__main__':
    main()
