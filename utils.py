import pandas as pd
import requests
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
    df = pd.read_csv(path, index_col=col, parse_dates=True)
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
    in a subfolder given by lib with a filename given by name.
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


def index_parse(df: pd.DataFrame):
    if isinstance(df.columns, pd.MultiIndex):
        for _ in range(len(df.columns.names) - 1):
            df.columns = df.columns.droplevel()
    return df
