import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import re


def clean_values(date):
    '''
    converts date itended data to year integer
    '''
    date_arr = re.split('[^0-9a-zA-Z]', date)
    max = 0
    for value in date_arr:
        try:
            value = int(value)
            if value > max:
                max = value
        except ValueError:
            pass
    return max


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
    if len(str(df.loc[0, col])) > 4:
        try:
            df[col] = pd.to_datetime(df[col], format='%Y-%m-%d')
        except ValueError:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
    else:
        df[col] = pd.to_datetime(df[col], format='%Y')
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


def inflation_adjust(date: pd.Timestamp, col: str, df: pd.DataFrame,
                     inflation: pd.DataFrame) -> float:
    """
    Adjusts a single value at a given date (from a datetime-like pandas index)
    at a column col in a DataFrame df varying over time for inflation
    by multiplying the value by the associated multiplier (reciprocal
    of the ratio between CPI at a given time and 100). If no multiplier exists
    for a time in the column, will give NaN for that timeframe. Returns the
    new value as a float.
    """
    try:
        mon = str(date.month)
        if len(mon) == 1:
            mon = '0' + mon
        multiplier = float(inflation.loc[str(date.year) + '-' + mon + '-01'])
        value = float(df.loc[date, col])
        return multiplier * value
    except KeyError:
        return np.nan
