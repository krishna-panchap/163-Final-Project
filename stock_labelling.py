"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Insert documentation here.
"""

import pandas as pd
from utils import time_series, inflation_adjust


def process_entry(date: pd.Timestamp, start: int, finish: int) -> int:
    """
    Processes a single index average entry with respect to a single war's
    start and end dates. If the entry is less than 6 years before the given
    start year, returns 1. If within the war, returns 2. If less than 6 years
    after the given finish year, returns 3. If none apply, returns 0.
    """
    date = date.year
    if (start - 5) <= date and date < start:
        return 1
    if start <= date and date < finish:
        return 2
    if finish <= date and date <= finish + 5:
        return 3
    return 0


def process_war(index: int, dates: pd.Series, wars: pd.DataFrame) -> pd.Series:
    """
    Processes a single war from the wars DataFrame at the given index,
    returning a pandas Series that represents where each index average
    entry is in relationship to the start and end dates of the war.
    """
    start = wars.loc[index, 'Start']
    finish = wars.loc[index, 'Finish']
    return dates.apply(lambda x: process_entry(x, start, finish))


def set_stocks() -> pd.Series:
    """
    Sets up the necessary stock data by adjusting the GDP-weighted average from
    ./datasets/stocks/processed/averaged.csv for inflation and returning it
    as a mean resampled by week as a pandas Series.
    """
    stocks = time_series('averaged', 'stocks/processed/', concat=False)
    stocks.sort_index(inplace=True)
    inflation = time_series('inflation_ratios', col='Unnamed: 0', concat=False)
    adj_avg = pd.Series(stocks.index).apply(lambda x: inflation_adjust(x,
                                            'Average', stocks, inflation))
    adj_avg.index = stocks.index
    adj_avg.name = 'Adjusted Average'
    return adj_avg.resample('7D').mean()


def set_wars() -> pd.DataFrame:
    """
    Sets up the necessary wars data by converting dtypes where necessary and
    trimming unnecessary columns, returning the requisite table as a pandas
    DataFrame.
    """
    input_csv = input('Which csv do you want to use for wars? ')
    wars = pd.read_csv('./datasets/' + input_csv + '.csv')
    if wars.loc[0, 'Start'] == 2023:
        wars: pd.DataFrame = wars.loc[1:]
    wars['Start'] = wars['Start'].astype(int)
    wars['Finish'] = wars['Finish'].astype(int)
    return wars.loc[:, wars.columns != 'Unnamed: 0']


def main():
    stocks = set_stocks()
    wars = set_wars()

    dates = pd.Series(stocks.index)
    wars_index = pd.Series(wars.index).astype(int)

    df = wars_index.apply(lambda i: process_war(i, dates, wars)).T
    df.columns = wars['Name of Conflict']
    df.index = stocks.index
    final = pd.DataFrame(stocks).merge(df, left_index=True, right_index=True)
    filename = input('What do you want the name of the generated csv to be? ')
    final.to_csv('./datasets/' + filename + '.csv')


if __name__ == '__main__':
    main()
