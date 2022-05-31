import os
import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup


def time_series(filename: str, lib: str = '', col: str = 'Date',
                concat: bool = True) -> pd.DataFrame:
    """
    Transforms a csv from the datasets folder into a Time Series as a pandas
    dataframe. The filename will be the name of the file alone without the
    csv extension, the library will be the internal folder (e.g. 'stocks/raw/')
    and concat represents whether or not to associate the names of the columns
    with the file.
    """
    path = './datasets/' + lib + filename + '.csv'
    df = index_parse(pd.read_csv(path))
    df[col] = pd.to_datetime(df[col])
    df = df.set_index(col)
    df = df.loc[:, df.columns != 'Unnamed: 0']
    if concat:
        df.columns = [(filename + ' ' + col) for col in df.columns]
    return df


def html_to_csv(filename: str, elib: str = '', blib: str = ''):
    """
    Transforms an html file from the datasets/html_tables folder into a csv.
    The filename will be the name of the file alone & the libraries will be the
    internal folders (e.g. 'stocks/raw/').
    """
    with open('./datasets/html_tables/' + blib + filename + '.html') as f:
        df_arr = pd.read_html(f.read())
        df = index_parse(pd.DataFrame(df_arr[0]))
        df.to_csv('./datasets/' + elib + filename + '.csv')


def web_tables(url: str, name: str, lib: str = '', bounds: tuple = (0, 0)):
    """
    Given a web url containing some html tables, concatenates the occurrences
    within a range given by the tuple bounds (inclusive on low, exclusive on
    high) into a single table, then saved as a csv within the library datasets
    in a subfolder given by lib with a filename given by name. If bounds is
    not given, concatenates all occurences together.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    tables = soup.find_all('table')
    if bounds == (0, 0):
        bounds = (0, len(tables))
    df_lists = [pd.read_html(str(tables[i]))
                for i in range(bounds[0], bounds[1])]
    df = pd.concat([index_parse(df_list[0]) for df_list in df_lists])
    df.to_csv('./datasets/' + lib + name + '.csv')


def index_parse(df: pd.DataFrame) -> pd.DataFrame:
    """
    Deals with MultiIndexes in pandas DataFrames when reading in from a source
    like a website that might contain them because of formatting. Drops all
    rows of the index but the lowest, leaving a standard index, and returns
    the altered DataFrame.w
    """
    if isinstance(df.columns, pd.MultiIndex):
        for _ in range(len(df.columns.names) - 1):
            df.columns = df.columns.droplevel()
    return df


def time_inflation():
    """
    Transforms the consumer price index (CPI) into a csv of multipliers which
    represent the values needed to multiply any quantity unadjusted for
    inflation by to adjust for inflation. Calculated by taking the ratio
    between the CPI at any time and the benchmark 100, then taking its
    reciprocal. Saves this multipliers csv to datasets.
    """
    inflation = time_series('cpi', col='Year', concat=False)
    inflation.loc['2022-01-01', 'May':'Dec'] = np.nan  # Unpublished months
    multipliers = (inflation.astype(float) / 100) ** (-1)
    rearranged = pd.Series()
    for year in multipliers.iterrows():
        rearranged = pd.concat([rearranged, year[1]])
    print(rearranged)
    dates = []  # 1913 first
    for i in range(len(rearranged)):
        year = str(1913 + (i // 12)) + '-'
        month = str((i % 12) + 1)
        if len(month) == 1:
            month = '0' + month
        dates.append(year + month + '-01')
    rearranged = rearranged.set_axis(dates).dropna()
    rearranged.name = 'Multipliers'
    rearranged.to_csv('./datasets/inflation_ratios.csv')


def inflation_adjust(df: pd.DataFrame, col: str) -> pd.Series:
    """
    Adjusts any column col in a DataFrame df varying over time for inflation
    by multiplying the column through by the associated multipliers (reciprocal
    of the ratio between CPI at a given time and 100). If no multiplier exists
    for a time in the column, will give NaN for that timeframe. The change is
    not inplace, so returns a new pandas Series.
    """
    if 'inflation_ratios.csv' not in os.listdir('./datasets/'):
        time_inflation()
    inflation = time_series('inflation_ratios', col='Unnamed: 0', concat=False)
    adj = dict()
    for date in df.iterrows():
        date = str(date[0]).split()[0]
        try:
            adj[date] = df.loc[date, col] * inflation.loc[date[:-3] + '-01']
        except KeyError:
            adj[date] = np.nan
    result = pd.Series(adj, index=None, dtype=float)
    result.name = col + ' Adjusted'
    return result
