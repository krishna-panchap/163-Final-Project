"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Insert documentation here.
"""

# used for type annotation
from typing import Iterable
import pandas as pd
import os


def time_series(filename: str) -> pd.DataFrame:
    """
    Transforms a single csv representing historical data for a stock given by a
    str filename into a Time Series, returning the DataFrame.
    """
    path = './datasets/stocks/' + filename + '.csv'
    df = pd.read_csv(path, index_col='Date', parse_dates=True)
    df = df.loc[:, df.columns != 'Unnamed: 0']
    df.columns = [(filename + ' ' + col) for col in df.columns]
    return df


def joins(stocks: Iterable[str]) -> pd.DataFrame:
    """
    Joins together all the data in csvs whose file names are given by a
    nonempty Iterable of str stocks, returning the resultant DataFrame.
    """
    df = time_series(stocks[0])
    for i in range(1, len(stocks)):
        df = df.merge(time_series(stocks[i]), how='outer',
                      left_on='Date', right_on='Date')
    return df


def main():
    names = [stock.split('.')[0] for stock in os.listdir('./datasets/stocks')]
    stocks = joins(names)
    stocks.to_csv('./datasets/merged_stocks.csv')
    closings = stocks.loc[:, [('Adj Close' in col) for col in stocks.columns]]
    closings.columns = [col.split()[0] for col in closings.columns]
    closings.to_csv('./datasets/closing_prices.csv')


if __name__ == '__main__':
    main()
