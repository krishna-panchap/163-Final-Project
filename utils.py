import pandas as pd


def time_series(filename: str, lib: str = '') -> pd.DataFrame:
    """
    Transforms a single csv representing historical data for a stock given by a
    str filename into a Time Series, returning the DataFrame.
    """
    path = './datasets/' + lib + filename + '.csv'
    df = pd.read_csv(path, index_col='Date', parse_dates=True)
    df = df.loc[:, df.columns != 'Unnamed: 0']
    df.columns = [(filename + ' ' + col) for col in df.columns]
    return df
