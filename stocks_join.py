"""
Krishna Panchapagesan, Mark Pock
CSE 163 Final Project

Creates a master CSV containing all the data for the major indices we use.
Pares that CSV down to adjusted closing prices and proceeds to create
another CSV with the adjusted ratios between the 2010 (immediately after
the end of the Great Recession) values and each value contained in the CSV.
"""

# used for type annotation
from typing import Iterable
from utils import time_series
import pandas as pd
import os


def joins(stocks: Iterable[str]) -> pd.DataFrame:
    """
    Joins together all the data in csvs whose file names are given by a
    nonempty Iterable of str stocks, returning the resultant DataFrame.
    """
    df = time_series(stocks[0], 'stocks/raw/')
    for i in range(1, len(stocks)):
        df = df.merge(time_series(stocks[i], 'stocks/raw/'), how='outer',
                      left_on='Date', right_on='Date')
    return df


def main():
    stocks = joins([stock.split('.')[0] for stock in
                    os.listdir('./datasets/stocks/raw/')])
    stocks.to_csv('./datasets/stocks/processed/merged_stocks.csv')
    closings = stocks.loc[:, [('Adj Close' in col) for col in stocks.columns]]
    closings.columns = [col.split()[0] for col in closings.columns]
    closings.to_csv('./datasets/stocks/processed/closing_prices.csv')

    benchmark = closings.loc['2010-01-04']  # The values of each stock index on
    # the first trading day of 2010, in the immediate aftermath of the Great
    # Recession's end.

    ratios = (closings / benchmark) * 100
    ratios.to_csv('./datasets/stocks/processed/ratios_benchmark.csv')


if __name__ == '__main__':
    main()
