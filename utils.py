import pandas as pd


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


def html_to_csv(filename: str, elib: str = '', blib: str = '') -> pd.DataFrame:
    """
    Transforms an html file from the datasets/html_tables folder into a csv.
    The filename will be the name of the file alone & the libraries will be the
    internal folders (e.g. 'stocks/raw/').
    """
    with open('./datasets/html_tables/' + blib + filename + '.html') as f:
        df_arr = pd.read_html(f.read())
        df = pd.DataFrame(df_arr[0])
        if isinstance(df.columns, pd.MultiIndex):
            for _ in range(len(df.columns.names) - 1):
                df.columns = df.columns.droplevel()
        df.to_csv('./datasets/' + elib + filename + '.csv')
