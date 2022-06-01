"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Insert documentation here.
"""

import pandas as pd
from utils import time_series


def label_year(year: str, war: str, wars: pd.DataFrame):
    """
    Given a year and a war as str along with a DataFrame of wars, labels the
    year by what it is in relation to the war - before, during, after (5 years
    on each side) or not applicable.
    """
    yearint = int(year)
    result = 'NA'
    start = int(wars.loc[wars['Name of Conflict'] == war, 'Start'])
    end = int(wars.loc[wars['Name of Conflict'] == war, 'Finish'])
    if (start - 5) <= yearint and yearint < start:
        result = 'Pre'
    if start <= yearint and yearint < end:
        result = 'In'
    if end <= yearint and yearint <= end + 5:
        result = 'Post'
    return result


def main():
    stocks = time_series('averaged', 'stocks/processed/', concat=False)
    stocks = pd.DataFrame(stocks['Average'])
    wars = pd.read_csv('./datasets/final_list_of_wars.csv')
    dates = pd.Series(stocks.index)
    for war in wars['Name of Conflict']:
        stocks[war] = dates.apply(lambda x: label_year(
                                  str(x).split('-')[0], war, wars))
    stocks.to_csv('./datasets/mega.csv')


if __name__ == '__main__':
    main()
